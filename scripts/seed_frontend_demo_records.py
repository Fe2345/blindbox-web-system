from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "back-end"
sys.path.insert(0, str(BACKEND))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402


django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.db import transaction  # noqa: E402
from django.utils import timezone  # noqa: E402

from apps.accounts.models import Address, Division  # noqa: E402
from apps.assets.models import Asset  # noqa: E402
from apps.merchant.models import Product, ShipmentTask  # noqa: E402
from apps.operations.models import ExceptionRecord, OpLog, RuleConfig, TransactionLedger  # noqa: E402
from apps.orders.models import Order  # noqa: E402


MARK = "P3_DEMO"


def get_user(username: str):
    User = get_user_model()
    user = User.objects.filter(username=username).first()
    if not user:
        raise RuntimeError(f"Missing user: {username}. Run scripts/seed_real_product_data.py first.")
    return user


def clean_old_demo():
    Order.objects.filter(order_no__startswith=MARK).delete()
    ShipmentTask.objects.filter(task_no__startswith=MARK).delete()
    Address.objects.filter(receiver_name__startswith=MARK).delete()
    OpLog.objects.filter(detail__contains=MARK).delete()
    ExceptionRecord.objects.filter(description__contains=MARK).delete()
    TransactionLedger.objects.filter(description__contains=MARK).delete()


def seed_address(user):
    province = Division.objects.get(code="44")
    city = Division.objects.get(code="4403")
    district = Division.objects.get(code="440305")
    Address.objects.create(
        user=user,
        receiver_name=f"{MARK}测试收件人",
        receiver_phone="13800000001",
        province=province,
        city=city,
        district=district,
        street="粤海街道",
        detail="科技园测试地址 1001 室",
        is_default=True,
    )


def seed_orders(user):
    assets = list(Asset.objects.filter(user=user, source_name__startswith="P3_REAL").order_by("id")[:3])
    if len(assets) < 3:
        raise RuntimeError("Not enough P3_REAL assets to create demo orders.")

    statuses = [Order.Status.PENDING, Order.Status.SHIPPED, Order.Status.COMPLETED]
    for index, asset in enumerate(assets, start=1):
        status = statuses[index - 1]
        order = Order.objects.create(
            user=user,
            order_no=f"{MARK}-ORDER-{index:03d}",
            type=Order.OrderType.SHIPMENT,
            asset=asset,
            asset_name=asset.product_name,
            asset_image=asset.product_image,
            status=status,
            receiver_name="测试收件人",
            receiver_phone="13800000001",
            receiver_address="广东省 深圳市 南山区 科技园测试地址 1001 室",
            logistics_company="顺丰速运" if status != Order.Status.PENDING else "",
            tracking_no=f"SF{timezone.now().strftime('%m%d%H%M')}{index:03d}" if status != Order.Status.PENDING else "",
            shipped_at=timezone.now() if status != Order.Status.PENDING else None,
            completed_at=timezone.now() if status == Order.Status.COMPLETED else None,
        )
        if status == Order.Status.PENDING:
            asset.status = Asset.Status.PENDING_SHIPMENT
        elif status == Order.Status.SHIPPED:
            asset.status = Asset.Status.SHIPPED
        else:
            asset.status = Asset.Status.COMPLETED
        asset.save(update_fields=["status", "updated_at"])
        yield order


def seed_shipments(orders):
    products = list(Product.objects.filter(review_note__contains="P3_REAL").order_by("id")[:3])
    for index, order in enumerate(orders, start=1):
        product = products[(index - 1) % len(products)] if products else order.asset.product
        ShipmentTask.objects.create(
            product=product,
            task_no=f"{MARK}-SHIP-{index:03d}",
            order_no=order.order_no,
            receiver_name=order.receiver_name,
            receiver_phone=order.receiver_phone,
            receiver_address=order.receiver_address,
            status=ShipmentTask.Status.PENDING if order.status == Order.Status.PENDING else ShipmentTask.Status.SHIPPED,
            logistics_company=order.logistics_company,
            tracking_no=order.tracking_no,
            shipped_at=order.shipped_at,
        )


def seed_operations():
    rule = RuleConfig.get()
    rule.updated_by = "P3_DEMO"
    rule.save(update_fields=["updated_by", "updated_at"])

    OpLog.objects.create(operator="admin", action="初始化测试数据", target="数据库", detail=f"{MARK} 完整区划与演示数据")
    OpLog.objects.create(operator="merchant", action="调整库存", target="P3真实测试商品", detail=f"{MARK} 商家库存页面演示")

    ExceptionRecord.objects.create(
        type=ExceptionRecord.ExceptionType.ORDER,
        description=f"{MARK} 示例订单异常：物流单号待补充",
        related_id=f"{MARK}-ORDER-001",
        status=ExceptionRecord.Status.OPEN,
    )
    ExceptionRecord.objects.create(
        type=ExceptionRecord.ExceptionType.STOCK,
        description=f"{MARK} 示例库存异常：奖品库存低于阈值",
        related_id=f"{MARK}-STOCK-001",
        status=ExceptionRecord.Status.PROCESSING,
    )

    TransactionLedger.objects.create(type=TransactionLedger.LedgerType.SYSTEM, description=f"{MARK} 系统初始化积分", amount=10000)
    TransactionLedger.objects.create(type=TransactionLedger.LedgerType.SHIPMENT, description=f"{MARK} 用户申请发货", amount=0)
    TransactionLedger.objects.create(type=TransactionLedger.LedgerType.RECYCLE, description=f"{MARK} 回收资产返还积分", amount=80)


@transaction.atomic
def main():
    clean_old_demo()
    user = get_user("testuser")
    seed_address(user)
    orders = list(seed_orders(user))
    seed_shipments(orders)
    seed_operations()
    print(f"Seed marker: {MARK}")
    print(f"Addresses: {Address.objects.filter(receiver_name__startswith=MARK).count()}")
    print(f"Orders: {Order.objects.filter(order_no__startswith=MARK).count()}")
    print(f"Shipments: {ShipmentTask.objects.filter(task_no__startswith=MARK).count()}")
    print(f"Op logs: {OpLog.objects.filter(detail__contains=MARK).count()}")
    print(f"Exceptions: {ExceptionRecord.objects.filter(description__contains=MARK).count()}")
    print(f"Ledger: {TransactionLedger.objects.filter(description__contains=MARK).count()}")


if __name__ == "__main__":
    main()
