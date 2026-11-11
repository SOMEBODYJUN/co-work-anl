"""Exact recovery of a full-state marginal witness, then canonical minima.

The active piece of each upper envelope is used only to find rational mu.
The resulting auxiliaries are recomputed as exact min(q,y), and every saved
symbolic row is checked over Fraction.  This imports no discovery code.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def bit(s, k):
    return (s >> (4-k)) & 1


def solve_affine(equations, nv, approximate):
    """Exact row-echelon basis; rational nearby values for any free variables."""
    basis, chosen = {}, []
    for name, coeff, rhs in equations:
        a = list(coeff)+[rhs]
        for p, b in sorted(basis.items()):
            if a[p]:
                factor = a[p]
                for k in range(p, nv+1):
                    a[k] -= factor*b[k]
        pivot = next((k for k in range(nv) if a[k]), None)
        if pivot is None:
            if a[-1]:
                raise ValueError(('inconsistent purported active face', name, str(a[-1])))
            continue
        p = a[pivot]
        a = [v/p for v in a]
        basis[pivot] = a
        chosen.append(name)
    x = [F(v).limit_denominator(10**12) for v in approximate]
    for p, a in sorted(basis.items(), reverse=True):
        x[p] = a[-1]-sum((a[k]*x[k] for k in range(p+1, nv)), F())
    assert all(sum((a*xj for a, xj in zip(coeff, x)), F()) == rhs for _, coeff, rhs in equations)
    return x, chosen, nv-len(basis)


def main():
    start = time.perf_counter()
    symbolic = HERE/'symbolic_coefficients_exact.json'
    raw = json.loads(symbolic.read_text())
    disc = json.loads((HERE/'phase1_discovery.json').read_text())
    assert disc['symbolic_sha256'] == sha(symbolic) and disc['success'] and disc['phase'] < 1e-10
    old = [F(c['weight']) for c in raw['original_columns']]
    nm = raw['mu_column_count']
    support = [j for j, v in enumerate(disc['mu']) if v > 1e-9]
    pos = {j: k for k, j in enumerate(support)}
    lookup = {(m['hist'], m['old_word'], m['state']): j for j, m in enumerate(raw['mu_columns'])}
    cap, ycols, chosen_old = [], [], []
    for a in raw['aux_columns']:
        cap.append(sum((old[j]*F(v) for j, v in a['old_cap']), F()))
        cols = [lookup[a['hist'], a['old_word'], s] for s in range(32) if bit(s, a['tail'])]
        ycols.append(cols)
        yy = sum(disc['mu'][j] for j in cols)
        chosen_old.append(float(cap[-1]) <= yy)

    def equation(r):
        coeff = [F() for _ in support]
        const = sum((old[j]*F(v) for j, v in r['old']), F())
        for j, v in r['mu']:
            if j in pos:
                coeff[pos[j]] += F(v)
        for j, v in r['aux']:
            v = F(v)
            if chosen_old[j]:
                const += v*cap[j]
            else:
                for k in ycols[j]:
                    if k in pos:
                        coeff[pos[k]] += v
        return coeff, -const

    equations = []
    for r in raw['equalities']:
        coeff, rhs = equation(r)
        equations.append((r['name'], coeff, rhs))
    canonical_float = [min(float(c), sum(disc['mu'][j] for j in cc)) for c, cc in zip(cap, ycols)]
    for i, r in enumerate(raw['rows'][:raw['principal_row_count']]):
        value = sum(float(F(v))*float(old[j]) for j, v in r['old'])
        value += sum(float(F(v))*disc['mu'][j] for j, v in r['mu'])
        value += sum(float(F(v))*canonical_float[j] for j, v in r['aux'])
        if abs(value) < 2e-9:
            coeff, rhs = equation(r)
            equations.append((['principal', i, r['name']], coeff, rhs))
    seen = set()
    for j, (c, cols) in enumerate(zip(cap, ycols)):
        key = (c, tuple(k for k in cols if k in pos))
        yy = sum(disc['mu'][k] for k in cols)
        if key in seen or abs(yy-float(c)) >= 2e-9:
            continue
        seen.add(key)
        coeff = [F(int(k in cols)) for k in support]
        equations.append((['min-boundary', j], coeff, c))
    weights, active, free = solve_affine(equations, len(support), [disc['mu'][j] for j in support])
    mu = [F() for _ in range(nm)]
    for j, w in zip(support, weights):
        assert w > 0, (j, w)
        mu[j] = w
    canonical = [min(c, sum((mu[j] for j in cols), F())) for c, cols in zip(cap, ycols)]
    assert all(v >= 0 for v in canonical)
    checks = []
    for r in raw['rows']:
        value = sum((old[j]*F(v) for j, v in r['old']), F())
        value += sum((mu[j]*F(v) for j, v in r['mu']), F())
        value += sum((canonical[j]*F(v) for j, v in r['aux']), F())
        assert value >= 0, (r['name'], str(value), float(value))
        checks.append(dict(row=r['name'], slack=str(value), float=float(value)))
    for r in raw['equalities']:
        value = sum((old[j]*F(v) for j, v in r['old']), F())+sum((mu[j]*F(v) for j, v in r['mu']), F())
        assert value == 0, r['name']
    mainrows = checks[:raw['principal_row_count']]
    root = next(r for r in mainrows if r['row'] == ['root-source'])
    out = dict(scope='Complete-32-state single-root marginal lift feasibility, with canonical min upper envelopes; not a common R/Z/root law or SPE.',
               point_sha256=raw['point_sha256'], symbolic_sha256=sha(symbolic),
               discovery_sha256=sha(HERE/'phase1_discovery.json'), recovery_sha256=sha(__file__),
               principal_rows=raw['principal_row_count'], complete_mu_columns=nm,
               root_word_groups=len(raw['root_groups']), all_rows=len(raw['rows']),
               min_auxiliaries=len(canonical), positive_mu=len(support),
               mu=[str(v) for v in mu], canonical_min=[str(v) for v in canonical],
               positive_states=[dict(column=j, **raw['mu_columns'][j], mass=str(mu[j])) for j in support],
               active_equations=active, exact_face_equations=len(equations), free_variables=free,
               root_source_slack=root['slack'], root_source_slack_float=root['float'],
               principal_slacks=mainrows, all_slacks=checks,
               principal_zero=sum(F(r['slack']) == 0 for r in mainrows),
               elapsed_seconds=time.perf_counter()-start,
               omitted=raw['omitted'], no_SPE_claim=True, no_complete_239_dominance_claim=True)
    (HERE/'marginal_completion_exact.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ('mu', 'canonical_min', 'positive_states', 'active_equations', 'principal_slacks', 'all_slacks')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
