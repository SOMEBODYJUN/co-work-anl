#!/usr/bin/env python3
"""Rebuild every old positive row on arbitrary legal six-query menus.

Only mathematical formulas and frozen JSON data are used; no local Python
module is imported.  Zero-paid OPT upper caps are not asserted for arbitrary O.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib
import json

OUT = Path(__file__).resolve().parent
WS = OUT.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(rel):
    return json.loads((WS / rel).read_text())


def share(t, L):
    return F(t, L) if L else F(0)


def store(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2,
                                     default=lambda x: str(x) if isinstance(x, F) else None) + '\n')


sources = [
    'visible_maximum_joint_v5/exact_input.json',
    'visible_maximum_joint_v5_solve/exact_certificate.json',
    'universal_true_x_tail/proof.md',
    'main_thirty_index_strengthening/proof.md',
    'all_source_minimal_cap_safe/proof.md',
    'source2_minimal_cap_safe/proof.md',
]
pins = {f: sha(WS / f) for f in sources}
data = read(sources[0])
cert = read(sources[1])
rows, atoms = data['raw_rows'], data['atom_columns']
positive = [i for i, v in enumerate(cert['dual']['raw_row_weights']) if F(v)]
assert positive == [46,47,134,218,221,868,1803,2563,2564,2606]
recovered = {i: [] for i in positive}
true_x_tables = []
c30_tables = []
for j, t in enumerate(atoms):
    aa, x, o, c = t['a'], t['x'], t['o'], t['c']
    L, prefix5, P = sum(aa), sum(aa[:5]), sum(aa[:4])
    u = [share(a, L) for a in aa]
    recovered[46].append(u[5] - F(x, prefix5 + 1))
    recovered[47].append(u[5] - F(o, 6 * (prefix5 + 1)))
    D = P + 1
    # RC(X,mean): two truthful ICs plus f_P(X)>=f_P(J_X).
    recovered[134].append(u[4] - F(o,6*D) + F(x*o,6*D*(D+1)))
    if c == 0:
        b = sum(aa[:3])
        d = b+x+1
        theta = F(o,6)
        vals = []
        for y, z in product([0,1], repeat=2):
            value = F(4096*x,b+1+y+z)+F(800*y,D)+71*z+384*(theta-z)/(d+y)
            value += 512*((aa[5]+theta)/d-aa[5]*theta/(d*(d+1))
                          -F(y,d+z)-F(z,d+y)-F(y,d*(d+1)))
            value += 900*((z+theta)/D-z*theta/(D*(D+1)))
            kernel = F(384,d+y)+512*(F(1,d)-F(aa[5],d*(d+1)))
            kernel += 900*(F(1,D)-F(z,D*(D+1)))
            assert kernel > 0
            vals.append({'tail':[y,z], 'cost':value, 'd_to_o_monotonicity_kernel':kernel})
        minimum = min(v['cost'] for v in vals)
        for v in vals:
            v['residual_to_minimum'] = v['cost']-minimum
        true_x_tables.append({'old_eight_bit_type':j//2, 'minimum':minimum,
                              'all_weak_tails':[v['tail'] for v in vals if v['cost']==minimum],
                              'all_four_states':vals})
    else:
        minimum = true_x_tables[-1]['minimum']
    recovered[218].append(4096*u[3]+900*u[4]+F(1700*x,D)-minimum)
    # C30 is evaluated on every actual type, retaining both X/C duplicates.
    b = aa[0]+aa[1]
    aq = []
    for q in [0,1]:
        values = []
        for r,y,z in product([0,1],repeat=3):
            dd = 1+b+q+r
            cost = F(126000*q,b+1+r+y+z)+F(43*r+31218*y+34458*z,b+aa[2]+3)
            cost += F(1654*(r+y+z),b+aa[2]+aa[3]+aa[4]+1)
            cost += 5400*(F(o,6)-z)/(dd+y)
            cost += 7740*(F(o,3*dd)-F(y,dd+z)-F(z,dd+y)-F(y,dd*(dd+1)))
            values.append(cost)
        aq.append(min(values))
    envelope = aq[0] if not o else min((5*aq[0]+aq[1])/6,aq[1])
    recovered[221].append(126000*u[2]+65719*u[3]+4962*u[5]-envelope)
    c30_tables.append({'column':j,'a0':aq[0],'a1':aq[1],'complete_menu_envelope':envelope})

source_states = []
params = {
    1803:([F(0),F(5977,6912),F(43,48)],F(61273,6912),'C',True),
    2563:([F(0),F(0),F(8,9)],F(9),'A5',False),
    2564:([F(0),F(0),F(8,9)],F(9),'A6',False),
    2606:([F(0),F(5977,6912),F(43,48)],F(0),'C',False),
}
for index,(tau,s,target,c_only) in params.items():
    beta = [F(1,12)+tau[0]+tau[1]/72+tau[2]/36,
            F(1,12)+tau[1]+tau[2]/36,F(1,12)+tau[2]]
    S = 1+sum(beta)
    a = 25+sum(tau)-s
    assert a > 0 and min(beta)>0 and min(tau)>=0
    mins = {}
    tables = []
    for p,t,o in product([0,1],repeat=3):
        vals = []
        for tail in product([0,1],repeat=4):
            L = p+t+sum(tail)
            first = (a*t-tail[3]-sum(tau[k]*tail[k] for k in range(3)))/L if L else F(0)
            cost = first + sum(beta[k]*tail[k] for k in range(3))+tail[3]
            cost += F(o,6*(p+t+sum(tail[:3])+1))
            cost += sum(tau[k]*F(o,6*(p+t+sum(tail[:k])+4-k)) for k in range(3))
            vals.append({'tail':list(tail),'cost':cost})
        m = min(v['cost'] for v in vals)
        closed = t*(S+F(24,p+5)-s/5)+F(o,6*(p+4*t+1))
        closed += sum(tau[k]*F(o,6*(p+(k+1)*t+4-k)) for k in range(3))
        assert m == closed
        for v in vals:v['residual_to_minimum'] = v['cost']-m
        tables.append({'pto':[p,t,o],'minimum':m,
                       'all_weak_tails':[v['tail'] for v in vals if v['cost']==m],
                       'all16_states':vals})
        mins[p,t,o] = m
    for obj in atoms:
        aa,o,c = obj['a'],obj['o'],obj['c']
        target_member = c if target=='C' else aa[int(target[1])-1]
        val = a*share(aa[1],sum(aa))-mins[aa[0],target_member,o]
        if c_only:val += (S-s/5)*c
        recovered[index].append(val)
    recovered[index].append(s/5 if c_only else S)
    source_states.append({'raw_index':index,'forced_target':target,'tau':tau,'s':s,
                          'a':a,'beta':beta,'S':S,'C_only':c_only,'tables':tables})
for i in [46,47,134,221]:recovered[i].append(F(0))
recovered[218].append(F(71))
root_a = F(883952004100291,8438786930961360)
root_b = F(37482242363557,1875285984658080)
recovered[868] = [share(t['a'][0],sum(t['a']))-root_b*t['o'] for t in atoms]+[-root_a]
checks = []
for i in positive:
    assert len(recovered[i])==513
    for j, v in enumerate(recovered[i]):
        actual = F(rows[i]['a'].get(str(j),'0'))
        assert v == actual, (i,j,v,actual)
        checks.append({'raw_index':i,'column':j,'from_true_budget':v,
                       'frozen_input_coefficient':actual,'difference':v-actual})
assert len(checks)==5130
assert all(sha(WS/f)==v for f,v in pins.items())
store('all5130_original_positive_source_coefficients.json',checks)
store('original_true_X_all1024_states.json',true_x_tables)
store('original_actual_C30_all512_envelopes.json',c30_tables)
store('original_positive_source2_all512_hidden_states.json',source_states)
summary = {'status':'PASS_ALL_OLD_POSITIVE_ROWS_ARBITRARY_LEGAL_SIX_QUERY_UNION',
           'agent_id':'/root/delta_uniform_audit','optimizer_calls':0,'producer_imports':0,
           'all_positive_raw_indices':positive,'all5130_coefficients_equal':True,
           'true_X_four_tail_states':1024,'source2_original_hidden_states':512,
           'source2_all_weak_ties_retained':True,
           'X_is_legal_fP_maximizer_at_the_actual_four_action_prefix':True,
           'X_and_C_not_identified':True,
           'arbitrary_menu_validity':'All positively paid sources use legal queries, their true continuations, and nonnegative membership weakening; no positive OPT upper-cap weight.',
           'all_sources_unchanged':True,'source_pins':pins}
store('positive_source_scope_check.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
