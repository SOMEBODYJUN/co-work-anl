#!/usr/bin/env python3
"""Check saved rational weights at every ordered history, independently of LP."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import lcm
import json

ROOT = Path(__file__).resolve().parent
certificate = json.loads((ROOT / 'runtime/evidence/certificates/customer_attraction/individual_security_failure.json').read_text())
actions = {tuple(r['history']): r['action'] for r in certificate['strategy']['actions']}
histories = [h for length in range(3) for h in product(range(6), repeat=length)]
assert set(actions) == set(histories)


def finish(history):
    while len(history) < 3:
        history = history + (actions[history],)
    return history


def payoff(weights, terminal, role):
    topic = terminal[role]
    return sum((mass / sum(bool(mask & (1 << a)) for a in terminal)
                for mask, mass in weights.items() if mask & (1 << topic)), F(0))


reports = []
for row in json.loads((ROOT / 'replay_exact_source.json').read_text()):
    weights = {int(k): F(v) for k, v in row['w'].items()}
    assert all(w >= 0 for w in weights.values())
    slacks = []
    for h in histories:
        actual = payoff(weights, finish(h), len(h))
        slacks.extend(actual - payoff(weights, finish(h + (a,)), len(h)) for a in range(6))
    root = payoff(weights, finish(()), 0)
    query = {'uniform': [F(1, 6)] * 6,
             'v3_original': [F(n, 82) for n in (10, 10, 21, 10, 10, 21)],
             'v4_original': [F(n, 118) for n in (25, 25, 9, 25, 25, 9)]}[row['query']]
    # Ordered triples deliberately retain repetitions; they project to 56 backgrounds.
    values = []
    count_vectors = set()
    for background in product(range(6), repeat=3):
        count_vectors.add(tuple(background.count(a) for a in range(6)))
        value = sum((mass * sum(query[a] for a in range(6) if mask & (1 << a))
                     / (1 + sum(bool(mask & (1 << a)) for a in background))
                     for mask, mass in weights.items()), F(0))
        values.append(value)
    assert min(slacks) == F(row['exact_reconstruction_IC'])
    assert root == F(row['root'])
    assert min(values) == F(row['fixed_query_guarantee'])
    scale = lcm(*(w.denominator for w in weights.values()))
    reports.append({'query': row['query'], 'ordered_history_nodes': len(histories),
                    'action_comparisons': len(slacks), 'ordered_backgrounds': len(values),
                    'distinct_backgrounds': len(count_vectors), 'root': str(root),
                    'minimum_IC': str(min(slacks)), 'minimum_IC_decimal': float(min(slacks)),
                    'query_guarantee': str(min(values)), 'scale': scale,
                    'scaled_customer_count': int(scale * sum(weights.values())),
                    'is_complete_SPE_after_integer_scaling': min(slacks) >= 0,
                    'fixed_query_below_root': min(values) < root})
print(json.dumps(reports, ensure_ascii=False, indent=2))
