"""Construct and directly audit a complete ordered-history product SPE.

The constructor uses elementary backwards induction on expanded unit clients.
The auditor independently replays every alternative at every one of the 91
decision histories. A separate canonical set-valued solver only cross-checks L.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver

OUT=Path(__file__).resolve().parent
LETTERS='ABC'
VECTORS=tuple(product(range(3),repeat=2))
LABELS=tuple(''.join(LETTERS[a] for a in v) for v in VECTORS)
# Component clients b, ab, c, ac0, ac1.
BASE=(frozenset((1,)),frozenset((0,1)),frozenset((2,)),frozenset((0,2)),frozenset((0,2)))
TOPICS=tuple(frozenset(5*k+x for k in range(2) for x,inc in enumerate(BASE) if v[k] in inc) for v in VECTORS)

def payoff(path,role):
    return sum((F(1,sum(x in TOPICS[a] for a in path)) for x in TOPICS[path[role]]),F(0))

def construct():
    policy={}; theta={}
    for a in range(9):
        second_values=[]
        for b in range(9):
            br=max(payoff((a,b,c),2) for c in range(9))
            opts=[c for c in range(9) if payoff((a,b,c),2)==br]
            c=min(opts,key=lambda c:(payoff((a,b,c),1),c))
            policy[(a,b)]=c
            second_values.append(payoff((a,b,c),1))
        theta[a]=max(second_values)
        b=min(range(9),key=lambda b:(-second_values[b],b))
        policy[(a,)]=b
    bb=LABELS.index('BB'); bc=LABELS.index('BC'); ca=LABELS.index('CA')
    assert payoff((bb,bc,ca),1)==theta[bb]==3
    assert payoff((bb,bc,ca),2)==max(payoff((bb,bc,c),2) for c in range(9))
    policy[(bb,)]=bc; policy[(bb,bc)]=ca
    root_pay=[]
    for a in range(9):
        b=policy[(a,)]; c=policy[(a,b)]
        root_pay.append(payoff((a,b,c),0))
    policy[()]=min(range(9),key=lambda a:(-root_pay[a],a))
    return policy,theta,root_pay

def audit(policy):
    # Independent representation: client incidence across all nine labels.
    incidence=[{a for a,t in enumerate(TOPICS) if x in t} for x in range(10)]
    def leaf(h):
        while len(h)<3: h=h+(policy[h],)
        return h
    def u(z,i):
        ans=F(0)
        for inc in incidence:
            if z[i] in inc: ans+=F(1,sum(a in inc for a in z))
        return ans
    rows=[]
    for depth in range(3):
        for h in product(range(9),repeat=depth):
            z=leaf(h); actual=u(z,depth)
            for a in range(9):
                zd=leaf(h+(a,)); slack=actual-u(zd,depth)
                assert slack>=0,(h,a,z,zd,slack)
                rows.append({'history':[LABELS[b] for b in h],'alternative':LABELS[a],'slack':str(slack)})
    z=leaf(())
    return {'decision_histories':len(policy),'comparisons':len(rows),'minimum_slack':str(min(F(r['slack']) for r in rows)),
            'actual_path':[LABELS[a] for a in z],'actual_payoffs':[str(u(z,i)) for i in range(3)],
            'actual_W':len(set().union(*(TOPICS[a] for a in z))), 'all_comparisons':rows}

def main():
    policy,theta,root_pay=construct(); report=audit(policy)
    component=Instance(('A','B','C'),tuple(CustomerType(inc,1) for inc in BASE),3)
    cs=ExactSPESolver(component)
    single_L=min(component.topic_payoff(1,t) for t in cs.outcomes((0,1,0)))
    ctypes=tuple(CustomerType(frozenset(a for a,t in enumerate(TOPICS) if x in t),1) for x in range(10))
    inst=Instance(LABELS,ctypes,3); solver=ExactSPESolver(inst)
    bb=LABELS.index('BB'); h=tuple(int(a==bb) for a in range(9))
    product_L=min(inst.topic_payoff(bb,t) for t in solver.outcomes(h))
    assert single_L==F(3,2) and product_L==F(5,2)
    report.update({'component_L_B':str(single_L),'product_L_BB':str(product_L),'product_theta_after_BB':str(solver.threshold(h)),
                   'root_menu_payoffs':{LABELS[a]:str(v) for a,v in enumerate(root_pay)},
                   'status':'Exact counterexample to additivity of all-continuation L; not a SM or welfare counterexample.'})
    payload={'instance':inst.to_dict(),'policy':[{'history':[LABELS[a] for a in h],'action':LABELS[a]} for h,a in sorted(policy.items())],
             'forced_BB_path':['BB','BC','CA'],'forced_BB_payoffs':['5/2','3','9/2']}
    (OUT/'product_transfer_certificate.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    (OUT/'product_transfer_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='all_comparisons'},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
