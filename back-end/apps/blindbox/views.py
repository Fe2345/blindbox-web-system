import logging
import random
import uuid
from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apps.common.permissions import IsAdmin, IsAuthenticated
from apps.common.response import error, flatten_errors, success
from apps.common.valuation import resolve_estimated_points, resolve_recyclable_points

from .models import BlindBox, DrawRecord, Prize
from .probabilities import calculate_prize_probabilities, probability_to_weight
from .serializers import (
    AdminBlindBoxSerializer,
    BlindBoxSerializer,
    BlindBoxStatusSerializer,
    BlindBoxWriteSerializer,
    DrawRecordSerializer,
    DrawResultSerializer,
    PrizeWriteSerializer,
)

logger = logging.getLogger("blindbox")


@method_decorator(csrf_exempt, name="dispatch")
class CSRFExemptView(APIView):
    pass


class BlindBoxListView(CSRFExemptView):
    def get(self, request):
        now = timezone.now()
        qs = BlindBox.objects.filter(
            status=BlindBox.Status.ACTIVE,
            start_time__lte=now,
            end_time__gte=now,
        ).prefetch_related("prizes")
        category = request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        keyword = request.query_params.get("keyword")
        if keyword:
            qs = qs.filter(name__icontains=keyword)
        return success(data=BlindBoxSerializer(qs, many=True).data)


class BlindBoxDetailView(CSRFExemptView):
    def get(self, request, pk):
        try:
            box = BlindBox.objects.prefetch_related("prizes").get(pk=pk)
        except BlindBox.DoesNotExist:
            return error(message="盲盒不存在", http_status=404)
        return success(data=BlindBoxSerializer(box).data)


