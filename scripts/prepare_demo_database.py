import os
import sys
from datetime import timedelta


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND = os.path.join(ROOT, "back-end")
if BACKEND not in sys.path:
    sys.path.insert(0, BACKEND)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Address, Division
from apps.assets.models import Asset
from apps.blindbox.models import BlindBox, DrawRecord, Prize
from apps.exchange.models import ExchangeApplication, ExchangePost
from apps.merchant.models import Inventory, InventoryRecord, Merchant, Product, ShipmentTask
from apps.orders.models import Order
from apps.points.models import PointsAccount, PointsRecord, TransactionRecord


DEMO_PREFIX = "DEMO20260609"


def clean_demo_text(value):
    if value is None:
        return value
    text = str(value)
    replacements = [
        "P3_REAL",
        "P3真实测试",
        "P3真实",
        "P3测试",
        "P3",
        "真实测试",
        "真实类",
        "真实",
        "测试",
        "test",
        "Test",
    ]
    for item in replacements:
        text = text.replace(item, "")
    while "  " in text:
        text = text.replace("  ", " ")
    return text.strip(" -_，,")


def clean_model_text(model, fields):
    changed = 0
    for obj in model.objects.all():
        update_fields = []
        for field in fields:
            original = getattr(obj, field, "")
            cleaned = clean_demo_text(original)
            if cleaned != original:
                setattr(obj, field, cleaned or original)
                update_fields.append(field)
        if update_fields:
            obj.save(update_fields=update_fields)
            changed += 1
    return changed


def get_or_create_user(username, role, password="123456", phone="13800000000", first_name=""):
    User = get_user_model()
    user, created = User.objects.get_or_create(username=username, defaults={
        "role": role,
        "phone": phone,
        "first_name": first_name,
        "is_active": True,
    })
    changed_fields = []
    if created:
        user.set_password(password)
        changed_fields.append("password")
    if user.role != role:
        user.role = role
        changed_fields.append("role")
    if phone and user.phone != phone:
        user.phone = phone
        changed_fields.append("phone")
    if first_name and user.first_name != first_name:
        user.first_name = first_name
        changed_fields.append("first_name")
    if not user.is_active:
        user.is_active = True
        changed_fields.append("is_active")
    if changed_fields:
        user.save(update_fields=changed_fields)
    return user


def ensure_address(user, receiver_name, receiver_phone, detail):
    province = Division.objects.filter(level=1, name__contains="广东").first() or Division.objects.filter(level=1).first()
    city = Division.objects.filter(level=2, parent=province, name__contains="广州").first() if province else None
    city = city or Division.objects.filter(level=2, parent=province).first() if province else Division.objects.filter(level=2).first()
    district = Division.objects.filter(level=3, parent=city).first() if city else Division.objects.filter(level=3).first()
    if not (province and city and district):
        return None
    address, _ = Address.objects.update_or_create(
        user=user,
        receiver_name=receiver_name,
        defaults={
            "receiver_phone": receiver_phone,
            "province": province,
            "city": city,
            "district": district,
            "street": "大学城校区",
            "detail": detail,
            "is_default": True,
        },
    )
    return f"{province.name}{city.name}{district.name}大学城校区{detail}"


def ensure_merchants():
    merchant_specs = [
        ("merchant_p3", "潮玩优选供货商", "林经理", "13800138001", "动漫手办、徽章、海报及盲盒周边供货"),
        ("p3_real_merchant", "乐抽官方供货商", "周经理", "13800138002", "正版 IP 周边、限定款手办及抽盒商品供货"),
        ("merchant_test", "星谷周边供货商", "陈经理", "13800138003", "游戏、动画和收藏卡周边供货"),
    ]
    merchants = []
    for username, name, contact, phone, scope in merchant_specs:
        user = get_or_create_user(username, "merchant", phone=phone, first_name=name)
        merchant, _ = Merchant.objects.update_or_create(
            user=user,
            defaults={
                "name": name,
                "contact_name": contact,
                "phone": phone,
                "email": f"{username}@demo.local",
                "license": f"DEMO-LICENSE-{username.upper()}",
                "business_scope": scope,
                "supply_desc": "演示用稳定供货商，商品、库存和发货数据已同步。",
                "status": Merchant.Status.APPROVED,
                "credit_score": 96,
                "review_note": "演示账号，已通过资质审核。",
                "reviewed_at": timezone.now(),
            },
        )
        merchants.append(merchant)
    return merchants


