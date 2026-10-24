"""Attack TB-ANY via a valid upper bound on its robust thresholds.

For one complete SPE sigma and any arbitrary path z,
theta(h_i) <= current-player payoff under sigma from h_i.
Thus a strictly negative W(z)+sum(current sigma values)-coverage(T)
would disprove TB-ANY. Fixed-policy full-history IC is linear in types.
Numerical LP output alone is NOT an exact counterexample certificate.
"""
import json
import random
import sys
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import CustomerType, Instance
from customer_attraction.exact import ExactSPESolver


def coefficients(p, m, actions):
    masks = tuple(range(1, 1 << p))

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == m else terminal(h + (actions[h],))

    def payoff(a, z):
        return np.array([1 / sum(bool(mask >> b & 1) for b in z)
                         if mask >> a & 1 else 0 for mask in masks])

    @lru_cache(None)
    def current(h):
        return payoff(actions[h], terminal(h))

    rows = []
    for h, a in actions.items():
        for b in range(p):
            if b != a:
                rows.append(current(h) - payoff(b, terminal(h + (b,))))
    return masks, current, np.array(rows)


def best_path(p, m, masks, current, weights):
    @lru_cache(None)
    def value(h):
        if len(h) == m:
            support = sum(1 << a for a in set(h))
            cov = np.array([bool(mask & support) for mask in masks], dtype=float)
            return float(cov @ weights), cov, h
        children = [value(h+(a,)) for a in range(p)]
        v, coeff, z = min(children, key=lambda q: q[0])
        return v+float(current(h) @ weights), coeff+current(h), z
    return value(())


if __name__ == "__main__":
    rng = random.Random(202610242)
    tested = 0
    for p, m, rounds in [(5, 4, 35), (6, 4, 35), (7, 4, 20), (6, 5, 20)]:
        for trial in range(rounds):
            weights = np.array([rng.randrange(0, 8) if rng.random()<.35 or mask.bit_count()==1 else 0
                                for mask in range(1, 1 << p)])
            it = Instance(tuple(map(str, range(p))),
                          tuple(CustomerType(frozenset(a for a in range(p) if mask >> a & 1), int(w))
                                for mask, w in enumerate(weights,1) if w), m)
            solver = ExactSPESolver(it)
            cert = solver.worst_certificate()
            masks, current, gamma = coefficients(p, m, cert.actions)
            # Each optimization uses an actual all-history SPE cone.
            for refinement in range(4):
                _, cpath, z = best_path(p,m,masks,current,weights)
                opt_candidates = list(combinations(range(p),min(p,m)))
                rng.shuffle(opt_candidates)
                best = None
                for topics in opt_candidates:
                    support = sum(1 << a for a in topics)
                    objective = cpath - np.array([bool(mask & support) for mask in masks])
                    res = linprog(objective,A_ub=-gamma,b_ub=np.zeros(len(gamma)),
                                  A_eq=np.ones((1,len(masks))),b_eq=[1],bounds=(0,None),method="highs")
                    tested += 1
                    if res.success and (best is None or res.fun < best.fun):
                        best=res
                        best_topics=topics
                    if res.success and res.fun < -1e-7:
                        print(json.dumps({"candidate":"TB-ANY", "status":"numerical-only candidate; exact verification required",
                            "p":p,"m":m,"trial":trial,"path":z,"comparison":topics,
                            "objective":res.fun,"weights":res.x.tolist(),
                            "actions":[{"history":h,"action":a} for h,a in cert.actions.items()]},indent=2))
                        raise SystemExit
                if best is None:
                    break
                weights=best.x
    print(json.dumps({"tested_lp":tested,"counterexample":None,
                      "status":"finite negative search is not a proof"}))
