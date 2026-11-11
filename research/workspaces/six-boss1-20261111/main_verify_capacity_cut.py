"""Independent literal four-follower check of one cross-branch capacity cut.

This reconstructs its customer cost directly from five sorts of true IC/price
rows. It does not import a row generator, an LP, or stored cut coefficients.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from hashlib import sha256
import json
import sys


def share(num, den):
    return F(num, den) if num else F()


def minimum(p, ell, t, q):
    values = []
    for follower in product((0, 1), repeat=4):
        middle, last = sum(follower[:3]), follower[3]
        den = p + t + sum(follower)
        # Source IC, actual-last prices, last-topic capacity, branch-last IC.
        cost = share(t, den) - share(last, den) / 16
        cost += F(3 * middle + last, 64 * (ell + 1)) + F(3 * last, 64)
        cost += F(q, 16 * (p + t + middle + 1))
        values.append(cost)
    return min(values)


def audit(point):
    raw = Path(point).read_bytes()
    data = json.loads(raw)
    cols = data['columns']
    vals = [F(col['weight']) for col in cols]
    assert cols[0]['kind'] == 'K'
    left = F(3, 64) * vals[0]
    for j, col in enumerate(cols):
        if col['kind'] != 'hist':
            continue
        a = tuple(map(int, col['actual_bits']))
        left += vals[j] * (share(a[1], sum(a)) + F(10, 64) * share(a[5], sum(a)))
    right = F()
    by_hist = {}
    cache = {}
    for j, col in enumerate(cols):
        if col['kind'] != 'maximum-root-family-state':
            continue
        hj = col['hist_column']
        a = tuple(map(int, cols[hj]['actual_bits']))
        # H_4 is the zero-based final follower in (M,H_0,...,H_4).
        key = (a[0], sum(a[:5]), col['hidden'][-1], a[5])
        if key not in cache:
            cache[key] = minimum(*key)
        contribution = vals[j] * cache[key]
        right += contribution
        by_hist[hj] = by_hist.get(hj, F()) + contribution
    return {
        'input': str(point), 'input_sha256': sha256(raw).hexdigest(),
        'source': 2, 'target': 'maximum-root H_4', 'query': 'A_6',
        'left': str(left), 'right': str(right), 'slack': str(left - right),
        'slack_float': float(left - right), 'negative': left < right,
        'left_budget': 'u_2 + (10/64) u_6 + (3/64) K',
        'literal_follower_states_per_visible_type': 16,
        'visible_types_checked': len(cache),
        'right_by_hist': {str(k): str(v) for k, v in sorted(by_hist.items())},
        'scope': 'one valid necessary cut at the exact supplied point; no SPE claim',
    }


if __name__ == '__main__':
    result = audit(sys.argv[1])
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
