from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_UP
from itertools import product

from apps.common.valuation import resolve_estimated_points, resolve_recyclable_points


PROBABILITY_QUANT = Decimal("0.0001")
SEARCH_STEP = Decimal("0.5")
RARITY_ORDER = ["SSR", "SR", "R", "N"]
RARITY_LIMITS = {
    "SSR": (Decimal("0.5"), Decimal("12.0")),
    "SR": (Decimal("8.0"), Decimal("30.0")),
    "R": (Decimal("20.0"), Decimal("55.0")),
    "N": (Decimal("20.0"), Decimal("90.0")),
}


def quantize_probability(value: Decimal) -> Decimal:
    return value.quantize(PROBABILITY_QUANT, rounding=ROUND_HALF_UP)


def _item_rarity(item) -> str:
    return item["rarity"] if isinstance(item, dict) else item.rarity


def _candidate_values(rarity: str, only_rarity: bool = False):
    if only_rarity:
        return [Decimal("100.0")]

    start, end = RARITY_LIMITS.get(rarity, (Decimal("0"), Decimal("100")))
    count = int(((end - start) / SEARCH_STEP).to_integral_value()) + 1
    return [start + SEARCH_STEP * index for index in range(count)]


def _is_valid_distribution(totals: dict[str, Decimal]) -> bool:
    total = sum(totals.values())
    if total != Decimal("100.0"):
        return False

    lowest_present = [rarity for rarity in reversed(RARITY_ORDER) if rarity in totals][0]
    for rarity, value in totals.items():
        minimum, maximum = RARITY_LIMITS.get(rarity, (Decimal("0"), Decimal("100")))
        if rarity == lowest_present:
            maximum = Decimal("100.0")
            minimum = Decimal("0.0")
        if len(totals) > 1 and not (minimum <= value <= maximum):
            return False

    ordered = [rarity for rarity in RARITY_ORDER if rarity in totals]
    for rarer, lower in zip(ordered, ordered[1:]):
        if totals[rarer] > totals[lower]:
            return False
    return True


def _score_distribution(totals, avg_values, avg_recycle_values, target_value, target_recycle):
    display_ev = sum((totals[rarity] / Decimal("100")) * avg_values[rarity] for rarity in totals)
    recycle_ev = sum((totals[rarity] / Decimal("100")) * avg_recycle_values[rarity] for rarity in totals)
    display_error = abs(display_ev - target_value)
    recycle_error = abs(recycle_ev - target_recycle)
    return display_error * Decimal("3") + recycle_error, display_ev, recycle_ev


def calculate_probability_plan(prizes, cost_points: int):
    items = list(prizes)
    if not items:
        return [], {}

    rarities = [_item_rarity(item) for item in items]
    counts = Counter(rarities)
    present_rarities = [rarity for rarity in RARITY_ORDER if rarity in counts]
    values_by_rarity = defaultdict(list)
    recycle_by_rarity = defaultdict(list)

    for item in items:
        rarity = _item_rarity(item)
        values_by_rarity[rarity].append(Decimal(resolve_estimated_points(item, cost_points)))
        recycle_by_rarity[rarity].append(Decimal(resolve_recyclable_points(item, cost_points)))

    avg_values = {
        rarity: sum(values) / Decimal(len(values))
        for rarity, values in values_by_rarity.items()
    }
    avg_recycle_values = {
        rarity: sum(values) / Decimal(len(values))
        for rarity, values in recycle_by_rarity.items()
    }

    if len(present_rarities) == 1:
        totals = {present_rarities[0]: Decimal("100.0")}
        display_ev = avg_values[present_rarities[0]]
        recycle_ev = avg_recycle_values[present_rarities[0]]
    else:
        best = None
        enumerated = present_rarities[:-1]
        last_rarity = present_rarities[-1]
        ranges = [_candidate_values(rarity) for rarity in enumerated]
        target_value = Decimal(cost_points)
        target_recycle = Decimal(cost_points) * Decimal("0.50")

        for values in product(*ranges):
            totals = dict(zip(enumerated, values))
            totals[last_rarity] = Decimal("100.0") - sum(values)
            if not _is_valid_distribution(totals):
                continue
            score, display_ev, recycle_ev = _score_distribution(
                totals, avg_values, avg_recycle_values, target_value, target_recycle
            )
            if best is None or score < best[0]:
                best = (score, totals, display_ev, recycle_ev)

        if best is None:
            even = Decimal("100.0") / Decimal(len(present_rarities))
            totals = {rarity: even for rarity in present_rarities}
            display_ev = sum((totals[rarity] / Decimal("100")) * avg_values[rarity] for rarity in totals)
            recycle_ev = sum((totals[rarity] / Decimal("100")) * avg_recycle_values[rarity] for rarity in totals)
        else:
            _, totals, display_ev, recycle_ev = best

    per_item_by_rarity = {
        rarity: quantize_probability(total / Decimal(counts[rarity]))
        for rarity, total in totals.items()
    }
    probabilities = [per_item_by_rarity[rarity] for rarity in rarities]
    diff = quantize_probability(Decimal("100") - sum(probabilities))
    if diff:
        probabilities[-1] = quantize_probability(probabilities[-1] + diff)

    plan = {
        "rarityTotals": {rarity: float(quantize_probability(total)) for rarity, total in totals.items()},
        "displayExpectedPoints": float(display_ev.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        "recycleExpectedPoints": float(recycle_ev.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        "targetDisplayPoints": int(cost_points),
        "targetRecyclePoints": float((Decimal(cost_points) * Decimal("0.50")).quantize(Decimal("0.01"))),
    }
    return probabilities, plan


def calculate_prize_probabilities(prizes, cost_points: int):
    probabilities, _ = calculate_probability_plan(prizes, cost_points)
    return probabilities


def probability_to_weight(probability: Decimal) -> int:
    return max(int((Decimal(probability) * Decimal("10000")).to_integral_value(rounding=ROUND_HALF_UP)), 1)
