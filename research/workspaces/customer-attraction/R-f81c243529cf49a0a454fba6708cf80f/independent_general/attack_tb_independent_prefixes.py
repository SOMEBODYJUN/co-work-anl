"""Discovery LP for TB-ANY, using independent complete sub-SPEs at each prefix.

This attacks only TB-ANY. A positive floating LP is not an exact counterexample.
No finite negative run has a proof interpretation.
"""
import json
import random
import sys
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import CustomerType, Instance
from customer_attraction.exact import ExactSPESolver


def inc(k, a):
    return k[:a] + (k[a] + 1,) + k[a + 1:]


def discover(instance, rng):
    solver = ExactSPESolver(instance)
    solver.outcomes()
    p, m = instance.topic_count, instance.players
    masks = tuple(range(1, 1 << p))

    @lru_cache(None)
    def coeff(k, a):
        out = []
        for mask in masks:
            den = sum(k[t] for t in range(p) if mask >> t & 1)
            out.append(Fraction(1, den) if mask >> a & 1 else Fraction(0))
        return tuple(out)

    @lru_cache(None)
    def cost(k):
        if sum(k) == m:
            return Fraction(instance.welfare(k)), ()
        v, path = min((cost(inc(k, a))[0], (a,) + cost(inc(k, a))[1])
                      for a in range(p))
        return v + solver.threshold(k), path

    zero = (0,) * p
    seed_cost, path = cost(zero)
    count = instance.counts(path)
    cover = tuple(int(any(count[a] and (mask >> a & 1) for a in range(p)))
                  for mask in masks)
    best_support = max((s for j in range(min(m, p) + 1)
                        for s in combinations(range(p), j)),
                       key=lambda s: instance.welfare(tuple(int(a in s) for a in range(p))))
    compare = tuple(int(any(mask >> a & 1 for a in best_support)) for mask in masks)
    rows = []
    nodes = {}

    def pick(seq):
        seq = sorted(seq)
        return rng.choice(seq)

    def expand(k, target, forced=None):
        if sum(k) == m:
            return
        key = (k, target, forced)
        if key in nodes:
            return
        floor = solver.threshold(k)
        admissible = [a for a in range(p)
                      if target in solver.outcomes(inc(k, a))
                      and solver._utility(target, a) >= floor]
        chosen = forced if forced is not None else pick(admissible)
        if chosen not in admissible:
            raise AssertionError("invalid forced action")
        children = []
        for a in range(p):
            if a == chosen:
                desired = target
            else:
                child = solver.outcomes(inc(k, a))
                low = min(solver._utility(q, a) for q in child)
                desired = pick([q for q in child if solver._utility(q, a) == low])
            children.append(desired)
        nodes[key] = (chosen, tuple(children))
        chosen_row = coeff(target, chosen)
        for a, desired in enumerate(children):
            if a != chosen:
                rows.append(tuple(x - y for x, y in zip(chosen_row, coeff(desired, a))))
            expand(inc(k, a), desired)

    roots = []
    cap = [Fraction(0)] * len(masks)
    for i in range(m):
        k = instance.counts(path[:i])
        floor = solver.threshold(k)
        witnesses = [(a, q) for a in range(p)
                     for q in solver.outcomes(inc(k, a))
                     if solver._utility(q, a) == floor]
        if not witnesses:
            raise AssertionError("threshold not attained")
        a, target = pick(witnesses)
        expand(k, target, a)
        roots.append((k, target, a))
        cap = [x + y for x, y in zip(cap, coeff(target, a))]
    objective = [Fraction(compare[j] - cover[j]) - cap[j] for j in range(len(masks))]
    # Repeated payoff comparisons from different ordered histories are identical
    # coefficients, so deduplication loses no required IC.
    rows = sorted(set(rows))
    result = linprog(-np.array(objective, dtype=float),
                     A_ub=-np.array(rows, dtype=float), b_ub=np.zeros(len(rows)),
                     A_eq=np.ones((1, len(masks))), b_eq=[1.0],
                     bounds=(0, None), method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    gap = -result.fun
    return gap, {"candidate": "TB-ANY", "seed_instance": instance.to_dict(),
                 "path": path, "seed_minimum_cost": str(seed_cost),
                 "seed_optimum": instance.optimal_welfare(),
                 "comparison_support": best_support, "masks": masks,
                 "weights_float": result.x.tolist(), "gap_float": gap,
                 "rows": [[str(x) for x in r] for r in rows] if gap > 1e-8 else None,
                 "objective": [str(x) for x in objective],
                 "roots": roots,
                 "nodes": [{"counts": k, "target": t, "forced": f,
                            "chosen": ch, "children": cs}
                           for (k, t, f), (ch, cs) in nodes.items()] if gap > 1e-8 else None,
                 "row_count": len(rows), "node_count": len(nodes)}


def main():
    rng = random.Random(721924)
    best = -1.0
    n = 0
    examples = ["root_tax_failure", "individual_security_failure",
                "coverage_opportunity_failure", "global_decorrelation_failure",
                "worst_cce_welfare_failure", "eight_cce_welfare_gap"]
    seeds = [Instance.from_dict(json.loads((ROOT / "examples/customer_attraction" / (name + ".json")).read_text()))
             for name in examples]
    for p, m in [(4, 4), (5, 4), (5, 5), (6, 5)]:
        for _ in range(8):
            # Sparse supports, as dense universes usually have excessive actual coverage.
            chosen = rng.sample(range(1, 1 << p), min((1 << p) - 1, p + 4))
            seeds.append(Instance(tuple(map(str, range(p))),
                         tuple(CustomerType(frozenset(a for a in range(p) if mask >> a & 1),
                                            rng.randrange(1, 17)) for mask in chosen), m))
    for seed in seeds:
        for _ in range(2):
            gap, data = discover(seed, rng)
            n += 1
            if gap > best + 1e-9:
                best = gap
                print(json.dumps({"tested": n, "best_float_gap": best,
                                  "players": seed.players, "topics": seed.topic_count,
                                  "rows": data["row_count"]}), flush=True)
            if gap > 1e-8:
                target = Path(__file__).with_name("tb_independent_prefix_discovery.json")
                target.write_text(json.dumps(data, ensure_ascii=False, indent=2))
                print(json.dumps({"discovery": str(target), "gap_float": gap}), flush=True)
                return
    print(json.dumps({"tested": n, "best_float_gap": best,
                      "status": "no discovery; finite negative run is not a proof"}), flush=True)


if __name__ == "__main__":
    main()
