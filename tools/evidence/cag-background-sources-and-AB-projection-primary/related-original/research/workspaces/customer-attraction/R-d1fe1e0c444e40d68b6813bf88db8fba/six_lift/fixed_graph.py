"""Six-player true fixed-query graph. Necessary relaxation, never an SPE claim.

13 membership bits retain all six positions on three paths. The old 587
necessary rows are embedded, then every documented new row is added. Discovery
uses floats; --verify checks the saved sparse point entirely with Fraction.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import json, sys, time
import numpy as np
from scipy.optimize import linprog
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/proofs/half5_exact_v1').is_dir())
OLD=ROOT/'research/workspaces/customer-attraction/R-07e871289a6b4c1fb07244c97eb4aac8/three_certificate_comparison'
sys.path.insert(0,str(OLD))
from nested_horizon_refine import system as oldsystem
from six_stress import exact_solve
LABELS='ABCDEFGHIJKLM'
PATHS={'actual':'ABCDEF','second':'AFGHIJ','third':'ABFKLM'}
TRUE={'actual':tuple(range(6)),'second':tuple(range(2,6)),'third':tuple(range(3,6))}
N=6

def sh(a,path,j):
 z=sum(a[LABELS.index(c)] for c in path);v=a[LABELS.index(path[j])]
 return F(v,z) if v else F(0)
@lru_cache(None)
def projection(k,p,ell,t,q):
 alpha=(F(1,8),)*(k-2)+(F(1,5),);beta=F(1,20);mu=F(1,4)
 def val(f):
  z=p+t+sum(f)
  return ((F(t,z) if t else F(0))+sum(a*x for a,x in zip(alpha,f))/F(ell+1)
   +beta*f[-1]-mu*(F(f[-1],z) if f[-1] else F(0))+mu*F(q,p+t+sum(f[:-1])+1))
 return min(val(f) for f in product((0,1),repeat=k-1))

def new_specs(priced=False):
 specs=[]
 def add(x):specs.append(tuple(x))
 for label in LABELS:add(('cap',label))
 for tag,path in PATHS.items():
  for j in TRUE[tag]:
   for label in LABELS:add(('floor',tag,j,label))
   add(('optfloor',tag,j));add(('ofloor',tag,j))
  for qi,q in enumerate(LABELS):
   for r in LABELS[qi:]:add(('pair',tag,q,r))
   add(('pair-opt',tag,q))
  add(('pair-diag',tag));add(('pair-off',tag));add(('pair-o',tag))
  if priced:
   for j in TRUE[tag]:
    if j>=5:continue
    # Rows at actual sources with actual queries already occur in old587;
    # retaining them again is harmless and records a uniform graph rule.
    for t in LABELS:
     for q in LABELS:add(('priced',tag,j,t,q))
    for t in LABELS:
     add(('priced-t-opt',tag,j,t));add(('priced-opt-q',tag,j,t))
    add(('priced-diag',tag,j));add(('priced-off',tag,j))
 for tag,j in [('second',1),('third',2)]:add(('forced',tag,j))
 return specs

def exact_new(s,a,d):
 kind=s[0];bb=lambda c:a[LABELS.index(c)]
 if kind=='cap':return -F(bb(s[1])),F(1)
 tag=s[1];path=PATHS[tag]
 if kind=='forced':return sh(a,PATHS['actual'],s[2])-sh(a,path,s[2]),F(0)
 if kind in ('floor','optfloor','ofloor'):
  j=s[2];p=sum(bb(c) for c in path[:j]);den=p+N-j;u=sh(a,path,j)
  if kind=='floor':return u-F(bb(s[3]),den),F(0)
  if kind=='optfloor':return N*u-F(d,den),F(0)
  return N*(N-j)*u+F(p,den)-int(d>0),F(0)
 if kind.startswith('pair'):
  p=sum(bb(c) for c in path[:4]);delta=(p+1)*(p+2)
  H=sh(a,path,4)+sh(a,path,5)+F(bb(path[4]),delta)
  if kind=='pair':return H-F(bb(s[2])+bb(s[3]),p+1)+F(bb(s[2])*bb(s[3]),delta),F(0)
  if kind=='pair-opt':return N*H-F(N*bb(s[2])+d,p+1)+F(bb(s[2])*d,delta),F(0)
  if kind=='pair-diag':return N*H-F(2*d,p+1)+F(d,delta),F(0)
  if kind=='pair-off':return N*(N-1)*H-F(2*(N-1)*d,p+1)+F(d*(d-1),delta),F(0)
  return F(N,2)*H+F(p,p+1)-int(d>0),F(0)
 if kind.startswith('priced'):
  j=s[2];k=N-j;p=sum(bb(c) for c in path[:j]);ell=sum(a[:5])
  u=sh(a,path,j)+(F(k-2,8)+F(1,5))*sh(a,PATHS['actual'],5)
  psi=lambda t,q:projection(k,p,ell,t,q)
  if kind=='priced':credit=psi(bb(s[3]),bb(s[4]))
  elif kind=='priced-t-opt':credit=F(N-d,N)*psi(bb(s[3]),0)+F(d,N)*psi(bb(s[3]),1)
  elif kind=='priced-opt-q':credit=F(N-d,N)*psi(0,bb(s[3]))+F(d,N)*psi(1,bb(s[3]))
  elif kind=='priced-diag':credit=F(N-d,N)*psi(0,0)+F(d,N)*psi(1,1)
  else:
   count={(1,1):d*(d-1),(1,0):d*(N-d),(0,1):d*(N-d),(0,0):(N-d)*(N-d-1)}
   credit=sum(F(v,N*(N-1))*psi(t,q) for (t,q),v in count.items())
  return u-credit,F(1,20)
 raise ValueError(s)

class Model:
 def __init__(self,priced=False):
  self.oldtypes,self.oldrows,_=oldsystem()
  self.oldlookup={t:i for i,t in enumerate(self.oldtypes)}
  self.specs=new_specs(priced)
  self.bits=np.array(list(product((0,1),repeat=13)),dtype=np.int8)
  self.a=np.repeat(self.bits,7,axis=0);self.d=np.tile(np.arange(7),len(self.bits))
  self.oldids=np.array([self.oldlookup[(tuple(a[:6]),int(d))] for a,d in zip(self.a,self.d)])
  self.names=['old:'+name for name,row in self.oldrows]+['new:'+':'.join(map(str,s)) for s in self.specs]
  self.w=np.r_[(self.a[:,:6].sum(axis=1)>0).astype(float),0.]
  self.o=np.r_[(self.d>0).astype(float),0.]
 def exact(self,i,a,d):
  if i<len(self.oldrows):
   row=self.oldrows[i][1];return row[self.oldlookup[(tuple(a[:6]),d)]],row[-1]
  return exact_new(self.specs[i-len(self.oldrows)],a,d)
 def matrix(self):
  print('building',len(self.names),'rows',len(self.w),'columns',flush=True)
  mat=np.empty((len(self.names),len(self.w)),dtype=np.float32)
  oldmat=np.array([[float(x) for x in row] for _,row in self.oldrows],dtype=np.float32)
  mat[:len(self.oldrows),:-1]=oldmat[:,self.oldids];mat[:len(self.oldrows),-1]=oldmat[:,-1]
  # Every raw coefficient depends on the fixed bits and d. Compute exact
  # unique signatures, cache by the memberships actually occurring in a row.
  for i,s in enumerate(self.specs,len(self.oldrows)):
   involved=set()
   if s[0]=='cap':involved.add(s[1])
   else:
    involved.update(PATHS[s[1]])
    if s[0]=='forced':involved.update(PATHS['actual'])
    if s[0] in ('floor','pair','pair-opt'):involved.update(x for x in s[2:] if isinstance(x,str))
    if s[0].startswith('priced'):
     involved.update(PATHS['actual']);involved.update(x for x in s[3:] if isinstance(x,str))
   ids=sorted(LABELS.index(c) for c in involved)
   sig=(self.a[:,ids]*(1<<np.arange(len(ids)))).sum(axis=1)*7+self.d
   vals=np.zeros((1<<len(ids))*7,dtype=np.float32);kap=None
   for code in range(1<<len(ids)):
    aa=[0]*13
    for k,j in enumerate(ids):aa[j]=(code>>k)&1
    for dd in range(7):
     v,kap=exact_new(s,aa,dd);vals[code*7+dd]=float(v)
   mat[i,:-1]=vals[sig];mat[i,-1]=float(kap)
   if i%100==0:print('built',i,flush=True)
  # Positive row scaling is harmless and improves HiGHS conditioning.
  self.norm=np.maximum(1.,np.max(np.abs(mat),axis=1))
  mat/=self.norm[:,None]
  return mat

def discover(priced=False):
 model=Model(priced);mat=model.matrix();rng=np.random.default_rng(20261026)
 selected=set(rng.choice(len(model.w)-1,size=1000,replace=False));selected.add(len(model.w)-1)
 # Seed with every combination of actual bits and d, extending off branches
 # by zero and by all ones; do not assert those extensions are realizable.
 for idx in range(448):selected.add(idx)
 for iteration in range(100):
  ids=np.array(sorted(selected));sub=np.asarray(mat[:,ids],dtype=np.float64)
  sol=linprog(model.w[ids],A_ub=-sub,b_ub=np.zeros(len(model.names)),A_eq=[model.o[ids]],b_eq=[1.],bounds=(0,None),method='highs')
  assert sol.success,sol.message
  lam=-sol.ineqlin.marginals;nu=sol.eqlin.marginals[0]
  residual=model.w-model.o*nu-lam@mat
  neg=np.flatnonzero(residual < -2e-7)
  print('round',iteration,'value',sol.fun,'columns',len(ids),'minrc',float(residual.min()),'negative',len(neg),flush=True)
  if not len(neg):break
  # Best cost columns plus a random negative sample prevent one orbit from
  # monopolizing the restricted master.
  picks=neg[np.argsort(residual[neg])[:250]]
  selected.update(map(int,picks))
  if len(neg)>250:selected.update(map(int,rng.choice(neg,size=min(250,len(neg)),replace=False)))
 else:raise RuntimeError('column generation did not converge')
 support=[int(ids[j]) for j,x in enumerate(sol.x) if x>1e-8]
 xs=[sol.x[j] for j,x in enumerate(sol.x) if x>1e-8]
 print('rationalizing',len(support),'support',flush=True)
 # Exact equations from active constraints, evaluated from row definitions.
 pointtypes=[(tuple(map(int,model.a[j])),int(model.d[j])) if j<len(model.w)-1 else None for j in support]
 active=np.flatnonzero(np.abs(sub@sol.x)<1e-7)
 eqs=[]
 for i in active:
  vals=[]
  for pt in pointtypes:
   if pt is None:vals.append(model.exact(int(i),(0,)*13,0)[1])
   else:vals.append(model.exact(int(i),*pt)[0])
  eqs.append(vals+[F(0)])
 eqs.append([F(model.o[j]) for j in support]+[F(1)])
 exact=exact_solve(eqs,len(support))
 assert min(exact)>=0
 data={'scope':'Necessary row relaxation, not SPE; indexed reply families not retained',
 'labels':LABELS,'paths':PATHS,'true_positions_zero_based':TRUE,'priced':priced,
 'n_rows':len(model.names),'n_columns':len(model.w),'W':str(sum(F(model.w[j])*x for j,x in zip(support,exact))),
 'O':'1','K':str(sum(x for j,x in zip(support,exact) if j==len(model.w)-1)),
 'support':[{'bits':''.join(map(str,pt[0])),'d':pt[1],'weight':str(x)} for pt,x in zip(pointtypes,exact) if pt is not None and x],
 'floating_column_generation_value':float(sol.fun),'rounds':iteration+1}
 out=Path(__file__).with_name('fixed_graph_priced.json' if priced else 'fixed_graph_raw.json')
 out.write_text(json.dumps(data,indent=2)+'\n');verify(out)

def verify(path):
 data=json.loads(Path(path).read_text());model=Model(data['priced'])
 pts=[(tuple(map(int,x['bits'])),x['d'],F(x['weight'])) for x in data['support']]
 K=F(data['K']);assert K>=0 and min(x[2] for x in pts)>=0
 O=sum(v for a,d,v in pts if d>0);W=sum(v for a,d,v in pts if any(a[:6]));assert O==1 and str(W)==data['W']
 slacks=[]
 for i,name in enumerate(model.names):
  kap=model.exact(i,(0,)*13,0)[1]
  slack=kap*K+sum(model.exact(i,a,d)[0]*v for a,d,v in pts)
  assert slack>=0,(name,slack)
  slacks.append(slack)
 assert W<F(1,2)
 report={'exact_verified':True,'W':str(W),'O':str(O),'twice_W_minus_O':str(2*W-O),
 'n_rows':len(slacks),'support_size':len(pts),'minimum_slack':str(min(slacks)),
 'zero_rows':sum(v==0 for v in slacks),'scope':data['scope']}
 Path(path).with_name(Path(path).stem+'_verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
 if '--verify' in sys.argv:verify(sys.argv[-1])
 else:discover('--priced' in sys.argv)
