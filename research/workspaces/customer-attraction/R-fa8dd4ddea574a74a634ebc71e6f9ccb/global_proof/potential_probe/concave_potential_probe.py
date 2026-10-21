"""Fixed-policy probe of insertion VI in monotone concave DR lattice potentials.

This is a wider class than CAG. Positive output requires exact reconstruction
and verification; an LP point is never a Q-CAG-HALF counterexample.
"""
import argparse,json
from itertools import product
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix,csr_matrix

ap=argparse.ArgumentParser()
ap.add_argument('--players',type=int,default=3)
ap.add_argument('--topics',type=int,default=3)
ap.add_argument('--iterations',type=int,default=100)
ap.add_argument('--seed',type=int,default=911)
ap.add_argument('--dr-only',action='store_true')
args=ap.parse_args();m,p=args.players,args.topics
rng=np.random.default_rng(args.seed)
def states(k,left=p):
 if left==1:yield(k,)
 else:
  for t in range(k+1):
   for z in states(k-t,left-1):yield(t,)+z
layers=[list(states(k))for k in range(m+2)]
allq=[q for l in layers for q in l];index={q:i for i,q in enumerate(allq)}
L=len(allq);nv=L if args.dr_only else L*(p+1)
eye=np.eye(p,dtype=int)
def add(q,a):return tuple(np.array(q)+eye[a])
def sub(q,a):return tuple(np.array(q)-eye[a])
def row(**kw):return np.zeros(nv)
def utility(q,a):
 z=np.zeros(nv);z[index[q]]=1;z[index[sub(q,a)]]=-1;return z
base=[]
# Monotonicity and coordinatewise diminishing returns, on the whole domain.
for d in range(m+1):
 for q in layers[d]:
  for a in range(p):
   z=np.zeros(nv);z[index[q]]=1;z[index[add(q,a)]]=-1;base.append(z)
for d in range(m):
 for q in layers[d]:
  for a in range(p):
   for b in range(a,p):
    z=np.zeros(nv)
    for s,v in[(add(add(q,a),b),1),(add(q,a),-1),(add(q,b),-1),(q,1)]:z[index[s]]+=v
    base.append(z)
if not args.dr_only:
 # A nonnegative supergradient at every grid point produces an actual monotone
 # concave polyhedral extension on their convex hull (the simplex sum x<=m+1).
 for q in allq:
  for r in allq:
   if q==r:continue
   z=np.zeros(nv);z[index[r]]=1;z[index[q]]=-1
   z[L+p*index[q]:L+p*index[q]+p]=np.array(q)-np.array(r)
   base.append(z)
base=np.array(base)
maskinc=np.array([[int(B>>a&1)for a in range(p)]for B in range(1,1<<p)])
best=-1e9
for it in range(args.iterations):
 weights=rng.exponential(size=len(maskinc))*(rng.random(len(maskinc))<.8)
 t=rng.choice([.1,.25,.5,.75,1],size=len(maskinc))
 fv={}
 for q in allq:
  c=maskinc@q
  fv[q]=float(weights@np.array([sum(tt**j for j in range(int(k)))for tt,k in zip(t,c)]))
 final={q:q for q in layers[m]};sigma={}
 for d in reversed(range(m)):
  for q in layers[d]:
   children=[final[add(q,a)]for a in range(p)]
   vals=np.array([fv[z]-fv[sub(z,a)]for a,z in enumerate(children)])
   a=int(rng.choice(np.flatnonzero(vals>=vals.max()-1e-9)))
   sigma[q]=a;final[q]=children[a]
 rows=[]
 for q,a in sigma.items():
  for b in range(p):rows.append(utility(final[add(q,b)],b)-utility(final[q],a))
 A=csr_matrix(np.vstack([base,np.array(rows)]))
 actual=final[(0,)*p]
 W=sum((actual[a]*utility(actual,a)for a in range(p)if actual[a]),np.zeros(nv))
 J=np.zeros(nv)
 for a in range(p):
  J[index[add(actual,a)]]+=actual[a]
  J[index[actual]]-=actual[a]
 eq=np.zeros((2,nv));eq[0,index[(0,)*p]]=1;eq[1]=W
 for query in range(p):
  obj=J-2*W;obj[index[add(actual,query)]]+=m;obj[index[actual]]-=m
  res=linprog(-obj,A_ub=A,b_ub=np.zeros(A.shape[0]),A_eq=eq,b_eq=[0,1],bounds=(0,None),method='highs')
  if res.success:
   value=float(obj@res.x)
   if value>best+1e-8:
    best=value;print('best',it,value,actual,query,flush=True)
   if value>1e-6:
    out=dict(scope='general monotone concave DR potential, NOT CAG',players=m,topics=p,
      seed=args.seed,iteration=it,query=query,actual=actual,value=value,dr_only=args.dr_only,
      values=[dict(q=q,value=float(res.x[index[q]]))for q in allq],
      sigma=[dict(counts=q,action=a)for q,a in sigma.items()])
    if not args.dr_only:out['supergradients']=[dict(q=q,gradient=list(map(float,res.x[L+p*index[q]:L+p*index[q]+p])))for q in allq]
    path=Path(__file__).with_name('concave_potential_candidate.json')
    path.write_text(json.dumps(out,indent=2)+'\n');print('CANDIDATE',path,flush=True);raise SystemExit
print('finished',args.iterations,'best',best,flush=True)
