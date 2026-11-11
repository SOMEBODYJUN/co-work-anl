"""Main independently rebuilds both new universal families; no optimization."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

P = Path(__file__).resolve().parent
paths = [
    'source2_joint_internal_safe/sixteen_reweighted_vertex_family.json',
    'source2_joint_internal_safe/proof.md',
    'all_source_nested_safe_family/exact_family.json',
    'all_source_nested_safe_family/proof.md',
    'visible_maximum_joint_v2/exact_input.json',
    'visible_maximum_joint_v2_solve/exact_certificate.json',
]
pins = {s: hashlib.sha256((P/s).read_bytes()).hexdigest() for s in paths}
joint = json.loads((P/paths[0]).read_text())
cross = json.loads((P/paths[2]).read_text())['rows']
old = json.loads((P/paths[4]).read_text())
cert = json.loads((P/paths[5]).read_text())
atoms = list(product((0, 1), repeat=9))
assert len(joint) == 16 and len(cross) == 36
assert old['variables'] == 513 and len(old['raw_rows']) == 1003
for h, a in enumerate(atoms):
    col = old['atom_columns'][h]
    assert (tuple(col['a']) + (col['x'], col['o'], col['c'])) == a

def coeff(row, h):
    return F(row['a'].get(str(h), '0'))

local_joint = []
joint_coeffs = 0
for row in joint:
    th = tuple(map(F, row['theta3_theta4_theta5']))
    s = F(row['s'])
    a = 25 + sum(th) - s
    assert a == F(row['actual_source2_IC_weight']) and a >= 16
    assert min(th) >= 0 and th[2] <= F(5, 12)
    assert th[1] + th[2]/36 <= F(5, 12)
    assert th[0] + th[1]/72 + th[2]/36 <= F(5, 12)
    assert s in [0, 9]
    assert F(row['rhs']) == 0 and F(row['numerical_divisor']) == 25
    for p, c, o in product((0, 1), repeat=3):
        wanted = F(5*c, 2) + F(24*c, p+5) - s*c/5
        wanted += F(o, 6*(p+4*c+1))
        wanted += sum(th[j-3]*F(o, 6*(p+(j-2)*c+7-j)) for j in range(3, 6))
        actual = []
        for r in product((0, 1), repeat=4):
            load = p+c+sum(r)
            value = (a*c-r[3]-sum(th[k]*r[k] for k in range(3)))/load if load else F(0)
            value += F(sum(r[:3]), 2)+r[3]+F(o, 6*(p+c+sum(r[:3])+1))
            value += sum(th[j-3]*F(o, 6*(p+c+sum(r[:j-3])+7-j)) for j in range(3, 6))
            assert value >= wanted, (row['name'], p, c, o, r)
            actual.append(value)
        assert min(actual) == wanted
        local_joint.append({'row': row['name'], 'pco': [p,c,o], 'minimum': str(wanted),
                            'zero_states': [list(r) for r,v in zip(product((0,1),repeat=4),actual) if v == wanted]})
    for h, bits in enumerate(atoms):
        b, x, o, c = bits[:6], bits[6], bits[7], bits[8]
        p = b[0]
        u = F(b[1], sum(b)) if sum(b) else F(0)
        expected = a*u - F(24*c,p+5) - F(o,6*(p+4*c+1))
        expected -= sum(th[j-3]*F(o,6*(p+(j-2)*c+7-j)) for j in range(3,6))
        assert coeff(row,h) == expected, (row['name'], h)
        joint_coeffs += 1
    assert coeff(row,512) == s/5
    joint_coeffs += 1

theta = F(5,12)
def m(i,p,t,o):
    n = 6-i
    D = p+n+1
    return (F((n+1)*t,2) + F(24*t,D) + F(o,6*(p+1+n*t))
            + theta*(F(o,6*(p+(5-i)*t+2))-F(t,min(D,5))))

cross_states = 0
cross_minima = []
for i in range(1,5):
    n = 6-i
    for p in range(i):
        for t,o in product((0,1),repeat=2):
            values = []
            for r in product((0,1), repeat=n):
                load = p+t+sum(r)
                value = (F(25*t-r[-1])-theta*r[-2])/load if load else F(0)
                value += F(sum(r[:-1]),2)+r[-1]+F(o,6*(p+t+sum(r[:-1])+1))
                value += theta*F(o,6*(p+t+sum(r[:-2])+2))
                assert value >= m(i,p,t,o), (i,p,t,o,r)
                values.append(value)
                cross_states += 1
            assert min(values) == m(i,p,t,o)
            cross_minima.append({'i':i,'p':p,'t':t,'o':o,'minimum':str(min(values))})
assert cross_states == 416 and len(cross_minima) == 40

cross_coeffs = 0
for row in cross:
    i,T = row['source'],row['T']
    n = 6-i
    assert F(row['rhs']) == 0 and F(row['numerical_divisor']) == 25
    for h,bits in enumerate(atoms):
        b,x,o,c = bits[:6],bits[6],bits[7],bits[8]
        p = sum(b[:i-1])
        u = F(b[i-1],sum(b)) if sum(b) else F(0)
        if T == 'outerOmean':
            cost = m(i,p,0,o)+F(o,6)*(m(i,p,1,o)-m(i,p,0,o))
        else:
            t = b[int(T[1:])-1] if T.startswith('A') else {'X':x,'C':c}[T]
            cost = m(i,p,t,o)
        assert coeff(row,h) == 25*u-cost, (row['name'],h)
        cross_coeffs += 1
    assert coeff(row,512) == F(n+1,2)
    cross_coeffs += 1

ns5 = old['raw_rows'][-1]
c2 = next(r for r in cross if r['source']==2 and r['T']=='C')
for h in range(513):
    ec = atoms[h][-1] if h < 512 else -1
    assert coeff(ns5,h) == 12*coeff(c2,h)+29*ec

primal = list(map(F,cert['primal']))
diagnostics = []
for row in joint+cross:
    slack = sum(coeff(row,h)*primal[h] for h in range(513))-F(row['rhs'])
    diagnostics.append({'name':row['name'],'slack':str(slack),'negative':slack<0})
assert pins == {s:hashlib.sha256((P/s).read_bytes()).hexdigest() for s in paths}
result = {'owner':'Boss1/Main','status':'PASS','optimizer_calls':0,
          'proofs_read': [paths[1],paths[3]], 'source_sha256':pins,
          'joint_hidden_states':2048,'joint_minima':local_joint,
          'joint_full_coefficients':joint_coeffs,'cross_hidden_states':cross_states,
          'cross_minima':cross_minima,'cross_full_coefficients':cross_coeffs,
          'NS5_C2_full_column_identity':513,'frozen1003_diagnostics':diagnostics,
          'scope':'Universal necessary rows and exact fixed old-point diagnostics; no new optimizer or SPE existence claim.'}
(P/'main_joint_cross_family_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','joint_coefficients':joint_coeffs,'cross_coefficients':cross_coeffs,
                  'negative_on_frozen1003':[x for x in diagnostics if x['negative']]},ensure_ascii=False))
