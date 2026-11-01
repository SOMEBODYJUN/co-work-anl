"""Explore the enlarged last-maximal customer columns for seven maxima, six players.

This is a necessary-condition cone, not an exact SPE solver.  It reconstructs
the source inequalities in six_maxima_joint_bound.md with s=7.
"""
import argparse
from fractions import Fraction
from itertools import combinations
import numpy as np
from scipy.optimize import linprog

N = 6
S = 7
PAIRS = list(combinations(range(S), 2)) + [(i, i) for i in range(S)]
PAIRS.sort()

def mixed_coeffs():
    A, B = [], []
    for t in range(N - 1):
        z = Fraction(t) + Fraction(S * (N-t), 2)
        a = Fraction(N+t, 2*(t+1))
        A.append(a/z)
        B.append(1/z)
    A.append(Fraction(1,N+S-1))
    B.append(Fraction(N+1,N*(N+S-1)))
    return [min(A[t:]) for t in range(N)], [min(B[t:]) for t in range(N)]

def build(excluded, route=None):
    aa, bb=mixed_coeffs()
    names=[f'M{i}' for i in range(N)]+[f'P{i}{j}' for i in range(N-1) for j in range(S)]+[f'L{j}' for j in range(S)]+[f'T{j}{k}' for j,k in PAIRS]
    columns=[]
    rhs=[]
    typ=[]
    for I in range(1,1<<S):
      f=bool(I&1)
      m=I.bit_count()
      for pbits in range(1<<(N-1)):
       if route is not None and any((pbits&(1<<t)) and not (I&(1<<route[t])) for t in range(N-1)):
        continue
       d=bool(pbits & (1<<(N-2)))
       p=(pbits & ((1<<(N-2))-1)).bit_count()
       J=pbits | (int(f)<<(N-1))
       count=J.bit_count()
       cover=int(count>0)
       share=[Fraction(int(J&(1<<t)),count) if count else Fraction(0) for t in range(N)]
       core=m==S
       priv=m==1
       floor=[Fraction(1,N) if core else aa[t] if priv else bb[t] for t in range(N)]
       col=[share[t]-floor[t] for t in range(N)]
       for t in range(N-1):
        pt=(J & ((1<<t)-1)).bit_count()
        for j in range(S):
         col.append(share[t]-(Fraction(1,pt+N-t) if (I&(1<<j)) else 0))
       col += [share[-1]-Fraction(int(bool(I&(1<<j))),p+d+1) for j in range(S)]
       for j,k in PAIRS:
        mjk=int(bool(I&(1<<j)))+int(bool(I&(1<<k)))
        tax=Fraction(int(d),(p+1)*(p+2))
        col.append(share[-2]+share[-1]+tax-(Fraction(mjk,p+mjk) if mjk else 0))
       target=int(bool(I & (((1<<S)-1) ^ (1<<excluded))))
       columns.append([float(v) for v in col])
       rhs.append(float(Fraction(cover)-Fraction(target,2)))
       typ.append((I,J))
    return names,np.array(columns),np.array(rhs),typ

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--excluded',type=int,default=6)
    ap.add_argument('--route',type=str,default=None,help='five digits from 0 to 6; last route is fixed 0')
    args=ap.parse_args()
    route=None if args.route is None else tuple(int(q) for q in args.route)
    assert route is None or (len(route)==5 and all(0<=q<7 for q in route))
    names,A,b,typ=build(args.excluded,route)
    print('columns',len(b),'rows',len(names),'minimum RHS',min(b))
    res=linprog(np.zeros(A.shape[1]),A_ub=A,b_ub=b,bounds=(0,None),method='highs')
    print('feasibility',res.status,res.message)
    if res.success:
        print('multipliers',[(names[i],x) for i,x in enumerate(res.x) if x>1e-7])
        print('minimum surplus',np.min(b-A@res.x))
    else:
        sep=linprog(b, A_ub=-A.T, b_ub=np.zeros(A.shape[1]),
                    A_eq=np.ones((1,len(b))), b_eq=[1.0],
                    bounds=(0,None),method='highs')
        print('normalized separator',sep.status,sep.fun if sep.success else sep.message)
        if sep.success:
            print('support',[(typ[i],v,b[i]) for i,v in enumerate(sep.x) if v>1e-8])
