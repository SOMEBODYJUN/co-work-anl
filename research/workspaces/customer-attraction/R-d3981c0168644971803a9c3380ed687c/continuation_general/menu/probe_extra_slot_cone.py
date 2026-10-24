"""Single-formal-tree attack on the universal extra-slot aggregate candidate.

Exact statement tested: sum_i p^T K_i p <= W for all p and every full SPE.
LP proposes rational customer reweightings; every proposed witness is checked
against every ordered-history SPE inequality using Fraction arithmetic.
"""
import itertools,json,pathlib,math
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog

OUT=pathlib.Path(__file__).resolve().parent

def main():
    k=6;m=3;types=range(1,1<<k)
    def action(h):
        if not h:return 0
        if len(h)==1:return 3 if h[0]<3 else 0
        group=range(3) if h[1]<3 else range(3,6)
        return next(a for a in group if a not in h)
    def end(h):
        while len(h)<m:h=h+(action(h),)
        return h
    def coef(t,a,z,extra=0):
        return F(int(bool(t&(1<<a))),extra+sum(bool(t&(1<<v)) for v in z)) if t&(1<<a) else F()
    histories=[h for d in range(m) for h in itertools.product(range(k),repeat=d)]
    rows=[[coef(t,action(h),end(h))-coef(t,a,end(h+(a,))) for t in types] for h in histories for a in range(k)]
    G=np.array([[float(v) for v in row] for row in rows]);z=end(())
    Z=[[end(z[:i]+(a,)) for a in range(k)] for i in range(m)]
    ps=[]
    for mask in types:
        support=[a for a in range(k) if mask&(1<<a)]
        ps.append([F(int(a in support),len(support)) for a in range(k)])
    for a,b in itertools.combinations(range(k),2):
        for q in (F(1,4),F(3,4)):
            ps.append([q if v==a else 1-q if v==b else F() for v in range(k)])
    best=None
    for p in ps:
        obj=[sum((p[t]*p[a]*coef(mask,t,Z[i][a],1) for i,t,a in itertools.product(range(m),range(k),range(k))),F())-int(any(mask&(1<<a) for a in z)) for mask in types]
        result=linprog([-float(v) for v in obj],A_ub=-G,b_ub=np.zeros(len(rows)),A_eq=np.ones((1,len(types))),b_eq=[1],bounds=(0,None),method='highs')
        if not result.success:continue
        gap=-result.fun
        if best is None or gap>best['gap_float']:
            w=[F(float(v)).limit_denominator(10000000) for v in result.x];w=[v/sum(w) for v in w]
            slacks=[sum((c*v for c,v in zip(row,w)),F()) for row in rows]
            exact=sum((c*v for c,v in zip(obj,w)),F())
            den=math.lcm(*(v.denominator for v in w))
            best={'gap_float':gap,'exact_gap':str(exact),'min_spe_slack':str(min(slacks)),'p':[str(v) for v in p],'customers':[[t,int(v*den)] for t,v in zip(types,w) if v],'customer_scale':den,'exact_valid':min(slacks)>=0}
    report={'candidate':'sum_i p^T K_i p <= W, K_i full m-slot extra insertion','scope':'one fixed complete 3-player/6-action formal strategy and 93 specified queries; no all-input inference','best':best}
    (OUT/'extra_slot_cone_diagnostic.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
