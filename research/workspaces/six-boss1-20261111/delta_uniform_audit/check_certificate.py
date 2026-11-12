#!/usr/bin/env python3
"""Second literal checker.  Does not import the audit or any producer."""
from pathlib import Path
from fractions import Fraction
from itertools import product
import hashlib
import json

Q = Fraction
HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def load(path):
    return json.loads(path.read_text())


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


input_path = BASE / 'visible_maximum_joint_v5/exact_input.json'
data = load(input_path)
old = load(BASE / 'visible_maximum_joint_v5_solve/exact_certificate.json')
assert len(data['raw_rows']) == 3056 and len(data['atom_columns']) == 512
rows = data['raw_rows']
original_weights = [Q(z) for z in old['dual']['raw_row_weights']]
old_res = [Q(z) for z in old['dual']['nonnegative_column_residual']]
alpha = Q(old['objective'])
lam0, lamr = original_weights[2606], original_weights[868]
eps = Q(1, 144)
root_eta = Q(1087978231314917, 84387869309613600)
S0 = Q(1528993, 497664)
free_c = Q(old['dual']['equality_multipliers'][1]) - lam0 * S0
tau = [Q(0), Q(5929, 6912), Q(65, 72)]
betas = [Q(59881, 497664), Q(20035, 20736), Q(71, 72)]
S = 1 + sum(betas)
statefile = load(HERE / 'all256_true_delta_state_checks.json')
state_count = 0
for bank, s in zip(statefile, [Q(0), Q(61273, 6912)]):
    a = 25 + sum(tau) - s
    for rec in bank['states']:
        p, c, o = rec['pco']
        costs = {}
        for tail in product([0, 1], repeat=4):
            r3, r4, r5, r6 = tail
            L = p + c + sum(tail)
            part = (a*c-r6-tau[0]*r3-tau[1]*r4-tau[2]*r5) / L if L else Q(0)
            value = part + betas[0]*r3+betas[1]*r4+betas[2]*r5+r6
            value += Q(o, 6*(p+c+r3+r4+r5+1))
            value += tau[0]*Q(o, 6*(p+c+4))
            value += tau[1]*Q(o, 6*(p+c+r3+3))
            value += tau[2]*Q(o, 6*(p+c+r3+r4+2))
            costs[tail] = value
            state_count += 1
        m = min(costs.values())
        assert m == Q(rec['minimum'])
        assert [list(t) for t,v in costs.items() if v == m] == rec['all_weak_tails']
        for z in rec['all_costs']:
            assert costs[tuple(z['tail'])] == Q(z['cost'])
            assert Q(z['residual_to_minimum']) == Q(z['cost']) - m >= 0
assert state_count == 256

reports = []
for denominator in [72, 36]:
    cert_path = HERE / f'certificate_gamma{denominator}.json'
    cert = load(cert_path)
    assert cert['base_input_sha256'] == hash_file(input_path)
    weights = [Q(v) for v in cert['all3056_payments_before_normalization']]
    nweights = [Q(v) for v in cert['all3056_payments_normalized']]
    residual = [Q(v) for v in cert['all513_residuals_before_normalization']]
    nresidual = [Q(v) for v in cert['all513_residuals_normalized']]
    gamma = lam0 * eps / denominator
    assert Q(cert['gamma']) == gamma and Q(cert['normalization_divisor']) == 1 + gamma
    assert Q(cert['alpha_new']) == (alpha+gamma)/(1+gamma) > alpha
    assert len(weights) == len(nweights) == 3056
    assert len(residual) == len(nresidual) == 513
    assert min(weights) >= 0 and min(residual) >= 0
    assert weights == [v + (gamma if 869 <= i <= 874 else 0) for i,v in enumerate(original_weights)]
    assert nweights == [v/(1+gamma) for v in weights]
    assert nresidual == [v/(1+gamma) for v in residual]
    assert Q(cert['free_EC_weight_before_normalization']) == free_c
    assert Q(cert['free_EC_weight_normalized']) == free_c/(1+gamma)
    assert [i for i,r in enumerate(rows) if Q(r['rhs']) == -1] == cert['all30_rhs_minus_one_rows_retained']
    assert all(weights[i] == 0 for i in cert['all30_rhs_minus_one_rows_retained'])
    overrides = cert['row_coefficient_overrides']
    assert set(overrides) == {'868', '2606'}
    for j in range(513):
        if j < 512:
            t = data['atom_columns'][j]
            aa, o, c = t['a'], t['o'], t['c']
            p = aa[0]
            w = Q(bool(sum(aa)))
            ec = Q(c)
            u2 = Q(aa[1], sum(aa)) if sum(aa) else Q(0)
            analytic_delta = (25+sum(tau))*u2-Q(24*c,p+5)-Q(o,6*(p+4*c+1))
            analytic_delta -= sum(tau[k]*Q(o,6*(p+(k+1)*c+4-k)) for k in range(3))
            analytic_delta += Q(p*c*(1-o),180)
            analytic_root = Q(rows[868]['a'].get(str(j),'0'))-root_eta*c*(1-o)
            tc = c*(sum(Q(1,sum(aa[:i])+6-i) for i in range(6))-1)
            expected_res = old_res[j]+(lamr*root_eta+gamma)*c*(1-o)-lam0*Q(p*c*(1-o),180)+gamma*tc
            expected_res += lam0*eps*Q((1-p)*o*(1-c),72) if denominator==72 else -lam0*eps*Q(p*o*(1-c),72)
        else:
            w,o,ec = Q(0),Q(0),Q(-1)
            analytic_delta = Q(0)
            analytic_root = Q(rows[868]['a'].get(str(j),'0'))
            expected_res = old_res[j]
        assert Q(overrides['2606']['coefficients'].get(str(j),'0')) == analytic_delta
        assert Q(overrides['868']['coefficients'].get(str(j),'0')) == analytic_root
        assert residual[j] == expected_res >= 0
        aggregate = free_c*ec+residual[j]
        naggregate = free_c*ec/(1+gamma)+nresidual[j]
        for i in range(3056):
            if weights[i] == 0:
                continue
            ri = overrides.get(str(i))
            coeff = Q((ri['coefficients'] if ri else rows[i]['a']).get(str(j),'0'))
            rhs = Q(ri['rhs'] if ri else rows[i]['rhs'])
            homogeneous = coeff-rhs*o
            aggregate += weights[i]*homogeneous
            naggregate += nweights[i]*homogeneous
        assert aggregate == (1+gamma)*w-(alpha+gamma)*o
        assert naggregate == w-Q(cert['alpha_new'])*o
    reports.append({'denominator':denominator, 'certificate_sha256':hash_file(cert_path),
                    'all513_unnormalized_columns': 'PASS',
                    'all513_normalized_columns': 'PASS',
                    'all3056_payments': 'PASS', 'all30_affine_rows': 'PASS'})

pins = load(HERE / 'source_pins_and_immutability.json')['source_pins']
assert all(hash_file(BASE/rel) == value for rel,value in pins.items())
result = {'status':'PASS_SECOND_LITERAL_CHECK_NO_PRODUCER_IMPORTS',
          'agent_id':'/root/delta_uniform_audit', 'optimizer_calls':0,
          'source256_true_states_and_all_ties':'PASS', 'certificates':reports,
          'all_pinned_sources_unchanged':True}
(HERE/'second_literal_check_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