def ensure_products_have_merchants(merchants):
    products = list(Product.objects.filter(status=Product.Status.APPROVED).order_by("rarity", "id"))
    if not products:
        raise RuntimeError("没有可用的已审核商品，请先导入商品数据。")
    for index, product in enumerate(products):
        changed = []
        cleaned_name = clean_demo_text(product.name)
        cleaned_description = clean_demo_text(product.description)
        if cleaned_name != product.name:
            product.name = cleaned_name or product.name
            changed.append("name")
        if cleaned_description != product.description:
            product.description = cleaned_description
            changed.append("description")
        if product.merchant_id is None:
            product.merchant = merchants[index % len(merchants)]
            changed.append("merchant")
        if not product.estimated_points:
            fallback = {"N": 60, "R": 90, "SR": 150, "SSR": 260}.get(product.rarity, 80)
            product.estimated_points = fallback
            changed.append("estimated_points")
        if changed:
            product.save(update_fields=sorted(set(changed)))
        inv, _ = Inventory.objects.get_or_create(product=product, defaults={"current_stock": 80})
        if inv.current_stock < 30:
            before = inv.current_stock
            inv.current_stock = 80
            inv.save(update_fields=["current_stock"])
            InventoryRecord.objects.create(
                product=product,
                type=InventoryRecord.ChangeType.MODIFY,
                before_stock=before,
                after_stock=80,
                reason="演示前补足库存",
            )
    return list(Product.objects.filter(status=Product.Status.APPROVED).select_related("merchant").order_by("-rarity", "id"))


def purge_old_demo_rows():
    ShipmentTask.objects.filter(task_no__startswith="P3_DEMO").delete()
    Order.objects.filter(order_no__startswith=DEMO_PREFIX).delete()
    ShipmentTask.objects.filter(task_no__startswith=DEMO_PREFIX).delete()
    TransactionRecord.objects.filter(description__startswith="演示").delete()
    PointsRecord.objects.filter(related_id__startswith=DEMO_PREFIX).delete()
    ExchangeApplication.objects.filter(remark__startswith="可补差价积分").delete()
    ExchangePost.objects.filter(remark__startswith="演示换物帖").delete()
    Asset.objects.filter(description__startswith="演示数据").delete()


def set_created(obj, when):
    obj.created_at = when
    obj.updated_at = when
    obj.save(update_fields=["created_at", "updated_at"])


def source_name_for(product):
    box = BlindBox.objects.filter(category=product.category, status=BlindBox.Status.ACTIVE).first()
    if box:
        return clean_demo_text(box.name)
    return f"{product.category}主题盲盒"


def create_asset(user, product, status, days_ago):
    obtained_at = timezone.now() - timedelta(days=days_ago)
    recyclable = max(1, int((product.estimated_points or 80) * 0.5))
    asset = Asset.objects.create(
        user=user,
        product=product,
        product_name=clean_demo_text(product.name),
        product_image=product.image,
        category=product.category,
        rarity=product.rarity,
        description=f"演示数据：{clean_demo_text(product.description) or product.category + '周边'}",
        source_type=Asset.SourceType.BLINDBOX,
        source_name=source_name_for(product),
        obtained_at=obtained_at,
        status=status,
        estimated_points=product.estimated_points or 80,
        recyclable_points=recyclable,
    )
    set_created(asset, obtained_at)
    return asset


def create_order_and_shipment(seq, user, product, status, days_ago, receiver_name, receiver_phone, address):
    now = timezone.now()
    created_at = now - timedelta(days=days_ago)
    asset_status = {
        Order.Status.PENDING: Asset.Status.PENDING_SHIPMENT,
        Order.Status.SHIPPED: Asset.Status.SHIPPED,
        Order.Status.COMPLETED: Asset.Status.COMPLETED,
    }[status]
    asset = create_asset(user, product, asset_status, days_ago + 1)
    order_no = f"{DEMO_PREFIX}{seq:03d}"
    shipped_at = created_at + timedelta(days=1) if status in (Order.Status.SHIPPED, Order.Status.COMPLETED) else None
    completed_at = created_at + timedelta(days=4) if status == Order.Status.COMPLETED else None
    order = Order.objects.create(
        user=user,
        order_no=order_no,
        type=Order.OrderType.SHIPMENT,
        asset=asset,
        asset_name=asset.product_name,
        asset_image=asset.product_image,
        status=status,
        receiver_name=receiver_name,
        receiver_phone=receiver_phone,
        receiver_address=address,
        logistics_company="顺丰速运" if shipped_at else "",
        tracking_no=f"SF{order_no[-9:]}" if shipped_at else "",
        shipped_at=shipped_at,
        completed_at=completed_at,
    )
    set_created(order, created_at)
    task = ShipmentTask.objects.create(
        product=product,
        task_no=f"{DEMO_PREFIX}T{seq:03d}",
        order_no=order_no,
        receiver_name=receiver_name,
        receiver_phone=receiver_phone,
        receiver_address=address,
        status=ShipmentTask.Status.SHIPPED if shipped_at else ShipmentTask.Status.PENDING,
        logistics_company=order.logistics_company,
        tracking_no=order.tracking_no,
        shipped_at=shipped_at,
    )
    set_created(task, created_at)
    TransactionRecord.objects.create(
        user=user,
        type=TransactionRecord.RecordType.SHIPMENT,
        description=f"演示订单 {order_no}：{'待商家发货' if status == Order.Status.PENDING else '商家已发货' if status == Order.Status.SHIPPED else '用户已确认收货'}",
        related_asset_name=asset.product_name,
        status_change=f"可操作 -> {asset.status}",
    )
    return order


