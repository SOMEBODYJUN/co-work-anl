"""Exploratory exact check of the uniform actual-prefix portfolio interface.

This is not a search for the half-coverage conjecture's negation.  For each
sampled input it minimizes the portfolio queries over continuations compatible
with a selected actual path, using the canonical exact all-SPE solver.
"""
import argparse
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance


def check(instance):
    solver = ExactSPESolver(instance)
    optimum = instance.optimal_welfare()
    opt_supports = []
    for size in range(1, min(instance.players, instance.topic_count) + 1):
        for support in combinations(range(instance.topic_count), size):
            counts = tuple(int(a in support) for a in range(instance.topic_count))
            if instance.welfare(counts) == optimum:
                opt_supports.append(support)
    best = None
    for history in solver.ordered_outcomes():
        actual_counts = instance.counts(history, terminal=True)
        actual_utilities = instance.topic_payoffs(actual_counts)
        query_sums = [Fraction(0)] * instance.topic_count
        prefix = [0] * instance.topic_count
        for chosen in history:
            for a in range(instance.topic_count):
                if a == chosen:
                    query_sums[a] += actual_utilities[a]
                else:
                    child = prefix.copy()
                    child[a] += 1
                    query_sums[a] += min(instance.topic_payoff(a, q)
                                         for q in solver.outcomes(child))
            prefix[chosen] += 1
        welfare = instance.welfare(actual_counts)
        for support in opt_supports:
            padding = min(support, key=lambda a: query_sums[a])
            portfolio = support + (padding,) * (instance.players - len(support))
            query = sum(query_sums[a] for a in portfolio)
            slack = (instance.players - 1) * welfare + query - instance.players * optimum
            candidate = (slack, history, portfolio, welfare, query)
            if best is None or candidate[0] < best[0]:
                best = candidate
    return best, solver


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=int, default=3)
    parser.add_argument('--topics', type=int, default=5)
    parser.add_argument('--samples', type=int, default=100)
    parser.add_argument('--seed', type=int, default=734170)
    parser.add_argument('--input')
    parser.add_argument('--output')
    args = parser.parse_args()
    rng = random.Random(args.seed)
    minimum = None
    for sample in range(args.samples if args.input is None else 1):
        if args.input:
            instance = Instance.from_dict(json.loads(Path(args.input).read_text()))
        else:
            customers = []
            for mask in range(1, 1 << args.topics):
                weight = rng.choices([0, 1, 2, 3, 5, 8], [8, 8, 3, 2, 1, 1])[0]
                if weight:
                    customers.append(CustomerType(frozenset(a for a in range(args.topics)
                                                           if mask & (1 << a)), weight))
            instance = Instance(tuple(map(str, range(args.topics))), tuple(customers), args.players)
        result, solver = check(instance)
        if minimum is None or result[0] < minimum:
            minimum = result[0]
            print(json.dumps({'sample': sample, 'slack': str(minimum), 'path': result[1],
                              'portfolio': result[2], 'W': result[3], 'query': str(result[4]),
                              'OPT': instance.optimal_welfare()}, ensure_ascii=False), flush=True)
        if result[0] < 0:
            if args.output:
                output = {'instance': instance.to_dict(), 'slack': str(result[0]),
                          'path': result[1], 'portfolio': result[2], 'W': result[3],
                          'query': str(result[4]), 'certificate': solver.certificate(on_path=result[1]).to_dict()}
                Path(args.output).write_text(json.dumps(output, indent=2) + '\n')
            break


if __name__ == '__main__':
    main()
