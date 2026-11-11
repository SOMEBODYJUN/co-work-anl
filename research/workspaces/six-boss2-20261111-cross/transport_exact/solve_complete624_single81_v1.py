#!/usr/bin/env python3
"""Gated solve and exact certificates for complete624 + 81 separate minima.

Only this directory receives writes.  The 20701 x 20585 matrix stays intact;
support selection and symbolic elimination are recovery devices, not domain
deletion.  Every accepted certificate is checked against all rational rows and
columns.  This finite necessary system is not a complete-history SPE system.
"""
from __future__ import annotations

from array import array
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import argparse
import datetime
import gzip
import hashlib
import json
import math
import platform
import resource
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RUN = HERE.parent
ROOT = HERE.parents[3]
MASTER = RUN / 'master_cuts'
PARENT_MATRIX = RUN / 'joint_requery/complete624_actual4_R00_v1_matrix.json.gz'
PARENT_SHA = '556c3cac51e87a699d1f3a9c427f556836932b6fc2399fa330f375c6efd8231a'
PARENT_POINT = MASTER / 'complete624_actual4_R00_opt_v2_exact.json'
PARENT_POINT_SHA = '02bcb92f33f7e7e4fac00a4c64fd39b0a4f0c68a736559c300bbfba255168817'
EXTENSION = ROOT / 'research/workspaces/six-boss1-20261111/tail_constraints/single-query-epigraph.json'
EXTENSION_SHA = '964ef22c37f9338a5e29423ff6009611256f5720b5f0b7016bb55940e570a94c'
ZZ_MAP = MASTER / 'complete_zz_5799_v1_mapping.json'
ZZ_MAP_SHA = '2305633361e0e543fbcb11497a555445460c80d2d4ff1bd3f844e0964b37ca6a'
MACRO_MAP = RUN / 'joint_requery/complete624_actual4_R00_v1_mapping.json'
MACRO_MAP_SHA = '24a601ebc1e2f7dc5e175bca453a5ab05433e046dfc7c2a782e830849817d109'
ENGINE = MASTER / 'merge_master.py'
ENGINE_SHA = '2afa5e8d9713c39170c547cdfa8b63ad5da8079668b669c0e961e29628999a6c'
SEMANTIC_SHA = 'afce2dcdff01e9393c04e317ee6bd52f5c0b378daedd92816647412243362460'
SCOPE = ('Fixed16 complete624/ZZ plus the full epigraph extension for 81 separate '
         'single-query minimum costs. Finite necessary LP only; neither common '
         'transport, the 12 paired-query bounds, nor complete-history SPE is asserted.')
