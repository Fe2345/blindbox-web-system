from rest_framework.views import APIView
from django.db import transaction

from apps.common.permissions import IsAuthenticated
from apps.common.response import error, flatten_errors, success

from .models import PointsAccount, PointsRecord, TransactionRecord
from .serializers import PointsRechargeSerializer, PointsRecordSerializer, TransactionRecordSerializer


RECHARGE_RATE = 100


class PointsBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account, _ = PointsAccount.objects.get_or_create(
            user=request.user,
            defaults={"balance": 0},
        )
        return success(data={"balance": account.balance})


class PointsRecordListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = PointsRecord.objects.filter(user=request.user)
        record_type = request.query_params.get("type")
        if record_type:
            qs = qs.filter(type=record_type)
        return success(data=PointsRecordSerializer(qs, many=True).data)


class PointsRechargeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PointsRechargeSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        amount_yuan = serializer.validated_data["amount_yuan"]
        points = int(amount_yuan * RECHARGE_RATE)
        if points <= 0:
            return error(message="充值金额不正确", http_status=400)

        with transaction.atomic():
            account, _ = PointsAccount.objects.select_for_update().get_or_create(
                user=request.user,
                defaults={"balance": 0},
            )
            account.balance += points
            account.save(update_fields=["balance", "updated_at"])
            record = PointsRecord.objects.create(
                user=request.user,
                type=PointsRecord.RecordType.RECHARGE,
                amount=points,
                balance=account.balance,
                description=f"积分充值：{amount_yuan} 元兑换 {points} 积分",
                related_id=f"RECHARGE-{record_id_seed(request.user.id)}",
            )

        return success(data={
            "balance": account.balance,
            "amountYuan": amount_yuan,
            "points": points,
            "record": PointsRecordSerializer(record).data,
        })


class TransactionRecordListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = TransactionRecord.objects.filter(user=request.user)
        record_type = request.query_params.get("type")
        if record_type:
            qs = qs.filter(type=record_type)
        return success(data=TransactionRecordSerializer(qs, many=True).data)


def record_id_seed(user_id):
    from django.utils import timezone

    return f"{timezone.now().strftime('%Y%m%d%H%M%S')}-{user_id}"
