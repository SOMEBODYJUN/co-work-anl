"""Independent exact result verification, Python standard library only.

The constructor, recoverers, optimizer and numerical arrays are not imported.
The previously audited symbolic matrix is rebound by SHA.  Primal values
are independently canonicalized; a Farkas result is recombined in all columns.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(p):
    if str(p).endswith('.gz'):
        with gzip.open(p, 'rt') as f:
            return json.load(f)
    return json.loads(Path(p).read_text())


def main():
    start = time.perf_counter()
    kind = sys.argv[1]
    assert kind in ('primal', 'farkas')
    matrixpath = HERE/'symbolic_matrix_exact.json.gz'
    model = read(matrixpath)
    audit = read(HERE/'symbolic_independent_audit.json')
    assert audit['status'] == 'INDEPENDENT_SYMBOLIC_LITERAL_SORTING_AUDIT_PASS'
    assert audit['matrix_sha256'] == sha(matrixpath)
    pointpath = BASE/model['point_path']
    assert sha(pointpath) == model['point_sha256'] == 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'
    point = read(pointpath)
    assert model['original_columns'] == [{k: v for k, v in c.items() if k != 'weight'} for c in point['columns'][:4849]]
    old = [F(c['weight']) for c in point['columns'][:4849]]
    certpath = HERE/('root_completion_exact.json.gz' if kind == 'primal' else 'farkas_exact.json.gz')
    cert = read(certpath)
    assert cert['point_sha256'] == sha(pointpath) and cert['matrix_sha256'] == sha(matrixpath)
    assert cert['solver_arrays_sha256'] == sha(HERE/'actions_discovery/floating_solver_arrays.npz')
    assert cert['discovery_sha256'] == sha(HERE/'actions_discovery/phase1_discovery.json')
    report = verify_primal(model, cert, old) if kind == 'primal' else verify_farkas(model, cert, old)
    report.update(point_sha256=sha(pointpath), matrix_sha256=sha(matrixpath), certificate_sha256=sha(certpath),
                  verifier_sha256=sha(__file__), symbolic_audit_sha256=sha(HERE/'symbolic_independent_audit.json'),
                  kind=kind, elapsed_seconds=time.perf_counter()-start)
    (HERE/(kind+'_independent_audit.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False))


def verify_primal(model, cert, old):
    assert cert['status'] == 'EXACT_ROOT_SORTING_COMPLETION'
    mu = list(map(F, cert['mu']))
    assert len(mu) == model['mu_column_count'] == 1216 and min(mu) >= 0
    hist = {i: c for i, c in enumerate(model['original_columns']) if c['kind'] == 'hist'}
    groups = [(h, w) for h, c in hist.items() for w, n in enumerate(c['hist']) if n]
    expected = [dict(hist=h, old_word=w, state=s) for h, w in groups for s in range(32)]
    assert expected == model['mu_columns'] and len(groups) == 38 and len(hist) == 16
    lookup = {(m['hist'], m['old_word'], m['state']): j for j, m in enumerate(expected)}
    for h, w in groups:
        assert sum((mu[lookup[h, w, s]] for s in range(32)), F()) == old[h]
    assert sum(old[h] == 0 for h in hist) == 6
    minimum = []
    for d in model['aux_columns']:
        cap = sum((old[col]*F(v) for col, v in d['old_cap']), F())
        y = sum((mu[lookup[d['hist'], d['old_word'], s]] for s in range(32)
                 if format(s, '05b')[d['tail']] == '1'), F())
        minimum.append(min(cap, y))
    assert len(minimum) == 2700 and min(minimum) >= 0
    assert minimum == list(map(F, cert['canonical_min']))
    lower, dual_cases = [], 0
    for d in model['lower_columns']:
        prices = list(map(F, d['prices']))
        masses = [mu[k] for k in d['source_mu']]
        q = sum((old[k]*F(v) for k, v in d['query_old']), F())
        q += sum((mu[k]*F(v) for k, v in d['query_mu']), F())
        assert 0 <= q <= sum(masses) == old[d['hist']]
        left, cost = q, F()
        for s in sorted(range(32), key=lambda s: (prices[s], s)):
            take = min(left, masses[s]); left -= take; cost += take*prices[s]
        assert left == 0
        alternatives = [lam*q-sum((m*max(lam-p, F()) for m, p in zip(masses, prices)), F())
                        for lam in set(prices)]
        assert max(alternatives) == cost
        dual_cases += len(alternatives)
        lower.append(cost)
    assert len(lower) == 9572 and lower == list(map(F, cert['canonical_L']))
    vectors = dict(old=old, mu=mu, aux=minimum, lower=lower)
    slacks, families = [], defaultdict(list)
    for i, row in enumerate(model['rows']):
        value = sum((vectors[kind][j]*F(v) for kind in vectors for j, v in row[kind]), F())
        assert value >= 0, (i, row['name'], value)
        assert value == F(cert['all_row_slacks'][i])
        slacks.append(value)
        if i < 438:
            families[row['name'][0]].append(value)
    assert len(slacks) == len(cert['all_row_slacks']) == 36776
    for i, row in enumerate(model['equalities']):
        value = sum((vectors[kind][j]*F(v) for kind in vectors for j, v in row[kind]), F())
        assert value == F(cert['mass_equalities'][i]) == 0
    assert sum(x > 0 for x in mu) == cert['positive_mu']
    assert sum(v == 0 for v in slacks[:438]) == cert['principal_zero']
    return dict(status='INDEPENDENT_EXACT_ROOT_SORTING_COMPLETION_PASS',
                all_hist=16, zero_hist=6, groups=38, complete_mu_columns=1216,
                positive_mu=sum(x > 0 for x in mu), canonical_min=2700, canonical_L=9572,
                exact_dual_piece_comparisons=dual_cases, principal_rows=438,
                inequalities=36776, mass_equalities=38, principal_zero=sum(v == 0 for v in slacks[:438]),
                family_summary=[dict(family=k, count=len(v), minimum=str(min(v)),
                                     minimum_float=float(min(v)), zero=sum(x == 0 for x in v))
                                for k, v in families.items()],
                scope='Nonseparation by this complete fixed-hist block sorting cone; no joint law and no SPE claim.')


def verify_farkas(model, cert, old):
    assert cert['status'] == 'EXACT_OLD_ONLY_FARKAS'
    nm, na, nl = model['mu_column_count'], model['aux_column_count'], model['lower_column_count']
    offsets = dict(mu=0, aux=nm, lower=nm+na)
    new = [F() for _ in range(nm+na+nl)]
    original = [F() for _ in range(4849)]
    seen, mainsum = set(), F()
    for rowno, rawweight in cert['multipliers']:
        weight = F(rawweight)
        assert weight > 0 and rowno not in seen and 0 <= rowno < len(model['rows'])
        seen.add(rowno)
        if rowno < 438:
            mainsum += weight
        row = model['rows'][rowno]
        for j, v in row['old']:
            original[j] += weight*F(v)
        for kind, offset in offsets.items():
            for j, v in row[kind]:
                new[offset+j] += weight*F(v)
    eta = list(map(F, cert['mass_multipliers']))
    assert len(eta) == len(model['equalities']) == 38
    for weight, row in zip(eta, model['equalities']):
        for j, v in row['old']:
            original[j] += weight*F(v)
        for kind, offset in offsets.items():
            for j, v in row[kind]:
                new[offset+j] += weight*F(v)
    assert mainsum == 1
    residual = list(map(F, cert['nonnegative_variable_multipliers']))
    assert len(residual) == len(new) == 13488 and min(residual) >= 0
    assert all(a+b == 0 for a, b in zip(new, residual))
    row = [[j, str(v)] for j, v in enumerate(original) if v]
    assert row == cert['old_only_row']
    oldvalue = sum((v*x for v, x in zip(original, old)), F())
    assert oldvalue == F(cert['old_value']) and oldvalue < 0
    return dict(status='INDEPENDENT_EXACT_OLD_ONLY_FARKAS_PASS',
                all_inequalities=36776, main_rows=438, mass_equalities=38,
                nonnegative_row_multipliers=len(seen), positive_main_multipliers=sum(i < 438 for i in seen),
                new_columns_exactly_eliminated=13488, old_semantic_columns=4849,
                old_nonzero_coefficients=len(row), old_value=str(oldvalue), old_value_float=float(oldvalue),
                scope='Exact necessary old-only negative row excludes bound cb45 point for this fixed-hist lift; original half question remains open.')


if __name__ == '__main__':
    main()
