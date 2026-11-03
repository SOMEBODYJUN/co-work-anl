"""Independent exact audit of saved policy tables and rounded LP support.
No import of any discovery program or canonical solver. Count-policy audit
represents every ordered history via deterministic count continuation.
"""
import json,math
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
BASE=Path(__file__).resolve().parent
FILES=['count_m5k6.json','count_m7k7.json','bg_m5r4k6.json','strong_count_m5k6.json','full_m5k7.json','full_bi_m5k7.json','canonical_strong.json','prefix_family_m5.json','price_m5k7.json']

def audit(rec):
 cert=rec.get('cert',rec.get('certificate'))
 root=tuple(rec['root']);k=len(root);m=sum(root);bg=tuple(rec.get('background',[0]*k));r=m-sum(bg)
 raw=cert['actions'] if cert else rec['actions'];countmode='counts' in raw[0];key='counts' if countmode else 'history';actions={tuple(a[key]):a['action'] for a in raw}
 expected=math.comb(k+r-1,k) if countmode else sum(k**d for d in range(m))
 if len(actions)!=expected:raise AssertionError((len(actions),expected))
 weights=[(int(mask),F(str(v)).limit_denominator(1000000)) for mask,v in rec['weights'].items()]
 @lru_cache(None)
 def terminal(h):
  if (sum(h) if countmode else len(h))==m:return h if countmode else tuple(h.count(a) for a in range(k))
  a=actions[h]
  if countmode:
   q=list(h);q[a]+=1;return terminal(tuple(q))
  return terminal(h+(a,))
 @lru_cache(None)
 def payoff(q,a):
  return sum((w/F(sum(q[b] for b in range(k) if mask>>b&1)) for mask,w in weights if mask>>a&1),F(0))
 start=bg if countmode else ();assert terminal(start)==root
 low=F(0);comparisons=0
 for h,a in actions.items():
  if countmode:
   assert all(h[b]>=bg[b] for b in range(k)) and sum(h)<m
  chosen=payoff(terminal(h),a)
  for b in range(k):
   if a==b:continue
   if countmode:
    q=list(h);q[b]+=1;q=tuple(q)
   else:q=h+(b,)
   slack=chosen-payoff(terminal(q),b);low=min(low,slack);comparisons+=1
 return {'mode':'count_table_all_ordered_histories' if countmode else 'full_ordered_history_table','states_checked':len(actions),'comparisons_checked':comparisons,'full_ordered_histories_represented':sum(k**d for d in range(r)),'min_exact_rounded_mass_slack':str(low),'rounded_mass_policy_valid':low>=0,'support':len(weights),'m':m,'k':k,'old':sum(bg)}

def main():
 reports=[]
 for name in FILES:
  obj=json.loads((BASE/name).read_text());recs=obj.get('records',[obj]);rs=[audit(rec) for rec in recs]
  out={'file':name,'records':len(rs),'valid_rounded_supports':sum(r['rounded_mass_policy_valid'] for r in rs),'states_checked':sum(r['states_checked'] for r in rs),'comparisons_checked':sum(r['comparisons_checked'] for r in rs),'full_ordered_histories_represented':sum(r['full_ordered_histories_represented'] for r in rs),'max_saved_value':max(r['value'] for r in recs),'record_audits':rs};reports.append(out)
  print(json.dumps({k:v for k,v in out.items() if k!='record_audits'}),flush=True)
 (BASE/'scope_audit.json').write_text(json.dumps({'status':'finite_exact_policy_table_audit_only; no universal candidate result','rationalization_denominator_limit':1000000,'reports':reports},indent=2)+'\n')
if __name__=='__main__':main()
