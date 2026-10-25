"""Search genuine full-history SPEs against P_3+K>=3 v_5. No HALF claim."""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from pathlib import Path
import json,random,sys
import numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance,CustomerType,ExactSPESolver,verify_certificate

def comps(n,k):
 if k==1: yield (n,);return
 for a in range(n+1):
  for b in comps(n-a,k-1):yield (a,)+b

def security(g):
 ks=g.topic_count; bs=list(comps(4,ks)); M=[]
 for b in bs:
  M.append([sum(F(t.multiplicity,1+sum(b[q] for q in t.topics)) for t in g.customers if a in t.topics) for a in range(ks)])
 z=linprog([0]*ks+[-1],A_ub=np.c_[-np.array(M,dtype=float),np.ones(len(M))],b_ub=np.zeros(len(M)),A_eq=[[1]*ks+[0]],b_eq=[1],bounds=[(0,None)]*ks+[(None,None)],method='highs')
 p=[F(float(x)).limit_denominator(1000000) for x in z.x[:-1]]; total=sum(p);p=[x/total for x in p]
 v=min(sum(a*b for a,b in zip(p,row)) for row in M)
 return p,v

def tail_info(g,path,cert):
 qh=tuple(path[:3]); q=g.counts(qh); pay=g.player_payoffs(path); u4=pay[3]; E=path[4]
 f=lambda a:sum(F(t.multiplicity,1+sum(q[b] for b in t.topics)) for t in g.customers if a in t.topics)
 gg=lambda a,b:sum(F(t.multiplicity,(1+sum(q[c] for c in t.topics))*(2+sum(q[c] for c in t.topics))) for t in g.customers if a in t.topics and b in t.topics)
 phi=lambda a,b:f(a)+f(b)-gg(a,b)
 mm=max(phi(a,b) for a in range(g.topic_count) for b in range(g.topic_count))
 ts=[a for a in range(g.topic_count) if any(phi(a,b)==mm for b in range(g.topic_count))]
 vals=[]
 for a in ts:
  R=cert.actions[qh+(a,)]
  assert phi(a,R)==mm
  delta=f(a)-gg(a,R)
  assert delta<=u4
  vals.append(f(R)-f(E))
 K=max(vals); gamma=mm-phi(path[3],E)
 assert 0<=gamma<=K<=u4/2
 return pay,K,gamma,ts

def probe(g,rng):
 p,v=security(g); sol=ExactSPESolver(g); outs=list(sol.outcomes()); cand=[]
 for out in outs:
  pays=g.topic_payoffs(out)
  occupied=[a for a,x in enumerate(out) if x]
  for first in product(occupied,repeat=3):
   if any(first.count(a)>out[a] for a in occupied):continue
   P=sum(pays[a] for a in first)
   if P<3*v:cand.append((P,first,out))
 cand.sort()
 for _,first,out in cand[:25]:
  paths=[z for z in sol.ordered_outcomes(out) if z[:3]==first]
  rng.shuffle(paths)
  for path in paths[:3]:
   try: cert=sol.certificate(out,on_path=path)
   except ValueError:continue
   pay,K,gamma,ts=tail_info(g,path,cert)
   excess=sum(pay[:3])+K-3*v
   if excess<0:
    ver=verify_certificate(g,cert);assert ver.valid
    return {'status':'genuine_complete_SPE_bridge_counterexample_not_HALF','instance':g.to_dict(),'certificate':cert.to_dict(),'path':path,'payoffs':list(map(str,pay)),'query':list(map(str,p)),'security_lower_bound':str(v),'K':str(K),'Gamma':str(gamma),'M2_optimal_first':ts,'bridge_excess':str(excess),'checked_nodes':ver.checked_histories,'checked_deviations':ver.checked_deviations}
 return None

if __name__=='__main__':
 rng=random.Random(38294); limit=int(sys.argv[1]) if len(sys.argv)>1 else 1000
 for j in range(limit):
  k=3 if j%3==0 else 4
  cs=[CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randint(1,12)) for mask in range(1,1<<k) if (rng.random()<.7)]
  cs=[c for c in cs if c.multiplicity]
  g=Instance(tuple(f'T{a}' for a in range(k)),tuple(cs),5)
  z=probe(g,rng)
  if z:
   path=Path(__file__).with_name('one_k_counterexample.json');path.write_text(json.dumps(z,indent=2));print({k:v for k,v in z.items() if k not in ('instance','certificate')});break
  if j%50==0:print('tested',j,flush=True)
 else:print('no counterexample; not proof')