ROW_COUNT, COL_COUNT = 20701, 20585
OLD_ROWS, OLD_COLS, SEMANTIC_COLS = 12666, 12631, 4849
ARGS = None


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def canonical_sha(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()


def log(stage, **kw):
    print(json.dumps({'stage': stage, **kw}, ensure_ascii=False), flush=True)


def path(kind):
    assert ARGS.label and all(c.isalnum() or c in '_-' for c in ARGS.label)
    return HERE / f'{ARGS.label}_{kind}'


def write(kind, value):
    p = path(kind + '.json')
    with p.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')
    return p


@lru_cache(None)
def frac(v):
    return F(v)


def check_gate():
    """No optimization/recovery is reachable without a SHA-bound Main PASS."""
    assert ARGS.matrix_sha and len(ARGS.matrix_sha) == 64
    assert sha(ARGS.matrix) == ARGS.matrix_sha, 'matrix SHA mismatch'
    if ARGS.mode == 'preflight':
        return None
    assert ARGS.review is not None, 'Main review file is required'
    review = json.loads(ARGS.review.read_text())
    assert review['status'] == 'PASS', 'Main matrix review is not PASS'
    assert review['matrix_sha256'] == ARGS.matrix_sha, 'Main review binds another matrix'
    return review


def load():
    check_gate()
    for p, digest in [(PARENT_MATRIX, PARENT_SHA), (EXTENSION, EXTENSION_SHA),
                      (ZZ_MAP, ZZ_MAP_SHA), (MACRO_MAP, MACRO_MAP_SHA), (ENGINE, ENGINE_SHA)]:
        assert sha(p) == digest, str(p)
    with gzip.open(ARGS.matrix, 'rt', encoding='utf-8') as f:
        data = json.load(f)
    assert (data['row_count'], data['column_count']) == (ROW_COUNT, COL_COUNT)
    assert len(data['rows']) == ROW_COUNT and len(data['columns']) == COL_COUNT
    assert len(data['objective']) == COL_COUNT and len(data['normalization']) == COL_COUNT
    assert canonical_sha(data['columns'][:SEMANTIC_COLS]) == SEMANTIC_SHA
    assert all(F(v) == 0 for v in data['objective'][OLD_COLS:])
    assert all(F(v) == 0 for v in data['normalization'][OLD_COLS:])
    ext = json.loads(EXTENSION.read_text())
    assert data['columns'][OLD_COLS:] == ext['new_columns']
    aux = {}
    budgets = []
    for local, source in enumerate(ext['rows']):
        i = OLD_ROWS + local
        target = data['rows'][i]
        transformed = [[j if j < SEMANTIC_COLS else OLD_COLS + j - SEMANTIC_COLS, v]
                       for j, v in source['coefficients']]
        assert target['index'] == i and target['name'] == 'single81:' + source['name']
        assert target['nonzero'] == transformed
        assert target['sparse_sha256'] == canonical_sha(transformed)
        new = [(j, F(v)) for j, v in transformed if j >= OLD_COLS]
        assert all(j < SEMANTIC_COLS or j >= OLD_COLS for j, _ in transformed)
        if source['kind'] in ('tail-threshold', 'Z-threshold'):
            assert len(new) == 1 and new[0][1] == 1
            j = new[0][0]
            assert j not in aux
            aux[j] = {'column': j, 'threshold': i, 'kind': source['kind'],
                      'old_part': [(k, F(v)) for k, v in transformed if k < SEMANTIC_COLS]}
        else:
            assert source['kind'] in ('tail-budget', 'Z-budget')
            budgets.append(i)
            for j, v in new:
                assert v < 0 and j in aux and 'budget' not in aux[j]
                aux[j].update(budget=i, beta=-v)
    assert len(aux) == 7954 and len(budgets) == 81
    assert set(aux) == set(range(OLD_COLS, COL_COUNT))
    assert all('budget' in a for a in aux.values())
    rows = []
    for i, r in enumerate(data['rows']):
        assert r['index'] == i
        row = {j: frac(v) for j, v in r['nonzero']}
        assert len(row) == len(r['nonzero']) and all(row.values())
        rows.append(row)
    assert sum(map(len, rows)) == 3044395
    return data, rows, list(map(frac, data['objective'])), list(map(frac, data['normalization'])), aux, budgets


def preflight():
    """Read-only structural validation.  Does not import or call an optimizer."""
    began = time.time()
    data, rows, obj, norm, aux, budgets = load()
    with gzip.open(PARENT_MATRIX, 'rt', encoding='utf-8') as f:
        old = json.load(f)
    assert data['columns'][:OLD_COLS] == old['columns']
    assert data['rows'][:OLD_ROWS] == old['rows']
    assert data['objective'][:OLD_COLS] == old['objective']
    assert data['normalization'][:OLD_COLS] == old['normalization']
    for r in data['rows']:
        assert canonical_sha(r['nonzero']) == r['sparse_sha256']
    out = {'status': 'PASS_STRUCTURAL_ONLY', 'scope': SCOPE,
           'matrix_sha256': ARGS.matrix_sha, 'parent_matrix_sha256': PARENT_SHA,
           'extension_sha256': EXTENSION_SHA, 'rows': ROW_COUNT, 'columns': COL_COUNT,
           'nonzeros': sum(map(len, rows)), 'all_parent_objects_unchanged': True,
           'all_extension_rows_exactly_remapped': True, 'new_auxiliaries': len(aux),
           'new_budgets': len(budgets), 'optimizer_calls': 0,
           'main_coefficient_review_required_for_solve': True, 'seconds': time.time() - began}
    write('preflight', out)
    log('structural-preflight-passed', **out)


def solve():
    import numpy as np
    import scipy
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix
    assert not path('float.npz').exists() and not path('float.json').exists()
    began = time.time()
    data, rows, obj, norm, aux, budgets = load()
    rr, cc, vv = array('i'), array('i'), array('d')
    scales = []
    for i, row in enumerate(rows):
        scale = max((abs(float(v)) for v in row.values()), default=1.0)
        assert scale > 0
        scales.append(scale)
        for j, v in row.items():
            rr.append(i); cc.append(j); vv.append(-float(v) / scale)
    mat = csr_matrix((np.frombuffer(vv, dtype=np.float64),
                      (np.frombuffer(rr, dtype=np.int32), np.frombuffer(cc, dtype=np.int32))),
                     shape=(ROW_COUNT, COL_COUNT))
    log('float-start', rows=ROW_COUNT, columns=COL_COUNT, nonzeros=int(mat.nnz),
        load_seconds=time.time() - began, method='highs-ipm with crossover')
    options = {'primal_feasibility_tolerance': 1e-10, 'dual_feasibility_tolerance': 1e-10,
               'ipm_optimality_tolerance': 1e-12, 'time_limit': ARGS.time_limit}
    sol = linprog(list(map(float, obj)), A_ub=mat, b_ub=np.zeros(ROW_COUNT),
                  A_eq=csr_matrix([list(map(float, norm))]), b_eq=[1], bounds=(0, None),
                  method='highs-ipm', options=options)
    out = {'scope': SCOPE, 'float_only': True, 'success': bool(sol.success),
           'status': int(sol.status), 'message': sol.message,
           'W_float': None if sol.fun is None else float(sol.fun),
           'matrix_sha256': ARGS.matrix_sha, 'rows': ROW_COUNT, 'columns': COL_COUNT,
           'method': 'highs-ipm with crossover', 'options': options,
           'numpy': np.__version__, 'scipy': scipy.__version__,
           'seconds': time.time() - began,
           'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if sol.x is not None:
        with path('float.npz').open('xb') as f:
            np.savez(f, x=sol.x, scaled_slacks=sol.ineqlin.residual,
                     inequality_marginals=sol.ineqlin.marginals,
                     equality_marginals=sol.eqlin.marginals,
                     lower_marginals=sol.lower.marginals, scales=np.array(scales))
        out.update(iterations=int(sol.nit),
                   crossover_iterations=int(getattr(sol, 'crossover_nit', 0)),
                   positive_columns_selected=int(sum(sol.x > ARGS.support_tolerance)),
                   minimum_scaled_slack_float=float(min(sol.ineqlin.residual)),
                   minimum_lower_marginal_float=float(min(sol.lower.marginals)))
    write('float', out)
    log('float-finished', **out)
    assert sol.success, sol.message


def exact_slacks(rows, x):
    return [sum((a * x[j] for j, a in row.items() if x[j]), F()) for row in rows]


def selected_primal_system(rows, norm, aux, fl):
    import numpy as np
    fx = fl['x'].copy()
    # Decreasing each epigraph variable to its positive part preserves every
    # old row and can only increase its unique budget; this is face discovery.
    max_change = 0.0
    for j, a in aux.items():
        canonical = max(0.0, -math.fsum(float(v) * fx[k] for k, v in a['old_part']))
        max_change = max(max_change, abs(float(fx[j]) - canonical))
        fx[j] = canonical
    positive = {int(j) for j in np.flatnonzero(fx > ARGS.support_tolerance)}
    sl = np.array([math.fsum(float(v) * fx[j] for j, v in row.items()) / scale
                   for row, scale in zip(rows, fl['scales'])])
    dependent, definitions = {}, []
    zz = json.loads(ZZ_MAP.read_text())
    for a in zz['auxiliaries']:
        j = a['column_index']
        if j not in positive:
            continue
        for rk, ck in [('upper_q_row', 'source_R_columns'), ('upper_v_row', 'query_Z_columns')]:
            if abs(sl[a[rk]]) < ARGS.dependency_tolerance:
                expression = {k: F(1) for k in a[ck] if k in positive}
                if not expression:
                    continue
                dependent[j] = expression
                definitions.append({'column': j, 'kind': 'ZZ_upper', 'row': a[rk],
                                    'expression': [[k, str(v)] for k, v in expression.items()]})
                break
    mapping = json.loads(MACRO_MAP.read_text())
    for group in mapping['groups']:
        for state in group['states']:
            pos = [j for j in state['hidden_columns'] if j in positive]
            if not pos:
                continue
            j = max(pos, key=lambda k: fx[k])
            expression = {k: F(v) for k, v in state['old_marginal_affine'] if k in positive}
            expression.update({k: F(-1) for k in pos if k != j})
            dependent[j] = expression
            definitions.append({'column': j, 'kind': 'macro_margin', 'row': state['equality_plus_row'],
                                'expression': [[k, str(v)] for k, v in expression.items()]})
    for j, a in aux.items():
        if j not in positive:
            continue
        expression = {k: -v for k, v in a['old_part'] if k in positive}
        assert expression
        dependent[j] = expression
        definitions.append({'column': j, 'kind': 'single81_positive_part', 'row': a['threshold'],
                            'expression': [[k, str(v)] for k, v in expression.items()]})
    core = sorted(positive - set(dependent))
    index = {j: k for k, j in enumerate(core)}
    assert all(k in index for expression in dependent.values() for k in expression)

    def project(row):
        result = defaultdict(F)
        for j, v in row.items():
            if j in dependent:
                for k, a in dependent[j].items():
                    result[index[k]] += v * a
            elif j in index:
                result[index[j]] += v
        return tuple(result.get(k, F()) for k in range(len(core)))

    equations, rhs, origins, seen = [], [], [], set()
    for i, row in enumerate(rows):
        if abs(sl[i]) > ARGS.active_tolerance:
            continue
        small = project(row)
        if not any(small) or small in seen:
            continue
        seen.add(small); equations.append(list(small)); rhs.append(F()); origins.append(i)
    equations.append(list(project({j: v for j, v in enumerate(norm) if v})))
    rhs.append(F(1)); origins.append('O=1')
    return core, dependent, definitions, equations, rhs, origins, max_change


def reconstruct():
    import numpy as np
    sys.path.insert(0, str(MASTER))
    from merge_master import exact_linear_system
    assert not path('exact.json').exists()
    began = time.time()
    data, rows, obj, norm, aux, budgets = load()
    floating = json.loads(path('float.json').read_text())
    assert floating['success'] and floating['matrix_sha256'] == ARGS.matrix_sha
    fl = np.load(path('float.npz'))
    core, dependent, definitions, equations, rhs, origins, change = selected_primal_system(rows, norm, aux, fl)
    log('exact-primal-start', core_variables=len(core), eliminated=len(dependent),
        candidate_equations=len(equations), elimination_kinds=dict(Counter(d['kind'] for d in definitions)))
    values, chosen = exact_linear_system(equations, rhs)
    x = [F()] * COL_COUNT
    for j, v in zip(core, values):
        x[j] = v
    for j, expression in dependent.items():
        x[j] = sum((a * x[k] for k, a in expression.items()), F())
    slacks = exact_slacks(rows, x)
    negative_columns = [[j, str(v)] for j, v in enumerate(x) if v < 0]
    negative_rows = [[i, str(v)] for i, v in enumerate(slacks) if v < 0]
    if negative_columns or negative_rows:
        write('primal_diagnostic', {'negative_columns': negative_columns, 'negative_rows': negative_rows,
                                   'support_tolerance': ARGS.support_tolerance,
                                   'active_tolerance': ARGS.active_tolerance})
    assert min(x) >= 0 and min(slacks) >= 0
    assert sum(n * v for n, v in zip(norm, x)) == 1
    assert all(x[j] == max(F(), -sum((v * x[k] for k, v in a['old_part']), F())) for j, a in aux.items())
    W = sum(c * v for c, v in zip(obj, x))
    out = {'scope': SCOPE, 'exact_feasible': True, 'exact_optimum_claim': False,
           'matrix_sha256': ARGS.matrix_sha, 'matrix_path': str(ARGS.matrix.relative_to(ROOT)),
           'O': '1', 'W': str(W), 'W_float_for_display': float(W), 'K': str(x[0]),
           'strict_half_gap_O_minus_2W': str(1 - 2 * W), 'verified_rows': ROW_COUNT,
           'minimum_slack': str(min(slacks)), 'minimum_column_weight': str(min(x)),
           'positive_columns': sum(v > 0 for v in x),
           'positive_columns_by_block': {name: sum(v > 0 for v in x[a:b]) for name, a, b in
                                         [('original4849', 0, 4849), ('ZZ', 4849, 7639),
                                          ('macro624', 7639, OLD_COLS), ('single81', OLD_COLS, COL_COUNT)]},
           'all_new_auxiliaries_canonical': True,
           'columns': [dict(c, weight=str(v)) for c, v in zip(data['columns'], x)]}
    pp = write('exact', out)
    write('basis', {'core_columns': core, 'dependent_columns': definitions,
                    'chosen_equation_rows': [origins[k] for k in chosen],
                    'candidate_equations': len(equations), 'core_variables': len(core),
                    'floating_new_aux_canonicalization_max_change': change,
                    'support_tolerance': ARGS.support_tolerance, 'active_tolerance': ARGS.active_tolerance,
                    'engine_sha256': ENGINE_SHA, 'seconds': time.time() - began})
    write('slacks', {'point_sha256': sha(pp), 'rows': [
        {'index': i, 'name': data['rows'][i]['name'], 'slack': str(v)} for i, v in enumerate(slacks)]})
    write('single81_budgets', {'point_sha256': sha(pp), 'matrix_sha256': ARGS.matrix_sha,
                              'canonical_at_this_new_point': True, 'negative_count': 0,
                              'minimum_slack': str(min(slacks[i] for i in budgets)),
                              'budgets': [{'row_index': i, 'name': data['rows'][i]['name'],
                                           'slack': str(slacks[i])} for i in budgets]})
    log('exact-primal-passed', W=str(W), W_display=float(W), positive_columns=out['positive_columns'],
        core_variables=len(core), minimum_slack=str(min(slacks)), seconds=time.time() - began)


def solve_scaled_dual(equations, rhs):
    import numpy as np
    from scipy.linalg import qr
    from sympy import ZZ
    from sympy.polys.matrices import DomainMatrix
    n = len(equations[0])
    arr = np.array([[float(v) for v in r] for r in equations])
    scale = np.max(abs(arr), axis=1); scale[scale == 0] = 1
    _, r, piv = qr((arr / scale[:, None]).T, mode='economic', pivoting=True)
    diag = abs(np.diag(r))
    rank = int(sum(diag > 1e-10 * max(diag[0], 1)))
    assert rank == n, ('dual rank', rank, n, diag[-5:].tolist())
    chosen = list(map(int, piv[:n]))
    multipliers = [math.lcm(*(equations[q][k].denominator for q in chosen)) for k in range(n)]
    denominator = math.lcm(*(rhs[q].denominator for q in chosen))
    ae, be = {}, {}
    for k, q in enumerate(chosen):
        for j, v in enumerate(equations[q]):
            if v:
                ae[k, j] = ZZ((v * multipliers[j]).numerator)
        if rhs[q]:
            be[k, 0] = ZZ((rhs[q] * denominator).numerator)
    a = DomainMatrix.from_dok(ae, (n, n), ZZ)
    b = DomainMatrix.from_dok(be, (n, 1), ZZ)
    numer, denom = a.solve_den(b, method='rref')
    values = [F(int(v[0]), int(denom)) * F(m, denominator) for v, m in zip(numer.to_list(), multipliers)]
    assert all(sum(v * x for v, x in zip(equations[q], values)) == rhs[q] for q in chosen)
    return values, chosen


def dual():
    import numpy as np
    assert not path('dual.json').exists()
    began = time.time()
    data, rows, obj, norm, aux, budgets = load()
    pp = path('exact.json'); point = json.loads(pp.read_text())
    assert point['matrix_sha256'] == ARGS.matrix_sha
    x = [F(c['weight']) for c in point['columns']]
    W = F(point['W']); slacks = exact_slacks(rows, x)
    fl = np.load(path('float.npz'))
    scores = -fl['inequality_marginals'] / fl['scales']
    proposed = {int(i) for i in np.flatnonzero(scores > ARGS.dual_support_tolerance)}
    support = {i for i in proposed if slacks[i] == 0}
    active = {j for j in range(COL_COUNT) if x[j] > 0 or abs(fl['lower_marginals'][j]) < ARGS.dual_active_tolerance}
    dependent, definitions = {}, []
    for j, a in aux.items():
        threshold, budget, beta = a['threshold'], a['budget'], a['beta']
        if j not in active:
            continue
        # A zero primal column has no mandatory complementary equation.
        # Exact positive threshold slack forces its multiplier to zero, so a
        # small floating reduced cost must not force a positive budget to zero.
        if x[j] == 0 and slacks[threshold] > 0:
            active.discard(j)
            continue
        if budget in support:
            assert slacks[threshold] == 0
            support.add(threshold)
            dependent[threshold] = {budget: beta}
            definitions.append({'row': threshold, 'kind': 'positive_part_dual_column_balance',
                                'column': j, 'primal_positive': x[j] > 0,
                                'expression': [[budget, str(beta)]]})
        else:
            support.discard(threshold)
    core = sorted(support - set(dependent))
    index = {i: k for k, i in enumerate(core)}
    assert all(k in index for expr in dependent.values() for k in expr)
    columns = defaultdict(lambda: defaultdict(F))
    for i in sorted(support):
        expr = dependent.get(i, {i: F(1)})
        for j, a in rows[i].items():
            for k, v in expr.items():
                columns[j][index[k]] += a * v
    equations, rhs, origins, seen = [], [], [], set()
    for j in sorted(active):
        r = tuple(columns[j].get(k, F()) for k in range(len(core)))
        b = obj[j] - W * norm[j]
        if not any(r):
            assert b == 0, ('empty dual equation with nonzero RHS', j, str(b))
            continue
        if (r, b) in seen:
            continue
        seen.add((r, b)); equations.append(r); rhs.append(b); origins.append(j)
    log('exact-dual-start', floating_support=len(proposed), expanded_support=len(support),
        eliminated=len(dependent), core_unknowns=len(core), candidate_equations=len(equations))
    values, chosen = solve_scaled_dual(equations, rhs)
    multipliers = {i: v for i, v in zip(core, values)}
    for i, expr in dependent.items():
        multipliers[i] = sum(v * multipliers[k] for k, v in expr.items())
    negative = [[i, str(v)] for i, v in sorted(multipliers.items()) if v < 0]
    if negative:
        write('dual_negative_diagnostic', {'negative_multipliers': negative,
                                          'core_rows': core, 'selected_column_equations': [origins[k] for k in chosen]})
    assert not negative
    records = [{'row_index': i, 'row_name': data['rows'][i]['name'], 'weight': str(v)}
               for i, v in sorted(multipliers.items()) if v > 0]
    residual = [c - W * n for c, n in zip(obj, norm)]
    for rec in records:
        i, v = rec['row_index'], F(rec['weight'])
        assert slacks[i] == 0
        for j, a in rows[i].items():
            residual[j] -= v * a
    bad = [[j, str(v)] for j, v in enumerate(residual) if v < 0]
    if bad:
        write('dual_residual_diagnostic', {'negative_columns': bad, 'row_multipliers': records})
    assert not bad and sum(v * r for v, r in zip(x, residual)) == 0
    write('dual', {'status': 'PASS', 'scope': SCOPE, 'primal_value': str(W), 'dual_value': str(W),
                   'normalization_multiplier': str(W), 'matrix_sha256': ARGS.matrix_sha,
                   'point_sha256': sha(pp), 'minimum_dual_residual': str(min(residual)),
                   'positive_multipliers': len(records), 'row_multipliers': records,
                   'residuals': list(map(str, residual)), 'core_rows': core,
                   'dependent_rows': definitions, 'selected_column_equations': [origins[k] for k in chosen],
                   'floating_positive_but_exact_slack_nonzero_rows': sorted(proposed - {i for i in proposed if slacks[i] == 0}),
                   'reconstruction': 'Integer-scaled exact solve after positive-part dual column elimination; all columns verified.',
                   'seconds': time.time() - began})
    log('exact-dual-passed', W=str(W), positive_multipliers=len(records),
        minimum_dual_residual=str(min(residual)), seconds=time.time() - began)


def verify():
    began = time.time()
    data, rows, obj, norm, aux, budgets = load()
    pp, dp = path('exact.json'), path('dual.json')
    point, certificate = json.loads(pp.read_text()), json.loads(dp.read_text())
    assert certificate['matrix_sha256'] == ARGS.matrix_sha and certificate['point_sha256'] == sha(pp)
    assert [{k: v for k, v in c.items() if k != 'weight'} for c in point['columns']] == data['columns']
    for r in data['rows']:
        assert canonical_sha(r['nonzero']) == r['sparse_sha256']
    x = [F(c['weight']) for c in point['columns']]
    assert min(x) >= 0 and sum(n * v for n, v in zip(norm, x)) == 1
    W = sum(c * v for c, v in zip(obj, x))
    assert W == F(point['W']) == F(certificate['dual_value']) == F(certificate['normalization_multiplier'])
    slacks = exact_slacks(rows, x)
    assert min(slacks) >= 0
    assert all(x[j] == max(F(), -sum((v * x[k] for k, v in a['old_part']), F())) for j, a in aux.items())
    residual = [c - W * n for c, n in zip(obj, norm)]
    used = set()
    for rec in certificate['row_multipliers']:
        i, v = rec['row_index'], F(rec['weight'])
        assert i not in used and v > 0; used.add(i)
        assert rec['row_name'] == data['rows'][i]['name'] and v * slacks[i] == 0
        for j, a in rows[i].items():
            residual[j] -= v * a
    assert min(residual) >= 0 and list(map(str, residual)) == certificate['residuals']
    assert sum(v * r for v, r in zip(x, residual)) == 0
    zz = json.loads(ZZ_MAP.read_text())
    canonical_zz = list(x)
    for a in zz['auxiliaries']:
        canonical_zz[a['column_index']] = min(sum(x[j] for j in a['source_R_columns']),
                                              sum(x[j] for j in a['query_Z_columns']))
    zz_slacks = [sum(v * canonical_zz[j] for j, v in rows[c['row_index']].items()) for c in zz['classes']]
    assert min(zz_slacks) >= 0
    assert sha(PARENT_POINT) == PARENT_POINT_SHA
    old_W = F(json.loads(PARENT_POINT.read_text())['W'])
    assert W >= old_W
    projection = {'scope': 'Original 4849-column projection of complete624 plus single81 necessary LP; not SPE.',
                  'exact_feasible': True, 'exact_optimum_claim': False, 'O': '1', 'W': str(W), 'K': str(x[0]),
                  'parent_full_point_sha256': sha(pp), 'parent_full_matrix_sha256': ARGS.matrix_sha,
                  'verified_old_rows': 5799, 'additional_verified_ZZ_min_bounds': 39,
                  'additional_verified_separate_single_query_bounds': 81,
                  'positive_columns': sum(v > 0 for v in x[:SEMANTIC_COLS]),
                  'minimum_old_slack': str(min(slacks[:5799])), 'columns': point['columns'][:SEMANTIC_COLS]}
    proj = write('original4849_exact', projection)
    hist = [dict(c, column_index=j) for j, c in enumerate(projection['columns']) if c['kind'] == 'hist']
    utilities = [sum(F(c['weight']) * F(int(c['actual_bits'][i]), sum(map(int, c['actual_bits'])))
                     for c in hist if c['actual_bits'][i] == '1') for i in range(6)]
    write('visible', {'source': str(proj.relative_to(ROOT)), 'point_sha256': sha(proj),
                      'full_point_sha256': sha(pp), 'O': '1', 'W': str(W), 'K': str(x[0]),
                      'actual_utilities': list(map(str, utilities)), 'histograms': hist})
    out = {'status': 'PASS', 'scope': SCOPE, 'rows': ROW_COUNT, 'columns': COL_COUNT,
           'exact_optimum': str(W), 'parent_complete624_W': str(old_W), 'W_change': str(W - old_W),
           'strict_half_gap_O_minus_2W': str(1 - 2 * W),
           'minimum_primal_slack': str(min(slacks)), 'minimum_column_weight': str(min(x)),
           'minimum_dual_residual': str(min(residual)), 'positive_columns': sum(v > 0 for v in x),
           'positive_multipliers': len(used), 'positive_new_dual_rows': [r for r in certificate['row_multipliers'] if r['row_index'] >= OLD_ROWS],
           'all_39_ZZ_min_bounds_nonnegative': True, 'minimum_ZZ_min_bound': str(min(zz_slacks)),
           'all_81_separate_single_query_bounds_nonnegative': True,
           'minimum_single81_budget': str(min(slacks[i] for i in budgets)),
           'all_new_auxiliaries_canonical': True,
           'matrix_sha256': ARGS.matrix_sha, 'point_sha256': sha(pp), 'dual_sha256': sha(dp),
           'original4849_projection_sha256': sha(proj), 'optimizer_calls': 0,
           'mathematical_float_operations': 0, 'seconds': time.time() - began}
    write('verification', out)
    log('full-exact-certificate-passed', **{k: v for k, v in out.items() if k != 'positive_new_dual_rows'})


def main():
    global ARGS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('preflight', 'solve', 'reconstruct', 'dual', 'verify'))
    parser.add_argument('--matrix', type=Path, default=RUN / 'transport_closure/complete624_single81_v1_matrix.json.gz')
    parser.add_argument('--matrix-sha', required=True)
    parser.add_argument('--review', type=Path)
    parser.add_argument('--label', default='complete624_single81_opt_v1')
    parser.add_argument('--time-limit', type=float, default=240)
    parser.add_argument('--support-tolerance', type=float, default=1e-10)
    parser.add_argument('--active-tolerance', type=float, default=1e-8)
    parser.add_argument('--dependency-tolerance', type=float, default=1e-10)
    parser.add_argument('--dual-support-tolerance', type=float, default=1e-10)
    parser.add_argument('--dual-active-tolerance', type=float, default=1e-12)
    ARGS = parser.parse_args()
    ARGS.matrix = ARGS.matrix.resolve()
    if ARGS.review:
        ARGS.review = ARGS.review.resolve()
    started = time.time(); stamp = datetime.datetime.now(datetime.timezone.utc).isoformat(); success = False
    assert not path('execution_' + ARGS.mode + '.json').exists(), 'Use a new label; existing evidence is immutable'
    try:
        globals()[ARGS.mode]()
        success = True
    finally:
        write('execution_' + ARGS.mode, {'command': [sys.executable, '-B', *sys.argv], 'cwd': str(Path.cwd()),
              'started_utc': stamp, 'elapsed_seconds': time.time() - started, 'success': success,
              'python': platform.python_version(), 'script_sha256': sha(__file__),
              'matrix_path': str(ARGS.matrix), 'matrix_sha256': ARGS.matrix_sha,
              'main_review_path': None if ARGS.review is None else str(ARGS.review),
              'main_review_sha256': None if ARGS.review is None or not ARGS.review.exists() else sha(ARGS.review),
              'frozen_dependencies': {str(p.relative_to(ROOT)): digest for p, digest in
                                      [(PARENT_MATRIX, PARENT_SHA), (EXTENSION, EXTENSION_SHA),
                                       (ZZ_MAP, ZZ_MAP_SHA), (MACRO_MAP, MACRO_MAP_SHA), (ENGINE, ENGINE_SHA)]},
              'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})


if __name__ == '__main__':
    main()
