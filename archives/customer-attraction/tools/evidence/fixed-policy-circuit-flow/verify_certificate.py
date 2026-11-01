"""Independent exact semantics and sparse-flow verification; stdlib only.

No import of the author's program, NumPy, SciPy, or an SPE solver.
The unit-customer cube proves identities and dilution validity, while the true
edges are conditional on the explicitly given complete policy being an SPE.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def count(h):
    return tuple(h.count(a) for a in range(6))


states = sorted(q for q in product(range(4), repeat=6) if sum(q) == 3)
vertices = [(q, a) for q in states for a in range(6) if q[a]]
index = {v: i for i, v in enumerate(vertices)}
assert len(states) == 56 and len(vertices) == 126


def row(*terms):
    result = {}
    for coefficient, q, a in terms:
        i = index[q, a]
        result[i] = result.get(i, F(0))+F(coefficient)
    return {i: x for i, x in result.items() if x}


def dot(r, vector):
    return sum((c*vector[i] for i, c in r.items()), F(0))


def policy(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return min(a for a in group if a not in h)


def endpoint(h):
    while len(h) < 3:
        h = h+(policy(h),)
    return count(h)


def total(q):
    return row(*[(q[a], q, a) for a in range(6) if q[a]])


nonnegative, identities = {}, {}
for depth in range(3):
    for h in product(range(6), repeat=depth):
        for b in range(6):
            nonnegative['true_edge', h, b] = row((1, endpoint(h), policy(h)),
                                                (-1, endpoint(h+(b,)), b))
for a in range(6):
    occupied = [q for q in states if q[a]]
    for q in occupied:
        for r in occupied:
            if q == r:
                continue
            kappa = max(F(sum(r[j] for j in range(6) if mask >> j & 1),
                          sum(q[j] for j in range(6) if mask >> j & 1))
                        for mask in range(1, 64) if mask >> a & 1)
            nonnegative['dilution', q, r, a, kappa] = row((kappa, r, a), (-1, q, a))
for a, b in combinations(range(6), 2):
    pa, pb, q, r = count((a, a, a)), count((b, b, b)), count((a, a, b)), count((a, b, b))
    identities['difference_1', a, b] = row((1, r, a), (-1, q, b), (-3, pa, a), (3, pb, b))
    identities['difference_2', a, b] = row((2, q, a), (-2, r, b), (-3, pa, a), (3, pb, b))
    identities['pair_positive', a, b] = row((2, q, a), (2, r, b), (-1, r, a), (-3, pb, b))
for triple in combinations(range(6), 3):
    for c in triple:
        a, b = [x for x in triple if x != c]
        abc, aac, bbc = count(triple), count((a, a, c)), count((b, b, c))
        identities['six_payoff', a, b, c] = row((4, abc, a), (8, bbc, b), (1, bbc, c),
                                               (-4, abc, b), (-8, aac, a), (-1, aac, c))
assert len(nonnegative) == 2778 and len(identities) == 105
root, objective = total(endpoint(())), total(count((1, 2, 4)))

# Complete single-customer incidence domain, including uninterested mask zero.
units = []
for mask in range(64):
    units.append([F(1, sum(q[b] for b in range(6) if mask >> b & 1))
                  if mask >> a & 1 else F(0) for q, a in vertices])
identity_checks = 0
dilution_checks = 0
for r in identities.values():
    for unit in units:
        assert dot(r, unit) == 0
        identity_checks += 1
for key, r in nonnegative.items():
    if key[0] == 'dilution':
        for unit in units:
            assert dot(r, unit) >= 0
            dilution_checks += 1


def coverage_value(values, support):
    support = sorted(support)
    q = [int(a in support) for a in range(6)]
    q[support[0]] += 3-len(support)
    return dot(total(tuple(q)), values)


def verify(path):
    d = json.loads(path.read_text())
    assert d['players'] == 3 and d['topics'] == 6
    assert tuple(d['root']) == endpoint(()) and d['comparison'] == [1, 2, 4]
    beta = F(d['bound'])
    assert beta == F(8, 5)
    y, seen = [F(0)]*126, set()
    for r in d['primal']:
        v = (tuple(r['q']), r['a'])
        assert v in index and v not in seen
        seen.add(v)
        y[index[v]] = F(r['value'])
    assert all(x >= 0 for x in y)
    primal_slacks = [dot(r, y) for r in nonnegative.values()]
    assert min(primal_slacks) >= 0
    assert all(dot(r, y) == 0 for r in identities.values())
    assert dot(root, y) == 1 and dot(objective, y) == beta
    flow = [F(0)]*126
    mu_seen, theta_seen = set(), set()
    for r in d['nonnegative_rows']:
        if r['kind'] == 'true_edge':
            key = ('true_edge', tuple(r['history']), r['deviation'])
        else:
            assert r['kind'] == 'dilution'
            key = ('dilution', tuple(r['q']), tuple(r['r']), r['topic'], F(r['kappa']))
        assert key in nonnegative and key not in mu_seen
        mu_seen.add(key)
        value = F(r['multiplier'])
        assert value >= 0
        for i, c in nonnegative[key].items():
            flow[i] += value*c
    for r in d['circuit_rows']:
        key = (r['kind'], r['a'], r['b'])
        if r['kind'] == 'six_payoff':
            key += (r['background'],)
        assert key in identities and key not in theta_seen
        theta_seen.add(key)
        value = F(r['multiplier'])  # Equality coefficients have either sign.
        for i, c in identities[key].items():
            flow[i] += value*c
    slack_seen = set()
    for r in d['slack']:
        v = (tuple(r['q']), r['a'])
        assert v in index and v not in slack_seen
        slack_seen.add(v)
        value = F(r['coefficient'])
        assert value >= 0
        flow[index[v]] += value
    assert all(beta*root.get(i, 0)-objective.get(i, 0) == flow[i] for i in range(126))
    expected_counts = {'vertices': 126, 'true_edges': 258, 'dilutions': 2520,
                       'pair_circuits': 45, 'six_payoff_circuits': 60,
                       'positive_rows_used': len(mu_seen), 'identities_used': len(theta_seen)}
    assert d['counts'] == expected_counts
    c12, c14, c1, c124 = [coverage_value(y, s) for s in [(1, 2), (1, 4), (1,), (1, 2, 4)]]
    gap = c12+c14-c1-c124
    assert (c12, c14, c1, c124, gap) == (F(8, 9), F(8, 9), F(32, 45), F(8, 5), -F(8, 15))
    return {'file': str(path.relative_to(HERE)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'primal_nonzero_coordinates': len(seen), 'nonnegative_rows': 2778,
            'primal_positive_row_slacks': sum(x > 0 for x in primal_slacks),
            'primal_zero_row_slacks': sum(x == 0 for x in primal_slacks),
            'identities': 105, 'dual_nonnegative_rows_used': len(mu_seen),
            'dual_signed_identities_used': len(theta_seen), 'coordinate_remainders': len(slack_seen),
            'dual_coordinate_equalities': 126, 'root_normalization': '1', 'abstract_optimum': '8/5',
            'coverage_obstruction': {'labels_are_zero_based': True, 'C_12': str(c12),
                                     'C_14': str(c14), 'C_1': str(c1), 'C_124': str(c124),
                                     'submodular_residual': str(gap),
                                     'therefore_nonnegative_common_customer_realization': False}}


original = HERE/'original/circuit_flow_certificate.json'
results = [verify(original)]
replay = HERE/'replay/circuit_flow_certificate.json'
if replay.exists():
    if replay.read_bytes() == original.read_bytes():
        new_binding = {'file': str(replay.relative_to(HERE)), 'byte_equal_to_verified_original': True}
    else:
        results.append(verify(replay))
        new_binding = {'file': str(replay.relative_to(HERE)), 'byte_equal_to_verified_original': False}
else:
    new_binding = None
report = {'status': 'PASS', 'method': 'independent stdlib exact row semantics and sparse primal-dual identity',
          'original_program_imports': 0, 'optimizer_imports_or_calls': 0, 'spe_solver_calls': 0,
          'complete_unit_incidence_patterns': 64, 'unit_identity_checks': identity_checks,
          'unit_dilution_checks': dilution_checks, 'certificates': results, 'current_replay': new_binding,
          'scope': 'fixed three-provider policy, one comparison; abstract optimum, not realizable CAG sharpness'}
(HERE/'exact-certificate-audit.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
