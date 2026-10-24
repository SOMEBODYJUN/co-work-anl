"""Independent exact finite audit of the last-successor peeling identity.

The universal statement is proved algebraically, not by this finite audit.
No author implementation, game solver, or floating-point arithmetic is used.
Run from any directory; JSON is written beside this file.
"""
from fractions import Fraction as Q
from itertools import product
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import platform


def audit():
    counts = {k: 0 for k in (
        "games", "complete_policies", "full_SPE_policies", "identity_checks",
        "path_identity_checks", "nonanonymous_SPE_policies", "SPE_comparisons")}
    extrema = {"minimum_delta": None, "minimum_paid_balance": None}
    witness = None
    # Each incidence copy is a distinct unit customer. The empty incidence
    # contributes nothing and is retained in selected cases as a boundary.
    distributions = ((Q(1), Q(0)), (Q(0), Q(1)),
                     (Q(1, 3), Q(2, 3)), (Q(1, 2), Q(1, 2)))
    for m in (1, 2, 3):
        histories = tuple(h for d in range(m) for h in product(range(2), repeat=d))
        for mult in product(range(3), repeat=3):
            customers = tuple(mask for mask, n in zip((1, 2, 3), mult)
                              for _ in range(n))
            counts["games"] += 1
            for choices in product(range(2), repeat=len(histories)):
                actions = dict(zip(histories, choices))
                counts["complete_policies"] += 1

                def contains(x, a):
                    return int(a is not None and bool(x & (1 << a)))

                def load(h):
                    return tuple(sum(contains(x, a) for a in h) for x in customers)

                @lru_cache(None)
                def leaf(h):
                    return h if len(h) == m else leaf(h + (actions[h],))

                def utility(h, a):
                    return sum((Q(contains(x, a), c) for x, c in zip(customers, load(h))
                                if contains(x, a)), Q(0))

                valid = True
                for h in histories:
                    selected = utility(leaf(h), actions[h])
                    for a in range(2):
                        counts["SPE_comparisons"] += 1
                        if selected < utility(leaf(h + (a,)), a):
                            valid = False
                if valid:
                    counts["full_SPE_policies"] += 1
                    if m == 3 and actions[(0, 1)] != actions[(1, 0)]:
                        counts["nonanonymous_SPE_policies"] += 1

                def row(h, p):
                    r = m - len(h)
                    # h_A excludes the forced current and original last slots.
                    leaves = {a: leaf(h + (a,)) for a in range(2)}
                    bg = {a: load(h + leaves[a][len(h) + 1:-1])
                          if r >= 2 else load(h) for a in range(2)}
                    last = {a: leaves[a][-1] if r >= 2 else None for a in range(2)}

                    def U(b, a, t):
                        return sum((Q(1, c + 1 + contains(x, t))
                                    for x, c in zip(customers, b) if contains(x, a)), Q(0))

                    def F0(b, a):
                        return U(b, a, None)

                    def phi(b, a, t):
                        return U(b, a, t) + F0(b, t)

                    D = sum((p[a] * U(bg[a], a, last[a]) for a in range(2)), Q(0))
                    F = C = L = delta = J = delta7 = delta8 = Q(0)
                    c_cols = []
                    for a in range(2):
                        c_col = Q(0)
                        for t in range(2):
                            wt = p[a] * p[t]
                            f = U(bg[a], t, last[a])
                            c = sum((Q(1, z + 1 + contains(x, a) + contains(x, last[a]))
                                     for x, z in zip(customers, bg[a]) if contains(x, t)), Q(0))
                            F += wt * f
                            C += wt * c
                            c_col += p[t] * c
                            j = sum((Q(1, (z + contains(x, last[a]) + 1) *
                                            (z + contains(x, last[a]) + 2))
                                     for x, z in zip(customers, bg[a])
                                     if contains(x, a) and contains(x, t)), Q(0))
                            J += wt * j
                            if r >= 2:
                                ell = U(bg[a], last[a], a) - U(bg[a], last[t], a)
                                if valid:
                                    assert ell >= 0
                                L += wt * ell
                                delta += wt * (phi(bg[a], a, last[t]) - phi(bg[t], a, last[t]))
                                for x, za, zt in zip(customers, bg[a], bg[t]):
                                    k = contains(x, a) + contains(x, last[t])
                                    delta7 += wt * (zt - za) * sum(
                                        (Q(1, (za + j0) * (zt + j0)) for j0 in range(1, k + 1)), Q(0))
                                delta8 += wt * ((phi(bg[a], a, last[t]) - phi(bg[a], t, last[a]))
                                              -(phi(bg[t], a, last[t]) - phi(bg[t], t, last[a])))
                        c_cols.append(c_col)
                    assert D - F == L + delta
                    assert F - C == J
                    assert D - C == L + delta + J
                    assert delta == delta7 == delta8 / 2
                    if r <= 2:
                        assert delta == 0
                    actual_u = utility(leaf(h), actions[h])
                    e = actual_u - D
                    G = C - min(c_cols)
                    if valid:
                        assert e >= 0 and L >= 0 and J >= 0 and G >= 0
                    counts["identity_checks"] += 1
                    return dict(D=D, F=F, C=C, L=L, delta=delta, J=J,
                                e=e, G=G, psi=min(c_cols))

                for p in distributions:
                    for h in histories:
                        rr = row(h, p)
                        if valid:
                            for key, val in (("minimum_delta", rr["delta"]),
                                             ("minimum_paid_balance", rr["e"] + rr["L"] + rr["J"] + rr["delta"])):
                                if extrema[key] is None or val < extrema[key]:
                                    extrema[key] = val
                            if rr["delta"] < 0 and witness is None:
                                witness = {"m": m, "multiplicities": mult, "prefix": h,
                                           "p": list(map(str, p)),
                                           "actions": [{"history": k, "action": v} for k, v in actions.items()],
                                           "row": {k: str(v) for k, v in rr.items()}}
                    z = leaf(())
                    rows = [row(z[:i], p) for i in range(m)]
                    W = sum(bool(c) for c in load(z))
                    assert W == sum(utility(z, a) for a in z)
                    assert W - sum(q["psi"] for q in rows) == sum(
                        q["e"] + q["L"] + q["J"] + q["G"] + q["delta"] for q in rows)
                    counts["path_identity_checks"] += 1
    return {"claim": "PEEL/PAY/PATH-PEEL algebra and SPE signs; finite regression only",
            "python": platform.python_version(), "counts": counts,
            "extrema": {k: str(v) for k, v in extrema.items()},
            "negative_delta_full_SPE_witness": witness}


if __name__ == "__main__":
    result = audit()
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_name("peeling_independent_audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "negative_delta_full_SPE_witness"},
                     ensure_ascii=False, indent=2))
