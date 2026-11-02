"""Independent Fraction reconstruction of one saved route/size-halfspace certificate.

No original row module, NumPy, LP solver, or SPE solver is imported. The full
row-name roster binds the saved indices; only the 19 positive rows are evaluated.
"""
from __future__ import annotations

import argparse
import ast
from fractions import Fraction as F
import gzip
import hashlib
from itertools import combinations_with_replacement as cwr
import json
from pathlib import Path
import platform
import time


def names_for(hs):
    base = [('M', t) for t in range(6)] + [('L', j) for j in range(7)]
    base += [('T', j, k) for j, k in cwr(range(7), 2)]
    base += [('worst', t, j) for t in range(5) for j in range(7)]
    base += [('H', t, h) for t in range(5) for h in range(1, 128)]
    for marker in (3, 4):
        base += [('profit', marker, tt) for tt in cwr(range(7), marker)]
    out = [('base', d) for d in base]
    for t, h in enumerate(hs):
        for owner in range(7):
            out.append(('ASR', t, owner, h))
    for t, h in enumerate(hs):
        for one in h:
            for other in [(j, k) for j in range(7) for k in range(1, 7 - t)]:
                if other not in h:
                    out.append(('ORD', t, one, other))
    return base, out


def coefficient(i, j, name, route):
    membership = lambda k: int(bool(i & (1 << k)))
    share = lambda t: F(1, j.bit_count()) if j & (1 << t) else F()
    past = lambda t: (j & ((1 << t) - 1)).bit_count()
    if name[0] == 'ORD':
        _, t, (a, k), (b, ell) = name
        prefix = route[:t]
        return F(membership(a), prefix.count(a) + k) - F(membership(b), prefix.count(b) + ell)
    assert name[0] == 'base'
    desc = name[1]
    kind = desc[0]
    if kind == 'M':
        t = desc[1]
        shared = (F(1, 21), F(2, 37), F(1, 16), F(2, 27), F(1, 11), F(7, 72))
        floor = F(1, 6) if i.bit_count() == 7 else F(1, 12) if i.bit_count() == 1 else shared[t]
        return share(t) - floor
    if kind == 'L':
        return share(5) - F(membership(desc[1]), past(5) + 1)
    if kind == 'T':
        overlap = past(4)
        load = membership(desc[1]) + membership(desc[2])
        tax = F(int(bool(j & (1 << 4))), (overlap + 1) * (overlap + 2))
        return share(4) + share(5) + tax - (F(load, overlap + load) if load else F())
    if kind == 'worst':
        _, t, label = desc
        return share(t) - F(membership(label), past(t) + 6 - t)
    if kind == 'H':
        _, t, selected = desc
        r = 6 - t
        factor = r + selected.bit_count() - 1
        if i.bit_count() == 7:
            floor = F(1, 6)
        elif i.bit_count() == 1:
            floor = F(int(bool(i & selected)), factor * (past(t) + 1))
        else:
            floor = F((i & selected).bit_count(), factor * (past(t) + r))
        return share(t) - floor
    raise AssertionError(('unexpected positive row', name))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    raw = args.input.read_bytes()
    source = json.loads(raw)
    route = tuple(source['route'])
    assert route == (0, 0, 0, 0, 1, 0) and source['K'] == 125
    hs = [tuple(map(tuple, h)) for h in source['Hs']]
    base, names = names_for(hs)
    assert len(base) == 1005 and len(names) == source['rows'] == 1482
    support = []
    for w in source['weights']:
        name = ast.literal_eval(w['name'])
        assert names[w['index']] == name
        weight = F(w['weight'])
        assert weight > 0 and weight.denominator <= 10**9
        support.append((w['index'], name, weight))
    assert len(support) == len({x[0] for x in support}) == 19
    assert all(x[1][0] != 'ASR' for x in support)
    order = [x for x in support if x[1][0] == 'ORD']
    assert len(order) == 1 and order[0][1] == ('ORD', 4, (6, 1), (1, 1))
    columns = []
    for i in range(1, 128):
        eligible = sum(1 << t for t, label in enumerate(route[:-1]) if i & (1 << label))
        last = int(bool(i & 1)) << 5
        sub = eligible
        while True:
            columns.append((i, sub | last))
            if not sub:
                break
            sub = (sub - 1) & eligible
    assert len(columns) == source['cols'] == 1631 and len(set(columns)) == 1631
    residuals = []
    for i, j in columns:
        target = F(int(bool(j))) - F(int(bool(i & 125)), 2)
        value = target - sum((weight * coefficient(i, j, name, route)
                              for _, name, weight in support), F())
        assert value > 0
        assert coefficient(i, j, order[0][1], route) == F(int(bool(i & 64)) - int(bool(i & 2)))
        residuals.append({'I': i, 'J': j, 'residual': str(value)})
    minimum = min(F(x['residual']) for x in residuals)
    witnesses = [[x['I'], x['J']] for x in residuals if F(x['residual']) == minimum]
    assert str(minimum) == source['exact_min'] and source['arg'] in witnesses
    sizes = list(map(F, ('23.8609321669','10.7601323143','0.4811564626',
                        '0.1085592917','1.1094273945','0.4166165803','13.6519395361')))
    for t, selected in enumerate(hs):
        prefix = route[:t]
        ranked = sorted([(sizes[label] / (prefix.count(label) + k), label, k)
                         for label in range(7) for k in range(1, 7 - t)], reverse=True)
        assert tuple((label, k) for _, label, k in ranked[:5 - t]) == selected
    args.output_dir.mkdir(parents=True, exist_ok=False)
    payload = json.dumps(residuals, separators=(',', ':')).encode()
    compressed = gzip.compress(payload, mtime=0)
    (args.output_dir / 'all-1631-residuals.json.gz').write_bytes(compressed)
    report = {
        'scope': 'One fixed saved rational coefficient certificate, independently reconstructed; no LP, original entry, SPE search, or actual-input IC checks.',
        'input_sha256': hashlib.sha256(raw).hexdigest(),
        'base_rows_named': len(base), 'ASR_rows_named': 42, 'order_rows_named': 435,
        'total_rows_named': len(names), 'columns': len(columns),
        'positive_base_weights': 18, 'positive_ASR_weights': 0, 'positive_order_weights': 1,
        'active_coefficients_reconstructed': len(columns) * len(support),
        'exact_min': str(minimum), 'all_minimum_witnesses': witnesses,
        'all_residuals_strictly_positive': True,
        'active_order': {'name': str(order[0][1]), 'weight': str(order[0][2]),
                         'meaning': 'size(B6)-size(B1)'},
        'readme_rounded_size_vector_top_seats_exactly_match': True,
        'residual_payload_sha256': hashlib.sha256(payload).hexdigest(),
        'compressed_residual_sha256': hashlib.sha256(compressed).hexdigest(),
        'python': platform.python_version(), 'elapsed_seconds': time.perf_counter() - started,
        'current_original_entry_runs': 0, 'current_LP_calls': 0,
        'current_SPE_solver_calls': 0,
    }
    (args.output_dir / 'summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