class DrawView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            draw_count = int(request.data.get("count", 1))
        except (TypeError, ValueError):
            return error(message="抽取次数不正确", http_status=400)
        if draw_count not in [1, 5, 10]:
            return error(message="仅支持单抽、五连抽和十连抽", http_status=400)

        try:
            box = BlindBox.objects.prefetch_related("prizes").get(pk=pk)
        except BlindBox.DoesNotExist:
            return error(message="盲盒不存在", http_status=404)

        now = timezone.now()
        if box.status != BlindBox.Status.ACTIVE:
            return error(message="盲盒未上架", http_status=400)
        if now < box.start_time or now > box.end_time:
            return error(message="不在活动时间内", http_status=400)
        if draw_count > box.max_draw_count:
            return error(message=f"单次最多只能抽取 {box.max_draw_count} 次", http_status=400)

        from apps.points.models import PointsAccount
        try:
            account = PointsAccount.objects.get(user=user)
        except PointsAccount.DoesNotExist:
            return error(message="积分账户不存在", http_status=400)

        total_cost = box.cost_points * draw_count
        if account.balance < total_cost:
            return error(message="积分不足", http_status=400)

        active_prizes = box.prizes.filter(is_active=True, remaining_quantity__gt=0)
        if not active_prizes.exists():
            return error(message="奖品已抽完", http_status=400)
        if sum(p.remaining_quantity for p in active_prizes) < draw_count:
            return error(message="奖品库存不足，无法完成本次连抽", http_status=400)

        batch_no = f"B{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"

        try:
            with transaction.atomic():
                from apps.assets.models import Asset
                from apps.points.models import PointsRecord

                account = PointsAccount.objects.select_for_update().get(pk=account.pk)
                if account.balance < total_cost:
                    return error(message="积分不足", http_status=400)
                account.balance -= total_cost
                account.save(update_fields=["balance"])

                records = []
                for _ in range(draw_count):
                    available_prizes = list(
                        Prize.objects
                        .select_for_update()
                        .filter(blindbox=box, is_active=True, remaining_quantity__gt=0)
                    )
                    prize = self._pick_prize(available_prizes)
                    if prize is None:
                        raise ValueError("抽奖失败，请重试")

                    prize.remaining_quantity -= 1
                    prize.save(update_fields=["remaining_quantity"])

                    estimated_points = resolve_estimated_points(prize, box.cost_points)
                    recyclable_points = resolve_recyclable_points(prize, box.cost_points)
                    asset = Asset.objects.create(
                        user=user,
                        product=prize.product,
                        product_name=prize.name,
                        product_image=prize.image,
                        category=box.category,
                        rarity=prize.rarity,
                        description=f"来自{box.name}",
                        source_type=Asset.SourceType.BLINDBOX,
                        source_name=box.name,
                        obtained_at=now,
                        estimated_points=estimated_points,
                        recyclable_points=recyclable_points,
                    )

                    records.append(DrawRecord.objects.create(
                        user=user,
                        blindbox=box,
                        prize=prize,
                        asset=asset,
                        prize_name=prize.name,
                        prize_image=prize.image,
                        rarity=prize.rarity,
                        ip_name_snapshot=prize.ip_name_snapshot,
                        cost_points=box.cost_points,
                        remaining_points=account.balance,
                        batch_no=batch_no,
                        draw_type=DrawRecord.DrawType.REAL,
                        draw_status=DrawRecord.DrawStatus.SUCCESS,
                    ))

                PointsRecord.objects.create(
                    user=user,
                    type=PointsRecord.RecordType.BLINDBOX_CONSUME,
                    amount=-total_cost,
                    balance=account.balance,
                    description=f"抽取{box.name} x{draw_count}",
                    related_id=batch_no,
                )
        except ValueError as e:
            return error(message=str(e), http_status=400)
        except Exception:
            logger.exception("抽取失败")
            return error(message="抽取失败，请稍后重试", http_status=500)

        if draw_count == 1:
            return success(data=DrawResultSerializer(records[0]).data)
        return success(data={
            "batchNo": batch_no,
            "count": draw_count,
            "totalCostPoints": total_cost,
            "remainingPoints": account.balance,
            "blindBoxId": box.pk,
            "blindBoxName": box.name,
            "results": DrawResultSerializer(records, many=True).data,
        })

    @staticmethod
    def _pick_prize(prizes):
        total = sum(p.probability for p in prizes)
        if total <= 0:
            return None
        rand = Decimal(str(random.random())) * Decimal(total)
        cumulative = Decimal("0")
        for prize in prizes:
            cumulative += prize.probability
            if rand < cumulative:
                return prize
        return prizes[-1] if prizes else None


class AdminBlindBoxListView(CSRFExemptView):
    permission_classes = [IsAdmin]

    def get(self, request):
        qs = BlindBox.objects.prefetch_related("prizes").all()
        status = request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        keyword = request.query_params.get("keyword")
        if keyword:
            qs = qs.filter(name__icontains=keyword)
        return success(data=AdminBlindBoxSerializer(qs, many=True).data)


