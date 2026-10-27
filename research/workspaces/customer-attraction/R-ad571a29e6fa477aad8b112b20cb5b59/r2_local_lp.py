from fractions import Fraction
import itertools
import numpy as np
from scipy.optimize import linprog

m, r_exc = 6, 2
rows = []
for a, b, p, e, d, ell, h in itertools.product(
        [0, 1], [0, 1], range(m - 1), range(r_exc + 1),
        range(m + 1), range(m + 1), range(m + 1)):
    if e > p or h > min(d, ell) or h < max(0, d + ell - m):
        continue
    o, w = int(d > 0), int(p + a + b > 0)
    D, den = (p + 1) * (p + 2), p + a + b
    alpha = Fraction(a, den) if den else Fraction(0)
    beta = Fraction(b, den) if den else Fraction(0)
    S = m * alpha - Fraction(d, p + 1) + Fraction(h, D)
    Z = m * beta - Fraction(ell, p + a + 1)
    V = Fraction(d * ell - m * h, D)
    K = (Fraction(e, den) if den else Fraction(0)) - Fraction(r_exc * a, m)
    K += ((Fraction(r_exc * b, den) if den else Fraction(0))
          - Fraction(e, p + a + 1)) / (m - 1)
    H_E = (Fraction(e, den) if den else Fraction(0)) - Fraction(r_exc * a, m)
    H_N = (Fraction(p - e, den) if den else Fraction(0)) - Fraction((m - 2 - r_exc) * a, m)
    rows.append((Fraction(2 * w - o), m * S + V, Z, K, H_E, H_N,
                 (a, b, p, e, d, ell, h)))

A = [[float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5])] for r in rows]
b = [float(r[0]) for r in rows]
result = linprog([0.0] * 5, A_ub=np.asarray(A), b_ub=np.asarray(b),
                 bounds=[(0, None)] * 5, method="highs")
print({"states": len(rows), "status": result.status,
       "message": result.message, "x": None if not result.success else result.x.tolist()})
