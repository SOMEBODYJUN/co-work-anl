"""Exact fixed-input audit, separate from the frozen discovery programs.

Run with Python 3; no third-party dependency.  Insurance IC checks cover only
180 actual-prefix deviations; the all-history SPE theorem is analytic.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text())


def geometry(m, actions, inc, weights, finish):
    z = finish(())
    cols = []
    for i in range(m):
        row = []
        for a in actions:
            leaf = finish(z[:i] + (a,))
            row.append([sum(inc[b][x] for j, b in enumerate(leaf) if j != i)
                        for x in range(len(weights))])
        cols.append(row)
    us = [sum(Q(weights[x] * inc[a][x], 1 + cols[i][actions.index(a)][x])
              for x in range(len(weights))) for i, a in enumerate(z)]
    return z, cols, us


def balance(m, actions, inc, weights, cols, us, p, q):
    n = len(weights)
    assert len(q) == m
    assert all(sum(row) == 1 and min(row) >= 0 for row in q)
    L = [sum(q[i][b] * cols[i][b][x] for i in range(m)
             for b in range(len(actions))) / m for x in range(n)]
    rho = [sum(p[a] * inc[b][x] for a, b in enumerate(actions)) for x in range(n)]
    t = [1 / (1 + l) for l in L]
    val = sum(weights[x] * rho[x] * t[x] for x in range(n))
    C = D = query_total = Q(0)
    ic_count = 0
    for i in range(m):
        for a, b in enumerate(actions):
            d = sum(Q(weights[x] * inc[b][x], 1 + cols[i][a][x]) for x in range(n))
            assert d <= us[i]
            ic_count += 1
            query_total += p[a] * d
            for x in range(n):
                delta = cols[i][a][x] - L[x]
                C += p[a] * weights[x] * inc[b][x] * t[x] ** 2 * delta
                D += p[a] * weights[x] * inc[b][x] * t[x] ** 2 * delta ** 2 / (1 + cols[i][a][x])
    IC = sum(us) - query_total
    assert sum(us) - m * val == IC - C + D
    values = [[sum(weights[x] * rho[x] * t[x] ** 2 * col[x] for x in range(n))
               for col in row] for row in cols]
    residual = max(max(values[i]) - values[i][a]
                   for i in range(m) for a in range(len(actions)) if q[i][a])
    return {"L": L, "F": val, "C": C, "D": D, "IC": IC,
            "W_minus_mF": sum(us) - m * val,
            "KKT_positive_support_residual": residual,
            "actual_prefix_IC_checks": ic_count}


def old36():
    inp = load("related/old36-input.json")
    cert = load("related/old36-strategy.json")
    frozen = load("original/check_shared_load_old36.json")
    actions = tuple(range(6))
    inc = {a: [int(a in c["topics"]) for c in inp["customers"]] for a in actions}
    weights = [c["multiplicity"] for c in inp["customers"]]
    policy = {tuple(r["history"]): r["action"] for r in cert["strategy"]["actions"]}

    def finish(h):
        while len(h) < 3:
            h += (policy[h],)
        return h

    z, cols, us = geometry(3, actions, inc, weights, finish)
    full_ic = 0
    for depth in range(3):
        for h in product(actions, repeat=depth):
            prescribed = finish(h)
            a = prescribed[depth]
            counts = [sum(inc[b][x] for b in prescribed) for x in range(len(weights))]
            value = sum(Q(weights[x] * inc[a][x], counts[x])
                        for x in range(len(weights)) if inc[a][x])
            for b in actions:
                leaf = finish(h + (b,))
                alt_counts = [sum(inc[c][x] for c in leaf) for x in range(len(weights))]
                alt = sum(Q(weights[x] * inc[b][x], alt_counts[x])
                          for x in range(len(weights)) if inc[b][x])
                assert value >= alt
                full_ic += 1
    result = balance(3, actions, inc, weights, cols, us,
                     list(map(Q, frozen["p"])), [[Q(v) for v in row] for row in frozen["q"]])
    for name, key in [("F", "F_shared"), ("C", "C"), ("D", "D"),
                      ("IC", "IC_sum"), ("W_minus_mF", "W_minus_mF")]:
        assert result[name] == Q(frozen[key])
    assert result["C"] < 0 and result["KKT_positive_support_residual"] > 0
    result.update({"actual_leaf": z, "utilities": us, "unit_customers": sum(weights),
                   "complete_history_nodes": len(policy), "all_history_IC_checks": full_ic,
                   "frozen_fields_reproduced_exactly": True,
                   "rational_q_is_exact_optimizer": False})
    return result


def insurance():
    m = 6
    actions = tuple(product(range(m), range(m - 1)))
    inc = {a: [int(x == a[0]) for x in range(m)]
           + [int(x == a[1]) for x in range(m - 1)] for a in actions}
    weights = [1] * m + [2] * (m - 1)

    @lru_cache(None)
    def action(h):
        if not h:
            return (0, 0)
        anchor_e, anchor_b = h[0]
        mode, target = "BASE", None
        used_b = {anchor_b}
        for a in h[1:]:
            if mode == "BASE" and a != (anchor_e, min(set(range(m - 1)) - used_b)):
                mode = "EXIT" if a[1] in used_b else "PUNISH"
                if mode == "PUNISH":
                    target = a[1]
            elif mode == "PUNISH" and a[1] in used_b:
                mode = "EXIT"
            used_b.add(a[1])
        fresh_e = set(range(m)) - {a for a, b in h}
        fresh_b = set(range(m - 1)) - used_b
        last = len(h) == m - 1
        if mode == "BASE":
            return (min(fresh_e), anchor_b) if last else (anchor_e, min(fresh_b))
        if mode == "PUNISH" and last:
            return (min(fresh_e), target)
        return (min(fresh_e), min(fresh_b))

    @lru_cache(None)
    def finish(h):
        return h if len(h) == m else finish(h + (action(h),))

    z, cols, us = geometry(m, actions, inc, weights, finish)
    sparse = [{5: Q(1, 5), 20: Q(7, 20), 25: Q(9, 20)}, {10: Q(1)},
              {0: Q(3, 5), 10: Q(1, 5), 15: Q(1, 5)}, {5: Q(1)}, {5: Q(1)}, {0: Q(1)}]
    q = [[row.get(a, Q(0)) for a in range(30)] for row in sparse]
    p = [Q(1, 30)] * 30
    result = balance(m, actions, inc, weights, cols, us, p, q)
    exact = load("related/insurance-covariance-exact.json")
    for name, key in [("F", "F_optimum"), ("C", "C"), ("D", "D"),
                      ("IC", "IC"), ("W_minus_mF", "W_minus_mF")]:
        assert result[name] == Q(exact[key])
    assert result["L"] == list(map(Q, exact["L"]))
    assert result["KKT_positive_support_residual"] == 0
    mins = [min(c[0] for c in row) for row in cols]
    assert mins == [1, 1, 2, 3, 4, 5]
    assert all(sum(c[:6]) == 5 and sum(c[6:]) == 5 for row in cols for c in row)

    frozen = load("original/insurance_shared_covariance_m6.json")
    fq = frozen["q"]
    fl = [sum(fq[i][a] * cols[i][a][x] for i in range(m) for a in range(30)) / m
          for x in range(11)]
    rho = [1 / 6] * 6 + [1 / 5] * 5
    ft = [1 / (1 + l) for l in fl]
    fv = sum(weights[x] * rho[x] * ft[x] for x in range(11))
    fc = sum(p[a] * weights[x] * inc[b][x] * ft[x] ** 2 * (cols[i][a][x] - fl[x])
             for i in range(m) for a, b in enumerate(actions) for x in range(11))
    fd = sum(p[a] * weights[x] * inc[b][x] * ft[x] ** 2 * (cols[i][a][x] - fl[x]) ** 2
             / (1 + cols[i][a][x]) for i in range(m) for a, b in enumerate(actions) for x in range(11))
    float_errors = {"L": max(abs(fl[x] - frozen["L"][x]) for x in range(11)),
                    "F": abs(fv - frozen["F"]), "C": abs(fc - frozen["C"]),
                    "D": abs(fd - frozen["D"]), "IC": abs(float(result["IC"]) - frozen["IC"])}
    assert max(float_errors.values()) < 1e-10
    result.update({"actual_leaf": z, "utilities": us, "unit_customers": sum(weights),
                   "menu_minimum_anchor_load": mins, "frozen_float_field_errors": float_errors,
                   "frozen_float_row_sum_error": max(abs(sum(row) - 1) for row in fq),
                   "frozen_float_min_probability": min(map(min, fq)),
                   "fixed_uniform_p_exact_KKT": True,
                   "full_SPE_scope": "Inherited all-m analytic controller theorem; no all-tree enumeration here"})
    return result


def encode(v):
    if isinstance(v, Q):
        return str(v)
    raise TypeError(type(v).__name__)


if __name__ == "__main__":
    result = {"old36": old36(), "insurance_m6": insurance(), "all_checks_passed": True,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out = HERE / "verification.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False, default=encode) + "\n")
    print(out.read_text())
