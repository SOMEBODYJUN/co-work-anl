"""Numerical diagnostic only: enlarge harmonic coverage to general DR potentials.

Every player's utility is the marginal Phi(q)-Phi(q-e_a). This enlarged class
is deliberately NOT the customer-attraction input class. A witness here would
only identify what cannot follow from DR-submodularity alone.
"""
from __future__ import annotations
import argparse, itertools, json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--k',type=int,default=3)
    ap.add_argument('--n',type=int,default=3)
    ap.add_argument('--trials',type=int,default=200)
    ap.add_argument('--seed',type=int,default=22101)
    ap.add_argument('--no-dr',action='store_true')
    ap.add_argument('--policy',choices=['random','monotone','plateau','cag','groups'],default='random')
    ap.add_argument('--first',type=int,default=0,help='0 means all players; otherwise test this prefix budget')
    ap.add_argument('--query',help='comma-separated rational query weights')
    ap.add_argument('--iterations',type=int,default=5)
    ap.add_argument('--harmonic-diagonals',action='store_true')
    ap.add_argument('--harmonic-repeats',action='store_true')
    ap.add_argument('--third-positive',action='store_true')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args(); k,n=args.k,args.n
    rng=np.random.default_rng(args.seed)
    states=[q for q in itertools.product(range(n+1),repeat=k) if 0<sum(q)<=n]
    index={q:i for i,q in enumerate(states)}; z=np.zeros(len(states))
    def e(q):
        v=z.copy()
        if sum(q):v[index[tuple(q)]]=1
        return v
    def inc(q,a):
        q=list(q);q[a]+=1;return tuple(q)
    def utility(q,a):
        p=list(q);p[a]-=1
        return e(q)-e(p)
    dr=[]
    zero=(0,)*k
    for q in [zero]+states:
        if sum(q)<n:
            for a in range(k):dr.append(e(inc(q,a))-e(q))
        if sum(q)<n-1 and not args.no_dr:
            for a in range(k):
                for b in range(k):
                    dr.append(e(inc(q,a))+e(inc(q,b))-e(q)-e(inc(inc(q,a),b)))
    dr=np.array(dr)
    if args.third_positive:
        third=[]
        for actions in itertools.combinations_with_replacement(range(k),3):
            row=z.copy()
            for bits in itertools.product((0,1),repeat=3):
                q=list(zero)
                for a,yes in zip(actions,bits):q[a]+=yes
                row+=(-1)**(3-sum(bits))*e(q)
            third.append(row)
        dr=np.vstack((dr,third))
    backgrounds=[q for q in states if sum(q)==n-1]
    static=np.array([[e(inc(q,a))-e(q) for a in range(k)] for q in backgrounds])
    norm=sum((e(q) for q in states if sum(q)==n),z.copy())
    extra=[]
    if args.harmonic_diagonals or args.harmonic_repeats:
        for a in range(k):
            for j in range(2,n+1):
                q=[0]*k;q[a]=j
                extra.append(e(q)-sum(1/i for i in range(1,j+1))*e(inc(zero,a)))
    if args.harmonic_repeats:
        assert n==3
        for a in range(k):
            for b in range(k):
                if a!=b:
                    extra.append(6*e(inc(inc(inc(zero,a),a),b))-e(inc(zero,a))+2*e(inc(zero,b))-8*e(inc(inc(zero,a),b)))
    best=0.;summary={'status':'floating diagnostic in an enlarged model, not CAG evidence','args':vars(args).copy(),'best_objective':0.}
    summary['args']['output']=str(args.output)
    for trial in range(args.trials):
        policy={h:int(rng.integers(k)) for d in range(n) for h in itertools.product(range(k),repeat=d)}
        if args.policy=='groups':
            assert n==3 and k==6
            policy[()]=0
            for a in range(k):
                policy[(a,)]=3 if a<3 else 0
                for b in range(k):
                    group=range(3) if b<3 else range(3,6)
                    policy[(a,b)]=next(c for c in group if c not in (a,b))
        elif args.policy!='random':
            phis={zero:0.}
            if args.policy in ('monotone','plateau'):
                for q in sorted(states,key=sum):
                    phis[q]=max(phis[tuple(q[a]-int(a==b) for a in range(k))] for b in range(k) if q[b])+float(rng.integers(0,3) if args.policy=='plateau' else rng.exponential())
            else:
                masks=np.arange(1,1<<k);member=((masks[None,:]>>np.arange(k)[:,None])&1)
                weights=rng.integers(1,10,size=len(masks)).astype(float);weights[rng.random(len(masks))<.7]=0
                harmonic=np.r_[0.,np.cumsum(1/np.arange(1,n+1))]
                for q in states:phis[q]=float(weights@harmonic[np.array(q)@member])
            phivec=np.array([phis[q] for q in states])
            ends={h:h for h in itertools.product(range(k),repeat=n)}
            for d in reversed(range(n)):
                for h in itertools.product(range(k),repeat=d):
                    values=[utility(tuple(ends[h+(a,)].count(b) for b in range(k)),a)@phivec for a in range(k)]
                    bestv=max(values);choices=[a for a in range(k) if values[a]>=bestv-1e-10]
                    a=int(rng.choice(choices));policy[h]=a;ends[h]=ends[h+(a,)]
        terminal={h: h for h in itertools.product(range(k),repeat=n)}
        for d in reversed(range(n)):
            for h in itertools.product(range(k),repeat=d):terminal[h]=terminal[h+(policy[h],)]
        def counts(h):return tuple(h.count(a) for a in range(k))
        gamma=[]
        for h,a in policy.items():
            original=utility(counts(terminal[h]),a)
            for b in range(k):
                if b!=a:gamma.append(original-utility(counts(terminal[h+(b,)]),b))
        gamma=np.array(gamma)
        root=terminal[()];q=counts(root)
        budget=root[:args.first] if args.first else root
        factor=len(budget)
        total=sum((utility(q,a) for a in budget),z.copy())
        pstarts=[np.ones(k)/k,rng.dirichlet(np.ones(k)),rng.dirichlet(np.ones(k)*.15)]
        if args.query:
            from fractions import Fraction
            pstarts=[np.array([float(Fraction(t)) for t in args.query.split(',')])]
        for p in pstarts:
            for iteration in range(args.iterations):
                beta=np.einsum('a,bat->bt',p,static)
                aub=np.vstack((np.c_[-dr,np.zeros(len(dr))],np.c_[-gamma,np.zeros(len(gamma))],np.c_[-beta,np.ones(len(beta))]))
                res=linprog(np.r_[total,-factor],A_ub=aub,b_ub=np.zeros(len(aub)),A_eq=[np.r_[norm,0]]+[np.r_[row,0] for row in extra],b_eq=[1]+[0]*len(extra),bounds=[(None,None)]*len(states)+[(None,None)],method='highs')
                if not res.success:raise RuntimeError(res.message)
                if res.fun<best-1e-9:
                    best=float(res.fun)
                    summary.update(best_objective=best,witness={'trial':trial,'iteration':iteration,'root':root,'p':p.tolist(),'value_lower':float(res.x[-1]),'welfare':float(total@res.x[:-1]),'states':states,'potential':res.x[:-1].tolist(),'policy':{','.join(map(str,h)):a for h,a in policy.items()}})
                    args.output.write_text(json.dumps(summary,indent=2)+'\n')
                    print(json.dumps({'trial':trial,'objective':best,'root':root}),flush=True)
                # Reoptimize the query strategy, retaining the potential.
                matrix=np.einsum('bat,t->ba',static,res.x[:-1])
                sr=linprog(np.r_[np.zeros(k),-1],A_ub=np.c_[-matrix,np.ones(len(matrix))],b_ub=np.zeros(len(matrix)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
                if np.max(np.abs(p-sr.x[:-1]))<1e-10:break
                p=sr.x[:-1]
        if best< -1e-7:break
    summary['completed']=trial+1
    args.output.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'completed':trial+1,'best':best}),flush=True)

if __name__=='__main__':main()
