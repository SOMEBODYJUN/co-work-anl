"""Exploratory LP in a larger support-budget DR game class, never CAG evidence.

Phi is represented by a support set value W using the exact budget recurrence
|q|Phi(q)=W(supp(q))+sum_a q_a Phi(q-e_a).  The LP retains all monotone and
DR inequalities for Phi and all ordered-history comparisons of one policy.
"""
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=4)
    ap.add_argument('--k',type=int,default=6);ap.add_argument('--trials',type=int,default=100)
    ap.add_argument('--iterations',type=int,default=4);ap.add_argument('--seed',type=int,default=271)
    ap.add_argument('--policy',choices=['cag','submod','random','groups'],default='cag')
    ap.add_argument('--w-monotone',action='store_true');ap.add_argument('--w-submodular',action='store_true')
    ap.add_argument('--alternating',action='store_true');ap.add_argument('--factor',type=float)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    n,k=args.n,args.k;rng=np.random.default_rng(args.seed)
    masks=[t for t in range(1,1<<k) if t.bit_count()<=n]
    mi={t:j for j,t in enumerate(masks)};d=len(masks);zero=(0,)*k
    qs=sorted((q for q in itertools.product(range(n+1),repeat=k) if sum(q)<=n),key=sum)
    def inc(q,a):return tuple(v+int(a==b) for b,v in enumerate(q))
    def dec(q,a):return tuple(v-int(a==b) for b,v in enumerate(q))
    def support(q):return sum((1<<a) for a,v in enumerate(q) if v)
    phi={zero:np.zeros(d)}
    for q in qs[1:]:
        v=np.zeros(d);v[mi[support(q)]]=1
        for a,c in enumerate(q):
            if c:v+=c*phi[dec(q,a)]
        phi[q]=v/sum(q)
    util={(q,a):phi[q]-phi[dec(q,a)] for q in qs for a,c in enumerate(q) if c}
    dr=[]
    for q in qs:
        if sum(q)<n:
            for a in range(k):dr.append(phi[inc(q,a)]-phi[q])
        if sum(q)<n-1:
            for a in range(k):
                for b in range(a,k):
                    dr.append(phi[inc(q,a)]+phi[inc(q,b)]-phi[q]-phi[inc(inc(q,a),b)])
    def unit(t):
        v=np.zeros(d)
        if t:v[mi[t]]=1
        return v
    if args.w_monotone or args.w_submodular:
        for t in [0]+masks:
            if t.bit_count()<n:
                for a in range(k):
                    if not (t>>a)&1:dr.append(unit(t|(1<<a))-unit(t))
    if args.w_submodular:
        for t in [0]+masks:
            if t.bit_count()<n-1:
                for a,b in itertools.combinations([a for a in range(k) if not (t>>a)&1],2):
                    dr.append(unit(t|(1<<a))+unit(t|(1<<b))-unit(t)-unit(t|(1<<a)|(1<<b)))
    if args.alternating:
        for order in range(3,n+1):
            for q in qs:
                if sum(q)+order>n:continue
                for acts in itertools.combinations_with_replacement(range(k),order):
                    row=np.zeros(d)
                    for bits in itertools.product((0,1),repeat=order):
                        at=q
                        for a,yes in zip(acts,bits):
                            if yes:at=inc(at,a)
                        row+=(-1)**(order-sum(bits))*phi[at]
                    dr.append((-1)**(order+1)*row)
    dr=np.array(dr)
    hist={j:list(itertools.product(range(k),repeat=j)) for j in range(n+1)}
    counts={h:tuple(h.count(a) for a in range(k)) for j in hist for h in hist[j]}
    backgrounds=[q for q in qs if sum(q)==n-1]
    static=np.array([[phi[inc(q,a)]-phi[q] for a in range(k)] for q in backgrounds])
    norm=np.array([float(t.bit_count()==1) for t in masks]);summary=dict(status='EXPLORATORY_LARGER_MODEL_NOT_CAG',args=vars(args).copy(),best=0.)
    summary['args']['output']=str(args.output);best=0.
    types=np.arange(1,1<<k);membership=((types[None,:]>>np.arange(k)[:,None])&1)
    for trial in range(args.trials):
        if args.policy=='random':policy={h:int(rng.integers(k)) for j in range(n) for h in hist[j]}
        elif args.policy=='groups':
            assert n==3 and k==6
            policy={():0}
            for a in range(k):
                policy[(a,)]=3 if a<3 else 0
                for b in range(k):policy[(a,b)]=next(c for c in (range(3) if b<3 else range(3,6)) if c not in (a,b))
        else:
            wt=rng.integers(1,20,size=len(types)).astype(float);wt[rng.random(len(types))<.7]=0
            if args.policy=='submod':
                cap=rng.integers(1,k+1,size=len(types))
                W=np.array([float(wt@np.minimum(cap,np.array([int(t&int(s)).bit_count() for s in types]))) for t in masks])
            else:W=np.array([float(wt@((types&t)!=0)) for t in masks])
            ends={h:h for h in hist[n]};policy={}
            for j in reversed(range(n)):
                for h in hist[j]:
                    vals=[util[(counts[ends[h+(a,)]],a)]@W for a in range(k)]
                    mx=max(vals);choices=np.flatnonzero(np.array(vals)>=mx-1e-9)
                    a=int(rng.choice(choices));policy[h]=a;ends[h]=ends[h+(a,)]
        ends={h:h for h in hist[n]}
        for j in reversed(range(n)):
            for h in hist[j]:ends[h]=ends[h+(policy[h],)]
        G=[]
        for h,a in policy.items():
            original=util[(counts[ends[h]],a)]
            for b in range(k):
                if b!=a:G.append(original-util[(counts[ends[h+(b,)]],b)])
        G=np.array(G);root=ends[()];total=np.zeros(d);total[mi[support(counts[root])]]=1
        pstarts=[np.ones(k)/k,rng.dirichlet(np.ones(k)*.2)]
        for p in pstarts:
            for iteration in range(args.iterations):
                beta=np.einsum('a,bat->bt',p,static)
                A=np.vstack((np.c_[-dr,np.zeros(len(dr))],np.c_[-G,np.zeros(len(G))],np.c_[-beta,np.ones(len(beta))]))
                lp=linprog(np.r_[total,-(args.factor if args.factor is not None else n)],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[norm,0]],b_eq=[1],bounds=[(None,None)]*(d+1),method='highs')
                if not lp.success:raise RuntimeError(lp.message)
                if lp.fun<best-1e-9:
                    best=float(lp.fun);summary.update(best=best,witness=dict(trial=trial,iteration=iteration,root=root,p=p.tolist(),value_lower=float(lp.x[-1]),welfare=float(total@lp.x[:-1]),masks=masks,W=lp.x[:-1].tolist(),policy={','.join(map(str,h)):a for h,a in policy.items()}))
                    args.output.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(dict(trial=trial,best=best,root=root)),flush=True)
                matrix=np.einsum('bat,t->ba',static,lp.x[:-1])
                sr=linprog(np.r_[np.zeros(k),-1],A_ub=np.c_[-matrix,np.ones(len(matrix))],b_ub=np.zeros(len(matrix)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
                if np.max(np.abs(sr.x[:-1]-p))<1e-9:break
                p=sr.x[:-1]
        if best< -1e-7:break
        if (trial+1)%10==0:print(json.dumps(dict(completed=trial+1,best=best)),flush=True)
    summary['completed']=trial+1;args.output.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(dict(completed=trial+1,best=best)),flush=True)


if __name__=='__main__':main()
