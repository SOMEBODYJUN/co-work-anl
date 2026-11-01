"""Exploratory real-SPE graph / signed common-client relaxation search."""
from fractions import Fraction
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
import argparse,json,random,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,vstack

BASE=Path(__file__).resolve().parent

def compositions(n,p):
    if p==1:return [(n,)]
    return [(i,)+q for i in range(n+1) for q in compositions(n-i,p-1)]

def prepare(n,p):
    qs=compositions(n,p); qid={q:i for i,q in enumerate(qs)}
    vs=[(q,a) for q in qs for a in range(p) if q[a]];vid={v:i for i,v in enumerate(vs)}
    types=list(range(1,1<<p))
    den=np.array([[sum(q[b] for b in range(p) if B>>b&1) for B in types] for q in qs])
    F=np.array([[int(B>>a&1)/den[qid[q],j] if B>>a&1 else 0 for j,B in enumerate(types)] for q,a in vs])
    universal=[]
    for a in range(p):
        inds=[i for i,(q,b) in enumerate(vs) if a==b]
        for i in inds:
            q,_=vs[i]
            for j in inds:
                if i==j:continue
                r,_=vs[j]
                # Max ratio is reached at a prefix of descending r_b/q_b;
                # zero-q positive-r terms are included for free.
                num=r[a]+sum(r[c] for c in range(p) if c!=a and not q[c]);denom=q[a]
                kap=Fraction(num,denom)
                order=sorted((c for c in range(p) if c!=a and q[c]),key=lambda c:Fraction(r[c],q[c]),reverse=True)
                for c in order:
                    num+=r[c];denom+=q[c];kap=max(kap,Fraction(num,denom))
                universal.append(F[i]-float(kap)*F[j])
    universal=np.vstack([universal,-F])
    # Remove numerically zero and duplicate exact-scale rows for speed.
    universal=universal[np.max(np.abs(universal),axis=1)>1e-10]
    universal=np.unique(np.round(universal,13),axis=0)
    cover={A:np.array([int(any(B>>a&1 for a in A)) for B in types],dtype=float) for A in combinations(range(p),min(n,p))}
    return qs,vs,vid,F,universal,cover

def real_strategy(n,p,weights,rng,vid,F):
    # Exact utility table; full histories choose independently on all exact ties.
    utility={v:sum(Fraction(int(B>>v[1]&1)*w,sum(v[0][b] for b in range(p) if B>>b&1)) for B,w in enumerate(weights,1) if w and B>>v[1]&1) for v in vid}
    actions={};terminal={}
    for d in range(n,-1,-1):
        for h in product(range(p),repeat=d):
            if d==n:terminal[h]=tuple(h.count(a) for a in range(p));continue
            scores=[utility[terminal[h+(a,)],a] for a in range(p)]
            best=max(scores);a=rng.choice([a for a in range(p) if scores[a]==best])
            actions[h]=a;terminal[h]=terminal[h+(a,)]
    graph=np.array([F[vid[terminal[h+(b,)],b]]-F[vid[terminal[h],a]] for h,a in actions.items() for b in range(p)])
    return actions,terminal,graph

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=3);ap.add_argument('--p',type=int,default=6);ap.add_argument('--trials',type=int,default=100);ap.add_argument('--seed',type=int,default=9451);args=ap.parse_args()
    n,p=args.n,args.p;rng=random.Random(args.seed)
    qs,vs,vid,F,universal,cover=prepare(n,p)
    best=0;report=[];start=time.time()
    print(json.dumps({'n':n,'p':p,'vertices':len(vs),'universal_constraints':len(universal),'types':(1<<p)-1}),flush=True)
    for trial in range(args.trials):
        # Sparse / dense mixtures, repeated singleton baselines and strong overlaps.
        weights=[rng.randrange(1,30) if rng.random()<rng.choice([.12,.3,.65]) else 0 for B in range(1,1<<p)]
        for a in range(p):weights[(1<<a)-1]+=rng.randrange(0,4)
        if not any(weights):continue
        actions,terminal,graph=real_strategy(n,p,weights,rng,vid,F)
        root=np.array([int(any(terminal[()][a] and B>>a&1 for a in range(p))) for B in range(1,1<<p)],dtype=float)
        aub=np.vstack([universal,graph]);rhs=np.zeros(len(aub))
        # Try actual optimum target first, then a random target; every graph is real SPE.
        actual=lambda A:sum(weights[B-1]*v for B,v in enumerate(cover[A],1))
        A=max(cover,key=actual)
        targets=[A]
        if len(cover)>1:targets.append(rng.choice(list(cover)))
        for A in targets:
            sol=linprog(-cover[A],A_ub=aub,b_ub=rhs,A_eq=root[None,:],b_eq=[1],bounds=(None,None),method='highs')
            value=-sol.fun if sol.success else (float('inf') if sol.status==3 else None)
            if value is not None and value>best+1e-7:
                best=value
                print(json.dumps({'trial':trial,'target':A,'best':value,'seconds':round(time.time()-start,2)}),flush=True)
                payload={'n':n,'p':p,'seed':args.seed,'trial':trial,'target':A,'value':value,'actual_customer_weights':weights,'strategy_actions':[{'history':list(h),'action':a} for h,a in sorted(actions.items())]}
                if sol.success:payload['signed_customer_weights']=[{'mask':B,'weight':str(Fraction(float(v)).limit_denominator(10000000))} for B,v in enumerate(sol.x,1) if abs(v)>1e-9]
                (BASE/f'signed_search_n{n}_p{p}_best.json').write_text(json.dumps(payload,indent=2)+'\n')
            if value is not None and value>2+1e-6:
                print('FOUND_ABOVE_TWO',flush=True);return
        if trial%20==19:print(json.dumps({'completed':trial+1,'best':best,'seconds':round(time.time()-start,2)}),flush=True)
    print(json.dumps({'completed':args.trials,'best':best,'seconds':round(time.time()-start,2)}),flush=True)

if __name__=='__main__':main()
