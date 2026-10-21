"""Discovery-only mass deletion minimizing a Cartesian inefficiency example."""
from cartesian_probe import *
p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=6113);p.add_argument('--rounds',type=int,default=100);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
k=n=3;K=9
C=np.array([[(mask>>b)&1 for mask in range(1,8)]for b in range(3)])
Cp=np.array([np.r_[C[i],C[j]]for i,j in it.product(range(3),repeat=2)])
zs,qs,ix=profiles(K,n);us,ws=utility(qs,Cp)
zc,qc,ic=profiles(k,n);uc,wc=utility(qc,C)
rng=np.random.default_rng(a.seed)
def evalr(r):
 vals=[]
 for x in range(2):
  rr=r[x*7:(x+1)*7];w=wc@rr;o,_=outcomes(uc@rr,w,k,n,ic);vals.append(min(w[o]))
  if min(w[o])<max(w)-1e-9:return None
 u,w=us@r,ws@r;o,_=outcomes(u,w,K,n,ix);W=min(w[o])
 return (W,vals)if W<sum(vals)-1e-9 else None
best=np.array([0,7,3,2,2,4,9,8,0,1,1,4,8,2]);e=evalr(best)
for t in range(a.rounds):
 r=best.copy()
 if t:
  r+=rng.integers(0,3,14)*(rng.random(14)<.2)
  if evalr(r)is None:continue
 changed=True
 while changed:
  changed=False
  for j in rng.permutation(14):
   if r[j]>0:
    rr=r.copy();rr[j]-=1;ev=evalr(rr)
    if ev is not None:r=rr;changed=True
 if r.sum()<best.sum():
  best=r.copy();e=evalr(best);record=dict(seed=a.seed,trial=t,weights=best.tolist(),clients=int(best.sum()),W=e[0],component_min=e[1],status='numerical_only');print(json.dumps(record,default=lambda x:x.item()),flush=True);a.out.write_text(json.dumps(record,indent=2,default=lambda x:x.item()))
print('FINISHED',flush=True)
