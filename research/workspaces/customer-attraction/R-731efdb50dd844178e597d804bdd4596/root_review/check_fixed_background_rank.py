"""Independent Fraction check, importing no author code or CAG solver.

Build every customer column directly from topic membership and terminal counts;
derive row rank and nullspaces by elimination. Finite checks audit the symbolic
Cauchy/rational-function proof and do not replace it.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def rank(matrix):
    A=[list(map(F,row)) for row in matrix]
    if not A:return 0
    r=0
    for c in range(len(A[0])):
        k=next((k for k in range(r,len(A)) if A[k][c]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r]
        pivot=A[r][c];A[r]=[x/pivot for x in A[r]]
        for k in range(len(A)):
            if k!=r and A[k][c]:
                v=A[k][c];A[k]=[x-v*y for x,y in zip(A[k],A[r])]
        r+=1
        if r==len(A):break
    return r


def rows(v,M):
    p=len(v)+2
    labels=[(a,j) for a in (0,1) for j in range(1,M+1)]
    out=[]
    for a,j in labels:
        counts=[0]*p;counts[a]=j;counts[1-a]=M-j;counts[2:]=v
        row=[]
        for mask in range(1,1<<p):
            den=sum(c for t,c in enumerate(counts) if mask>>t&1)
            row.append(F(1,den) if mask>>a&1 else F(0))
        out.append(row)
    return out


def basis(T,M):
    d=len(T)
    if d>=M:return []
    def h(J):
        result=[F(0)]*M
        for j in J:
            top=1;bottom=1
            for t in T:top*=j+t
            for k in J:
                if k!=j:bottom*=j-k
            result[j-1]=F(top,bottom)
        return result
    J=list(range(1,d+2));b=h(J)
    out=[b+[-x for x in b]]
    for r in range(d+2,M+1):
        b=h(J+[r]);out.extend([b+[F(0)]*M,[F(0)]*M+b])
    return out


def main():
    backgrounds=[()]+[(i,) for i in range(1,5)]
    backgrounds += list(product(range(1,4),repeat=2))
    backgrounds += [(1,1,1),(1,2,3),(2,2,2),(2,3,4),(1,1,1,1)]
    cases=circuits=fours=0
    for v in backgrounds:
        T=sorted({sum(c for j,c in enumerate(v) if mask>>j&1) for mask in range(1<<len(v))})
        for M in range(1,9):
            matrix=rows(v,M);d=len(T)
            assert rank(matrix)==min(2*M,2*d+1),(v,M)
            B=basis(T,M)
            assert rank(B)==max(0,2*M-2*d-1)
            for b in B:
                assert all(sum(b[i]*matrix[i][j] for i in range(2*M))==0 for j in range(len(matrix[0])))
            cases+=1;circuits+=len(B)
        if v:
            for r in range(2,7):
                for s in range(1,r):
                    M=r+s;matrix=rows(v,M)
                    # U_a(q_r), U_b(q_s), U_a(q_s), U_b(q_0).
                    selected=[matrix[r-1],matrix[M+(M-s)-1],matrix[s-1],matrix[2*M-1]]
                    assert rank(selected)==4,(v,r,s)
                    fours+=1
    result={'status':'passed','independent_of_author_code':True,'background_M_cases':cases,
            'nullspace_basis_vectors':circuits,'four_slot_cases':fours,
            'universal_proof':'Cauchy rank plus polynomial root count and rational partial fractions, checked separately in review',
            'Q_CAG_HALF':'OPEN'}
    path=Path(__file__).with_name('fixed_background_rank_review.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
