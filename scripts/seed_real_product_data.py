from __future__ import annotations

import os
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "back-end"
MEDIA_PRODUCT = BACKEND / "media" / "product"
sys.path.insert(0, str(BACKEND))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402


django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.db import transaction  # noqa: E402
from django.utils import timezone  # noqa: E402

from apps.assets.models import Asset  # noqa: E402
from apps.blindbox.models import BlindBox, Prize  # noqa: E402
from apps.blindbox.probabilities import calculate_prize_probabilities, probability_to_weight  # noqa: E402
from apps.exchange.models import ExchangeApplication, ExchangePost  # noqa: E402
from apps.merchant.models import Inventory, InventoryRecord, Merchant, Product  # noqa: E402
from apps.points.models import PointsAccount, PointsRecord, TransactionRecord  # noqa: E402


MARK = "P3_REAL"
PASSWORD = "123456"

IP_RULES = [
    ("宝可梦", ["皮卡丘", "超梦", "沙奈朵", "丰缘", "骑拉帝纳", "喷火龙", "伊布", "梦幻"]),
    ("咒术回战", ["五条悟", "伏黑", "虎杖", "钉崎", "宿傩"]),
    ("鬼灭之刃", ["炭治郎", "祢豆子", "善逸", "伊之助", "蝴蝶忍"]),
    ("原神", ["雷电影", "纳西妲", "钟离", "芙宁娜", "万叶", "魈", "甘雨", "胡桃"]),
    ("明日方舟", ["凯尔希", "史尔特尔", "森蚺", "斯卡蒂", "能天使", "艾雅法拉", "阿米娅", "银灰"]),
    ("EVA", ["EVA", "初号机", "明日香", "绫波丽"]),
    ("Fate", ["Saber", "远坂凛", "间桐樱", "誓约胜利之剑"]),
    ("海贼王", ["路飞", "索隆", "娜美", "乔巴"]),
    ("JOJO", ["乔鲁诺", "黄金体验", "空条", "承太郎", "迪奥"]),
    ("黑白的阿维斯塔", ["黑白的阿维斯塔", "凶战士", "惭愧之空", "不变之物", "堕天无惭乐土"]),
]

CATEGORY_RULES = [
    ("手办", ["手办", "模型", "雕像"]),
    ("海报", ["海报"]),
    ("徽章", ["徽章"]),
    ("亚克力", ["亚克力", "立牌"]),
    ("毛绒", ["毛绒", "玩偶"]),
    ("色纸", ["色纸"]),
    ("卡册", ["卡册"]),
    ("卡片", ["卡片", "卡牌"]),
    ("挂件", ["挂件", "钥匙扣"]),
    ("小说", ["小说", "卷"]),
]

RARITY_POINTS = {
    "SSR": (520, 260),
    "SR": (300, 150),
    "R": (160, 80),
    "N": (80, 40),
}


def infer_ip(name: str) -> str:
    for ip_name, keywords in IP_RULES:
        if any(keyword in name for keyword in keywords):
            return ip_name
    return "综合动漫"


def infer_category(name: str) -> str:
    for category, keywords in CATEGORY_RULES:
        if any(keyword in name for keyword in keywords):
            return category
    return "周边"


def infer_rarity(name: str, category: str) -> str:
    if category == "手办" or any(keyword in name for keyword in ["超梦", "五条悟", "Saber", "雷电影", "钟离", "骑拉帝纳"]):
        return "SSR"
    if category in {"亚克力", "色纸"} or any(keyword in name for keyword in ["套装", "限定", "三神", "初号机"]):
        return "SR"
    if category in {"海报", "毛绒", "卡册", "小说"}:
        return "R"
    return "N"


def ensure_user(username: str, role: str, phone: str):
    User = get_user_model()
    user, _ = User.objects.get_or_create(
        username=username,
        defaults={"role": role, "phone": phone, "email": f"{username}@example.com"},
    )
    user.role = role
    user.phone = phone
    user.email = f"{username}@example.com"
    user.set_password(PASSWORD)
    user.save()
    return user


def clean_seed_data():
    ExchangeApplication.objects.filter(remark__contains=MARK).delete()
    ExchangePost.objects.filter(remark__contains=MARK).delete()
    Asset.objects.filter(source_name__startswith=MARK).delete()
    BlindBox.objects.filter(name__startswith="P3真实").delete()
    Product.objects.filter(merchant__name="P3真实测试商家").delete()
    Merchant.objects.filter(name="P3真实测试商家").delete()
    PointsRecord.objects.filter(related_id=MARK).delete()
    TransactionRecord.objects.filter(description__contains=MARK).delete()


