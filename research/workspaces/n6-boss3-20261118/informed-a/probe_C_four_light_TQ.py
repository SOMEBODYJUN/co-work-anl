"""Unpaid C four-light-branch necessary LP, one pair pattern first.
All five new anchors are retained; only block5 is old. Not full SPE synthesis.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parent
PATTERN=((0,1),(1,0),(2,3),(3,2))
TYPES=[(block,bits) for block in range(7) for bits in product((0,1),repeat=5)
       if block<6 or any(bits)]
assert len(TYPES)==223

def build(pattern=PATTERN, exact=False):
    nv=len(TYPES)+1
    def vec(fn):return np.array([F(fn(block,bits)) if exact else float(fn(block,bits)) for block,bits in TYPES]+[F(0) if exact else 0.0],dtype=object if exact else float)
    def has(label,block,bits):
        return int(block==label) if isinstance(label,int) else bits[0] if label=='E' else bits[1+label[1]]
    # C actual three-prefix is (one old anchor5, E, E) in arbitrary label order.
    def bg(j,block,bits):return 2*bits[0]+int(block==5)+int(block==j)
    def utility(j,A,Y):
        return vec(lambda b,v:F(has(A,b,v),bg(j,b,v)+has(A,b,v)+has(Y,b,v)) if has(A,b,v) else 0)
    def query_last(j,A,Q):
        return vec(lambda b,v:F(has(Q,b,v),bg(j,b,v)+has(A,b,v)+1) if has(Q,b,v) else 0)
    def f(j,T):return vec(lambda b,v:F(has(T,b,v),bg(j,b,v)+1) if has(T,b,v) else 0)
    def query_H(j,T):return vec(lambda b,v:F(has(T,b,v),bg(j,b,v)+2) if has(T,b,v) else 0)
    rows=[];rhs=[];names=[]
    def le(name,row,cap):rows.append(row);rhs.append(F(cap) if exact else float(cap));names.append(name)
    eq=[vec(lambda b,v:int(b==k)) for k in range(6)]
    for k in range(5):le('extra-cap-'+str(k),vec(lambda b,v:v[k]),1)
    # P_j=(2/3)|E intersect T_j| <=1/3 iff |E intersect T_j|<=1/2.
    for j in range(4):le('light-E-intersection-'+str(j),vec(lambda b,v:int(b==j)*v[0]),F(1,2))
    catalog=list(range(6))+['E']+[('F',k) for k in range(4)]
    E=[vec(lambda b,v:int(b==k)*v[0]) for k in range(5)]
    for j,(a,y) in enumerate(pattern):
        A=('F',a);Y=('F',y);ua=utility(j,A,Y);uy=utility(j,Y,A)
        w=vec(lambda b,v:F(1,2*v[0]+1+has(A,b,v)+has(Y,b,v)) if b==j else 0)
        force=w.copy();force[-1]=-1
        le('branch'+str(j)+'-force-at-most-gamma',force,0)
        le('branch'+str(j)+'-penultimate-7/12',-ua,-F(7,12))
        le('branch'+str(j)+'-last-7/12',-uy,-F(7,12))
        for Q in catalog:le('branch'+str(j)+'-last-query-'+str(Q),query_last(j,A,Q)-uy,0)
        for T in catalog:le('branch'+str(j)+'-penultimate-H-'+str(T),query_H(j,T)-ua,0)
        # All OTHER FOUR new anchors are genuine comparisons, including block4.
        for k in range(5):
            if k==j:continue
            eothers=sum((E[l] for l in range(5) if l not in (j,k)),np.zeros(nv,dtype=object if exact else float))
            le('branch'+str(j)+'-penultimate-true-anchor-'+str(k),
               -ua-F(2,3)*E[k]-F(2,9)*eothers,-1)
        for k,l in product(range(4),repeat=2):
            T=('F',k);Q=('F',l)
            le('branch'+str(j)+'-TQ-'+str(k)+'-'+str(l),f(j,T)+query_last(j,T,Q)-ua,1)
    objective=np.zeros(nv,dtype=object if exact else float);objective[-1]=F(1) if exact else 1
    return objective,np.array(rows),np.array(rhs),np.array(eq),np.array([F(1)]*6,dtype=object) if exact else np.ones(6),names

def run(pattern=PATTERN):
    c,A,b,E,d,names=build(pattern)
    result=linprog(c,A_ub=A,b_ub=b,A_eq=E,b_eq=d,bounds=(0,None),method='highs')
    answer={'scope':'Unpaid necessary relaxation for C, four selected light new anchors, one specified pair mode. Fifth new anchor remains fresh and queryable; not a pure-SPE proof.',
            'pattern':[list(p) for p in pattern],'client_types':len(TYPES),'columns':len(c),
            'inequality_rows':len(b),'success':result.success,'message':result.message}
    if result.success:
        answer.update({'gamma':float(result.fun),'atoms':[{'block':block,'bits':list(bits),'mass':float(x)} for (block,bits),x in zip(TYPES,result.x[:-1]) if x>1e-9],
                       'active_rows':[name for name,s in zip(names,result.ineqlin.residual) if s<1e-8],
                       'minimum_slack':float(min(result.ineqlin.residual))})
    return answer

if __name__=='__main__':
    answer=run()
    (ROOT/'C-four-light-pair-TQ-output.json').write_text(json.dumps(answer,indent=2)+'\n')
    print(json.dumps({k:v for k,v in answer.items() if k not in ('atoms','active_rows')},indent=2))
