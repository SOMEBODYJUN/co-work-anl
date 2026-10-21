"""Exact m=3 test of worst-welfare Markovization, including all terminal ties.

This tests a structural reduction, not Q-CAG-HALF. All payoffs are integral
after multiplying by 6. Markov SPEs are enumerated by their last-layer action
choices; earlier full count strategies then have no shared nodes left.
"""
from itertools import combinations_with_replacement, product
import argparse
import json
from pathlib import Path
import time

import numpy as np


def check(weights, k, max_policies):
    types = np.arange(1, 1 << k)
    inc = ((types[:, None] >> np.arange(k)) & 1).astype(int)
    pairs = list(combinations_with_replacement(range(k), 2))
    triples = list(combinations_with_replacement(range(k), 3))
    ti = {t: i for i, t in enumerate(triples)}
    pi = {p: i for i, p in enumerate(pairs)}
    pay, welfare = [], []
    for t in triples:
        load = inc[:, t].sum(axis=1)
        share = np.array([0 if z == 0 else 6 // z for z in load]) * weights
        pay.append(share @ inc)
        welfare.append(int(weights[load > 0].sum()))
    pay, welfare = np.asarray(pay), np.asarray(welfare)
    leaves = np.asarray([[ti[tuple(sorted(p + (a,)))] for a in range(k)] for p in pairs])
    lastvals = np.asarray([[pay[leaves[p, a], a] for a in range(k)] for p in range(len(pairs))])
    best = [list(np.flatnonzero(row == row.max())) for row in lastvals]
    policy_count = int(np.prod([len(x) for x in best]))
    if policy_count > max_policies:
        return None

    # Full-history exact set-valued BI: each ordered pair chooses its own tie.
    second_sets = []
    for a in range(k):
        child = [set(leaves[pi[tuple(sorted((a,b)))], best[pi[tuple(sorted((a,b)))]]])
                 for b in range(k)]
        floor = max(min(pay[t,b] for t in child[b]) for b in range(k))
        second_sets.append(set(t for b in range(k) for t in child[b] if pay[t,b] >= floor))
    root_floor = max(min(pay[t,a] for t in second_sets[a]) for a in range(k))
    full_leaves = set(t for a in range(k) for t in second_sets[a] if pay[t,a] >= root_floor)
    full_min = min(welfare[t] for t in full_leaves)

    markov_min = 10**15
    for actions in product(*best):
        selected = leaves[np.arange(len(pairs)), actions]
        opts = []
        for a in range(k):
            child = [selected[pi[tuple(sorted((a,b)))]] for b in range(k)]
            vals = [pay[t,b] for b,t in enumerate(child)]
            opts.append(set(t for b,t in enumerate(child) if vals[b] == max(vals)))
        floor = max(min(pay[t,a] for t in opts[a]) for a in range(k))
        possible = [t for a in range(k) for t in opts[a] if pay[t,a] >= floor]
        markov_min = min(markov_min, min(welfare[t] for t in possible))
        if markov_min == full_min:
            break
    return full_min, markov_min, policy_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topics", type=int, default=4)
    parser.add_argument("--samples", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=71)
    parser.add_argument("--max-policies", type=int, default=100000)
    parser.add_argument("--output", default="markov_gap.json")
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    started = time.monotonic()
    checked, skipped = 0, 0
    for i in range(args.samples):
        weights = rng.integers(0, 5, (1 << args.topics) - 1)
        weights *= rng.random(len(weights)) < rng.uniform(.2, 1)
        result = check(weights, args.topics, args.max_policies)
        if result is None:
            skipped += 1
            continue
        checked += 1
        full, markov, count = result
        if full < markov:
            record = {"topics": args.topics, "players": 3,
                      "weights": weights.tolist(), "full_min": full,
                      "markov_min": markov, "last_policies": count,
                      "sample": i, "checked": checked, "skipped": skipped}
            Path(args.output).write_text(json.dumps(record, indent=2) + "\n")
            print(json.dumps(record), flush=True)
            break
    print(json.dumps({"done": True, "checked": checked, "skipped": skipped,
                      "seconds": time.monotonic() - started}), flush=True)
