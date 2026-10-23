"""One fixed two-player policy diagnostic, not a universal proof.

All 63 nonempty unit-customer incidence types may have nonnegative real
multiplicity. The selected policy has root A and replies B,S,R,S,S,R.
TQ is required to beat every other unordered comparison pair by 1e-6 W.
Only positive results with exact recovery could become counterexamples;
this script does not recover any dual or rational candidate.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import json
import numpy as np
import scipy
from scipy.optimize import linprog

K = 6
A, B, T, Q, R, S = range(K)
REPLIES = (B, S, R, S, S, R)
MASKS = tuple(range(1, 1 << K))
STRICT_OPT_GAP = 1e-6


def utility(mask, action, path):
    return F(1, sum(bool(mask >> z & 1) for z in path)) if mask >> action & 1 else F(0)


def harmonic(n):
    return sum((F(1, j) for j in range(1, n + 1)), F(0))


rows = []
for a in range(K):
    for z in range(K):
        rows.append([utility(mask, REPLIES[a], (a, REPLIES[a])) - utility(mask, z, (a, z)) for mask in MASKS])
for a in range(K):
    rows.append([utility(mask, A, (A, B)) - utility(mask, a, (a, REPLIES[a])) for mask in MASKS])
welfare = [int(bool(mask & (1 << A | 1 << B))) for mask in MASKS]
optimal = [int(bool(mask & (1 << T | 1 << Q))) for mask in MASKS]
optimum_rows = []
for a, b in combinations_with_replacement(range(K), 2):
    if (a, b) != (T, Q):
        optimum_rows.append([int(bool(mask & (1 << a | 1 << b))) - optimal[mask - 1] for mask in MASKS])

results = []
for mode in ('harmonic', 'query'):
    objective = []
    for mask in MASKS:
        c = int(bool(mask >> A & 1)) + int(bool(mask >> B & 1))
        d = int(bool(mask >> T & 1)) + int(bool(mask >> Q & 1))
        outside = int(c > 0 and d == 0)
        fee = harmonic(c + d) - harmonic(c) if mode == 'harmonic' else F(d, c + 1)
        objective.append(fee - int(c > 0) - outside)
    result = linprog(-np.asarray(objective, float),
                     A_ub=np.vstack([-np.asarray(rows, float), np.asarray(optimum_rows, float)]),
                     b_ub=np.r_[np.zeros(len(rows)), np.full(len(optimum_rows), -STRICT_OPT_GAP)],
                     A_eq=np.asarray([welfare], float), b_eq=[1], bounds=(0, None), method='highs')
    results.append({'fee': mode, 'success': bool(result.success),
                    'maximum_fee_minus_W_minus_outside_float': -float(result.fun) if result.success else None,
                    'solver_message': result.message})

report = {'scope': 'One selected complete-policy cone only; no general assertion or exact negative certificate',
          'numpy': np.__version__, 'scipy': scipy.__version__, 'method': 'highs',
          'variables': len(MASKS), 'SPE_rows_including_self': len(rows), 'other_optimum_pairs': len(optimum_rows),
          'normalization_W': 1, 'strict_opt_gap_normalized': STRICT_OPT_GAP,
          'randomness': 'none', 'exact_recovery': 'not attempted; no positive candidate', 'results': results}
path = Path(__file__).resolve().with_name('signed_harmonic_single_policy_probe.json')
path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
