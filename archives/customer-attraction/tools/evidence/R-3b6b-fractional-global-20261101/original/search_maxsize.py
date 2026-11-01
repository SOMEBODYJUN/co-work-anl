from fractional_explore import benchmark
from customer_attraction.model import Instance,CustomerType
from pathlib import Path
import random,json,itertools
rng=random.Random(883)
for n in [3,4,5]:
 for trial in range(1000):
  k=6
  ts=[CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randrange(1,10)) for mask in range(1,1<<k) if rng.random()<.35]
  ins=Instance(tuple(map(str,range(k))),tuple(ts),n); M,_=benchmark(ins,(0,)*k)
  sizes=[sum(x.multiplicity for x in ts if a in x.topics) for a in range(k)]
  a=max(range(k),key=lambda a:sizes[a])
  for bs in itertools.combinations_with_replacement(range(k),n-1):
   q=ins.counts(bs+(a,)); pay=ins.topic_payoffs(q)
   if float(pay[a])<M-1e-6 and min(float(pay[b]) for b in bs)>=M+1e-6:
    out={'instance':ins.to_dict(),'M':M,'largest':a,'witness':bs,'payoffs':list(map(str,ins.player_payoffs(bs+(a,))))}
    Path(__file__).with_name('maxsize_obstruction.json').write_text(json.dumps(out,indent=2))
    print(n,trial,'M',M,'q',bs+(a,),'pay',out['payoffs'],flush=True);raise SystemExit
 print('finished',n,flush=True)
