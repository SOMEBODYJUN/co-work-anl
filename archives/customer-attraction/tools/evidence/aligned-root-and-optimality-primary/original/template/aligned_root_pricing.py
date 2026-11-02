"""Root genuine indexed-complement and offdiagonal rows; discovery only."""
from pathlib import Path
import sys,json,time
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
SRC=ROOT/'research/workspaces/customer-attraction/R-428f842e483745ffbe55235bfd7d250a/five_c'
sys.path.insert(0,str(SRC))
import root_pricing as base
from root_pricing import RPOS,TYPES,sc,q,rkey,PATHS
from full_pricing import terminal_rows,pair_rows
TABLE_FILES=['binary_pareto_residual_table.json','binary_pareto_1999_residual_table.json']
TABLES=[{k:list(map(F,v)) for k,v in json.loads((HERE.parent/'root_tail'/fn).read_text())['table'].items()} for fn in TABLE_FILES]

def aligned_rows(hist,exact=True,bits=None):
 Q=base.EX['q'] if exact else base.VE['q']
 def sm(fn):return sum((n*fn(*map(int,ty)) for n,ty in zip(hist,TYPES)),F() if exact else 0)
 d=sm(lambda t,x,y,z,k:t)
 if exact:cov=int(d>0)
 else:cov=np.asarray(d>0,dtype=int)
 share={m:sm(lambda *tt:Q(tt[i],sum(tt))) for i,m in enumerate(RPOS)}
 count={m:sm(lambda *tt:tt[i]) for i,m in enumerate(RPOS)}
 out={}
 out['Root:aligned:r4']=1499*sum(share[m] for m in RPOS[1:])-3000*cov
 out['Root:aligned:r4-binary']=6*sum(share[m] for m in RPOS[1:])+share['T']-d-12*cov
 out['Root:aligned:r4-binary1999']=5997*sum(share[m] for m in RPOS[1:])+997*share['T']-997*d-12000*cov
 for v,table in enumerate(TABLES):
  def residual(t,x,y,z,k):
   vv=table[''.join(map(str,(t,x,y,z,k)))];e=d-t
   return vv[int(e)] if exact else np.take(np.asarray(vv,dtype=float),np.asarray(e,dtype=int))
  aa=F(2) if v==0 else F(1999,1000)
  def value(t,x,y,z,k):
   beta=F(5,3) if t else aa
   return (beta if exact else float(beta))*Q(x+y+z+k,t+x+y+z+k)-residual(t,x,y,z,k)
  out[f'Root:aligned:r4-pareto{v}']=sm(value)-4*cov
 def g4(p,c):return Q(c*(c-1),p+c-1)+Q((5-c)*c,p+c)
 for m,cc in count.items():
  out[f'Root:aligned:r4-binary-menu:{m}']=29985*sum(share[z] for z in RPOS[1:])+4985*share['T']-4985*d-3000*sm(lambda t,x,y,z,k:g4(t,cc))
 b=list(map(int,bits)) if bits is not None else [0]*10
 ld=sum(b[:5]);u1=Q(b[0],ld);tail=Q(sum(b[1:5]),ld)
 out['Root:aligned:actual4-binary']=29985*tail-4985*(b[0]-u1)-3000*g4(b[0],d)
 r0=list(map(F,['0','0','1/750','1/1500','1/1500','39/500','1/1000','623/3000','2747/12000','691/6000','47/1500','1919/12000','0','77/750','1/4000','1169/6000']))
 r1=list(map(F,['0','133/750','2003/12000','61853/180000','251/3000','6331/22500','7363/36000','26047/60000','239/1200','14579/45000','22183/90000','5177/12000','15767/90000','63893/180000','43349/180000','41143/90000']))
 out['Root:aligned:r4-credit']=2998*sum(share[m] for m in RPOS[1:])-6000*cov-sm(lambda t,x,y,z,k:1500*(r1 if t else r0)[8*x+4*y+2*z+k])
 # At branch (T_i,X_i), compare all four triples chosen from T_{-i}.
 def g3(p,c):return Q(c*(4-c)*(3-c)/2,p+1)+Q(c*(c-1)*(4-c),p+2)+Q(c*(c-1)*(c-2)/2,p+3)
 # c=d-t is fixed conditional on a histogram. Closure handles d as vector.
 out['Root:aligned:r3']=20*sum(share[m] for m in RPOS[2:])-3*sm(lambda t,x,y,z,k:g3(t+x,d-t))
 H=share['Z']+share['K']+sm(lambda t,x,y,z,k:Q(z,(t+x+y+1)*(t+x+y+2)))
 out['Root:aligned:r2']=6*H-sm(lambda t,x,y,z,k:Q((d-t)*(4-d+t),t+x+y+1)+Q((d-t)*(d-t-1),t+x+y+2))
 for i in range(1,5):
  sh=share[RPOS[i]]
  out[f'Root:aligned:opt:{i}']=4*sh-sm(lambda *tt:Q(d-tt[0],sum(tt[:i])+5-i))
  for j,m in enumerate(RPOS[1:],1):
   de=sm(lambda *tt:Q(1,sum(tt[:i])+5-i))
   own=sm(lambda *tt:Q(tt[j],sum(tt[:i])+5-i))
   out[f'Root:aligned:menu:{i}:{m}']=4*sh-count[m]*de+own
 return out

