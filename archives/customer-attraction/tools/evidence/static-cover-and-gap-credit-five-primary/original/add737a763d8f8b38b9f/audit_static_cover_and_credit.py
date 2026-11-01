#!/usr/bin/env python3
"""Definition-level exact audit; no CAG solver/verifier imports.

Reads only existing source instances and full ordered strategies.  Unit customer
multiplicities are expanded.  This is a candidate attack, not a general proof.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "customer_attraction/model.py").is_file())


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def audit(name, uniform=False):
    raw = json.loads((ROOT / f"examples/customer_attraction/{name}.json").read_text())
    m, n = raw["players"], len(raw["topics"])
    customers = tuple(frozenset(t["topics"]) for t in raw["customers"]
                      for _ in range(t["multiplicity"]))
    if name == "general_tax_failure":
        actions = {h: 0 for k in range(m) for h in product(range(n), repeat=k)}
    else:
        source = json.loads((ROOT / f"evidence/certificates/customer_attraction/{name}.json").read_text())
        source = source.get("strategy", source)
        actions = {tuple(t["history"]): t["action"] for t in source["actions"]}
    histories = tuple(h for k in range(m) for h in product(range(n), repeat=k))
    assert set(actions) == set(histories)

    @lru_cache(None)
    def leaf(h):
        return h if len(h) == m else leaf(h + (actions[h],))

    @lru_cache(None)
    def shares(z):
        counts = tuple(sum(a in x for a in z) for x in customers)
        return tuple(tuple(F(int(z[i] in x), c) if c else F(0)
                           for x, c in zip(customers, counts))
                     for i in range(m))

    def payoff(z, i):
        return sum(shares(z)[i], F(0))

    comparisons = 0
    for h in histories:
        i = len(h)
        chosen = payoff(leaf(h), i)
        for a in range(n):
            assert chosen >= payoff(leaf(h + (a,)), i)
            comparisons += 1
    z = leaf(())
    c = tuple(sum(a in x for a in z) for x in customers)
    W = sum(bool(k) for k in c)
    u = tuple(payoff(z, i) for i in range(m))
    tuples = tuple(combinations_with_replacement(range(n), m))
    cover = {T: sum(any(a in x for a in T) for x in customers) for T in tuples}
    O = max(cover.values())
    opts = tuple(T for T in tuples if cover[T] == O)
    role_report = []
    for i in range(m):
        per_opt = []
        a = tuple(int(z[i] in x) for x in customers)
        b = tuple(cx - ax for cx, ax in zip(c, a))
        for T in opts:
            d = tuple(sum(t in x for t in T) for x in customers)
            o = tuple(int(dx > 0) for dx in d)
            E = tuple(F(dx - ax, 1 + bx) - ox + int(cx > 0)
                      for dx, ax, bx, ox, cx in zip(d, a, b, o, c))
            S = sum((F(dx, 1 + bx) for dx, bx in zip(d, b)), F(0))
            query_leaves = tuple(leaf(z[:i] + (t,)) for t in T)
            q = tuple(sum((shares(zz)[i][x] for zz in query_leaves), F(0))
                      for x in range(len(customers)))
            Q = sum(q, F(0))
            ell = tuple(F(dx, 1 + bx) - qx for dx, bx, qx in zip(d, b, q))
            L = sum(ell, F(0))
            assert all(ex >= 0 for ex in E)
            assert F(O - W) == S - u[i] - sum(E)
            assert F(O - W) == Q - u[i] + L - sum(E)
            assert Q <= m * u[i]
            net_groups = [F(0) for _ in range(4)]
            for x, (cx, ax, ox, qx) in enumerate(zip(c, a, o, q)):
                if cx and not ax:
                    assert ell[x] <= E[x]
                if ox and not cx:
                    net_groups[0] += qx - 1
                elif ax and ox:
                    net_groups[1] += qx - F(1, cx)
                elif cx and not ax and ox:
                    net_groups[2] += qx
                elif cx and not ox:
                    net_groups[3] += 1 - F(ax, cx)
            assert sum(net_groups) == sum(E) - L
            assert net_groups[2] >= 0 and net_groups[3] >= 0
            per_opt.append({"T": T, "S": S, "Q": Q, "E": sum(E), "L": L,
                            "net_groups": net_groups, "Q_minus_u_minus_gap": Q-u[i]-(O-W)})
        role_report.append({"i": i, "minimum_surplus": min(p["Q_minus_u_minus_gap"] for p in per_opt),
                            "maximum_surplus": max(p["Q_minus_u_minus_gap"] for p in per_opt),
                            "first_optimum": per_opt[0]})
    report = {"instance": name, "players": m, "unit_customers": len(customers),
              "ordered_decision_histories": len(histories), "comparisons_including_self": comparisons,
              "actual": z, "u": u, "W": W, "OPT": O, "optimal_multiset_count": len(opts),
              "roles": role_report}
    if uniform:
        assert opts == ((1, 2, 3),)
        static_matrix = tuple(tuple(payoff(z[:i] + (t,) + z[i+1:], i) for t in opts[0])
                              for i in range(m))
        uniform_sum = sum((sum(row, F(0)) for row in static_matrix), F(0))
        best_matching = min(sum((static_matrix[i][p[i]] for i in range(m)), F(0))
                            for p in permutations(range(m)))
        assert uniform_sum == F(58, 3) > m*W
        assert best_matching == F(16, 3) < W
        report["uniform_opt_refutation"] = {"static_matrix": static_matrix,
                                             "sum_all_entries": uniform_sum,
                                             "uniform_assignment_value": uniform_sum/m,
                                             "best_matching_value": best_matching}
    return report


def main():
    results = {"status": "Exact finite candidate attack and identity audit; general half remains OPEN",
               "audits": [audit("eight_cce_welfare_gap", uniform=True),
                          audit("root_tax_failure"), audit("general_tax_failure")]}
    text = json.dumps(encode(results), indent=2) + "\n"
    (HERE / "exact_audit.json").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
