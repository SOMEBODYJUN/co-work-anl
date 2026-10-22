"""Exploratory fixed-SPE-cone attack on max_F(|union F|-|F|u_i)<=W.

Floating LP output is discovery-only. This script proves no universal claim.
"""
from functools import lru_cache
from itertools import product
import argparse
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linprog


def run(k, m, iterations, seed):
    rng = np.random.default_rng(seed)
    types = tuple(range(1, 1 << k))
    profiles = tuple(product(range(k), repeat=m))
    payoffs = {}
    covers = {}
    for s in profiles:
        counts = np.array([sum(bool(t >> a & 1) for a in s) for t in types])
        covers[s] = (counts > 0).astype(float)
        payoffs[s] = np.array([[float(bool(t >> a & 1)) / c if c else 0
                               for t, c in zip(types, counts)] for a in s])
    best = {"ratio": -1.0}
    started = time.monotonic()
    solves = 0
    for iteration in range(iterations):
        weights = rng.integers(0, 9, size=len(types)).astype(float)
        weights *= rng.random(len(types)) < rng.uniform(.08, .8)
        if not weights.any():
            weights[0] = 1
        strategy = {}

        @lru_cache(None)
        def build(h):
            if len(h) == m:
                return h
            continuations = [build(h + (a,)) for a in range(k)]
            values = [payoffs[s][len(h)] @ weights for s in continuations]
            candidates = [a for a, value in enumerate(values)
                          if value >= max(values) - 1e-9]
            a = int(rng.choice(candidates))
            strategy[h] = a
            return continuations[a]

        root = build(())

        @lru_cache(None)
        def outcome(h):
            if len(h) == m:
                return h
            return outcome(h + (strategy[h],))

        gamma = []
        for depth in range(m):
            for h in product(range(k), repeat=depth):
                original = payoffs[outcome(h)][depth]
                for a in range(k):
                    gamma.append(original - payoffs[outcome(h + (a,))][depth])
        gamma = np.array(gamma)
        welfare = covers[root]
        for family in range(1, 1 << k):
            coverage = np.array([float(bool(t & family)) for t in types])
            for i in range(m):
                objective = coverage - family.bit_count() * payoffs[root][i]
                result = linprog(-objective, A_ub=-gamma, b_ub=np.zeros(len(gamma)),
                                 A_eq=[welfare], b_eq=[1], bounds=(0, None), method="highs")
                solves += 1
                if result.success and -result.fun > best["ratio"] + 1e-8:
                    best = {
                        "ratio": -result.fun, "family": family, "player": i,
                        "root": root, "iteration": iteration,
                        "weights": [[t, float(value)] for t, value in zip(types, result.x)
                                    if value > 1e-8],
                        "strategy": [[list(h), a] for h, a in strategy.items()],
                    }
                    print(json.dumps({key: best[key] for key in
                                      ("ratio", "family", "player", "root", "iteration")}), flush=True)
                if best["ratio"] > 1 + 1e-7:
                    break
            if best["ratio"] > 1 + 1e-7:
                break
        if best["ratio"] > 1 + 1e-7:
            break
    return {"status": "discovery-only", "k": k, "m": m, "requested_iterations": iterations,
            "seed": seed, "solves": solves, "seconds": time.monotonic() - started, "best": best}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topics", type=int, default=6)
    parser.add_argument("--players", type=int, default=3)
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--seed", type=int, default=2026102110)
    args = parser.parse_args()
    result = run(args.topics, args.players, args.iterations, args.seed)
    path = Path(__file__).with_name("integral_price_probe.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("solves", "seconds", "status")}))
