"""Parent reconstruction of saved root-branch coefficient certificates.

This program reads only the explicit certificate and the separately frozen old
lifted point. It neither imports the author's verifier nor modifies its input.
The mathematical validity of the primitive rows is reviewed in the note.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np


def audit(path):
    raw = path.read_bytes()
    cert = json.loads(raw)
    labels = list(cert['names'])
    paths = [list(p) for p in cert['paths']]
    genuine = cert['first_genuine']
    assert len(set(labels)) == len(labels)
    assert all(len(p) == 6 and set(p) <= set(labels) for p in paths)
    assert paths[0][0] == 'T' and genuine[0] == 1
    edges = {f'COPY:{s}:{i}:{t}': (s, i, t)
             for s, i, t in cert['copy_edges']}
    for s, i, t in edges.values():
        assert paths[s][:i] == paths[t][:i]
        assert i >= genuine[s] and genuine[t] == i + 1
    weights = cert['multipliers_numerators']
    den, equality = cert['denominator'], cert['equality_numerator']
    assert type(den) is int and den > 0
    assert all(type(v) is int and v >= 0 for v in weights.values())
    # Each scaled primitive coefficient has absolute value <= 12*60.
    bound = 60 * (den + abs(equality) + 12 * sum(weights.values()))
    assert bound < 2**63
    reciprocal = np.array([0] + [60 // i for i in range(1, 7)], dtype=np.int64)
    assert all(60 % i == 0 for i in range(1, 7))
    min_residual, zero_count, count = None, 0, 0
    for start in range(0, 2**len(labels), 16384):
        ids = np.arange(start, min(start + 16384, 2**len(labels)), dtype=np.int64)
        membership = {a: ((ids >> j) & 1) for j, a in enumerate(labels)}
        bits = [[membership[a] for a in p] for p in paths]
        prefix = [[np.zeros_like(ids)] for _ in paths]
        for j in range(len(paths)):
            for b in bits[j]:
                prefix[j].append(prefix[j][-1] + b)
        profits = [[b * reciprocal[prefix[j][6]] for b in bits[j]]
                   for j in range(len(paths))]
        # Negative primitive rows (<=0) on the customer columns.
        total = den * profits[0][0] - 60 * equality * membership['T']
        for label, weight in weights.items():
            fields = label.split(':')
            kind = fields[0]
            if kind == 'CAP':
                assert fields[1] != 'T'
                row = 60 * membership[fields[1]]
            elif kind == 'COPY':
                s, i, t = edges[label]
                row = profits[t][i] - profits[s][i]
            elif kind == 'SAFE':
                j, i, a = int(fields[1]), int(fields[2]), fields[3]
                assert genuine[j] <= i <= 5
                row = membership[a] * reciprocal[prefix[j][i] + 6 - i] - profits[j][i]
            elif kind == 'LASTO':
                j = int(fields[1])
                assert genuine[j] <= 5
                p = prefix[j][5]
                row = -6 * profits[j][5] - p * reciprocal[p + 1]
            elif kind == 'PAIRO':
                j = int(fields[1])
                assert genuine[j] <= 4
                p = prefix[j][4]
                divisor = (p + 1) * (p + 2)
                assert np.all(60 % divisor == 0)
                tax = bits[j][4] * (60 // divisor)
                row = -3 * (profits[j][4] + profits[j][5] + tax) - p * reciprocal[p + 1]
            else:
                raise AssertionError(label)
            assert np.max(np.abs(row)) <= 720
            total = total + weight * row
        current = int(total.min())
        min_residual = current if min_residual is None else min(min_residual, current)
        zero_count += int(np.count_nonzero(total == 0))
        count += len(ids)
    assert min_residual >= 0
    alpha = F(sum(v for k, v in weights.items() if k.startswith(('LASTO:', 'PAIRO:'))), den)
    beta = F(equality - sum(v for k, v in weights.items() if k.startswith('CAP:')), den)
    assert alpha >= 0
    # The old necessary-condition point is a separate input, never an SPE.
    old = Path(__file__).resolve().parent.parent / 'R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json'
    old_raw = old.read_bytes()
    point = json.loads(old_raw)
    root_profit, capital = F(0), None
    actual_welfare = F(0)
    for col in point['columns']:
        if col['kind'] == 'K':
            capital = F(col['weight'])
        elif col['kind'] == 'hist':
            b = list(map(int, col['actual_bits']))
            if sum(b):
                actual_welfare += F(col['weight'])
                root_profit += F(col['weight']) * b[0] / sum(b)
    assert actual_welfare == F(point['W'])
    margin = root_profit - alpha * F(point['O']) - beta * capital
    return dict(input=str(path.name), sha256=hashlib.sha256(raw).hexdigest(),
                states=count, integer_bound=bound, min_residual=min_residual,
                zero_states=zero_count, alpha=str(alpha), beta=str(beta),
                old_point_sha256=hashlib.sha256(old_raw).hexdigest(),
                old_point_margin=str(margin), separates_old_point=margin < 0,
                status='independent parent coefficient reconstruction; local row only')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='+', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    results = [audit(path) for path in args.inputs]
    args.output.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
