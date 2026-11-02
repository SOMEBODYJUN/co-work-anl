"""One fixed saved complete policy, its source and optimized unit-customer inputs.
Exact stdlib integer comparison; does not import the walk, LP, or outcome oracle.
"""
from pathlib import Path
from itertools import product, combinations
from functools import lru_cache
from math import lcm
from fractions import Fraction as F
from collections import Counter
import json,hashlib
HERE=Path(__file__).resolve().parent
P,M=7,5
SCALE=lcm(*range(1,M+1))

def main():
 data=json.loads((HERE/'original/f4ee26fe8ac278bb7d81/best_policy.json').read_text())
 entries=data['strategy']['actions']
 assert all(set(row)=={'history','action'} for row in entries)
 actions={tuple(row['history']):row['action'] for row in entries}
 expected={h for d in range(M) for h in product(range(P),repeat=d)}
 assert len(actions)==len(entries)==2801 and set(actions)==expected
 assert all(type(a)==int and a in range(P) for a in actions.values())
 assert set(actions.values())=={0,1}
 @lru_cache(None)
 def finish(h):return h if len(h)==M else finish(h+(actions[h],))
 actual=finish(());counts=[actual.count(a) for a in range(P)]
 assert counts==data['strategy']['terminal_counts']==data['target']
 out={'scope':'one saved strategy, exactly two fixed customer inputs; all ordered histories retained','scale':SCALE,'decision_histories':len(expected),'actual':actual,'counts':counts,'action_counts':dict(Counter(actions.values())),'models':[]}
 for key in ('source','integer_clones'):
  vector=data[key];assert len(vector)==127 and all(type(n)==int and n>=0 for n in vector)
  blocks=[(mask,n) for mask,n in enumerate(vector,1) if n]
  @lru_cache(None)
  def utility(z,a):
   value=0
   for mask,n in blocks:
    if mask>>a&1:
     denominator=sum(mask>>b&1 for b in z)
     assert denominator>0 and SCALE%denominator==0
     value+=n*(SCALE//denominator)
   return value
  def coverage(z):return sum(n for mask,n in blocks if any(mask>>a&1 for a in z))
  strict=ties=0;minimum=None;maximum=None;levels=[]
  for depth in range(M):
   lev={'depth':depth,'histories':P**depth,'comparisons':0,'strict':0,'ties':0}
   for h in product(range(P),repeat=depth):
    a=actions[h];u=utility(finish(h),a)
    for q in range(P):
     slack=u-utility(finish(h+(q,)),q)
     assert slack>=0,(key,h,a,q,slack)
     minimum=slack if minimum is None else min(minimum,slack)
     maximum=slack if maximum is None else max(maximum,slack)
     lev['comparisons']+=1;lev['strict']+=int(slack>0);lev['ties']+=int(slack==0)
   strict+=lev['strict'];ties+=lev['ties'];levels.append(lev)
  supports=list(combinations(range(P),M));vals=[coverage(s) for s in supports];optimum=max(vals)
  w=coverage(actual);payoffs=[str(F(utility(actual,a),SCALE)) for a in actual]
  static=[]
  for i,a in enumerate(actual):
   base=utility(actual,a)
   for q in range(P):
    z=actual[:i]+(q,)+actual[i+1:];slack=base-utility(z,q)
    assert slack>=0
    static.append(slack)
  result={'field':key,'vector_sha256':hashlib.sha256(json.dumps(vector,separators=(',',':')).encode()).hexdigest(),'unit_customers':sum(vector),'nonzero_mask_multiplicities':dict(blocks),'actual_payoffs':payoffs,'W':w,'OPT_5':optimum,'ratio':str(F(optimum,w)),'half_margin':2*w-optimum,'coverage_supports_checked':len(supports),'optimal_supports':[s for s,v in zip(supports,vals) if v==optimum],'portfolio_coverage':coverage(data['portfolio']),'IC_comparisons_including_self':strict+ties,'strict':strict,'ties':ties,'minimum_slack':str(F(minimum,SCALE)),'maximum_slack':str(F(maximum,SCALE)),'levels':levels,'static_PNE_comparisons':len(static),'static_minimum_slack':str(F(min(static),SCALE)),'static_maximum_slack':str(F(max(static),SCALE))}
  assert w==5 and optimum==9 and result['ratio']=='9/5'
  assert sum(F(v) for v in payoffs)==w
  if key=='integer_clones':assert (w,optimum)==(data['welfare'],data['optimum'])
  out['models'].append(result)
 return out

if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=2))
