"""Attack ONE-K(5) in an existing complete-policy cone; no conclusions from failure."""
from pathlib import Path
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
import importlib.util,json,numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance,CustomerType,StrategyCertificate,verify_certificate
ROOT=Path.cwd(); HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('one_k',HERE/'attack_one_k.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
g=Instance.from_dict(json.loads((ROOT/'examples/customer_attraction/five_individual_security.json').read_text()))
raw=json.loads((ROOT/'evidence/certificates/customer_attraction/five_individual_security.json').read_text());cert=StrategyCertificate.from_dict(raw['strategy'])
p=list(map(F,raw['security']['primary'])); pol=cert.actions;K=g.topic_count;N=len(g.customers)
@lru_cache(None)
def term(h):return h if len(h)==5 else term(h+(pol[h],))
@lru_cache(None)
def coeff60(a,z):
 return tuple(int(F(60,sum(1 for q in z if q in t.topics))) if a in t.topics else 0 for t in g.customers)
rows=[]
for h,chosen in pol.items():
 chosenvec=np.array(coeff60(chosen,term(h)),dtype=int)
 for a in range(K):
  r=np.array(coeff60(a,term(h+(a,))),dtype=int)-chosenvec
  if r.any():rows.append(tuple(r))
rows=list(set(rows)); print('distinct SPE inequalities',len(rows),flush=True)
A=[list(r)+[0,0] for r in rows]; names=['SPE']*len(A)
for b in mod.comps(4,K):
 c=[]
 for t in g.customers:
  c.append(sum(p[a] for a in t.topics)*F(60,1+sum(b[a] for a in t.topics)))
 A.append(list(-np.array(c,dtype=float))+[0,60]);names.append('security')
z=term(()); q=z[:3]; f=[]
for a in range(K):f.append([F(60,1+sum(b in t.topics for b in q)) if a in t.topics else F(0) for t in g.customers])
for a in range(K):
 R=pol[q+(a,)];A.append([float(x-y) for x,y in zip(f[R],f[z[-1]])]+[-60,0]);names.append('Kbar')
P=sum((np.array(coeff60(a,z),dtype=float) for a in q),np.zeros(N))
w=np.array([int(any(a in t.topics for a in z)) for t in g.customers])
res=linprog(list(P)+[60,-180],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[list(w)+[0,0]],b_eq=[1],bounds=[(0,None)]*(N+2),method='highs')
out={'status':'floating_fixed_policy_cone_only','success':bool(res.success),'message':res.message,'rows':len(A)}
if res.success:
 out.update(objective=float(res.fun/60),weights=list(map(float,res.x[:N])),Kbar=float(res.x[-2]),v=float(res.x[-1]),p=list(map(str,p)),path=z)
print({k:v for k,v in out.items() if k not in ('weights','p')})
(HERE/'one_k_cone_diagnostic.json').write_text(json.dumps(out,indent=2))
