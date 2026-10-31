from fractions import Fraction
from itertools import combinations, product
import hashlib, json
from pathlib import Path
SRC=Path('../../cyclic-extension-terminal-support-and-root-audit-primary/related-original/largest_incumbent_n3p6_best.json').resolve()
raw=SRC.read_bytes(); data=json.loads(raw)
inst=data['instance']; p,m=len(inst['topics']),inst['players']
units=tuple(frozenset(row['topics']) for row in inst['customers'] for _ in range(row['multiplicity']))
policy={tuple(row['history']):row['action'] for row in data['strategy']['actions']}
histories=tuple(h for d in range(m) for h in product(range(p),repeat=d))
assert len(units)==963 and len(policy)==len(histories)==43
assert set(policy)==set(histories) and all(a in range(p) for a in policy.values())
def terminal(h):
 while len(h)<m: h=h+(policy[h],)
 return h
def payoff(h,a):
 path=terminal(h)
 return sum((Fraction(1,sum(t in B for t in path)) for B in units if a in B),Fraction(0))
def welfare(path): return sum(any(a in B for a in path) for B in units)
bad=[]; rows=0
for h in histories:
 a=policy[h];actual=payoff(h,a)
 for b in range(p):
  if b==a: continue
  rows+=1; dev=payoff(h+(b,),b)
  if actual<dev: bad.append({'history':h,'chosen':a,'deviation':b,'actual':str(actual),'deviating':str(dev),'gain':str(dev-actual),'branch_terminal':terminal(h+(b,))})
path=terminal(())
opt=max(welfare(J) for J in combinations(range(p),min(m,p)))
assert tuple(path.count(a) for a in range(p))==tuple(data['strategy']['terminal_counts'])
assert path==(0,2,3) and payoff((),0)==Fraction(375,2) and payoff((3,),3)==357
assert len(bad)==5 and all(not b['history'] for b in bad)
out={'source':str(SRC),'source_sha256':hashlib.sha256(raw).hexdigest(),'unit_customers':len(units),'players':m,'topics':p,'decision_histories':len(histories),'proper_deviation_checks':rows,'full_history_SPE':False,'root_bad_count':len(bad),'bad_comparisons':bad,'actual_path':path,'actual_payoffs':[str(payoff((),a)) for a in path],'welfare':welfare(path),'optimum':opt,'source_verified_flag':data['verified'],'status':'pass-root-omission-confirmed'}
print(json.dumps(out,indent=2))
