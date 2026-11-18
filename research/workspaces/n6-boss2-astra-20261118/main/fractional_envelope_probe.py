"""Research probe: six-player fractional-cover proof cone, not SPE search.

Rows are actual-prefix pure-deviation safety, actual-action queries,
the existing weighted terminal-price envelope, and strong PAIR.
All rational coefficients; floating LP only proposes multipliers.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
import sympy as sp

TYPES = list(product(product((0, 1), repeat=6), (0, 1)))
ETAS = tuple(map(F, (0, 1))) + tuple(F(1, j) for j in range(2, 7))
NAMES = ([f'F{i+1}' for i in range(6)]
         + [f'H{i+1}_{j+1}' for i in range(6) for j in range(6)]
         + [f'R{eta}' for eta in ETAS] + ['PAIR'])


def matrix(tau):
    rows, target = [], []
    for e, o in TYPES:
        c = sum(e)
        u = [F(z, c) if c else F(0) for z in e]
        b = [sum(e[:i]) for i in range(6)]
        p, a = b[4], e[4]
        coef = [tau * u[i] - F(o, b[i] + 6-i) for i in range(6)]
        coef += [u[i] - F(e[j], b[i] + 6-i) for i in range(6) for j in range(6)]
        for eta in ETAS:
            theta = min(F(1, p+1), F(1, p+2)+eta/F(p+a+1))
            coef.append(tau*u[4]+eta*u[5]-o*theta)
        coef.append(u[4]+u[5]+F(a, (p+1)*(p+2))
                    - o*(F(2, 1)/(tau*(p+1))-F(1, 1)/(tau*tau*(p+1)*(p+2))))
        rows.append(coef)
        target.append(F(2*(c>0)-o))
    return rows, target


def solve(tau):
    rows, target = matrix(tau)
    result = linprog(np.ones(len(NAMES)), A_ub=np.array(rows, dtype=float),
                     b_ub=np.array(target, dtype=float), bounds=(0, None), method='highs')
    record = {'tau': str(tau), 'status': int(result.status), 'message': result.message}
    if result.success:
        record['multipliers_float'] = {n: float(x) for n, x in zip(NAMES, result.x) if x > 1e-9}
        guess = [F(float(x)).limit_denominator(10**8) if x > 1e-9 else F(0) for x in result.x]
        residual = [t-sum(a*x for a, x in zip(row, guess)) for row, t in zip(rows, target)]
        record['rounded_rational_min_residual'] = str(min(residual))
        record['rounded_rational_verified'] = min(residual) >= 0
        if min(residual) >= 0:
            record['multipliers_exact'] = {n: str(x) for n, x in zip(NAMES, guess) if x}
        support = [i for i, x in enumerate(result.x) if x > 1e-9]
        active = [i for i, (row, t) in enumerate(zip(rows, target))
                  if abs(float(t)-sum(float(a)*x for a, x in zip(row, result.x))) < 1e-7]
        mat = sp.Matrix([[sp.Rational(rows[i][j].numerator, rows[i][j].denominator)
                          for j in support] for i in active])
        pivots = mat.T.rref()[1]
        if len(pivots) == len(support):
            chosen = [active[i] for i in pivots]
            lhs = sp.Matrix([[sp.Rational(rows[i][j].numerator, rows[i][j].denominator)
                              for j in support] for i in chosen])
            rhs = sp.Matrix([sp.Rational(target[i].numerator, target[i].denominator) for i in chosen])
            exact = list(lhs.inv()*rhs)
            candidate = [F(0) for _ in NAMES]
            for j, x in zip(support, exact):
                candidate[j] = F(int(x.p), int(x.q))
            residual = [t-sum(a*x for a,x in zip(row,candidate)) for row,t in zip(rows,target)]
            record['exact_basis_min_residual'] = str(min(residual))
            record['exact_basis_min_multiplier'] = str(min(candidate))
            record['exact_basis_verified'] = min(residual) >= 0 and min(candidate) >= 0
            if record['exact_basis_verified']:
                record['multipliers_exact'] = {n:str(x) for n,x in zip(NAMES,candidate) if x}
                record['exact_residuals'] = [str(x) for x in residual]
    return record


if __name__ == '__main__':
    records = [solve(F(s)) for s in ('9/2', '23/5', '19/4', '5', '21/4', '11/2', '6')]
    out = Path(__file__).with_name('fractional-envelope-probe.json')
    out.write_text(json.dumps({'kind': 'finite-proof-cone-probe', 'types':128,
                              'row_names': NAMES, 'records': records}, indent=2)+'\n')
    for r in records:
        print(r['tau'], r['status'], r.get('rounded_rational_min_residual'))
