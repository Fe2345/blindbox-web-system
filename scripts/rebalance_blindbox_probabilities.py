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

from apps.blindbox.models import BlindBox  # noqa: E402
from apps.blindbox.probabilities import calculate_prize_probabilities, probability_to_weight  # noqa: E402
from apps.common.valuation import resolve_estimated_points, resolve_recyclable_points  # noqa: E402


@transaction.atomic
def main():
    updated = 0
    for box in BlindBox.objects.prefetch_related("prizes").order_by("id"):
        prizes = list(box.prizes.all().order_by("id"))
        if not prizes:
            continue
        probabilities = calculate_prize_probabilities(prizes, box.cost_points)
        for prize, probability in zip(prizes, probabilities):
            prize.probability = probability
            prize.weight = probability_to_weight(probability)
            prize.save(update_fields=["probability", "weight", "updated_at"])
            updated += 1
        total = sum(prize.probability for prize in prizes)
        display_ev = sum((prize.probability / 100) * resolve_estimated_points(prize, box.cost_points) for prize in prizes)
        recycle_ev = sum((prize.probability / 100) * resolve_recyclable_points(prize, box.cost_points) for prize in prizes)
        print(
            f"{box.id} {box.name}: {len(prizes)} prizes, total probability={total}%, "
            f"display EV≈{display_ev:.2f}, recycle EV≈{recycle_ev:.2f}, target={box.cost_points}"
        )
    print(f"Updated prizes: {updated}")


if __name__ == "__main__":
    main()