def create_products(merchant: Merchant):
    files = sorted(
        [item for item in MEDIA_PRODUCT.iterdir() if item.is_file() and item.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}],
        key=lambda item: item.name,
    )
    products = []
    for item in files:
        raw_name = item.stem.strip()
        ip_name = infer_ip(raw_name)
        category = infer_category(raw_name)
        rarity = infer_rarity(raw_name, category)
        estimated_points, _ = RARITY_POINTS[rarity]
        product = Product.objects.create(
            merchant=merchant,
            name=raw_name,
            image=f"/media/product/{item.name}",
            category=category,
            rarity=rarity,
            description=f"{ip_name} {category}周边，角色/主题：{raw_name}。用于P3盲盒抽取、我的资产和换物测试。",
            estimated_points=estimated_points,
            status=Product.Status.APPROVED,
            review_note=f"{MARK} seed",
        )
        Inventory.objects.create(product=product, current_stock=50)
        InventoryRecord.objects.create(
            product=product,
            type=InventoryRecord.ChangeType.INCREASE,
            before_stock=0,
            after_stock=50,
            reason=f"{MARK} 初始测试库存",
        )
        product.seed_ip_name = ip_name
        products.append(product)
    return products


def create_blindboxes(products):
    grouped = defaultdict(list)
    for product in products:
        grouped[product.seed_ip_name].append(product)

    now = timezone.now()
    boxes = []
    for index, (ip_name, group) in enumerate(sorted(grouped.items()), start=1):
        selected = group[: min(len(group), 8)]
        if len(selected) < 2:
            continue
        cost = 80 if ip_name == "综合动漫" else 100
        box = BlindBox.objects.create(
            name=f"P3真实{ip_name}主题盲盒",
            cover=selected[0].image,
            description=f"{MARK} 基于真实图片生成的{ip_name}测试盲盒，支持单抽、五连抽、十连抽和结果回收。",
            category="IP主题盲盒",
            ip_name=ip_name,
            cost_points=cost,
            status=BlindBox.Status.ACTIVE,
            start_time=now - timezone.timedelta(days=1),
            end_time=now + timezone.timedelta(days=90),
            max_draw_count=10,
            allow_simulation=True,
            sort_order=index,
        )
        calculated_probabilities = calculate_prize_probabilities(selected, cost)
        for product, probability in zip(selected, calculated_probabilities):
            Prize.objects.create(
                blindbox=box,
                product=product,
                name=product.name,
                image=product.image,
                rarity=product.rarity,
                probability=probability,
                weight=probability_to_weight(probability),
                quantity=35,
                remaining_quantity=35,
                is_active=True,
                ip_name_snapshot=ip_name,
            )
        boxes.append(box)
    return boxes


