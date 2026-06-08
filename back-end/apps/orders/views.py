import logging

from django.db import transaction
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apps.assets.models import Asset
from apps.common.permissions import IsAuthenticated
from apps.common.response import error, success

from .models import Order
from .serializers import OrderSerializer

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
