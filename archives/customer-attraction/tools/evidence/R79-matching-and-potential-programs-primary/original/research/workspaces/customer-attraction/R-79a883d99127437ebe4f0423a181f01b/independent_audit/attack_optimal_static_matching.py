"""Attack one precise general candidate, never infer it from finite negatives.

Candidate: every SPE terminal z admits an OPT_m-attaining comparison tuple T
and a bijection to player slots such that sum_i u_i(T_i,z_-i) <= W(z).
All game payoffs and final candidate checks use exact Fractions.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations_with_replacement
import json
from pathlib import Path
import random
import sys

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate


def frozen_cost(instance, path, topic):
    result = []
    for slot in range(instance.players):
        other = path[:slot] + path[slot + 1:]
        result.append(sum((Fraction(c.multiplicity,
            1 + sum(a in c.topics for a in other))
            for c in instance.customers if topic in c.topics), Fraction()))
    return result


def matching(cost, comparison):
    # Repeated columns are permitted; subsets of labeled comparison slots give
    # a simple exact minimum assignment dynamic program.
    m = len(comparison)
    dp = {0: (Fraction(), ())}
    for slot in range(m):
        new = {}
        for mask, (value, assignment) in dp.items():
            for j, topic in enumerate(comparison):
                if not mask & (1 << j):
                    nextmask = mask | (1 << j)
                    proposal = (value + cost[topic][slot], assignment + (topic,))
                    if nextmask not in new or proposal < new[nextmask]:
                        new[nextmask] = proposal
        dp = new
    return dp[(1 << m) - 1]


def inspect(instance):
    k, m = instance.topic_count, instance.players
    solver = ExactSPESolver(instance)
    optimal = instance.optimal_welfare()
    comparisons = [t for t in combinations_with_replacement(range(k), m)
        if instance.welfare(instance.counts(t, terminal=True)) == optimal]
    for counts in sorted(solver.outcomes()):
        # Static matching depends on terminal action multiset, not play order.
        path = tuple(a for a, q in enumerate(counts) for _ in range(q))
        w = instance.welfare(counts)
        cost = [frozen_cost(instance, path, topic) for topic in range(k)]
        best = min((matching(cost, t)[0], t, matching(cost, t)[1])
                   for t in comparisons)
        if best[0] > w:
            certificate = solver.certificate(counts)
            verification = verify_certificate(instance, certificate)
            return {"instance": instance.to_dict(),
                    "certificate": certificate.to_dict(),
                    "verification": verification,
                    "counts": counts, "canonical_path": path,
                    "W": w, "OPT": optimal,
                    "minimum_optimal_matching": str(best[0]),
                    "comparison": best[1], "assignment": best[2],
                    "cost": [[str(v) for v in row] for row in cost]}
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=300)
    parser.add_argument("--topics", type=int, default=5)
    parser.add_argument("--players", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20261024)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    for trial in range(args.trials):
        customers = []
        for mask in range(1, 1 << args.topics):
            multiplicity = rng.randrange(5) if rng.random() < .45 else 0
            if multiplicity:
                customers.append(CustomerType(frozenset(a for a in
                    range(args.topics) if mask & (1 << a)), multiplicity))
        instance = Instance(tuple(map(str, range(args.topics))),
                            tuple(customers), args.players)
        counterexample = inspect(instance)
        if counterexample:
            counterexample.update(trial=trial, seed=args.seed)
            if args.out:
                args.out.write_text(json.dumps(counterexample, indent=2) + "\n")
            print(json.dumps(counterexample, indent=2))
            return
    print(json.dumps({"candidate": "existence of OPT static matching <= W",
        "result": "no counterexample in finite stated search; no proof",
        "trials": args.trials, "topics": args.topics,
        "players": args.players, "seed": args.seed}))


if __name__ == "__main__":
    main()
