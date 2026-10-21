from probe_branch_endpoint import compositions
from itertools import product,combinations_with_replacement
import numpy as np
from scipy.optimize import linprog

def rows(n,ps):
 A=[];y=[];states=[];patterns=list(product(range(2),repeat=3))
 for hist in compositions(n,8):
  seq=[]
  for h,v in zip(hist,patterns):seq.extend([v]*h)
  nums=[sum(s[j] for s in seq) for j in range(3)]
  for p in ps:
   rootQ=sum(t/(p+1+q+r) for t,q,r in seq)
   mids=[q/(p+t+1+r) for t,q,r in seq]; fins=[r/(p+t+q+1) for t,q,r in seq]
   hh=[mid+fin+q/((p+t+1)*(p+t+2)) for mid,fin,(t,q,r) in zip(mids,fins,seq)]
   ds=[1/(p+t+1) for t,q,r in seq]; gs=[1/((p+t+1)*(p+t+2)) for t,q,r in seq]
   floor=sum(1/(p+t+2) for t,q,r in seq);price=sum(1/(p+t+q+1) for t,q,r in seq)
   for a,b,c in product(range(2),repeat=3):
    s=a+b+c;alpha=a/(p+s) if a else 0;beta=b/(p+s) if b else 0;gamma=c/(p+s) if c else 0
    actual=[a,b,c]
    vals=[n*alpha-rootQ,n*alpha-nums[1]/(p+3),n*alpha-nums[2]/(p+3)]
    vals.extend([n*sum(mids)-k*floor for k in nums]);vals.extend([sum(mids)-k*floor for k in actual])
    vals.extend([n*sum(fins)-k*price for k in nums]);vals.extend([sum(fins)-k*price for k in actual])
    vals.extend([n*gamma-k/(p+a+b+1) for k in nums]);vals.extend([n*beta-k/(p+a+2) for k in nums])
    for j in range(3):
     diag=sum(fin-seq[i][j]/(p+seq[i][0]+seq[i][1]+1) for i,fin in enumerate(fins))
     vals.extend([diag,n*sum(fins)-nums[j]*price-diag])
    # Branch retained-overlap taxes, all equality patterns i,j,k.
    for M,N in combinations_with_replacement(range(3),2):
     acc=[0.]*5
     for i in range(n):
      for j in range(n):
       for k in range(n):
        typ=0 if i==j==k else 1 if j==k else 2 if i==j else 3 if i==k else 4
        acc[typ]+=hh[i]-(seq[j][M]+seq[k][N])*ds[i]+seq[j][M]*seq[k][N]*gs[i]
     vals.extend(acc)
    # Branch tax fixed actual queries and family queries.
    for z in actual:
     for M in range(3):
      diag=sum(hh[i]-(z+seq[i][M])*ds[i]+z*seq[i][M]*gs[i] for i in range(n))
      allrow=sum(n*hh[i]-(n*z+nums[M])*ds[i]+z*nums[M]*gs[i] for i in range(n))
      vals.extend([diag,allrow-diag])
    for z,zz in combinations_with_replacement(actual,2):
     vals.append(sum(hh[i]-(z+zz)*ds[i]+z*zz*gs[i] for i in range(n)))
    # Actual tail tax and all family pairs, diagonal and offdiagonal.
    H=beta+gamma+b/((p+a+1)*(p+a+2));dd=1/(p+a+1);gg=1/((p+a+1)*(p+a+2))
    for M,N in combinations_with_replacement(range(3),2):
     overlap=sum(seq[i][M]*seq[i][N] for i in range(n))
     diag=n*H-(nums[M]+nums[N])*dd+overlap*gg
     allrow=n*n*H-n*(nums[M]+nums[N])*dd+nums[M]*nums[N]*gg
     vals.extend([diag,allrow-diag])
    A.append(vals);y.append(int(p+s>0)+n*alpha-int(nums[0]>0));states.append((p,a,b,c,hist))
 return np.array(A),np.array(y),states
if __name__=='__main__':
 for n in [3,4,5]:
  A,y,states=rows(n,range(n-2))
  res=linprog(np.zeros(A.shape[1]),A_ub=A,b_ub=y,bounds=(0,None),method='highs')
  print(n,A.shape,res.success,res.x if res.success else res.message,flush=True)
