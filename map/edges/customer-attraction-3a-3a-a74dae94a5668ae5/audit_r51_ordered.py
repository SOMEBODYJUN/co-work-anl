"""Independent full ordered-history recursion for R-51's finite replay."""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
from random import Random
import sys


def audit(weights, m, p):
    labels = range(p)
    queries = tuple(combinations_with_replacement(labels, m))
    sequences = tuple(product(labels, repeat=m))

    def mask(path):
        return sum(1 << a for a in set(path))

    def coverage(mask_):
        return sum(n for b, n in enumerate(weights) if b & mask_)

    def terminal_payoff(path):
        return tuple(sum((Fraction(n, sum(bool((1 << b) & interests) for b in path))
                          for interests, n in enumerate(weights) if n and interests & (1 << a)),
                         Fraction()) for a in path)

    @lru_cache(None)
    def payoffs(path):
        return terminal_payoff(path)

    @lru_cache(None)
    def continuations(h):
        if len(h) == m:
            return (h,)
        children = [continuations(h + (a,)) for a in labels]
        i = len(h)
        floor = max(min(payoffs(z)[i] for z in child) for child in children)
        return tuple(z for child in children for z in child if payoffs(z)[i] >= floor)

    roots = continuations(())
    assert roots and set(roots) <= set(sequences)
    best = max(coverage(mask(z)) for z in queries)
    optimal = tuple(z for z in queries if coverage(mask(z)) == best)
    answers = []
    for z in roots:
        totals = [Fraction() for _ in labels]
        for i, a in enumerate(z):
            for b in labels:
                totals[b] += (payoffs(z)[i] if b == a else
                              min(payoffs(q)[i] for q in continuations(z[:i] + (b,))))
        actual_welfare = coverage(mask(z))
        for q in optimal:
            query = sum(totals[a] for a in q)
            slack = (m - 1) * actual_welfare + query - m * best
            answers.append((slack, z, q, actual_welfare, query, best))
    return min(answers), len(roots)


def sample_cases():
    random = Random(734170)
    for _ in range(300):
        yield [0] + [random.choices([0, 1, 2, 3, 5, 8], [8, 8, 3, 2, 1, 1])[0]
                     for _ in range(31)]


def from_json(source):
    case = json.loads(source.read_text())
    topic_count = len(case["topics"])
    weights = [0] * (1 << topic_count)
    for item in case["customers"]:
        mask = sum(1 << a for a in item["topics"])
        weights[mask] += item.get("multiplicity", 1)
    return weights, case["players"], topic_count


def record(result):
    (slack, path, portfolio, w, query, opt), credible_paths = result
    return {"slack": str(slack), "path": path, "portfolio": portfolio,
            "W": w, "query": str(query), "OPT": opt, "credible_paths": credible_paths}


def main(folder):
    results = [audit(weights, 3, 5) for weights in sample_cases()]
    sample, best = min(enumerate(results), key=lambda result: (result[1][0][0], result[0]))
    official = [json.loads(line) for line in (folder / "run300.stdout").read_text().splitlines()]
    running = None
    observed = []
    for i, result in enumerate(results):
        row = record(result)
        if running is None or Fraction(row["slack"]) < running:
            running = Fraction(row["slack"])
            observed.append((i, row))
    assert [(i, row["slack"]) for i, row in observed] == [
        (row["sample"], row["slack"]) for row in official
    ]
    assert sample == 23 and best[0][0] == 16
    assert sum(result[0][0] < 0 for result in results) == 0
    print(json.dumps({"samples": len(results), "negative_samples": 0,
                      "minimum_sample": sample, "minimum": record(best),
                      "total_ordered_paths_across_samples": sum(result[1] for result in results),
                      "running_minima": observed,
                      "additional_inputs": {name: record(audit(*from_json(folder / f"{name}.json")))
                                            for name in ["smoke_input", "big_family"]},
                      "boundaries": {"one_player_empty_customers": record(audit([0, 0], 1, 1)),
                                     "two_players_empty_customers": record(audit([0, 0], 2, 1))}},
                     indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
