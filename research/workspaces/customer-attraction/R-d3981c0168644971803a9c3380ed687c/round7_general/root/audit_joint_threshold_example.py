"""Independent full ordered BI for explicit three-resource x two-resource products.
Only audits the stated all-parameter formula; does not prove arbitrary-m half.
"""
from fractions import Fraction as F
from itertools import product
from math import floor
from pathlib import Path
import json

def check(q,a,b,bank_copies=None):
    banks=q if bank_copies is None else bank_copies
    actions=tuple(product(tuple(product(range(3),repeat=q)),tuple(product(range(2),repeat=banks))))
    K=len(actions)
    clients=[]
    for j in range(q):
        for e in range(3):
            interest=frozenset(k for k,(es,bs) in enumerate(actions) if es[j]==e)
            clients.extend([interest]*a)
    for j in range(banks):
        for v in range(2):
            interest=frozenset(k for k,(es,bs) in enumerate(actions) if bs[j]==v)
            clients.extend([interest]*b)
    def pay(z):
        vals=[F(0)]*3
        for interest in clients:
            own=[j for j,t in enumerate(z) if t in interest]
            for j in own: vals[j]+=F(1,len(own))
        return tuple(vals)
    ell=[];thetas=[];witnesses=[];leaves=0;comparisons=0
    for root in range(K):
        br={};thresholds={};pays={}
        for nxt in range(K):
            allp=tuple(pay((root,nxt,last)) for last in range(K));leaves+=K
            best=max(v[2] for v in allp)
            br[nxt]=tuple(last for last in range(K) if allp[last][2]==best)
            thresholds[nxt]=min(allp[last][1] for last in br[nxt])
            for last in range(K):pays[nxt,last]=allp[last]
            comparisons+=K
        theta=max(thresholds.values());thetas.append(theta)
        feasible=[(pays[nxt,last][0],nxt,last) for nxt in range(K) for last in br[nxt] if pays[nxt,last][1]>=theta]
        value,nstar,lstar=min(feasible);ell.append(value)
        # A full child controller, with every off-path next action punished by a real last BR.
        last_policy={nxt:(lstar if nxt==nstar else min(br[nxt],key=lambda l:(pays[nxt,l][1],l))) for nxt in range(K)}
        obey=pays[nstar,lstar][1]
        for nxt in range(K):
            assert obey>=pays[nxt,last_policy[nxt]][1]
            comparisons+=1
            assert last_policy[nxt] in br[nxt]
        witnesses.append({'root_action':root,'next_action':nstar,'last_action':lstar,'root_profit':str(value),'next_profit':str(obey),'theta':str(theta),'last_action_for_each_next_action':[last_policy[j] for j in range(K)]})
    rem=banks*b-a*(banks*b//a)
    formula=F(q*a+banks*b,2)+F(a,2)*max(0,q-banks*b//a)
    assert set(ell)=={formula}
    assert set(thetas)=={F(q*a)+F(banks*b,2)}
    root_IC=sum(1 for x in ell if ell[0]>=x)
    assert root_IC==K
    target0=actions.index(((0,)*q,(0,)*banks))
    target2=actions.index(((1,)*q,(1,)*banks))
    target_pay=pay((target0,target0,target2))
    assert target_pay==(F(q*a+banks*b,2),F(q*a+banks*b,2),F(q*a+banks*b))
    assert sum(target_pay)==2*(q*a+banks*b)
    assert len(clients)-2*sum(target_pay)==-(q*a+2*banks*b)
    # Inverse reconstruction of the common shadow-price optimum and the rounding remainder.
    dual=lambda t:q*min(F(a,2)*(1+t),F(a))+banks*F(b,2)*(1-t)
    smooth=max(dual(F(0)),dual(F(1)))
    assert smooth==max(F(q*a),F(q*a+banks*b,2))
    assert 0<=formula-smooth<=F(max(a,b),2)
    old=F(q*a)+F(banks*b,2)
    target=F(q*a+banks*b,2)
    g1=formula-target;g2=F(q*a,2)
    assert 0<=g1<=g2
    C_new=2*(g1+g2)+g2
    C_old=F(5*q*a,2)
    saved=C_old-C_new
    expected_saved=F(a*min(q,banks*b//a))
    assert saved==expected_saved
    assert C_new+saved==C_old
    B_half=q*a+2*banks*b
    assert B_half+C_new>0
    return {'q':q,'bank_copies':banks,'a':a,'b':b,'unit_clients':len(clients),'topics':K,'all_forced_roots':K,'all_terminal_profiles':leaves,'last_action_comparisons_plus_next_IC':comparisons,'complete_strategy_IC_checks':comparisons+root_IC,'root_action':0,'M_exact':str(formula),'one_total_constraint_value':str(smooth),'rounding_remainder':str(formula-smooth),'old_component_bound':str(old),'target_prefix_profits':[str(target),str(target)],'M_second':str(F(q*a)+F(banks*b,2)),'signed_old_repair':str(C_old),'signed_new_repair':str(C_new),'repair_saved':str(saved),'target_half_slack':str(B_half),'target_plus_new_repair':str(B_half+C_new),'full_child_witnesses':witnesses}

if __name__=='__main__':
    params=[(1,1,1),(1,1,2),(1,2,1),(2,2,1),(2,3,1),(2,3,2),(2,1,2,1)]
    rows=[check(*t) for t in params]
    result={'status':'PASS','independence':'Only raw unit interests and Fraction ordered BI; no author or canonical imports','scope':'Exact regression of explicit parameterized product example, not a general proof','records':rows}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','records':[{k:r[k] for k in ('q','a','b','topics','all_terminal_profiles','M_exact','one_total_constraint_value','repair_saved','target_plus_new_repair')} for r in rows]},indent=2))
