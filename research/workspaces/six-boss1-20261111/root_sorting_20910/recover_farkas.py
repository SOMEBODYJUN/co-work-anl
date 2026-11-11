"""Recover an exact old-only Farkas row from one positive phase-I discovery.

No optimization.  Sparse elimination removes sorting/min multipliers first;
floating activity only proposes equations.  All final signs and all columns
must hold over Fraction before any old-point exclusion can be asserted.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import gzip
import hashlib
import json
import time
import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write(p, obj):
    data = (json.dumps(obj, ensure_ascii=False, separators=(',', ':'))+'\n').encode()
    with open(p, 'wb') as f:
        with gzip.GzipFile(fileobj=f, mode='wb', mtime=0) as g:
            g.write(data)


def main():
    start = time.perf_counter()
    matrixpath = HERE/'symbolic_matrix_exact.json.gz'
    with gzip.open(matrixpath, 'rt') as f:
        raw = json.load(f)
    discovery = HERE/'actions_discovery'
    summary = json.loads((discovery/'phase1_discovery.json').read_text())
    assert summary['success'] and summary['phase'] > 1e-10
    assert summary['matrix_sha256'] == sha(matrixpath)
    arraypath = discovery/'floating_solver_arrays.npz'
    assert sha(arraypath) == summary['solver_arrays_sha256']
    with np.load(arraypath, allow_pickle=False) as data:
        lam_float = -data['inequality_marginals']
        eta_float = data['equality_marginals'].copy()
        primal = data['x'].copy()
        costs = data['lower_bound_marginals'].copy()
    nm, na, nl = raw['mu_column_count'], raw['aux_column_count'], raw['lower_column_count']
    nv = nm+na+nl
    offsets = {'mu': 0, 'aux': nm, 'lower': nm+na}
    support = [i for i, x in enumerate(lam_float) if x > 1e-10]
    # Pivots on one-block piece/cap weights precede shared main weights.
    support.sort(key=lambda i: (0 if i >= 438+5400 else 1 if i >= 438 else 2, i))
    pmap = {i: j for j, i in enumerate(support)}
    neq = len(raw['equalities'])
    unknown = len(support)+neq
    approx = [float(lam_float[i]) for i in support]+list(map(float, eta_float))
    constraints = [defaultdict(F) for _ in range(nv)]
    for i in support:
        for kind, offset in offsets.items():
            for col, val in raw['rows'][i][kind]:
                constraints[offset+col][pmap[i]] += F(val)
    for i, r in enumerate(raw['equalities']):
        for kind, offset in offsets.items():
            for col, val in r[kind]:
                constraints[offset+col][len(support)+i] += F(val)
    basis, selected, rejected = {}, [], []

    def equation(name, coeff, rhs, mandatory=False):
        original = dict(name=name, coefficients=[[k, str(v)] for k, v in sorted(coeff.items()) if v], rhs=str(rhs))
        row = {k: v for k, v in coeff.items() if v}
        rhs = F(rhs)
        while row:
            p = min(row)
            if p not in basis:
                z = row[p]
                basis[p] = ({k: v/z for k, v in row.items()}, rhs/z)
                selected.append(original)
                return
            b, brhs = basis[p]
            z = row[p]
            for k, v in b.items():
                row[k] = row.get(k, F())-z*v
                if not row[k]:
                    del row[k]
            rhs -= z*brhs
        if rhs:
            assert not mandatory, (name, rhs)
            rejected.append(dict(**original, exact_inconsistency=str(rhs)))

    # Fix scale before any possibly overoptimistic floating activity equations.
    equation(['phase-normalization'], {pmap[i]: F(1) for i in support if i < 438}, F(1), True)
    order = list(range(nm+na, nv))+list(range(nm, nm+na))+list(range(nm))
    candidates = 0
    for col in order:
        if primal[col] > 1e-10 or abs(costs[col]) < 2e-9:
            equation(['lifted-zero', col], constraints[col], F())
            candidates += 1
    exact = [F(v).limit_denominator(10**12) for v in approx]
    free = [dict(unknown=j, value=str(exact[j])) for j in range(unknown) if j not in basis]
    for pivot, (row, rhs) in sorted(basis.items(), reverse=True):
        exact[pivot] = rhs-sum((v*exact[k] for k, v in row.items() if k != pivot), F())
    lambdas = [F() for _ in raw['rows']]
    for i in support:
        lambdas[i] = exact[pmap[i]]
    eta = exact[len(support):]
    newcoef = [sum((coef*exact[j] for j, coef in row.items()), F()) for row in constraints]
    oldcoef = defaultdict(F)
    for i in support:
        for col, val in raw['rows'][i]['old']:
            oldcoef[col] += lambdas[i]*F(val)
    for multiplier, row in zip(eta, raw['equalities']):
        for col, val in row['old']:
            oldcoef[col] += multiplier*F(val)
    oldcoef = {k: v for k, v in oldcoef.items() if v}
    pointpath = BASE/raw['point_path']
    assert sha(pointpath) == summary['point_sha256'] == raw['point_sha256']
    point = json.loads(pointpath.read_text())
    weights = [F(c['weight']) for c in point['columns'][:4849]]
    old_value = sum((weights[k]*v for k, v in oldcoef.items()), F())
    attempt = dict(point_sha256=raw['point_sha256'], matrix_sha256=sha(matrixpath),
                   discovery_sha256=sha(discovery/'phase1_discovery.json'), array_sha256=sha(arraypath),
                   recovery_sha256=sha(__file__), support=support, unknowns=unknown,
                   rank=len(basis), free=free, selected_equations=selected,
                   rejected_candidate_equations=rejected, candidate_equations=candidates,
                   lambdas=[[i, str(v)] for i, v in enumerate(lambdas) if v],
                   mass_multipliers=list(map(str, eta)),
                   minimum_lambda=str(min(lambdas)), maximum_lifted_coefficient=str(max(newcoef)),
                   old_value=str(old_value), old_value_float=float(old_value))
    write(HERE/'dual_recovery_attempt.json.gz', attempt)
    assert min(lambdas) >= 0, ('negative multiplier', min(lambdas))
    assert max(newcoef) <= 0, ('uneliminated positive lifted coefficient', max(newcoef))
    assert sum(lambdas[:438]) == 1
    assert old_value < 0, ('no negative old-only row', old_value)
    cert = dict(status='EXACT_OLD_ONLY_FARKAS', scope='Necessary row on original 4849 coordinates for fixed hist identities; excludes only the bound point.',
                point_sha256=raw['point_sha256'], matrix_sha256=sha(matrixpath),
                discovery_sha256=sha(discovery/'phase1_discovery.json'), solver_arrays_sha256=sha(arraypath),
                recovery_sha256=sha(__file__),
                multipliers=[[i, str(v)] for i, v in enumerate(lambdas) if v],
                mass_multipliers=list(map(str, eta)),
                nonnegative_variable_multipliers=[str(-v) for v in newcoef],
                old_only_row=[[i, str(v)] for i, v in sorted(oldcoef.items())],
                old_value=str(old_value), old_value_float=float(old_value),
                positive_main_multipliers=sum(v > 0 for v in lambdas[:438]),
                positive_multipliers=sum(v > 0 for v in lambdas),
                lifted_columns_eliminated=nv, old_semantic_columns=4849,
                elapsed_seconds=time.perf_counter()-start, no_global_half_claim=True)
    write(HERE/'farkas_exact.json.gz', cert)
    print(json.dumps({k: v for k, v in cert.items() if k not in
          ('multipliers', 'mass_multipliers', 'nonnegative_variable_multipliers', 'old_only_row')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
