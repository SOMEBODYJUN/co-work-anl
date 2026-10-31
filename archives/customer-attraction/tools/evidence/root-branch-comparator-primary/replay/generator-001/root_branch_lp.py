import itertools
from math import comb
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
m=5
n=9
base=np.array(list(itertools.product([0,1],repeat=n)),float).T
bits=np.repeat(base,6,axis=1)
j=np.tile(np.arange(6),base.shape[1]);o=(j>0).astype(float)
paths=[list(range(5)),[4,5,6,7,8]]
rows=[];names=[]
def add(name,row): rows.append(row);names.append(name)
def opt_sub_profit(p,k):
 vals=np.zeros(len(j))
 for d in range(1,6):
  sel=j==d
  for q in range(1,k+1):
   if q<=d and 0<=k-q<=5-d:vals[sel]+=comb(d,q)*comb(5-d,k-q)*q/(p[sel]+q)
 return vals
for r,path in enumerate(paths):
 c=bits[path].sum(axis=0)
 pay=np.divide(bits[path],c,out=np.zeros((5,len(c))),where=c>0)
 for i in range(0 if r==0 else 1,5):
  p=bits[path[:i]].sum(axis=0);k=5-i
  for t in range(n):add(f'{r}:{i}:K{t}',pay[i]-bits[t]/(p+k))
  add(f'{r}:{i}:sumopt',5*pay[i]-j/(p+k))
  add(f'{r}:{i}:O',5*k*pay[i]+p/(p+k)-o)
  if k in [3,4]:add(f'{r}:{i}:profit{k}',comb(5,k)*(5/3 if k==3 else 1499/750)*pay[i:].sum(axis=0)-opt_sub_profit(p,k))
 p=bits[path[:3]].sum(axis=0)
 H=pay[3]+pay[4]+bits[path[3]]/((p+1)*(p+2))
 add(f'{r}:twoO',2.5*H+p/(p+1)-o)
 add(f'{r}:twoj',10*H-(j*(5-j)/(p+1)+j*(j-1)/(p+2)))
 if r==0:actualpay=pay;W=(c>0).astype(float)
 else:branchpay=pay
add('root',actualpay[0]-branchpay[0])
A=np.array(rows)
z=linprog(-o,A_ub=csr_matrix(-A),b_ub=np.zeros(len(rows)),A_eq=W[None,:],b_eq=[1],bounds=(0,None),method='highs')
print('result',z.message,'nrow',len(rows),'ncol',len(o),'beta',-z.fun)
print('pays',actualpay@z.x,'branch',branchpay@z.x)
print('support',np.count_nonzero(z.x>1e-8))
print('dual',[(name,round(-d,8)) for name,d in zip(names,z.ineqlin.marginals) if d<-1e-8])
np.savez(__file__+'.npz',bits=bits,j=j,rows=A,W=W,weights=z.x,names=names)
