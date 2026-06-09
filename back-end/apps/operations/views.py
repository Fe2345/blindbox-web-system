from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apps.common.permissions import IsAdmin
from apps.common.response import success, error, flatten_errors

from .models import RuleConfig, OpLog, ExceptionRecord, TransactionLedger
from .serializers import (
    RuleConfigSerializer,
    RuleConfigWriteSerializer,
    OpLogSerializer,
    ExceptionRecordSerializer,
    ExceptionResolveSerializer,
    TransactionLedgerSerializer,
)


class CSRFExemptView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AdminRuleConfigView(CSRFExemptView):
    """规则配置（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        config = RuleConfig.get()
        return success(data=RuleConfigSerializer(config).data)

    def post(self, request):
        config = RuleConfig.get()
        serializer = RuleConfigWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        for field, value in serializer.validated_data.items():
            setattr(config, field, value)
        config.updated_by = request.user.username
        updated_fields = list(serializer.validated_data.keys()) + ["updated_by"]
        config.save(update_fields=updated_fields)
        return success(data=RuleConfigSerializer(config).data)


class AdminOpLogListView(CSRFExemptView):
    """操作日志列表（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        qs = OpLog.objects.all().order_by("-created_at")[:100]
        return success(data=OpLogSerializer(qs, many=True).data)


class AdminExceptionListView(CSRFExemptView):
    """异常工单列表（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        qs = ExceptionRecord.objects.all().order_by("-created_at")
        status = request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return success(data=ExceptionRecordSerializer(qs[:100], many=True).data)


class AdminExceptionResolveView(CSRFExemptView):
    """异常工单处理（管理端）"""

    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            record = ExceptionRecord.objects.get(pk=pk)
        except ExceptionRecord.DoesNotExist:
            return error(message="工单不存在", http_status=404)

        if record.status == ExceptionRecord.Status.RESOLVED:
            return error(message="工单已解决", http_status=400)

        serializer = ExceptionResolveSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        record.result = serializer.validated_data["result"]
        record.status = ExceptionRecord.Status.RESOLVED
        record.resolved_at = timezone.now()
        record.save(update_fields=["result", "status", "resolved_at"])
        return success(data=ExceptionRecordSerializer(record).data)


class AdminLedgerListView(CSRFExemptView):
    """交易账本列表（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        qs = TransactionLedger.objects.all().order_by("-created_at")
        ledger_type = request.query_params.get("type")
        if ledger_type:
            qs = qs.filter(type=ledger_type)
        try:
            start_date = request.query_params.get("start_date")
            if start_date:
                qs = qs.filter(created_at__date__gte=start_date)
            end_date = request.query_params.get("end_date")
            if end_date:
                qs = qs.filter(created_at__date__lte=end_date)
        except (ValueError, TypeError):
            return error(message="日期格式无效", http_status=400)
        return success(data=TransactionLedgerSerializer(qs[:200], many=True).data)
