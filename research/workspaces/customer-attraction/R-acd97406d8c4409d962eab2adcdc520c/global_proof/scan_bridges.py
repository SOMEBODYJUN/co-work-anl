import random,itertools,json,time
from customer_attraction import Instance, CustomerType, ExactSPESolver

def comps(n,k):
 if k==1:yield (n,);return
 for x in range(n+1):
  for z in comps(n-x,k-1):yield (x,)+z

def check(inst):
 solver=ExactSPESolver(inst)
 outcomes=solver.outcomes()
 pne=[]
 for c in comps(inst.players,inst.topic_count):
  pays=inst.topic_payoffs(c)
  ok=True
  for a in range(inst.topic_count):
   if not c[a]:continue
   for b in range(inst.topic_count):
    d=list(c);d[a]-=1;d[b]+=1
    if inst.topic_payoff(b,d)>pays[a]:ok=False;break
   if not ok:break
  if ok:pne.append(c)
 minpne=min(inst.welfare(c) for c in pne)
 for c in outcomes:
  w=inst.welfare(c)
  if minpne>w:return 'PNE',c,minpne,solver
  residual=Instance(inst.topics,tuple(z for z in inst.customers if not any(c[t] for t in z.topics)),inst.players)
  r=residual.optimal_welfare()
  if r>w:return 'RESIDUAL',c,r,solver
 return None

if __name__=='__main__':
 rng=random.Random(197)
 start=time.time()
 for j in range(2000):
  k=rng.choice([4,5,6]);m=rng.choice([2,3,4])
  customers=tuple(CustomerType(frozenset(t for t in range(k) if mask>>t&1),rng.randint(1,8)) for mask in range(1,1<<k) if rng.random()<.4)
  inst=Instance(tuple(map(str,range(k))),customers,m)
  result=check(inst)
  if result:
   kind,c,v,solver=result
   obj={'kind':kind,'instance':inst.to_dict(),'counts':c,'welfare':inst.welfare(c),'comparison':v,'certificate':solver.certificate(target_counts=c).to_dict()}
   path='research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/bridge_counterexample.json'
   open(path,'w').write(json.dumps(obj,indent=2));print(kind,c,inst.welfare(c),v,j,flush=True);break
  if j%50==0:print(j,round(time.time()-start,2),flush=True)
