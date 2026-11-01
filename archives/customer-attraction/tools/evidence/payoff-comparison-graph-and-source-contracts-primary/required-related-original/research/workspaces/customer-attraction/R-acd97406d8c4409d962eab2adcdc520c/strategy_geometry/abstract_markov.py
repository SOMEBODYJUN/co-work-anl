import sys,random,json
from pathlib import Path
from itertools import product
sys.path.insert(0,str(Path(__file__).parent))
from markov_outcomes import vectors,increment
from functools import lru_cache

class Table:
 def __init__(self,p,n,rng):
  self.topic_count=p;self.players=n
  self.payoff={q:tuple(rng.randrange(3) if q[a] else 0 for a in range(p))for q in vectors(p,n)}
 def topic_payoffs(self,q):return self.payoff[q]

def full_outcomes(inst):
 p,n=inst.topic_count,inst.players
 @lru_cache(None)
 def solve(q):
  if sum(q)==n:return frozenset((q,))
  children=[solve(increment(q,a))for a in range(p)]
  threshold=max(min(inst.payoff[t][a]for t in child)for a,child in enumerate(children))
  return frozenset(t for a,child in enumerate(children)for t in child if inst.payoff[t][a]>=threshold)
 return solve((0,)*p)

if __name__=='__main__':
 from markov_outcomes import markov_outcomes
 rng=random.Random(643);p=3;n=3
 for t in range(10000):
  inst=Table(p,n,rng);full=full_outcomes(inst)
  try:markov,count=markov_outcomes(inst,200000)
  except OverflowError:continue
  if full!=markov:
   d={'iteration':t,'players':n,'topics':p,'payoffs':[{'q':q,'u':u}for q,u in inst.payoff.items()],'full':list(full),'markov':list(markov),'missing':list(full-markov)}
   path=Path(__file__).parent/'abstract_markov_counterexample.json';path.write_text(json.dumps(d,indent=2))
   print(json.dumps(d),flush=True);break
 else:print('no mismatch')
