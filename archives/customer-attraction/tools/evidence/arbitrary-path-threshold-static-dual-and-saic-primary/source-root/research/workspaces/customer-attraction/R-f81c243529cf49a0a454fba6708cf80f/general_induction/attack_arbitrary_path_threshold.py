"""Attack the explicit general strengthening TB-ANY, not Q-CAG-HALF.

TB-ANY: every arbitrary m-topic path z satisfies
OPT_m <= W(z) + sum_i theta(prefix_i), where theta is the max-min
complete-SPE continuation threshold of the original finite game.
The search has no positive proof interpretation.
"""
import json
import random
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import CustomerType, Instance
from customer_attraction.exact import ExactSPESolver


def attack(instance):
    solver = ExactSPESolver(instance)
    solver.outcomes()
    p, m = instance.topic_count, instance.players

    @lru_cache(None)
    def cost(k):
        if sum(k) == m:
            return instance.welfare(k), ()
        children = []
        for a in range(p):
            kk = list(k)
            kk[a] += 1
            val, path = cost(tuple(kk))
            children.append((val, (a,) + path))
        val, path = min(children)
        return val + solver.threshold(k), path

    val, path = cost((0,) * p)
    opt = instance.optimal_welfare()
    if val < opt:
        thresholds = [str(solver.threshold(instance.counts(path[:i]))) for i in range(m)]
        return {"candidate": "TB-ANY", "instance": instance.to_dict(),
                "path": path, "thresholds": thresholds,
                "welfare": instance.welfare(instance.counts(path)),
                "optimum": opt, "cost": str(val), "gap": str(val-opt),
                "path_is_spe": instance.counts(path) in solver.outcomes() and
                               path in tuple(solver.ordered_outcomes(instance.counts(path)))}


if __name__ == "__main__":
    rng = random.Random(20261024)
    tested = 0
    for p, m, repetitions in [(3, 4, 1000), (4, 4, 1000), (5, 4, 500), (5, 5, 500), (6, 5, 250)]:
        for _ in range(repetitions):
            customers = tuple(CustomerType(frozenset(a for a in range(p) if mask >> a & 1), w)
                              for mask in range(1, 1 << p)
                              if (w := rng.randrange(0, 12)) > 0)
            instance = Instance(tuple(map(str, range(p))), customers, m)
            result = attack(instance)
            tested += 1
            if result:
                print(json.dumps({"tested": tested, "result": result}, ensure_ascii=False, indent=2))
                raise SystemExit
    print(json.dumps({"tested": tested, "counterexample": None,
                      "status": "finite negative search is not a proof"}))
