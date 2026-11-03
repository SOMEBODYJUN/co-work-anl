"""Independent definition-level replay of the old exact FOMA-EXISTS separator.
No canonical model/solver or original audit imports. No new-input search.
"""
from fractions import Fraction
from itertools import product,permutations
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
SOURCE=ROOT/'research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json'
d=json.loads(SOURCE.read_text());raw=d['instance'];m=raw['players'];n=len(raw['topics'])
clients=[frozenset(r['topics']) for r in raw['customers'] for _ in range(r['multiplicity'])]
rows=d['certificate']['actions'];sigma={tuple(r['history']):r['action'] for r in rows}
assert len(rows)==len(sigma)==sum(n**k for k in range(m))
assert set(sigma)=={h for k in range(m) for h in product(range(n),repeat=k)}
def finish(h):
 h=tuple(h)
 while len(h)<m:h+=sigma[h],
 return h
def utility(z,i):
 return sum((Fraction(1,sum(a in x for a in z)) for x in clients if z[i] in x),Fraction(0))
def welfare(z):return sum(any(a in x for a in z) for x in clients)
actual=finish(());W=welfare(actual);checks=0
for h in sigma:
 u=utility(finish(h),len(h))
 for a in range(n):
  assert u>=utility(finish(h+(a,)),len(h));checks+=1
leaves=list(product(range(n),repeat=m));OPT=max(map(welfare,leaves));opts=[z for z in leaves if welfare(z)==OPT]
matrix=[[str(utility(actual[:i]+(a,)+actual[i+1:],i)) for a in (0,1,4,5)] for i in range(m)]
costs=[sum((utility(actual[:i]+(t[i],)+actual[i+1:],i) for i in range(m)),Fraction(0)) for t in opts]
report={'source':str(SOURCE.relative_to(ROOT)),'scope':'old exact FOMA-EXISTS counterexample only, not Q-CAG-HALF','unit_customers':len(clients),'histories':len(sigma),'IC_checks_including_self':checks,'actual':actual,'payoffs':[str(utility(actual,i)) for i in range(m)],'W':W,'OPT':OPT,'optimal_supports':sorted({tuple(sorted(set(t))) for t in opts}),'optimal_ordered_tuples':len(opts),'query_columns':[0,1,4,5],'query_matrix':matrix,'min_K':str(min(costs)),'max_K':str(max(costs)),'FOMA_EXISTS_false':min(costs)>W}
assert report['FOMA_EXISTS_false'] and W==47 and OPT==52 and min(costs)==48
(HERE/'old_foma_counterexample_independent.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
