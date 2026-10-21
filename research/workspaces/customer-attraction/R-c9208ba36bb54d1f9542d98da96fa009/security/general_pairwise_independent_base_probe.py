"""Discovery: enlarge the high-background matrix to arbitrary symmetric nonnegative C.
A witness here is not a legal CAG unless C has the required nonnegative incidence form.
"""
from pathlib import Path
import numpy as np,random,json
from scipy.optimize import linprog
OUT=Path(__file__).resolve().parent
rng=random.Random(3889)
def run(K,r):
 pairs=[(a,b) for a in range(K) for b in range(a,K)];D=len(pairs)+K;idx={ab:i for i,ab in enumerate(pairs)}
 def entry(a,b):return idx[(min(a,b),max(a,b))]
 def cost(a,z):
  v=np.zeros(D);v[len(pairs)+a]+=1
  for b in list(z[:z.index(a)]) if False else []:pass
  for b in z:v[entry(a,b)]+=1
  v[entry(a,a)]-=1 # remove the player's own occurrence, leaving fixed diagonal plus others
  return v
 def policy(w):
  actions={}
  def rec(h):
   if len(h)==r:return h
   zs=[rec(h+(a,)) for a in range(K)];vals=[cost(a,zs[a])@w for a in range(K)];low=min(vals)
   A=rng.choice([a for a in range(K) if vals[a]<=low+1e-9]);actions[h]=A;return zs[A]
  z=rec(());return actions,z
 def mat(actions):
  rows=[]
  def rec(h):
   if len(h)==r:return h
   zs=[rec(h+(a,)) for a in range(K)];A=actions[h]
   for a in range(K):
    if a!=A:rows.append(cost(a,zs[a])-cost(A,zs[A]))
   return zs[A]
  z=rec(());return np.unique(np.array(rows),axis=0),cost(z[0],z),z
 def tax(w):
  A=np.array([[w[len(pairs)+a]+(r-1)*w[entry(a,b)] for b in range(K)] for a in range(K)])
  ans=linprog(np.r_[np.zeros(K),1],A_ub=np.c_[A.T,-np.ones(K)],b_ub=np.zeros(K),A_eq=[np.r_[np.ones(K),0]],b_eq=[1],bounds=[(0,None)]*K+[(None,None)],method='highs')
  return ans.x[:-1],ans.fun
 best=-1e9
 for it in range(100):
  w=np.array([rng.random() for _ in range(D)]);actions,z=policy(w);G,actual,z=mat(actions);p,v=tax(w)
  for alt in range(4):
   B=np.zeros((K,D))
   for b in range(K):
    for a in range(K):B[b,len(pairs)+a]+=p[a];B[b,entry(a,b)]+=(r-1)*p[a]
   ans=linprog(np.r_[-actual,1],A_ub=np.vstack([np.c_[-G,np.zeros(len(G))],np.c_[B,-np.ones(K)]]),b_ub=np.zeros(len(G)+K),bounds=[(0,1)]*D+[(None,None)],method='highs')
   w=ans.x[:-1];p,v=tax(w);loss=actual@w-v
   if loss>best+1e-8:best=loss
   if loss>1e-7:
    rec={'r':r,'K':K,'iteration':it,'alt':alt,'loss':loss,'pairs':pairs,'C_and_base':w.tolist(),'query':p.tolist(),'z':z,'actions':[{'history':h,'action':a} for h,a in actions.items()]};(OUT/'general_pairwise_independent_base_candidate.json').write_text(json.dumps(rec,indent=2));print(json.dumps({key:rec[key] for key in ['r','K','iteration','alt','loss','z']}),flush=True);return True
 print('done',r,K,'best',best,flush=True);return False
for r,K in [(3,4),(3,5),(4,4),(4,5),(5,4),(5,5)]:
 if run(K,r):break