class AdminBlindBoxCreateView(CSRFExemptView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = BlindBoxWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        data = serializer.validated_data
        box = BlindBox.objects.create(
            name=data["name"],
            cover=data["cover"],
            description=data.get("description", ""),
            category=data["category"],
            ip_name=data.get("ip_name", ""),
            cost_points=data["cost_points"],
            status=data.get("status", BlindBox.Status.INACTIVE),
            start_time=data["start_time"],
            end_time=data["end_time"],
            max_draw_count=data.get("max_draw_count", 10),
            allow_simulation=data.get("allow_simulation", True),
            sort_order=data.get("sort_order", 0),
        )
        return success(data=AdminBlindBoxSerializer(box).data)


class AdminBlindBoxDetailView(CSRFExemptView):
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        try:
            box = BlindBox.objects.prefetch_related("prizes").get(pk=pk)
        except BlindBox.DoesNotExist:
            return error(message="盲盒不存在", http_status=404)
        return success(data=AdminBlindBoxSerializer(box).data)

    def put(self, request, pk):
        try:
            box = BlindBox.objects.get(pk=pk)
        except BlindBox.DoesNotExist:
            return error(message="盲盒不存在", http_status=404)

        serializer = BlindBoxWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        data = serializer.validated_data
        box.name = data["name"]
        box.cover = data["cover"]
        box.description = data.get("description", "")
        box.category = data["category"]
        box.ip_name = data.get("ip_name", "")
        box.cost_points = data["cost_points"]
        box.status = data.get("status", box.status)
        box.start_time = data["start_time"]
        box.end_time = data["end_time"]
        box.max_draw_count = data.get("max_draw_count", box.max_draw_count)
        box.allow_simulation = data.get("allow_simulation", box.allow_simulation)
        box.sort_order = data.get("sort_order", box.sort_order)
        box.save()
        return success(data=AdminBlindBoxSerializer(box).data)


class AdminBlindBoxStatusView(CSRFExemptView):
    permission_classes = [IsAdmin]

    def put(self, request, pk):
        try:
            box = BlindBox.objects.get(pk=pk)
        except BlindBox.DoesNotExist:
            return error(message="盲盒不存在", http_status=404)

        serializer = BlindBoxStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        box.status = serializer.validated_data["status"]
        box.save(update_fields=["status"])
        return success(data=AdminBlindBoxSerializer(box).data)


class AdminPrizePoolView(CSRFExemptView):
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            box = BlindBox.objects.get(pk=pk)
        except BlindBox.DoesNotExist:
            return error(message="盲盒不存在", http_status=404)

        prizes_data = request.data.get("prizes")
        if not isinstance(prizes_data, list):
            return error(message="prizes 必须是数组", http_status=400)

        validated = []
        for item in prizes_data:
            serializer = PrizeWriteSerializer(data=item)
            if not serializer.is_valid():
                return error(message=flatten_errors(serializer.errors), http_status=400)
            validated.append(serializer.validated_data)

        try:
            calculated_probabilities = calculate_prize_probabilities(validated, box.cost_points)
        except ValueError as exc:
            return error(message=str(exc), http_status=400)

        with transaction.atomic():
            existing_ids = {item.get("id") for item in validated if item.get("id")}
            box.prizes.exclude(pk__in=existing_ids).delete()

            for item, calculated_probability in zip(validated, calculated_probabilities):
                prize_id = item.get("id")
                if prize_id:
                    try:
                        prize = Prize.objects.get(pk=prize_id, blindbox=box)
                    except Prize.DoesNotExist:
                        continue
                    prize.name = item["name"]
                    prize.image = item["image"]
                    prize.rarity = item["rarity"]
                    prize.probability = calculated_probability
                    prize.weight = probability_to_weight(calculated_probability)
                    prize.quantity = item.get("quantity", 0)
                    prize.remaining_quantity = item.get("remaining_quantity", 0)
                    prize.is_active = item.get("is_active", True)
                    prize.ip_name_snapshot = item.get("ip_name_snapshot", "")
                    if item.get("product_id"):
                        prize.product_id = item["product_id"]
                    prize.save()
                else:
                    Prize.objects.create(
                        blindbox=box,
                        name=item["name"],
                        image=item["image"],
                        rarity=item["rarity"],
                        probability=calculated_probability,
                        weight=probability_to_weight(calculated_probability),
                        quantity=item.get("quantity", 0),
                        remaining_quantity=item.get("remaining_quantity", 0),
                        is_active=item.get("is_active", True),
                        ip_name_snapshot=item.get("ip_name_snapshot", ""),
                        product_id=item.get("product_id"),
                    )

        box.refresh_from_db()
        return success(data=AdminBlindBoxSerializer(box).data)


class AdminDrawRecordListView(CSRFExemptView):
    permission_classes = [IsAdmin]

    def get(self, request):
        qs = DrawRecord.objects.select_related("blindbox").all()
        blindbox_id = request.query_params.get("blindbox_id")
        if blindbox_id:
            qs = qs.filter(blindbox_id=blindbox_id)
        draw_type = request.query_params.get("draw_type")
        if draw_type:
            qs = qs.filter(draw_type=draw_type)
        return success(data=DrawRecordSerializer(qs[:50], many=True).data)
