"""Definition-level Fraction audit; reads saved customers and full ordered policies only."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib,sys

def audit(path):
 data=Path(path).read_bytes(); x=json.loads(data); inst=x['instance']
 n=inst['players']; k=len(inst['topics']); types=[(frozenset(y['topics']),y['multiplicity']) for y in inst['customers']]
 actions={tuple(h):a for h,a in x['actions']}; cert=x['certificate']
 assert len(actions)==len(x['actions']) and len(actions)==sum(k**d for d in range(n))
 assert actions=={tuple(r['history']):r['action'] for r in cert['actions']}
 for d in range(n):
  assert all(h in actions and 0<=actions[h]<k for h in product(range(k),repeat=d))
 def finish(h):
  while len(h)<n: h=h+(actions[h],)
  return h
 def payoff(t,i):
  return sum((F(m,sum(a in S for a in t)) for S,m in types if t[i] in S),F())
 def coverage(t): return sum(m for S,m in types if any(a in S for a in t))
 terminal=finish(()); counts=[terminal.count(a) for a in range(k)]
 assert counts==x['actual']==cert['terminal_counts'] and terminal[0]==x['root_action']
 checks=[]
 for d in range(n):
  for h in product(range(k),repeat=d):
   actual=finish(h); u=payoff(actual,d)
   for a in range(k):
    deviated=finish(h+(a,)); delta=u-payoff(deviated,d)
    checks.append({'history':list(h),'chosen':actions[h],'deviation':a,'chosen_terminal':list(actual),'deviation_terminal':list(deviated),'slack':str(delta)})
 negatives=[r for r in checks if F(r['slack'])<0]
 opt=max(coverage(t) for t in product(range(k),repeat=n)); w=coverage(terminal)
 return {'source':str(path),'source_sha256':hashlib.sha256(data).hexdigest(),'players':n,'topics':k,'unit_customers':sum(m for S,m in types),'ordered_nodes':len(actions),'comparisons_including_self':len(checks),'comparisons_excluding_self':len(checks)-len(actions),'minimum_slack':str(min(F(r['slack']) for r in checks)),'negative_comparisons':len(negatives),'full_ordered_pure_SPE':not negatives,'actual_terminal':list(terminal),'actual_payoffs':list(map(str,[payoff(terminal,i) for i in range(n)])),'welfare':w,'static_optimum_with_repetitions':opt,'half_margin':str(F(w)-F(opt,2)),'comparison_table':checks}
if __name__=='__main__':
 print(json.dumps([audit(p) for p in sys.argv[1:]],ensure_ascii=False,indent=2))
