"""Exact arithmetic unpacking of already verified coupling witnesses.

This is a cleanup supplement. It does not discover an LP point or repeat the
original full-tree incentive/dual verification. Those obligations are recorded
in replay/verification.json and the unchanged original verifier.
"""
from ast import literal_eval
from fractions import Fraction as F
from itertools import combinations
from math import lcm
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent


def coverage(weights, labels):
    mask = sum(1 << a for a in labels)
    return sum(w for typ, w in weights.items() if typ & mask)


def profits(weights, path):
    return [
        sum((F(w, sum(bool(typ >> b & 1) for b in path))
             for typ, w in weights.items() if typ >> a & 1), F(0))
        for a in path
    ]


def summaries(weights):
    supports = [
        s for k in range(4) for s in combinations(range(6), k)
    ]
    best = max(coverage(weights, s) for s in supports)
    return {
        "total_customers": sum(weights.values()),
        "root_path": [0, 3, 4],
        "root_coverage": coverage(weights, (0, 3, 4)),
        "root_payoffs": [str(x) for x in profits(weights, (0, 3, 4))],
        "fixed_comparison": [1, 2, 4],
        "fixed_comparison_coverage": coverage(weights, (1, 2, 4)),
        "best_over_all_42_supports_of_size_at_most_3": best,
        "maximizing_supports": [list(s) for s in supports if coverage(weights, s) == best],
        "equal_coverage_label_pairs": [
            [a, b] for a in range(6) for b in range(a + 1, 6)
            if not any(w and bool(typ >> a & 1) != bool(typ >> b & 1)
                       for typ, w in weights.items())
        ],
    }


def main():
    primary_path = BASE / "original/coupling_layers.json"
    primary_bytes = primary_path.read_bytes()
    assert hashlib.sha256(primary_bytes).hexdigest() == (
        "184a07294fed638d4202e153da4fd691e2349225041574bd8943193d834ef281"
    )
    original = json.loads(primary_bytes)
    reviewed = json.loads((BASE / "replay/verification.json").read_text())
    assert reviewed["exact"] and len(reviewed["layers"]) == 7
    point = {int(k): F(v) for k, v in original["layers"][-1]["positive_values"].items()}
    scale = lcm(*(v.denominator for v in point.values()))
    assert scale == 138
    integer_base = {typ: int(w * scale) for typ, w in point.items()}
    assert all(w * scale == integer_base[typ] for typ, w in point.items())

    seed_path = BASE.parent / "stationary-pair-transport/examples/customer_attraction/root_stationary_kernel.json"
    seed_bytes = seed_path.read_bytes()
    assert hashlib.sha256(seed_bytes).hexdigest() == (
        "1f849141d40f8bf7335aa0fd42304d2d4b00a0e167b169eef212688e9d4c5dbc"
    )
    seed_source = json.loads(seed_bytes)
    seed = {}
    for customer in seed_source["customers"]:
        typ = sum(1 << a for a in customer["topics"])
        seed[typ] = seed.get(typ, 0) + customer["multiplicity"]

    actions = {tuple(x["history"]): x["action"] for x in original["strategy_actions"]}
    for h, a in actions.items():
        if len(h) == 0:
            expected = 0
        elif len(h) == 1:
            expected = 3 if h[0] < 3 else 0
        else:
            group = range(3) if h[1] < 3 else range(3, 6)
            expected = min(x for x in group if x not in h)
        assert a == expected
    assert len(actions) == 43

    base_summary = summaries(integer_base)
    seed_summary = summaries(seed)
    combined = {typ: integer_base.get(typ, 0) + seed.get(typ, 0)
                for typ in integer_base.keys() | seed.keys()}
    combined_summary = summaries(combined)
    assert base_summary["total_customers"] == 198
    assert base_summary["root_coverage"] == 138
    assert base_summary["root_payoffs"] == ["48", "48", "42"]
    assert base_summary["fixed_comparison_coverage"] == 198
    assert base_summary["maximizing_supports"] == [[1, 2, 4]]
    assert base_summary["equal_coverage_label_pairs"] == [[0, 3]]
    assert seed_summary["total_customers"] == 22
    assert seed_summary["root_coverage"] == 17
    assert seed_summary["root_payoffs"] == ["6", "6", "5"]
    assert seed_summary["fixed_comparison_coverage"] == 19
    assert seed_summary["equal_coverage_label_pairs"] == []
    assert combined_summary["root_coverage"] == 155
    assert combined_summary["best_over_all_42_supports_of_size_at_most_3"] == 217
    assert combined_summary["root_payoffs"] == ["54", "54", "47"]
    assert combined_summary["maximizing_supports"] == [[1, 2, 4]]
    assert combined_summary["equal_coverage_label_pairs"] == []

    pair_point = {
        literal_eval(k): F(v)
        for k, v in original["layers"][1]["positive_values"].items()
    }
    def value(q, a):
        return pair_point.get((tuple(q), a), F(0))
    A = value([3, 0, 0, 0, 0, 0], 0)
    B = value([0, 3, 0, 0, 0, 0], 1)
    X = value([2, 1, 0, 0, 0, 0], 0)
    Y = value([2, 1, 0, 0, 0, 0], 1)
    Z = value([1, 2, 0, 0, 0, 0], 0)
    W = value([1, 2, 0, 0, 0, 0], 1)
    assert Z - Y == 3 * (A - B)
    assert X - W == F(3, 2) * (A - B)
    assert 2 * X + Y == Z + 2 * W
    assert 2 * X + 2 * W - Z - 3 * B == F(2, 21)

    out = {
        "scope": "cleanup arithmetic supplement; no optimizer; original full-tree/dual verification is separate",
        "unit_scale": scale,
        "unit_base": {str(k): v for k, v in sorted(integer_base.items())},
        "base": base_summary,
        "seed": seed_summary,
        "family": {
            "parameter": "integer N >= 1",
            "type_multiplicity_linear_N_constant": {
                str(typ): [integer_base.get(typ, 0), seed.get(typ, 0)]
                for typ in sorted(integer_base.keys() | seed.keys())
            },
            "total_customers": "198*N+22",
            "root_coverage": "138*N+17",
            "root_payoffs": ["48*N+6", "48*N+6", "42*N+5"],
            "OPT3": "198*N+19",
            "unique_maximizing_support": [1, 2, 4],
            "general_OPT_reason": "Every other <=3-label support misses a singleton type of size at least 23*N in the base; seed gain over T is at most 3.",
            "ratio_gap_below_33_over_23": "124/(23*(138*N+17))",
            "N1": combined_summary,
            "full_SPE_reason": "For each of the 258 original fixed-strategy IC rows: N times verified base slack plus verified seed slack is nonnegative.",
            "SPE_not_reenumerated_by_this_supplement": True,
        },
        "old_selected_pair_missing_identity": {
            "pair": [0, 1],
            "variables": {k: str(v) for k, v in zip(["A", "B", "X", "Y", "Z", "W"], [A, B, X, Y, Z, W])},
            "two_selected_difference_equalities": True,
            "same_support_total": True,
            "2X+2W-Z-3B": "2/21",
        },
        "policy_rule_matches_frozen_43_actions": True,
    }
    target = BASE / "replay/derived-unit-family-and-pair-gap.json"
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "scope": out["scope"], "unit_scale": scale,
        "base_customers": 198, "base_W": 138, "base_OPT3": 198,
        "N1_customers": 220, "N1_W": 155, "N1_OPT3": 217,
        "selected_pair_missing_identity_gap": "2/21",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
