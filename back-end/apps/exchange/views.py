import logging

from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apps.assets.models import Asset
from apps.common.permissions import IsAuthenticated
from apps.common.response import error, success

from .models import ExchangeApplication, ExchangePost
from .serializers import ExchangeApplicationSerializer, ExchangePostSerializer

logger = logging.getLogger("blindbox")


@method_decorator(csrf_exempt, name="dispatch")
class CSRFExemptView(APIView):
    pass


class ExchangePostListView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = ExchangePost.objects.select_related("user", "asset").all()
        return success(data=ExchangePostSerializer(qs, many=True).data)


class ExchangePostDetailView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = ExchangePost.objects.select_related("user", "asset").get(pk=pk)
        except ExchangePost.DoesNotExist:
            return error(message="换物帖子不存在", http_status=404)
        return success(data=ExchangePostSerializer(post).data)


class ExchangeApplyView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        asset_id = request.data.get("assetId") or request.data.get("asset_id")
        remark = request.data.get("remark", "")
        if not asset_id:
            return error(message="请选择用于交换的资产", http_status=400)

        try:
            with transaction.atomic():
                post = (
                    ExchangePost.objects
                    .select_for_update()
                    .select_related("asset", "user")
                    .get(pk=pk)
                )
                applicant_asset = (
                    Asset.objects
                    .select_for_update()
                    .get(pk=asset_id, user=request.user)
                )

                if post.user_id == request.user.id:
                    return error(message="不能申请交换自己的帖子", http_status=400)
                if post.status != ExchangePost.Status.PUBLISHED:
                    return error(message="当前换物帖不可申请", http_status=400)
                if applicant_asset.status != Asset.Status.AVAILABLE:
                    return error(message="申请方资产状态不可交换", http_status=400)
                if ExchangeApplication.objects.filter(
                    post=post, applicant=request.user, status=ExchangeApplication.Status.PENDING
                ).exists():
                    return error(message="您已对此帖子提交过申请，请等待处理", http_status=400)

                applicant_asset.status = Asset.Status.EXCHANGE_LOCKED
                applicant_asset.save(update_fields=["status"])

                application = ExchangeApplication.objects.create(
                    post=post,
                    applicant=request.user,
                    applicant_asset=applicant_asset,
                    applicant_asset_name=applicant_asset.product_name,
                    applicant_asset_image=applicant_asset.product_image,
                    applicant_asset_rarity=applicant_asset.rarity,
                    post_asset_name=post.asset_name,
                    post_asset_image=post.asset_image,
                    post_asset_rarity=post.asset_rarity,
                    remark=remark,
                )
        except ExchangePost.DoesNotExist:
            return error(message="换物帖子不存在", http_status=404)
        except Asset.DoesNotExist:
            return error(message="资产不存在或不属于当前用户", http_status=404)
        except Exception:
            logger.exception("申请换物失败")
            return error(message="申请换物失败，请稍后重试", http_status=500)

        return success(data=ExchangeApplicationSerializer(application).data, message="申请已提交")


class ExchangeApplicationListView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = (
            ExchangeApplication.objects
            .select_related("post", "post__asset", "applicant", "applicant_asset")
            .filter(post__user=request.user)
        )
        return success(data=ExchangeApplicationSerializer(qs, many=True).data)


class ExchangeApplicationDetailView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            application = (
                ExchangeApplication.objects
                .select_related("post", "post__asset", "applicant", "applicant_asset")
                .get(pk=pk, post__user=request.user)
            )
        except ExchangeApplication.DoesNotExist:
            return error(message="换物申请不存在", http_status=404)
        return success(data=ExchangeApplicationSerializer(application).data)


class ExchangeApplicationAcceptView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            with transaction.atomic():
                application = (
                    ExchangeApplication.objects
                    .select_for_update()
                    .select_related("post", "post__asset", "applicant_asset")
                    .get(pk=pk, post__user=request.user)
                )
                post = application.post
                post_asset = Asset.objects.select_for_update().get(pk=post.asset_id)
                applicant_asset = Asset.objects.select_for_update().get(pk=application.applicant_asset_id)

                if application.status != ExchangeApplication.Status.PENDING:
                    return error(message="当前申请已处理", http_status=400)
                if post.status != ExchangePost.Status.PUBLISHED:
                    return error(message="当前换物帖不可处理", http_status=400)

                publisher = post.user
                applicant = application.applicant
                post_asset.user = applicant
                post_asset.status = Asset.Status.AVAILABLE
                post_asset.save(update_fields=["user", "status"])

                applicant_asset.user = publisher
                applicant_asset.status = Asset.Status.AVAILABLE
                applicant_asset.save(update_fields=["user", "status"])

                application.status = ExchangeApplication.Status.ACCEPTED
                application.save(update_fields=["status"])

                post.status = ExchangePost.Status.COMPLETED
                post.save(update_fields=["status"])

                # 拒绝同帖子其他待处理申请，并解锁其申请人资产
                other_apps = (
                    ExchangeApplication.objects
                    .filter(post=post, status=ExchangeApplication.Status.PENDING)
                    .exclude(pk=application.pk)
                )
                other_applicant_ids = list(other_apps.values_list("applicant_asset_id", flat=True))
                other_apps.update(status=ExchangeApplication.Status.REJECTED)
                if other_applicant_ids:
                    Asset.objects.filter(pk__in=other_applicant_ids).update(
                        status=Asset.Status.AVAILABLE
                    )
        except ExchangeApplication.DoesNotExist:
            return error(message="换物申请不存在", http_status=404)
        except Exception:
            logger.exception("接受换物失败")
            return error(message="接受换物失败，请稍后重试", http_status=500)

        return success(message="已接受")


class ExchangeApplicationRejectView(CSRFExemptView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            with transaction.atomic():
                application = (
                    ExchangeApplication.objects
                    .select_for_update()
                    .select_related("post", "post__asset", "applicant_asset")
                    .get(pk=pk, post__user=request.user)
                )
                if application.status != ExchangeApplication.Status.PENDING:
                    return error(message="当前申请已处理", http_status=400)

                applicant_asset = Asset.objects.select_for_update().get(pk=application.applicant_asset_id)
                applicant_asset.status = Asset.Status.AVAILABLE
                applicant_asset.save(update_fields=["status"])

                application.status = ExchangeApplication.Status.REJECTED
                application.save(update_fields=["status"])
        except ExchangeApplication.DoesNotExist:
            return error(message="换物申请不存在", http_status=404)
        except Exception:
            logger.exception("拒绝换物失败")
            return error(message="拒绝换物失败，请稍后重试", http_status=500)

        return success(message="已拒绝")
