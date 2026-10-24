"""Finite attacks on an all-input anchored deletion-budget candidate.

Q is a free mixture of backgrounds obtained by deleting one active provider
from one actual terminal. The static ancestor reserve is paid pointwise by
actual ancestors, but no query cap is assumed. This is not a half proof.
"""
from __future__ import annotations
import json, sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver

def matrix(instance,b,z):
    r=instance.players-sum(b)
    deleted=[a for a in range(instance.topic_count) if z[a]>b[a]]
    cols=[]; reserves=[]
    for a in deleted:
        q=list(z);q[a]-=1
        cols.append(tuple(sum((F(c.multiplicity,1+sum(q[t] for t in c.topics)) for c in instance.customers if t0 in c.topics),F(0)) for t0 in range(instance.topic_count)))
        reserves.append(sum((F(c.multiplicity*sum(b[t] for t in c.topics),1+sum(q[t] for t in c.topics)) for c in instance.customers),F(0)))
    return r,deleted,cols,reserves

def budget(instance,b,z,k):
    r,deleted,cols,a=matrix(instance,b,z)
    C=k+r-1
    K=np.array([[float(col[t]) for col in cols] for t in range(instance.topic_count)])
    result=linprog([float(v) for v in a]+[C],A_ub=np.column_stack([K,-np.ones(instance.topic_count)]),b_ub=np.zeros(instance.topic_count),A_eq=[[1]*len(cols)+[0]],b_eq=[1],bounds=[(0,None)]*(len(cols)+1),method='highs')
    if not result.success:raise RuntimeError(result.message)
    lam=[F(float(x)).limit_denominator(10000000) for x in result.x[:-1]]
    lam=[x/sum(lam) for x in lam]
    t=max(sum((lam[j]*cols[j][s] for j in range(len(cols))),F(0)) for s in range(instance.topic_count))
    upper=C*t+sum((lam[j]*a[j] for j in range(len(cols))),F(0))
    rho=[F(max(0,float(-x))).limit_denominator(10000000) for x in result.ineqlin.marginals]
    rho=[C*x/sum(rho) for x in rho]
    lower=min(a[j]+sum((rho[s]*cols[j][s] for s in range(instance.topic_count)),F(0)) for j in range(len(cols)))
    B=sum((F(c.multiplicity*sum(b[t] for t in c.topics),sum(z[t] for t in c.topics)) for c in instance.customers if any(b[t] for t in c.topics)),F(0))
    assert all(x<=B for x in a)
    W=instance.welfare(z)
    return {'prefix':b,'terminal':z,'coefficient':C,'W':W,'OPT_k':None,'lower':str(lower),'upper':str(upper),'gap_lower':str(lower-2*W),'gap_upper':str(upper-2*W),'deleted':deleted,'lambda':list(map(str,lam)),'query_prices':[[str(v) for v in col] for col in cols],'ancestor_reserves':list(map(str,a)),'actual_ancestor_profit':str(B),'dual_rho':list(map(str,rho))}

def main():
    summaries=[];counter=[]
    for f in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
        try: inst=Instance.from_dict(json.loads(f.read_text()))
        except (ValueError,KeyError,TypeError):continue
        if inst.topic_count>7 or inst.players>6 or inst.players<2:continue
        solver=ExactSPESolver(inst);root=(0,)*inst.topic_count
        worst=None;count=0
        # Every root equilibrium outcome, and every fixed-one-root SPE child
        # outcome; no anonymous restriction is imposed on the outcome solver.
        for b in [root]+[tuple(int(a==j) for a in range(inst.topic_count)) for j in range(inst.topic_count)]:
            for z in solver.outcomes(b):
                row=budget(inst,b,z,inst.players)
                count+=1
                if worst is None or F(row['gap_lower'])>F(worst['gap_lower']):worst=row
                if F(row['gap_lower'])>0:
                    row['name']=f.name;row['instance']=inst.to_dict();counter.append(row)
        summaries.append({'name':f.name,'cases':count,'worst':worst})
    out={'scope':'Known existing examples only; weak anchored actual-deletion cap J<=2W is under attack. No finite pass proves it. Exact rational primal/dual bounds are reconstructed after floating LP.','summaries':summaries,'strict_failures':counter}
    dest=Path(__file__).with_name('anchored_deletion_probe.json');dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'instances':len(summaries),'cases':sum(x['cases'] for x in summaries),'strict_failures':len(counter),'max_gap':max((F(x['worst']['gap_lower']) for x in summaries),default=0).__str__(),'output':str(dest.relative_to(ROOT))}))
if __name__=='__main__':main()
