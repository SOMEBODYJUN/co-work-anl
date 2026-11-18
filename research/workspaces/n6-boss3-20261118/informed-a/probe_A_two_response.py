"""One common-response control and one 2+2 A mode; necessary rows only.
Fourth-player full three-tail IC is intentionally unpaid. Not SPE synthesis.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parent
TYPES=[(b,v) for b in range(7) for v in product((0,1),repeat=5) if b<6 or any(v)]
COMMON=((0,1,2),(0,2,1),(0,3,4),(0,4,3))
TWO_TWO=((0,1,2),(0,2,1),(1,3,4),(1,4,3))

def run(pattern):
    nv=len(TYPES)+1
    def vec(fn):return np.array([float(fn(b,v)) for b,v in TYPES]+[0.0])
    def has(L,b,v):return int(b==L) if isinstance(L,int) else v[L[1]]
    def p(j,b):return int(4<=b<6)+int(b==j)
    def payoff(j,who,triple):
        return vec(lambda b,v:F(has(who,b,v),p(j,b)+sum(v[k] for k in triple)) if has(who,b,v) else 0)
    def last_query(j,e,a,Q):
        return vec(lambda b,v:F(has(Q,b,v),p(j,b)+v[e]+v[a]+1) if has(Q,b,v) else 0)
    def H4(j,Q):return vec(lambda b,v:F(has(Q,b,v),p(j,b)+3) if has(Q,b,v) else 0)
    def H5(j,e,Q):return vec(lambda b,v:F(has(Q,b,v),p(j,b)+v[e]+2) if has(Q,b,v) else 0)
    def f5(j,e,T):return vec(lambda b,v:F(has(T,b,v),p(j,b)+v[e]+1) if has(T,b,v) else 0)
    rows=[];rhs=[];names=[]
    def le(name,row,cap):rows.append(row);rhs.append(float(cap));names.append(name)
    eq=[vec(lambda b,v:int(b==k)) for k in range(6)]
    for k in range(5):le('extra-cap-'+str(k),vec(lambda b,v:v[k]),1)
    labels=list(range(6))+[('F',k) for k in range(5)]
    for j,(e,a,y) in enumerate(pattern):
        assert len({e,a,y})==3
        E=('F',e);A=('F',a);Y=('F',y)
        u4=payoff(j,E,(e,a,y));u5=payoff(j,A,(e,a,y));u6=payoff(j,Y,(e,a,y))
        w=vec(lambda b,v:F(1,1+v[e]+v[a]+v[y]) if b==j else 0)
        w[-1]=-1
        le('branch'+str(j)+'-force-at-most-gamma',w,0)
        le('branch'+str(j)+'-fourth-clean-1/2',-u4,-F(1,2))
        le('branch'+str(j)+'-fifth-7/12',-u5,-F(7,12))
        le('branch'+str(j)+'-sixth-7/12',-u6,-F(7,12))
        for Q in labels:le('branch'+str(j)+'-fourth-H-'+str(Q),H4(j,Q)-u4,0)
        for Q in labels:le('branch'+str(j)+'-last-query-'+str(Q),last_query(j,e,a,Q)-u6,0)
        for Q in labels:le('branch'+str(j)+'-fifth-H-'+str(Q),H5(j,e,Q)-u5,0)
        ej=[vec(lambda b,v:int(b==k)*v[e]) for k in range(4)]
        for k in range(4):
            if k==j:continue
            other=sum((ej[l] for l in range(4) if l not in (j,k)),np.zeros(nv))
            le('branch'+str(j)+'-fifth-anchor-deficit-'+str(k),-u5-F(1,2)*ej[k]-F(1,4)*other,-1)
        for k,l in product(range(5),repeat=2):
            T=('F',k);Q=('F',l)
            le('branch'+str(j)+'-fifth-TQ-'+str(k)+'-'+str(l),f5(j,e,T)+last_query(j,e,k,Q)-u5,1)
    c=np.zeros(nv);c[-1]=1
    z=linprog(c,A_ub=np.array(rows),b_ub=np.array(rhs),A_eq=np.array(eq),b_eq=np.ones(6),bounds=(0,None),method='highs')
    answer={'pattern':[list(p) for p in pattern],'scope':'One A three-distinct-extra pattern; necessary relaxation with fourth clean-prefix floor/H only, no complete fourth three-tail deviations.',
            'types':len(TYPES),'columns':nv,'inequality_rows':len(rows),'success':z.success,'message':z.message}
    if z.success:
        answer.update({'gamma':float(z.fun),'atoms':[{'block':b,'bits':list(v),'mass':float(x)} for (b,v),x in zip(TYPES,z.x[:-1]) if x>1e-9],
                       'active_rows':[name for name,s in zip(names,z.ineqlin.residual) if s<1e-8]})
    return answer

if __name__=='__main__':
    out={'common_response_control':run(COMMON),'two_two_response':run(TWO_TWO)}
    (ROOT/'A-two-response-probe-output.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({name:{k:v for k,v in result.items() if k not in ('atoms','active_rows')} for name,result in out.items()},indent=2))
