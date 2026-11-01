"""Conditional LP: open potential budget, all mixed tuples, true late menu.

Not an SPE search and not a proof of the open potential-budget candidate.
Optimal-label symmetry is exact for the listed rows. Concavity of H implies
the strongest symmetric potential tuple uses each selected optimal label once.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog


def compositions(total, width):
    if width == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, width - 1):
            yield (first,) + rest


def safe(n, d):
    return F(n, d) if n else F(0)


def recover(rows, w, floating):
    support = [k for k, x in enumerate(floating) if x > 1e-8]
    candidates = [(list(map(F, w)), F(1))]
    candidates += [(row, F(0)) for row in rows
                   if abs(sum(float(row[k]) * floating[k] for k in support)) < 1e-7]
    basis = {}
    for row, rhs in candidates:
        reduced = [row[k] for k in support] + [rhs]
        for pivot in sorted(basis):
            coefficient = reduced[pivot]
            if coefficient:
                reduced = [x - coefficient * y for x, y in zip(reduced, basis[pivot])]
        pivot = next((j for j, x in enumerate(reduced[:-1]) if x), None)
        if pivot is not None:
            coefficient = reduced[pivot]
            basis[pivot] = [x / coefficient for x in reduced]
        elif reduced[-1]:
            continue
        if len(basis) == len(support):
            break
    if len(basis) != len(support):
        raise RuntimeError('floating optimum not a recovered vertex')
    values = [F(0)] * len(support)
    for pivot in sorted(basis, reverse=True):
        row = basis[pivot]
        values[pivot] = row[-1] - sum(row[j] * values[j] for j in range(pivot + 1, len(support)))
    full = [F(0)] * len(floating)
    for k, value in zip(support, values):
        full[k] = value
    assert all(x >= 0 for x in full)
    assert sum(F(int(w[k])) * full[k] for k in support) == 1
    residuals = [-sum(row[k] * full[k] for k in support) for row in rows]
    assert min(residuals) >= 0
    return full, min(residuals)


def main():
    types = [(mask, d, ell, overlap) for mask in range(64) for d in range(7)
             for ell, overlap in sorted({(0, 0), (d, d), (6-d, 0), (6, d)})
             if mask or d or ell]
    h = [sum((F(1, j) for j in range(1, i + 1)), F(0)) for i in range(7)]
    records = []
    for mask, d, ell, overlap in types:
        e = [(mask >> j) & 1 for j in range(6)]
        c = sum(e); p = sum(e[:4]); a, b = e[4:]
        u = [safe(ei, c) for ei in e]
        prefix = np.cumsum([0] + e[:-1]).tolist()
        tax = sum((safe(e[j], prefix[j] + 1) - safe(e[j], prefix[j] + 6 - j)
                   for j in range(6)), F(0))
        g = (6 * u[4] + u[5] / 2 - F(d, p + 1) - F(ell, 12 * (p + a + 1))
             + F(d * ell, 6 * (p + 1) * (p + 2)))
        s = 6 * u[4] - F(d, p + 1) + F(overlap, (p+1)*(p+2))
        z = 6 * u[5] - F(ell, p + a + 1)
        v = F(d * ell - 6 * overlap, (p+1)*(p+2))
        assert g == s + z/12 + v/6
        floors = []
        for j in range(5):
            floors.extend(u[j] - safe(e[k], prefix[j] + 6 - j) for k in range(6))
            floors.append(6 * u[j] - F(d, prefix[j] + 6 - j))
            floors.append(6 * u[j] - F(ell, prefix[j] + 6 - j))
        floors.extend(u[5] - F(e[k], p + a + 1) for k in range(6))
        floors.append(6 * u[5] - F(d, p + a + 1))
        denom = (p+1)*(p+2)
        floors.extend(F(ell - 6*e[k], p+1) + F(d*e[k] - overlap, denom) for k in range(6))
        reply_vs_own = F(ell, p+1) - F(overlap, denom) - F(d, p+2)
        reply_vs_all = F(6*(ell-d), p+1) + F(d*d-6*overlap, denom)
        floors.extend((reply_vs_own, reply_vs_all - reply_vs_own))
        records.append((e, int(c > 0), int(d > 0), tax, g, floors, (s,z,v)))
    w = np.array([r[1] for r in records]); o = np.array([r[2] for r in records])
    rows = []; names = []
    for used in range(7):
        k = 6 - used
        for q in compositions(used, 6):
            row = []
            for (mask, d, ell, overlap), (e, wi, oi, tax, g, floors, primitive) in zip(types, records):
                actual_load = sum(x * y for x, y in zip(e, q))
                potential = sum((F(comb(d, j) * comb(6 - d, k - j), comb(6, k))
                                 * h[actual_load + j]
                                 for j in range(max(0, k + d - 6), min(k, d) + 1)), F(0))
                row.append(potential - wi - tax)
            rows.append(row); names.append(('potential', q, k))
    rows.append([-r[4] for r in records]); names.append(('late_G',))
    for k in range(3):
        rows.append([-r[6][k] for r in records]); names.append(('late_SZV', k))
    for j in range(len(records[0][5])):
        rows.append([-r[5][j] for r in records]); names.append(('floor', j))
    # Optional new experiment: exact-catalog private-seat row.  The saved
    # obstruction above deliberately omits this row; use --private to attack
    # the stronger system without replacing its frozen JSON.
    import sys
    private_mode = '--private' in sys.argv
    if private_mode:
        rows.append([F(d,6)+F(5,6)*int(mask==0 and d==1 and ell==0)-wi
                     for (mask,d,ell,overlap),(_,wi,*rest) in zip(types,records)])
        names.append(('exact_catalog_private_seat',))
        for player in range(6):
            rows.append([F(d,6)+F(5,6)*int(mask==0 and d==1 and ell==0)
                         -6*safe((mask>>player)&1,mask.bit_count())
                         for mask,d,ell,overlap in types])
            names.append(('symmetric_private_individual_seat',player))
    matrix = np.array(rows, dtype=float)
    print('types', len(types), 'rows', len(rows), flush=True)
    res = linprog(-o, A_ub=matrix, b_ub=np.zeros(len(rows)), A_eq=w[None, :], b_eq=[1],
                  bounds=(0, None), method='highs')
    result = {'scope': 'conditional necessary-row relaxation only', 'status': res.message}
    if res.success:
        result['value'] = float(-res.fun)
        exact, minimum_residual = recover(rows, w.tolist(), res.x)
        objective = sum(F(int(oi)) * xi for oi, xi in zip(o, exact))
        if not private_mode:
            assert objective > 2
        result['exact_value'] = str(objective)
        result['minimum_residual'] = str(minimum_residual)
        result['positive_types'] = [[list(t), str(x)] for t, x in zip(types, exact) if x]
        result['floating_dual_not_certified'] = [[names[k], str(F(float(-x)).limit_denominator(10**8))]
                          for k, x in enumerate(res.ineqlin.marginals) if abs(x) > 1e-9]
        print('objective', -res.fun, 'support', len(result['positive_types']), flush=True)
    output=Path(__file__).with_name('potential_menu_joint_private.json') if private_mode else Path(__file__).with_suffix('.json')
    output.write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