class Universe(base.RootUniverse):
 def __init__(self):
  super().__init__()
  rr=aligned_rows(self.rh.T,False);self.anames=list(rr);self.names+=self.anames
  for n,v in rr.items():
   if n=='Root:aligned:actual4-binary':continue
   self.local[n]=np.asarray(v,dtype=float)*120 if 'pareto' in n else sc(v)
  for a in (0,1):
   self.local[f'actual4binary:{a}']=np.asarray([-3000*(q(int(d)*(int(d)-1),a+int(d)-1)+q((5-int(d))*int(d),a+int(d))) for d in self.rd],dtype=float)*120
  print(json.dumps({'aligned_rows':len(rr),'total_rows':len(self.names)}),flush=True)
 def atom_rows(self,a):
  rr=super().atom_rows(a);rr.update(aligned_rows(a['root_hist'],True,a['bits']));return rr
 def root_score(self,bits,weights,integer=False):
  own=[(n,v) for n,v in weights if n.startswith('Root:aligned:')]
  others=[(n,v) for n,v in weights if not n.startswith('Root:aligned:')]
  _,const,co,E,H=super().root_score(bits,others,integer)
  for n,v in own:
   if n=='Root:aligned:actual4-binary':
    bb=list(map(int,bits));ld=sum(bb[:5]);u1=q(bb[0],ld);tail=q(sum(bb[1:5]),ld)
    const+=v*float(120*(29985*tail-4985*(bb[0]-u1)))
    co[f'actual4binary:{bb[0]}']+=v
   else:co[n]+=v
  key=tuple(sorted((n,v) for n,v in co.items() if v))
  return key,const,co,E,H

def float_atom_rows(a):
 rr=base.VE['evaluate'](tuple(map(int,a['bits'])),[a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True)
 rr.update(terminal_rows(a));rr.update(pair_rows(a,overlap=1))
 rr.update(base.root_rows(tuple(map(int,a['bits'])),a['root_hist'],a['menus_lh'],False))
 rr.update(aligned_rows(a['root_hist'],False,a['bits']))
 return rr

def run(maxiter=50):
 U=Universe();data=json.loads((SRC/'root_cg.json').read_text());atoms=[];keys=set();cols=[];ws=[];os=[]
 def add(a):
  k=rkey(a)
  if k in keys:return 0
  rr=float_atom_rows(a);cols.append([float(rr[n]) for n in U.names]);atoms.append(a);keys.add(k)
  ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])));return 1
 previous=HERE/'aligned_root_cg.json'
 warm=json.loads(previous.read_text()) if previous.exists() else data
 # Keep positive support and recently priced columns; full pricing can recover dropped zeros.
 pp=warm['primal_float'];keep=[i for i,m in enumerate(pp) if m>1e-10]
 keep+=list(range(max(0,len(warm['atoms'])-160),len(warm['atoms'])))
 for i in sorted(set(keep)):add(warm['atoms'][i])
 # All-active fallback maintains feasibility at ratio one.
 for d in (0,5):
  h3=[0]*8;h3[3 if d==0 else 7]=5;h4=[0]*16;h4[7 if d==0 else 15]=5;h5=[0]*32;h5[15 if d==0 else 31]=5
  add({'bits':'1111111111','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'root_hist':h5,'menus_lh':[(5,d)]*3})
 # Deterministic exact-row crosscheck of the fast column generator.
 for a in atoms[::max(1,len(atoms)//8)]:
  exact=U.atom_rows(a);fast=float_atom_rows(a)
  assert max(abs(float(exact[n])-float(fast[n])) for n in U.names)<1e-9
 print(json.dumps({'initial_columns':len(atoms),'float_generator_exact_crosschecks':min(9,len(atoms))}),flush=True)
 hist=[]
 for it in range(maxiter):
  start=time.time();mat=np.array(cols).T
  out=linprog(-np.array(os,dtype=float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs')
  if not out.success:raise RuntimeError(out.message)
  beta=-out.fun;lam=-out.ineqlin.marginals;minimum,new,contexts=U.price(lam,beta);n=sum(add(a) for _,a in new)
  rec={'iteration':it,'columns':len(atoms),'beta':beta,'minimum_scaled_residual':minimum,'new':n,'contexts':contexts,'seconds':time.time()-start};hist.append(rec);print(json.dumps(rec),flush=True)
  report={'scope':'floating necessary-condition discovery, not a theorem or game','row_names':U.names,'atoms':atoms,'primal_float':out.x.tolist()+[0.]*n,'dual_beta_float':beta,'dual_multipliers_float':{name:float(v) for name,v in zip(U.names,lam) if v>1e-10},'history':hist}
  previous.write_text(json.dumps(report,indent=2)+'\n')
  if n==0:break
 return U,out,atoms
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 50)
