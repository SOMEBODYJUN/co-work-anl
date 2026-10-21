from probe_branch_endpoint import compositions
from itertools import product,combinations_with_replacement
import numpy as np
from scipy.optimize import linprog

def rows(n,ps):
 A=[];y=[];states=[];patterns=list(product(range(2),repeat=4)) # t,q,r,l
 for hist in compositions(n,16):
  seq=[]
  for h,v in zip(hist,patterns):seq.extend([v]*h)
  nums=[sum(s[j] for s in seq) for j in range(4)]
  overlaps=[[sum(s[j]*s[k] for s in seq) for k in range(4)] for j in range(4)]
  for p in ps:
   rootQ=sum(t/(p+1+q+r) for t,q,r,l in seq)
   mids=[q/(p+t+1+r) for t,q,r,l in seq];fins=[r/(p+t+q+1) for t,q,r,l in seq]
   hh=[mid+fin+q/((p+t+1)*(p+t+2)) for mid,fin,(t,q,r,l) in zip(mids,fins,seq)]
   ds=[1/(p+t+1) for t,q,r,l in seq];gs=[1/((p+t+1)*(p+t+2)) for t,q,r,l in seq]
   floor=sum(1/(p+t+2) for t,q,r,l in seq);prices=[1/(p+t+q+1) for t,q,r,l in seq];price=sum(prices)
   for a,b,c in product(range(2),repeat=3):
    s=a+b+c;alpha=a/(p+s) if a else 0;beta=b/(p+s) if b else 0;gamma=c/(p+s) if c else 0
    actual=[a,b,c]
    vals=[n*alpha-rootQ,n*alpha-nums[1]/(p+3),n*alpha-nums[2]/(p+3),n*alpha-nums[3]/(p+3)]
    vals.extend([n*sum(mids)-k*floor for k in nums]);vals.extend([sum(mids)-k*floor for k in actual])
    vals.extend([n*sum(fins)-k*price for k in nums]);vals.extend([sum(fins)-k*price for k in actual])
    vals.extend([n*gamma-k/(p+a+b+1) for k in nums]);vals.extend([n*beta-k/(p+a+2) for k in nums])
    for j in range(4):
     diag=sum(fin-seq[i][j]*prices[i] for i,fin in enumerate(fins));vals.extend([diag,n*sum(fins)-nums[j]*price-diag])
    for M,N in combinations_with_replacement(range(4),2):
     MM,NN,K=nums[M],nums[N],overlaps[M][N];acc=[0.]*5
     for i in range(n):
      mm,nn=seq[i][M],seq[i][N];h,d,g=hh[i],ds[i],gs[i]
      acc[0]+=h-(mm+nn)*d+mm*nn*g
      acc[1]+=(n-1)*h-(MM+NN-mm-nn)*d+(K-mm*nn)*g
      acc[2]+=(n-1)*h-((n-1)*mm+NN-nn)*d+mm*(NN-nn)*g
      acc[3]+=(n-1)*h-(MM-mm+(n-1)*nn)*d+(MM-mm)*nn*g
      acc[4]+=(n-1)*(n-2)*h-(n-2)*(MM+NN-mm-nn)*d+((MM-mm)*(NN-nn)-(K-mm*nn))*g
     vals.extend(acc)
    for z in actual:
     for M in range(4):
      diag=sum(hh[i]-(z+seq[i][M])*ds[i]+z*seq[i][M]*gs[i] for i in range(n))
      allrow=sum(n*hh[i]-(n*z+nums[M])*ds[i]+z*nums[M]*gs[i] for i in range(n));vals.extend([diag,allrow-diag])
    for z,zz in combinations_with_replacement(actual,2):vals.append(sum(hh[i]-(z+zz)*ds[i]+z*zz*gs[i] for i in range(n)))
    H=beta+gamma+b/((p+a+1)*(p+a+2));dd=1/(p+a+1);gg=1/((p+a+1)*(p+a+2))
    for M,N in combinations_with_replacement(range(4),2):
     diag=n*H-(nums[M]+nums[N])*dd+overlaps[M][N]*gg
     allrow=n*n*H-n*(nums[M]+nums[N])*dd+nums[M]*nums[N]*gg;vals.extend([diag,allrow-diag])
    # Full actual tail menu: second deviation T_i and genuine terminal L_i.
    vals.append(n*beta-nums[0]/(p+a+1)+overlaps[0][3]/((p+a+1)*(p+a+2)))
    for j in range(4):
     # each source (A,T_i), actual L_i; matched and unmatched query family j
     src=sum(seq[i][3]/(p+a+seq[i][0]+1) for i in range(n))
     diag=src-sum(seq[i][j]/(p+a+seq[i][0]+1) for i in range(n))
     allrow=n*src-nums[j]*sum(1/(p+a+seq[i][0]+1) for i in range(n));vals.extend([diag,allrow-diag])
    A.append(vals);y.append(int(p+s>0)+n*alpha-int(nums[0]>0));states.append((p,a,b,c,hist))
 return np.array(A),np.array(y),states
if __name__=='__main__':
 for n in [3,4]:
  A,y,states=rows(n,range(n-2));res=linprog(np.zeros(A.shape[1]),A_ub=A,b_ub=y,bounds=(0,None),method='highs')
  print(n,A.shape,res.success,res.x if res.success else res.message,flush=True)
