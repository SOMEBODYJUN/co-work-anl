"""One-action diagnostic: can a maximum-standalone action fail lambda_3?

This does not test the general first-player candidate, because another action
may rescue the root. All rational coefficient rows are retained for review.
"""
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog

def solve(q, first=0, reply=1):
    m=len(q); types=list(range(1,1<<m))
    def inc(t,a): return F((t>>a)&1)
    def f(a): return [inc(t,a) for t in types]
    def u(a,b): return [inc(t,a)/(1+inc(t,b)) for t in types]
    def sub(x,y): return [a-b for a,b in zip(x,y)]
    def g(t): return 1-t+t*t/3
    alpha=[[inc(t,a)*g(sum(q[b] for b in range(m) if (t>>b)&1))
            for t in types] for a in range(m)]
    support=[a for a in range(m) if q[a]]; ref=support[0]
    gamma=[sub(f(first),f(a)) for a in range(m)]
    gamma += [sub(u(reply,first),u(a,first)) for a in range(m)]
    gamma += [sub(alpha[ref],alpha[a]) for a in range(m) if not q[a]]
    eq=[sub(alpha[ref],alpha[a]) for a in support[1:]]
    obj=sub(alpha[ref],u(first,reply))
    r=linprog(-np.array(obj,dtype=float),A_ub=-np.array(gamma,dtype=float),
              b_ub=np.zeros(len(gamma)),A_eq=np.array(eq+[[1]*len(types)],dtype=float),
              b_eq=[0]*len(eq)+[1],bounds=(0,None),method='highs')
    return {"q":[str(x) for x in q],"success":r.success,
            "lambda3_minus_max_f_action": None if not r.success else -r.fun,
            "weights":None if not r.success else
            {str(t):str(F(float(w)).limit_denominator(100000))
             for t,w in zip(types,r.x) if w>1e-8}}

if __name__=='__main__':
    print(json.dumps([solve([F(1,6)]*6),
                      solve([F(0)]+[F(1,5)]*5),
                      solve([F(1,2),F(1,2)]+[F(0)]*4),
                      solve([F(0),F(1,2),F(1,2)]+[F(0)]*3)],indent=2))
