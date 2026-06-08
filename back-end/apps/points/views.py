from rest_framework.views import APIView

from apps.common.permissions import IsAuthenticated
from apps.common.response import success

from .models import PointsAccount, PointsRecord, TransactionRecord
from .serializers import PointsRecordSerializer, TransactionRecordSerializer


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


class TransactionRecordListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = TransactionRecord.objects.filter(user=request.user)
        record_type = request.query_params.get("type")
        if record_type:
            qs = qs.filter(type=record_type)
        return success(data=TransactionRecordSerializer(qs, many=True).data)
