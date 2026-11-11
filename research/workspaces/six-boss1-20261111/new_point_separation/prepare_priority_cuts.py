#!/usr/bin/env python3
"""Six exact early cuts at the SHA-bound ZZ13931 point; no frozen mutation."""
from __future__ import annotations
import gzip
import hashlib
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RUN = HERE.parent
sys.path.insert(0, str(RUN / 'cross_branch_math'))
import new_theme_early_projections as base
import discover_projection_weights as free

EXPECTED = '3ba6eb84ca024a6e7bf2816eea010f8bfaf6de610a7a93229711af4bd26a671b'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canon(row):
    pairs = row.items() if isinstance(row, dict) else row
    return tuple(sorted((int(i), F(v)) for i, v in pairs if F(v)))


def vector_sha(row):
    return sha(json.dumps([[i, str(v)] for i, v in canon(row)], separators=(',', ':')).encode())


def literal_audit(source, params):
    """Independent literal-successor enumeration on all 64 actual signatures."""
    am, al, bm, bl, mu = params
    assert min(params) >= 0 and source in range(5)
    n = 5 - source
    table = []
    checks = 0
    for actual in product((0, 1), repeat=6):
        p, ell = sum(actual[:source]), sum(actual[:5])
        for t, q in product((0, 1), repeat=2):
            literal = []
            for successor in product((0, 1), repeat=n):
                g = successor[-1]
                s = sum(successor[:-1])
                z = p + t + sum(successor)
                source_cost = F(t, z) if t else F()
                terminal_own = F(g, z) if g else F()
                value = (source_cost
                         + sum((am * F(h, ell+1) + bm*h for h in successor[:-1]), F())
                         + al*F(g, ell+1) + bl*g
                         + mu*(F(q, p+t+s+1)-terminal_own))
                literal.append(value)
                checks += 1
            minimum = min(literal)
            compressed = free.exact_min('portfolio', source, (p, ell, t, q), params)
            assert minimum == compressed
            table.append({'actual': ''.join(map(str, actual)), 't': t, 'q': q,
                          'minimum': str(minimum), 'hidden_count': len(literal)})
    return {'complete_actual_signatures': 64, 'visible_cases': len(table),
            'literal_hidden_candidates_checked': checks,
            'integer_n': n, 'all_literal_and_count_minima_equal': True,
            'table': table}


def main():
    point_path = RUN/'zz_closure_lp/augmented_lp_exact.json'
    matrix_path = RUN/'zz_closure_lp/exact_matrix.json.gz'
    raw = point_path.read_bytes()
    assert sha(raw) == EXPECTED
    point = json.loads(raw)
    matrix_raw = matrix_path.read_bytes()
    matrix = json.loads(gzip.decompress(matrix_raw))
    columns, hist, weights, profits, family, _ = base.topology(point)
    descriptors = [{k: v for k, v in c.items() if k != 'weight'} for c in columns]
    assert descriptors == matrix['columns']
    assert len(columns) == 12803 and len(matrix['rows']) == 13931
    baseline = {}
    for idx, row in enumerate(matrix['rows']):
        baseline.setdefault(canon(row), []).append({'index': idx, 'name': matrix['row_names'][idx]})
    specs = ((2, 'H3', 'H1'), (3, 'H1', 'H3'), (2, 'H3', 'H2'))
    rows = []
    audits = {}
    for seed, forced, query in specs:
        params = base.PORTFOLIO[seed]
        spec = {'name': f'new-theme-portfolio:{seed}:1:M1:{forced}:{query}',
                'mechanism': 'portfolio', 'seed': seed,
                'actual_source_zero_based': 1, 'family': 'M1',
                'forced': forced, 'query': query, 'parameters': list(map(str, params))}
        row = canon(base.row_coefficients(spec, columns, hist, family))
        rows.append((spec, row, (params[0], params[1], F(), params[2], params[3])))
    for _, forced, query in specs:
        params = tuple(map(F, ('0', '0', '3/64', '1/16', '1/16')))
        spec = {'name': f'free-capacity-second:M1:{forced}:{query}',
                'mechanism': 'portfolio-free', 'actual_source_zero_based': 1,
                'family': 'M1', 'forced': forced, 'query': query,
                'parameters': list(map(str, params)),
                'parameter_names': ['alpha_middle', 'alpha_last', 'beta_middle', 'beta_last', 'mu']}
        build_spec = dict(spec, mechanism='portfolio')
        row = canon(free.build_exact_row(build_spec, params, columns, hist, family))
        rows.append((spec, row, params))
    selected = []
    seen = set()
    for spec, row, params in rows:
        assert row and max(i for i, _ in row) < 4849
        value = sum((coefficient*weights[i] for i, coefficient in row), F())
        assert value < 0 and row not in baseline and row not in seen
        seen.add(row)
        pkey = ','.join(map(str, params))
        if pkey not in audits:
            audits[pkey] = literal_audit(1, params)
        selected.append(dict(spec, slack=str(value), slack_float=float(value),
                             coefficients=[[i, str(v)] for i, v in row],
                             sparse_sha256=vector_sha(row), full_column_count=len(columns),
                             original_coordinate_limit=4849,
                             baseline_duplicate_rows=[], full_domain_audit_key=pkey))
    out = {'scope': 'Six valid necessary early cuts at exact ZZ13931; fixed support only, not SPE or half',
           'source': str(point_path), 'source_sha256': EXPECTED,
           'matrix': str(matrix_path), 'matrix_sha256': sha(matrix_raw),
           'columns': len(columns), 'original_columns': 4849, 'baseline_rows': len(matrix['rows']),
           'input_records': 6, 'distinct_rows': 6, 'duplicates': [],
           'all_negative_exact': True, 'all_absent_from_baseline': True,
           'selected_rows': selected, 'full_domain_audits': audits}
    target = HERE/'priority_six_cuts_13931.json'
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'output': str(target), 'sha256': sha(target.read_bytes()),
                      'count': len(selected), 'minimum': min(selected, key=lambda r:F(r['slack']))['slack'],
                      'all_absent_from_13931': True}), flush=True)


if __name__ == '__main__':
    main()
