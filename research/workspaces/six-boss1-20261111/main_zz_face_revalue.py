"""Recompute true-prefix ZZ Frechet upper bounds on a newly bound point.

Only original own four-state marginals enter. No old auxiliary min or overlap
column is treated as a true intersection. This is a necessary-domain audit,
not a construction or an SPE verification.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json


def canonical(values):
    names = {}
    return ''.join(str(names.setdefault(x, len(names))) for x in values)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('point', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    point = json.loads(args.point.read_bytes())
    columns = point['columns'][:4849]
    hist = {}
    table = defaultdict(dict)
    for index, column in enumerate(columns):
        if column['kind'] == 'hist':
            h = index
            hist[h] = column
        elif column['kind'] == 'joint-reply':
            f, diag, w, v = column['group']
            key = f, diag, tuple(w), tuple(v)
            table[h].setdefault(key, {})[tuple(column['state'])] = F(column['weight'])
    nodes = [e for e in product(range(2), range(6), range(6)) if e[0] or e[1] != e[2]]
    orbits = defaultdict(list)
    for e, (f, i, j) in enumerate(nodes):
        for q, (g, k, l) in enumerate(nodes):
            orbits[f, g, canonical((i, j, k, l))].append((e, q))
    assert len(orbits) == 42 and sum(map(len, orbits.values())) == 4356
    bounds = {o: F() for o in orbits}
    contributions = defaultdict(dict)
    own_report = []
    for h, column in hist.items():
        mass = F(column['weight'])
        words = [w for w, n in zip(product(range(2), repeat=3), column['hist']) for _ in range(n)]
        assert len(words) == 6
        own = []
        for f, i, j in nodes:
            m = table[h][f, int(i == j), words[i], words[j]]
            values = [mass - sum(m.values()), m[0, 1], m[1, 0], m[1, 1]]
            assert min(values) >= 0
            own.append(values)
        p = sum(map(int, column['actual_bits'][:4]))
        for orbit, members in orbits.items():
            value = F()
            for e, q in members:
                qr = own[e][2] + own[e][3]
                vz = own[q][1] + own[q][3]
                ve = own[e][1] + own[e][3]
                value += (ve-vz) / (p+1) + (min(qr, vz)-own[e][3]) / ((p+1)*(p+2))
            value /= len(members)
            contributions[orbit][h] = str(value)
            bounds[orbit] += value
        own_report.append({'hist_column': h, 'mass': str(mass),
                           'positive_own_cells': sum(v > 0 for m in own for v in m),
                           'full_own_nodes': sum(all(m) for m in own)})
    rows = []
    for orbit, members in sorted(orbits.items()):
        rows.append({'orbit': list(orbit), 'literal_queries': len(members),
                     'self_query': all(e == q for e, q in members),
                     'upper': str(bounds[orbit]), 'approx': float(bounds[orbit]),
                     'hist_contributions': contributions[orbit]})
    proper = [r for r in rows if not r['self_query']]
    assert len(proper) == 39
    zero = [r for r in proper if F(r['upper']) == 0]
    negative = [r for r in proper if F(r['upper']) < 0]
    report = {'scope': 'Exact point-specific old ZZ Frechet budgets, not joint feasibility or SPE.',
              'point_path': str(args.point),
              'point_sha256': hashlib.sha256(args.point.read_bytes()).hexdigest(),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'W': point['W'], 'hist': own_report, 'orbit_records': rows,
              'nonself_orbits': len(proper), 'negative_orbits': negative,
              'zero_orbits': [r['orbit'] for r in zero],
              'zero_literal_queries': sum(r['literal_queries'] for r in zero),
              'minimum_positive_upper': str(min(F(r['upper']) for r in proper if F(r['upper']) > 0))}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('point_sha256', 'zero_orbits', 'zero_literal_queries',
                                           'negative_orbits', 'minimum_positive_upper')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
