"""Finite attack on an optimized fractional-background individual floor.

Numerical convex optimization is used only to propose gaps. A positive
candidate must be separately certified before it is a mathematical result.
"""
import argparse
import json
from pathlib import Path
import random
import sys
import time

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / "customer_attraction/__init__.py").is_file())
sys.path.insert(0, str(ROOT))
import numpy as np
from scipy.optimize import minimize
from customer_attraction import CustomerType, ExactSPESolver, Instance


def fractional_floor(instance):
    q = instance.topic_count
    incidence = np.array([[int(a in x.topics) for a in range(q)]
                          for x in instance.customers], dtype=float)
    weights = np.array([x.multiplicity for x in instance.customers], dtype=float)
    k = instance.players - 1
    def values(z):
        return incidence.T @ (weights / (1 + k * (incidence @ z[:q])))
    result = minimize(lambda z: z[-1],
                      np.r_[np.ones(q) / q, max(1, sum(weights))],
                      constraints=[{"type": "eq", "fun": lambda z: z[:q].sum()-1},
                                   {"type": "ineq", "fun": lambda z: z[-1]-values(z)}],
                      bounds=[(0, 1)]*q+[(0, None)], method="SLSQP",
                      options={"ftol": 1e-10, "maxiter": 400})
    return result, values(result.x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--players", type=int, default=3)
    ap.add_argument("--topics", type=int, default=6)
    ap.add_argument("--trials", type=int, default=200)
    ap.add_argument("--seed", type=int, default=99771291)
    ap.add_argument("--seconds", type=float, default=45)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    start = time.monotonic()
    best = None
    complete = 0
    for trial in range(args.trials):
        if time.monotonic()-start >= args.seconds:
            break
        types = tuple(CustomerType(frozenset(a for a in range(args.topics) if mask >> a & 1),
                                   rng.randint(1, 9))
                      for mask in range(1, 1 << args.topics) if rng.random() < .28)
        if not types:
            continue
        instance = Instance(tuple(map(str, range(args.topics))), types, args.players)
        solver = ExactSPESolver(instance)
        root = solver.threshold((0,) * args.topics)
        result, values = fractional_floor(instance)
        complete += 1
        score = float(root) / result.fun
        if result.success and (best is None or score < best["root_over_fractional"]):
            best = {"trial": trial, "root_floor": str(root),
                    "fractional_numerical": float(result.fun),
                    "root_over_fractional": score, "fractional_q": result.x[:-1].tolist(),
                    "fractional_values": values.tolist(), "instance": instance.to_dict()}
        if result.success and score < 1-1e-7:
            best["candidate_only"] = True
            break
    out = {"scope": "finite random instances; complete SPE outcome oracle; numerical fractional optimization",
           "universal_claim_proved": False, "completed": complete,
           "parameters": {k: str(v) if isinstance(v, Path) else v for k,v in vars(args).items()},
           "elapsed": time.monotonic()-start, "best": best}
    args.output.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({k: v for k, v in out.items() if k != "best"} | {"best": best}, indent=2))


if __name__ == "__main__":
    main()
