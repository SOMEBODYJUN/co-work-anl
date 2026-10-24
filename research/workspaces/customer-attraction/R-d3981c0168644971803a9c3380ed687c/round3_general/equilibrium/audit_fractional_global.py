"""Definition-level exact audit of the single targeted raw witness.

No model, SPE solver, LP, or discovery-script imports. Multiplicities are
expanded into distinct unit customers. Every ordered history is checked.
"""
from fractions import Fraction
from itertools import product, combinations_with_replacement
from pathlib import Path
import json

D=Path(__file__).resolve().parent
raw=json.loads((D/'fractional_global_raw.json').read_text())
players=raw['players']; labels=range(len(raw['topics']))
customers=[]
for mask,count in raw['customer_mask_multiplicities'].items():
    interested=frozenset(a for a in labels if (int(mask)>>a)&1)
    customers.extend([interested]*count)
policy={tuple(row['history']):row['action'] for row in raw['policy']}
p=tuple(Fraction(s) for s in raw['p'])
assert sum(p)==1 and all(q>=0 for q in p)
assert len(policy)==sum(len(raw['topics'])**i for i in range(players))

def finish(prefix):
    h=list(prefix)
    while len(h)<players:h.append(policy[tuple(h)])
    return tuple(h)

def payoff(profile,position):
    return sum((Fraction(1,sum(a in interest for a in profile))
                for interest in customers if profile[position] in interest),Fraction(0))

min_ic=None; comparisons=0; strict=0
for depth in range(players):
    for prefix in product(labels,repeat=depth):
        prescribed=finish(prefix)
        prescribed_utility=payoff(prescribed,depth)
        for action in labels:
            alternative=finish(prefix+(action,))
            gap=prescribed_utility-payoff(alternative,depth)
            assert gap>=0,(prefix,action,gap)
            min_ic=gap if min_ic is None else min(min_ic,gap)
            comparisons+=1; strict+=gap>0

z=finish(())
u=[payoff(z,i) for i in range(players)]
W=sum(any(action in interest for action in z) for interest in customers)
assert sum(u)==W
rows=[]
for i in range(players):
    endpoints=[finish(z[:i]+(a,)) for a in labels]
    competitors=[y[:i]+y[i+1:] for y in endpoints]
    diagonal=sum((p[a]*payoff(endpoints[a],i) for a in labels),Fraction(0))
    integer=Fraction(0); fractional=Fraction(0); variance_credit=Fraction(0)
    for interest in customers:
        px=sum(p[a] for a in interest)
        counts=[sum(b in interest for b in B) for B in competitors]
        mean=sum(p[a]*counts[a] for a in labels)
        inverse=sum((p[a]/(1+counts[a]) for a in labels),Fraction(0))
        integer+=px*inverse
        fractional+=px/(1+mean)
        variance_credit+=px*sum((p[a]*(counts[a]-mean)**2/
                                ((1+counts[a])*(1+mean)**2)
                                for a in labels),Fraction(0))
    assert integer-fractional==variance_credit
    slack=u[i]-diagonal; correlation=diagonal-integer
    assert slack>=0
    assert u[i]-fractional==slack+correlation+variance_credit
    rows.append({'position':i+1,'u':str(u[i]),'D':str(diagonal),'C':str(integer),
                 'F':str(fractional),'e':str(slack),'kappa':str(correlation),
                 'Jensen':str(variance_credit),'u_minus_F':str(u[i]-fractional)})

Ftotal=sum(Fraction(r['F']) for r in rows)
assert Ftotal-W==Fraction(199,60)
assert list(z)==raw['claimed_path'] and str(W)==raw['claimed_welfare']

# Merely a transparent static upper witness: this finite minimization does not
# solve the mixed value and does not claim p is optimal.
static_caps=[]
for B in combinations_with_replacement(labels,players-1):
    queries=[sum((Fraction(1,1+sum(b in interest for b in B))
                  for interest in customers if a in interest),Fraction(0)) for a in labels]
    static_caps.append((max(queries),B,queries))
cap,B,queries=min(static_caps)
opt=max(sum(any(a in interest for a in profile) for interest in customers)
        for profile in product(labels,repeat=players))
result={'status':'PASS','unit_customers':len(customers),'topics':len(raw['topics']),
        'players':players,'ordered_histories':len(policy),'comparisons_including_self':comparisons,
        'strict_comparisons':strict,'minimum_ic':str(min_ic),'path':list(z),'payoffs':list(map(str,u)),
        'W':W,'OPT':opt,'p':list(map(str,p)),'rows':rows,'fractional_sum':str(Ftotal),
        'fractional_sum_minus_W':str(Ftotal-W),'best_pure_static_upper':{'competitors':list(B),
        'query_values':list(map(str,queries)),'cap':str(cap)},
        'scope':'Only disproves all-p sum_i F_i(p)<=W. No claim of optimal p, mixed/static fractional counterexample, or half counterexample.'}
(D/'fractional_global_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
