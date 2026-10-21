"""Probe whether all two-support payoff identities close arbitrary real graphs."""
from fractions import Fraction
from itertools import product,combinations
from pathlib import Path
import argparse,json,random,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,vstack
from search_signed_graphs import compositions,real_strategy

BASE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--trials',type=int,default=200);ap.add_argument('--seed',type=int,default=6611);args=ap.parse_args()
    n,p=3,6;rng=random.Random(args.seed)
    qs=compositions(n,p);vs=[(q,a) for q in qs for a in range(p) if q[a]];vid={v:i for i,v in enumerate(vs)}
    def row(q,a):
        out=np.zeros(len(vs));out[vid[q,a]]=1;return out
    covers={}
    for q in qs:
        A=tuple(a for a in range(p) if q[a])
        if A not in covers:covers[A]=sum(q[a]*row(q,a) for a in A)
    pair=[]
    for a in range(p):
        states=[q for q in qs if q[a]]
        for q in states:
            for r in states:
                if q==r:continue
                kap=max(Fraction(sum(r[c] for c in range(p) if B>>c&1),sum(q[c] for c in range(p) if B>>c&1)) for B in range(1,1<<p) if B>>a&1)
                pair.append(row(q,a)-float(kap)*row(r,a))
    pair=np.array(pair)
    identities=[]
    for q,a in vs:
        A=[b for b in range(p) if q[b]]
        if len(A)!=2:continue
        b=next(b for b in A if b!=a);r,s=q[a],q[b]
        identities.append(n*r*row(q,a)-r*covers[(a,)]-s*(covers[tuple(A)]-covers[(b,)]))
    F=np.array([[Fraction(int(B>>a&1),sum(q[b] for b in range(p) if B>>b&1)) if B>>a&1 else 0 for B in range(1,1<<p)] for q,a in vs],dtype=float)
    best=0
    for trial in range(args.trials):
        if trial%5==0:weights=[int(B&(B-1)==0) for B in range(1,1<<p)]
        else:weights=[rng.randrange(1,10) if rng.random()<.3 else 0 for B in range(1,1<<p)]
        if not any(weights):continue
        actions,terminal,unused=real_strategy(n,p,weights,rng,vid,F)
        graph=np.array([row(terminal[h+(b,)],b)-row(terminal[h],a) for h,a in actions.items() for b in range(p)])
        Aroot=tuple(a for a in range(p) if terminal[()][a]);root=covers[Aroot]
        # The selected cover row equals the terminal sum even with repeated topics,
        # because all two-support identities imply same-support conservation.
        eq=np.vstack([root,identities]);rhs=np.r_[1,np.zeros(len(eq)-1)]
        aub=np.vstack([graph,pair])
        targets=list(combinations(range(p),3));rng.shuffle(targets)
        for A in targets[:3]:
            objective=covers[A]
            sol=linprog(-objective,A_ub=aub,b_ub=np.zeros(len(aub)),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
            value=-sol.fun if sol.success else float('inf') if sol.status==3 else None
            if value is not None and value>best+1e-7:
                best=value;print(json.dumps({'trial':trial,'best':best,'target':A}),flush=True)
            if value is not None and value>2+1e-7:
                payload={'n':n,'p':p,'trial':trial,'seed':args.seed,'target':list(A),'root':list(terminal[()]),'source_customer_weights':weights,'strategy_actions':[{'history':list(h),'action':a} for h,a in sorted(actions.items())],'y':[{'q':list(q),'a':a,'value':str(Fraction(float(sol.x[i])).limit_denominator(10000000))} for i,(q,a) in enumerate(vs)],'value':value}
                (BASE/'all_pair_identities_obstruction_candidate.json').write_text(json.dumps(payload,indent=2)+'\n')
                print('FOUND_ABOVE_TWO',flush=True);return
        if trial%20==19:print(json.dumps({'completed':trial+1,'best':best}),flush=True)

if __name__=='__main__':main()
