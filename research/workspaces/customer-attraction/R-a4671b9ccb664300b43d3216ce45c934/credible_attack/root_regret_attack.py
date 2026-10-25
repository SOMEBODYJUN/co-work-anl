"""Attack the exact universal root-regret repair condition, not a new bridge.

For a complete ordered policy, keep every positive-depth IC and optimize
OPT_m - 2 W - 3 Delta, where Delta bounds every real root deviation gain.
A strictly positive EXACT feasible point would compile to a genuine half
counterexample. Floating negative results are only finite diagnostics.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests/audits"))
from customer_attraction import Instance, ExactSPESolver
from customer_attraction_strategy_lp import StrategyCone, payoff_row, coverage_row, dot, serializable

HERE = Path(__file__).resolve().parent


def inc(q, a):
    return tuple(x + (j == a) for j, x in enumerate(q))


def root_relaxed_policy(solver, root):
    """Root may be irrational; every child is a genuine complete SPE."""
    inst = solver.instance
    p, m = inst.topic_count, inst.players
    policy = {(): root}
    targets = {}
    for b in range(p):
        qs = solver.outcomes(inc((0,) * p, b))
        if b == root:
            # A specific low-welfare child, not a purported universal selector.
            targets[b] = min(qs, key=lambda q: (inst.welfare(q), inst.topic_payoff(b, q), q))
        else:
            targets[b] = min(qs, key=lambda q: (inst.topic_payoff(b, q), inst.welfare(q), q))

    def expand(h, q, target):
        if len(h) == m:
            return
        floor = solver.threshold(q)
        choices = [a for a in range(p)
                   if target in solver.outcomes(inc(q, a))
                   and inst.topic_payoff(a, target) >= floor]
        a = min(choices)
        policy[h] = a
        for b in range(p):
            nxt = inc(q, b)
            if b == a:
                child = target
            else:
                child = min(solver.outcomes(nxt),
                            key=lambda z: (inst.topic_payoff(b, z), inst.welfare(z), z))
            expand(h + (b,), nxt, child)

    for b in range(p):
        expand((b,), inc((0,) * p, b), targets[b])
    return policy


def build_cone(policy, p, m):
    cone = StrategyCone(p, m, policy)
    rows = set()
    for h, a in policy.items():
        if not h:
            continue
        actual = payoff_row(p, cone.terminals[h], a)
        for b in range(p):
            row = tuple(x-y for x, y in zip(actual, payoff_row(p, cone.terminals[h+(b,)], b)))
            if any(row):
                rows.add(row + (F(0),))
    a = policy[()]
    actual = payoff_row(p, cone.root, a)
    for b in range(p):
        dev = payoff_row(p, cone.terminals[(b,)], b)
        # actual - deviation + Delta >= 0.
        rows.add(tuple(x-y for x, y in zip(actual, dev)) + (F(1),))
    return cone, tuple(sorted(rows))


def verify_point(cone, rows, values):
    return (all(v >= 0 for v in values)
            and dot(cone.welfare + (F(0),), values) == 1
            and all(dot(row, values) >= 0 for row in rows))


def main():
    # Deliberate mechanisms, not an unbounded random cone sweep: the old
    # 34-client adaptive reply module and the old residual reply-cycle module.
    plans = [("individual_security_failure", 5, 0),
             ("individual_security_failure", 5, 2),
             ("residual_counterexample", 5, 0)]
    records = []
    for name, m, root in plans:
        obj = json.loads((ROOT / "examples/customer_attraction" / (name + ".json")).read_text())
        obj = obj.get("instance", obj)
        obj["players"] = m
        inst = Instance.from_dict(obj)
        solver = ExactSPESolver(inst)
        policy = root_relaxed_policy(solver, root)
        p = inst.topic_count
        cone, rows = build_cone(policy, p, m)
        matrix = np.asarray(rows, dtype=float)
        welfare = cone.welfare + (F(0),)
        best = None
        for portfolio in combinations(range(p), min(p, m)):
            objective = tuple(v - 2*w for v, w in zip(coverage_row(p, portfolio), cone.welfare)) + (F(-3),)
            result = linprog(-np.asarray(objective, dtype=float),
                             A_ub=-matrix, b_ub=np.zeros(len(rows)),
                             A_eq=np.asarray([welfare], dtype=float), b_eq=[1],
                             bounds=(0, None), method="highs")
            if not result.success:
                records.append(dict(seed=name, players=m, root=root,
                                    portfolio=portfolio, status=result.message))
                continue
            value = -result.fun
            if best is None or value > best[0]:
                best = value, portfolio
            rec = dict(seed=name, players=m, topics=p, root=root,
                       portfolio=portfolio, positive_depth_nodes=len(policy)-1,
                       exact_constraint_rows=len(rows), floating_gap=value,
                       status="finite floating diagnostic; no universal conclusion")
            if value > 1e-8:
                vals = tuple(F(float(v)).limit_denominator(10**7) for v in result.x)
                rec["direct_rational_recovery_feasible"] = verify_point(cone, rows, vals)
                if verify_point(cone, rows, vals):
                    gap = dot(objective, vals)
                    rec.update(exact_gap=gap, values=vals)
                    if gap > 0:
                        witness = dict(scope="Exact positive root-regret repair input; requires independent compiled all-history audit",
                                       seed=name, players=m, topics=p, root=root,
                                       portfolio=portfolio, values=vals, exact_gap=gap,
                                       actions=[dict(history=h, action=a) for h, a in sorted(policy.items())])
                        (HERE / "positive_root_regret_input.json").write_text(json.dumps(serializable(witness), indent=2)+"\n")
            records.append(rec)
        print(name, m, root, "best", best, flush=True)
        (HERE / "root_regret_attack_report.json").write_text(json.dumps(serializable(dict(
            scope="Three selected finite policy cones only; no finite negative result is mathematical support",
            records=records)), indent=2)+"\n")


if __name__ == "__main__":
    main()
