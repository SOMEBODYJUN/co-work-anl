#!/usr/bin/env python3
"""Independent exact verification of Main's reweighted four-parameter extension.

Main proposed alpha=25+sum(theta)-s and s in [0,9].  This file verifies that
proposal from literal true shares, not by importing any Main or prior code.
No optimizer or numerical package is used.  The current1003 input stays read-only.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import lcm
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
PINS = {
    'visible_maximum_joint_v2/exact_input.json':
        '0d80f56ac0b1f82350ae5e307370d9860b21382c7059b688904230a3b80f20a4',
    'visible_maximum_joint_v2_solve/exact_certificate.json':
        'b9c1d5339b21823b5f448f8c8242bf8b1394b181c099c2bf7d87c68d3f227aea',
    'visible_maximum_joint_v2_solve/freeze_manifest.json':
        '110e6b873a0d7d61f552b8c2c97a28a1dc571a7b130137a5926a36496f6713ce',
    'visible_maximum_joint_v2_solve/optimal_face.json':
        'dc15708a840f0c28e89e006d5dc115cc7a089600f7030c4ec337e32f1eafb9ca',
    'visible_maximum_joint/exact_input.json':
        'b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33',
    'main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json':
        'a852e9f8c16fa8fd8a2785034d220de1b90193036d1d4ceb9d0fe431481cd4ba',
}
for name, digest in PINS.items():
    assert sha256((WS / name).read_bytes()).hexdigest() == digest, name


def read(name):
    return json.loads((WS / name).read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def share(bit, prefix, following=0):
    return F(1, prefix + 1 + following) if bit else F(0)


def cost(p, c, menu, tail, theta, s):
    alpha = 25 + sum(theta) - s
    value = alpha * share(c, p, sum(tail)) + F(sum(tail[:3]), 2) + tail[3]
    value -= share(tail[3], p + c + sum(tail[:3]))
    value += sum((share(q, p + c + sum(tail[:3])) for q in menu), F(0)) / 6
    for k, (source, weight) in enumerate(zip((3, 4, 5), theta)):
        actual = share(tail[k], p + c + sum(tail[:k]), sum(tail[k + 1:]))
        query = sum((share(q, p + c + sum(tail[:k]), 6 - source) for q in menu), F(0)) / 6
        value += weight * (query - actual)
    return value


def minimum(p, c, o, theta, s):
    answer = F(5, 2) * c + F(24 * c, p + 5) + F(o, 6 * (p + 4 * c + 1)) - s * c / 5
    return answer + sum((t * F(o, 6 * (p + (j - 2) * c + 7 - j))
                         for j, t in zip((3, 4, 5), theta)), F(0))


parameter_data = json.loads((HERE / 'parameter_polytope.json').read_text())
vertices3 = {name: tuple(map(F, values)) for name, values in parameter_data['vertices'].items()}
assert len(vertices3) == 8
vertices4 = {name + '_S' + str(s): (theta, F(s)) for name, theta in vertices3.items() for s in (0, 9)}
assert len(vertices4) == 16
hidden, minima = [], []
for name, (theta, s) in vertices4.items():
    assert all(t >= 0 for t in theta) and 25 + sum(theta) - s >= 16
    for p, c, o in product((0, 1), repeat=3):
        target = minimum(p, c, o, theta, s)
        actual = {}
        for tail in product((0, 1), repeat=4):
            value = cost(p, c, (o, 0, 0, 0, 0, 0), tail, theta, s)
            assert value >= target
            actual[tail] = value
            hidden.append({'vertex': name, 'p': p, 'c': c, 'o': o, 'tail': list(tail),
                           'cost': str(value), 'minimum': str(target), 'residual': str(value - target)})
        common = (0, 0, 0, 0) if not c else (1, 1, 1, 1 - p)
        assert actual[common] == min(actual.values()) == target
        minima.append({'vertex': name, 'p': p, 'c': c, 'o': o, 'minimum': str(target),
                       'zero_states': [list(t) for t, value in actual.items() if value == target]})
assert len(hidden) == 2048 and len(minima) == 128

# Verify exact necessary boundary expressions as affine forms in four params.
# Values at zero and all four coordinate unit points determine each form.
unit_params = [((F(0), F(0), F(0)), F(0))]
unit_params += [(tuple(F(k == j) for k in range(3)), F(0)) for j in range(3)]
unit_params += [((F(0), F(0), F(0)), F(1))]
necessity = []
for label, p, c, o, tail, expected in [
    ('theta5_cap', 0, 0, 1, (0, 0, 1, 0), [F(5,12), F(0), F(0), F(-1), F(0)]),
    ('theta4_cap', 0, 0, 1, (0, 1, 0, 0), [F(5,12), F(0), F(-1), -F(1,36), F(0)]),
    ('theta3_cap', 0, 0, 1, (1, 0, 0, 0), [F(5,12), F(-1), -F(1,72), -F(1,36), F(0)]),
    ('s_lower', 1, 1, 0, (1, 1, 1, 1), [F(0), F(0), F(0), F(0), F(1,30)]),
    ('s_upper', 0, 1, 0, (1, 1, 1, 0), [F(9,20), F(0), F(0), F(0), -F(1,20)]),
]:
    vals = [cost(p, c, (o, 0, 0, 0, 0, 0), tail, theta, s)
            - minimum(p, c, o, theta, s) for theta, s in unit_params]
    coeff = [vals[0]] + [v - vals[0] for v in vals[1:]]
    assert coeff == expected
    necessity.append({'boundary': label, 'p': p, 'c': c, 'o': o, 'tail': list(tail),
                      'constant_theta3_theta4_theta5_s': list(map(str, coeff))})

# Generic menu weakening is independent of alpha; verify all real menus at
# all sixteen endpoints, retaining one common six-label menu for all queries.
menu_checks = 0
for name, (theta, s) in vertices4.items():
    for p, c in product((0, 1), repeat=2):
        for menu in product((0, 1), repeat=6):
            d, o = sum(menu), int(any(menu))
            for tail in product((0, 1), repeat=4):
                real = cost(p, c, menu, tail, theta, s)
                weak = cost(p, c, (o, 0, 0, 0, 0, 0), tail, theta, s)
                gap = F(d - o, 6) * (F(1, p + c + sum(tail[:3]) + 1)
                       + sum((t * F(1, p + c + sum(tail[:k]) + 7 - j)
                              for k, (j, t) in enumerate(zip((3,4,5), theta))), F(0)))
                assert real - weak == gap >= 0
                menu_checks += 1
assert menu_checks == 65536

inp = read('visible_maximum_joint_v2/exact_input.json')
cert = read('visible_maximum_joint_v2_solve/exact_certificate.json')
old = read('visible_maximum_joint/exact_input.json')
assert len(inp['raw_rows']) == 1003 and inp['raw_rows'][:1002] == old['raw_rows']
assert inp['atom_columns'] == old['atom_columns'] and inp['equalities'] == old['equalities']
assert inp['objective'] == old['objective'] and inp['K_column'] == 512
assert cert['input_sha256'] == PINS['visible_maximum_joint_v2/exact_input.json']


def vec(a):
    return [F(a.get(str(j), '0')) for j in range(513)]


U, B, M, N3, N4, N5, CS = ([F(0)] * 513 for _ in range(7))
Ns = [N3, N4, N5]
for j, atom in enumerate(inp['atom_columns']):
    aa, p, c, o = atom['a'], atom['a'][0], atom['c'], atom['o']
    U[j] = share(aa[1], p, sum(aa[2:]))
    B[j], M[j], CS[j] = F(c, p + 5), F(o, 6 * (p + 4 * c + 1)), F(c)
    for n, source in zip(Ns, (3,4,5)):
        n[j] = F(o, 6 * (p + (source - 2) * c + 7 - source))
K = [F(0)] * 512 + [F(1)]


def row(theta, s):
    alpha = 25 + sum(theta) - s
    return [alpha * U[j] + s * K[j] / 5 - 24 * B[j] - M[j]
            - sum((t * n[j] for t, n in zip(theta, Ns)), F(0)) for j in range(513)]


family = []
for name, (theta, s) in vertices4.items():
    coeff = row(theta, s)
    alpha, g = 25 + sum(theta) - s, F(5,2) - s / 5
    for j, atom in enumerate(inp['atom_columns']):
        p, c, o = atom['a'][0], atom['c'], atom['o']
        assert coeff[j] == alpha * U[j] - minimum(p, c, o, theta, s) + g * c
    assert coeff[512] == F(5,2) - g
    family.append({'name': 'SOURCE2_MAXIMUM_C_REWEIGHTED_INTERNAL_SAFE_' + name,
                   'family': 'TRUE_SAME_BRANCH_REWEIGHTED_THREE_INTERNAL_SAFE',
                   'theta3_theta4_theta5': list(map(str, theta)), 's': str(s),
                   'actual_source2_IC_weight': str(alpha),
                   'a': {str(j): str(v) for j, v in enumerate(coeff)},
                   'rhs': '0', 'numerical_divisor': '25'})

# Original sourceIC25 family is exactly an interior convex combination of
# the two s endpoint rows at the same theta.
for name, theta in vertices3.items():
    s = sum(theta)
    assert 0 <= s <= 9
    direct = row(theta, s)
    lo, hi = row(theta, F(0)), row(theta, F(9))
    assert direct == [(1-s/9)*a+(s/9)*b for a,b in zip(lo,hi)]
    expected = next(r for r in json.loads((HERE/'eight_vertex_family.json').read_text()) if r['name'].endswith(name))
    assert direct == vec(expected['a'])

single = read('main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json')
old_NS5 = vec(single['a'])
assert vec(inp['raw_rows'][1002]['a']) == old_NS5
special_theta = vertices3['V001']
special = row(special_theta, F(9))
gap_vector = [U[j] - K[j]/5 for j in range(513)]
for j in range(513):
    assert 60*special[j] == 5*old_NS5[j]-515*gap_vector[j]
    assert 12*special[j] == old_NS5[j]-103*gap_vector[j]
special_line = {'name':'SOURCE2_MAXIMUM_C_REWEIGHTED_NS5_985',
                'family':'TRUE_SAME_BRANCH_REWEIGHTED_NS5',
                'a':{str(j):str(60*v) for j,v in enumerate(special)},
                'rhs':'0','numerical_divisor':'985',
                'wallet':'985u2+108K-1440B-60M-25N5>=0',
                'scale_from_BR_weight_one':'60'}

# Recheck the current1003 numeric certificate, then derive the full-face
# constants independently with rational elimination rather than reading its
# claimed fixed-function coefficients.
z = list(map(F, cert['primal']))
assert len(z)==513 and all(v>=0 for v in z)
raw=inp['raw_rows'];eq=[vec(e['a']) for e in inp['equalities']];rhs=[F(e['rhs']) for e in inp['equalities']]
assert [dot(e,z) for e in eq]==rhs
ys=list(map(F,cert['dual']['raw_row_weights']));etas=list(map(F,cert['dual']['equality_multipliers']))
assert len(ys)==1003 and all(y>=0 for y in ys)
positive=[j for j,y in enumerate(ys) if y>0]
assert positive==cert['dual']['positive_raw_indices'] and 1002 in positive
for j,r in enumerate(raw):
    slack=sum((F(v)*z[int(k)] for k,v in r['a'].items()),F(0))-F(r['rhs'])
    assert slack==F(cert['raw_row_slacks'][j])>=0 and ys[j]*slack==0
objective=vec(inp['objective']);A=[vec(raw[j]['a']) for j in positive]
dual_res=[objective[j]-sum((ys[k]*a[j] for k,a in zip(positive,A)),F(0))
          -sum((v*e[j] for v,e in zip(etas,eq)),F(0)) for j in range(513)]
assert dual_res==list(map(F,cert['dual']['nonnegative_column_residual']))
assert all(v>=0 for v in dual_res) and all(v*r==0 for v,r in zip(z,dual_res))
assert dot(objective,z)==F(cert['objective'])==sum((ys[j]*F(raw[j]['rhs']) for j in positive),F(0))+dot(etas,rhs)
ZR=[j for j,r in enumerate(dual_res) if r==0]
E=A+eq;H=[F(raw[j]['rhs']) for j in positive]+rhs
labels=[raw[j]['name'] for j in positive]+[e['name'] for e in inp['equalities']]
rr=[[e[j] for j in ZR] for e in E];ops=[[F(i==j) for j in range(len(E))] for i in range(len(E))]
pivots=[];lead=0
for col in range(len(ZR)):
    pivot=next((j for j in range(lead,len(E)) if rr[j][col]),None)
    if pivot is None:continue
    rr[lead],rr[pivot]=rr[pivot],rr[lead];ops[lead],ops[pivot]=ops[pivot],ops[lead]
    d=rr[lead][col];rr[lead]=[v/d for v in rr[lead]];ops[lead]=[v/d for v in ops[lead]]
    for j in range(len(E)):
        if j!=lead and rr[j][col]:
            d=rr[j][col];rr[j]=[a-d*b for a,b in zip(rr[j],rr[lead])];ops[j]=[a-d*b for a,b in zip(ops[j],ops[lead])]
    pivots.append(col);lead+=1
    if lead==len(E):break
assert lead==14 and len(ZR)==21


def fixed_identity(name,target):
    cur=[target[j] for j in ZR];beta=[F(0)]*len(E)
    for r,col in enumerate(pivots):
        d=cur[col];cur=[a-d*b for a,b in zip(cur,rr[r])];beta=[a+d*b for a,b in zip(beta,ops[r])]
    assert cur==[F(0)]*len(ZR),name
    value=dot(beta,H)
    rem=[target[j]-sum((b*e[j] for b,e in zip(beta,E)),F(0)) for j in range(513)]
    assert all(rem[j]==0 for j in ZR)
    assert all(dual_res[j]>0 for j in range(513) if rem[j])
    assert value==dot(target,z)
    for j in range(513):assert target[j]==sum((b*e[j] for b,e in zip(beta,E)),F(0))+rem[j]
    return {'name':name,'constant':str(value),
            'signed_equation_multipliers':{n:str(v) for n,v in zip(labels,beta)},
            'full513_off_support_remainder':{str(j):str(v) for j,v in enumerate(rem)}}


gap_identity=fixed_identity('u2_minus_K_over5',gap_vector)
assert F(gap_identity['constant'])==F(2090367050511169183056222233334689252587,30660506182147093764423146102516809914102360)>0
face_identities=[fixed_identity(r['name'],vec(r['a'])) for r in family]
old_three_values={name:str(dot(row(theta,sum(theta)),z)) for name,theta in vertices3.items()}
new_values={f['name']:f['constant'] for f in face_identities}
best=min(map(F,new_values.values()));best_names=[n for n,v in new_values.items() if F(v)==best]
assert dot(old_NS5,z)==0
special_identity=fixed_identity(special_line['name'],vec(special_line['a']))
assert F(special_identity['constant'])==-515*F(gap_identity['constant'])<0

write('reweighted_polytope.json',{
    'attribution':'Main proposed alpha=25+Theta-s and product domain; early_shared_x_source_audit independently verifies all source shares and finite states.',
    'domain':'three-theta six-facet polytope times [0,9]',
    'necessity_witnesses':necessity,
    'vertices':{n:{'theta':list(map(str,t)),'s':str(s),'alpha':str(25+sum(t)-s)} for n,(t,s) in vertices4.items()},
    'full_hidden_vertex_checks':2048,'exact_minimum_cases':128,
    'common_attainer':'tail0000 if c0; tail1111 if p0c1; tail1110 if p1c1',
    'alpha_minimum':'16','scope':'Complete domain for stated affine MIN and nonnegative internal weights; no arbitrary-wallet optimality claim.'})
write('reweighted_hidden_states.json',hidden)
write('reweighted_minimum_tables.json',minima)
write('sixteen_reweighted_vertex_family.json',family)
write('SOURCE2_MAXIMUM_C_REWEIGHTED_NS5_985.json',special_line)
write('comparison_frozen1003.json',{
    'input_sha256':PINS['visible_maximum_joint_v2/exact_input.json'],
    'certificate_sha256':PINS['visible_maximum_joint_v2_solve/exact_certificate.json'],
    'scale':'BR-average weight1: all rows have common 24B+M query part; original joint has u2 weight25, reweighted alpha varies.',
    'original_eight_theta_row_values':old_three_values,'sixteen_reweighted_row_values':new_values,
    'most_negative_vertices_at_current_face':best_names,'most_negative_value':str(best),
    'u2_minus_K_over5':gap_identity['constant'],
    'old_NS5_slack':'0','special985_integer_slack':special_identity['constant'],
    'special985_over5_identity':'row985/5=oldNS5-103*(u2-K/5)',
    'all_values_constant_on_entire_current_optimal_face':True})
write('current1003_face_identities.json',{
    'equation_names':labels,'equation_rhs':list(map(str,H)),
    'zero_residual_columns':ZR,'restricted_rank':lead,
    'gap_identity':gap_identity,'sixteen_row_identities':face_identities,
    'special985_identity':special_identity,
    'scope':'Signed equalities only on the current optimal face; off-support remainder lies only on columns forced zero by strictly positive old dual residuals.',
    'all513_columns_checked_for_each_identity':True})
result={
    'status':'PASS_MAIN_REWEIGHTED_EXTENSION_COMPLETE_PRODUCT_DOMAIN_AND_CURRENT_FACE_CUTS',
    'Main_attribution_preserved':True,'full_four_parameter_domain_proved':True,
    'theta_vertices':8,'s_endpoints':[0,9],'reweighted_vertices':16,
    'hidden_state_checks':2048,'minimum_cases':128,'literal_menu_checks':menu_checks,
    'row_coefficients_checked':16*513,'source_alpha_lower_bound':'16',
    'original_eight_wallets_exact_convex_combinations':True,
    'current1003_certificate_replay':'1003 raw inequalities,513 dual columns,2 equalities,nonnegativity,complementarity,exact objective PASS',
    'current_face_restricted_rank':lead,'current_face_zero_residual_columns':len(ZR),
    'current_face_signed_identities_checked':18,
    'best_current_face_vertices':best_names,'best_current_face_value':str(best),
    'special985_integer_value':special_identity['constant'],
    'optimizer_calls':0,'Main_builder_solver_or_prior_audit_code_executed_or_imported':False,
    'source_sha256':{'research/workspaces/six-boss1-20261111/'+p:h for p,h in PINS.items()},
    'not_claimed':['new optimization','new global optimum','optimality among arbitrary SPE wallets','half theorem'],
    'outstanding_errors':[]}
write('reweighted_checker_output.json',result)
print(json.dumps({k:result[k] for k in ['status','hidden_state_checks','literal_menu_checks','row_coefficients_checked',
    'best_current_face_vertices','best_current_face_value','special985_integer_value','outstanding_errors']},indent=2))
