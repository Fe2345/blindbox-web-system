import logging
import uuid
from collections import defaultdict

from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apps.common.permissions import IsAuthenticated
from apps.common.response import error, success
from apps.common.valuation import recycle_points_for_value

from .models import Asset
from .serializers import AssetSerializer

logger = logging.getLogger("blindbox")


@method_decorator(csrf_exempt, name="dispatch")
class CSRFExemptView(APIView):
    pass


class AssetListView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Asset.objects.filter(user=request.user)
        return success(data=AssetSerializer(qs, many=True).data)


class AssetDetailView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            asset = Asset.objects.get(pk=pk, user=request.user)
        except Asset.DoesNotExist:
            return error(message="资产不存在", http_status=404)
        return success(data=AssetSerializer(asset).data)


class AssetRecycleView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        result, err = recycle_assets(request.user, Asset.objects.filter(pk=pk))
        if err:
            return err
        return success(data=result, message="回收成功")


class AssetBulkRecycleView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        qs = Asset.objects.filter(user=request.user, status=Asset.Status.AVAILABLE)

        asset_ids = request.data.get("assetIds") or request.data.get("asset_ids")
        if asset_ids:
            qs = qs.filter(pk__in=asset_ids)

        rarities = request.data.get("rarities") or []
        if rarities:
            qs = qs.filter(rarity__in=rarities)

        product_name = request.data.get("productName") or request.data.get("product_name")
        if product_name:
            qs = qs.filter(product_name=product_name)

        source_batch_no = request.data.get("sourceBatchNo") or request.data.get("source_batch_no")
        if source_batch_no:
            qs = qs.filter(draw_records__batch_no=source_batch_no)

        assets = list(qs.select_related("product").order_by("-obtained_at", "-id").distinct())
        if request.data.get("keepOneByProduct") or request.data.get("keep_one_by_product"):
            assets = keep_one_per_product(assets)

        result, err = recycle_assets(request.user, assets)
        if err:
            return err
        return success(data=result, message="批量回收成功")


class AssetShipView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            asset = Asset.objects.get(pk=pk, user=request.user)
        except Asset.DoesNotExist:
            return error(message="资产不存在", http_status=404)

        if asset.status != Asset.Status.AVAILABLE:
            return error(message="当前状态不可发货", http_status=400)

        asset.status = Asset.Status.PENDING_SHIPMENT
        asset.save(update_fields=["status"])
        return success(message="发货申请已提交")


class AssetPublishExchangeView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            with transaction.atomic():
                asset = Asset.objects.select_for_update().get(pk=pk, user=request.user)
                if asset.status != Asset.Status.AVAILABLE:
                    return error(message="????????", http_status=400)

                from apps.exchange.models import ExchangePost
                from apps.exchange.serializers import ExchangePostSerializer

                active_post_exists = ExchangePost.objects.filter(
                    asset=asset,
                    status__in=[ExchangePost.Status.PUBLISHED, ExchangePost.Status.LOCKED],
                ).exists()
                if active_post_exists:
                    return error(message="??????????", http_status=400)

                asset.status = Asset.Status.EXCHANGE_PUBLISHED
                asset.save(update_fields=["status", "updated_at"])

                post = ExchangePost.objects.create(
                    user=request.user,
                    asset=asset,
                    asset_name=asset.product_name,
                    asset_image=asset.product_image,
                    asset_rarity=asset.rarity,
                    asset_category=asset.category,
                    expect_description=request.data.get("expectDescription") or request.data.get("expect_description") or "",
                    remark=request.data.get("remark", ""),
                    status=ExchangePost.Status.PUBLISHED,
                )
        except Asset.DoesNotExist:
            return error(message="?????", http_status=404)

        return success(data=ExchangePostSerializer(post).data, message="????")


def keep_one_per_product(assets):
    groups = defaultdict(list)
    for asset in assets:
        groups[(asset.product_id, asset.product_name)].append(asset)

    recyclable = []
    for group_assets in groups.values():
        recyclable.extend(group_assets[1:])
    return recyclable


def recycle_assets(user, assets_or_qs):
    assets = list(assets_or_qs)
    if not assets:
        return None, error(message="没有可回收的资产", http_status=400)

    for asset in assets:
        if asset.user_id != user.id:
            return None, error(message="资产不存在", http_status=404)
        if asset.status != Asset.Status.AVAILABLE:
            return None, error(message=f"{asset.product_name} 当前状态不可回收", http_status=400)

    from apps.points.models import PointsAccount, PointsRecord, TransactionRecord

    try:
        with transaction.atomic():
            account = PointsAccount.objects.select_for_update().get(user=user)
            locked_assets = list(
                Asset.objects
                .select_for_update()
                .select_related("product")
                .filter(pk__in=[asset.pk for asset in assets], user=user)
            )

            total_points = 0
            recycled_ids = []
            names = []
            for asset in locked_assets:
                if asset.status != Asset.Status.AVAILABLE:
                    return None, error(message=f"{asset.product_name} 当前状态不可回收", http_status=400)
                recycle_points = resolve_recycle_points(asset)
                total_points += recycle_points
                recycled_ids.append(asset.pk)
                names.append(asset.product_name)

                asset.status = Asset.Status.RECYCLED
                if asset.recyclable_points != recycle_points:
                    asset.recyclable_points = recycle_points
                    asset.save(update_fields=["status", "recyclable_points"])
                else:
                    asset.save(update_fields=["status"])

                TransactionRecord.objects.create(
                    user=user,
                    type=TransactionRecord.RecordType.RECYCLE,
                    description=f"回收{asset.product_name}",
                    related_asset_name=asset.product_name,
                    status_change="available -> recycled",
                )

            account.balance += total_points
            account.save(update_fields=["balance"])

            description = names[0] if len(names) == 1 else f"批量回收{len(names)}件资产"
            PointsRecord.objects.create(
                user=user,
                type=PointsRecord.RecordType.RECYCLE_RETURN,
                amount=total_points,
                balance=account.balance,
                description=description,
                related_id=f"RB{uuid.uuid4().hex[:12].upper()}",
            )
    except PointsAccount.DoesNotExist:
        return None, error(message="积分账户不存在", http_status=400)
    except Exception:
        logger.exception("回收失败")
        return None, error(message="回收失败，请稍后重试", http_status=500)

    return {
        "recycledCount": len(recycled_ids),
        "recycledAssetIds": recycled_ids,
        "recycledPoints": total_points,
        "balance": account.balance,
    }, None


def resolve_recycle_points(asset):
    if asset.recyclable_points > 0:
        return asset.recyclable_points

    estimated_points = asset.estimated_points
    if estimated_points <= 0 and asset.product_id:
        estimated_points = asset.product.estimated_points

    return recycle_points_for_value(estimated_points, asset.rarity) if estimated_points > 0 else 0
