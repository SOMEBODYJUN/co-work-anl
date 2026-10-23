"""Definition-level ordered-history audit; no CAG imports or optimizer."""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def build(m, a):
    bank = frozenset(range(m*a+1))
    covers = [bank]
    blocks = []
    cursor = len(bank)
    for _ in range(m-1):
        q = frozenset(range(cursor, cursor+a))
        cursor += a
        blocks.append(q)
        covers.extend((q | {0}, q | {1}))
    return tuple(covers), tuple(blocks), cursor


def utility(covers, path, who):
    return sum((Fraction(1, sum(x in covers[t] for t in path))
                for x in covers[path[who]]), Fraction(0))


def audit(m, a):
    covers, blocks, total = build(m, a)
    p = len(covers)
    assert len(set(covers)) == p
    assert all(not (x < y) for x in covers for y in covers)
    histories = comparisons = ties = 0
    minimum = None
    for depth in range(m):
        for h in product(range(p), repeat=depth):
            actual = h + (0,) * (m-depth)
            actual_u = utility(covers, actual, depth)
            histories += 1
            for t in range(p):
                branch = h + (t,) + (0,) * (m-depth-1)
                slack = actual_u - utility(covers, branch, depth)
                assert slack >= 0, (m, a, h, t, slack)
                comparisons += 1
                ties += slack == 0
                minimum = slack if minimum is None else min(minimum, slack)
    union = frozenset().union(*covers)
    actual_union = covers[0]
    optimum = max(len(frozenset().union(*(covers[j] for j in support)))
                  for r in range(1, min(m, p)+1)
                  for support in combinations(range(p), r))
    missed = union - actual_union
    assert len(union) == total == (2*m-1)*a+1
    assert len(actual_union) == m*a+1
    assert optimum == total
    assert all(sum(x in t for t in covers) == 2 for x in missed)
    assert missed == frozenset().union(*blocks)
    assert Fraction(optimum, len(actual_union)) == (
        2 - Fraction(1, m) - Fraction(m-1, m*(m*a+1)))
    return {"players": m, "block_size": a, "topics": p,
            "unit_customers": total, "ordered_histories": histories,
            "action_comparisons_including_self": comparisons,
            "zero_slacks": ties, "minimum_slack": str(minimum),
            "welfare": len(actual_union), "optimum": optimum,
            "ratio": str(Fraction(optimum, len(actual_union))),
            "omitted_customers": len(missed), "omitted_maximal_degree": 2,
            "actual_only_waste": 0}


def small_certificate():
    m, a = 3, 2
    covers, _, total = build(m, a)
    p = len(covers)
    return {"players": m, "unit_customer_count": total,
            "topics": [sorted(t) for t in covers],
            "actions": [{"history": list(h), "action": 0}
                        for depth in range(m)
                        for h in product(range(p), repeat=depth)],
            "actual_path": [0]*m}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    reports = [audit(m, a) for m in range(2, 6) for a in (1, 3)]
    report = {"status": "definition_level_exact_pass",
              "scope": "Eight finite full ordered-history trees; arbitrary parameters rely on the analytic proof.",
              "cases": reports,
              "totals": {"ordered_histories": sum(x["ordered_histories"] for x in reports),
                         "action_comparisons_including_self": sum(x["action_comparisons_including_self"] for x in reports)},
              "complete_finite_certificate": small_certificate()}
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as f:
            f.write(payload)
    print(json.dumps({k: v for k, v in report.items() if k != "complete_finite_certificate"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
