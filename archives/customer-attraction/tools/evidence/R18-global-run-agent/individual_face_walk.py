from __future__ import annotations
from pathlib import Path
import sys,json,random,math,time,argparse,hashlib
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'counterexample_search'))
from cone_walk import Engine,baseline,verify_canonical

def recover(G,norm,x):
 supp=np.flatnonzero(x>1e-8).tolist();active=np.flatnonzero(np.abs(G@x)<1e-7)
 basis={}
 for ri,row in enumerate([norm]+[G[j] for j in active]):
  v=[F(int(row[j])) for j in supp]+[F(ri==0)]
  for pivot in sorted(basis):
   z=v[pivot]
   if z:v=[a-z*b for a,b in zip(v,basis[pivot])]
  pivot=next((j for j,z in enumerate(v[:-1]) if z),None)
  if pivot is not None:
   z=v[pivot];basis[pivot]=[a/z for a in v]
  elif v[-1]:return None
  if len(basis)==len(supp):break
 if len(basis)!=len(supp):return None
 sol=[F(0)]*len(supp)
 for pivot in sorted(basis,reverse=True):sol[pivot]=basis[pivot][-1]-sum(basis[pivot][j]*sol[j] for j in range(pivot+1,len(supp)))
 if min(sol)<0:return None
 scale=math.lcm(*(v.denominator for v in sol));clones=[0]*len(x)
 for j,v in zip(supp,sol):clones[j]=int(v*scale)
 common=math.gcd(*clones);clones=[v//common for v in clones]
 if any(sum(int(row[j])*clones[j] for j in supp)<0 for row in G):return None
 return clones

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=5);ap.add_argument('--topics',type=int,default=7);ap.add_argument('--steps',type=int,default=200);ap.add_argument('--seed',type=int,default=68111);args=ap.parse_args()
 rng=random.Random(args.seed);n=args.players;p=args.topics;eng=Engine(n,p,rng);started=time.time()
 seeds=[baseline(n,p)];endpoints=[];best=F(0);seen=set();records=[]
 for s in range(20):
  r=baseline(n,p);scale=rng.choice([1,3,10]);r=[v*scale for v in r]
  for j in range(rng.randrange(1,7)):
   mask=sum(1<<a for a in rng.sample(range(p),rng.randrange(2,min(p,5)+1)));r[mask-1]+=rng.randint(1,2*scale)
  seeds.append(r)
 for s in range(100):
  r=[rng.randrange(1,15) if rng.random()<rng.choice([.1,.3,.6]) else 0 for j in range((1<<p)-1)]
  if sum(r):seeds.append(r)
 for step in range(args.steps):
  if seeds:r=seeds.pop(0)
  else:
   r=list(rng.choice(endpoints));scale=rng.choice([1,5,20,100]);r=[v*scale for v in r]
   for j in range(rng.randrange(1,4)):r[rng.randrange(len(r))]+=rng.random()*.05
  eng.solve(r)
  outcomes=eng.R[0][0];mins=np.array([min(eng.u[t,a] for a,q in enumerate(eng.terminal[t]) if q) for t in outcomes]);ts=outcomes[mins<=mins.min()+eng.eps]
  target=int(rng.choice(list(ts)));a=min((a for a,q in enumerate(eng.terminal[target]) if q),key=lambda a:eng.u[target,a])
  actions,G=eng.strategy(target);key=hashlib.sha256(repr(actions).encode()).hexdigest()
  if key in seen:continue
  seen.add(key);norm=eng.pay[target,a]
  js=list(dict.fromkeys([int(np.argmax(eng.v@np.array(r))),rng.randrange(len(eng.portfolios))]))
  for jid in js:
   objective=eng.v[jid].astype(float)
   res=linprog(-objective,A_ub=-G.astype(float),b_ub=np.zeros(len(G)),A_eq=[norm.astype(float)],b_eq=[eng.L],bounds=(0,None),method='highs')
   if not res.success:continue
   x=res.x;value=float(objective@x);endpoints.append(x.tolist())
   records.append({'step':step,'target':eng.terminal[target].tolist(),'a':a,'value':value,'J':eng.portfolios[jid],'rows':len(G)})
   if value>float(best)+1e-8:
    clones=recover(G,norm,x)
    if clones is None:print(json.dumps({'unrecovered':value,'step':step}),flush=True);continue
    inst,cert=verify_canonical(n,p,clones,actions,eng.terminal[target].tolist());root=tuple(map(int,eng.terminal[target]));u=inst.topic_payoff(a,root);O=inst.optimal_welfare();ratio=F(O,u)
    if ratio>best:
     best=ratio;proof={'scope':'one full-history pure SPE, individual OPT/(2m-1) bridge probe','parameters':vars(args),'step':step,'individual_ratio':str(ratio),'a':a,'u':str(u),'OPT':O,'W':inst.welfare(root),'instance':inst.to_dict(),'strategy':cert.to_dict(),'verified':True}
     (HERE/f'individual_face_walk_n{n}p{p}_best.json').write_text(json.dumps(proof,indent=2)+'\n')
     print(json.dumps({'step':step,'new_exact_best':str(best),'threshold':2*n-1,'elapsed':round(time.time()-started,2)}),flush=True)
     if best>2*n-1:print('BRIDGE COUNTEREXAMPLE',flush=True);return
   if value>=2*n-1-1e-8 and rng.random()<.8:seeds.append(x.tolist())
  if step%10==0:
   report={'parameters':vars(args),'steps':step+1,'best':str(best),'elapsed':time.time()-started,'records':records};(HERE/f'individual_face_walk_n{n}p{p}_run.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'step':step,'cones':len(seen),'best':str(best),'elapsed':round(time.time()-started,2)}),flush=True)
 (HERE/f'individual_face_walk_n{n}p{p}_run.json').write_text(json.dumps({'parameters':vars(args),'best':str(best),'elapsed':time.time()-started,'records':records},indent=2)+'\n')
if __name__=='__main__':main()
