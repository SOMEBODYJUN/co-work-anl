#!/usr/bin/env python3
"""Exact missing old-terminal-R queries to named new branch topics.

The input is one saved common-hist point, not a game or a full SPE.
No author row builder, LP solver, or strategy code is imported.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path


PAT = tuple(product((0, 1), repeat=3))
ORBITS = ((0, 0), (1, 0), (1, 1))


def group_key(value):
    f, diagonal, first, second = value
    return (f, diagonal, tuple(first), tuple(second))


def group_multiplicity(hist, group):
    _, diagonal, first, second = group
    n1, n2 = hist[PAT.index(first)], hist[PAT.index(second)]
    if diagonal:
        assert first == second
        return n1
    return n1 * n2 - (n1 if first == second else 0)


def add(row, column, value):
    if value:
        row[column] += value
        if not row[column]:
            del row[column]


def build(point):
    columns = point['columns']
    weights = [F(c['weight']) for c in columns]
    assert all(v >= 0 for v in weights)
    hist = {}
    group_columns = defaultdict(lambda: defaultdict(list))
    source_states = defaultdict(lambda: defaultdict(list))
    current_hist = None
    for index, column in enumerate(columns):
        kind = column['kind']
        if kind == 'hist':
            current_hist = index
            hist[index] = column
            assert len(column['actual_bits']) == 6
            assert sum(column['hist']) == 6
        elif kind == 'joint-reply':
            assert current_hist is not None
            group_columns[current_hist][group_key(column['group'])].append(index)
        elif kind == 'actual-B-family-state':
            source_states[('B', column['source'])][column['hist_column']].append(index)
        elif kind == 'maximum-root-family-state':
            source_states[('M', 1)][column['hist_column']].append(index)

    # Source state masses use the saved *current* hist addresses; joint-reply
    # old addresses are deliberately not interpreted as current addresses.
    for source, by_hist in source_states.items():
        assert set(by_hist) == set(hist)
        for hi, indexes in by_hist.items():
            assert sum((weights[i] for i in indexes), F(0)) == weights[hi]
            for i in indexes:
                expected_len = 5 if source[0] == 'M' else 6 - source[1]
                assert len(columns[i]['hidden']) == expected_len

    targets = []
    for source in sorted(source_states):
        hidden_count = 5 if source[0] == 'M' else 6 - source[1]
        if source[0] == 'M':
            targets.append((source, 'M', None))
        targets.extend((source, 'H', j) for j in range(hidden_count))
        targets.append((source, 'Y-average', None))

    rows = []
    theta_table = []
    for orbit in ORBITS:
        count = 6 if orbit[1] else 30
        profit_row = defaultdict(F)
        theta = {}
        for hi, hc in hist.items():
            background = sum(map(int, hc['actual_bits'][:3]))
            multiplier_sum = 0
            value = F(0)
            for group, indexes in group_columns[hi].items():
                family, diagonal, first, second = group
                if (family, diagonal) != orbit:
                    continue
                multiplicity = group_multiplicity(hc['hist'], group)
                assert multiplicity > 0
                multiplier_sum += multiplicity
                forcing_bit = second[1 if family == 0 else 2]
                denominator = background + first[0] + forcing_bit + 1
                coefficient = F(multiplicity, count * denominator)
                value += coefficient
                assert len(indexes) == 3
                assert {tuple(columns[i]['state']) for i in indexes} == {(0, 1), (1, 0), (1, 1)}
                assert sum((weights[i] for i in indexes), F(0)) <= weights[hi]
                for i in indexes:
                    if columns[i]['state'][0]:
                        add(profit_row, i, coefficient)
            assert multiplier_sum == count
            theta[hi] = value
            theta_table.append({'orbit': list(orbit), 'hist_column': hi, 'theta': str(value)})

        for source, kind, slot in targets:
            row = defaultdict(F, profit_row)
            for hi, indexes in source_states[source].items():
                for i in indexes:
                    c = columns[i]
                    if kind == 'M':
                        member = F(c['M'])
                    elif kind == 'H':
                        member = F(c['hidden'][slot])
                    else:
                        member = F(c['ell'], 6)
                    add(row, i, -theta[hi] * member)
            value = sum((a * weights[i] for i, a in row.items()), F(0))
            name = f"oldR-query-new:{orbit[0]}:{orbit[1]}:{source[0]}:{source[1]}:{kind}:{slot}"
            rows.append({
                'name': name, 'orbit': list(orbit),
                'target_source': list(source), 'target_kind': kind, 'target_slot': slot,
                'slack': str(value), 'slack_float': float(value),
                'coefficients': [[i, str(a)] for i, a in sorted(row.items())]
            })
    assert len(rows) == 57
    return rows, theta_table


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--point', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    raw = args.point.read_bytes()
    point = json.loads(raw)
    rows, theta = build(point)
    negatives = [r for r in rows if F(r['slack']) < 0]
    vectors = {tuple((i, a) for i, a in r['coefficients']) for r in rows}
    output = {
        'scope': '57 valid necessary full-topic IC averages, at one saved relaxation point; not a full SPE',
        'source': str(args.point.resolve()),
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'columns': len(point['columns']),
        'row_count': len(rows), 'distinct_coefficient_vectors': len(vectors),
        'negative_count': len(negatives),
        'minimum_slack': min((r['slack'] for r in rows), key=F),
        'theta': theta, 'rows': rows,
    }
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in output.items() if k not in {'rows', 'theta'}}, ensure_ascii=False))
    for row in sorted(negatives, key=lambda r: F(r['slack'])):
        print(row['name'], row['slack'], row['slack_float'])


if __name__ == '__main__':
    main()
