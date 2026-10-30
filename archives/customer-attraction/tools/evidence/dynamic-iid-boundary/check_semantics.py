"""Supplemental exact reconstruction from the two finite certificates.

This file imports no historical audit or game solver. It checks the complete
tie-priority construction, the extra 194/9 example, and the conditional
certificate's original36 cone membership. General proofs are in state/.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT/'original/evidence/certificates/customer_attraction/dynamic_iid_local.json').read_text())
game = json.loads((ROOT/'original/examples/customer_attraction/dynamic_iid_local.json').read_text())
w = {sum(1 << a for a in row['topics']): row['multiplicity'] for row in game['customers']}
policy = {tuple(row['history']): row['action'] for row in data['certificate']['actions']}
assert set(data) == {'claim','scope','certificate','root','root_payoffs','construction','dynamic_iid_states','weak_local_deficit','root_Z_exactly_computed','root_Z_upper_bound'}
assert set(data['certificate']) == {'terminal_counts','actions'}
assert len(policy) == len(data['certificate']['actions']) == 2801
ends = {}
def payoff(z, i):
    return sum((F(v, sum(bool(T & (1 << a)) for a in z)) for T,v in w.items() if T & (1 << z[i])), F(0))
def old_action(h):
    if not h: return 0
    if len(h) == 1: return 3 if h[0] < 3 else 0
    return next(a for a in (range(3) if h[1] < 3 else range(3,6)) if a not in h)
for k in range(4,-1,-1):
    for h in product(range(7), repeat=k):
        alternatives = [h+(a,) if k==4 else ends[h+(a,)] for a in range(7)]
        values = [payoff(z,k) for z in alternatives]
        priority = []
        if h.count(6)<2: priority.append(6)
        old_h = tuple(a for a in h if a != 6)
        if len(old_h)<3: priority.append(old_action(old_h))
        priority.extend(range(7))
        best = max(values)
        selected = next(a for a in priority if values[a]==best)
        assert selected == policy[h], (h,selected,policy[h])
        ends[h] = alternatives[selected]
actual_deviations=[]
for k in range(5):
    h=tuple(data['root'][:k])
    vals=[payoff(h+(a,) if k==4 else ends[h+(a,)],k) for a in range(7)]
    actual_deviations.append({'history':list(h),'action':policy[h],'payoffs':list(map(str,vals))})
uniform = [F(1,6)]*6+[F(0)]
h=(6,6,0);r=2
raw_Z=F(0)
for A in product(range(6),repeat=r):
    for T,v in w.items():
        p=sum(bool(T&(1<<a)) for a in h)
        b=sum(bool(T&(1<<a)) for a in A)
        if b: raw_Z+=F(v*b,p+b)/6**r
assert raw_Z==F(194,9)>21

cert=json.loads((ROOT/'original/evidence/certificates/customer_attraction/iid_security_conditional_36.json').read_text())
oldw={T: v for T,v in w.items() if T<64}
def complete(h):
    while len(h)<3: h=h+(old_action(h),)
    return h
def coeff(T,z,i):
    return F(1,sum(bool(T&(1<<a)) for a in z)) if T&(1<<z[i]) else F(0)
root=complete(())
gammas={}
for k in range(3):
    for h in product(range(6),repeat=k):
        z=complete(h)
        for a in range(6):
            alt=complete(h+(a,))
            gammas[h,a]={T:coeff(T,z,k)-coeff(T,alt,k) for T in range(1,64)}
spe_slacks=[sum(F(oldw.get(T,0))*x for T,x in row.items()) for row in gammas.values()]
assert min(spe_slacks)==0 and all(x>=0 for x in spe_slacks)
E={}
psi={}
for T in range(1,64):
    t=F(T.bit_count(),6)
    psi[T]=1-(1-t)**3
    g=1-t+t*t/3
    for a in range(6): E[a,T]=psi[T]-3*bool(T&(1<<a))*g
assert all(sum(F(oldw.get(T,0))*E[a,T] for T in range(1,64))==0 for a in range(6))
residuals={}
for T in range(1,64):
    rhs=sum(F(row['lambda'])*gammas[tuple(row['history']),row['deviation']][T] for row in cert['sparse_spe'])
    rhs+=sum(F(row['lambda'])*E[row['action'],T] for row in cert['sparse_ne'])
    c=int(any(T&(1<<a) for a in root))
    residue=F(c)-psi[T]-rhs
    assert residue==F(cert['residuals'].get(str(T),'0'))>=0
    residuals[str(T)]=str(residue)
assert len(cert['sparse_spe'])==24 and len(cert['sparse_ne'])==2
out={
    'all_dynamic_certificate_entries_consumed':True,
    'complete_tie_priority_reconstruction_nodes':len(ends),
    'actual_deviations':actual_deviations,
    'uniform_old_q_at_PPX0_Z':str(raw_Z),
    'conditional_original36':{'ordered_histories':43,'all_action_comparisons':len(gammas),'minimum_SPE_slack':str(min(spe_slacks)),'all_six_stationarity_slacks_zero':True},
    'conditional_identity_columns':len(residuals),
    'conditional_positive_residuals':sum(F(x)>0 for x in residuals.values()),
    'conditional_residuals':residuals,
}
print(json.dumps(out,indent=2))
