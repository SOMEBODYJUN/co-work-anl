"""Independent Fraction audit of the all-support marginal/circuit identities."""
from fractions import Fraction as Q
from itertools import combinations
import json

def subsets(A):
 A=tuple(A)
 for k in range(len(A)+1):
  yield from combinations(A,k)

def comps(m,p):
 if p==1:yield (m,);return
 for k in range(m+1):
  for r in comps(m-k,p-1):yield (k,)+r

def lam(q,a,R,removed=()):
 # Drop optional removed labels from the integral, useful for equal-count swaps.
 support=[b for b in range(len(q)) if q[b] and b not in removed]
 total=sum(q[b] for b in support)
 return sum((Q((-1)**len(D),total-sum(q[b] for b in R)+sum(q[b] for b in D)) for D in subsets(R)),Q(0))

def cov(T,B):return Q(bool(set(T)&set(B)))
def payoff(q,a,B):return Q(1,sum(q[b] for b in B)) if a in B else Q(0)
def rank(rows):
 mat=[r[:] for r in rows];nr=len(mat);nc=len(mat[0]) if nr else 0;row=0
 for c in range(nc):
  pivot=next((i for i in range(row,nr) if mat[i][c]),None)
  if pivot is None:continue
  mat[row],mat[pivot]=mat[pivot],mat[row]
  k=mat[row][c];mat[row]=[v/k for v in mat[row]]
  for i in range(row+1,nr):
   if mat[i][c]:
    k=mat[i][c];mat[i]=[a-k*b for a,b in zip(mat[i],mat[row])]
  row+=1
  if row==nr:break
 return row

def audit(m,p):
 types=list(subsets(range(p)))[1:];vertices=[(q,a) for q in comps(m,p) for a in range(p) if q[a]]
 vindex={v:i for i,v in enumerate(vertices)};N=len(vertices)
 cover={():[Q(0)]*N};identities=[];checked=0;swaps=0
 for k in range(1,min(m,p)+1):
  for A in combinations(range(p),k):
   vids=[v for v in vertices if tuple(i for i,x in enumerate(v[0]) if x)==A]
   expansions=[]
   for q,a in vids:
    other=tuple(b for b in A if b!=a)
    ls={R:lam(q,a,R) for R in subsets(other)}
    assert all(x>0 for x in ls.values())
    assert sum(ls.values(),Q(0))==Q(1,q[a])
    for B in types:
     rhs=sum((val*(cov(R+(a,),B)-cov(R,B)) for R,val in ls.items()),Q(0))
     assert rhs==payoff(q,a,B),(m,p,q,a,B,rhs)
     checked+=1
    beta=ls[other];lower=[Q(0)]*N
    for R,val in ls.items():
     T=tuple(sorted(R+(a,)))
     if T!=A:lower=[x+val*y for x,y in zip(lower,cover[T])]
     lower=[x-val*y for x,y in zip(lower,cover[tuple(R)])]
    formal=[-x/beta for x in lower];formal[vindex[q,a]]+=1/beta
    expansions.append(formal)
   cover[A]=expansions[0]
   identities.extend([[x-y for x,y in zip(row,cover[A])] for row in expansions[1:]])
 # Every proposed formal identity vanishes on every actual type.
 cols=[[payoff(q,a,B) for q,a in vertices] for B in types]
 for row in identities:
  assert all(sum((x*y for x,y in zip(row,col)),Q(0))==0 for col in cols)
 d=sum(__import__('math').comb(p,k) for k in range(1,min(m,p)+1))
 assert len(identities)==N-d
 assert rank(identities)==N-d
 for q,a in vertices:
  for b in range(a+1,p):
   if q[b]!=q[a]:continue
   D=tuple(c for c in range(p) if q[c] and c not in (a,b))
   theta={R:lam(q,a,R,removed=(b,)) for R in subsets(D)}
   assert sum(theta.values(),Q(0))==Q(1,q[a])
   for B in types:
    rhs=sum((t*(cov(R+(a,),B)-cov(R+(b,),B)) for R,t in theta.items()),Q(0))
    assert rhs==payoff(q,a,B)-payoff(q,b,B)
    swaps+=1
 return dict(m=m,p=p,vertices=N,coverage_dimension=d,independent_identities=N-d,pointwise_marginals=checked,pointwise_swaps=swaps)

if __name__=='__main__':
 print(json.dumps([audit(m,p) for m,p in [(1,3),(2,4),(3,4),(4,3),(3,6)]],indent=2))