def create_points_history(user, base_balance, seq):
    PointsAccount.objects.update_or_create(user=user, defaults={"balance": base_balance})
    records = [
        (PointsRecord.RecordType.RECHARGE, 500, 500, "演示充值：50 元兑换 500 积分", 16),
        (PointsRecord.RecordType.BLINDBOX_CONSUME, -100, 400, "演示抽取：EVA主题盲盒 单抽", 15),
        (PointsRecord.RecordType.BLINDBOX_CONSUME, -500, 900, "演示抽取：宝可梦主题盲盒 五连抽", 10),
        (PointsRecord.RecordType.RECYCLE_RETURN, 55, 955, "演示回收：重复款周边返还积分", 7),
        (PointsRecord.RecordType.RECHARGE, 300, base_balance, "演示充值：30 元兑换 300 积分", 3),
    ]
    for index, (record_type, amount, balance, desc, days_ago) in enumerate(records, start=1):
        record = PointsRecord.objects.create(
            user=user,
            type=record_type,
            amount=amount,
            balance=balance if index < len(records) else base_balance,
            description=desc,
            related_id=f"{DEMO_PREFIX}P{seq}{index}",
        )
        set_created(record, timezone.now() - timedelta(days=days_ago))


def create_demo_orders(products):
    users = [
        get_or_create_user("demo_user_a", "user", phone="13900000001", first_name="演示用户A"),
        get_or_create_user("demo_user_b", "user", phone="13900000002", first_name="演示用户B"),
        get_or_create_user("demo_buyer", "user", phone="13900000003", first_name="演示用户C"),
    ]
    addresses = [
        ensure_address(users[0], "李同学", "13900000001", "1栋305宿舍") or "广东省广州市番禺区大学城校区1栋305宿舍",
        ensure_address(users[1], "王同学", "13900000002", "2栋418宿舍") or "广东省广州市番禺区大学城校区2栋418宿舍",
        ensure_address(users[2], "陈同学", "13900000003", "综合楼服务台") or "广东省广州市番禺区大学城校区综合楼服务台",
    ]
    for index, user in enumerate(users, start=1):
        create_points_history(user, 800 + index * 120, index)

    specs = [
        (1, users[0], products[0], Order.Status.PENDING, 2, "李同学", "13900000001", addresses[0]),
        (2, users[0], products[1], Order.Status.SHIPPED, 6, "李同学", "13900000001", addresses[0]),
        (3, users[0], products[2], Order.Status.COMPLETED, 13, "李同学", "13900000001", addresses[0]),
        (4, users[1], products[3], Order.Status.PENDING, 1, "王同学", "13900000002", addresses[1]),
        (5, users[1], products[4], Order.Status.SHIPPED, 8, "王同学", "13900000002", addresses[1]),
        (6, users[2], products[5], Order.Status.COMPLETED, 18, "陈同学", "13900000003", addresses[2]),
        (7, users[2], products[6], Order.Status.COMPLETED, 24, "陈同学", "13900000003", addresses[2]),
    ]
    orders = []
    for spec in specs:
        orders.append(create_order_and_shipment(*spec))

    for index, (user, product) in enumerate([(users[0], products[7]), (users[1], products[8]), (users[2], products[9])], start=1):
        create_asset(user, product, Asset.Status.AVAILABLE, 5 + index)
    return orders


