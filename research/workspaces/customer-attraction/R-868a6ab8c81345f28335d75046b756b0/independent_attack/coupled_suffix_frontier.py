"""Test a precise general compiler candidate using an asymptotic coupled product.
Discovery only. Exact Fraction convex hull calculation, m=3 components with
singleton resources. This does not test or refute Q-CAG-HALF.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json


def hull_opt(points, threshold, objective, maximize=False):
    candidates=[]
    for point in points:
        if point[1]>=threshold:
            candidates.append((objective(point),[(F(1),point)]))
    for i,p in enumerate(points):
        for q in points[:i]:
            if (p[1]-threshold)*(q[1]-threshold)<0:
                lam=(threshold-q[1])/(p[1]-q[1])
                value=lam*objective(p)+(1-lam)*objective(q)
                candidates.append((value,[(lam,p),(1-lam,q)]))
    return (max if maximize else min)(candidates,key=lambda x:x[0])

def solve(weights):
    k=len(weights); menus=[]; floors=[]; lows=[]
    for a in range(k):
        points=[]; mins=[]
        for b in range(k):
            utility=[F(weights[c],1+(a==c)+(b==c)) for c in range(k)]
            replies=[c for c in range(k) if utility[c]==max(utility)]
            row=[]
            for c in replies:
                n=[(a==j)+(b==j)+(c==j) for j in range(k)]
                point=(F(weights[a],n[a]),F(weights[b],n[b]),
                       sum(weights[j] for j in range(k) if n[j]),a,b,c)
                points.append(point);row.append(point[1])
            mins.append(min(row))
        floor=max(mins)
        low=hull_opt(points,floor,lambda z:z[0])
        menus.append(points);floors.append(floor);lows.append(low)
    M=max(z[0] for z in lows)
    optimum=sum(sorted(weights,reverse=True)[:3])
    best=[]
    for a in range(k):
        high=hull_opt(menus[a],floors[a],lambda z:3*z[0]-2*z[2],True)
        gain=high[0]+optimum-3*M
        best.append((gain,a,high))
    return M,lows,max(best,key=lambda z:z[0]),floors

if __name__=='__main__':
    best=None;count=0
    for k in (3,4,5):
        for weights in combinations_with_replacement(range(1,15),k):
            if weights[-1]>3*weights[0]+5:continue
            M,lows,z,floors=solve(weights);count+=1
            if best is None or z[0]>best[0]:
                best=(z[0],weights,M,lows,z,floors)
    print('exact_fraction_cases',count)
    print(best)
