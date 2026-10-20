from toy_search import mixed_efx,cycle_trials
from itertools import product
from random import Random
from pathlib import Path
import json
P=Path(__file__).resolve().parent

def test_graph(n,edges,vals,trials,seed):
 rng=Random(seed);ends=list(product(vals,repeat=2));orient=list(product((0,1),repeat=len(edges)));bad=None
 for t in range(trials):
  p=tuple(rng.choice(ends) for e in edges)
  if not any(mixed_efx(n,edges,p,o,True) for o in orient):bad={'endpoint_utilities':p,'trial':t};break
 return {'n':n,'edges':edges,'endpoint_values':vals,'requested_trials':trials,'completed_trials':t+1,'seed':seed,'orientations_per_profile':len(orient),'counterexample_to_universal_EFXplus0':bad}
if __name__=='__main__':
 out=[cycle_trials(3,(-1,0,1)),cycle_trials(4,(-1,0,1)),test_graph(6,[(0,1),(1,2),(2,0),(0,3),(3,4),(2,5)],[-2,-1,0,1,2],10000,20261025),test_graph(5,[(0,1),(1,2),(2,0),(0,3),(3,4),(4,0)],[-2,-1,0,1,2],1000,20261026)]
 (P/'mixed_extension_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
