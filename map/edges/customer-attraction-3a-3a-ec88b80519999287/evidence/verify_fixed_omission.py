"""Replay the two frozen policies and certify pointwise coverage by query orders."""

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


ORIGINALS = Path("archives/customer-attraction/tools/evidence/whole-subtree-nine-endpoints-primary/original")
POLICIES = {
    "sigma252": (
        "m5p7_residual.json",
        "2a154303b023acfdc7b09c8576f63b3acb50abb02bd8e3cca6a793152ad07233",
        (0, 0, 0, 1, 1),
        (3, 2, 4, 5, 6),
    ),
    "sigma48": (
        "m5p7_reentry_incumbent_half.json",
        "e6269ea7551820d0d2c6192dd96d60b7bd2ce1f92b6ffd463fd8a13f89da0565",
        (0, 1, 0, 1, 0),
        (2, 3, 4, 6, 5),
    ),
}
LABELS = tuple(range(7))
PLAYERS = 5
MASKS = tuple(range(1, 1 << len(LABELS)))
OMITTED_MASKS = tuple(mask for mask in MASKS if not mask & 3)
FULL_OMITTED_ORDER = (2, 3, 4, 5, 6)
SCALE = 60


def label_mask(labels):
    return sum(1 << label for label in set(labels))


def read_policy(root, spec):
    filename, digest, actual, full_omission_order = spec
    raw = (root / ORIGINALS / filename).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == digest
    exact = json.loads(raw)["exact"]
    entries = exact["strategy"]["actions"]
    actions = {tuple(row["history"]): row["action"] for row in entries}
    layers = [list(itertools.product(LABELS, repeat=depth)) for depth in range(PLAYERS + 1)]
    assert len(actions) == len(entries) and set(actions) == {h for layer in layers[:-1] for h in layer}
    assert set(actions.values()) <= set(LABELS)
    leaves = {h: h for h in layers[-1]}
    for layer in reversed(layers[:-1]):
        for h in layer:
            leaves[h] = leaves[h + (actions[h],)]
    assert leaves[()] == actual and set(actual) == {0, 1}
    return actions, leaves, exact["integer_clones"], actual, full_omission_order


def query_weights(leaf, a):
    weights = []
    for mask in OMITTED_MASKS:
        if mask & (1 << a):
            load = sum(bool(mask & (1 << t)) for t in leaf)
            assert 1 <= load <= PLAYERS and SCALE % load == 0
            weights.append(SCALE // load)
        else:
            weights.append(0)
    return weights


def compare_supports(leaves, actual, full_order):
    forced = {(i, a): leaves[actual[:i] + (a,)] for i in range(PLAYERS) for a in LABELS}
    weights = {(i, a): query_weights(leaf, a) for (i, a), leaf in forced.items()}

    def certificate(order, demand):
        paid = [sum(weights[i, a][j] for i, a in enumerate(order)) for j in range(len(OMITTED_MASKS))]
        return [x - y for x, y in zip(paid, demand, strict=True)]

    result = []
    for support in itertools.combinations(LABELS, PLAYERS):
        demand = [SCALE * bool(mask & label_mask(support)) for mask in OMITTED_MASKS]
        paying = []
        for order in itertools.permutations(support):
            slack = certificate(order, demand)
            if min(slack) >= 0:
                paying.append((order, slack))
        assert paying, support
        order, slack = paying[0]
        result.append({
            "support": support, "paying_order_count": len(paying), "order": order,
            "true_leaves": [forced[i, a] for i, a in enumerate(order)], "slack_times_60": slack,
        })
    full_leaves = [forced[i, a] for i, a in enumerate(full_order)]
    assert all(leaf.count(a) <= 1 for leaf in full_leaves for a in FULL_OMITTED_ORDER)
    full_slack = certificate(full_order, [SCALE] * len(OMITTED_MASKS))
    assert min(full_slack) == 0
    return result, {"order": full_order, "true_leaves": full_leaves, "slack_times_60": full_slack}


def point_checks(actions, leaves, actual, full_certificate, counts):
    def cover(labels):
        selected = label_mask(labels)
        return sum(count for mask, count in zip(MASKS, counts, strict=True) if mask & selected)

    def payoff(leaf, a):
        return sum((Fraction(count, sum(bool(mask & (1 << t)) for t in leaf))
                    for mask, count in zip(MASKS, counts, strict=True) if count and mask & (1 << a)),
                   Fraction(0))

    strict = ties = 0
    for h, a in actions.items():
        real = payoff(leaves[h], a)
        for b in LABELS:
            if a != b:
                other = payoff(leaves[h + (b,)], b)
                assert real >= other, (h, a, b, real, other)
                strict += real > other
                ties += real == other
    assert strict + ties == len(actions) * (len(LABELS) - 1) == 16806

    order = full_certificate["order"]
    forced = [leaves[actual[:i] + (a,)] for i, a in enumerate(order)]
    payments = [Fraction(sum(counts[mask - 1] * weight for mask, weight in zip(
                    OMITTED_MASKS, query_weights(leaf, a), strict=True)), SCALE)
                for a, leaf in zip(order, forced, strict=True)]
    assert all(q <= payoff(leaf, a) <= payoff(actual, actual[i])
               for i, (q, leaf, a) in enumerate(zip(payments, forced, order, strict=True)))
    w = cover(actual)
    v = cover(LABELS)
    assert v - w <= sum(payments) <= w
    supports = {support: cover(support) for support in itertools.combinations(LABELS, PLAYERS)}
    optimum = max(supports.values())
    return {
        "histories": len(actions), "strict": strict, "ties": ties, "clients": sum(counts),
        "W": w, "V": v, "OPT5": optimum, "optimal_five_label_supports": [
            support for support, value in supports.items() if value == optimum],
        "L_all": v - w, "P_components": list(map(str, payments)), "P": str(sum(payments)),
    }


def main(root):
    result = {}
    for key, spec in POLICIES.items():
        actions, leaves, counts, actual, order = read_policy(root, spec)
        support_rows, full_certificate = compare_supports(leaves, actual, order)
        original_point = point_checks(actions, leaves, actual, full_certificate, counts)
        sharp_counts = tuple({1: 3, 2: 2, 4: 1, 8: 1, 16: 1, 32: 1, 64: 1}.get(mask, 0)
                             for mask in MASKS)
        sharp_point = point_checks(actions, leaves, actual, full_certificate, sharp_counts)
        assert (sharp_point["W"], sharp_point["V"], sharp_point["OPT5"], sharp_point["P"]) == (5, 10, 8, "5")
        result[key] = {"actual": actual, "all_supports": support_rows,
                       "full_omission": full_certificate, "original": original_point, "sharp": sharp_point}
    assert result["sigma252"]["original"]["P"] == "199/2"
    assert result["sigma48"]["original"]["P"] == "23"
    print(json.dumps({"scale": SCALE, "omitted_masks": OMITTED_MASKS, "policies": result}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", type=Path)
    main(parser.parse_args().repo_root)
