"""Exact finite discovery: append a disjoint private topic to the old 3-player gadget.
No claim of arbitrary-n behavior or full strategy enumeration.
"""
import json,sys,time
from pathlib import Path
from fractions import Fraction as F
from customer_attraction import Instance,ExactSPESolver
old=json.loads(Path('examples/customer_attraction/coverage_opportunity_failure.json').read_text())
for k in map(int,sys.argv[1:] or ['1','2','3','5','8','11']):
 d={'topics':old['topics']+['P'],'players':k+3,'customers':[{'topics':c['topics'],'multiplicity':2*c['multiplicity']} for c in old['customers']]+[{'topics':[5],'multiplicity':5*k}]}
 inst=Instance.from_dict(d);s=ExactSPESolver(inst);start=time.time();target=(2,1,0,0,0,k)
 outs=s.outcomes();feas=target in outs
 if feas:
  pref=(0,)*6
  for a in (5,)*k+(0,0,1):
   assert target in s.outcomes(pref)
   assert inst.topic_payoff(a,target)>=s.threshold(pref)
   pref=tuple(x+int(j==a) for j,x in enumerate(pref))
  n=k+3;alpha=F(n-1,n)
  load=[sum(target[a] for a in c['topics'])for c in d['customers']]
  g=[sum((F(c['multiplicity'])/(1+alpha*h) for c,h in zip(d['customers'],load) if a in c['topics']),F(0))for a in range(6)]
  G=sum((F(c['multiplicity'])/(1+alpha*h)for c,h in zip(d['customers'],load)if h),F(0));u=inst.topic_payoffs(target)
  print(k,'feasible',feas,'M',str(max(g)),'G',str(G),'min_u',str(min(u[a]for a,q in enumerate(target)if q)),'ind_gap',str(max(g)-G/n-min(u[a]for a,q in enumerate(target)if q)),'secs',time.time()-start,'stats',s.stats,flush=True)
 else:print(k,'feasible',feas,'secs',time.time()-start,'stats',s.stats,flush=True)
