"""Attack the optimal-portfolio static-assignment bridge (not Q-CAG-HALF).

All terminal SPE count vectors come from the repository's set-valued exact
solver.  Each target is an m-tuple with optimal union, repetitions allowed.
For each target multiset, dynamic programming minimizes frozen-opponents
deviation payoffs over every assignment to the actual players.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance, verify_certificate


def minimum_matching(instance: Instance, actual: tuple[int, ...]):
    p, m = instance.topic_count, instance.players
    path = tuple(a for a, count in enumerate(actual) for _ in range(count))
    optimum = instance.optimal_welfare()
    costs = []
    for old in path:
        row = []
        for new in range(p):
            counts = list(actual)
            counts[old] -= 1
            counts[new] += 1
            row.append(instance.topic_payoff(new, counts))
        costs.append(tuple(row))
    best, witness = None, None
    for target in combinations_with_replacement(range(p), m):
        if instance.welfare(instance.counts(target)) != optimum:
            continue
        target_counts = instance.counts(target)

        @lru_cache(None)
        def dp(remaining):
            i = m - sum(remaining)
            if i == m:
                return Fraction(0), ()
            options = []
            for a, count in enumerate(remaining):
                if count:
                    nxt = list(remaining)
                    nxt[a] -= 1
                    value, assignment = dp(tuple(nxt))
                    options.append((costs[i][a] + value, (a,) + assignment))
            return min(options)

        value, assignment = dp(target_counts)
        if best is None or value < best:
            best, witness = value, assignment
    return best, witness


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=1021)
    parser.add_argument('--games', type=int, default=1000)
    parser.add_argument('--players', type=int, default=3)
    parser.add_argument('--topics', type=int, default=5)
    parser.add_argument('--active-types', type=int, default=0)
    parser.add_argument('--max-weight', type=int, default=4)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if min(args.games, args.players, args.topics, args.max_weight) < 1:
        parser.error('games, players, topics and max-weight must be positive')
    if not 0 <= args.active_types < (1 << args.topics):
        parser.error('active-types must lie between zero and 2**topics-1')
    rng = random.Random(args.seed)
    checked, best_gap = 0, None
    result = None
    for game in range(args.games):
        masks = (rng.sample(range(1, 1 << args.topics), args.active_types)
                 if args.active_types else range(1, 1 << args.topics))
        customers = tuple(CustomerType(frozenset(a for a in range(args.topics)
                                               if mask >> a & 1), weight)
                          for mask in masks
                          if (weight := rng.randrange(args.max_weight+1)))
        instance = Instance(tuple(map(str, range(args.topics))), customers, args.players)
        solver = ExactSPESolver(instance)
        for actual in sorted(solver.outcomes()):
            checked += 1
            value, target = minimum_matching(instance, actual)
            welfare = instance.welfare(actual)
            gap = value - welfare
            if best_gap is None or gap > best_gap:
                best_gap = gap
            if gap > 0:
                certificate = solver.certificate(actual)
                verify_certificate(instance, certificate).assert_valid()
                result = dict(status='bridge_counterexample', game=game,
                              instance=instance.to_dict(), counts=actual,
                              matching_value=str(value), target=target,
                              welfare=welfare, optimum=instance.optimal_welfare(),
                              certificate=certificate.to_dict())
                break
        if result:
            break
    result = dict(result or dict(status='no_counterexample_in_finite_run'),
                  seed=args.seed, requested_games=args.games, players=args.players,
                  topics=args.topics, games_processed=game+1,
                  active_types=args.active_types, max_weight=args.max_weight,
                  SPE_count_vectors_checked=checked, maximum_gap=str(best_gap))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
    print(json.dumps({k:v for k,v in result.items()
                      if k not in {'instance', 'certificate'}}, ensure_ascii=False))


if __name__ == '__main__':
    main()
