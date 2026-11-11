"""Exact primal face recovery from the sole Actions discovery, no optimization.

Only positive floating mu support is used to identify a candidate face.
Candidate active faces are proposals, not asserted mathematical facts.
Every eventual certificate must independently pass exact canonical checks.
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
    if str(p).endswith('.gz'):
        with open(p, 'wb') as f:
            with gzip.GzipFile(fileobj=f, mode='wb', mtime=0) as g:
                g.write(data)
    else:
        Path(p).write_bytes(data)


def nz(d):
    return {k: v for k, v in d.items() if v}


def main():
    start = time.perf_counter()
    path = HERE/'symbolic_matrix_exact.json.gz'
    with gzip.open(path, 'rt') as f:
        raw = json.load(f)
    discovery = HERE/'actions_discovery'
    summary = json.loads((discovery/'phase1_discovery.json').read_text())
    assert summary['matrix_sha256'] == sha(path) and summary['success']
    assert abs(summary['phase']) < 1e-8
    pointpath = BASE/raw['point_path']
    assert sha(pointpath) == raw['point_sha256'] == summary['point_sha256']
    point = json.loads(pointpath.read_text())
    old = [F(c['weight']) for c in point['columns'][:4849]]
    arraypath = discovery/'floating_solver_arrays.npz'
    assert sha(arraypath) == summary['solver_arrays_sha256']
    with np.load(arraypath, allow_pickle=False) as arrays:
        approx = arrays['mu'].copy()
    support = [j for j, x in enumerate(approx) if x > 1e-10]
    pos = {j: i for i, j in enumerate(support)}
    lookup = {(r['hist'], r['old_word'], r['state']): j for j, r in enumerate(raw['mu_columns'])}
    approx_support = [float(approx[j]) for j in support]

    # Expressions are constant plus a sparse linear function of positive mu.
    def expression(old_terms=(), mu_terms=()):
        const = sum((old[j]*F(v) for j, v in old_terms), F())
        coeff = defaultdict(F)
        for j, v in mu_terms:
            if j in pos:
                coeff[pos[j]] += F(v)
        return const, nz(coeff)

    def value(expr):
        c, a = expr
        return float(c)+sum(float(v)*approx_support[j] for j, v in a.items())

    def difference(a, b):
        d = defaultdict(F, a[1])
        for j, v in b[1].items():
            d[j] -= v
        return a[0]-b[0], nz(d)

    min_expr, min_boundaries = [], []
    for j, d in enumerate(raw['aux_columns']):
        cap = expression(old_terms=d['old_cap'])
        y = expression(mu_terms=[(lookup[d['hist'], d['old_word'], s], '1')
                     for s in range(32) if ((s >> (4-d['tail'])) & 1)])
        min_expr.append(cap if value(cap) <= value(y) else y)
        if abs(value(cap)-value(y)) < 2e-9:
            min_boundaries.append((['min-boundary', j], difference(cap, y)))
    lower_expr, lower_boundaries = [], []
    for j, d in enumerate(raw['lower_columns']):
        qexpr = expression(d['query_old'], d['query_mu'])
        choices = []
        for lam in map(F, d['lambdas']):
            const, coeff = qexpr[0]*lam, defaultdict(F, {k: v*lam for k, v in qexpr[1].items()})
            for col, price in zip(d['source_mu'], map(F, d['prices'])):
                if col in pos and price < lam:
                    coeff[pos[col]] -= lam-price
            choices.append((lam, (const, nz(coeff))))
        best_lam, best = max(choices, key=lambda p: value(p[1]))
        lower_expr.append(best)
        for lam, candidate in choices:
            if lam != best_lam and abs(value(candidate)-value(best)) < 2e-9:
                lower_boundaries.append((['sorting-boundary', j, str(best_lam), str(lam)], difference(best, candidate)))

    def expand(r):
        const, terms = expression(r['old'], r['mu'])
        terms = defaultdict(F, terms)
        for kind, exprs in (('aux', min_expr), ('lower', lower_expr)):
            for j, v in r[kind]:
                v = F(v); const += v*exprs[j][0]
                for k, coef in exprs[j][1].items():
                    terms[k] += v*coef
        return const, nz(terms)

    equations = []
    for r in raw['equalities']:
        equations.append((r['name'], expand(r), True))
    for i, r in enumerate(raw['rows'][:438]):
        expr = expand(r)
        if abs(value(expr)) < 2e-9:
            equations.append((['principal', i, r['name']], expr, False))
    equations += [(name, expr, False) for name, expr in min_boundaries+lower_boundaries]
    basis, selected, rejected, seen = {}, [], [], set()
    for name, (const, coeff), mandatory in equations:
        row = dict(coeff)
        rhs = -const
        signature = (tuple(sorted(row.items())), rhs)
        if signature in seen:
            continue
        seen.add(signature)
        original = dict(name=name, coefficients=[[k, str(v)] for k, v in sorted(row.items())], rhs=str(rhs))
        for pivot, (b, brhs) in sorted(basis.items()):
            scale = row.get(pivot, F())
            if not scale:
                continue
            for k, v in b.items():
                row[k] = row.get(k, F())-scale*v
                if not row[k]:
                    del row[k]
            rhs -= scale*brhs
        if not row:
            if rhs:
                assert not mandatory, (name, rhs)
                rejected.append(dict(**original, exact_inconsistency=str(rhs)))
            continue
        pivot = min(row); scale = row[pivot]
        basis[pivot] = ({k: v/scale for k, v in row.items()}, rhs/scale)
        selected.append(original)
    exact = [F(x).limit_denominator(10**12) for x in approx_support]
    free = [dict(mu_column=support[j], local_column=j, mass=str(exact[j]))
            for j in range(len(support)) if j not in basis]
    for pivot, (row, rhs) in sorted(basis.items(), reverse=True):
        exact[pivot] = rhs-sum((v*exact[k] for k, v in row.items() if k != pivot), F())
    mu = [F() for _ in raw['mu_columns']]
    for j, x in zip(support, exact):
        mu[j] = x
    attempt = dict(point_sha256=raw['point_sha256'], matrix_sha256=sha(path),
                   discovery_sha256=sha(discovery/'phase1_discovery.json'),
                   array_sha256=sha(arraypath), recovery_sha256=sha(__file__),
                   support=support, candidate_equations=len(equations), unique_equations=len(seen),
                   selected_equations=selected, rejected_nonmandatory_candidates=rejected,
                   rank=len(basis), free=free, recovered_mu=list(map(str, mu)),
                   exact_nonnegativity=min(mu) >= 0)
    write(HERE/'primal_recovery_attempt.json.gz', attempt)
    assert min(mu) >= 0, ('negative recovered mu', min(mu))
    minimum = []
    for d in raw['aux_columns']:
        cap = sum((old[j]*F(v) for j, v in d['old_cap']), F())
        y = sum((mu[lookup[d['hist'], d['old_word'], s]] for s in range(32)
                 if (s >> (4-d['tail'])) & 1), F())
        minimum.append(min(cap, y))
    lowers = []
    for d in raw['lower_columns']:
        q = sum((old[j]*F(v) for j, v in d['query_old']), F())
        q += sum((mu[j]*F(v) for j, v in d['query_mu']), F())
        prices = list(map(F, d['prices']))
        masses = [mu[j] for j in d['source_mu']]
        assert 0 <= q <= sum(masses), ('invalid query mass', d, q, sum(masses))
        left, cost = q, F()
        for s in sorted(range(32), key=lambda s: (prices[s], s)):
            take = min(left, masses[s]); left -= take; cost += take*prices[s]
        assert left == 0
        lowers.append(cost)
    assert min(minimum) >= 0 and min(lowers) >= 0
    vectors = dict(old=old, mu=mu, aux=minimum, lower=lowers)
    slacks, negatives = [], []
    for i, r in enumerate(raw['rows']):
        val = sum((vectors[k][j]*F(v) for k in vectors for j, v in r[k]), F())
        slacks.append(str(val))
        if val < 0:
            negatives.append(dict(row=i, name=r['name'], value=str(val), float=float(val)))
    equality = []
    for r in raw['equalities']:
        equality.append(sum((vectors[k][j]*F(v) for k in vectors for j, v in r[k]), F()))
    check = dict(negative_rows=negatives, nonzero_equalities=[str(v) for v in equality if v],
                 smallest_slack=str(min(map(F, slacks))), elapsed_seconds=time.perf_counter()-start)
    write(HERE/'primal_recovery_check.json', check)
    assert not negatives and all(v == 0 for v in equality), check
    result = dict(status='EXACT_ROOT_SORTING_COMPLETION', point_sha256=raw['point_sha256'],
                  matrix_sha256=sha(path), discovery_sha256=sha(discovery/'phase1_discovery.json'),
                  solver_arrays_sha256=sha(arraypath), recovery_sha256=sha(__file__),
                  mu=list(map(str, mu)), canonical_min=list(map(str, minimum)),
                  canonical_L=list(map(str, lowers)), all_row_slacks=slacks,
                  mass_equalities=list(map(str, equality)), positive_mu=sum(x > 0 for x in mu),
                  principal_rows=438, principal_zero=sum(F(x) == 0 for x in slacks[:438]),
                  root_source_slack=slacks[next(i for i, r in enumerate(raw['rows']) if r['name'] == ['root-source'])],
                  complete_groups=38, complete_mu_columns=1216, all_hist=16,
                  scope='Necessary complete block sorting envelope; not a common customer law or SPE.',
                  elapsed_seconds=time.perf_counter()-start)
    write(HERE/'root_completion_exact.json.gz', result)
    print(json.dumps({k: v for k, v in result.items() if k not in
          ('mu', 'canonical_min', 'canonical_L', 'all_row_slacks', 'mass_equalities')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