def ensure_exchange_demo(products):
    users = [
        get_or_create_user("demo_user_a", "user", phone="13900000001", first_name="演示用户A"),
        get_or_create_user("demo_user_b", "user", phone="13900000002", first_name="演示用户B"),
    ]
    owner_asset = create_asset(users[0], products[10], Asset.Status.EXCHANGE_PUBLISHED, 4)
    applicant_asset = create_asset(users[1], products[11], Asset.Status.AVAILABLE, 3)
    post = ExchangePost.objects.create(
        user=users[0],
        asset=owner_asset,
        asset_name=owner_asset.product_name,
        asset_image=owner_asset.product_image,
        asset_rarity=owner_asset.rarity,
        asset_category=owner_asset.category,
        expect_description="希望交换同系列手办或限定徽章，成色完整即可。",
        remark="演示换物帖，可用于老师查看换物流程。",
        status=ExchangePost.Status.PUBLISHED,
    )
    set_created(post, timezone.now() - timedelta(days=4))
    application = ExchangeApplication.objects.create(
        post=post,
        applicant=users[1],
        applicant_asset=applicant_asset,
        applicant_asset_name=applicant_asset.product_name,
        applicant_asset_image=applicant_asset.product_image,
        applicant_asset_rarity=applicant_asset.rarity,
        post_asset_name=owner_asset.product_name,
        post_asset_image=owner_asset.product_image,
        post_asset_rarity=owner_asset.rarity,
        remark="可补差价积分，想换同系列收藏。",
        status=ExchangeApplication.Status.PENDING,
    )
    set_created(application, timezone.now() - timedelta(days=3))


def clean_visible_content():
    return {
        "blindbox": clean_model_text(BlindBox, ["name", "description", "ip_name"]),
        "product": clean_model_text(Product, ["name", "category", "description"]),
        "prize": clean_model_text(Prize, ["name", "ip_name_snapshot"]),
        "draw_record": clean_model_text(DrawRecord, ["prize_name", "ip_name_snapshot"]),
        "asset": clean_model_text(Asset, ["product_name", "category", "description", "source_name"]),
        "order": clean_model_text(Order, ["asset_name", "receiver_address", "logistics_company"]),
        "merchant": clean_model_text(Merchant, ["name", "business_scope", "supply_desc", "review_note"]),
        "exchange_post": clean_model_text(ExchangePost, ["asset_name", "asset_category", "expect_description", "remark"]),
        "exchange_application": clean_model_text(ExchangeApplication, ["applicant_asset_name", "post_asset_name", "remark"]),
        "points_record": clean_model_text(PointsRecord, ["description", "related_id"]),
        "transaction_record": clean_model_text(TransactionRecord, ["description", "related_asset_name", "status_change"]),
    }


@transaction.atomic
def main():
    cleaned = clean_visible_content()
    purge_old_demo_rows()
    merchants = ensure_merchants()
    products = ensure_products_have_merchants(merchants)
    if len(products) < 12:
        raise RuntimeError("演示数据至少需要 12 个已审核商品。")
    orders = create_demo_orders(products)
    ensure_exchange_demo(products)

    leftovers = {}
    for model, fields in [
        (BlindBox, ["name", "description", "ip_name"]),
        (Product, ["name", "category", "description"]),
        (Merchant, ["name", "business_scope", "supply_desc"]),
        (Asset, ["product_name", "source_name", "description"]),
        (Order, ["asset_name", "receiver_address"]),
        (ShipmentTask, ["receiver_address"]),
        (ExchangePost, ["asset_name", "expect_description", "remark"]),
    ]:
        count = 0
        for field in fields:
            query = {f"{field}__regex": r"(P3|真实|测试|P3_REAL)"}
            count += model.objects.filter(**query).count()
        leftovers[model.__name__] = count

    print("演示数据库整理完成")
    print(f"清理可见字段：{cleaned}")
    print(f"演示商家：{Merchant.objects.filter(user__username__in=['merchant_p3', 'p3_real_merchant', 'merchant_test']).count()} 个")
    print(f"已审核商品：{Product.objects.filter(status=Product.Status.APPROVED).count()} 个")
    print(f"新增演示订单：{len(orders)} 个")
    print(f"同步发货任务：{ShipmentTask.objects.filter(task_no__startswith=DEMO_PREFIX).count()} 个")
    print(f"演示积分流水：{PointsRecord.objects.filter(related_id__startswith=DEMO_PREFIX).count()} 条")
    print(f"可见字段残留检查：{leftovers}")


if __name__ == "__main__":
    main()
