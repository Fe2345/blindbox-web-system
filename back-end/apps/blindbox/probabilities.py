from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_UP
from itertools import product

from apps.common.valuation import resolve_estimated_points, resolve_recyclable_points


PROBABILITY_QUANT = Decimal("0.0001")
SEARCH_STEP = Decimal("0.5")
MIN_VALUE_WEIGHT_SHARE_RATIO = Decimal("0.10")
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


def _item_value(item, cost_points: int) -> Decimal:
    return Decimal(max(resolve_estimated_points(item, cost_points), 1))


def _item_recycle_value(item, cost_points: int) -> Decimal:
    return Decimal(max(resolve_recyclable_points(item, cost_points), 0))


def _value_weighted_shares(items, cost_points: int) -> list[Decimal]:
    """Split one rarity total by value: higher estimated value means lower odds."""
    if not items:
        return []

    raw_weights = [Decimal("1") / _item_value(item, cost_points) for item in items]
    raw_total = sum(raw_weights)
    if raw_total <= 0:
        return [Decimal("1") / Decimal(len(items)) for _ in items]

    raw_shares = [weight / raw_total for weight in raw_weights]
    minimum_share = (Decimal("1") / Decimal(len(items))) * MIN_VALUE_WEIGHT_SHARE_RATIO
    adjusted_shares = [max(share, minimum_share) for share in raw_shares]
    adjusted_total = sum(adjusted_shares)
    return [share / adjusted_total for share in adjusted_shares]


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
    items_by_rarity = defaultdict(list)

    for item in items:
        rarity = _item_rarity(item)
        items_by_rarity[rarity].append(item)

    rarity_item_shares = {
        rarity: _value_weighted_shares(rarity_items, cost_points)
        for rarity, rarity_items in items_by_rarity.items()
    }

    avg_values = {}
    avg_recycle_values = {}
    for rarity, rarity_items in items_by_rarity.items():
        shares = rarity_item_shares[rarity]
        avg_values[rarity] = sum(
            share * _item_value(item, cost_points)
            for item, share in zip(rarity_items, shares)
        )
        avg_recycle_values[rarity] = sum(
            share * _item_recycle_value(item, cost_points)
            for item, share in zip(rarity_items, shares)
        )

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

    indexes_by_rarity = defaultdict(list)
    for index, rarity in enumerate(rarities):
        indexes_by_rarity[rarity].append(index)

    probabilities = [Decimal("0") for _ in items]
    for rarity, indexes in indexes_by_rarity.items():
        rarity_total = totals[rarity]
        rarity_items = [items[index] for index in indexes]
        shares = _value_weighted_shares(rarity_items, cost_points)
        for index, share in zip(indexes, shares):
            probabilities[index] = quantize_probability(rarity_total * share)

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
