#!/usr/bin/env python3
"""Independent integer oracle for the perturbed minimum-work face family.

No import of the construction/audit under review. All arithmetic is integral:
processing times are scaled by m. Exhaustive schedules only for m=2,3.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import platform
from fractions import Fraction as F
from pathlib import Path


def matrix(m):
    # column 0 is the common large job; then (home, index) small jobs
    return [[m*m] + [m if i == h else m+1
                     for h in range(m) for _ in range(m-1)]
            for i in range(m)]


def loads(p, a):
    return [sum(p[i][j] for j in range(len(a)) if a[j] == i)
            for i in range(len(p))]


def rank(a):
    a = [list(map(F, row)) for row in a]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = a[r][c]
        a[r] = [v/z for v in a[r]]
        for i in range(r+1, len(a)):
            z = a[i][c]
            if z:
                a[i] = [x-z*y for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r


def audit():
    exhaustive=[]
    for m in (2,3):
        p=matrix(m)
        n=len(p[0])
        optimum=None
        mincost=None
        mincost_values=set()
        count=0
        for a in itertools.product(range(m), repeat=n):
            z=loads(p,a)
            val=max(z)
            cost=sum(z)
            optimum=val if optimum is None else min(optimum,val)
            if mincost is None or cost<mincost:
                mincost=cost
                mincost_values={val}
            elif cost==mincost:
                mincost_values.add(val)
            count+=1
        assert optimum==m*m+1
        assert mincost==m**3
        assert mincost_values=={m*(2*m-1)}
        exhaustive.append({'m':m,'assignments':count,
                           'scaled_opt':optimum,
                           'scaled_min_work':mincost,
                           'scaled_mincost_makespans':sorted(mincost_values)})

    vertex=[]
    # Row rank computed independently on the complete positive-variable system.
    for m in range(2,9):
        p=matrix(m)
        n=len(p[0])
        positive=[(i,0) for i in range(m)] + [
            (h,1+h*(m-1)+t) for h in range(m) for t in range(m-1)]
        equations=[[int(j==q) for _,j in positive] for q in range(n)]
        equations += [[p[i][j] if a==i else 0 for a,j in positive]
                      for i in range(m-1)]
        r=rank(equations)
        assert r==len(positive)==m*m
        vertex.append({'m':m,'positive_variables':len(positive),'active_rank':r})

    identities=[]
    for m in list(range(2,101))+[10**6,10**50+7]:
        target=F(m*m+1,m)
        shares=[F(m+1,m*m)]*(m-1)+[F(1,m*m)] if m<1000 else None
        if shares is not None:
            assert sum(shares)==1 and min(shares)>0
            assert [F(m-1)+m*q for q in shares[:-1]]==[target]*(m-1)
            assert F(m-1)+m*shares[-1]<target
        bad=2*m-1
        ratio=F(m*(2*m-1),m*m+1)
        assert ratio*target==bad
        assert ratio==2-F(m+2,m*m+1)
        lp=F(m)
        assert target/lp==1+F(1,m*m)
        assert F(m)+F(1,m)<m+1
        assert F((m-1)*m)+F(m-1,m)==(m-1)*target
        identities.append({'m':m,'OPT':str(target),'LST':str(lp),'ratio':str(ratio)})
    return {'title':'最小总处理时间支撑面的独立整数与基矩阵审计',
            'arithmetic':'Python integers and Fraction only',
            'python':platform.python_version(),
            'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'exhaustive':exhaustive,'basic_rank':vertex,'identities':identities,
            'limits':'Only m=2,3 full schedule enumeration; finite rank/formula checks do not prove the general claim.'}


if __name__=='__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
