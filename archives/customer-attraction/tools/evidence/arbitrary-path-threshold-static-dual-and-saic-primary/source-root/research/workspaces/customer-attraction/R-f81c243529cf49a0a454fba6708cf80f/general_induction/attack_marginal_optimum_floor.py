"""Test MARGINAL-FLOOR only: theta_r(b)>=F_r(b)-F_(r-1)(b).

F_j(b) is maximum coverage of clients not already covered by prefix b,
using j catalog topics. All count prefixes are tested; theta is computed
by complete-SPE outcome-set recursion. Finite nonfailure proves nothing.
"""
import json
import random
import sys
from functools import lru_cache
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import CustomerType, Instance
from customer_attraction.exact import ExactSPESolver


def attack(instance):
    solver = ExactSPESolver(instance)
    solver.outcomes()
    p, m = instance.topic_count, instance.players

    @lru_cache(None)
    def residual_opt(support, slots):
        remaining = tuple(c for c in instance.customers if not c.topics.intersection(support))
        return max(sum(c.multiplicity for c in remaining if c.topics.intersection(topics))
                   for topics in combinations(range(p), min(slots, p)))

    for b in solver._thresholds:
        r = m - sum(b)
        support = frozenset(a for a, count in enumerate(b) if count)
        fr, fr0 = residual_opt(support, r), residual_opt(support, r-1)
        theta = solver.threshold(b)
        if theta < fr - fr0:
            return {"candidate": "MARGINAL-FLOOR", "instance": instance.to_dict(),
                    "prefix_counts": b, "remaining": r, "theta": str(theta),
                    "F_r": fr, "F_r_minus_one": fr0,
                    "gap": str(theta - (fr-fr0))}


if __name__ == "__main__":
    rng = random.Random(202610241)
    tested = 0
    for p, m, repetitions in [(4, 4, 500), (5, 4, 1000), (6, 4, 1000), (6, 5, 500), (8, 4, 500)]:
        for i in range(repetitions):
            # Sparse supports and private clients make the marginal gap visible.
            weights = {}
            for a in range(p):
                weights[1 << a] = rng.randrange(0, 80)
            for _ in range(2*p):
                mask = rng.randrange(1, 1 << p)
                weights[mask] = rng.randrange(0, 80)
            customers = tuple(CustomerType(frozenset(a for a in range(p) if mask >> a & 1), w)
                              for mask, w in weights.items() if w > 0)
            instance = Instance(tuple(map(str, range(p))), customers, m)
            result = attack(instance)
            tested += 1
            if result:
                print(json.dumps({"tested": tested, "result": result}, ensure_ascii=False, indent=2))
                raise SystemExit
    print(json.dumps({"tested": tested, "counterexample": None,
                      "status": "finite negative search is not a proof"}))
