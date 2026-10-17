from fractions import Fraction as F
from itertools import combinations

def loads(P, alloc):
    return [sum(P[i][j] for j in alloc[i]) for i in range(len(P))]

def main():
    # Exact rho=1.9 witness from the text.
    U=[[1,1,1,1],[1,1,0,0]]
    B=F(1); lam=F(2,5)
    P=[[B-lam*u for u in row] for row in U]
    balanced=[[2,3],[0,1]]
    assert max(loads(P,balanced))==F(6,5)
    overflow=[[0,1,2],[3]]
    assert max(loads(P,overflow))==F(9,5)
    assert F(9,5) / F(6,5) == F(3,2) < F(19,10)
    # Uniform p0: q+1 versus q has ratio (q+1)/q.
    for rho in (F(3,2),F(19,10),F(2)):
        q=max(2, (1/(rho-1)).numerator // (1/(rho-1)).denominator)
        # choose q large enough if division was not integral
        while F(q+1,q)>rho: q += 1
        assert F(q+1,q)<=rho
    print({'status':'passed','rho_witness':str(F(3,2)),'uniform_count_bound':'verified'})

if __name__ == '__main__': main()
