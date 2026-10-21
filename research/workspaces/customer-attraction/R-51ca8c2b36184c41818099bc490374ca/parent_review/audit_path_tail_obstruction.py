"""Independent definition-level audit of the path-plus-tail relaxation.

Each theme is a disjoint block of distinct unit customers.  This audit uses
only block cardinality/counting and does not import the author's implementation
or the repository SPE solver.  The symbolic proof remains necessary for all m.
"""

from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from math import lcm
import json
from pathlib import Path


def case(m, k, radius=0):
    assert 1 <= k < m
    n = m-k
    assert 0 <= radius < n
    d = n-radius
    scale = lcm(*range(1, d+1))
    sizes = tuple(scale//max(n-i-radius, 1) for i in range(n))+(scale,)*m

    def action(h):
        if len(h) >= n:
            return next(a for a in range(n, n+m) if a not in h)
        wrong = tuple(a for i, a in enumerate(h) if a != i)
        if not wrong:
            return len(h)
        if len(wrong) <= radius:
            return next(a for a in range(n, n+m) if a not in h)
        return wrong[0]

    def complete(h):
        while len(h) < m:
            h = h+(action(h),)
        return h

    def utility(h, a):
        assert len(h) == m and a in h
        return F(sizes[a], h.count(a))

    path = complete(())
    welfare = sum(sizes[a] for a in set(path))
    optimum = sum(sorted(sizes, reverse=True)[:m])
    harmonic = sum((F(1, j) for j in range(1, d+1)), F(0))
    assert welfare == scale*(harmonic+radius+k)
    assert optimum == m*scale
    checks = 0
    min_slack = None
    for i in range(m):
        h = path[:i]
        u = utility(path, path[i])
        for a in range(len(sizes)):
            v = utility(complete(h+(a,)), a)
            slack = u-v
            assert slack >= 0, (m, k, h, a, slack)
            min_slack = slack if min_slack is None else min(min_slack, slack)
            checks += 1

    # Every arbitrary ordered tail history has a count state in this list.
    # The tail policy and all subsequent terminal utilities depend only on
    # this count state, so a sorted representative checks each distinct state.
    tail_checks = 0
    if radius == 0 and (m, k) in ((2, 1), (3, 1), (4, 2), (5, 2), (7, 1)):
        for depth in range(n, m):
            for h in combinations_with_replacement(range(len(sizes)), depth):
                chosen = action(h)
                actual = complete(h)
                u = utility(actual, chosen)
                assert u == scale
                for a in range(len(sizes)):
                    assert u >= utility(complete(h+(a,)), a)
                    tail_checks += 1

    # Full uncompressed ordered-history check for small cases; do not assert
    # SPE.  The point is that off-path early incentive inequalities fail.
    full_checks = 0
    negative = []
    if m <= 4:
        for depth in range(m):
            for h in product(range(len(sizes)), repeat=depth):
                actual = complete(h)
                u = utility(actual, action(h))
                for a in range(len(sizes)):
                    slack = u-utility(complete(h+(a,)), a)
                    full_checks += 1
                    if slack < 0:
                        distance = sum(a != j for j, a in enumerate(h))
                        assert depth < n and distance > radius
                        negative.append((h, a, str(slack)))

    first_offpath = None
    if d >= 2:
        h = tuple(range(n, n+radius+1))
        u = utility(complete(h), action(h))
        fresh = n+radius+1
        v = utility(complete(h+(fresh,)), fresh)
        assert u == F(scale, d) and v == scale and u < v
        first_offpath = {"history": h, "u": str(u), "deviation_u": str(v)}

    return {
        "m": m, "k": k, "radius": radius, "n": n, "d": d, "scale": scale,
        "W": welfare, "OPT": optimum, "ratio": str(F(optimum, welfare)),
        "OPT_minus_2W": optimum-2*welfare,
        "all_path_comparisons": checks, "tail_count_comparisons": tail_checks,
        "full_ordered_comparisons": full_checks,
        "negative_offpath_early_comparisons": len(negative),
        "first_offpath_failure": first_offpath,
    }


def main():
    records = [case(m, k, r) for m in range(2, 16)
               for k in range(1, m) for r in range(m-k)]
    bad = [x for x in records if x["OPT_minus_2W"] > 0]
    first = {}
    for x in bad:
        first.setdefault(f'k{x["k"]}_r{x["radius"]}', x["m"])
    report = {
        "status": "exact finite implementation audit; not a general proof or SPE counterexample",
        "cases": len(records), "first_half_failures_per_k_in_range": first,
        "records": records,
    }
    out = Path(__file__).with_name("path_tail_obstruction_audit.json")
    out.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({key: value for key, value in report.items() if key != "records"}))
    print(json.dumps(next(x for x in records if x["m"] == 7 and x["k"] == 1)))


if __name__ == "__main__":
    main()
