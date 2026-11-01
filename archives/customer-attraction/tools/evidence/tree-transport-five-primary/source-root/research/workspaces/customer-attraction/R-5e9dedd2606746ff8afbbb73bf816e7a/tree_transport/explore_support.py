"""Exploratory LP: graph + dilution + support efficiency; exact-check candidate."""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
SOURCE=ROOT/'research/workspaces/customer-attraction/R-d7f409d6a5914bdeb09875ab32618466/tree_duality/pair_dilution_obstruction.json'

def run(mode='support'):
    src=json.loads(SOURCE.read_text());m,p=src['n'],src['p']
    pol={tuple(z['history']):z['action'] for z in src['strategy_actions']}
    leaves={}
    for depth in range(m,-1,-1):
        for h in product(range(p),repeat=depth):
            leaves[h]=tuple(h.count(a) for a in range(p)) if depth==m else leaves[h+(pol[h],)]
    vertices=sorted({(q,a) for q in leaves.values() for a in range(p) if q[a]})
    ix={v:i for i,v in enumerate(vertices)};V=len(vertices)
    def vector(entries):
        z=[Q(0) for _ in range(V)]
        for v,c in entries:z[ix[v]]+=c
        return z
    ub=[];eq=[]
    for h,a in pol.items():
        for b in range(p):
            ub.append(vector([((leaves[h+(b,)],b),Q(1)),((leaves[h],a),Q(-1))]))
    for q,a in vertices:
        for r,b in vertices:
            if a!=b or q==r:continue
            k=max(Q(sum(r[c] for c in range(p) if t>>c&1),sum(q[c] for c in range(p) if t>>c&1)) for t in range(1,1<<p) if t>>a&1)
            ub.append(vector([((q,a),Q(1)),((r,a),-k)]))
    cov={}
    for q in sorted({q for q,a in vertices}):
        s=frozenset(a for a in range(p) if q[a]);z=vector([((q,a),Q(q[a])) for a in s])
        if s in cov:eq.append([a-b for a,b in zip(z,cov[s])])
        else:cov[s]=z
    if mode in ('monotone','submodular','image_submodular'):
        sets=list(cov)
        cov[frozenset()]=[Q(0)]*V
        for a in sets:
            for b in sets:
                if a<=b:ub.append([x-y for x,y in zip(cov[a],cov[b])])
                if mode in ('submodular','image_submodular') and a|b in cov:ub.append([x+y-z-w for x,y,z,w in zip(cov[a|b],cov[a&b],cov[a],cov[b])])
    root=leaves[()];O=frozenset(src['portfolio'])
    W=cov[frozenset(a for a in range(p) if root[a])];o=cov[O]
    A=np.array(ub,dtype=float);E=np.array(eq+[W],dtype=float)
    image=mode.startswith('image')
    if image:
        F=[[Q(1,sum(q[c]for c in range(p)if t>>c&1))if t>>a&1 else Q(0)for t in range(1,1<<p)]for q,a in vertices]
        M=np.array(F,dtype=float)
        AA=np.vstack([A@M,-M]);EE=E@M
        res=linprog(-np.array(o,dtype=float)@M,A_ub=AA,b_ub=np.zeros(len(AA)),A_eq=EE,b_eq=np.array([0]*len(eq)+[1]),bounds=(None,None),method='highs')
    else:
        res=linprog(-np.array(o,dtype=float),A_ub=A,b_ub=np.zeros(len(A)),A_eq=E,b_eq=np.array([0]*len(eq)+[1]),bounds=(0,None),method='highs')
    print(mode,res.message, None if res.x is None else -res.fun,flush=True)
    if res.x is None:return
    for limit in [100,10000,1000000,1000000000]:
        v=[Q(float(x)).limit_denominator(limit) for x in res.x]
        y=[sum(a*b for a,b in zip(row,v))for row in F]if image else v
        dot=lambda z:sum(a*b for a,b in zip(z,y))
        if min(y)>=0 and all(dot(z)<=0 for z in ub) and all(dot(z)==0 for z in eq) and dot(W)==1:break
    else:
        print('exact recovery failed');return
    out={'mode':mode,'m':m,'p':p,'vertices':[{'q':q,'a':a,'y':str(y[i])}for i,(q,a) in enumerate(vertices)],'value':str(dot(o)),'inequalities':len(ub),'equalities':len(eq),'root':root,'portfolio':src['portfolio'],'strategy_actions':src['strategy_actions']}
    if image:out['signed_customers']=[{'mask':i+1,'weight':str(a)}for i,a in enumerate(v)if a]
    path=Path(__file__).parent/f'{mode}_candidate.json';path.write_text(json.dumps(out,indent=2)+'\n');print('exact',out['value'])

if __name__=='__main__':
    import sys
    run(sys.argv[1] if len(sys.argv)>1 else 'support')
