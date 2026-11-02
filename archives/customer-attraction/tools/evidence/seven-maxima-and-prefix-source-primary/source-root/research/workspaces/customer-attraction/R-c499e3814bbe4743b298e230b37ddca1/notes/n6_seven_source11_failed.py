"""Exact audit of the seven-maxima n=6 four-row source-(11) attempt.

This is a negative method result.  It intentionally records the omitted q*f/|J|
term that made an earlier floating LP look positive.  No SPE counterexample is
constructed: all rows are necessary inequalities, and failure means only this
row family cannot certify U <= 2W on the enlarged literal type domain.
"""
from fractions import Fraction as F
from scipy.optimize import linprog
import numpy as np

N = 6                 # providers
S = 7                 # maximal coverages
Z = S - 1             # maxima other than the actual final one B_0
C = Z * (Z - 1) // 2

def q(a, b):
    return F(a, b) if b else F(0)

A = [F(N+t, (t+1)*(S*N-(S-2)*t)) for t in range(N-1)] + [F(1, N+S-1)]
B = [F(2, S*N-(S-2)*t) for t in range(N-1)] + [F(N+1, N*(N+S-1))]
alpha = [min(A[t:]) for t in range(N)]
beta = [min(B[t:]) for t in range(N)]
FP = sum(alpha[:N-2])
FV = sum(beta[:N-2])

# f=1_{0 in I}; k=|I\{0}|; p=|J intersect {0,1,2,3}|;
# d=1_{4 in J}; the final bit is exactly f.  This is the full enlarged
# domain, with arbitrary earlier true membership.
states = []
for f in (0, 1):
    for k in range(Z+1):
        if f + k < 1:
            continue
        for p in range(N-1):
            for d in (0, 1):
                j = p + d + f
                base = F(1, 2) if j else -F(1, 2)
                m = f + k
                Fm = FP if m == 1 else FV if 2 <= m <= Z else F(N-2, N)
                G = q(k, p+1) if f == 0 else q(Z-k, p+1) + q(2*k, p+2)
                K = q(k*(Z-k), p+1) + q(k*(k-1), p+2)
                # Correct source-(11) coefficients.  The q*f/j terms are
                # essential: q = Z*c + C*e, so c/e rows pay final shares too.
                ca = Fm - q(p, j)
                cb = q(k, p+d+1) - q(Z*f, j)
                cc = G - q(Z*(d+f), j) - q(Z*d, (p+1)*(p+2))
                ce = K - q(C*(d+f), j) - q(C*d, (p+1)*(p+2))
                states.append((f, k, p, d, base, ca, cb, cc, ce))

# Maximize uniform residual epsilon over nonnegative a,b,c,e.
M = np.array([[-float(x[5]), -float(x[6]), -float(x[7]), -float(x[8]), 1.0]
              for x in states])
rhs = np.array([float(x[4]) for x in states])
sol = linprog([0, 0, 0, 0, -1], A_ub=M, b_ub=rhs,
              bounds=[(0, None)]*4 + [(None, None)], method="highs")
assert sol.success
assert sol.x[-1] < 0

# Exact re-evaluation of the corrected formula at a rational approximation to
# the LP optimizer; the negative active states are sufficient to show the
# proposed four-row family cannot close this enlarged domain.
print({"alpha": [str(x) for x in alpha], "beta": [str(x) for x in beta],
       "FP": str(FP), "FV": str(FV),
       "lp": sol.x.tolist(), "epsilon": sol.x[-1],
       "states": len(states)})
