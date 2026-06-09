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

from django.db import transaction  # noqa: E402

from apps.assets.models import Asset  # noqa: E402
from apps.blindbox.models import BlindBox  # noqa: E402
from apps.blindbox.probabilities import calculate_prize_probabilities, probability_to_weight  # noqa: E402
from apps.common.valuation import estimate_points_for_rarity, recycle_points_for_value  # noqa: E402


@transaction.atomic
def main():
    product_values = {}
    for box in BlindBox.objects.prefetch_related("prizes__product").order_by("id"):
        prizes = list(box.prizes.all())
        single_rarity_pool = len({prize.rarity for prize in prizes}) == 1
        for prize in prizes:
            if prize.product_id:
                product_values[prize.product_id] = (
                    box.cost_points if single_rarity_pool else estimate_points_for_rarity(prize.rarity, box.cost_points)
                )

    product_updated = 0
    from apps.merchant.models import Product

    for product_id, value in product_values.items():
        product_updated += Product.objects.filter(pk=product_id).update(estimated_points=value)

    asset_updated = 0
    for asset in Asset.objects.select_related("product").all():
        if asset.product_id and asset.product.estimated_points > 0:
            estimated_points = asset.product.estimated_points
        else:
            estimated_points = asset.estimated_points
        recyclable_points = recycle_points_for_value(estimated_points, asset.rarity) if estimated_points > 0 else 0
        if asset.estimated_points != estimated_points or asset.recyclable_points != recyclable_points:
            asset.estimated_points = estimated_points
            asset.recyclable_points = recyclable_points
            asset.save(update_fields=["estimated_points", "recyclable_points", "updated_at"])
            asset_updated += 1

    prize_updated = 0
    for box in BlindBox.objects.prefetch_related("prizes__product").order_by("id"):
        prizes = list(box.prizes.all().order_by("id"))
        if not prizes:
            continue
        probabilities = calculate_prize_probabilities(prizes, box.cost_points)
        for prize, probability in zip(prizes, probabilities):
            prize.probability = probability
            prize.weight = probability_to_weight(probability)
            prize.save(update_fields=["probability", "weight", "updated_at"])
            prize_updated += 1

        display_ev = sum(
            (prize.probability / 100) * (prize.product.estimated_points if prize.product_id else 0)
            for prize in prizes
        )
        recycle_ev = sum(
            (prize.probability / 100)
            * recycle_points_for_value(prize.product.estimated_points if prize.product_id else 0, prize.rarity)
            for prize in prizes
        )
        print(
            f"{box.id} {box.name}: display EV={display_ev:.2f}/{box.cost_points}, "
            f"recycle EV={recycle_ev:.2f}/{box.cost_points * 0.5:.2f}"
        )

    print(f"Updated products={product_updated}, assets={asset_updated}, prizes={prize_updated}")


if __name__ == "__main__":
    main()
