"""One existing-input diagnostic of pair >= 2*v_(r+1)(background).
The extra security game has r static competitor slots, never r-1.
"""
from pathlib import Path
import json,sys
from fractions import Fraction as F
from itertools import product
import numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance,ExactSPESolver
from customer_attraction.exact import _increment

def comps(n,k):
    if k==1:yield(n,);return
    for i in range(n+1):
        for q in comps(n-i,k-1):yield(i,)+q

def security(ins,background,r):
    n=ins.topic_count;rows=[]
    for q in comps(r,n):
        rows.append(tuple(sum((F(c.multiplicity,1+sum((background[a]+q[a]) for a in c.topics)) for c in ins.customers if t in c.topics),F()) for t in range(n)))
    M=np.array(rows,dtype=float)
    lp=linprog(np.r_[np.zeros(n),-1.],A_ub=np.c_[-M,np.ones(len(rows))],b_ub=np.zeros(len(rows)),A_eq=np.array([np.r_[np.ones(n),0.]]),b_eq=[1.],bounds=[(0,None)]*n+[(None,None)],method='highs')
    assert lp.success
    p=tuple(F(float(v)).limit_denominator(10**6) for v in lp.x[:n]);p=tuple(v/sum(p) for v in p)
    val=min(sum((a*b for a,b in zip(p,row)),F()) for row in rows)
    return val,p,len(rows)

def minpair(ins,sol,background):
    floor=sol.threshold(background);best=None
    for z in sol.outcomes(background):
        pay=ins.topic_payoffs(z)
        for a in range(ins.topic_count):
            if not z[a] or pay[a]<floor:continue
            child=_increment(background,a)
            if z not in sol.outcomes(child):continue
            fl=sol.threshold(child)
            for b in range(ins.topic_count):
                if not z[b] or pay[b]<fl or z not in sol.outcomes(_increment(child,b)):continue
                item=(pay[a]+pay[b],a,b,z)
                if best is None or item<best:best=item
    assert best is not None
    return best

if __name__=='__main__':
    source=Path(sys.argv[1]);obj=json.loads(source.read_text());ins=Instance.from_dict(obj.get('instance',obj));sol=ExactSPESolver(ins)
    sol.outcomes();best=None;total=0;rows=[]
    # All legal backgrounds with >=3 remaining; r=2 is already an established general case.
    for depth in range(ins.players-2):
        for bg in comps(depth,ins.topic_count):
            r=ins.players-depth;pair,a,b,z=minpair(ins,sol,bg);val,p,count=security(ins,bg,r)
            row={'background':list(bg),'remaining':r,'pair_min':str(pair),'pair_actions':[a,b],'terminal':list(z),'security_lower':str(val),'query':list(map(str,p)),'static_count':count,'margin_pair_minus_2lower':str(pair-2*val)}
            rows.append(row);total+=1
            if best is None or pair-2*val<F(best['margin_pair_minus_2lower']):best=row;print(json.dumps({'checked':total,'best':best}),flush=True)
            if pair<2*val:
                print(json.dumps({'candidate':'pair >= 2v_(r+1)(b)','source':str(source),'separation':row}),flush=True);sys.exit(0)
    print(json.dumps({'candidate':'pair >= 2v_(r+1)(b)','source':str(source),'backgrounds_checked':total,'best':best,'rows':rows,'scope':'One existing-input targeted finite diagnostic, no universal positive evidence.'}),flush=True)
