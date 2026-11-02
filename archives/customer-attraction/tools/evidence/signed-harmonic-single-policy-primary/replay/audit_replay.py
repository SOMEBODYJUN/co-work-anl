"""Replay unchanged primary bytes and independently check the generated LP rows.

This audit checks finite row semantics and one exact seed. It does not recover
an LP dual, prove an exact optimum, or enumerate other complete policies.
"""
from contextlib import redirect_stdout, redirect_stderr
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import io
import json
import platform
import runpy
import shutil
import time

import numpy as np
import scipy
import scipy.optimize

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parent / 'original'
NAME = 'signed_harmonic_single_policy_probe.py'
shutil.copyfile(ORIGINAL / NAME, HERE / NAME)
source_bytes = (ORIGINAL / NAME).read_bytes()
assert (HERE / NAME).read_bytes() == source_bytes
captured = []
original_linprog = scipy.optimize.linprog

def recording_linprog(c, **kwargs):
    result = original_linprog(c, **kwargs)
    captured.append((np.array(c), kwargs, result))
    return result

stdout, stderr = io.StringIO(), io.StringIO()
start = time.monotonic()
scipy.optimize.linprog = recording_linprog
try:
    with redirect_stdout(stdout), redirect_stderr(stderr):
        data = runpy.run_path(str(HERE / NAME), run_name='__main__')
finally:
    scipy.optimize.linprog = original_linprog
    (HERE / 'stdout.txt').write_text(stdout.getvalue())
    (HERE / 'stderr.txt').write_text(stderr.getvalue())
seconds = time.monotonic() - start

# Independently use customer membership sets rather than bit arithmetic.
types = [frozenset(t for t in range(6) if n & (1 << t)) for n in range(1, 64)]
reply = [1, 5, 4, 5, 5, 4]
def share(S, player_action, other_action):
    if player_action not in S:
        return F(0)
    return F(1, 1 + (other_action in S))
def union_hit(S, a, b):
    return int(a in S or b in S)
def H(n):
    return sum((F(1, r) for r in range(1, n + 1)), F(0))

ic = []
for first in range(6):
    for deviation in range(6):
        ic.append([share(S, reply[first], first) - share(S, deviation, first) for S in types])
for deviation in range(6):
    ic.append([share(S, 0, 1) - share(S, deviation, reply[deviation]) for S in types])
welfare = [union_hit(S, 0, 1) for S in types]
other_pairs = [p for p in combinations_with_replacement(range(6), 2) if p != (2, 3)]
optimality = [[union_hit(S, a, b) - union_hit(S, 2, 3) for S in types] for a, b in other_pairs]
objectives = {}
for mode in ('harmonic', 'query'):
    coefficients = []
    for S in types:
        c = int(0 in S) + int(1 in S)
        d = int(2 in S) + int(3 in S)
        fee = H(c + d) - H(c) if mode == 'harmonic' else F(d, c + 1)
        coefficients.append(fee - int(c > 0) - int(c > 0 and d == 0))
    objectives[mode] = coefficients
assert data['rows'] == ic
assert data['welfare'] == welfare
assert data['optimum_rows'] == optimality
assert len(captured) == 2
matrix = np.vstack([-np.asarray(ic, float), np.asarray(optimality, float)])
for mode, (objective, args, result) in zip(('harmonic', 'query'), captured):
    assert np.array_equal(objective, -np.asarray(objectives[mode], float))
    assert np.array_equal(args['A_ub'], matrix)
    assert np.array_equal(args['A_eq'], np.asarray([welfare], float))
    assert np.array_equal(args['b_ub'], np.r_[np.zeros(42), np.full(20, -1e-6)])
    assert np.array_equal(args['b_eq'], np.array([1]))
    assert args['bounds'] == (0, None) and args['method'] == 'highs'
    assert result.success

# The k=3, 12-incidence-type, 71-unit-customer seed is a sanity check,
# not the optimizer returned by either LP.
seed_types = {'A':10, 'ARS':6, 'B':13, 'BRS':4, 'BTRS':1, 'BQRS':1,
              'T':8, 'TR':5, 'TS':5, 'Q':8, 'QR':5, 'QS':5}
letters = 'ABTQRS'
seed = {frozenset(letters.index(t) for t in S): n for S, n in seed_types.items()}
z = [seed.get(S, 0) for S in types]
def dot(row):
    return sum((x * n for x, n in zip(row, z)), F(0))
seed_welfare = dot(welfare)
seed_ic = [dot(row) for row in ic]
seed_gaps = [-dot(row) for row in optimality]
assert sum(z) == 71 and seed_welfare == 35
assert min(seed_ic) == 0 and min(seed_gaps) == 1
assert all(dot(objectives[mode]) == -31 for mode in objectives)

old = json.loads((ORIGINAL / 'signed_harmonic_single_policy_probe.json').read_text())
new = json.loads((HERE / 'signed_harmonic_single_policy_probe.json').read_text())
assert old == new
results = []
for mode, (objective, args, result) in zip(('harmonic', 'query'), captured):
    results.append({
        'fee': mode,
        'maximum_float': -float(result.fun),
        'minimum_x_float': float(np.min(result.x)),
        'max_Aub_x_minus_bub_float': float(np.max(args['A_ub'] @ result.x - args['b_ub'])),
        'max_abs_Aeq_x_minus_beq_float': float(np.max(np.abs(args['A_eq'] @ result.x - args['b_eq']))),
        'negative_result_exact_certificate': False,
    })
record = {
    'event': 'one unchanged primary replay; two floating LP calls',
    'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__,
    'source_sha256': hashlib.sha256(source_bytes).hexdigest(),
    'elapsed_seconds': seconds,
    'independent_exact_coefficient_audit': {'variables':63, 'SPE_rows_including_self':42,
        'SPE_zero_rows': sum(all(x == 0 for x in row) for row in ic),
        'other_optimum_pairs':20, 'all_matrices_objectives_and_constraints_match':True},
    'exact_seed_check': {'customers':71, 'welfare':str(seed_welfare),
        'minimum_SPE_slack':str(min(seed_ic)), 'minimum_TQ_optimality_gap':str(min(seed_gaps)),
        'both_fee_minus_W_minus_outside': '-31',
        'both_normalized_fee_minus_W_minus_outside': '-31/35'},
    'original_report_equal_fields': old == new,
    'original_report_equal_bytes': (ORIGINAL / 'signed_harmonic_single_policy_probe.json').read_bytes() == (HERE / 'signed_harmonic_single_policy_probe.json').read_bytes(),
    'results':results,
    'limits': ['no rational primal or dual recovery', 'no exact negative certificate',
        'one selected two-player complete policy only', 'strict TQ gap omits ties and smaller relative gaps'],
}
(HERE / 'execution-and-row-audit.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
