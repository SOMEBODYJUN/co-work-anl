"""Targeted original-model full-count-policy cone attack from the 18-action seed.

Floating discovery only. Every cone constraint is a genuine one-step SPE IC at
all count histories; a count selector defines a strategy at every ordered
history. Strict candidates require rational recovery and exact full verification.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from itertools import combinations
from pathlib import Path
import argparse,json,time
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent

def compositions(n,k):
 if k==1:yield (n,);return
 for v in range(n+1):
  for w in compositions(n-v,k-1):yield(v,)+w

class Attack:
 def __init__(self,seed):
  self.k=len(seed['topics']);self.m=seed['players'];self.cust=seed['customers'];self.n=len(self.cust)
  self.inc=np.array([[int(j in q['topics']) for j in range(self.k)] for q in self.cust],dtype=np.int8)
  total=sum(q['multiplicity'] for q in self.cust);self.initial=np.array([q['multiplicity']/total for q in self.cust],dtype=float)
  self.levels=[list(compositions(t,self.k)) for t in range(self.m+1)]
  self.term=np.array(self.levels[-1],dtype=np.int8)
  load=self.term@self.inc.T
  self.inv=np.zeros_like(load,dtype=np.int8)
  for d in range(1,self.m+1):self.inv[load==d]=60//d
  self.cover=load>0
  self.child=[]
  for r in range(self.m):
   ix={q:j for j,q in enumerate(self.levels[r+1])}
   self.child.append(np.array([[ix[q[:a]+(q[a]+1,)+q[a+1:]] for a in range(self.k)] for q in self.levels[r]],dtype=np.int32))
  self.opt_supports=list(combinations(range(self.k),min(self.m,self.k)))
  self.opts=np.array([(self.inc[:,c].sum(axis=1)>0) for c in self.opt_supports],dtype=np.int8)
  print('BUILT',self.k,self.n,'term',len(self.term),'nodes',sum(map(len,self.levels[:-1])),'opts',len(self.opts),flush=True)
 def payoffs(self,w):
  if self.n<=256:return (self.inv*(w/60)[None,:])@self.inc
  ans=np.empty((len(self.term),self.k))
  for start in range(0,len(self.term),2048):ans[start:start+2048]=(self.inv[start:start+2048]*(w/60)[None,:])@self.inc
  return ans
 def policy(self,w,rng,tol=1e-10):
  U=self.payoffs(w);W=self.cover@w;T=[None]*(self.m+1);A=[None]*self.m;T[-1]=np.arange(len(self.term),dtype=np.int32)
  for r in range(self.m-1,-1,-1):
   leaves=T[r+1][self.child[r]];scores=U[leaves,np.arange(self.k)[None,:]]
   valid=scores>=np.max(scores,axis=1)[:,None]-tol
   if rng.random()<.8:
    vals=np.where(valid,W[leaves],np.inf);valid &= vals<=np.min(vals,axis=1)[:,None]+tol
   coin=rng.random(scores.shape);coin[~valid]=-1
   A[r]=coin.argmax(axis=1);T[r]=leaves[np.arange(len(leaves)),A[r]]
  keys=[]
  for r in range(self.m):
   dst=T[r+1][self.child[r]];src=np.repeat(T[r],self.k);aa=np.repeat(A[r],self.k);jj=np.tile(np.arange(self.k),len(A[r]));dd=dst.reshape(-1)
   take=aa!=jj;keys.append(np.column_stack((src[ take],aa[take],dd[take],jj[take])))
  keys=np.unique(np.concatenate(keys),axis=0)
  return A,T,keys
 def row(self,keys):
  # deviation minus prescribed, multiplied by 60.
  return self.inv[keys[:,2]].astype(np.int16)*self.inc[:,keys[:,3]].T-self.inv[keys[:,0]].astype(np.int16)*self.inc[:,keys[:,1]].T
 def optimize(self,A,T,keys,w,rng,side=False):
  root=T[0][0];optid=int(np.argmax(self.opts@w));obj=self.opts[optid].astype(float)
  W=self.cover[root].astype(float)
  # Discover full cone using cuts, never discard a violated global IC.
  selected=set();rows=[];oldw=w.copy();ans=None
  for iteration in range(80):
   if ans is not None:
    U=self.payoffs(ans.x);viol=U[keys[:,2],keys[:,3]]-U[keys[:,0],keys[:,1]]
    ids=np.flatnonzero(viol>2e-9)
    if not len(ids):return ans,optid,root,iteration,len(selected),float(viol.max(initial=0))
    ids=ids[np.argsort(viol[ids])[-min(1500,len(ids)):]]
   else:
    # Begin with source rows tight at current point plus reproducible samples.
    U=self.payoffs(w);viol=U[keys[:,2],keys[:,3]]-U[keys[:,0],keys[:,1]]
    ids=np.r_[np.argsort(viol)[-1000:],rng.choice(len(keys),min(1000,len(keys)),replace=False)]
   new=[int(i) for i in ids if int(i) not in selected]
   if not new:return None,optid,root,iteration,len(selected),float(viol.max())
   selected.update(new);rows.extend(self.row(keys[new]))
   coef=np.array(rows,dtype=float)/60
   if side:
    coef=np.vstack([coef,-obj]);rhs=np.r_[np.zeros(len(rows)),-side]
    target=rng.normal(size=self.n)
   else:rhs=np.zeros(len(rows));target=obj
   ans=linprog(-target,A_ub=coef,b_ub=rhs,A_eq=[W],b_eq=[1],bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
   if not ans.success:return ans,optid,root,iteration,len(selected),None
  return None,optid,root,80,len(selected),None
 def save(self,path,w,A,T,keys,ratio,optid,check):
  data={'status':'float full-count-policy feasible candidate, exact recovery required','topics':list(range(self.k)),'players':self.m,'support_customers':self.cust,'weights':w.tolist(),'ratio':ratio,'comparison':self.opt_supports[optid],'root':self.term[T[0][0]].tolist(),'all_count_IC_keys':len(keys),'floating_check':check,'policy':[{','.join(map(str,q)):int(a) for q,a in zip(self.levels[r],A[r])} for r in range(self.m)]}
  path.write_text(json.dumps(data,indent=2)+'\n')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--steps',type=int,default=20);ap.add_argument('--seed',type=int,default=33791);ap.add_argument('--input',type=Path,default=HERE.parent/'research_6/seed_full18.json');a=ap.parse_args();start=time.time();C=Attack(json.loads(a.input.read_text()));rng=np.random.default_rng(a.seed);w=C.initial.copy();best=0
 for step in range(a.steps):
  if step and step%10==0:w=C.initial*(rng.exponential(1,size=C.n)+.05)
  A,T,keys=C.policy(w,rng,tol=1e-10)
  ans,optid,root,ncut,nrow,viol=C.optimize(A,T,keys,w,rng)
  if ans is None or not ans.success:
   print('FAIL',step,None if ans is None else ans.message,ncut,nrow,viol,flush=True);w=C.initial*(rng.exponential(1,size=C.n)+.05);continue
  val=float(C.opts[optid]@ans.x)
  print('STEP',step,'ratio',val,'root',C.term[root].tolist(),'keys',len(keys),'cuts',ncut,nrow,'maxviol',viol,'seconds',time.time()-start,flush=True)
  if val>best+1e-8:
   best=val;C.save(HERE/'full18_best_float.json',ans.x,A,T,keys,val,optid,{'maximum_positive_IC_violation':viol})
  if val>2+1e-6:print('STRICT_TARGET_CANDIDATE',flush=True);break
  noise=C.initial*(rng.exponential(1,size=C.n)+.01);eps=float(rng.choice([1e-7,1e-5,.001,.03,.2]));w=np.maximum(ans.x,0)+eps*noise
 print('END',best,'seconds',time.time()-start,flush=True)
if __name__=='__main__':main()