def create_assets_and_exchange(users, products, boxes):
    main_user, exchange_user = users
    now = timezone.now()
    available_assets = []
    exchange_assets = []

    for index, product in enumerate(products[:36]):
        _, recycle_points = RARITY_POINTS[product.rarity]
        status = Asset.Status.RECYCLED if index in {7, 15, 23} else Asset.Status.AVAILABLE
        asset = Asset.objects.create(
            user=main_user,
            product=product,
            product_name=product.name,
            product_image=product.image,
            category=product.category,
            rarity=product.rarity,
            description=product.description,
            source_type=Asset.SourceType.BLINDBOX,
            source_name=f"{MARK} 我的资产测试",
            obtained_at=now - timezone.timedelta(minutes=index * 3),
            status=status,
            estimated_points=product.estimated_points,
            recyclable_points=recycle_points,
        )
        if status == Asset.Status.AVAILABLE:
            available_assets.append(asset)

    for duplicate_product in products[:8]:
        _, recycle_points = RARITY_POINTS[duplicate_product.rarity]
        available_assets.append(
            Asset.objects.create(
                user=main_user,
                product=duplicate_product,
                product_name=duplicate_product.name,
                product_image=duplicate_product.image,
                category=duplicate_product.category,
                rarity=duplicate_product.rarity,
                description=duplicate_product.description,
                source_type=Asset.SourceType.BLINDBOX,
                source_name=f"{MARK} 同类保留测试",
                obtained_at=now,
                status=Asset.Status.AVAILABLE,
                estimated_points=duplicate_product.estimated_points,
                recyclable_points=RARITY_POINTS[duplicate_product.rarity][1],
            )
        )

    for index, product in enumerate(products[36:56]):
        _, recycle_points = RARITY_POINTS[product.rarity]
        asset = Asset.objects.create(
            user=exchange_user,
            product=product,
            product_name=product.name,
            product_image=product.image,
            category=product.category,
            rarity=product.rarity,
            description=product.description,
            source_type=Asset.SourceType.BLINDBOX,
            source_name=f"{MARK} 换物市场测试",
            obtained_at=now - timezone.timedelta(minutes=index * 2),
            status=Asset.Status.AVAILABLE,
            estimated_points=product.estimated_points,
            recyclable_points=recycle_points,
        )
        exchange_assets.append(asset)

    for index, asset in enumerate(exchange_assets[:10]):
        asset.status = Asset.Status.EXCHANGE_PUBLISHED
        asset.save(update_fields=["status", "updated_at"])
        ExchangePost.objects.create(
            user=exchange_user,
            asset=asset,
            asset_name=asset.product_name,
            asset_image=asset.product_image,
            asset_rarity=asset.rarity,
            asset_category=asset.category,
            expect_description="希望交换同IP角色、SSR/SR手办、亚克力立牌或稀有徽章。",
            remark=f"{MARK} published exchange post {index + 1}",
            status=ExchangePost.Status.PUBLISHED,
        )

    if available_assets and exchange_assets:
        post = ExchangePost.objects.filter(remark__contains=MARK, status=ExchangePost.Status.PUBLISHED).first()
        applicant_asset = available_assets[0]
        ExchangeApplication.objects.create(
            post=post,
            applicant=main_user,
            applicant_asset=applicant_asset,
            applicant_asset_name=applicant_asset.product_name,
            applicant_asset_image=applicant_asset.product_image,
            applicant_asset_rarity=applicant_asset.rarity,
            post_asset_name=post.asset_name,
            post_asset_image=post.asset_image,
            post_asset_rarity=post.asset_rarity,
            remark=f"{MARK} pending application",
            status=ExchangeApplication.Status.PENDING,
        )

    return available_assets, exchange_assets


def seed_points(user):
    account, _ = PointsAccount.objects.get_or_create(user=user, defaults={"balance": 0})
    account.balance = 10000
    account.save(update_fields=["balance", "updated_at"])
    PointsRecord.objects.create(
        user=user,
        type=PointsRecord.RecordType.SYSTEM_ADJUST,
        amount=10000,
        balance=10000,
        description=f"{MARK} 测试积分初始化",
        related_id=MARK,
    )


@transaction.atomic
def main():
    if not MEDIA_PRODUCT.exists():
        raise RuntimeError(f"Image folder not found: {MEDIA_PRODUCT}")

    clean_seed_data()

    main_user = ensure_user("testuser", "user", "13800000001")
    exchange_user = ensure_user("p3_exchange_user", "user", "13800000002")
    merchant_user = ensure_user("p3_real_merchant", "merchant", "13800000003")
    merchant = Merchant.objects.create(
        user=merchant_user,
        name="P3真实测试商家",
        contact_name="P3测试负责人",
        phone="13800000003",
        email="p3_real_merchant@example.com",
        license="P3-REAL-SEED",
        business_scope="动漫IP周边、盲盒奖品、换物测试商品",
        supply_desc=f"{MARK} 由本地真实图片生成",
        status=Merchant.Status.APPROVED,
        credit_score=100,
        review_note=f"{MARK} 自动审核通过",
        reviewed_at=timezone.now(),
    )

    seed_points(main_user)
    seed_points(exchange_user)
    products = create_products(merchant)
    boxes = create_blindboxes(products)
    available_assets, exchange_assets = create_assets_and_exchange((main_user, exchange_user), products, boxes)

    print(f"Seed marker: {MARK}")
    print(f"Login user: testuser / {PASSWORD}")
    print(f"Exchange user: p3_exchange_user / {PASSWORD}")
    print(f"Merchant user: p3_real_merchant / {PASSWORD}")
    print(f"Products: {len(products)}")
    print(f"Blind boxes: {len(boxes)}")
    print(f"Main available assets: {len(available_assets)}")
    print(f"Exchange assets: {len(exchange_assets)}")
    print(f"Exchange posts: {ExchangePost.objects.filter(remark__contains=MARK).count()}")


if __name__ == "__main__":
    main()
