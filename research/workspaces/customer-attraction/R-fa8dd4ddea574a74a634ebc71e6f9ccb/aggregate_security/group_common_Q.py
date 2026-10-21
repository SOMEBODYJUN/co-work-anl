"""Floating common-Q separation for the three-player opposite-group policy.
A returned certificate must be exactly reconstructed before claiming a theorem.
"""
from pathlib import Path
from itertools import product,combinations_with_replacement
import argparse,json,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix,csr_matrix,hstack,vstack

def probe(t, simple=False, within=False, rational=False):
 k=2*t;n=3;d=(1<<k)-1
 masks=np.arange(1,1<<k);M=((masks[None,:]>>np.arange(k)[:,None])&1).astype(float)
 actions={():0}
 for a in range(k):
  actions[a,]=t if a<t else 0
  for b in range(k):actions[a,b]=next(c for c in (range(t) if b<t else range(t,k)) if c not in (a,b))
 def terminal(h):
  while len(h)<n:h=h+(actions[h],)
  return h
 def rho(a,h):return M[a]/np.maximum(M[list(h)].sum(axis=0),1)
 G=[];labels=[]
 for h,a in actions.items():
  z=terminal(h)
  for b in range(k):
   if b!=a:G.append(rho(a,z)-rho(b,terminal(h+(b,))));labels.append((h,b))
 G=np.array(G);gs=len(G);bs=list(combinations_with_replacement(range(k),n-1));nb=len(bs)
 root=terminal(());budget=rho(root[0],root)+rho(root[1],root)
 vals=[]
 for a in range(k):
  beta=np.array([M[a]/(1+M[list(bg)].sum(axis=0)) for bg in bs])
  left=csr_matrix(2*beta.T)
  blocks=[csr_matrix((d,gs)) for _ in range(k)];blocks[a]=csr_matrix(G.T)
  vals.append(hstack([left,*blocks],format='csr'))
 A=vstack(vals,format='csr');eq=csr_matrix((np.ones(nb),(np.zeros(nb),np.arange(nb))),shape=(1,nb+k*gs))
 bounds=[(0,None)]*(nb+k*gs)
 if simple:
  for j,bg in enumerate(bs):bounds[j]=(.5,.5) if bg in [(0,1),(t,t+1)] else (0,0)
 if within:
  for j,(a,b) in enumerate(bs):bounds[j]=(0,None) if a!=b and (a<t)==(b<t) else (0,0)
 if rational:
  for j,bg in enumerate(bs):bounds[j]=(7/12,7/12) if bg==(0,1) else (5/12,5/12) if bg==(0,2) else (0,0)
 start=time.time();res=linprog(np.r_[np.zeros(nb),np.ones(k*gs)],A_ub=A,b_ub=np.tile(budget,k),A_eq=eq,b_eq=[1],bounds=bounds,method='highs')
 out={'t':t,'k':k,'scope':'floating fixed formal strategy cone, not a general result','status':res.status,'message':res.message,'seconds':time.time()-start}
 if res.success:
  out['Q']=[{'B':bg,'p':float(p)} for bg,p in zip(bs,res.x[:nb]) if p>1e-8]
  out['lambda']=[{'a':a,'h':labels[j][0],'b':labels[j][1],'value':float(res.x[nb+a*gs+j])} for a in range(k) for j in range(gs) if res.x[nb+a*gs+j]>1e-8]
  out['min_remainder']=float(np.min(np.tile(budget,k)-A@res.x))
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--group',type=int,default=3);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--simple',action='store_true');ap.add_argument('--within',action='store_true');ap.add_argument('--rational',action='store_true');a=ap.parse_args();o=probe(a.group,a.simple,a.within,a.rational);a.output.write_text(json.dumps(o,indent=2)+'\n');print(json.dumps(o,indent=2))
