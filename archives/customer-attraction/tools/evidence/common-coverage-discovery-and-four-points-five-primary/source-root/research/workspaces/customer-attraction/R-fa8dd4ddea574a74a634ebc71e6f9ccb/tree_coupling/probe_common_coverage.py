"""Exploratory LPs; floating output is not a theorem or SPE certificate."""
from fractions import Fraction
from itertools import product, combinations
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[4]
SOURCE=ROOT/'research/workspaces/customer-attraction/R-d7f409d6a5914bdeb09875ab32618466/tree_duality/pair_dilution_obstruction.json'

def setup():
    obj=json.loads(SOURCE.read_text())
    n,p=obj['n'],obj['p']
    actions={tuple(x['history']):x['action'] for x in obj['strategy_actions']}
    terminals={}
    for d in range(n,-1,-1):
        for h in product(range(p),repeat=d):
            terminals[h]=tuple(h.count(a) for a in range(p)) if d==n else terminals[h+(actions[h],)]
    qs=sorted(set(terminals[h] for h in product(range(p),repeat=n)))
    vertices=[(q,a) for q in qs for a in range(p) if q[a]]
    vid={v:i for i,v in enumerate(vertices)}
    cols=len(vertices)
    graph=[]
    for h,a in actions.items():
        for b in range(p):
            r=np.zeros(cols);r[vid[terminals[h+(b,)],b]]+=1;r[vid[terminals[h],a]]-=1
            graph.append(r)
    pair=[]
    for q,a in vertices:
        for r,b in vertices:
            if a!=b or q==r:continue
            kap=max(Fraction(sum(r[c] for c in range(p) if mask>>c&1),sum(q[c] for c in range(p) if mask>>c&1)) for mask in range(1,1<<p) if mask>>a&1)
            row=np.zeros(cols);row[vid[q,a]]=1;row[vid[r,a]]-=float(kap);pair.append(row)
    total={}
    equal=[]
    for q in qs:
        row=np.zeros(cols)
        for a in range(p):
            if q[a]:row[vid[q,a]]=q[a]
        support=tuple(a for a in range(p) if q[a])
        if support in total:equal.append(row-total[support])
        else:total[support]=row
    root=np.zeros(cols)
    for a in range(p):
        if terminals[()][a]:root[vid[terminals[()],a]]=terminals[()][a]
    opt=tuple(obj['portfolio'].count(a) for a in range(p))
    objective=np.zeros(cols)
    for a in range(p):
        if opt[a]:objective[vid[opt,a]]=opt[a]
    types=list(range(1,1<<p))
    mat=np.array([[int(B>>a&1)/sum(q[b] for b in range(p) if B>>b&1) if B>>a&1 else 0 for B in types] for q,a in vertices])
    return obj,vertices,np.array(graph),np.array(pair),np.array(equal),root,objective,mat

def main():
    obj,vs,graph,pair,equal,root,objective,mat=setup()
    constraints=np.vstack([graph,pair])
    reports=[]
    for mode in ['pair','same_support','signed_customer','nonnegative_customer']:
        if mode in ['pair','same_support']:
            eq=np.vstack([root,equal]) if mode=='same_support' else root[None,:]
            rhs=np.r_[1,np.zeros(len(eq)-1)]
            sol=linprog(-objective,A_ub=constraints,b_ub=np.zeros(len(constraints)),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
            y=sol.x
        else:
            bounds=(0,None) if mode=='nonnegative_customer' else (None,None)
            sol=linprog(-(objective@mat),A_ub=np.vstack([constraints@mat,-mat]),b_ub=np.zeros(len(constraints)+len(mat)),A_eq=(root@mat)[None,:],b_eq=[1],bounds=bounds,method='highs')
            y=mat@sol.x
        report={'mode':mode,'success':sol.success,'status':sol.message,'value':float(objective@y) if sol.success else None}
        reports.append(report)
        if sol.success:
            payload={'n':obj['n'],'p':obj['p'],'mode':mode,'objective':report['value'],'strategy_actions':obj['strategy_actions'],'portfolio':obj['portfolio'],'y':[{'q':list(q),'a':a,'value':str(Fraction(float(y[i])).limit_denominator(10000000))} for i,(q,a) in enumerate(vs)]}
            if mode in ['signed_customer','nonnegative_customer']:
                payload['customer_weights']=[{'mask':B,'weight':str(Fraction(float(v)).limit_denominator(10000000))} for B,v in enumerate(sol.x,1) if abs(v)>1e-10]
            (BASE/('probe_'+mode+'.json')).write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps(reports,indent=2))

if __name__=='__main__':main()
