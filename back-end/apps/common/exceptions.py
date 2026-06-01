import logging

from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    NotFound,
    ParseError,
    PermissionDenied,
    ValidationError,
)
from rest_framework.views import exception_handler as drf_exception_handler

from apps.common.response import error

logger = logging.getLogger("blindbox")


def _first_message(detail):
    """从 DRF 的 detail 结构（列表/字典）中提取第一条消息"""
    if isinstance(detail, list):
        return str(detail[0])
    if isinstance(detail, dict):
        key = next(iter(detail))
        val = detail[key]
        if isinstance(val, list):
            return f"{key}: {val[0]}"
        return f"{key}: {val}"
    return str(detail)


def custom_exception_handler(exc, context):
    """统一异常响应 {code, message, data}"""
    response = drf_exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
            return error(message="请先登录", http_status=401)
        elif isinstance(exc, PermissionDenied):
            return error(message="没有权限执行此操作", http_status=403)
        elif isinstance(exc, NotFound):
            return error(message="资源不存在", http_status=404)
        elif isinstance(exc, (ValidationError, ParseError)):
            return error(message=_first_message(exc.detail), http_status=400)
        elif isinstance(exc, APIException):
            return error(message=str(exc.detail), http_status=exc.status_code)
        else:
            return error(message="请求处理错误", http_status=response.status_code)
    else:
        logger.exception("未处理的异常: %s", exc)
        return error(message="服务器内部错误", http_status=500)
