"""Find and exactly audit a universal two-player fresh-coverage certificate.

All 64 binary incidence patterns are checked. For occupied clients p>=1,
the numerator is affine in p, so its value at p=1 and its slope suffice.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).parent
LABELS = 'ABTSQR'
# Tuple means (chosen action, predecessor, deviation action).
LAST = [('B', 'A', x) for x in LABELS if x != 'B']
LAST += [('Q', 'T', x) for x in LABELS if x != 'Q']
LAST += [('R', 'S', x) for x in LABELS if x != 'R']
SLACKS = [('root_T', None), ('root_S', None)]
SLACKS += [('last_' + ''.join(c), c) for c in LAST]


def utility_numerator(bits, chosen, predecessor, p):
    return bits[chosen] * (p + 2 - bits[predecessor])


def values(bits, p):
    u = lambda a, b: utility_numerator(bits, a, b, p)
    result = [u('A', 'B') - u('T', 'Q'),
              u('A', 'B') - u('S', 'R')]
    result += [u(a, pred) - u(t, pred) for a, pred, t in LAST]
    return result


def target(bits, p, fresh):
    a, b, t, s = (bits[x] for x in 'ABTS')
    if fresh:
        assert p == 0
        return 2 * (2 * (a + b - a * b) - (t + s - t * s))
    return (p + 2) * (a + b) - 2 * a * b


def main():
    rows = []
    rhs = []
    types = []
    for bit_tuple in product((0, 1), repeat=6):
        bits = dict(zip(LABELS, bit_tuple))
        v0, v1, v2 = (values(bits, p) for p in (0, 1, 2))
        rows += [v0, v1, [y - x for x, y in zip(v1, v2)]]
        rhs += [target(bits, 0, True), target(bits, 1, False),
                target(bits, 2, False) - target(bits, 1, False)]
        types += [(bit_tuple, 'fresh'), (bit_tuple, 'occupied_at_1'), (bit_tuple, 'occupied_slope')]
    res = linprog(np.ones(len(SLACKS)), A_ub=np.array(rows), b_ub=np.array(rhs),
                  bounds=(0, None), method='highs')
    if not res.success:
        print(res.message)
        return
    lam = [Fraction(x).limit_denominator(100000) for x in res.x]
    residuals = [Fraction(b) - sum((Fraction(v) * x for v, x in zip(row, lam)), Fraction())
                 for row, b in zip(rows, rhs)]
    assert min(residuals) >= 0
    data = dict(scope='Exact coefficient certificate for P+Delta >= fresh_OPT_2 at every fixed background',
                labels=LABELS, slack_multipliers={name: str(x) for (name, _), x in zip(SLACKS, lam) if x},
                patterns=64, rows=192, min_residual=str(min(residuals)),
                residuals=[dict(bits=b, case=c, value=str(v)) for (b, c), v in zip(types, residuals)])
    (HERE / 'two_player_fresh_certificate.json').write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps({k: v for k, v in data.items() if k != 'residuals'}, indent=2))


if __name__ == '__main__':
    main()
