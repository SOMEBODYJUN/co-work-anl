"""Definition-level Fraction audit of a fixed-strategy common static Q.

This verifies a finite, explicit coefficient identity for all 63 interest types.
It is not a proof for arbitrary strategies, numbers of players or catalogs.
No imports from the numerical discoverer or canonical SPE solver.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

K=6;N=3
Q={(0,1):F(1,3),(0,2):F(1,3),(0,3):F(1,3)}
# These are coefficients for W/3-E_Q f_B(a), not W-sum_B f_B(a).
LAM={
0:[((),3,F(1,7)),((0,),0,F(4,21)),((0,),1,F(1,6)),((1,),0,F(1,6)),
   ((0,2),0,F(1,14)),((0,2),3,F(2,21)),((1,3),0,F(1,3))],
1:[((),3,F(1,6)),((0,),1,F(1,3)),((3,),1,F(1,12)),((4,),1,F(1,12)),
   ((0,3),1,F(1,4)),((0,4),1,F(1,12))],
2:[((),2,F(1,12)),((),3,F(1,6)),((),4,F(1,12)),((0,),2,F(7,24)),
   ((1,),2,F(1,24)),((3,),2,F(1,24)),((0,3),2,F(3,8)),
   ((0,5),2,F(1,12)),((1,4),0,F(1,24))],
3:[((),3,F(1,3)),((0,),1,F(1,3)),((0,2),3,F(1,3)),((0,3),3,F(1,3))],
4:[((),4,F(1,3)),((0,),1,F(1,3)),((0,2),4,F(1,3))],
5:[((),5,F(1,3)),((0,),1,F(1,3)),((0,2),5,F(1,3)),((0,3),5,F(1,3))]
}

def action(h):
    if len(h)==0:return 0
    if len(h)==1:return 3 if h[0]<3 else 0
    assert len(h)==2
    return next(c for c in (range(3) if h[1]<3 else range(3,6)) if c not in h)

def finish(h):
    while len(h)<N:h=h+(action(h),)
    return h

def rho(mask,a,z):
    return F(1,sum((mask>>b)&1 for b in z)) if (mask>>a)&1 else F(0)

def gamma(mask,h,a):
    return rho(mask,action(h),finish(h))-rho(mask,a,finish(h+(a,)))

def audit():
    rows=[]
    for a in range(K):
        residual={}
        for mask in range(1,1<<K):
            coverage=int(any((mask>>b)&1 for b in finish(())))
            lhs=F(coverage,3)-sum(prob*rho(mask,a,bg+(a,)) for bg,prob in Q.items())
            paid=sum(mult*gamma(mask,h,b) for h,b,mult in LAM[a])
            res=lhs-paid
            assert res>=0,(a,mask,lhs,paid,res)
            if res:residual[mask]=str(res)
        rows.append({'query':a,'nonzero_incentives':len(LAM[a]),'residual':residual})
    return {'scope':'All nonnegative customer masses for this one complete 3-player 6-label strategy cone; not arbitrary strategies',
            'strategy_histories':sum(K**d for d in range(N)),
            'strategy_actions_checked_for_definition':[(list(h),action(h)) for d in range(N) for h in product(range(K),repeat=d)],
            'root':finish(()),'Q':[{ 'background':b,'probability':str(prob)} for b,prob in Q.items()],
            'coefficient_identities_checked':K*((1<<K)-1),'queries':rows,'status':'pass'}

if __name__=='__main__':
    data=audit();print(json.dumps(data,indent=2))
    if '--output' in __import__('sys').argv:
        target=Path(__file__).with_name('group_common_dual_exact.json')
        with target.open('x') as f:json.dump(data,f,indent=2);f.write('\n')
