"""Attack a static floor-protection candidate, not an SPE search.

Candidate: at threshold w_r(b), some root action cannot have payoff below w
when each of the other r-1 providers earns at least w. Numerical discovery only.
"""
import argparse, json, random, time
from pathlib import Path
import numpy as np
from background_cone_attack import Game
from fractional_minmax_probe import value


def trial(g, w):
    val, q, pay = value(g.M, w, g.n, g.bg)
    U = (g.coeff @ w) / g.scale
    bads = []
    score = float('inf')
    for a in range(g.k):
        eligible = []
        for j, counts in enumerate(g.final):
            if counts[a] != 1:continue
            if all(U[j,b] >= val-1e-8 for b in range(g.k) if b != a and counts[b]):
                eligible.append(j)
        if not eligible:return None
        j = min(eligible,key=lambda j:U[j,a])
        score = min(score, val-U[j,a])
        bads.append(dict(action=a,terminal=g.final[j],utilities=U[j].tolist(),root=float(U[j,a])))
    norm = float(sum(w))
    return dict(status='NUMERICAL_STATIC_CANDIDATE_ONLY', r=g.n, k=g.k, prefix=g.prefix,
                weights=list(map(int,w)),value=val,query_q=q.tolist(),bads=bads,
                score=score,relative=score/norm)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--r',type=int,default=3)
    ap.add_argument('--k',type=int,default=6)
    ap.add_argument('--prefix',default=None)
    ap.add_argument('--seconds',type=int,default=45)
    ap.add_argument('--seed',type=int,default=32766)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    prefix=(0,)*a.k if a.prefix is None else tuple(map(int,a.prefix.split(',')))
    g=Game(a.r,a.k,prefix)
    rng=random.Random(a.seed)
    best,bank,trials=None,[],0
    start=time.monotonic()
    while time.monotonic()-start<a.seconds:
        if bank and rng.random()<.8:
            w=rng.choice(bank)['weights'].copy()
            for _ in range(rng.randrange(1,8)):
                j=rng.randrange(len(w));w[j]=max(0,w[j]+rng.randrange(-15,16))
        else:w=[rng.randrange(24) if rng.random()<.5 else 0 for _ in range(len(g.M))]
        w[-1]=0
        if not any(w):continue
        try:out=trial(g,np.array(w))
        except RuntimeError:continue
        trials+=1
        if out is None:continue
        bank.append(out);bank.sort(key=lambda x:-x['relative']);bank=bank[:20]
        if best is None or out['relative']>best['relative']+1e-10:
            best=out;print(json.dumps(dict(trial=trials,score=out['score'],relative=out['relative'],value=out['value'])),flush=True)
        a.output.write_text(json.dumps(dict(status='NUMERICAL_STATIC_SEARCH_ONLY',trials=trials,
             elapsed=time.monotonic()-start,best=best,bank=bank),indent=2)+'\n')
        if out['score']>1e-6:break

if __name__=='__main__':main()
