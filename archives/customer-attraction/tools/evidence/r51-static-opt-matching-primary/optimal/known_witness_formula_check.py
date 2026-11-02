"""One deterministic formula regression on an already archived 1953-client witness.
This does not run the LP or construct a new counterexample.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, permutations
import importlib.util, json, sys, hashlib
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent/'runtime'
SRC=ROOT/'research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/cone/probe_static_opt_matching.py'
spec=importlib.util.spec_from_file_location('probe_under_test',SRC)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
DATA=BASE/'known-witness-input'
inst=json.loads((DATA/'assignment_instance.json').read_text())
policy=json.loads((DATA/'assignment_full_policy.json').read_text())
p,m=len(inst['topics']),inst['players']
weights=[F(0)]*((1<<p)-1)
for c in inst['customers']:
 mask=sum(1<<a for a in c['topics']);weights[mask-1]+=c['multiplicity']
actions={tuple(map(int,h.split(','))) if h else ():a for h,a in policy['policy'].items()}
z=mod.root_path(actions,m)
C=[set(c['topics']) for c in inst['customers']]
def direct_payoff(t,i):
 return sum((F(c['multiplicity'],sum(a in sig for a in t)) for sig,c in zip(C,inst['customers']) if t[i] in sig),F(0))
def direct_coverage(t):
 return sum(c['multiplicity'] for sig,c in zip(C,inst['customers']) if any(a in sig for a in t))
W=direct_coverage(z)
supports=list(combinations(range(p),m))
optimum=max(direct_coverage(J) for J in supports)
optimal=[J for J in supports if direct_coverage(J)==optimum]
checks=0;table=[]
for J in optimal:
 for pi in permutations(J):
  direct=sum((direct_payoff(z[:i]+(a,)+z[i+1:],i) for i,a in enumerate(pi)),F(0))
  source=mod.dot(mod.static_cost_row(p,z,pi),weights)
  assert direct==source
  table.append({'assignment':list(pi),'static_cost':str(source)})
  checks+=1
assert z==(0,3,4) and W==1735 and optimum==1740 and optimal==[(1,2,5)]
assert min(F(x['static_cost']) for x in table)==1736
out={'scope':'known archived witness formula regression only; no LP run or new counterexample','input_sha256':hashlib.sha256((DATA/'assignment_instance.json').read_bytes()).hexdigest(),'policy_sha256':hashlib.sha256((DATA/'assignment_full_policy.json').read_bytes()).hexdigest(),'actual':z,'W':W,'OPT':optimum,'optimal_distinct_supports':optimal,'all_assignment_costs':table,'direct_vs_source_formula_checks':checks,'minimum_static_cost':'1736','status':'PASS'}
(BASE/'known-witness-formula-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':checks,'W':W,'OPT':optimum,'min_static_cost':1736}))
