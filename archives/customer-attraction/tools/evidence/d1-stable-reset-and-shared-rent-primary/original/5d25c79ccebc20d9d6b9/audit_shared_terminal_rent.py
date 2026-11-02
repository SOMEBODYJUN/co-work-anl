"""Exact finite replay of the stated shared terminal-rent family.

No canonical solver or model imports. Enumerates every ordered decision history
and every action, follows the explicit actual continuation, and compares Fraction
utilities from explicit distinct unit customers. This audits finite examples;
the accompanying analytic proof carries the arbitrary n,K quantifiers.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json


def build(n, k, s):
    next_customer = 0
    def block(size):
        nonlocal next_customer
        ans = frozenset(range(next_customer, next_customer + size))
        next_customer += size
        return ans
    q = block(n * s)
    rs = [block(n * s) for _ in range(k)]
    y = block(s)
    xs = [block(s) for _ in range(k)]
    b = q.union(*rs)
    themes = [b, (b - q) | y] + [(b - r) | x for r, x in zip(rs, xs)]
    return themes, q, y


def action(h, n, mode):
    if mode == "all_B":
        return 0
    return 1 if len(h) == n - 1 and 1 not in h else 0


def leaf(h, n, mode):
    h = tuple(h)
    while len(h) < n:
        h += (action(h, n, mode),)
    return h


def utilities(z, themes):
    counts = {}
    for a in z:
        for x in themes[a]:
            counts[x] = counts.get(x, 0) + 1
    us = [sum((F(1, counts[x]) for x in themes[a]), F(0)) for a in z]
    return us, len(counts)


def audit(n, k, s):
    themes, q, y = build(n, k, s)
    p = len(themes)
    checks = 0
    histories = 0
    for mode in ("terminal_T", "all_B"):
        for d in range(n):
            for h in product(range(p), repeat=d):
                histories += 1
                z = leaf(h, n, mode)
                current = utilities(z, themes)[0][d]
                for alt in range(p):
                    altz = leaf(h + (alt,), n, mode)
                    dev = utilities(altz, themes)[0][d]
                    checks += 1
                    assert current >= dev, (n, k, mode, h, alt, current, dev)

    actual = leaf((), n, "terminal_T")
    actual_us, welfare = utilities(actual, themes)
    base_us, _ = utilities(leaf((), n, "all_B"), themes)
    amp = F(s, n - 1)
    assert actual_us[0] - base_us[0] == amp
    branch_records = []
    for root in [0] + list(range(2, p)):
        z = leaf((root,), n, "terminal_T")
        assert z[-1] == 1 and all(a != 1 for a in z[:-1])
        switched = z[:-1] + (0,)
        old_u, _ = utilities(z, themes)
        new_u, _ = utilities(switched, themes)
        assert all(old_u[j] - new_u[j] == amp for j in range(n - 1))
        assert old_u[-1] == new_u[-1]
        # Four terms at the actual final T node; background b=0.
        loads = {x: sum(x in themes[a] for a in z[:-1]) for x in themes[0] | themes[1]}
        alpha = sum((F(1) for x in themes[1] - themes[0]), F(0))
        beta = sum((F(1, n) for x in themes[0] - themes[1]), F(0))
        a_term = sum((F(1) - F(1, loads[x] + 1) for x in y), F(0))
        e_term = sum((F(1, loads[x] + 1) - F(1, n) for x in q), F(0))
        gamma = old_u[-1] - new_u[-1]
        zeta = F(0)  # no future player at this final decision node
        assert alpha == beta == s
        assert a_term == e_term == gamma == zeta == 0
        branch_records.append({"root": root, "leaf": z, "epsilon": str(amp), "four_terms": ["0"] * 4})

    # At most n distinct themes suffice; repeating is never useful for coverage.
    opt = 0
    for r in range(1, min(n, p) + 1):
        for chosen in combinations(range(p), r):
            opt = max(opt, len(frozenset().union(*(themes[a] for a in chosen))))
    assert welfare == (k + 1) * n * s + s
    assert opt == (k + 1) * n * s + min(n, k + 1) * s
    assert actual_us[0] == F((k + 1) * s) + amp
    return {
        "n": n, "K": k, "s": s, "unit_customers": len(frozenset().union(*themes)),
        "themes": [sorted(a) for a in themes], "ordered_histories_both_policies": histories,
        "exact_action_comparisons": checks, "actual_leaf": actual,
        "root_high": str(actual_us[0]), "root_minimum_by_raw_B_bound_and_all_B_SPE": str(base_us[0]),
        "effective_amplitude": str(amp), "W": welfare, "OPT": opt,
        "half_slack": 2 * welfare - opt, "shared_Q": sorted(q),
        "branches": branch_records, "unweighted_branch_rent_sum": str((k + 1) * amp),
    }


if __name__ == "__main__":
    cases = [(2, 1, 1), (2, 12, 1), (3, 1, 1), (3, 7, 1), (4, 3, 1), (5, 3, 1), (4, 2, 2)]
    report = {
        "status": "all_exact_checks_passed_finite_audit_only",
        "cases": [audit(*c) for c in cases],
    }
    report["total_comparisons"] = sum(c["exact_action_comparisons"] for c in report["cases"])
    output = Path(__file__).with_name("shared_terminal_rent_audit.json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "cases": len(cases), "comparisons": report["total_comparisons"]}))
