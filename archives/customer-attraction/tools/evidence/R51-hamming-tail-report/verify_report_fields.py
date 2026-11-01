"""Check all frozen report fields from independent finite formulas.

No import or execution of audit_hamming_tail.py.  This checks report semantics,
enumeration cardinalities, roots and explicit negative witnesses.  It does not
re-enumerate every IC: the original generator and the published analytic proof
carry that separate responsibility.
"""
from fractions import Fraction
from math import comb, lcm
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent


def no_future_count(depth, m, radius):
    # At coordinate j, all incorrect labels except future A labels number m+j.
    elementary = [1] + [0] * radius
    for j in range(depth):
        for degree in range(min(radius, j + 1), 0, -1):
            elementary[degree] += (m + j) * elementary[degree - 1]
    return sum(elementary)


def expected_row(m, k, radius):
    n = m - k
    degree = n - radius
    labels = n + m
    scale = lcm(*range(1, degree + 1))
    near_histories = sum(
        sum(comb(t, errors) * (labels - 1) ** errors
            for errors in range(min(radius, t) + 1))
        for t in range(n)
    )
    future = near_histories - sum(
        no_future_count(t, m, radius) for t in range(n)
    )
    welfare = scale * (
        sum((Fraction(1, j) for j in range(1, degree + 1)), Fraction())
        + radius + k
    )
    assert welfare.denominator == 1
    welfare = int(welfare)
    optimum = m * scale
    row = {
        "m": m, "k": k, "r": radius, "d": degree, "L": scale,
        "near_comparisons": labels * near_histories,
        "tail_comparisons": sum(labels ** (t + 1) for t in range(n, m)),
        "near_histories_with_future_A": future,
        # Every kept node compares its own action, and the stated local proof
        # makes all other comparisons nonnegative; the true minimum is zero.
        "minimum_margin": "0",
        "root": {"path": list(range(m)), "W": welfare, "OPT": optimum,
                 "ratio": str(Fraction(optimum, welfare))},
    }
    if degree >= 2:
        row["far_violation"] = {
            "history": list(range(n, n + radius + 1)),
            "chosen": n,
            "deviation": n + radius + 1,
            "actual": str(Fraction(scale, degree)),
            "deviation_utility": str(scale),
            "margin": str(Fraction(scale, degree) - scale),
        }
    else:
        # For d=1, radius=n-1.  Every early history has distance <=t<=radius.
        assert radius == n - 1
        assert near_histories == sum(labels ** t for t in range(n))
        assert row["near_comparisons"] + row["tail_comparisons"] == sum(
            labels ** (t + 1) for t in range(m)
        )
        assert welfare == optimum
    return row


def main():
    original = HERE / "original/hamming_tail_audit.json"
    raw = original.read_bytes()
    assert len(raw) == 9758
    assert hashlib.sha256(raw).hexdigest() == (
        "b7fc7c50c846c63983dfc8747bf0e3acc33fb0a9bd16f0d18eebc11fafcf7199"
    )
    actual = json.loads(raw)
    rows = [expected_row(m, k, radius)
            for m in range(2, 6)
            for k in range(1, m)
            for radius in range(m-k)]
    # Dictionary equality checks all keys and values, not a selected subset.
    assert actual == {"status": "PASS", "instances": 20, "reports": rows}
    totals = {
        "near_comparisons": sum(row["near_comparisons"] for row in rows),
        "tail_comparisons": sum(row["tail_comparisons"] for row in rows),
        "near_histories_with_future_A": sum(
            row["near_histories_with_future_A"] for row in rows
        ),
    }
    assert totals == {"near_comparisons": 12205,
                      "tail_comparisons": 406555,
                      "near_histories_with_future_A": 640}
    full = [row for row in rows if row["d"] == 1]
    negative = [row for row in rows if "far_violation" in row]
    assert len(full) == len(negative) == 10
    assert all(2 * row["root"]["W"] >= row["root"]["OPT"] for row in rows)
    result = {
        "status": "PASS",
        "scope": "all-frozen-fields-via-independent-combinatorial-and-rational-formulas",
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "instances": len(rows),
        "totals": totals,
        "d1_complete_history_coverage": [
            {"m": row["m"], "k": row["k"], "r": row["r"],
             "labels": 2*row["m"]-row["k"],
             "all_history_action_comparisons":
                 row["near_comparisons"] + row["tail_comparisons"],
             "W": row["root"]["W"], "OPT": row["root"]["OPT"]}
            for row in full
        ],
        "explicit_negative_witnesses": len(negative),
        "all_twenty_roots_satisfy_half": True,
        "original_generator_executed_by_this_checker": False,
        "all_ICs_reenumerated_by_this_checker": False,
    }
    print(json.dumps(result, indent=2) + "\n", end="")


if __name__ == "__main__":
    main()
