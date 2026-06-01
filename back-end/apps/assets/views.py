import logging

from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apps.common.permissions import IsAuthenticated
from apps.common.response import error, success

from .models import Asset
from .serializers import AssetSerializer

logger = logging.getLogger("blindbox")


@method_decorator(csrf_exempt, name="dispatch")
class CSRFExemptView(APIView):
    pass


class AssetListView(CSRFExemptView):
    """资产列表"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Asset.objects.filter(user=request.user)
        return success(data=AssetSerializer(qs, many=True).data)


class AssetDetailView(CSRFExemptView):
    """资产详情"""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            asset = Asset.objects.get(pk=pk, user=request.user)
        except Asset.DoesNotExist:
            return error(message="资产不存在", http_status=404)
        return success(data=AssetSerializer(asset).data)


class AssetRecycleView(CSRFExemptView):
    """资产回收（返还积分）"""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            asset = Asset.objects.get(pk=pk, user=request.user)
        except Asset.DoesNotExist:
            return error(message="资产不存在", http_status=404)

        if asset.status != Asset.Status.AVAILABLE:
            return error(message="当前状态不可回收", http_status=400)

        from apps.points.models import PointsAccount, PointsRecord

        try:
            with transaction.atomic():
                account = PointsAccount.objects.select_for_update().get(user=request.user)
                account.balance += asset.recyclable_points
                account.save(update_fields=["balance"])

                asset.status = Asset.Status.RECYCLED
                asset.save(update_fields=["status"])

                PointsRecord.objects.create(
                    user=request.user,
                    type=PointsRecord.RecordType.RECYCLE_RETURN,
                    amount=asset.recyclable_points,
                    balance=account.balance,
                    description=f"回收{asset.product_name}",
                    related_id=str(asset.pk),
                )
        except PointsAccount.DoesNotExist:
            return error(message="积分账户不存在", http_status=400)
        except Exception:
            logger.exception("回收失败")
            return error(message="回收失败，请稍后重试", http_status=500)

        return success(data={"recycledPoints": asset.recyclable_points}, message="回收成功")


class AssetShipView(CSRFExemptView):
    """申请发货"""

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
    """发布换物"""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            asset = Asset.objects.get(pk=pk, user=request.user)
        except Asset.DoesNotExist:
            return error(message="资产不存在", http_status=404)

        if asset.status != Asset.Status.AVAILABLE:
            return error(message="当前状态不可换物", http_status=400)

        asset.status = Asset.Status.EXCHANGE_PUBLISHED
        asset.save(update_fields=["status"])

        return success(message="发布成功")
