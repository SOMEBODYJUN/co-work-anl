"""Independent unit-customer audit; imports no game or attack implementation."""
from fractions import Fraction as Q
from itertools import product,combinations_with_replacement
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
source=HERE.parent/'credible_construction'/'recursive_step_attack.json'
record=json.loads(source.read_text())[0]
instance=record['instance'];n=len(instance['topics']);m=instance['players']
customers=[frozenset(row['topics']) for row in instance['customers'] for _ in range(row['multiplicity'])]
actions={tuple(row['history']):row['action'] for row in record['strategy']['actions']}
assert len(actions)==sum(n**i for i in range(m))

def continue_path(prefix):
    h=tuple(prefix)
    while len(h)<m:h=h+(actions[h],)
    return h

def payoff(h,i):
    return sum((Q(1,sum(a in customer for a in h)) for customer in customers if h[i] in customer),Q(0))

histories=deviations=0;minslack=None
for depth in range(m):
    for h in product(range(n),repeat=depth):
        histories+=1
        actual=continue_path(h);v=payoff(actual,depth)
        for a in range(n):
            if a==actions[h]:continue
            deviations+=1
            dev=continue_path(h+(a,));s=v-payoff(dev,depth)
            assert s>=0,(h,a,v,payoff(dev,depth))
            minslack=s if minslack is None else min(minslack,s)

path=continue_path(());u=[payoff(path,i) for i in range(m)]
W=sum(any(a in c for a in path) for c in customers)
assert sum(u)==W

def profit(portfolio,background=()):
    out=Q(0)
    for c in customers:
        e=sum(a in c for a in portfolio);b=sum(a in c for a in background)
        if e:out+=Q(e,b+e)
    return out

def F(r,background=()):
    table=[(profit(p,background),p) for p in combinations_with_replacement(range(n),r)]
    value=max(v for v,p in table)
    return value,[p for v,p in table if v==value]

def floor(r,background=()):
    values=[sum((Q(1,r+sum(a in c for a in background)) for c in customers if t in c),Q(0)) for t in range(n)]
    return max(values),values

Froot,rootmax=F(4);Fchild,childmax=F(3,(path[0],))
hroot,hrootvalues=floor(4);hchild,hchildvalues=floor(3,(path[0],))
Rchild=profit(path[1:],(path[0],));Eroot=2*W-Froot;Echild=2*Rchild-Fchild
reserve=max(Q(0),6*hchild-Fchild);needed=Froot-Fchild-2*u[0]
rhs=max(8*hroot,2*u[0]+max(Fchild,6*hchild))
assert (Froot,Fchild,hroot,hchild,tuple(u),Rchild,Eroot,Echild,reserve,needed,rhs)==(Q(69),Q(41),Q(15,2),Q(15,2),(Q(10),Q(10),Q(10),Q(18)),Q(38),Q(27),Q(35),Q(4),Q(8),Q(65))
assert Eroot==Echild+2*u[0]-(Froot-Fchild)
report={'status':'independent unit-customer verification passed; floor-reserve transition is false','source':str(source.relative_to(HERE.parent)),'customers':len(customers),'histories':histories,'different_action_deviations':deviations,'minimum_SPE_slack':str(minslack),'actual_path':path,'payoffs':[str(x) for x in u],'W':W,'F_root':str(Froot),'F_root_maximizers':rootmax,'F_child':str(Fchild),'F_child_maximizers':childmax,'h_root':str(hroot),'h_root_action_values':[str(x) for x in hrootvalues],'h_child':str(hchild),'h_child_action_values':[str(x) for x in hchildvalues],'R_child_actual':str(Rchild),'E_root_actual':str(Eroot),'E_child_actual':str(Echild),'floor_reserve':str(reserve),'reserve_needed_for_bare_half_induction':str(needed),'root_floor_budget':str(8*hroot),'candidate_RHS':str(rhs),'strict_failure':str(Froot-rhs)}
print(json.dumps(report,indent=2))
