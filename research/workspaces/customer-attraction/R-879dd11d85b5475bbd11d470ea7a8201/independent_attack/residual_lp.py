"""Diagnostic only: two-player complete response menus vs residual union budget.
No finite search implies a general theorem. Float LP output requires exact audit.
"""
import itertools, random, numpy as np
from scipy.optimize import linprog

def coefficients(k):
 ts=np.arange(1,1<<k); bits=((ts[:,None]>>np.arange(k))&1).T
 def payoff(a,b,p):
  return bits[p]/(bits[a]+bits[b]+(bits[a]+bits[b]==0))
 def row(a,b,p):return payoff(a,b,p)
 return ts,bits,row

def attack(k=6,tries=5000,seed=1936):
 random.seed(seed); ts,bits,U=coefficients(k); best=0
 # Actual profile (0,1), comparison pair (2,3); other labels are suppressors.
 W=((bits[0]+bits[1])>0).astype(float)
 R=(((bits[2]+bits[3])>0)&(W==0)).astype(float)
 for z in range(tries):
  f=(1,)+tuple(random.randrange(k) for a in range(1,k))
  constraints=[]
  for a in range(k):
   for b in range(k):constraints.append(U(a,f[a],f[a])-U(a,b,b))
   constraints.append(U(0,1,0)-U(a,f[a],a))
  A=np.array(constraints)
  res=linprog(-R,A_ub=-A,b_ub=np.zeros(len(A)),A_eq=[W],b_eq=[1],bounds=(0,None),method='highs')
  if not res.success:continue
  val=-res.fun
  if val>best+1e-8:
   best=val;print('BEST',best,'f',f,'weights',[(int(ts[i]),round(w,12)) for i,w in enumerate(res.x) if w>1e-8],flush=True)
  if val>1+1e-8:return f,res.x
 print('done',k,tries,'best',best,flush=True)
if __name__=='__main__':attack()
