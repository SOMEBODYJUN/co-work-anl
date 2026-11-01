"""Exploratory block coordinate pricing for the enhanced indexed atom space.

Unlike price_aligned.py this accepts arbitrary dual supports in the 2196-row
system. Each block is optimized over its entire finite domain, but joint
coordinate ascent is heuristic and does not certify global pricing.
"""
from pathlib import Path
import sys,json,inspect,time,argparse
from itertools import product
import numpy as np
from price_aligned import TH,SH,TD,SD,TIDS,SIDS,LABELS,ROOT,SIB,off_rows,cross_rows,tax_rows,align_rows

def q(n,d):
 n,d=np.broadcast_arrays(np.asarray(n,float),np.asarray(d,float))
 return np.divide(n,d,out=np.zeros_like(n),where=(n!=0))

def transform(s):
 return s.replace('def q(n,v):return F(n,v) if n else F(0)','').replace('F(5,2)','2.5').replace('F(0)','0.').replace('F()','0.').replace('opt=int(d>0)','opt=(np.asarray(d)>0).astype(float)').replace("map(int,a['bits'])","a['bits']")

src=(ROOT/'tests/audits/customer_attraction_five_indexed.py').read_text().split('from pathlib import Path')[0]
ns={'np':np,'q':q}
exec(compile(transform(src),'<vectorized canonical rows>','exec'),ns)
ns['q']=q
extras=[]
for f in (off_rows,cross_rows,tax_rows,align_rows):
 env=dict(ns)
 from itertools import combinations_with_replacement
 env['combinations_with_replacement']=combinations_with_replacement
 exec(compile(transform(inspect.getsource(f)),'<vectorized extra rows>','exec'),env)
 extras.append(env['rows'])
BITMAT=np.array(list(product((0,1),repeat=10)),dtype=int)

class BlockPrice:
 def __init__(self,report):
  self.beta=report['dual_beta'];self.weights={n:v for n,v in zip(report['names'],report['dual_lambda']) if v>1e-10};self.names=report['names']
 def allrows(self,a,d):
  bits=a['bits'];his=[a['AB_hist'],a['AE_hist'],a['second_hist']];lhs=a['menus_lh']
  out=ns['old_rows'](bits,d,lhs)
  out.update(ns['third_rows'](bits,his[0],lhs,'AB'));out.update(ns['third_rows'](bits,his[1],lhs,'AE'))
  out.update(ns['second_rows'](bits,his[2]))
  for f in extras:out.update(f(a))
  return out
 def score(self,a,d):
  v=self.allrows(a,d);out=0.
  for n,w in self.weights.items():out=out+w*v[n]
  W=np.any(np.asarray(a['bits'])[:5],axis=0).astype(float)
  return out+int(d>0)-self.beta*W
 def domains(self,d):
  lh=np.array([(h+r,h) for h in range(d+1) for r in range(6-d)],int)
  return [BITMAT,TH[TIDS[d]],TH[TIDS[d]],SH[SIDS[d]],lh,lh,lh]
 def replace(self,a,block,values):
  b={k:v for k,v in a.items()};b['menus_lh']=[v for v in a['menus_lh']]
  if block==0:b['bits']=values
  elif block<=3:b[['AB_hist','AE_hist','second_hist'][block-1]]=values
  else:b['menus_lh'][block-4]=values
  return b
 def scalar_atom(self,a):
  return {'bits':''.join(str(int(i)) for i in a['bits']),
   'AB_hist':list(map(int,a['AB_hist'])),'AE_hist':list(map(int,a['AE_hist'])),'second_hist':list(map(int,a['second_hist'])),
   'menus_lh':[list(map(int,v)) for v in a['menus_lh']]}
 def vector_atom(self,a):
  return {'bits':list(map(int,a['bits'])),'AB_hist':a['AB_hist'],'AE_hist':a['AE_hist'],'second_hist':a['second_hist'],'menus_lh':a['menus_lh']}
 def check(self):
  from price_aligned import ns as direct_ns
  rng=np.random.default_rng(85012)
  for k in range(20):
   d=int(rng.integers(0,6));dom=self.domains(d);vs=[x[int(rng.integers(len(x)))] for x in dom]
   a={'bits':vs[0],'AB_hist':vs[1],'AE_hist':vs[2],'second_hist':vs[3],'menus_lh':vs[4:]}
   aa=self.scalar_atom(a);v=direct_ns['evaluate'](list(map(int,aa['bits'])),[aa['AB_hist'],aa['AE_hist'],aa['second_hist']],aa['menus_lh'],True)
   for f in (off_rows,cross_rows,tax_rows,align_rows):v.update(f(aa))
   vector=self.allrows(a,d)
   assert set(v)==set(vector)
   for n in v:assert abs(float(v[n])-float(vector[n]))<1e-9,(n,v[n],vector[n])
   block=k%7;cand=dom[block][:min(9,len(dom[block]))];va=self.replace(a,block,cand.T);vv=self.score(va,d)
   for i,c in enumerate(cand):
    scalar=float(self.score(self.replace(a,block,c),d));assert abs(scalar-vv[i])<1e-9,(block,scalar,vv[i])
  return 20
 def run(self,restarts,seed,maxpasses):
  rng=np.random.default_rng(seed);best=None;negative={};t0=time.time()
  for rep in range(restarts):
   d=(rep%5)+1;dom=self.domains(d);vs=[x[int(rng.integers(len(x)))] for x in dom]
   a={'bits':vs[0],'AB_hist':vs[1],'AE_hist':vs[2],'second_hist':vs[3],'menus_lh':vs[4:]};old=-np.inf
   for step in range(maxpasses):
    for block in rng.permutation(7):
     values=dom[block];scores=self.score(self.replace(a,block,values.T),d);idx=int(np.argmax(scores));a=self.replace(a,block,values[idx])
    value=float(self.score(a,d))
    if value>1e-8:
     atom=self.scalar_atom(a);key=json.dumps(atom,sort_keys=True);negative[key]={'residual':-value,'atom':atom}
    if value>old+1e-10:old=value
    else:break
   if best is None or value>best['violation']:best={'violation':value,'residual':-value,'atom':self.scalar_atom(a),'restart':rep,'passes':step+1}
   if rep%5==0:print(json.dumps({'restart':rep,'minimum_residual':best['residual'],'negative_columns':len(negative),'elapsed':time.time()-t0}),flush=True)
  return {'scope':'heuristic block coordinate pricing; each block enumerated, joint optimum uncertified','beta':self.beta,'active_rows':len(self.weights),'restarts':restarts,'seed':seed,'best':best,'negative_columns':list(negative.values()),'elapsed_seconds':time.time()-t0}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--dual',default=str(SIB/'reopt_added.json'));parser.add_argument('--restarts',type=int,default=30);parser.add_argument('--passes',type=int,default=8);parser.add_argument('--seed',type=int,default=20261021);parser.add_argument('--output',default=str(Path(__file__).with_suffix('.json')));args=parser.parse_args()
 p=BlockPrice(json.loads(Path(args.dual).read_text()));checks=p.check();report=p.run(args.restarts,args.seed,args.passes);report['allrow_formula_checks']=checks
 Path(args.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='negative_columns'},indent=2))
