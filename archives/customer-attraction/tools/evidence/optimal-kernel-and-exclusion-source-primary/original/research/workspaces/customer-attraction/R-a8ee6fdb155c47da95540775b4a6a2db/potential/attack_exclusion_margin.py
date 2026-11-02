#!/usr/bin/env python3
"""Attack E_k(b,A) <= root utility minus the self-copy floor.

A cone is specified by a complete count policy.  This is a subclass of
ordered-history policies, hence any exact positive witness refutes the
universal interface.  Negative searches establish no universal claim.
"""
from functools import lru_cache
from itertools import product
from math import lcm
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import linprog


def compositions(n, k):
    if k == 1:
        yield (n,)
        return
    for a in range(n + 1):
        for z in compositions(n - a, k - 1):
            yield (a,) + z


def attack(topics=6, remaining=3, past=0, trials=100, seed=628301):
    scale = lcm(*range(1, past + remaining + 1))
    types = np.array(list(product((0, 1), repeat=topics))[1:], dtype=np.int64)
    root = (past,) + (0,) * (topics - 1)
    finals = tuple(tuple(a + b for a, b in zip(root, q))
                   for q in compositions(remaining, topics))
    initial = types @ np.array(root)
    loads = types @ np.array(finals).T
    harmonic = [0]
    for j in range(1, past + remaining + 1):
        harmonic.append(harmonic[-1] + scale // j)
    phi = np.array(harmonic)[loads].T - np.array(harmonic)[initial]
    utility = np.array([types.T * (scale // np.maximum(z, 1))[None, :]
                        for z in loads.T])
    final_id = {q: i for i, q in enumerate(finals)}
    rng = np.random.default_rng(seed)
    results = []
    for trial in range(trials):
        weights = np.zeros(len(types), dtype=np.int64)
        for _ in range(20):
            weights[int(rng.integers(len(types)))] += int(rng.integers(1, 30))
        actions = {}

        @lru_cache(None)
        def terminal(q):
            if sum(q) == past + remaining:
                return final_id[q]
            ends = []
            for a in range(topics):
                z = list(q)
                z[a] += 1
                ends.append(terminal(tuple(z)))
            best = max(range(topics), key=lambda a: int(utility[ends[a], a] @ weights))
            actions[q] = best
            return ends[best]

        actual = terminal(root)
        a = actions[root]
        rows = []
        for q, action in actions.items():
            on = terminal(q)
            for other in range(topics):
                if other == action:
                    continue
                z = list(q)
                z[other] += 1
                rows.append(utility[on, action] - utility[terminal(tuple(z)), other])
        rows = np.array(rows)
        safe = types[:, a] * (scale // (initial + remaining))
        containing = [j for j, q in enumerate(finals) if q[a] > root[a]]
        excluding = [j for j, q in enumerate(finals) if q[a] == root[a]]
        # v bounds the potential of every completion containing the root action.
        A_ub = np.vstack([np.c_[-rows, np.zeros(len(rows))],
                          np.c_[phi[containing], -np.ones(len(containing))]])
        b_ub = np.zeros(len(A_ub))
        target_order = sorted(excluding, key=lambda j: int(phi[j] @ weights), reverse=True)
        best = 0.0
        for target in target_order:
            objective = np.r_[phi[target] - utility[actual, a] + safe, -1]
            sol = linprog(-objective, A_ub=A_ub, b_ub=b_ub,
                          A_eq=[np.r_[np.ones(len(types)), 0]], b_eq=[1],
                          bounds=[(0, None)] * len(types) + [(None, None)], method="highs")
            assert sol.success, sol.message
            best = max(best, -float(sol.fun))
            if sol.fun < -1e-7:
                report = {
                    "status": "FLOAT_POSITIVE_REQUIRES_EXACT_RECONSTRUCTION",
                    "candidate": "E_k(b,A) <= root utility - maximum-self-copy floor",
                    "scope": "complete count policy; not yet an exact counterexample",
                    "topics": topics, "remaining": remaining, "past_copies_topic0": past,
                    "scale": scale, "seed": seed, "trial": trial,
                    "root_action": a, "actual_counts": finals[actual],
                    "comparison_counts": finals[target], "gap_scaled": -float(sol.fun),
                    "types": types.tolist(), "weights": sol.x[:-1].tolist(),
                    "potential_containing_upper": float(sol.x[-1]),
                    "count_policy": [{"prefix": q, "action": b} for q, b in sorted(actions.items())],
                }
                return report
        results.append({"trial": trial, "root_action": a, "best_gap_scaled": best})
        print(f"trial={trial} root={a} best_gap_scaled={best}", flush=True)
    return {"status": "NO_POSITIVE_CONE_ATTACK_IN_STATED_FINITE_DOMAIN",
            "scope": "not a universal proof", "topics": topics, "remaining": remaining,
            "past_copies_topic0": past, "seed": seed, "trials": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topics", type=int, default=6)
    parser.add_argument("--remaining", type=int, default=3)
    parser.add_argument("--past", type=int, default=0)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=628301)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    params = {k: v for k, v in vars(args).items() if k != "output"}
    report = attack(**params)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ("types", "weights", "count_policy", "trials")}), flush=True)
