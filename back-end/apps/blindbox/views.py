import logging
import random
import uuid

from django.db import transaction
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apps.common.permissions import IsAdmin, IsAuthenticated
from apps.common.response import error, flatten_errors, success

from .models import BlindBox, DrawRecord, Prize
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
    """豁免 CSRF 的 APIView 基类"""
    pass


# ==================== 用户端 ====================


class BlindBoxListView(CSRFExemptView):
    """盲盒列表（用户端）"""

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
    """盲盒详情（用户端）"""

    def get(self, request, pk):
        try:
            box = BlindBox.objects.prefetch_related("prizes").get(pk=pk)
        except BlindBox.DoesNotExist:
            return error(message="盲盒不存在", http_status=404)
        return success(data=BlindBoxSerializer(box).data)


class DrawView(CSRFExemptView):
    """盲盒抽取（核心业务）"""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user

        # 1. 查盲盒
        try:
            box = BlindBox.objects.prefetch_related("prizes").get(pk=pk)
        except BlindBox.DoesNotExist:
            return error(message="盲盒不存在", http_status=404)

        # 2. 校验状态和时间
        now = timezone.now()
        if box.status != BlindBox.Status.ACTIVE:
            return error(message="盲盒未上架", http_status=400)
        if now < box.start_time or now > box.end_time:
            return error(message="不在活动时间内", http_status=400)

        # 3. 校验积分
        from apps.points.models import PointsAccount
        try:
            account = PointsAccount.objects.get(user=user)
        except PointsAccount.DoesNotExist:
            return error(message="积分账户不存在", http_status=400)
        if account.balance < box.cost_points:
            return error(message="积分不足", http_status=400)

        # 4. 获取可用奖品池
        active_prizes = box.prizes.filter(
            is_active=True,
            remaining_quantity__gt=0,
        )
        if not active_prizes.exists():
            return error(message="奖品已抽完", http_status=400)

        # 5. 按概率抽奖
        prize = self._pick_prize(active_prizes)
        if prize is None:
            return error(message="抽奖失败，请重试", http_status=500)

        # 6. 事务：扣积分、减库存、生成资产、写记录
        batch_no = f"B{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"

        try:
            with transaction.atomic():
                # 扣积分（行锁）
                from apps.points.models import PointsRecord
                account = PointsAccount.objects.select_for_update().get(pk=account.pk)
                if account.balance < box.cost_points:
                    return error(message="积分不足", http_status=400)
                account.balance -= box.cost_points
                account.save(update_fields=["balance"])

                # 减库存（行锁防超卖）
                prize = Prize.objects.select_for_update().get(pk=prize.pk)
                if prize.remaining_quantity <= 0:
                    raise ValueError("库存不足")
                prize.remaining_quantity -= 1
                prize.save(update_fields=["remaining_quantity"])

                # 生成资产
                from apps.assets.models import Asset
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
                    estimated_points=0,
                    recyclable_points=0,
                )

                # 写抽取记录
                record = DrawRecord.objects.create(
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
                )

                # 写积分流水
                PointsRecord.objects.create(
                    user=user,
                    type=PointsRecord.RecordType.BLINDBOX_CONSUME,
                    amount=-box.cost_points,
                    balance=account.balance,
                    description=f"抽取{box.name}",
                    related_id=str(record.pk),
                )

        except ValueError as e:
            return error(message=str(e), http_status=400)
        except Exception as e:
            logger.exception("抽取失败")
            return error(message="抽取失败，请稍后重试", http_status=500)

        return success(data=DrawResultSerializer(record).data)

    @staticmethod
    def _pick_prize(prizes):
        """按 probability 权重随机选一个奖品"""
        total = sum(p.probability for p in prizes)
        if total <= 0:
            return None
        rand = random.randint(1, total)
        cumulative = 0
        for p in prizes:
            cumulative += p.probability
            if rand <= cumulative:
                return p
        return prizes.last()


# ==================== 管理端 ====================


