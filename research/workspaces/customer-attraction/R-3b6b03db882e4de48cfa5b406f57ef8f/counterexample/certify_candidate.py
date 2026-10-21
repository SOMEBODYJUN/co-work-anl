"""Recover one floating cone point exactly and check its complete SPE certificate."""
from cone_search import Game
import argparse
from fractions import Fraction
from functools import reduce
from math import gcd, lcm
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, Instance, StrategyCertificate, verify_certificate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('candidate', type=Path)
    ap.add_argument('--private-floor', type=Fraction, default=Fraction(0))
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    data = json.loads(args.candidate.read_text())
    game = Game(data['topics'], data['players'])
    choices = {(tuple(t['prefix']), t['target']): (t['action'], tuple(t['children']))
               for t in data['choices']}
    root_target = game.tidx[tuple(data['record']['target'])]
    rows = []
    for (q, d), (a, targets) in choices.items():
        rows.extend(game.pay[d, a] - game.pay[targets[b], b]
                    for b in range(game.k) if b != a)
    matrix = np.unique(np.array(rows, dtype=np.int16), axis=0)
    floating = np.array(data['weights'])
    support = np.where(floating > 1e-8)[0].tolist()
    candidates = [(game.cov[root_target], Fraction(1))]
    for row in matrix:
        if abs(row @ floating) < 1e-7:
            candidates.append((row, Fraction(0)))
    for a in range(game.k):
        index = (1 << a) - 1
        if abs(floating[index] - float(args.private_floor)) < 1e-7:
            row = np.zeros(len(floating), dtype=int)
            row[index] = 1
            candidates.append((row, args.private_floor))
    basis = {}
    for row, rhs in candidates:
        r = [Fraction(int(row[j])) for j in support] + [rhs]
        for pivot in sorted(basis):
            coefficient = r[pivot]
            if coefficient:
                r = [x - coefficient * y for x, y in zip(r, basis[pivot])]
        pivot = next((j for j, x in enumerate(r[:-1]) if x), None)
        if pivot is not None:
            coefficient = r[pivot]
            basis[pivot] = [x / coefficient for x in r]
        elif r[-1]:
            raise AssertionError('inconsistent active equalities')
        if len(basis) == len(support):
            break
    assert len(basis) == len(support), (len(basis), len(support))
    solution = [Fraction(0)] * len(support)
    for pivot in sorted(basis, reverse=True):
        row = basis[pivot]
        solution[pivot] = row[-1] - sum(row[j] * solution[j] for j in range(pivot + 1, len(support)))
    weights = [Fraction(0)] * len(floating)
    for index, value in zip(support, solution):
        weights[index] = value
    assert all(value >= 0 for value in weights)
    assert sum(int(c) * w for c, w in zip(game.cov[root_target], weights)) == 1
    for row in matrix:
        assert sum(int(row[j]) * weights[j] for j in support) >= 0
    assert all(weights[(1 << a) - 1] >= args.private_floor for a in range(game.k))
    denominator = lcm(*(w.denominator for w in weights))
    clones = [int(w * denominator) for w in weights]
    divisor = gcd(*clones)
    clones = [v // divisor for v in clones]
    instance = Instance(tuple(f'T{a}' for a in range(game.k)),
                        tuple(CustomerType(frozenset(a for a in range(game.k) if mask & (1 << a)), count)
                              for mask, count in enumerate(clones, 1) if count), game.m)
    actions = {}

    def expand(history, q, target):
        if len(history) == game.m:
            assert game.tidx[q] == target
            return
        action, children = choices[q, target]
        actions[history] = action
        for b in range(game.k):
            child_q = game.children[q][b]
            expand(history + (b,), child_q, children[b])

    expand((), (0,) * game.k, root_target)
    certificate = StrategyCertificate(actions, game.terminals[root_target])
    report = verify_certificate(instance, certificate)
    report.assert_valid()
    w = instance.welfare(game.terminals[root_target])
    opt = instance.optimal_welfare()
    coverage = [{mask for mask, count in enumerate(clones, 1) if count and mask & (1 << a)}
                for a in range(game.k)]
    maximal = [a for a in range(game.k) if not any(coverage[a] < coverage[b] for b in range(game.k))]
    payload = {'status': 'exact SPE point; finite search only', 'source': args.candidate.name,
               'instance': instance.to_dict(), 'certificate': certificate.to_dict(),
               'welfare': w, 'optimum': opt, 'ratio': str(Fraction(opt, w)),
               'decision_histories': len(actions), 'distinct_maximal_coverages': len({frozenset(coverage[a]) for a in maximal}),
               'cone_rows': len(matrix), 'integer_total_customers': sum(clones)}
    args.output.write_text(json.dumps(payload, indent=2))
    print(json.dumps({k: v for k, v in payload.items() if k not in ['certificate', 'instance']}))


if __name__ == '__main__':
    main()
