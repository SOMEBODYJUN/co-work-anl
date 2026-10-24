"""ABANDONED AND NOT RUN: W >= OPT_m(N \ actual_union) is already false.

The parent identified an existing 71-customer complete SPE with W=35 and an
optimal comparison missing R=36 customers. See this directory's README and
nonuniform_capture_routes.md for the exact correction and original source.
The script was written before that correction and was never executed.
Retained as an unfinished, invalidated research checkpoint; do not resume it.
"""

import argparse
import itertools
import json
import random
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def attack(p, m, rounds, seed):
    rng = random.Random(seed)
    masks = list(range(1, 1 << p))
    histories = {
        d: list(itertools.product(range(p), repeat=d)) for d in range(m)
    }
    terminals = list(itertools.product(range(p), repeat=m))
    payoff = {}
    for z in terminals:
        loads = np.array([sum(bool(x >> a & 1) for a in z) for x in masks])
        for i in range(m):
            payoff[z, i] = np.array([
                (1 / loads[k]) if x >> z[i] & 1 else 0
                for k, x in enumerate(masks)
            ])
    best = None
    seen = set()
    for rep in range(rounds):
        weights = np.array([
            rng.randrange(10) if rng.random() < .6 else 0 for _ in masks
        ])
        policy, continuation = {}, {z: z for z in terminals}
        for d in reversed(range(m)):
            for h in histories[d]:
                values = [float(payoff[continuation[h + (a,)], d] @ weights)
                          for a in range(p)]
                top = max(values)
                chosen = rng.choice([a for a in range(p)
                                     if abs(values[a] - top) < 1e-9])
                policy[h] = chosen
                continuation[h] = continuation[h + (chosen,)]
        key = tuple(policy[h] for d in range(m) for h in histories[d])
        if key in seen:
            continue
        seen.add(key)
        z = continuation[()]
        actual_bits = sum(1 << a for a in set(z))
        coverage = np.array([bool(x & actual_bits) for x in masks], dtype=float)
        rows = []
        for d in range(m):
            for h in histories[d]:
                good = payoff[continuation[h], d]
                for a in range(p):
                    rows.append(good - payoff[continuation[h + (a,)], d])
        # Every uncovered customer occurs in an unused label. If there are at
        # most m unused labels, they fit one common comparison automatically.
        unused = [a for a in range(p) if a not in z]
        candidates = (list(itertools.combinations(unused, m))
                      if len(unused) > m else [unused])
        for target in candidates:
            target_bits = sum(1 << a for a in target)
            uncovered = np.array([
                bool(x & target_bits) and not bool(x & actual_bits)
                for x in masks
            ], dtype=float)
            fit = linprog(
                -uncovered, A_ub=-np.array(rows), b_ub=np.zeros(len(rows)),
                A_eq=coverage.reshape(1, -1), b_eq=[1], bounds=(0, None),
                method="highs",
            )
            if fit.success and (best is None or -fit.fun > best["ratio"]):
                best = {
                    "ratio": -float(fit.fun), "actual": z, "target": target,
                    "weights": {str(x): float(w) for x, w in zip(masks, fit.x)
                                if w > 1e-8},
                    "policy": {",".join(map(str, h)): a
                               for h, a in policy.items()},
                    "round": rep,
                }
                if best["ratio"] > 1 + 1e-7:
                    return {"p": p, "m": m, "seed": seed,
                            "policies": len(seen), "best": best}
    return {"p": p, "m": m, "seed": seed,
            "policies": len(seen), "best": best}


if __name__ == "__main__":
    raise SystemExit("Abandoned: this candidate already has an exact counterexample.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--topics", type=int, default=5)
    parser.add_argument("--players", type=int, default=3)
    parser.add_argument("--rounds", type=int, default=100)
    parser.add_argument("--seed", type=int, default=127)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = attack(args.topics, args.players, args.rounds, args.seed)
    raw = json.dumps(result, ensure_ascii=False, indent=2)
    print(raw)
    if args.output:
        with args.output.open("x") as stream:
            stream.write(raw + "\n")
