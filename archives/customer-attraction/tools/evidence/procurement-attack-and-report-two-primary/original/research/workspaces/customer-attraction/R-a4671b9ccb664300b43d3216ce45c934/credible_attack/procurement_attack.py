"""One targeted attack on the all-z root-menu procurement candidate.

Every root action uses a fixed genuine complete child SPE. Own root column is
the actual child. Root IC is deliberately absent. A positive exact optimum
refutes the procurement candidate only, not Q-CAG-HALF.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json
import numpy as np
from scipy.optimize import linprog
from root_regret_attack import (ROOT, HERE, Instance, ExactSPESolver,
                                root_relaxed_policy, build_cone, payoff_row,
                                dot, serializable)


def procurement_objective(cone, z):
    p = cone.topics
    drows = [payoff_row(p, cone.terminals[(a,)], a) for a in range(p)]
    return tuple(min(F(1), sum(z[a] for a in range(p) if mask & (1 << a)))
                 - sum(z[a] * drows[a][mask-1] for a in range(p))
                 - cone.welfare[mask-1]
                 for mask in range(1, 1 << p))


def exact_point(cone, floating):
    v = tuple(F(float(x)).limit_denominator(10**7) for x in floating)
    if not (cone.verify(v) and dot(cone.welfare, v) == 1):
        v = cone.recover_vertex(floating)
    if v is not None and cone.verify(v) and dot(cone.welfare, v) == 1:
        return v


def best_z(cone, weights):
    p = cone.topics
    n = len(weights)
    prices = [dot(payoff_row(p, cone.terminals[(a,)], a), weights) for a in range(p)]
    # Variables z_a in [0,1], y_mask in [0,1]; y_mask <= sum_(a in mask) z_a.
    mat = np.zeros((n, p+n))
    for j, mask in enumerate(range(1, 1 << p)):
        mat[j, :p] = [-int(bool(mask & (1 << a))) for a in range(p)]
        mat[j, p+j] = 1
    obj = np.asarray([float(v) for v in prices] + [-float(w) for w in weights])
    res = linprog(obj, A_ub=mat, b_ub=np.zeros(n), bounds=(0, 1), method="highs")
    assert res.success
    return tuple(F(float(x)).limit_denominator(10**6) for x in res.x[:p])


def main():
    name, m, root = "individual_security_failure", 5, 0
    obj = json.loads((ROOT / "examples/customer_attraction" / (name + ".json")).read_text())
    obj = obj.get("instance", obj)
    obj["players"] = m
    inst = Instance.from_dict(obj)
    solver = ExactSPESolver(inst)
    policy = root_relaxed_policy(solver, root)
    p = inst.topic_count
    cone, rows = build_cone(policy, p, m)
    cone.rows = tuple(row[:-1] for row in rows if row[-1] == 0 and any(row[:-1]))
    cone.matrix = np.asarray(cone.rows, dtype=float)
    records = []
    best = None
    starts = []
    for size in range(1, p+1):
        for support in combinations(range(p), size):
            starts.append(tuple(F(a in support) for a in range(p)))
    # A single complete integer-z pass, then at most three exact-weight /
    # continuous-z alternations from its best point. No random continuation sweep.
    turn = 0
    while turn < len(starts):
        z = starts[turn]
        objective = procurement_objective(cone, z)
        res = linprog(-np.asarray(objective, dtype=float),
                      A_ub=-cone.matrix, b_ub=np.zeros(len(cone.rows)),
                      A_eq=np.asarray([cone.welfare], dtype=float), b_eq=[1],
                      bounds=(0, None), method="highs")
        rec = dict(turn=turn, z=z, status=res.message)
        if res.success:
            gap = -res.fun
            rec["floating_gap"] = gap
            if best is None or gap > best[0]:
                best = gap, z, res.x
            if gap > 1e-8:
                weights = exact_point(cone, res.x)
                rec["exact_feasible"] = weights is not None
                if weights is not None:
                    exactgap = dot(objective, weights)
                    rec["exact_gap"] = exactgap
                    if exactgap > 0:
                        witness = dict(
                            scope="Exact procurement candidate counterexample only; root need not be optimal",
                            players=m, topics=p, actual_root=root, z=z, weights=weights,
                            exact_gap=exactgap,
                            actions=[dict(history=h, action=a) for h, a in sorted(policy.items())])
                        (HERE / "procurement_positive.json").write_text(json.dumps(serializable(witness), indent=2)+"\n")
                        records.append(rec)
                        break
        records.append(rec)
        turn += 1
        if turn == 2**p-1 and best is not None:
            weights = exact_point(cone, best[2])
            if weights is not None:
                starts.append(best_z(cone, weights))
        elif turn >= 2**p and turn < 2**p+2 and best is not None:
            weights = exact_point(cone, best[2])
            if weights is not None:
                starts.append(best_z(cone, weights))
    report = dict(scope="One selected root-relaxed full-child strategy cone; no negative result supports the general candidate",
                  seed=name, players=m, topics=p, actual_root=root,
                  actual_counts=cone.root, positive_depth_rows=len(cone.rows),
                  best_floating_gap=best[0] if best is not None else None,
                  records=records)
    (HERE / "procurement_attack_report.json").write_text(json.dumps(serializable(report), indent=2)+"\n")
    print(json.dumps(serializable(dict(best=report["best_floating_gap"], tests=len(records),
                                      positive_witness=(HERE / "procurement_positive.json").exists()))))


if __name__ == "__main__":
    main()
