import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.accounts.models import User
from apps.blindbox.models import BlindBox, Prize
from apps.points.models import PointsAccount
from django.utils import timezone

# 1. 创建 bububu 用户
User.objects.filter(username="bububu").delete()
user = User.objects.create_user(username="bububu", password="123456", phone="13800001234")
print(f"[OK] 用户 bububu 创建成功, id={user.id}")

# 2. 创建积分账户
PointsAccount.objects.filter(user=user).delete()
account = PointsAccount.objects.create(user=user, balance=10000)
print(f"[OK] 积分账户创建成功, 余额={account.balance}")

# 3. 创建盲盒
now = timezone.now()
box = BlindBox.objects.create(
    name="测试盲盒-动漫系列",
    cover="/media/blindbox/test.png",
    description="测试用盲盒，包含N/R/SR/SSR四种稀有度",
    category="动漫",
    ip_name="测试IP",
    cost_points=100,
    status=BlindBox.Status.ACTIVE,
    start_time=now - timezone.timedelta(days=1),
    end_time=now + timezone.timedelta(days=30),
    max_draw_count=10,
    allow_simulation=True,
    sort_order=1,
)
print(f"[OK] 盲盒创建成功, id={box.id}, 名称={box.name}")

# 4. 创建奖品池
prizes_data = [
    {"name": "普通玩偶-N", "rarity": "N", "probability": 50, "quantity": 100, "remaining_quantity": 100},
    {"name": "稀有玩偶-R", "rarity": "R", "probability": 30, "quantity": 50, "remaining_quantity": 50},
    {"name": "超稀有玩偶-SR", "rarity": "SR", "probability": 15, "quantity": 20, "remaining_quantity": 20},
    {"name": "传说玩偶-SSR", "rarity": "SSR", "probability": 5, "quantity": 5, "remaining_quantity": 5},
]
for p in prizes_data:
    Prize.objects.create(
        blindbox=box,
        name=p["name"],
        image="/media/prize/default.png",
        rarity=p["rarity"],
        probability=p["probability"],
        quantity=p["quantity"],
        remaining_quantity=p["remaining_quantity"],
        is_active=True,
    )
    print(f"[OK] 奖品创建成功: {p['name']} ({p['rarity']}, {p['probability']}%)")

print("\n=== 测试数据创建完成 ===")
print(f"用户: bububu / 123456")
print(f"积分: {account.balance}")
print(f"盲盒: {box.name} (id={box.id})")
print(f"奖品: {len(prizes_data)} 个")
