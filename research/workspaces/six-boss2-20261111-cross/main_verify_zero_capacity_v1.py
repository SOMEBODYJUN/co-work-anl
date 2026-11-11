"""Independent audit of the zero-K closed forms and shared R^C/Z^C bridge.

Rebuilds L from frozen alpha/beta through Main's earlier feature identities and
four-policy Bellman values. No discovering evaluator is imported.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json, time
from main_zero_capacity_features_v1 import L, PARAMS, SCALES

B = Path(__file__).resolve().parent
C = B / 'coverage_bridge'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
base_path = C / 'mainline_zero_capacity_v1.json'
ic_path = C / 'zero_capacity_ic_bridge_v1.json'
shared_path = C / 'shared_rz_zero_capacity_v1.json'
base, ic, shared = (json.loads(p.read_text()) for p in (base_path, ic_path, shared_path))
assert sha(shared_path) == '2bd7138c2d35c19100c7d12bde244d2d37695b4609fbbf51260b1574c4b64f34'
started = time.time()
tables = {2: base['cut2_complete_visible_table'], 13: base['cut13_complete_visible_table']}
counts, lambdas = {}, {}
for number, entries in tables.items():
    values_seen = []
    for row in entries:
        p, D, a6, n = row['p'], row['d'], row['A6'], row['n']
        if number == 2:
            x, y, ci, bj = row['x'], row['y'], row['Ci'], row['Bj']
        else:
            x, y, ci, bj = min(1, row['r']), max(0, row['r'] - 1), 0, 0
        vals = tuple(L(number, p, D, t, x, y, ci, bj, a6, n) for t in (0, 1))
        assert vals == tuple(map(F, row['L']))
        tau = F(n - x - y, 4)
        for t in (0, 1):
            baseline = L(number, p, D, t, 0, 0, 0, 0, 0, 0)
            if number == 2:
                bound = baseline + (41*x + 145*ci + 40*bj + 2*a6 + 13*tau)/(p+t+2) + (11*(x+y)+47*tau)/(p+3)
            else:
                bound = baseline + F(2162*a6, p+t+2) + F(581*n+3*(x+y), 4*(p+3))
            assert vals[t] >= bound
        delta = vals[1] - vals[0]
        assert delta > 0
        if number == 2:
            values_seen.append(delta * (p+x+bj+1))
        else:
            values_seen += [delta*(p+a4+1) for a4 in (0, 1) if 0 <= D-1-p-a4 <= 1]
    counts[number] = 2*len(entries)
    lambdas[number] = min(values_seen)
assert counts == {2: 3840, 13: 720}
assert lambdas[2] == F(ic['lambda2']) == F(447, 2)
assert lambdas[13] == F(ic['lambda13']) == F(3593, 2)
for rec in base['baselines']:
    number = rec['cut']
    for row in rec['entries']:
        vals = [L(number, row['p'], row['d'], t, 0, 0, 0, 0, 0, 0) for t in (0, 1)]
        assert vals == [F(row['base0']), F(row['base1'])]
        assert vals[1] - vals[0] == F(row['seed_increment'])


def orbit13(p, D, a6, n):
    ts = [int(i < n) for i in range(6)]
    return sum(L(13, p, D, 0, ts[i], ts[j], 0, 0, a6, n) for i in range(6) for j in range(6) if i != j) / 30


def enhanced(number, p, D, a4, a6, n):
    if number == 13:
        return orbit13(p, D, a6, n) + lambdas[13]*F(n, 6*(p+a4+2))
    ts = [int(i < n) for i in range(6)]
    total = F(0)
    for j in range(6):
        total += min(sum(L(2, p, D, 0, ts[i], ts[j], 0, bj, a6, n)
                         + lambdas[2]*F(n, 6*(p+ts[i]+bj+1)) for i in range(6) if i != j)
                     for bj in (0, 1))
    return total / 30


for number in (2, 13):
    missing = [enhanced(number, 0, 1, 0, 0, n) for n in range(1, 7)]
    credit = min(missing)
    tax = max(credit*int(n > 0)-enhanced(number, p, p+a4+a5+1, a4, a6, n)
              for p in range(4) for a4, a5, a6 in product((0, 1), repeat=3)
              for n in range(7) if p+a4+a5+a6 > 0)
    target = ic['enhanced_coverage'][str(number)]
    assert missing == list(map(F, target['miss_credits']))
    assert (credit, tax) == (F(target['A']), F(target['B']))
    obstruct = ic['two_signature_obstruction'][str(number)]
    assert enhanced(number, 0, 1, 0, 0, 1) == F(obstruct['after_ic_required_half_multiplier_upper'])
    assert SCALES[number] - enhanced(number, 0, 2, 1, 0, 1) == F(obstruct['after_ic_required_half_multiplier_lower'])

lam, minimum_R, minimum_Z, max_ratio = F(17965), None, None, F(0)
assert len(shared['four_state_type_table']) == 2560
for row in shared['four_state_type_table']:
    p, D, a4, a5, a6 = (row[k] for k in ('p', 'D', 'A4', 'A5', 'A6'))
    x, y, ci, cj, n = (row[k] for k in ('Ti', 'Tj', 'Ci', 'Cj', 'n'))
    assert D == p+a4+a5+1 and 0 <= n-x-y <= 4
    P, q = p+a4, F(n, 6)
    av = tuple(L(2, p, D, t, x, y, ci, cj, a6, n) for t in (0, 1))
    bv = tuple(L(13, p, D, t, x, y, 0, 0, a6, n) for t in (0, 1))
    assert av == tuple(map(F, row['A_values'])) and bv == tuple(map(F, row['B_values']))
    rm = 49*(av[1]-av[0])-lam*q/((P+1)*(P+2))
    zm = 10*(bv[1]-bv[0])-lam/(P+1)
    assert rm == F(row['R_margin']) >= 0 and zm == F(row['Z_margin']) >= 0
    minimum_R = rm if minimum_R is None else min(minimum_R, rm)
    minimum_Z = zm if minimum_Z is None else min(minimum_Z, zm)
    max_ratio = max(max_ratio, F(3593, 2)*q/((P+1)*(P+2)*(av[1]-av[0])))
    joint = min(49*av[r]+10*bv[z]+lam*(q-z)/(P+r+1) for r, z in product((0, 1), repeat=2))
    separate = 49*min(av)+min(10*bv[z]+lam*(q-z)/(P+r+1) for r, z in product((0, 1), repeat=2))
    assert joint == F(row['joint_four_state_min']) == 49*av[0]+10*bv[0]+lam*q/(P+1)
    assert separate == F(row['separate_min']) == 49*av[0]+10*bv[0]+lam*q/(P+2)
    assert joint-separate == F(row['exact_shared_R_gain']) == lam*q/((P+1)*(P+2))
assert (minimum_R, minimum_Z, max_ratio) == (F(5, 6), F(0), F(10779, 2200))

full_credits = []
assert len(shared['A6_credit_type_table']) == 960
for row in shared['A6_credit_type_table']:
    p, D, x, y, ci, cj, n = (row[k] for k in ('p', 'D', 'Ti', 'Tj', 'Ci', 'Cj', 'n'))
    av = [L(2, p, D, 0, x, y, ci, cj, a6, n) for a6 in (0, 1)]
    bv = [L(13, p, D, 0, x, y, 0, 0, a6, n) for a6 in (0, 1)]
    assert av == [F(row['A0_without_A6']), F(row['A0_with_A6'])]
    assert bv == [F(row['B0_without_A6']), F(row['B0_with_A6'])]
    assert av[1]-av[0] >= F(2, p+2) and bv[1]-bv[0] >= F(2162, p+2)
    gain = 49*(av[1]-av[0])+10*(bv[1]-bv[0])
    assert gain == F(row['weighted_increment']) and D*gain == F(row['increment_times_D'])
    full_credits.append(D*gain)
assert min(full_credits) == F(shared['observed_full_type_last_credit_minimum']) == 21669

baseline_nets = []
for row in shared['actual_baselines']:
    p, D, a4, a5, a6 = (row[k] for k in ('p', 'D', 'A4', 'A5', 'A6'))
    raw = 49*L(2, p, D, 0, 0, 0, 0, 0, 0, 0)+10*L(13, p, D, 0, 0, 0, 0, 0, 0, 0)
    overlap = F(10859*a6*(p+2*a4+2*a5), D*(p+2))
    assert F(21718*a6, p+2) == F(10859*a6, D)+overlap
    assert (raw, overlap, raw+overlap) == tuple(F(row[k]) for k in ('raw', 'last_overlap_credit', 'net'))
    if a6:
        assert raw+overlap >= 0
    baseline_nets.append(raw+overlap)
assert len(baseline_nets) == 32

common_C = {}
for row in shared['conditional_common_C_count_table']:
    p, D, n, Cnum = (row[k] for k in ('p', 'D', 'n', 'Cnum'))
    candidates = []
    for both in range(max(0, Cnum-(6-n)), min(n, Cnum)+1):
        bucket_counts = [6-n-Cnum+both, Cnum-both, n-both, both]
        assert min(bucket_counts) >= 0 and sum(bucket_counts) == 6
        words = tuple(v for v, count in zip(product((0, 1), repeat=2), bucket_counts) for _ in range(count))
        avg = sum(49*L(2, p, D, 0, words[i][0], words[j][0], words[i][1], words[j][1], 0, n)
                  +10*L(13, p, D, 0, words[i][0], words[j][0], 0, 0, 0, n)
                  for i in range(6) for j in range(6) if i != j)/30
        candidates.append((avg, both))
    val = min(v for v, both in candidates)
    assert val == F(row['base'])
    assert [both for v, both in candidates if v == val] == row['min_T_and_C_overlap_counts']
    common_C[p, D, n, Cnum] = val
assert len(common_C) == 588
for (p, D, n, Cnum), val in common_C.items():
    assert val >= common_C[p, D, n, 0]+F(9065*Cnum, 6*(p+2))


def final_cost(mode, p, a4, a5, a6, n):
    D, P = p+a4+a5+1, p+a4
    shift = 1 if mode == 'joint' else 2
    return common_C[p, D, n, 0]+lam*F(n, 6*(P+shift))+F(10859*a6*(p+2*a4+2*a5), D*(p+2))


for mode in ('joint', 'separate_same_weights'):
    rec = shared['coverage_contracts'][mode]
    uncovered = [final_cost(mode, 0, 0, 0, 0, n) for n in range(1, 7)]
    A = min(uncovered)
    covered = [(A*int(n > 0)-final_cost(mode, p, a4, a5, a6, n), (p, a4, a5, a6, n))
               for p in range(4) for a4, a5, a6 in product((0, 1), repeat=3)
               for n in range(7) if p+a4+a5+a6 > 0]
    tax = max(v for v, sig in covered)
    assert uncovered == list(map(F, rec['uncovered_by_opt_multiplicity']))
    assert A == F(rec['OPT_credit']) and tax == F(rec['W_tax'])
    assert 2*A-tax == F(rec['two_OPT_credit_minus_W_tax'])
    obstruct = shared['remaining_two_signature_obstruction'][mode]
    assert final_cost(mode, 0, 0, 0, 0, 1) == F(obstruct['half_multiplier_upper_at_U'])
    assert 148951-final_cost(mode, 0, 1, 0, 0, 1) == F(obstruct['half_multiplier_lower_at_C'])

assert F(10779, 2200) <= F(49, 10) <= F(4236, 859)
report = {'status': 'PASS', 'frozen_parameter_sha256': base['frozen_package_sha256'],
          'base_table_sha256': sha(base_path), 'terminal_bridge_sha256': sha(ic_path),
          'shared_RZ_sha256': sha(shared_path), 'L2_complete_values_checked': counts[2],
          'L13_complete_values_checked': counts[13], 'lambdas': {str(k): str(v) for k, v in lambdas.items()},
          'four_state_cases': 2560, 'minimum_R_margin': str(minimum_R), 'minimum_Z_margin': str(minimum_Z),
          'max_required_weight_ratio': str(max_ratio), 'shared_gain': '17965*n/[6*(P+1)*(P+2)]',
          'A6_increment_cases': 960, 'full_increment_minimum_times_D': '21669',
          'used_cash_shift': '10859*u6', 'budget': '148951*u4 + 9532*u6',
          'actual_baseline_cases': 32, 'all_A6_one_net_baselines_nonnegative': True,
          'common_T_C_count_cases': 588, 'all_reported_coverage_and_obstruction_constants_verified': True,
          'scope': 'Exact finite complete local-type proof of universal fixed-coefficient necessary contracts and same-weight shared-R gain; neither a half-coverage proof nor an SPE counterexample.',
          'seconds': time.time()-started, 'verifier_sha256': sha(Path(__file__))}
Path(__file__).with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
