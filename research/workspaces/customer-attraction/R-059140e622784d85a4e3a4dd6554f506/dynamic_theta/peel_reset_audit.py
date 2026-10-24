"""Independent unit-client audit of a recursive PEEL reset identity.

This reuses the existing 34-client counterexample, not a new search.  No
normative solver or certificate verifier is imported.  The computation tests
the precise proposed sign R>=0 after re-running the actual last response.
"""

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[5]
raw = json.loads((ROOT / 'examples/customer_attraction/individual_security_failure.json').read_text())
clients = [frozenset(c['topics']) for c in raw['customers'] for _ in range(c['multiplicity'])]
topics = range(6)


def utility(action, history):
    return sum((Q(1, sum(t in c for t in history)) for c in clients if action in c), Q())


def prescribed(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return next(t for t in group if t not in h)


def complete(h):
    while len(h) < 3:
        h += (prescribed(h),)
    return h


checked = 0
minimum = None
for depth in range(3):
    for h in product(topics, repeat=depth):
        z = complete(h)
        chosen = prescribed(h)
        for action in topics:
            alt = complete(h + (action,))
            slack = utility(chosen, z) - utility(action, alt)
            assert slack >= 0
            checked += 1
            minimum = slack if minimum is None else min(minimum, slack)


def U(bg, a, b):
    return sum((Q(1, 1 + int(bg in c) + int(b in c)) for c in clients if a in c), Q())


def F(bg, a):
    return sum((Q(1, 1 + int(bg in c)) for c in clients if a in c), Q())


p = [Q(v, 82) for v in (10, 10, 21, 10, 10, 21)]
values = {name: Q() for name in ('D', 'F', 'C', 'J', 'S', 'Q', 'R', 'L', 'Delta')}
for a, t in product(topics, repeat=2):
    weight = p[a] * p[t]
    ma, ba = complete((a,))[1:]
    mt, bt = complete((t,))[1:]
    cross = prescribed((a, mt))
    s = U(a, ma, ba) - U(a, mt, cross)
    q = U(a, cross, mt) - U(a, bt, mt)
    ell = U(ma, ba, a) - U(ma, bt, a)
    delta = U(ma, a, bt) + F(ma, bt) - U(mt, a, bt) - F(mt, bt)
    assert s >= 0 and q >= 0 and ell >= 0
    values['D'] += weight * U(ma, a, ba)
    values['F'] += weight * U(ma, t, ba)
    extra = sum((Q(1, 1 + int(a in c) + int(ma in c) + int(ba in c))
                 for c in clients if t in c), Q())
    values['C'] += weight * extra
    values['S'] += weight * s
    values['Q'] += weight * q
    values['R'] += weight * (F(a, ba) - F(a, cross))
    values['L'] += weight * ell
    values['Delta'] += weight * delta

values['J'] = values['F'] - values['C']
assert values['J'] >= 0
assert values['D'] - values['F'] == values['L'] + values['Delta']
assert values['D'] - values['F'] == values['S'] + values['Q'] + values['R']
assert values['R'] < 0
report = {
    'claim': 'PEEL is exact; recursively re-running the response creates a signed reset R',
    'fixture': 'examples/customer_attraction/individual_security_failure.json',
    'unit_clients': len(clients),
    'ordered_decision_histories': 43,
    'all_comparisons': checked,
    'minimum_IC_slack': str(minimum),
    'source_distribution': [str(v) for v in p],
    'values': {key: str(v) for key, v in values.items()},
    'D_minus_F': str(values['D'] - values['F']),
    'scope': 'Not a counterexample to Q-CAG-HALF, TB, SM, Mfull or Mpath',
}
out = Path(__file__).with_suffix('.json')
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
