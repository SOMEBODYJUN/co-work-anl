"""Exact verifier for the explicit failure certificate in the coNP proof.
No solver, floating point, or random sampling is used.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

def verify(A,I,S,delta,z,xis,y):
    R=len(A);m=len(A[0]);assert I and S
    assert len(set(I))==len(I) and len(set(S))==len(S)
    assert all(0<=r<R for r in I) and all(0<=j<m for j in S)
    assert all(t>=0 for t in delta) and sum(delta)==1
    assert all(delta[j]>0 for j in S)
    vals=[sum(a*t for a,t in zip(row,delta)) for row in A]
    assert all(vals[r]==z if r in I else vals[r]>z for r in range(R))
    gradients={}
    for j in S:
        xi=xis[j];assert len(xi)==len(I) and min(xi)>=0 and sum(xi)==1
        g=[sum(xi[t]*A[r][s] for t,r in enumerate(I)) for s in range(m)]
        assert all(g[j]>=g[s] for s in range(m));gradients[str(j)]=[str(v) for v in g]
    assert all(y.get((j,s),0)>=0 for j in S for s in range(m))
    dual=[sum(y.get((j,s),0)*(A[r][s]-A[r][j]) for j in S for s in range(m)) for r in I]
    assert min(dual)>=1
    return dict(status='verified exactly',active_values=[str(t) for t in vals],coordinate_gradients=gradients,farkas_M_transpose_y=[str(t) for t in dual])

if __name__=='__main__':
    A=[[Q(2),Q(0),Q(3,2)],[Q(0),Q(2),Q(3,2)]]
    result=verify(A,[0,1],[0,1],[Q(1,4),Q(1,4),Q(1,2)],Q(5,4),
                  {0:[Q(1),Q(0)],1:[Q(0),Q(1)]},{(0,2):Q(1),(1,2):Q(1)})
    print(json.dumps(result,indent=2))
    Path(__file__).with_name('verify_cloning_conp_certificate.json').write_text(json.dumps(result,indent=2))
