"""Independent unit-customer, full-history SPE audit; no canonical solver import."""
from fractions import Fraction
from itertools import product,combinations
import json
from pathlib import Path

HERE=Path(__file__).parent
SOURCE=HERE.parent/'next_boss'/'terminal_exact_audit.json'

def audit(record):
 instance=record['instance'];m=instance['players'];p=len(instance['topics'])
 # Each compressed multiplicity is expanded into separate unit customers.
 customers=[frozenset(c['topics']) for c in instance['customers'] for _ in range(c['multiplicity'])]
 assert all(isinstance(c['multiplicity'],int) and c['multiplicity']>=0 for c in instance['customers'])
 def pay(path):
  out=[Fraction(0) for _ in range(m)]
  for likes in customers:
   providers=[i for i,a in enumerate(path) if a in likes]
   for i in providers:out[i]+=Fraction(1,len(providers))
  return tuple(out)
 def welfare(path):return sum(any(a in likes for a in path) for likes in customers)
 def unit_rows(path):
  rows=[]
  for x,likes in enumerate(customers):
   providers=[i for i,a in enumerate(path) if a in likes]
   shares=[Fraction(1,len(providers)) if i in providers else Fraction(0) for i in range(m)]
   rows.append({'unit_customer':x,'likes':sorted(likes),'provider_indices':providers,'shares':[str(z) for z in shares]})
  return rows
 # First obtain all legal SPE outcomes directly on ordered histories, before
 # reading or trusting the supplied strategy, using per-unit terminal payoffs.
 sets={}
 def outcome_set(h):
  if len(h)==m:return (h,)
  branch=[outcome_set(h+(a,)) for a in range(p)]
  mover=len(h)
  floor=max(min(pay(t)[mover] for t in option) for option in branch)
  ans=tuple(sorted(set(t for option in branch for t in option if pay(t)[mover]>=floor)))
  sets[h]=ans;return ans
 all_root=outcome_set(())
 target=tuple(record['actual_path']);assert target in all_root
 # Now read the proposed full strategy. Validate every ordered history, then
 # evaluate all actual one-step deviations under these exact supplied replies.
 strategy=record['strategy'];actions={tuple(r['history']):r['action'] for r in strategy['actions']}
 expected={h for k in range(m) for h in product(range(p),repeat=k)}
 assert set(actions)==expected and len(actions)==len(strategy['actions'])
 assert all(isinstance(a,int) and 0<=a<p for a in actions.values())
 def continuation(h):
  while len(h)<m:h=h+(actions[h],)
  return h
 root=continuation(());assert root==target
 rows=[];deviations=0
 for h in sorted(expected,key=lambda h:(len(h),h)):
  mover=len(h);a=actions[h];term=continuation(h);own=pay(term)[mover]
  alternatives=[]
  for b in range(p):
   alt=continuation(h+(b,));val=pay(alt)[mover]
   assert own>=val,(h,a,b,own,val)
   if b!=a:deviations+=1
   alternatives.append({'action':b,'terminal':list(alt),'payoff':str(val),'slack':str(own-val)})
  rows.append({'history':list(h),'chosen':a,'terminal':list(term),'chosen_payoff':str(own),'alternatives':alternatives})
 U=pay(root);W=welfare(root);opt=max(welfare(t) for t in product(range(p),repeat=m))
 root_branches=[{'action':a,'terminal':list(continuation((a,))),'root_payoff':str(pay(continuation((a,)))[0])} for a in range(p)]
 last_table=[]
 for h in product(range(p),repeat=m-1):
  vals=[pay(h+(a,))[-1] for a in range(p)];mx=max(vals)
  last_table.append({'history':list(h),'values':[str(z) for z in vals],'best_actions':[a for a,z in enumerate(vals) if z==mx],'prescribed':actions[h]})
 return {'source':str(SOURCE),'method':'expanded unit customers, ordered-history set recursion before reading strategy, then definition-level full-strategy deviation audit; no customer_attraction imports','customers':len(customers),'histories':len(expected),'nontrivial_deviations':deviations,'complete':True,'valid_SPE':True,'root_path':list(root),'unit_customer_account':unit_rows(root),'root_utilities':[str(x) for x in U],'root_welfare':W,'OPT':opt,'last_to_first_ratio':str(U[-1]/U[0]),'C1_slack_2u1_minus_um':str(2*U[0]-U[-1]),'C2_slack_2W_minus_(m+1)um':str(2*W-(m+1)*U[-1]),'half_slack_2W_minus_OPT':2*W-opt,'all_root_SPE_paths':len(all_root),'target_independently_realizable':target in all_root,'root_branches':root_branches,'last_reply_table':last_table,'all_deviation_rows':rows}

def main():
 record=json.loads(SOURCE.read_text())[0]['records'][0]
 result=audit(record)
 HERE.joinpath('terminal_clone_refutation_review.json').write_text(json.dumps(result,indent=2))
 print(json.dumps({k:v for k,v in result.items() if k not in ('all_deviation_rows','last_reply_table','unit_customer_account')},indent=2))
if __name__=='__main__':main()
