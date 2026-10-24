#!/usr/bin/env python3
"""Exact small-instance audit of the dynamic threshold candidate.

This is finite evidence only. It enumerates all pure-SPE ordered outcomes through
customer_attraction.ExactSPESolver, then checks OPT <= W + sum threshold(prefix)
for every realized ordered path. It never asserts a universal theorem.
"""
from __future__ import annotations
import argparse, json, random
from itertools import combinations
from fractions import Fraction
from pathlib import Path
from customer_attraction import CustomerType, ExactSPESolver, Instance


def run(topic_count: int, players: int, exhaustive: bool, samples: int, seed: int):
    signatures = tuple(frozenset(s) for k in range(1, topic_count + 1)
                       for s in combinations(range(topic_count), k))
    rng = random.Random(seed)
    masks = list(range(1 << len(signatures))) if exhaustive else [
        rng.randrange(1 << len(signatures)) for _ in range(samples)
    ]
    checked_instances = checked_paths = 0
    min_slack: Fraction | None = None
    min_positive_slack: Fraction | None = None
    positive_witness = None
    witness = None
    for mask in masks:
        customers = tuple(CustomerType(signatures[i])
                          for i in range(len(signatures)) if (mask >> i) & 1)
        instance = Instance(tuple(f"T{i}" for i in range(topic_count)),
                            customers, players)
        solver = ExactSPESolver(instance)
        optimum = instance.optimal_welfare()
        for path in solver.ordered_outcomes():
            counts = (0,) * topic_count
            threshold_sum = Fraction(0)
            for action in path:
                threshold_sum += solver.threshold(counts)
                next_counts = list(counts)
                next_counts[action] += 1
                counts = tuple(next_counts)
            welfare = instance.welfare(counts)
            slack = Fraction(welfare) + threshold_sum - optimum
            checked_paths += 1
            if optimum > 0 and (min_positive_slack is None or slack < min_positive_slack):
                min_positive_slack = slack
                positive_witness = {
                    "mask": mask, "path": path, "welfare": welfare,
                    "optimum": optimum, "threshold_sum": str(threshold_sum),
                    "payoffs": [str(v) for v in instance.player_payoffs(path)],
                }
            if min_slack is None or slack < min_slack:
                min_slack = slack
                witness = {
                    "mask": mask, "path": path, "welfare": welfare,
                    "optimum": optimum, "threshold_sum": str(threshold_sum),
                    "payoffs": [str(v) for v in instance.player_payoffs(path)],
                }
            if slack < 0:
                raise AssertionError({"instance": instance.to_dict(), "path": path,
                                      "welfare": welfare, "optimum": optimum,
                                      "threshold_sum": str(threshold_sum)})
        checked_instances += 1
    return {
        "topic_count": topic_count, "players": players,
        "exhaustive": exhaustive, "samples": samples, "seed": seed,
        "instances": checked_instances, "ordered_paths": checked_paths,
        "min_slack": None if min_slack is None else str(min_slack),
        "min_positive_slack": None if min_positive_slack is None else str(min_positive_slack),
        "witness": witness,
        "positive_witness": positive_witness,
        "status": "finite_audit_only",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topics", type=int, required=True)
    parser.add_argument("--players", type=int, required=True)
    parser.add_argument("--sample", type=int, default=0)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.topics, args.players, args.sample == 0, args.sample, args.seed)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
