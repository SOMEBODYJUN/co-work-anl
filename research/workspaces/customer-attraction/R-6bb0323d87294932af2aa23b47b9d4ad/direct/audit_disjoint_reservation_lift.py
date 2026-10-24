"""Independent unit-client audit of the disjoint reservation lift example.

Does not import the construction, sibling checker, canonical model/solver,
certificate utilities, linear algebra, or an optimizer. The general theorem is
proved separately; this checks the saved concrete complete policy and p/Q.
"""
from pathlib import Path
from fractions import Fraction
from itertools import product, combinations_with_replacement
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
SEC=HERE.parent/'security'
old=json.loads((ROOT/'examples/customer_attraction/individual_security_failure.json').read_text())
new=json.loads((SEC/'positive_depth_floor_game.json').read_text())
cert=json.loads((SEC/'positive_depth_floor_certificate.json').read_text())
old_clients=tuple(frozenset(c['topics']) for c in old['customers'] for _ in range(c['multiplicity']))
clients=tuple(frozenset(c['topics']) for c in new['customers'] for _ in range(c['multiplicity']))
assert len(old_clients)==34
assert len(clients)==53
assert new['players']==4 and len(new['topics'])==7
assert clients[:34]==old_clients
assert all(c==frozenset({6}) for c in clients[34:])


def utility(clients, profile, i):
    topic=profile[i]
    return sum((Fraction(1,sum(a in c for a in profile)) for c in clients if topic in c),Fraction())


def old_action(h):
    if len(h)==0:return 0
    if len(h)==1:return 3 if h[0]<3 else 0
    assert len(h)==2
    group=range(3) if h[1]<3 else range(3,6)
    return min(a for a in group if a not in h)


def old_leaf(h):
    while len(h)<3:h=h+(old_action(h),)
    return h

old_histories=tuple(h for d in range(3) for h in product(range(6),repeat=d))
eta=min(utility(old_clients,old_leaf(h),len(h)) for h in old_histories)
old_comparisons=0
for h in old_histories:
    actual=utility(old_clients,old_leaf(h),len(h))
    for a in range(6):
        assert actual>=utility(old_clients,old_leaf(h+(a,)),len(h))
        old_comparisons+=1
sizes=tuple(sum(a in c for c in old_clients) for a in range(6))
deltas=tuple(min(sum(a in c and b in c for c in old_clients) for b in range(6)) for a in range(6))
J=Fraction(19);n=3
assert eta==Fraction(29,3)
assert J/2<=eta
assert J>=max(Fraction(s)-Fraction(d,2) for s,d in zip(sizes,deltas))
assert all(Fraction(s,2)>J/n for s in sizes)

rows=cert['strategy']['actions']
policy={tuple(row['history']):row['action'] for row in rows}
all_histories=tuple(h for d in range(4) for h in product(range(7),repeat=d))
assert len(rows)==len(policy)==len(all_histories)
assert set(policy)==set(all_histories)
assert all(type(a) is int and 0<=a<7 for a in policy.values())
assert policy[()]==6
nice=tuple(h for h in all_histories if h and h[0]==6 and 6 not in h[1:])
# The sibling's certificate selects different old terminal ties at some nice
# nodes. Preserve its valid offroot/extra-B subtrees, but implement the literal
# general lift under review by retaining the published old sigma on EVERY
# nice history, including off-path old-only histories after root B.
changed_nice=sum(policy[h]!=old_action(h[1:]) for h in nice)
for h in nice:policy[h]=old_action(h[1:])
assert all(policy[h]==old_action(h[1:]) for h in nice)

leaves={}

def leaf(h):
    if h not in leaves:
        if len(h)==4:leaves[h]=h
        else:leaves[h]=leaf(h+(policy[h],))
    return leaves[h]

new_comparisons=0
for h in all_histories:
    current=utility(clients,leaf(h),len(h))
    for a in range(7):
        alternative=utility(clients,leaf(h+(a,)),len(h))
        assert current>=alternative,(h,a,current,alternative)
        new_comparisons+=1
z=leaf(())
u=tuple(utility(clients,z,i) for i in range(4))
assert z==(6,0,3,4)
assert u==(Fraction(19),Fraction(29,3),Fraction(67,6),Fraction(67,6))
W=sum(any(a in c for a in z) for c in clients)
OPT=max(sum(any(a in c for a in choices) for c in clients) for choices in combinations_with_replacement(range(7),4))
assert W==51 and OPT==53

# Verify the exact static saddle point directly on expanded unit clients.
def query(a,B):
    return sum((Fraction(1,1+sum(b in c for b in B)) for c in clients if a in c),Fraction())

security=cert['security']
p=tuple(Fraction(x) for x in security['primary'])
Q=tuple((tuple(row['rivals']),Fraction(row['probability'])) for row in security['dual'])
assert len(p)==7 and all(v>=0 for v in p) and sum(p)==1
assert all(len(B)==3 and all(0<=b<7 for b in B) and q>=0 for B,q in Q)
assert sum(q for B,q in Q)==1
all_B=tuple(product(range(7),repeat=3))
primary_min=min(sum((p[a]*query(a,B) for a in range(7)),Fraction()) for B in all_B)
dual_values=tuple(sum((q*query(a,B) for B,q in Q),Fraction()) for a in range(7))
v=Fraction(security['value'])
assert primary_min==max(dual_values)==v==Fraction(28481,2924)
assert len(set(dual_values))==1
assert v-u[1]==Fraction(647,8772)>0

literal_cert=json.loads(json.dumps(cert))
literal_cert['strategy']['actions']=[{'history':list(h),'action':policy[h]}
                                   for h in sorted(policy,key=lambda h:(len(h),h))]
literal_cert['construction_note']='Literal disjoint reservation lift: published old34 sigma at all root-B old-only histories; sibling SPE continuations retained on the closed extra-B and first-old domains.'
(HERE/'disjoint_reservation_literal_certificate.json').write_text(json.dumps(literal_cert,indent=2)+'\n')

report={'status':'PASS','method':'expanded distinct unit clients, direct ordered-history policy replay, and exact saddle verification',
        'old_histories':len(old_histories),'old_action_comparisons':old_comparisons,'eta':str(eta),
        'old_sizes':sizes,'delta':deltas,'J':str(J),'tail_B_deviation_cap':str(J/2),
        'root_old_upper_bound':str(max(Fraction(s)-Fraction(d,2) for s,d in zip(sizes,deltas))),
        'minimum_last_old_alternative':str(min(Fraction(s,2) for s in sizes)),
        'all_B_last_payoff':str(J/n),'new_histories':len(all_histories),'nice_histories':len(nice),
        'sibling_nice_ties_overridden':changed_nice,
        'new_action_comparisons':new_comparisons,'actual_path':z,'utilities':list(map(str,u)),
        'W':W,'OPT':OPT,'static_backgrounds':len(all_B),'v4':str(v),'v4_minus_u2':str(v-u[1]),
        'scope':'general lift proof audited separately; concrete finite SPE and saddle point exact; Q-CAG-HALF remains OPEN'}
(HERE/'disjoint_reservation_lift_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
