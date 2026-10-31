"""Exact rational vertex enumeration of a 3-item, 2-resource LP.

No floating point solver or external dependencies.  Item a uses both resource
positions; b and c use one each, hence every column has consecutive ones.
This tests the tempting extension of scalar-assignment LP submodularity to
consecutive-ones/vector capacities.
"""
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path

A = [[1, 1, 0], [1, 0, 1]]

def solve_square(mat, rhs):
    aug = [[Q(x) for x in row]+[Q(y)] for row,y in zip(mat,rhs)]
    for k in range(len(mat)):
        pivot = next((i for i in range(k,len(mat)) if aug[i][k]), None)
        if pivot is None:
            return None
        aug[k],aug[pivot] = aug[pivot],aug[k]
        scale=aug[k][k]
        aug[k]=[x/scale for x in aug[k]]
        for i in range(len(mat)):
            if i != k:
                scale=aug[i][k]
                aug[i]=[x-scale*y for x,y in zip(aug[i],aug[k])]
    return [row[-1] for row in aug]

def optimum(mask):
    rows=[list(r) for r in A]
    rhs=[Q(1),Q(1)]
    for i in range(3):
        row=[0]*3;row[i]=1;rows.append(row)
        rhs.append(Q(bool(mask & (1<<i))))
        row=[0]*3;row[i]=-1;rows.append(row);rhs.append(Q(0))
    best=Q(-1);bestx=None
    for basis in combinations(range(len(rows)),3):
        x=solve_square([rows[i] for i in basis],[rhs[i] for i in basis])
        if x is not None and all(sum(Q(a)*v for a,v in zip(row,x))<=r
                                 for row,r in zip(rows,rhs)):
            if sum(x)>best:
                best=sum(x);bestx=x
    return best,bestx

result={str(mask):{'value':str(optimum(mask)[0]),
                   'witness':[str(x) for x in optimum(mask)[1]]}
        for mask in range(8)}
left=Q(result['3']['value'])+Q(result['5']['value'])
right=Q(result['1']['value'])+Q(result['7']['value'])
assert (left,right)==(Q(2),Q(3))
result['submodularity_check']={'A':3,'B':5,'lhs':str(left),'rhs':str(right),
                              'defect':str(right-left)}
path=Path(__file__).with_name('exact_vector_lp_results.json')
path.write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