class AdminBlindBoxListView(CSRFExemptView):
    """盲盒列表（管理端）"""

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
    """创建盲盒（管理端）"""

    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = BlindBoxWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        d = serializer.validated_data
        box = BlindBox.objects.create(
            name=d["name"],
            cover=d["cover"],
            description=d.get("description", ""),
            category=d["category"],
            ip_name=d.get("ip_name", ""),
            cost_points=d["cost_points"],
            status=d.get("status", "inactive"),
            start_time=d["start_time"],
            end_time=d["end_time"],
            max_draw_count=d.get("max_draw_count", 10),
            allow_simulation=d.get("allow_simulation", True),
            sort_order=d.get("sort_order", 0),
        )
        return success(data=AdminBlindBoxSerializer(box).data)


class AdminBlindBoxDetailView(CSRFExemptView):
    """盲盒详情 / 编辑（管理端）"""

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

        d = serializer.validated_data
        box.name = d["name"]
        box.cover = d["cover"]
        box.description = d.get("description", "")
        box.category = d["category"]
        box.ip_name = d.get("ip_name", "")
        box.cost_points = d["cost_points"]
        box.status = d.get("status", box.status)
        box.start_time = d["start_time"]
        box.end_time = d["end_time"]
        box.max_draw_count = d.get("max_draw_count", box.max_draw_count)
        box.allow_simulation = d.get("allow_simulation", box.allow_simulation)
        box.sort_order = d.get("sort_order", box.sort_order)
        box.save()
        return success(data=AdminBlindBoxSerializer(box).data)


class AdminBlindBoxStatusView(CSRFExemptView):
    """盲盒状态切换（管理端）"""

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
    """奖池配置（管理端）：批量更新某个盲盒的奖品列表"""

    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            box = BlindBox.objects.get(pk=pk)
        except BlindBox.DoesNotExist:
            return error(message="盲盒不存在", http_status=404)

        prizes_data = request.data.get("prizes")
        if not isinstance(prizes_data, list):
            return error(message="prizes 必须是数组", http_status=400)

        # 逐个校验
        validated = []
        for item in prizes_data:
            s = PrizeWriteSerializer(data=item)
            if not s.is_valid():
                return error(message=flatten_errors(s.errors), http_status=400)
            validated.append(s.validated_data)

        # 概率校验
        total_prob = sum(v["probability"] for v in validated)
        if total_prob != 100:
            return error(message=f"概率合计必须为100%，当前为{total_prob}%", http_status=400)

        # 同步更新
        with transaction.atomic():
            existing_ids = {v.get("id") for v in validated if v.get("id")}
            # 删除不在列表中的旧奖品
            box.prizes.exclude(pk__in=existing_ids).delete()

            for item in validated:
                prize_id = item.get("id")
                if prize_id:
                    # 更新已有奖品
                    try:
                        prize = Prize.objects.get(pk=prize_id, blindbox=box)
                    except Prize.DoesNotExist:
                        continue
                    prize.name = item["name"]
                    prize.image = item["image"]
                    prize.rarity = item["rarity"]
                    prize.probability = item["probability"]
                    prize.weight = item.get("weight", 0)
                    prize.quantity = item.get("quantity", 0)
                    prize.remaining_quantity = item.get("remaining_quantity", 0)
                    prize.is_active = item.get("is_active", True)
                    prize.ip_name_snapshot = item.get("ip_name_snapshot", "")
                    if item.get("product_id"):
                        prize.product_id = item["product_id"]
                    prize.save()
                else:
                    # 新增奖品
                    Prize.objects.create(
                        blindbox=box,
                        name=item["name"],
                        image=item["image"],
                        rarity=item["rarity"],
                        probability=item["probability"],
                        weight=item.get("weight", 0),
                        quantity=item.get("quantity", 0),
                        remaining_quantity=item.get("remaining_quantity", 0),
                        is_active=item.get("is_active", True),
                        ip_name_snapshot=item.get("ip_name_snapshot", ""),
                        product_id=item.get("product_id"),
                    )

        box.refresh_from_db()
        return success(data=AdminBlindBoxSerializer(box).data)


class AdminDrawRecordListView(CSRFExemptView):
    """抽取记录列表（管理端）"""

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
