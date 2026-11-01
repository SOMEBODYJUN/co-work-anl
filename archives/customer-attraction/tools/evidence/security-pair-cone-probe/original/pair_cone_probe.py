"""Optimize first-pair/security on valid full strategy cones with background."""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import random
import time

import numpy as np
from scipy.optimize import linprog

from background_pair_probe import old, minimum_pair, security

HERE=Path(__file__).resolve().parent


def policy_cone(sol,witness,rng):
    q,r=sol.q,sol.r
    masks=np.arange(1,1<<q)
    member=((masks[None,:] >> np.arange(q)[:,None])&1).astype(float)
    prefix=np.array(sol.prefix)
    first,second,target=witness
    target=tuple(target)
    rows=[]
    nodes={}

    def utility(a,t):
        load=(prefix+np.array(t))@member
        return member[a]/np.maximum(load,1)

    @lru_cache(None)
    def expand(c,t):
        if sum(c)==r:
            return
        idx=sol.tidx[t]
        floor=sol.thresholds[c]
        admissible=[]
        for a in range(q):
            ca=tuple(c[i]+int(i==a) for i in range(q))
            if sol.solve(ca)&(1<<idx) and sol.pays[idx][a]>=floor:
                admissible.append(a)
        if sum(c)==0:
            chosen=first
        elif sum(c)==1 and c[first]==1 and t==target:
            chosen=second
        else:
            chosen=rng.choice(admissible)
        assert chosen in admissible
        children=[]
        for a in range(q):
            ca=tuple(c[i]+int(i==a) for i in range(q))
            if a==chosen:
                child=t
            else:
                out=sol.solve(ca)
                indexes=[]
                while out:
                    bit=out&-out;out-=bit
                    indexes.append(bit.bit_length()-1)
                mini=min(sol.pays[i][a] for i in indexes)
                indexes=[i for i in indexes if sol.pays[i][a]==mini]
                child=sol.terminals[rng.choice(indexes)]
            children.append(child)
            rows.append(utility(chosen,t)-utility(a,child))
            expand(ca,child)
        nodes[(c,t)]=(chosen,children)
    expand((0,)*q,target)
    G=np.unique(np.array(rows),axis=0)
    cost=utility(first,target)+utility(second,target)
    backgrounds=np.array(list(old.compositions(r-1,q)))
    R=1/(1+(backgrounds+prefix)@member)
    return G,cost,member,R,nodes


def static_security(w,member,R):
    pay=(R*w)@member.T
    q=len(member)
    res=linprog(np.r_[np.zeros(q),-1.],
        A_ub=np.column_stack([-pay,np.ones(len(pay))]),b_ub=np.zeros(len(pay)),
        A_eq=np.array([np.r_[np.ones(q),0.]]),b_eq=[1.],
        bounds=[(0,None)]*q+[(None,None)],method='highs')
    assert res.success,res.message
    return res.x[-1],res.x[:-1]


def cone_step(G,cost,member,R,p):
    beta=R*(p@member)
    A=np.vstack([np.column_stack([-G,np.zeros(len(G))]),
                 np.column_stack([-beta,np.ones(len(beta))])])
    res=linprog(np.r_[np.zeros(len(cost)),-1.],A_ub=A,b_ub=np.zeros(len(A)),
        A_eq=np.array([np.r_[cost,0.]]),b_eq=[2.],
        bounds=[(0,None)]*len(cost)+[(None,None)],method='highs')
    assert res.success,res.message
    return res.x[:-1],res.x[-1]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trials',type=int,default=200)
    ap.add_argument('--q',type=int,default=6)
    ap.add_argument('--r',type=int,default=4)
    ap.add_argument('--seed',type=int,default=731941)
    args=ap.parse_args()
    rng=random.Random(args.seed)
    best=0.
    started=time.time()
    for trial in range(args.trials):
        q,r=args.q,args.r
        prefix=[0]*q
        for _ in range(rng.randrange(0,8)):
            prefix[rng.randrange(q)]+=1
        density=rng.choice([.08,.2,.5,1.])
        weights={mask:rng.randrange(1,20) for mask in range(1,1<<q) if rng.random()<density}
        if not weights:continue
        sol=old.BackgroundSolver(q,r,prefix,weights)
        pair,witness=minimum_pair(sol)
        G,cost,member,R,nodes=policy_cone(sol,witness,rng)
        ws=np.array([weights.get(mask,0) for mask in range(1,1<<q)])
        starts=[static_security(ws,member,R)[1],np.ones(q)/q]
        starts.append(np.random.default_rng(args.seed+trial).dirichlet(np.ones(q)))
        for si,p in enumerate(starts):
            prev=0.
            for iteration in range(8):
                w,v=cone_step(G,cost,member,R,p)
                v,p=static_security(w,member,R)
                if v>best+1e-8:
                    best=v
                    rec=dict(q=q,r=r,seed=args.seed,trial=trial,start=si,iteration=iteration,
                        ratio=v,prefix=prefix,weights=w.tolist(),query=p.tolist(),
                        witness=witness,rows=len(G),nodes=len(nodes),
                        automaton=[dict(counts=c,target=t,action=a,children=children)
                            for (c,t),(a,children) in nodes.items()],status='numerical cone point')
                    (HERE/f'pair_cone_best_{q}_{r}.json').write_text(json.dumps(rec,indent=2)+'\n')
                    print(json.dumps(dict(trial=trial,r=r,ratio=v,rows=len(G),nodes=len(nodes),seconds=time.time()-started)),flush=True)
                if v>1+1e-7:
                    print('PAIR_CONE_FAILURE',flush=True)
                    return
                if v<=prev+1e-9:break
                prev=v
    print(json.dumps(dict(completed=args.trials,best=best,seconds=time.time()-started)),flush=True)


if __name__=='__main__':main()
