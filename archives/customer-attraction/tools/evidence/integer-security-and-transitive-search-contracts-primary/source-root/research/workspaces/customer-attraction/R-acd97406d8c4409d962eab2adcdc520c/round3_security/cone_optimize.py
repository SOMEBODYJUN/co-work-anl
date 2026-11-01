"""Exploratory fixed-query optimization over a real full SPE policy cone.

No LP point is a certified game.  The final stored point includes the policy
inequality rows; any candidate needs rational reconstruction and an independent
full-tree SPE check before it can refute any mathematical assertion.
"""
import argparse, json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from search_security import Search


def cone(search,w):
    info,outcomes,u=search.evaluate(w,need_outcomes=True)
    welf=search.coverage_coeff@w
    root=min(outcomes[(0,)*search.k], key=lambda j:welf[j])
    seen=set();rows=set();stack=[((0,)*search.k,root)]
    while stack:
        q,target=stack.pop()
        if (q,target) in seen or sum(q)==search.n:continue
        seen.add((q,target))
        children=[outcomes[c] for c in search.children[q]]
        floor=max(np.min(u[child,a]) for a,child in enumerate(children))
        admissible=[a for a,child in enumerate(children)
                    if target in child and u[target,a]>=floor]
        a=admissible[0]
        stack.append((search.children[q][a],target))
        for b,child in enumerate(children):
            dev=target if b==a else min(child,key=lambda j:u[j,b])
            stack.append((search.children[q][b],dev))
            row=tuple((search.utility_coeff[target,a]-search.utility_coeff[dev,b]).tolist())
            if any(row):rows.add(row)
    return info,root,np.array(sorted(rows)),len(seen)


def optimize(search,w,rounds):
    info,root,G,states=cone(search,w)
    p=np.array(info['query']);last=None;trace=[]
    B=search.security_coeff/search.scale
    c=search.coverage_coeff[root]
    for i in range(rounds):
        fixed=np.einsum('a,hat->ht',p,B)
        lp=linprog(np.r_[np.zeros(len(w)),-1],
            A_ub=np.r_[np.c_[-G,np.zeros(len(G))],np.c_[-fixed,np.ones(len(fixed))]],
            b_ub=np.zeros(len(G)+len(fixed)),
            A_eq=[np.r_[c,0]],b_eq=[1],
            bounds=[(0,None)]*len(w)+[(None,None)],method='highs')
        if not lp.success:return dict(status=lp.message,initial=info)
        w=lp.x[:-1]
        pay=B@w
        query=linprog(np.r_[np.zeros(search.k),-1],A_ub=np.c_[-pay,np.ones(len(pay))],
            b_ub=np.zeros(len(pay)),A_eq=[np.r_[np.ones(search.k),0]],b_eq=[1],
            bounds=[(0,None)]*search.k+[(None,None)],method='highs')
        if not query.success:raise RuntimeError(query.message)
        p=query.x[:-1];v=query.x[-1]
        trace.append(dict(iteration=i,value=float(v),gap=float(1-search.n*v),
                          min_spe_margin=float(np.min(G@w)),support=int(np.count_nonzero(w>1e-9))))
        if last is not None and abs(v-last)<1e-10:break
        last=v
    return dict(status='UNCERTIFIED_LP_POINT',n=search.n,k=search.k,
                root_counts=search.final[root],policy_subproblems=states,
                Gamma_rows=len(G),initial=info,weights=w.tolist(),query=p.tolist(),
                trace=trace,rows=G.tolist())


def main():
    ap=argparse.ArgumentParser();ap.add_argument('seed',type=Path);ap.add_argument('--rounds',type=int,default=20)
    ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    seed=json.loads(a.seed.read_text());seeds=seed.get('bank',[seed.get('best',seed)])
    results=[]
    for j,x in enumerate(seeds[:20]):
        if not x:continue
        s=Search(x['n'],x['k']);r=optimize(s,np.array(x['weights'],dtype=np.int64),a.rounds)
        results.append(r)
        print(json.dumps(dict(seed=j,trace=r.get('trace'),states=r.get('policy_subproblems'))),flush=True)
        a.output.write_text(json.dumps(dict(status='EXPLORATORY',results=results),indent=2)+'\n')
        if r.get('trace') and r['trace'][-1]['gap'] < -1e-7:break

if __name__=='__main__':main()
