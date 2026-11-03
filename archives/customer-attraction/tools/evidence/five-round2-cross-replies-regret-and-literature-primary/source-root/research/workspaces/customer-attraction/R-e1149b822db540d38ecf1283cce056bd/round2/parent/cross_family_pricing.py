"""Discover five-player certificates using genuine cross-family query IC.

The output is floating column generation, not a theorem or an SPE instance.
All original files stay frozen; this file adds a separable, full-type row family.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,json,sys,time
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/model.py').is_file())
SOURCE=ROOT/'research/workspaces/customer-attraction/R-a27734a8bba345cbb5fad186c120d0bf'
sys.path.insert(0,str(SOURCE))
import root_shared_max_pricing as shared
old=shared.source.old
TAGS=('AB','AE','Sbranch')
QUERIES={'AB':('X','Y'),'AE':('X','Y'),'Sbranch':('U','V','W')}
SPECS=[(s,t,q) for s in TAGS for t in TAGS for q in QUERIES[t]]
NAMES=['XC:'+':'.join(s) for s in SPECS]

def q(n,d):return F(int(n),int(d)) if n else F()
def pref(bits,tag):return int(bits[0])+(int(bits[1]) if tag=='AB' else int(bits[4]) if tag=='AE' else 0)
def row_values(atom):
 bits=list(map(int,atom['bits']));d=sum(atom['AB_hist'][4:]);counts={};profit={}
 for tag in TAGS:
  k=4 if tag=='Sbranch' else 3
  h=atom['second_hist' if k==4 else tag+'_hist'];types=list(product((0,1),repeat=k))
  counts[tag]={name:sum(int(n)*t[j] for n,t in zip(h,types)) for j,name in enumerate(QUERIES[tag],1)}
  profit[tag]=sum((int(n)*q(t[1],pref(bits,tag)+sum(t)) for n,t in zip(h,types)),F())
 out={}
 for name,(s,t,c) in zip(NAMES,SPECS):
  p=pref(bits,s);r=3 if s=='Sbranch' else 2
  out[name]=5*profit[s]-counts[t][c]*(q(d,p+r+1)+q(5-d,p+r))
 return out

class Universe(shared.source.Universe):
 def __init__(self):
  super().__init__();self.names+=NAMES

 def atom_rows(self,atom):
  rows=super().atom_rows(atom);rows.update(row_values(atom));return rows

 def family_score(self,bits,tag,weights,integer=False):
  core=[(n,v) for n,v in weights if not n.startswith('XC:')]
  key,const,vec,me,mh=super().family_score(bits,tag,core,integer=integer)
  vec=list(vec);extra=[];k=4 if tag=='Sbranch' else 3;p=pref(bits,tag)
  for n,v in weights:
   if not n.startswith('XC:'):continue
   _,s,t,c=n.split(':')
   if tag==s:
    vec.append((v,5*self.M[k,p]['zu' if k==4 else 'zx']));extra.append((n,v,'source'))
   if tag==t:
    pp=pref(bits,s);r=3 if s=='Sbranch' else 2
    den=old.sc([q(int(d),pp+r+1)+q(5-int(d),pp+r) for d in self.d[k]])
    vec.append((-v,self.count[k][c]*den));extra.append((n,v,'target',pp,r))
  return (key[0],key,tuple(extra)),const,vec,me,mh

 def price(self,lam,beta,batch=40,integer=False,objective_scale=1):
  dtype=object if integer=='object' else np.int64 if integer else float
  weights=[(n,int(v) if integer else float(v)) for n,v in zip(self.names,lam) if abs(v)>1e-11]
  fam={t:[] for t in TAGS}
  for n,v in weights:
   if n.startswith('XC:'):
    _,s,t,_=n.split(':');fam[s].append((n,v))
    if t!=s:fam[t].append((n,v))
   else:
    tag=n.split(':')[0]
    if tag in fam:fam[tag].append((n,v))
    elif ':sum-S' in n:fam['Sbranch'].append((n,v))
  ow=np.asarray(lam,dtype=dtype)[self.oldids]
  base=self.base@ow;EC=self.ec@ow;HC=self.hc@ow
  cache={};best=[];minimum=1e100
  for bi,bits in enumerate(self.bits):
   fs=[];E=EC[bi].copy();H=HC[bi].copy();choices=[]
   for tag in TAGS:
    key,const,vec,me,mh=self.family_score(bits,tag,fam[tag],integer);k=key[0]
    if key not in cache:
     score=np.zeros(len(self.hist[k]),dtype=dtype)
     for v,a in vec:score+=v*(a.astype(object) if integer=='object' else a)
     vals=[];idx=[]
     for ids in self.ids[k]:
      arg=ids[int(np.argmax(score[ids]))];vals.append(score[arg]);idx.append(int(arg))
     cache[key]=(np.asarray(vals),idx)
    vals,idx=cache[key];fs.append(vals+const);choices.append(idx);E+=me.T;H+=mh.T
   for d in range(6):
    corners=[(0,0),(d,d),(5-d,0),(5,d)];menus=0;lhs=[]
    for f in range(3):
     lh=max(corners,key=lambda x:x[0]*E[d,f]+x[1]*H[d,f]);lhs.append(lh);menus+=lh[0]*E[d,f]+lh[1]*H[d,f]
    rho=120*(beta*int(any(bits[:5]))-objective_scale*int(d>0))-base[bi,d]-menus-sum(x[d] for x in fs)
    minimum=min(minimum,rho)
    if rho<(0 if integer else -1e-7):
     atom={'bits':''.join(map(str,bits)),'AB_hist':list(self.hist[3][choices[0][d]]),'AE_hist':list(self.hist[3][choices[1][d]]),'second_hist':list(self.hist[4][choices[2][d]]),'menus_lh':lhs}
     best.append((rho,atom))
  best.sort(key=lambda z:z[0])
  for rho,atom in best[:batch]:
   rr=self.atom_rows(atom)
   direct=120*(beta*int(any(map(int,atom['bits'][:5])))-objective_scale*int(any(atom['AB_hist'][4:])))
   direct-=120*sum((int(v)*rr[n] if integer else float(v)*float(rr[n])) for n,v in zip(self.names,lam))
   assert abs(direct-rho)<F(1,10**6),(direct,rho)
  return minimum,best[:batch],len(cache)

def run(maxiter=15):
 U=Universe();kcol=np.array([float(shared.KCO.get(n,0)) for n in U.names])
 warm=SOURCE/'root_shared_max_copy_cg.json';data=json.loads(warm.read_text())
 atoms=[];keys=set();columns=[];ws=[];os=[]
 def add(a):
  key=old.atom_key(a)
  if key in keys:return False
  rr=U.atom_rows(a);keys.add(key);atoms.append(a);columns.append([float(rr[n]) for n in U.names])
  ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])));return True
 for a in data['atoms']:add(a)
 history=[]
 for it in range(maxiter):
  begin=time.monotonic();mat=np.column_stack((np.asarray(columns).T,kcol))
  lp=linprog(-np.array(os+[0.]),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws+[0]],b_eq=[1.],bounds=(0,None),method='highs')
  assert lp.success,lp.message
  beta=float(-lp.fun);lam=-lp.ineqlin.marginals;minimum,new,ncache=U.price(lam,beta)
  count=sum(add(a) for _,a in new)
  rec={'iteration':it,'restricted_beta_float':beta,'minimum_scaled_float':float(minimum),'new_columns':count,'columns':len(atoms),'contexts':ncache,'seconds':time.monotonic()-begin}
  history.append(rec);print(json.dumps(rec),flush=True)
  report={'scope':'Floating full-type separable cross-family IC discovery; not HALF(5) or SPE','sources':{'path':str(warm.relative_to(ROOT)),'sha256':hashlib.sha256(warm.read_bytes()).hexdigest()},'row_names':U.names,'atoms':atoms,'primal_float':lp.x[:-1].tolist()+[0.]*count,'shared_K_float':float(lp.x[-1]),'K_column':kcol.tolist(),'dual_beta_float':beta,'dual_multipliers_float':{n:float(v) for n,v in zip(U.names,lam) if v>1e-12},'history':history}
  (HERE/'cross_family_cg.json').write_text(json.dumps(report,indent=2)+'\n')
  if count==0:break
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 15)
