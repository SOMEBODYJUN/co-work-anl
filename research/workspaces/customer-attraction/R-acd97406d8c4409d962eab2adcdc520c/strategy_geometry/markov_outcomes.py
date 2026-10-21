"""Compare exact all-history SPE outcomes with exhaustive count-Markov SPE outcomes.
Every state policy is enumerated; terminal outcomes at shared child states are one
common value. A state-map count cap aborts rather than claiming completeness.
"""
import sys,random,json
from pathlib import Path
from itertools import product
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver,verify_certificate

def vectors(p,d):
 if p==1:yield (d,);return
 for a in range(d+1):
  for tail in vectors(p-1,d-a):yield(a,)+tail

def increment(q,a):return q[:a]+(q[a]+1,)+q[a+1:]

def markov_outcomes(inst,cap=200000):
 p,n=inst.topic_count,inst.players
 payoff={q:inst.topic_payoffs(q) for q in vectors(p,n)}
 maps=[{}]
 for d in range(n-1,-1,-1):
  states=list(vectors(p,d));next_maps=[]
  for deep in maps:
   choices=[]
   for q in states:
    ends=[(increment(q,a) if d==n-1 else deep[increment(q,a)]) for a in range(p)]
    us=[payoff[end][a] for a,end in enumerate(ends)];mx=max(us)
    choices.append(set(end for end,u in zip(ends,us) if u==mx))
   for es in product(*choices):
    shallow=dict(deep);shallow.update(zip(states,es));next_maps.append(shallow)
    if len(next_maps)>cap:raise OverflowError
  maps=next_maps
 return {m[(0,)*p] for m in maps},len(maps)

if __name__=='__main__':
 p=int(sys.argv[1]) if len(sys.argv)>1 else 3;n=int(sys.argv[2]) if len(sys.argv)>2 else 3
 rng=random.Random(14037);maximum=0
 for t in range(20000):
  masses=[rng.randrange(4) for _ in range((1<<p)-1)]
  inst=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),r)for mask,r in enumerate(masses,1)if r),n)
  full=ExactSPESolver(inst).outcomes()
  try:markov,count=markov_outcomes(inst)
  except OverflowError:continue
  maximum=max(maximum,count)
  if full!=markov:
   d={'iteration':t,'players':n,'topics':p,'masses':masses,'full':list(full),'markov':list(markov),'missing':list(full-markov)}
   path=Path(__file__).parent/'markov_counterexample.json';path.write_text(json.dumps(d,indent=2))
   print('COUNTEREXAMPLE',json.dumps(d),flush=True);break
  if t%1000==0:print('progress',t,'max_policies',maximum,flush=True)
 else:print('No mismatch',p,n,maximum)
