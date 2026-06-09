import logging

from django.db import transaction
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apps.assets.models import Asset
from apps.common.permissions import IsAdmin, IsAuthenticated
from apps.common.response import error, flatten_errors, success

from .models import Order
from .serializers import AdminOrderSerializer, AdminOrderShipSerializer, OrderSerializer

logger = logging.getLogger("blindbox")


@method_decorator(csrf_exempt, name="dispatch")
class CSRFExemptView(APIView):
    pass


class OrderListView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Order.objects.select_related("asset").filter(user=request.user)
        return success(data=OrderSerializer(qs, many=True).data)


class OrderDetailView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.select_related("asset").get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return error(message="订单不存在", http_status=404)
        return success(data=OrderSerializer(order).data)


class OrderConfirmView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().select_related("asset").get(pk=pk, user=request.user)
                if order.status != Order.Status.SHIPPED:
                    return error(message="当前订单不能确认收货", http_status=400)

                order.status = Order.Status.COMPLETED
                order.completed_at = timezone.now()
                order.save(update_fields=["status", "completed_at"])

                asset = order.asset
                asset.status = Asset.Status.COMPLETED
                asset.save(update_fields=["status"])
        except Order.DoesNotExist:
            return error(message="订单不存在", http_status=404)
        except Exception:
            logger.exception("确认收货失败")
            return error(message="确认收货失败，请稍后重试", http_status=500)

        return success(message="确认收货成功")


# ==================== 管理端 ====================


class AdminOrderListView(CSRFExemptView):
    """订单列表（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        qs = Order.objects.select_related("user").all().order_by("-created_at")
        status = request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        order_type = request.query_params.get("type")
        if order_type:
            qs = qs.filter(type=order_type)
        return success(data=AdminOrderSerializer(qs[:100], many=True).data)


class AdminOrderShipView(CSRFExemptView):
    """订单发货（管理端）"""

    permission_classes = [IsAdmin]

    def post(self, request, pk):
        serializer = AdminOrderShipSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        company = serializer.validated_data["company"]
        tracking_no = serializer.validated_data["trackingNo"]

        with transaction.atomic():
            try:
                order = Order.objects.select_for_update().get(pk=pk, status=Order.Status.PENDING)
            except Order.DoesNotExist:
                return error(message="订单不存在或不在待处理状态", http_status=404)

            order.logistics_company = company
            order.tracking_no = tracking_no
            order.shipped_at = timezone.now()
            order.status = Order.Status.SHIPPED
            order.save(update_fields=["logistics_company", "tracking_no", "shipped_at", "status"])

            # 同步更新资产状态
            if order.asset:
                order.asset.status = Asset.Status.SHIPPED
                order.asset.save(update_fields=["status"])

            # 同步更新商家发货任务状态
            from apps.merchant.models import ShipmentTask
            ShipmentTask.objects.filter(
                order_no=order.order_no, status=ShipmentTask.Status.PENDING
            ).update(
                logistics_company=company,
                tracking_no=tracking_no,
                shipped_at=timezone.now(),
                status=ShipmentTask.Status.SHIPPED,
            )

        return success(data=AdminOrderSerializer(order).data)
