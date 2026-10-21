"""Attack graph transport in a wider anonymous own-congestion class.

The generated payoffs need NOT have nonnegative customer representations.
Any separating example therefore refutes only the graph template.
"""
from itertools import product, combinations_with_replacement
import random
import argparse
import json
import numpy as np
from scipy.optimize import linprog
from payoff_state_flow import PayoffGraph, counts


def build_payoffs(p,n,rng,mode):
    states=[counts(z,p) for z in combinations_with_replacement(range(p),n)]
    value={}
    for a in range(p):
        relevant=[q for q in states if q[a]]
        if mode=='isotone':
            raw={q:rng.randrange(0,100) for q in relevant}
            for q in relevant:
                value[q,a]=max(raw[r] for r in relevant if r[a]>=q[a] and all(
                    r[b]<=q[b] for b in range(p) if b!=a))
        elif mode=='conjunction':
            value.update({(q,a):rng.randrange(0,20) for q in relevant})
            terms=[(tuple(rng.randrange(n) for b in range(p) if b!=a),rng.randrange(0,100))
                   for _ in range(6)]
            baseline=rng.randrange(0,100)
            for q in relevant:
                other=[q[b] for b in range(p) if b!=a]
                value[q,a]=baseline+sum(w for v,w in terms if all(x>=y for x,y in zip(other,v)))
        else:
            raise ValueError(mode)
    return value


def equilibrium(p,n,value,rng):
    actions={};terms={}
    for depth in range(n,-1,-1):
        for h in product(range(p),repeat=depth):
            if depth==n:
                terms[h]=counts(h,p)
            else:
                best=max(value[terms[h+(a,)],a] for a in range(p))
                chosen=rng.choice([a for a in range(p) if value[terms[h+(a,)],a]==best])
                actions[h]=chosen;terms[h]=terms[h+(chosen,)]
    return actions,terms[()]


def security(p,n,value):
    backgrounds=[counts(z,p) for z in combinations_with_replacement(range(p),n-1)]
    matrix=[]
    for a in range(p):
        matrix.append([])
        for b in backgrounds:
            q=list(b);q[a]+=1
            matrix[-1].append(value[tuple(q),a])
    # max t: every background has p-expectation at least t
    result=linprog([0]*p+[-1],A_ub=np.column_stack((-np.array(matrix).T,np.ones(len(backgrounds)))),
                   b_ub=np.zeros(len(backgrounds)),A_eq=[[1]*p+[0]],b_eq=[1],bounds=[(0,None)]*p+[(None,None)])
    return -result.fun,result.x[:p]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--topics',type=int,default=3)
    parser.add_argument('--players',type=int,default=3);parser.add_argument('--samples',type=int,default=1000)
    parser.add_argument('--mode',default='isotone');args=parser.parse_args()
    rng=random.Random(20261021);max_ratio=0
    for i in range(args.samples):
        value=build_payoffs(args.topics,args.players,rng,args.mode)
        actions,root=equilibrium(args.topics,args.players,value,rng)
        welfare=sum(root[a]*value[root,a] for a in range(args.topics) if root[a])
        v,query=security(args.topics,args.players,value)
        if welfare: max_ratio=max(max_ratio,args.players*v/welfare)
        if welfare+1e-6<args.players*v:
            print(json.dumps({'status':'abstract_counterexample_not_customer_instance',
                              'iteration':i,'root':root,'welfare':welfare,'security':v,'query':list(query),
                              'payoffs':[{'q':q,'a':a,'u':u} for (q,a),u in value.items()],
                              'actions':[{'history':h,'action':a} for h,a in actions.items()]},indent=2))
            return
    print(json.dumps({'samples':args.samples,'maximum_n_security_over_welfare':max_ratio,
                      'status':'finite_no_obstruction_in_wider_class'}))


if __name__=='__main__':main()
