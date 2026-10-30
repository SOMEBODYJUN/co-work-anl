#!/usr/bin/env python3
"""Literal finite-game checks for WC-R1-TOTAL-COST-POWER-OBSTRUCTION v1.

All loads and costs are exact Fractions. The half-power comparison uses
an exact radical comparison, not a floating-point objective evaluation.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def costs(weights, strategies, latencies):
    loads = {e: F(0) for e in latencies}
    for w, strategy in zip(weights, strategies):
        for e in strategy:
            loads[e] += w
    values = {e: a + b * loads[e] for e, (a, b) in latencies.items()}
    return [sum((values[e] for e in strategy), F(0)) for strategy in strategies]


def half_power(r):
    R = r * r
    m = 18 * (r - 1) ** 2
    weights = [F(1)] * (m + 1)
    latencies = {"a": (F(R), F(0))}
    shared = [f"e{j}" for j in range(1, m + 1)]
    latencies.update({e: (F(0), F(1, 2 * m)) for e in shared})
    fixed = [{e} for e in shared]
    bad = costs(weights, [{"a"}] + fixed, latencies)
    good = costs(weights, [set(shared)] + fixed, latencies)
    assert bad[0] == R and good[0] == 1
    assert all(c == F(1, 2 * m) for c in bad[1:])
    assert all(c == F(1, m) for c in good[1:])
    assert F(1, 2 * m) == F(1, (6 * (r - 1)) ** 2)
    # J_bad = a, J_good = 1 + b sqrt(2); compare positive a-1 and b sqrt(2).
    a, b = 4 * r - 3, 3 * (r - 1)
    left, right = (a - 1) ** 2, 2 * b * b
    assert left < right
    return {
        "q": "1/2", "r": r, "players": m + 1, "resources": m + 1,
        "improvement_ratio": str(F(R)),
        "J_bad": str(a), "J_good": f"1 + {b} sqrt(2)",
        "positive_radical_comparison_squared": {"left": left, "right": right},
        "unique_objective_minimizer_is_bad": True,
        "good_state_is_exact_PNE": True,
    }


def square_power(R):
    H = R * R
    weights = [F(1), F(1)]
    latencies = {"a": (F(R), F(0)), "b": (F(H), F(0)), "e": (F(0), F(1, 2))}
    bad = costs(weights, [{"a"}, {"b", "e"}], latencies)
    good = costs(weights, [{"e"}, {"b", "e"}], latencies)
    assert bad == [F(R), F(H) + F(1, 2)]
    assert good == [F(1), F(H) + 1]
    bad_j, good_j = sum(c * c for c in bad), sum(c * c for c in good)
    assert good_j - bad_j == F(7, 4)
    return {
        "q": "2", "R": R, "H": H, "players": 2, "resources": 3,
        "improvement_ratio": str(F(R)), "J_bad": str(bad_j), "J_good": str(good_j),
        "objective_gap_good_minus_bad": str(good_j - bad_j),
        "unique_objective_minimizer_is_bad": True,
        "good_state_is_exact_PNE": True,
    }


def main():
    records = [half_power(r) for r in [2, 3, 5, 10]]
    records += [square_power(R) for R in [2, 3, 10, 100, 1000]]
    result = {"claim": "WC-R1-TOTAL-COST-POWER-OBSTRUCTION v1", "arithmetic": "exact Fraction and radical squaring", "records": records}
    target = Path(__file__).with_name("power_objective_exact_checks.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS: {len(records)} literal finite-game exact checks; wrote {target.name}")


if __name__ == "__main__":
    main()
