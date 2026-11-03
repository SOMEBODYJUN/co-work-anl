"""Consume all frozen primary JSON fields and bind the two actual original runs.
No optimizer, random scan, repeated equilibrium solve, or general SPE claim for
floating probe policies is performed here.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import product
from math import factorial
import json,hashlib
B=Path(__file__).resolve().parent
PFX='research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/direct_coverage/'
P=B/'original'/PFX;RUN=B/'replay/source-root'/PFX
out={'scope':'all primary saved-field reading and exact-source binding','files':{}}
def walk(x,c):
 c[type(x).__name__]+=1
 if isinstance(x,dict):
  for k,v in x.items():c['keys']+=1;walk(v,c)
 elif isinstance(x,list):
  for v in x:walk(v,c)
for p in sorted(P.glob('*.json')):
 d=json.loads(p.read_text());c=Counter();walk(d,c);out['files'][p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'field_counts':dict(c)}
outputs=['exact_materialized_audit.json','materialized_row3_catalog.json','materialized_row3_true_spe.json','peer_relations_independent_audit.json']
out['original_outputs_bound']={}
for n in outputs:
 a=(P/n).read_bytes();b=(RUN/n).read_bytes();assert a==b,n
 out['original_outputs_bound'][n]={'bytes':len(a),'sha256':hashlib.sha256(a).hexdigest(),'byte_identical':True}
cat=json.loads((P/'materialized_row3_catalog.json').read_text());cert=json.loads((P/'materialized_row3_true_spe.json').read_text())
assert cat['players']==3 and len(cat['topics'])==18 and len(cat['customers'])==185
assert all(type(r['multiplicity']) is int and r['multiplicity']>0 and r['topics'] and len(set(r['topics']))==len(r['topics']) and all(type(a) is int and 0<=a<18 for a in r['topics']) for r in cat['customers'])
assert len({tuple(r['topics']) for r in cat['customers']})==185
units=sum(r['multiplicity'] for r in cat['customers']);assert units==32164464720
ac={tuple(r['history']):r['action'] for r in cert['actions']};assert len(ac)==len(cert['actions'])==343 and set(ac)=={h for d in range(3) for h in product(range(18),repeat=d)}
h=()
while len(h)<3:h=h+(ac[h],)
assert cert['terminal_counts']==[h.count(a) for a in range(18)]
out['materialized_fields']={'positive_distinct_customer_types':185,'unit_customers':units,'all_actions_consumed':343,'actual_history':h,'actual_labels':[cat['topics'][a] for a in h],'minimum_multiplicity':min(r['multiplicity'] for r in cat['customers']),'maximum_multiplicity':max(r['multiplicity'] for r in cat['customers'])}
frozen=json.loads((P/'frozen_row3_source_support.json').read_text());out['frozen_orbits']=[]
for item in frozen['support']:
 b,c,d,e,hist=item['state'];assert b==0 and len(hist)==8 and sum(hist)==5
 orbit=factorial(5)
 for cnt in hist:orbit//=factorial(cnt)
 assert item['integer_orbit_weight']%orbit==0
 out['frozen_orbits'].append({'state':item['state'],'original_saved_float_weight':item['weight'],'integer_orbit_weight':item['integer_orbit_weight'],'distinct_permutations':orbit,'per_type_integer':item['integer_orbit_weight']//orbit})
assert sum(z['distinct_permutations'] for z in out['frozen_orbits'])==185

def comps(n,k):
 if k==1:yield(n,);return
 for i in range(n+1):
  for t in comps(n-i,k-1):yield(i,)+t
out['cone_saved_policies']={}
for name,coefficient in [('row_cone_best.json',F(1)),('row3_allbig_cone.json',F(1)),('row3_strong_cone_best.json',F(4,5))]:
 data=json.loads((P/name).read_text());d=data['data'];policy={tuple(q):a for q,a in d['policy']};required={q for depth in range(5) for q in comps(depth,7)}
 assert len(policy)==len(d['policy'])==330 and set(policy)==required
 assert all(type(a) is int and 0<=a<7 for a in policy.values())
 weights={int(mask):F(str(v)) for mask,v in d['weights']};assert all(0<m<128 and v>=0 for m,v in weights.items())
 def follow(q):
  while sum(q)<5:
   a=policy[q];q=q[:a]+(q[a]+1,)+q[a+1:]
  return q
 q=(0,)*7;path=[]
 while sum(q)<5:
  a=policy[q];path.append(a);q=q[:a]+(q[a]+1,)+q[a+1:]
 assert path==d['path'] and list(q)==d['actual_counts']
 def U(a,q):return sum((w/F(sum(q[b] for b in range(7) if mask>>b&1)) for mask,w in weights.items() if mask>>a&1),F(0))
 def C(A):return sum((w for mask,w in weights.items() if any(mask>>a&1 for a in A)),F(0))
 old=tuple(path[:2].count(a) for a in range(7));row=F(0)
 for a in d['opt']:
  z=follow(old[:a]+(old[a]+1,)+old[a+1:]);row+=U(a,z)
 W=C(path);O=C(d['opt']);score=coefficient*W-O+row
 out['cone_saved_policies'][name]={'all_count_state_records_consumed':len(policy),'complete_history_action_count_if_expanded':2801,'actual_path':path,'saved_float_score':data['score'],'score_from_saved_decimal_data':str(score),'score_float_difference':float(score)-data['score'],'actual_W_from_decimal_data':str(W),'comparison_union_from_decimal_data':str(O),'query_row_from_decimal_data':str(row),'policy_action_histogram':dict(Counter(policy.values())),'single_customer_interest_mask':next(iter(weights)) if len(weights)==1 and next(iter(weights.values()))==1 else None,'every_policy_action_in_that_interest_set':all(next(iter(weights))>>a&1 for a in policy.values()) if len(weights)==1 else None,'new_generic_policy_IC_or_dual_claim':False}
 assert abs(float(score)-data['score'])<1e-12
true=json.loads((P/'true_row_probe_best.json').read_text());d=true['data'];weights={int(k):int(v) for k,v in d['weights'].items()};assert len(weights)==14 and all(v>0 for v in weights.values())
assert d['row60']-d['gap60']==true['score60']==3832 and d['gap60']==60*(d['OPT']-d['W'])
assert d['row60']==sum(d['minima60'][a] for a in d['opt'])+(d['root_payoffs60'][d['actual_action']]-d['minima60'][d['actual_action']])
assert sum(d['terminal_counts'][a]*d['root_payoffs60'][a] for a in range(7))==60*d['W']
out['true_row_saved_fields']={'iteration':true['iteration'],'score60':3832,'score':str(F(3832,60)),'integer_types_consumed':14,'total_unit_customers':sum(weights.values()),'occupied_labels':[a for a,n in enumerate(d['terminal_counts']) if n],'absent_label_payoff_entries_are_not_actual_player_payoffs':True,'fresh_probe_run':False}
(B/'saved-field-review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['files','frozen_orbits']},ensure_ascii=False,indent=2))
