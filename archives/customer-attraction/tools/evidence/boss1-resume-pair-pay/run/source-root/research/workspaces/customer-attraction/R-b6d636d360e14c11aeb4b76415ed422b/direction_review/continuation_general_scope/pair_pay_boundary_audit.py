"""Read-only independent arithmetic checks of exact general interfaces.

Finite checks target the stated identities and an already supplied certificate;
they are not additional fixed-player research or evidence for Q-CAG-HALF.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json

ROOT=next(p for p in Path(__file__).resolve().parents if (p / 'customer_attraction' / '__init__.py').is_file())
NEW=ROOT/'research/workspaces/customer-attraction/R-7c3db62487a34730a704a4f2eb401556'

def direct_error(r,s,d,a,b):
    q=d+r*a+s*b
    qp=d+s*a+r*b
    return (F(r*s*a,q) if a else 0)+(F(r*(r-s)*b,qp) if b else 0)-(F(s*s*a,qp) if a else 0)-(r-s)*b

pair_checks=0
for r in range(1,9):
    for s in range(1,r+1):
        for d in range(21):
            for a,b,c in product((0,1),repeat=3):
                e=direct_error(r,s,d,a,b)
                rent=F(d,d+r+s*a) if b else F(0)
                rhs=F(s*(r-s)*d,(d+r)*(d+s)) if a and not b else F(0)
                assert e+(r-s)*rent==rhs>=0
                kernel=F(s*(r-s)*d,(d+r)*(d+s+r*b))
                assert e-direct_error(r,s,d,c,b)==kernel*(a-c)
                pair_checks+=1

# A label-balanced two-edge circulation with changing backgrounds, at the
# same total player count, has a residual. One client belongs only to a;
# backgrounds e_a and e_c both contain one provider.
residual=(direct_error(2,1,1,1,0)-direct_error(2,1,1,0,0)
          +direct_error(2,1,0,0,0)-direct_error(2,1,0,1,0))
assert residual==F(1,6)

def direct_charge(m,k,types):
    points={F(0),F(4)}
    points.update(F(4*m*(b+1),d*(k-1)+m*(b+1)) for w,b,d in types if w and d)
    def evaluate(t):
        return sum((w*(1-F(2*(k-2)*d,m*(b+k))
            -min(F(t*d,m*(b+1)),F(t*d/m+4-t,b+k)))
            for w,b,d in types if d),F(0))
    return min((evaluate(t),t) for t in points)

spec=importlib.util.spec_from_file_location('pay_subject',NEW/'pay/all_path_pay.py')
subject=importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)
quantile_checks=0
for m in range(2,9):
    for k in range(2,m+1):
        cases=[[],[(1,0,m)],[(2,m-k,1)],[(3,0,1),(5,m-k,m)],
               [(7,0,0),(2,0,m),(3,m-k,1)]]
        for types in cases:
            assert subject.charge(m,k,types)==direct_charge(m,k,types)
            quantile_checks+=1

# Independently verify the existing m=5 whole-history certificate from
# literal customer sets and strategies, without the model/certificate verifier.
obj=json.loads((NEW/'pay/monotone_parameter_m5.json').read_text())
rows=obj['instance']['customers']
actions={tuple(r['history']):r['action'] for r in obj['certificate']['actions']}
m=obj['instance']['players']
K=len(obj['instance']['topics'])
def walk(h):
    while len(h)<m:h=h+(actions[h],)
    return h
def payoff(q,a):
    return sum((F(row['multiplicity'],sum(z in row['topics'] for z in q))
                for row in rows if a in row['topics']),F(0))
history_checks=comparisons=0
for i in range(m):
    for h in product(range(K),repeat=i):
        history_checks+=1
        chosen=walk(h)
        for a in range(K):
            assert payoff(chosen,actions[h])>=payoff(walk(h+(a,)),a)
            comparisons+=1
M=3*(m-1)
jump=[]
for length in (1,2):
    charge,t=direct_charge(m,m-length,[(M,length,1),(m-1,0,1)])
    jump.append({'prefix_length':length,'t':str(t),'margin':str(charge-2*F(length*M,m))})
assert F(jump[1]['t'])<F(jump[0]['t'])
assert all(F(r['margin'])>0 for r in jump)
print(json.dumps({'status':'PASS','pair_rent_and_shared_kernel_checks':pair_checks,
 'variable_background_balanced_label_residual':str(residual),
 'quantile_endpoint_and_tie_checks':quantile_checks,
 'existing_m5_complete_history_checks':history_checks,
 'existing_m5_comparisons_including_self':comparisons,'left_jump':jump,
 'scope':'Exact finite regression of named general interfaces; no general proof.'},indent=2))
