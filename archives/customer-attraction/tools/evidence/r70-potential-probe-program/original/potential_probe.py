"""Exact ordered-history SPE probe for the harmonic potential conjecture.

All arithmetic is integral after scaling by lcm(1,...,m).  This is a
diagnostic only; no finite sample is a proof of the general theorem.
"""
import argparse
import itertools
import json
import math
import random


def one(weights, m, k):
    scale = math.lcm(*range(1, m + 1))
    profiles = list(itertools.product(range(k), repeat=m))
    payoff = {}
    phi = {}
    for p in profiles:
        counts = [sum((mask >> a) & 1 for a in p) for mask in range(1, 1 << k)]
        phi[p] = sum(w * sum(scale // j for j in range(1, c + 1))
                     for w, c in zip(weights, counts))
        payoff[p] = tuple(sum(w * scale // c for mask, w, c in zip(range(1, 1 << k), weights, counts)
                              if (mask >> a) & 1) for a in p)
    # Child sets are indexed by complete ordered prefixes.  Off-path children
    # are independent, so M=max(min child payoff) is the exact admissibility
    # threshold for all children, including arbitrary history-dependent ties.
    realizable = {p: [p] for p in profiles}
    for i in range(m - 1, -1, -1):
        for h in itertools.product(range(k), repeat=i):
            threshold = max(min(payoff[p][i] for p in realizable[h + (a,)]) for a in range(k))
            realizable[h] = [p for a in range(k) for p in realizable[h + (a,)]
                             if payoff[p][i] >= threshold]
    pmax = max(phi.values())
    best = None
    for p in realizable[()]:
        counts = [sum((mask >> a) & 1 for a in p) for mask in range(1, 1 << k)]
        welfare = sum(w * scale for w, c in zip(weights, counts) if c)
        safe = 0
        past = [0] * len(weights)
        for i, a in enumerate(p):
            safe += sum(w * scale // (past[mask - 1] + m - i)
                        for mask, w in zip(range(1, 1 << k), weights) if (mask >> a) & 1)
            for mask in range(1, 1 << k):
                past[mask - 1] += (mask >> a) & 1
        margin = phi[p] + welfare - safe - pmax
        if best is None or margin < best[0]:
            best = (margin, p, welfare, phi[p], safe)
    return best, pmax, len(realizable[()]), scale


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=3)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=670305)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    worst = (10**100, None)
    for j in range(args.trials):
        weights = [rng.choice([0] * 5 + [1, 2, 3, 5, 8, 13, 21, 34]) for _ in range((1 << args.k) - 1)]
        result = one(weights, args.m, args.k)
        if result[0][0] < worst[0]:
            worst = (result[0][0], dict(trial=j, weights=weights, result=result))
            print(json.dumps(worst[1]))
        if worst[0] < 0:
            break
