import numpy as np, scipy.optimize as so, itertools, random, json, time, sys
from functools import lru_cache
from pathlib import Path
BASE=Path(__file__).resolve().parent
K=7;N=5;MASKS=np.arange(1,1<<K);B=np.array([[(m>>a)&1 for m in MASKS] for a in range(K)],dtype=float)
@lru_cache(None)
def util(q,a):
 c=np.asarray(q)@B
 return np.divide(B[a],c,out=np.zeros(len(MASKS)),where=c>0)
def inc(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
@lru_cache(None)
def cov(q):return ((np.asarray(q)@B)>0).astype(float)
ROOT=(0,)*K
OPTS=list(itertools.combinations(range(K),5))

def single(w,rng):
 policy={};term={};nodes=[]
 @lru_cache(None)
 def go(q):
  if sum(q)==N:term[q]=q;return q
  branches=[go(inc(q,a)) for a in range(K)]
  vals=[util(branches[a],a)@w for a in range(K)]
  high=max(vals);ties=[a for a in range(K) if vals[a]>high-1e-7]
  a=ties[0];policy[q]=a;term[q]=branches[a];nodes.append(q)
  return branches[a]
 z=go(ROOT);q=ROOT;path=[]
 for i in range(N):
  a=policy[q];path.append(a);q=inc(q,a)
 rows=[]
 for q in nodes:
  a=policy[q]
  for t in range(K):
   if t!=a:rows.append(util(term[q],a)-util(term[inc(q,t)],t))
 mat=np.asarray(rows)
 prefix=ROOT
 for a in path[:2]:prefix=inc(prefix,a)
 opt=max(OPTS,key=lambda x:cov(tuple(int(a in x) for a in range(K)))@w)
 objective=cov(z)-cov(tuple(int(a in opt) for a in range(K)))
 for a in opt:objective+=util(term[inc(prefix,a)],a)
 res=so.linprog(objective,A_ub=-mat,b_ub=np.zeros(len(mat)),A_eq=cov(z)[None,:],b_eq=[1.],bounds=(0,None),method='highs')
 if not res.success:return None
 return res.fun,res.x,{"path":path,"opt":opt,"policy":[[list(q),a] for q,a in policy.items()],"actual_counts":z,"weights":[[int(m),float(v)] for m,v in zip(MASKS,res.x) if v>1e-9]}

if __name__=='__main__':
 rng=random.Random(1);w=np.zeros(len(MASKS));w[0]=5
 for a in range(1,5):w[(1<<a)-1]=1
 got=single(w,rng)
 print(got[0],got[2]['path'],got[2]['weights'])
 (BASE/'row3_allbig_cone.json').write_text(json.dumps({'score':got[0],'data':got[2]},indent=2))
