"""Exact row definitions for a largest-topic true-root-branch projection.

Exploratory finite *type* LP; every row is necessary for arbitrary catalogues.
No solution of this outer relaxation is claimed to be a complete SPE.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import linprog


def choose(n,k):
    return comb(n,k) if 0 <= k <= n else 0


STATES = list(product(product((0,1),repeat=5),range(6)))


def rows():
    names=[]; matrix=[]
    def add(name, fn):
        names.append(name); matrix.append([fn(a,j) for a,j in STATES])
    def pay(a,i):
        return F(a[i],sum(a)) if a[i] else F(0)
    # Row form s(x)+s_r*r >=0. Only root row has s_r=1.
    add('root_r_ge_true_C',lambda a,j:-pay(a,0))
    for t in range(1,5):
        add(f'size_C_ge_A{t+1}',lambda a,j:F(a[0]-a[t]))
    add('size_C_ge_mean_opt',lambda a,j:F(a[0])-F(j,5))
    for i in range(1,5):
        for t in range(5):
            add(f'IC_{i+1}_A{t+1}',lambda a,j,i=i,t=t:pay(a,i)-F(a[t],sum(a[:i])+5-i))
        add(f'IC_{i+1}_mean_opt',lambda a,j,i=i:pay(a,i)-F(j,5*(sum(a[:i])+5-i)))
    # Exact random comparator k-subtuple profit, same binary root background.
    for k,beta in [(3,F(5,3)),(4,F(1499,750))]:
        for pos in range(5-k,6-k):
            # For k=4 this is pos=1; k=3 pos=2.
            def fn(a,j,k=k,beta=beta,pos=pos):
                b=sum(a[:pos]); v=sum((pay(a,i) for i in range(pos,5)),F(0))
                q=sum((F(choose(j,h)*choose(5-j,k-h)*h,b+h) for h in range(1,k+1)),F(0))/choose(5,k)
                return beta*v-q
            add(f'tail{k}_random_opt',fn)
    def binary(a,j):
        c=sum(a[1:])
        v=F(c,a[0]+c) if c else F(0)
        weight=F(5,3) if a[0] else F(1999,1000)
        q=sum((F(choose(j,h)*choose(5-j,4-h)*h,a[0]+h) for h in range(1,5)),F(0))/5
        return weight*v-q
    add('binary_tail4_random_opt',binary)
    return names,matrix


def main():
    p=argparse.ArgumentParser();p.add_argument('--out');args=p.parse_args()
    names,S=rows(); S=np.array(S,dtype=float)
    K=np.array([a[0] for a,j in STATES],float)
    O=np.array([j>0 for a,j in STATES],float)
    out=[]
    for r in [F(1,5),F(21,100),F(11,50),F(23,100),F(6,25),F(1,4),F(13,50),F(27,100),F(7,25),F(3,10),F(1,3),F(2,5),F(1,2)]:
        rhs=np.zeros(len(names));rhs[0]=float(r)
        res=linprog(-O,A_ub=-S,b_ub=rhs,A_eq=K[None,:],b_eq=[1],bounds=(0,None),method='highs')
        if not res.success:
            print('FAIL',str(r),res.message,flush=True);continue
        mu=-res.ineqlin.marginals
        item={'r':str(r),'O':-res.fun,'alpha':mu[0], 'gamma':-res.eqlin.marginals[0],
              'dual':{n:float(v) for n,v in zip(names,mu) if v>1e-8},
              'support':[{'a':list(STATES[i][0]),'j':STATES[i][1],'mass':float(x)} for i,x in enumerate(res.x) if x>1e-8]}
        out.append(item)
        print(json.dumps({k:v for k,v in item.items() if k!='support'}),flush=True)
    if args.out:
        Path(args.out).write_text(json.dumps({'domain':'outer necessary type LP, not SPE','states':len(STATES),'rows':names,'runs':out},indent=2)+'\n')


if __name__=='__main__':main()
