from itertools import combinations_with_replacement
from math import lcm
import json, random, sys
import numpy as np
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver

m=int(sys.argv[1]) if len(sys.argv)>1 else 3
g=int(sys.argv[2]) if len(sys.argv)>2 else 3
iters=int(sys.argv[3]) if len(sys.argv)>3 else 10000
k=2*g+2
L=lcm(*range(1,m+1))
def cnt(t):
 r=[0]*k
 for a in t:r[a]+=1
 return tuple(r)
levels=[[cnt(t) for t in combinations_with_replacement(range(k),d)] for d in range(m+1)]
terms=levels[m]; tid={q:i for i,q in enumerate(terms)}
children={q:[tuple(v+(a==j) for j,v in enumerate(q)) for a in range(k)] for level in levels[:-1] for q in level}
# all covered types include either outside action 0 or k-1
cmasks=[mask for mask in range(1,1<<k) if mask&((1<<0)|(1<<(k-1)))]
umasks=[(1<<(2*j+1))|(1<<(2*j+2)) for j in range(g)]
masks=cmasks+umasks
coeff=np.zeros((len(masks),len(terms),k),dtype=np.int64)
for i,mask in enumerate(masks):
 for t,q in enumerate(terms):
  load=sum(q[a] for a in range(k) if mask>>a&1)
  if load:
   for a in range(k):
    if q[a] and mask>>a&1:coeff[i,t,a]=L//load
outs=[i for i,q in enumerate(terms) if all(q[a]==0 for a in range(1,k-1))]
rng=random.Random(283674)
for it in range(iters):
 weights=np.zeros(len(masks),dtype=np.int64)
 # vary number of covered clients and omitted block sizes on the same scale
 size=rng.randint(2,20)
 for j in rng.sample(range(len(cmasks)),rng.randint(2,min(18,len(cmasks)))):weights[j]=rng.randint(1,size)
 for j in range(g):weights[len(cmasks)+j]=rng.randint(1,size*2)
 W=int(sum(weights[:len(cmasks)])); D=int(sum(sorted(weights[len(cmasks):],reverse=True)[:m]))
 if W>=D:continue
 pay=np.tensordot(weights,coeff,axes=(0,0))
 sol={q:{tid[q]} for q in terms}
 for level in reversed(levels[:-1]):
  for q in level:
   ch=[sol[c] for c in children[q]]
   z=max(min(pay[t,a] for t in ch[a]) for a in range(k))
   sol[q]={t for a in range(k) for t in ch[a] if pay[t,a]>=z}
 bad=set(outs)&sol[(0,)*k]
 if bad:
  customers=[CustomerType(frozenset(a for a in range(k) if mask>>a&1),int(w)) for mask,w in zip(masks,weights) if w]
  inst=Instance(tuple(map(str,range(k))),tuple(customers),m)
  exact=ExactSPESolver(inst)
  q=terms[min(bad)]
  assert q in exact.outcomes()
  obj={'iteration':it,'instance':inst.to_dict(),'counts':q,'W':inst.welfare(q),'D':D,'OPT':inst.optimal_welfare()}
  Path(__file__).with_name('group_candidate.json').write_text(json.dumps(obj,indent=2))
  print(json.dumps(obj));break
 if it%1000==0:print('progress',it,flush=True)
else:print(json.dumps({'iterations':iters,'m':m,'groups':g,'found':False}))
