from fractions import Fraction as F
from itertools import combinations, product
from math import lcm
import json


def falling(x, k):
    ans = F(1)
    for r in range(k):
        ans *= x-r
    return ans


def audit(m):
    n=m+1
    t=F(n,m)
    basis=[()]
    for k in (1,2):
        for jobs in combinations(range(n),k):
            for cols in product(range(m),repeat=k):
                basis.append(tuple(zip(jobs,cols)))

    def moment(s):
        vals={}
        for j,a in s:
            if j in vals and vals[j] != a:
                return F(0)
            vals[j]=a
        k=len(vals)
        ans=F(1)
        for a in range(m):
            ans *= falling(t,sum(b==a for b in vals.values()))
        return ans/falling(n,k)

    rows=[[moment(s+u) for u in basis] for s in basis]
    scale=lcm(*(x.denominator for row in rows for x in row))
    a=[[int(scale*x) for x in row] for row in rows]
    dim=len(a)
    prev=1
    pivots=[]
    for k in range(dim):
        neg=next((r for r in range(k,dim) if a[r][r]<0),None)
        if neg is not None:
            return {'m':m,'n':n,'dim':dim,'psd':False,'negative_diagonal_stage':k,'row':neg,'value':str(a[neg][neg])}
        p=next((r for r in range(k,dim) if a[r][r]),None)
        if p is None:
            nonzero=next(((r,c) for r in range(k,dim) for c in range(k,dim) if a[r][c]),None)
            return {'m':m,'n':n,'dim':dim,'psd':nonzero is None,'rank':k,'tail_nonzero':nonzero,'integer_scale':scale,'pivot_signs':''.join(pivots)}
        if p != k:
            a[k],a[p]=a[p],a[k]
            for r in range(dim):
                a[r][k],a[r][p]=a[r][p],a[r][k]
        pivot=a[k][k]
        pivots.append('+')
        for r in range(k+1,dim):
            for c in range(r,dim):
                numerator=pivot*a[r][c]-a[r][k]*a[k][c]
                assert numerator % prev == 0
                a[r][c]=a[c][r]=numerator//prev
        for r in range(k+1,dim):
            a[r][k]=a[k][r]=0
        prev=pivot
    return {'m':m,'n':n,'dim':dim,'psd':True,'rank':dim,'integer_scale':scale,'pivot_signs':''.join(pivots)}


if __name__=='__main__':
    print(json.dumps([audit(m) for m in (2,3,4)],indent=2))
