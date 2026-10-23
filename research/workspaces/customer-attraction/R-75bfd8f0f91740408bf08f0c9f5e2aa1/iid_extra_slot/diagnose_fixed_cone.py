"""Diagnostic LP for the extra-slot candidate; no general theorem is inferred.

Retains every ordered history of the established six-action strategy and
imposes the exact uniform iid four-player KKT equalities. Background counts
are legal combinations of these same actions. SciPy only proposes candidates.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
import json
import numpy as np
from scipy.optimize import linprog, minimize

M=6
TYPES=list(range(1,1<<M))

def sigma(h):
    if not h: return 0
    if len(h)==1: return 3 if h[0]<3 else 0
    group=range(3) if h[1]<3 else range(3,6)
    return next(a for a in group if a not in h)

def finish(h):
    while len(h)<3: h=h+(sigma(h),)
    return h

def coefficients(z,a,bg):
    return [F(1,bg[t]+sum((t>>x)&1 for x in z)) if (t>>a)&1 else F(0)
            for t in TYPES]

def g(n,b,t):
    return sum(F(comb(n-1,k))*t**k*(1-t)**(n-1-k)/F(b+1+k)
               for k in range(n))

def rows(background):
    bg={t:sum(background[a] for a in range(M) if (t>>a)&1) for t in TYPES}
    gamma=[]
    for depth in range(3):
        for h in product(range(M),repeat=depth):
            actual=finish(h)
            for a in range(M):
                own=coefficients(actual,sigma(h),bg)
                dev=coefficients(finish(h+(a,)),a,bg)
                gamma.append([x-y for x,y in zip(own,dev)])
    alpha=[[g(4,bg[t],F(t.bit_count(),M)) if (t>>a)&1 else F(0)
            for t in TYPES] for a in range(M)]
    root=coefficients(finish(()),0,bg)
    objective=[x-y for x,y in zip(alpha[0],root)]
    equalities=[[x-y for x,y in zip(alpha[a],alpha[0])] for a in range(1,M)]
    return gamma, equalities,objective

def solve(background):
    gamma,eq,obj=rows(background)
    result=linprog(-np.array(obj,dtype=float),A_ub=-np.array(gamma,dtype=float),
                   b_ub=np.zeros(len(gamma)),A_eq=np.array(eq+[[F(1)]*len(TYPES)],dtype=float),
                   b_eq=np.array([0]*len(eq)+[1]),bounds=(0,None),method='highs')
    return {"background":background,"success":result.success,
            "lambda4_minus_root":None if not result.success else -result.fun,
            "positive_types":None if not result.success else
            {str(t):float(w) for t,w in zip(TYPES,result.x) if w>1e-8}}

if __name__=='__main__':
    bgs=[[0]*6,[1]*6,[2]*6,[10]*6,[100]*6,
         [1,0,0,0,0,0],[10,0,0,0,0,0],[1,1,1,0,0,0],[1,0,0,1,0,0]]
    print(json.dumps([solve(bg) for bg in bgs],indent=2))
