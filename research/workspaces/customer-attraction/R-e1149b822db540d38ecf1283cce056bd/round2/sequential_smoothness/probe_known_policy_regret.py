"""Targeted R/Tax LP over named, already documented complete SPE policies.

This is not an SPE counterexample unless a returned positive point is separately
converted to integer multiplicities and all original ordered-history IC replayed.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[6]
BASE = Path(__file__).resolve().parent


def inspect(name):
    instance = json.loads((ROOT / "examples/customer_attraction" / f"{name}.json").read_text())
    cert = json.loads((ROOT / "evidence/certificates/customer_attraction" / f"{name}.json").read_text())
    policy = {tuple(a["history"]): a["action"] for a in cert["actions"]}
    p, m = len(instance["topics"]), instance["players"]
    types = range(1, 1 << p)

    def terminal(history):
        h = tuple(history)
        while len(h) < m:
            h += (policy[h],)
        return h

    def u(profile, i):
        return np.array([float(F(1, sum((mask >> a) & 1 for a in profile)))
                         if (mask >> profile[i]) & 1 else 0.0 for mask in types])

    actual = terminal(())
    own = [u(actual, i) for i in range(m)]
    ownsum = sum(own)
    tax = np.array([1.0 / (1 + sum((mask >> a) & 1 for a in actual))
                    if any((mask >> a) & 1 for a in actual) else 0.0 for mask in types])
    rows = []
    for h in sorted(policy, key=lambda h: (len(h), h)):
        i = len(h)
        prescribed = u(terminal(h), i)
        for a in range(p):
            rows.append(prescribed - u(terminal(h + (a,)), i))
    rows = np.array(rows)
    static = []
    for i in range(m):
        values = []
        for a in range(p):
            changed = list(actual)
            changed[i] = a
            values.append(u(tuple(changed), i))
        static.append(values)
    best = None
    for br in product(range(p), repeat=m - 1):
        br += (actual[-1],)  # the last mover has static regret zero throughout the SPE cone
        objective = sum(static[i][br[i]] for i in range(m)) - ownsum
        result = linprog(-objective, A_ub=-rows, b_ub=np.zeros(len(rows)),
                         A_eq=[tax], b_eq=[1.0], bounds=(0, None), method="highs")
        if result.status == 3:
            return {"name": name, "players": m, "topics": p, "status": "unbounded", "br": br}
        if result.success and (best is None or -result.fun > best["ratio"]):
            best = {"name": name, "players": m, "topics": p, "actual": actual,
                    "ratio": float(-result.fun), "br": br,
                    "weights": {str(mask): float(w) for mask, w in zip(types, result.x) if w > 1e-9},
                    "minimum_IC_float": float(np.min(rows @ result.x))}
    return best


names = ("worst_pne_welfare_failure", "worst_cce_welfare_failure", "eight_cce_welfare_gap")
reports = [inspect(name) for name in names]
path = BASE / "probe_known_policy_regret.json"
path.write_text(json.dumps(reports, indent=2) + "\n")
print(json.dumps(reports, indent=2))
