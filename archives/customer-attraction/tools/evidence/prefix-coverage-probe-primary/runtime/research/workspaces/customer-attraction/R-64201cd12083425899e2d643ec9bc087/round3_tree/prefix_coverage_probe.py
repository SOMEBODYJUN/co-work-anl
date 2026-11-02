"""Attack 2*new_coverage + old_coverage >= k-topic residual optimum.

Finite exploratory search only. Uses the canonical set-valued full-history
SPE oracle; fixed old providers are a prefix, not active additional players.
"""
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import argparse
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver


def coverage(instance, counts, excluded=()):
    return sum(c.multiplicity for c in instance.customers
               if any(counts[a] for a in c.topics)
               and not any(excluded[a] for a in c.topics))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topics', type=int, default=5)
    parser.add_argument('--future', type=int, default=4)
    parser.add_argument('--old', type=int, default=2)
    parser.add_argument('--samples', type=int, default=100)
    parser.add_argument('--seed', type=int, default=2026102112)
    parser.add_argument('--output')
    args = parser.parse_args()
    rng = random.Random(args.seed)
    p, k, old = args.topics, args.future, args.old
    best = None
    for iteration in range(args.samples):
        weights = [rng.randrange(20) if rng.random() < .35 else 0
                   for _ in range(1, 1 << p)]
        inst = Instance(tuple(map(str, range(p))),
                        tuple(CustomerType(frozenset(a for a in range(p) if b >> a & 1), w)
                              for b, w in enumerate(weights, 1) if w), old + k)
        solver = ExactSPESolver(inst)
        for history in combinations_with_replacement(range(p), old):
            prefix = inst.counts(history)
            old_cov = inst.welfare(prefix)
            residual = max(sum(c.multiplicity for c in inst.customers
                               if not any(prefix[a] for a in c.topics)
                               and c.topics.intersection(comparison))
                           for comparison in combinations(range(p), min(k, p)))
            for terminal in solver.outcomes(prefix):
                new_cov = coverage(inst, terminal, prefix)
                slack = 2 * new_cov + old_cov - residual
                if best is None or slack < best['slack']:
                    best = dict(iteration=iteration, weights=weights, prefix=prefix,
                                terminal=terminal, old_coverage=old_cov,
                                new_coverage=new_cov, residual_optimum=residual, slack=slack)
                if slack < 0:
                    result = dict(status='counterexample', config=vars(args), best=best)
                    if args.output:
                        Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
                    print(json.dumps(result, indent=2))
                    return
    result = dict(status='finite-no-counterexample', config=vars(args), best=best)
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
