"""Exact vertices of the all-subset truncation arrangement, independent of SPE.

No floating-point decision occurs in vertex enumeration. The finite set suffices
for B(v) when customer multiplicities and v are nonnegative, including v=0.
Enumeration is exponential; p=5 already examines 170068 row subsets.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations,permutations
from pathlib import Path
import argparse,json,time


def solve_binary_ones(rows):
    """Solve A x = 1 exactly by integer Bareiss elimination; None if singular."""
    n=len(rows)
    if not n:return ()
    mat=[list(row)+[1] for row in rows]
    previous=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if mat[i][k]),None)
        if pivot is None:return None
        if pivot!=k:mat[k],mat[pivot]=mat[pivot],mat[k]
        value=mat[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n+1):
                num=mat[i][j]*value-mat[i][k]*mat[k][j]
                q,rem=divmod(num,previous)
                if rem:raise AssertionError('Bareiss division was not exact')
                mat[i][j]=q
            mat[i][k]=0
        previous=value
    if not mat[-1][n-1]:return None
    out=[F(0)]*n
    for i in range(n-1,-1,-1):
        out[i]=(F(mat[i][-1])-sum(F(mat[i][j])*out[j] for j in range(i+1,n)))/mat[i][i]
    if not all(sum(F(a)*z for a,z in zip(row,out))==1 for row in rows):raise AssertionError('solution replay')
    return tuple(out)


def enumerate_vertices(p):
    """Return (labeled_vertices, sorted_patterns, enumeration_stats).

    A positive support of size s needs s independent active subset sums=1.
    Relabel its coordinates to [s], enumerate every s-row subset of all nonempty
    binary rows, then embed into [p] using all distinct coordinate permutations.
    Sorting patterns loses no candidate, since the row universe is permutation
    invariant. Zero is included independently of the positive support loop.
    """
    if not isinstance(p,int) or isinstance(p,bool) or p<0:raise ValueError('p must be a nonnegative integer')
    patterns={(F(0),)*p};stats=[]
    for s in range(1,p+1):
        all_rows=tuple(tuple(int(mask>>a&1) for a in range(s)) for mask in range(1,1<<s))
        checked=singular=positive=0
        for selected in combinations(all_rows,s):
            checked+=1;z=solve_binary_ones(selected)
            if z is None:singular+=1;continue
            if all(0<x<=1 for x in z):
                positive+=1
                patterns.add(tuple(sorted(z,reverse=True))+(F(0),)*(p-s))
        stats.append({'support':s,'row_subsets':checked,'singular':singular,'positive_basis_solutions':positive})
    vertices=tuple(sorted({z for pat in patterns for z in permutations(pat)}))
    return vertices,tuple(sorted(patterns)),tuple(stats)


def payload(p):
    started=time.monotonic();vertices,patterns,stats=enumerate_vertices(p)
    return {'scope':'exact all-subset truncation arrangement vertices; no equilibrium assumption','topics':p,'fraction_encoding':'Fraction numerator/denominator strings','vertices':[[str(x) for x in z] for z in vertices],'sorted_patterns':[[str(x) for x in z] for z in patterns],'counts':{'vertices':len(vertices),'patterns':len(patterns)},'enumeration_stats':stats,'seconds':time.monotonic()-started}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=5);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    result=payload(args.topics);args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['counts']))
