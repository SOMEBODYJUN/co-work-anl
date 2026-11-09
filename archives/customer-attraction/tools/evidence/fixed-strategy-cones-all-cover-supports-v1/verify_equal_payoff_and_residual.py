"""Verify the equal-payoff rows and two exact optima of the common-IC relaxation."""

import argparse
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path


CERTIFICATE_DIR = Path(
    'archives/customer-attraction/tools/evidence/fixed-strategy-cones-all-cover-supports-v1'
)
REVERSE_ROWS = {
    'clients48': (74, 237),
    'clients252': (67, 71, 116, 188, 206, 688),
}
DUAL_NUMERATORS = {
    51: 130, 53: 50, 55: 130, 58: 65, 61: 105, 65: 130, 68: 65,
    155: 130, 156: 65, 158: 25, 164: 40, 165: 50, 169: 130, 170: 80,
    171: 180, 175: 105, 188: 40, 590: 358, 592: 90, 593: 50, 598: 130,
}
ATTAINING_CLIENTS = {
    4: 14, 6: 3, 7: 30, 8: 14, 9: 18, 10: 9, 16: 12, 17: 12,
    18: 9, 19: 10, 32: 11, 33: 18, 34: 12, 60: 3, 64: 23, 66: 3, 117: 6,
}
UNEQUAL_CLIENTS = {1: 9, 2: 11, 4: 3, 8: 3, 16: 3, 32: 3, 64: 3, 125: 10}


def verify(repo):
    folder = repo / CERTIFICATE_DIR
    spec = importlib.util.spec_from_file_location('fixed_cones', folder / 'verify_certificates.py')
    fixed_cones = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixed_cones)
    certificate = json.loads((folder / 'certificates.json').read_text())
    fixed_cones.verify(repo, certificate)
    policies = {name: fixed_cones.load_endpoint(repo, name) for name in REVERSE_ROWS}
    dot = fixed_cones.dot
    masks = fixed_cones.TYPES
    w = fixed_cones.coverage_row((0, 1))
    u0 = tuple(F(1, 3 + 2 * bool(mask & 2)) if mask & 1 else F(0) for mask in masks)
    u1 = tuple(F(1, 2 + 3 * bool(mask & 1)) if mask & 2 else F(0) for mask in masks)
    assert all(3 * x + 2 * y == z for x, y, z in zip(u0, u1, w))
    g = tuple(60 * (x - y) for x, y in zip(u0, u1))
    for name, indices in REVERSE_ROWS.items():
        policy = policies[name]
        assert policy['by_deviation'][((), 1)] == g
        rows = policy['rows']
        assert tuple(sum(rows[j][k] for j in indices) for k in range(len(masks))) == tuple(-x for x in g)

    shared = sorted(set(policies['clients48']['rows']) & set(policies['clients252']['rows']))
    assert len(shared) == 1753
    portfolio = (2, 3, 4, 5, 6)
    v = fixed_cones.coverage_row(portfolio)
    c = tuple(x - y - 5 * z for x, y, z in zip(v, w, u1))
    coverage_dual = next(proof for proof in certificate['suites']['shared'] if tuple(proof['J']) == portfolio)
    assert fixed_cones.check_dual(shared, w, v, coverage_dual) == F(207, 130)
    residual_dual = {'beta': F(-53, 130), 'mu': [(j, F(n, 65)) for j, n in DUAL_NUMERATORS.items()]}
    assert fixed_cones.check_dual(shared, w, c, residual_dual) == F(-53, 130)
    slack = tuple(F(-53, 130) * w[k] - sum(F(n, 3900) * shared[j][k] for j, n in DUAL_NUMERATORS.items()) - c[k]
                  for k in range(len(masks)))
    assert min(slack) == 0

    attaining = tuple(ATTAINING_CLIENTS.get(mask, 0) for mask in masks)
    assert min(dot(row, attaining) for row in shared) == 0
    assert (dot(w, attaining), dot(v, attaining), dot(u1, attaining), dot(c, attaining)) == (130, 207, 26, -53)
    assert all(min(dot(row, attaining) for row in policy['rows']) == -90 for policy in policies.values())
    assert F(207, 130) > F(63, 40) and F(-53, 130) > F(-17, 40)
    unequal = tuple(UNEQUAL_CLIENTS.get(mask, 0) for mask in masks)
    assert min(dot(row, unequal) for row in shared) >= 0
    assert dot(w, unequal) == 30 and dot(u1, unequal) == F(11, 2)
    print('Verified the 127-column equal-payoff row identities and both strict common-IC optima.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', type=Path, help='repository root with both frozen policies and the coverage certificates')
    verify(parser.parse_args().repository)
