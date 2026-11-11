"""Exact two-node cyclic transport envelopes on the 66 literal R/Z nodes.

This standalone parser imports no existing matrix or ZZ row generator.
Every true IC is weighted uniformly over customer blocks; only its valid
pointwise/marginal upper potential is selected separately in each block.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def canonical(xs):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in xs)


def group_key(raw):
    return raw[0], raw[1], tuple(raw[2]), tuple(raw[3])


def add(row, col, value):
    if value:
        row[col] = row.get(col, F()) + value
        if not row[col]:
            del row[col]


def row_value(row, masses):
    return sum((v * masses[j] for j, v in row.items()), F())


def parse(path):
    raw = path.read_bytes()
    point = json.loads(raw)
    cols = point['columns'][:4849]
    masses = [F(c['weight']) for c in cols]
    assert len(cols) == 4849 and min(masses) >= 0
    hist = {}
    groups = defaultdict(dict)
    current = None
    for j, c in enumerate(cols):
        if c['kind'] == 'hist':
            hist[j] = c
            current = j
        elif c['kind'] == 'joint-reply':
            g = group_key(c['group'])
            state = tuple(c['state'])
            assert state not in groups[current].setdefault(g, {})
            groups[current][g][state] = j
    for h, gs in groups.items():
        for g, ids in gs.items():
            assert set(ids) == {(0, 1), (1, 0), (1, 1)}
            assert sum(masses[j] for j in ids.values()) <= masses[h]
    return raw, point, cols, masses, hist, groups


def two_node_forms(ie, jf):
    """All six exact dual facets for S = -(r_e-r_f)(z_e-z_f)."""
    b, c, d = ie[0, 1], ie[1, 0], ie[1, 1]
    B, C, D = jf[0, 1], jf[1, 0], jf[1, 1]
    terms = [
        [(b, 1), (c, 1)],
        [(B, 1), (C, 1)],
        [(b, 1), (B, 1)],
        [(c, 1), (C, 1)],
        [(b, 1), (c, 1), (d, 1), (D, -1)],
        [(B, 1), (C, 1), (D, 1), (d, -1)],
    ]
    out = []
    for term in terms:
        row = {}
        for j, v in term:
            add(row, j, F(v))
        out.append(row)
    return out


def audit(path):
    raw, point, cols, masses, hist, groups = parse(path)
    nodes = [(f, i, j) for f, i, j in product(range(2), range(6), range(6))
             if f or i != j]
    assert len(nodes) == 66
    rows = defaultdict(dict)
    totals = defaultdict(F)
    free = defaultdict(F)
    terms = Counter()
    choices = defaultdict(Counter)
    per_hist = defaultdict(dict)
    for hi, h in hist.items():
        words = [word for word, n in zip(product(range(2), repeat=3), h['hist'])
                 for _ in range(n)]
        assert len(words) == 6
        node_group = {
            e: (e[0], int(e[1] == e[2]), words[e[1]], words[e[2]])
            for e in nodes
        }
        compressed = Counter()
        for e in nodes:
            for f in nodes:
                name = (e[0], f[0], canonical((e[1], e[2], f[1], f[2])))
                terms[name] += 1
                rows[name]
                if e != f:
                    compressed[name, node_group[e], node_group[f]] += 1
        p = sum(map(int, h['actual_bits'][:4]))
        denominator = (p + 1) * (p + 2)
        for (name, ge, gf), count in compressed.items():
            forms = two_node_forms(groups[hi][ge], groups[hi][gf])
            values = [row_value(form, masses) for form in forms]
            selected = min(range(6), key=values.__getitem__)
            value = values[selected] * F(count, denominator)
            totals[name] += value
            free[name] += min(values[2:]) * F(count, denominator)
            per_hist[name][hi] = per_hist[name].get(hi, F()) + value
            choices[name][hi, ge, gf, selected] += count
            for j, v in forms[selected].items():
                add(rows[name], j, v * F(count, denominator))
    records = []
    for name in sorted(rows):
        row = rows[name]
        value = row_value(row, masses)
        assert value == totals[name]
        records.append({
            'class': name,
            'value': str(value),
            'free_sum_value': str(free[name]),
            'improvement': str(free[name] - value),
            'literal_pairs_per_hist': terms[name] // len(hist),
            'per_hist': [[h, str(per_hist[name].get(h, F()))] for h in hist],
            'choices': [[h, ge, gf, endpoint, count]
                        for (h, ge, gf, endpoint), count in sorted(choices[name].items())],
            'row': [[j, str(v)] for j, v in sorted(row.items())],
        })
    assert len(records) == 42
    out = {
        'scope': 'Exact two-node cycle envelopes only; not a complete joint realization or SPE',
        'input_path': str(path.resolve()),
        'input_sha256': sha256(raw).hexdigest(),
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'point_W': point['W'],
        'point_exact_verified': point.get('exact_verified'),
        'original_columns_sha256': sha256(json.dumps(
            [{k: v for k, v in c.items() if k != 'weight'} for c in cols],
            sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest(),
        'classes': len(records),
        'nonempty_nonself_classes': sum(bool(r['row']) for r in records),
        'negative_count': sum(F(r['value']) < 0 for r in records),
        'improved_count': sum(F(r['improvement']) > 0 for r in records),
        'minimum': min(records, key=lambda r: F(r['value']))['value'],
        'direction': 'dot(row, x) >= 0',
        'records': records,
    }
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('point', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = audit(args.point)
    args.output.write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'records'}, ensure_ascii=False))
    print('negative', [(r['class'], r['value'], r['free_sum_value'])
                       for r in out['records'] if F(r['value']) < 0])


if __name__ == '__main__':
    main()
