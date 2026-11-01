"""Discovery only: walk full ordered-history policy cones for P+Delta-O_fresh.
A negative floating objective is a candidate, never a mathematical certificate.
"""
from pathlib import Path
from itertools import product, combinations
import argparse, json, random, time
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).parent

def probe(q,k,trials,seed):
 rng=random.Random(seed)
 masks=np.arange(1,1<<q)
 member=np.array([[(int(mask)>>a)&1 for a in range(q)]for mask in masks],dtype=float)
 histories=[h for d in range(k) for h in product(range(q),repeat=d)]
 terminals=list(product(range(q),repeat=k))
 counts=np.array([[h.count(a) for a in range(q)]for h in terminals])
 ti={h:i for i,h in enumerate(terminals)}
 loads=counts@member.T
 comparisons=list(combinations(range(q),min(k,q)))
 best=0.0; start=time.time(); walk_weights=None; prefix=None
 for trial in range(trials):
  if walk_weights is None or trial%12==0:
   prefix=[0]*q
   used=rng.sample(range(q),rng.choice([1,1,2,2,3]))
   for a in used:prefix[a]=rng.choice([1,1,2,3,6])
   bg=member@np.array(prefix);fresh=(bg==0).astype(float)
   total=loads+bg
   coeff=np.divide(member[None,:,:],total[:,:,None],out=np.zeros((len(terminals),len(masks),q)),where=total[:,:,None]!=0)
   walk_weights=np.array([rng.randrange(1,50)if rng.random()<.20 else 0 for _ in masks],dtype=float)
  else:
   walk_weights=walk_weights*(.5+np.array([rng.random() for _ in masks]))
   walk_weights+=np.array([rng.random()*4 if rng.random()<.04 else 0 for _ in masks])
  pay=np.einsum('tna,n->ta',coeff,walk_weights)
  policy={};out={h:h for h in terminals}
  for h in reversed(histories):
   vals=[pay[ti[out[h+(a,)]],a]for a in range(q)];top=max(vals)
   a=rng.choice([a for a,v in enumerate(vals) if abs(v-top)<1e-8]);policy[h]=a;out[h]=out[h+(a,)]
  actual=out[()];at=ti[actual]
  rows=[]
  for h in histories:
   a=policy[h];on=coeff[ti[out[h]],:,a]
   for d in range(q):
    if d!=a:rows.append(on-coeff[ti[out[h+(d,)]],:,d])
  rows=np.array(rows)
  profit=np.divide(loads[at],total[at],out=np.zeros(len(masks)),where=total[at]!=0)
  objectivebase=profit+fresh*(loads[at]>0)
  rng.shuffle(comparisons);chosen= None;chosenval=1.0
  for comp in comparisons:
   cmp=fresh*(member[:,comp].sum(axis=1)>0)
   if not any(cmp):continue
   obj=objectivebase-cmp
   if min(obj)>=0:continue
   res=linprog(obj,A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=[cmp],b_eq=[1.0],bounds=(0,None),method='highs')
   if res.success and res.fun<chosenval-1e-10:chosenval=res.fun;chosen=res.x
   if res.success and res.fun<best-1e-8:
    best=float(res.fun);data=dict(scope='Floating candidate only for P+Delta>=freshOPT at legal background',q=q,k=k,prefix=prefix,actual=actual,comparison=comp,policy=[[h,a]for h,a in policy.items()],weights={int(mask):float(w)for mask,w in zip(masks,res.x)if w>1e-9},gap=best,trial=trial,seed=seed)
    (HERE/'whole_gap_candidate.json').write_text(json.dumps(data,indent=2)+'\n');print('FOUND',json.dumps(data),flush=True);return
  if chosen is not None:
   walk_weights=chosen*1000
  else:walk_weights=None
  if trial%20==0:print('trial',trial,'elapsed',round(time.time()-start,1),'best',best,'last',round(chosenval,8),flush=True)
 print('done',dict(q=q,k=k,trials=trials,best=best,seconds=round(time.time()-start,1),seed=seed),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--q',type=int,default=6);p.add_argument('--k',type=int,default=3);p.add_argument('--trials',type=int,default=1000);p.add_argument('--seed',type=int,default=640130);a=p.parse_args();probe(a.q,a.k,a.trials,a.seed)
