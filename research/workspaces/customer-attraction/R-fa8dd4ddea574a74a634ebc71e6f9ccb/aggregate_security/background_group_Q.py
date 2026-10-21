"""Sufficient common-Q polynomial coefficient certificate for arbitrary customer backgrounds.
Multiply each residual by (b+1)(b+2)(b+3), require nonnegative coefficients.
Floating discovery only until exact independent reconstruction.
"""
from pathlib import Path
from itertools import product,combinations_with_replacement
import argparse,json,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,hstack,vstack

def probe(t):
 k=2*t;n=3;types=(1<<k)-1;d=3*types
 masks=np.arange(1,1<<k);M=((masks[None,:]>>np.arange(k)[:,None])&1).astype(float)
 # increasing polynomial order, row indexed by denominator.
 P=np.array([[0,0,0],[6,5,1],[3,4,1],[2,3,1]])
 actions={():0}
 for a in range(k):
  actions[a,]=t if a<t else 0
  for b in range(k):actions[a,b]=next(c for c in (range(t) if b<t else range(t,k)) if c not in (a,b))
 def terminal(h):
  while len(h)<n:h=h+(actions[h],)
  return h
 def rho(a,h):return (M[a,:,None]*P[M[list(h)].sum(axis=0).astype(int)]).flatten()
 G=[];labels=[]
 for h,a in actions.items():
  for b in range(k):
   if b!=a:G.append(rho(a,terminal(h))-rho(b,terminal(h+(b,))));labels.append((h,b))
 G=np.array(G);gs=len(G);bs=list(combinations_with_replacement(range(k),n-1));nb=len(bs)
 root=terminal(());budget=rho(root[0],root)+rho(root[1],root)
 blocks=[]
 for a in range(k):
  beta=np.array([rho(a,bg+(a,)) for bg in bs]);row=[csr_matrix(2*beta.T)]+[csr_matrix(G.T) if a==aa else csr_matrix((d,gs)) for aa in range(k)]
  blocks.append(hstack(row,format='csr'))
 A=vstack(blocks,format='csr');eq=csr_matrix((np.ones(nb),(np.zeros(nb),np.arange(nb))),shape=(1,nb+k*gs))
 res=linprog(np.r_[np.zeros(nb),np.ones(k*gs)],A_ub=A,b_ub=np.tile(budget,k),A_eq=eq,b_eq=[1],bounds=(0,None),method='highs')
 out={'t':t,'k':k,'scope':'floating fixed-policy cone, polynomial coefficient sufficiency for all nonnegative customer backgrounds','status':res.status,'message':res.message}
 if res.success:
  out['Q']=[{'B':bg,'p':float(p)} for bg,p in zip(bs,res.x[:nb]) if p>1e-8]
  out['lambda']=[{'a':a,'h':labels[j][0],'b':labels[j][1],'value':float(res.x[nb+a*gs+j])} for a in range(k) for j in range(gs) if res.x[nb+a*gs+j]>1e-8]
  out['min_remainder']=float(np.min(np.tile(budget,k)-A@res.x))
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--group',type=int,default=3);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();o=probe(a.group);a.output.write_text(json.dumps(o,indent=2)+'\n');print(json.dumps(o,indent=2))
