"""Discovery of two-player coefficient certificates using response-chain closure.
Finite LP feasibility is only for the specified named-branch template.
"""
from itertools import product
import argparse
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog

def attempt(depth,mode='whole'):
 # Actual A->B; two comparison themes follow two named response chains.
 labels=['A','B','T','S'];response={'A':'B'}
 chains=[['T'],['S']]
 for d in range(depth):
  for j in range(2):
   new=f'R{j}_{d}';labels.append(new);response[chains[j][-1]]=new;chains[j].append(new)
 parents=list(response)
 slacks=[('root',a,None)for a in parents if a!='A']
 slacks +=[('follow',p,t)for p in parents for t in labels if t!=response[p]]
 rows=[];rhs=[]
 for bt in product((0,1),repeat=len(labels)):
  bits=dict(zip(labels,bt))
  def u(a,b,p):return bits[a]*(p+2-bits[b])
  def vals(p):
   return [u('A','B',p)-u(a,response[a],p) if typ=='root' else u(response[a],a,p)-u(t,a,p)for typ,a,t in slacks]
  v0,v1,v2=(vals(p)for p in(0,1,2))
  a,b,t,s=[bits[z]for z in('A','B','T','S')]
  covered=a+b-a*b;opt=t+s-t*s
  if mode=='whole':f0=2*(2*covered-opt)
  elif mode=='residual':f0=2*(covered-(1-a)*(1-b)*opt)
  f1=3*(a+b)-2*a*b;slope=a+b
  rows +=[v0,v1,[y-x for x,y in zip(v1,v2)]];rhs +=[f0,f1,slope]
 result=linprog(np.ones(len(slacks)),A_ub=np.array(rows),b_ub=np.array(rhs),bounds=(0,None),method='highs')
 print('depth',depth,'mode',mode,'labels',len(labels),'slacks',len(slacks),result.message,flush=True)
 if result.success:
  lam=[Fraction(v).limit_denominator(100000)for v in result.x]
  residual=[Fraction(b)-sum((Fraction(v)*c for v,c in zip(row,lam)),Fraction())for row,b in zip(rows,rhs)]
  print('residual',min(residual));print([(slacks[i],str(v))for i,v in enumerate(lam)if v],flush=True)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--depth',type=int,default=2);p.add_argument('--mode',default='whole');a=p.parse_args();attempt(a.depth,a.mode)
