"""Joint old R/Z atoms and new B -> D,E promotion at the actual fourth source.
Discovery restricts old histograms, never a full-domain half proof.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import sys,json,time,argparse
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
PREV=ROOT/'research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/closure'
sys.path.insert(0,str(PREV));import joint_atoms as ja
import early_reply_promotion as ep

class Model:
 def __init__(self):
  self.oldnames,oldk,self.locs=ja.model();self.no=len(self.oldnames);self.nn=len(ep.NAMES)
  self.groups=[(hi,wi) for hi,loc in enumerate(self.locs) for wi,n in enumerate(loc['hist']['hist']) if n]
  self.gi={key:j for j,key in enumerate(self.groups)};self.nr=self.no+self.nn+len(self.groups)
  self.names=self.oldnames+[str(n) for n in ep.NAMES]+['promotion-state-upper:'+str(k) for k in self.groups]
  self.k=oldk+[F(6) if isinstance(n,tuple) and n[0]=='capacity' else F() for n in ep.NAMES]+[F()]*len(self.groups)
  self.constants=[];self.ykeys=[];self.ycols=[]
  for hi,loc in enumerate(self.locs):
   h=tuple(loc['hist']['hist']);a=tuple(map(int,loc['hist']['actual_bits']));const=[F()]*self.nn
   for wi,(word,n) in enumerate(zip(ep.PAT,h)):
    if not n:continue
    base=ep.coefficients(a,h,word,(0,0));const=[c+n*v for c,v in zip(const,base)]
    for de in ((0,1),(1,0),(1,1)):
     raw=ep.coefficients(a,h,word,de)
     col=[F()]*self.no+[n*(x-y) for x,y in zip(raw,base)]+[F()]*len(self.groups)
     col[self.no+self.nn+self.gi[hi,wi]]=-F(1)
     self.ykeys.append((hi,wi,de));self.ycols.append(col)
   bounds=[F(int(g==hi)) for g,wi in self.groups]
   self.constants.append(const+bounds)
 def atom(self,key,exact=False):
  hi,r,z=key
  if exact:return ja.atom(self.locs[hi],r,z,True)+self.constants[hi]
  return np.r_[ja.atom(self.locs[hi],r,z),np.array(self.constants[hi],float)]

def recover(model,keys,sol):
 ny=len(model.ycols);keep=[j for j,v in enumerate(sol) if v>1e-8];cols=[]
 for j in keep:
  cols.append(model.k if j==0 else model.ycols[j-1] if j<=ny else model.atom(keys[j-ny-1],True))
 matrix=list(map(list,zip(*cols)));values=sol[keep];equations=[]
 for row in matrix:
  scale=max([float(abs(v)) for v in row]+[1e-30])
  if abs(np.array(row,float)@values)<2e-8*scale:equations.append(row+[F()])
 norm=[F() if j<=ny else model.locs[keys[j-ny-1][0]]['norm'] for j in keep]
 equations.append(norm+[F(1)])
 vals=ja.exact_solve(equations,len(keep));assert min(vals)>=0
 slacks=[sum(x*y for x,y in zip(row,vals)) for row in matrix];assert min(slacks)>=0,(model.names[slacks.index(min(slacks))],min(slacks))
 K=F();ys=[];ats=[];W=F()
 for j,v in zip(keep,vals):
  if j==0:K=v
  elif j<=ny:
   hi,wi,de=model.ykeys[j-1];ys.append({'hist_index':hi,'word_index':wi,'DE':list(de),'weight':str(v)})
  else:
   hi,r,z=keys[j-ny-1];ats.append({'hist_index':hi,'R':list(r),'Z':list(z),'weight':str(v)});W+=v*model.locs[hi]['obj']
 assert W<F(1,2)
 return {'scope':'exact feasible necessary-system point; 1143 old raw families + full 88 promotion raw rows and state-mass bounds; not a game/SPE/half result','O':'1','W':str(W),'K':str(K),'rows':model.nr,'minimum_slack':str(min(slacks)),'histograms':[loc['hist'] for loc in model.locs],'groups':[[[g[0],g[1],list(g[2]),list(g[3])] for g in loc['groups']] for loc in model.locs],'RZ_atoms':ats,'promotion_states':ys}

def main(args):
 start=time.time();m=Model();ny=len(m.ycols);rng=np.random.default_rng(args.seed);keys=[];vectors=[];seen=set()
 def add(hi,r,z):
  key=(hi,tuple(map(int,r)),tuple(map(int,z)))
  if key in seen:return False
  seen.add(key);keys.append(key);vectors.append(m.atom(key));return True
 frozen=json.loads((PREV/'joint_atoms_exact.json').read_text())
 for a in frozen['atoms']:add(a['hist_index'],a['R'],a['Z'])
 for hi,loc in enumerate(m.locs):
  n=len(loc['groups'])
  for r,z in product(range(2),repeat=2):add(hi,(r,)*n,(z,)*n)
  for _ in range(args.initial):add(hi,rng.integers(0,2,n),rng.integers(0,2,n))
 prefix=np.array([m.k,*m.ycols],float).T;phase=1;sol=None
 for iteration in range(args.rounds):
  mat=np.column_stack([prefix,*vectors]);scale=np.max(abs(mat),axis=1);scale[scale==0]=1
  norm=np.array([0.]*(ny+1)+[float(m.locs[k[0]]['norm']) for k in keys]);objective=np.array([0.]*(ny+1)+[float(m.locs[k[0]]['obj']) for k in keys])
  if phase==1:mat=np.c_[mat,scale];norm=np.r_[norm,0.];objective=np.r_[np.zeros(len(objective)),1.]
  sol=linprog(objective,A_ub=csr_matrix(-mat/scale[:,None]),b_ub=np.zeros(m.nr),A_eq=[norm],b_eq=[1.],bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
  if not sol.success:raise RuntimeError(sol.message)
  if phase==1 and sol.fun<1e-9:phase=2;print('PHASE2',iteration,flush=True);continue
  if phase==2 and sol.fun<.5-1e-8:
   report=recover(m,keys,sol.x);(HERE/'promotion_joint_atoms_exact.json').write_text(json.dumps(report,indent=2)+'\n');print('EXACT BELOW HALF',report['W'],'atoms',len(report['RZ_atoms']),flush=True);return
  dual=-sol.ineqlin.marginals/scale;rho=sol.eqlin.marginals[0];added=0;best=0.
  for hi,loc in enumerate(m.locs):
   constant=dual[m.no:]@np.array(m.constants[hi],float)
   for score,r,z in ja.pricing(loc,dual[:m.no],rng,args.restarts):
    rc=(float(loc['obj']) if phase==2 else 0.)-rho*float(loc['norm'])-score-constant;best=min(best,rc)
    if rc < -1e-8:added+=add(hi,r,z)
  print(json.dumps({'iteration':iteration,'phase':phase,'objective':sol.fun,'columns':len(keys)+ny+1,'added':added,'min_discovered_rc':best,'seconds':time.time()-start}),flush=True)
  if not added:break
 report={'scope':'restricted original 16 histograms, heuristic R/Z pricing; no full-domain inference','phase':phase,'objective':sol.fun,'iterations':iteration+1,'columns':len(keys)+ny+1,'seconds':time.time()-start}
 (HERE/'promotion_joint_atoms_status.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--rounds',type=int,default=45);p.add_argument('--initial',type=int,default=8);p.add_argument('--restarts',type=int,default=96);p.add_argument('--seed',type=int,default=20261027);main(p.parse_args())
