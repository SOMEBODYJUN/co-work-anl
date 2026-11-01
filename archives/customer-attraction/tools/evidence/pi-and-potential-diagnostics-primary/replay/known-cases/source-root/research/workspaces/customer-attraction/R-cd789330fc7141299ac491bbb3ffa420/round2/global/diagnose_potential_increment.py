"""One diagnostic of the explicit optimal-potential increment candidate.
Known three/four-player instances only; exact outcome-set solver is imported
and this dependency is explicit. This is not a full-strategy independent audit.
"""
from pathlib import Path
from fractions import Fraction as F
import json
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate
HERE=Path(__file__).parent;REPO=HERE.parents[5]
def comps(n,k):
 if k==1:
  yield (n,);return
 for a in range(n+1):
  for t in comps(n-a,k-1):yield (a,)+t
cases=[]
for name in ('individual_security_failure','local_security_increment','prefix_balance_failure','fractional_actual_load_failure'):
 raw=json.loads((REPO/'examples/customer_attraction'/f'{name}.json').read_text())
 ins=Instance.from_dict(raw);solver=ExactSPESolver(ins);m=ins.players;k=ins.topic_count
 H=[F(0)]
 for i in range(1,m+2):H.append(H[-1]+F(1,i))
 prefixes=[(0,)*k]
 if m==4:prefixes +=[tuple(int(a==b) for a in range(k))for b in range(k)]
 for prefix in prefixes:
  r=m-sum(prefix)
  def potential(q):
   return sum((t.multiplicity*(H[sum((prefix[a]+q[a])for a in t.topics)]-H[sum(prefix[a]for a in t.topics)]) for t in ins.customers),F(0))
  opt={n:max((potential(q),q)for q in comps(n,k))for n in (r,r+1)}
  delta=opt[r+1][0]-opt[r][0];floor=solver.threshold(prefix)
  row={'source':name,'m':m,'prefix':prefix,'remaining':r,'root_floor_all_SPE':str(floor),'P_r':str(opt[r][0]),'P_r1':str(opt[r+1][0]),'delta':str(delta),'margin':str(floor-delta),'maximizers':{str(n):q for n,(_,q)in opt.items()}}
  cases.append(row)
  print(json.dumps(row),flush=True)
  if delta>floor:
   # Find the minimax-floor action and its worst child continuation, then
   # choose an allowed root outcome with that exact floor.
   target=None
   for a in range(k):
    child=list(prefix);child[a]+=1
    for q in solver.outcomes(child):
     if ins.topic_payoff(a,q)==floor:target=q;chosen=a;break
    if target is not None:break
   assert target is not None and prefix==(0,)*k
   cert=solver.certificate(target,on_path=next(p for p in solver.ordered_outcomes(target) if p[0]==chosen))
   ver=verify_certificate(ins,cert);ver.assert_valid()
   (HERE/'potential_increment_counterexample.json').write_text(json.dumps({'diagnostic':row,'instance':ins.to_dict(),'certificate':cert.to_dict(),'verification':{'histories':ver.checked_histories,'deviations':ver.checked_deviations}},indent=2)+'\n')
   (HERE/'potential_increment_diagnostic.json').write_text(json.dumps(cases,indent=2)+'\n')
   print('EXACT_CANDIDATE_COUNTEREXAMPLE');raise SystemExit
(HERE/'potential_increment_diagnostic.json').write_text(json.dumps(cases,indent=2)+'\n')
