from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP


DEFAULT_VALUE_MULTIPLIERS = {
    "N": Decimal("0.65"),
    "R": Decimal("0.90"),
    "SR": Decimal("1.60"),
    "SSR": Decimal("3.60"),
}

RECYCLE_RATES = {
    "N": Decimal("0.45"),
    "R": Decimal("0.48"),
    "SR": Decimal("0.52"),
    "SSR": Decimal("0.55"),
}


def rounded_points(value: Decimal | int | float) -> int:
    return max(int(Decimal(value).quantize(Decimal("1"), rounding=ROUND_HALF_UP)), 1)


def estimate_points_for_rarity(rarity: str, cost_points: int) -> int:
    multiplier = DEFAULT_VALUE_MULTIPLIERS.get(rarity, Decimal("1.00"))
    return rounded_points(Decimal(cost_points) * multiplier)


def resolve_estimated_points(item, cost_points: int) -> int:
    product = getattr(item, "product", None)
    if product is not None and getattr(product, "estimated_points", 0) > 0:
        return product.estimated_points

    product_id = item.get("product_id") if isinstance(item, dict) else getattr(item, "product_id", None)
    if product_id:
        try:
            from apps.merchant.models import Product

            product = Product.objects.only("estimated_points").get(pk=product_id)
            if product.estimated_points > 0:
                return product.estimated_points
        except Exception:
            pass

    rarity = item.get("rarity") if isinstance(item, dict) else getattr(item, "rarity", "N")
    return estimate_points_for_rarity(rarity, cost_points)


def recycle_points_for_value(estimated_points: int, rarity: str) -> int:
    if estimated_points <= 0:
        return 0
    rate = RECYCLE_RATES.get(rarity, Decimal("0.50"))
    return rounded_points(Decimal(estimated_points) * rate)


def resolve_recyclable_points(item, cost_points: int) -> int:
    estimated_points = resolve_estimated_points(item, cost_points)
    rarity = item.get("rarity") if isinstance(item, dict) else getattr(item, "rarity", "N")
    return recycle_points_for_value(estimated_points, rarity)
