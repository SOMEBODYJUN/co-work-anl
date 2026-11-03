"""Read all saved JSON fields and bind finite reports to the frozen bytes.
No LP/MILP, equilibrium oracle, old thirteen-player IC re-audit, or random scan.
The only mathematical checks here are source-specific certificate bookkeeping
and exact identities that make the saved trivial count-policy points explicit.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json,gzip,hashlib
BASE=Path(__file__).resolve().parent
P=BASE/'original/research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe'

def walk(x,counts):
 counts[type(x).__name__]+=1
 if isinstance(x,dict):
  for k,v in x.items(): counts['keys']+=1;counts['key_chars']+=len(k);walk(v,counts)
 elif isinstance(x,list):
  for v in x:walk(v,counts)
 elif isinstance(x,str):counts['string_chars']+=len(x)

report={'scope':'saved-field consumption and source/report binding, not a new solver audit','files':{}}
for p in sorted(P.rglob('*')):
 if p.suffix not in ('.json','.gz'):continue
 raw=p.read_bytes();d=json.loads(gzip.decompress(raw) if p.suffix=='.gz' else raw)
 c=Counter();walk(d,c)
 report['files'][str(p.relative_to(P))]={'sha256':hashlib.sha256(raw).hexdigest(),'counts':dict(c)}

# Each regenerated population node-table field is compared, not just the root.
pop=json.loads((P/'independent/population_audit.json').read_text())
newpop=json.loads((BASE/'replay/population/population_audit.json').read_text())
assert pop==newpop
small=json.loads((P/'independent/population_small.json').read_text())
assert small['instance']['customers']==pop['types']
assert len({tuple(r['history']) for r in small['worst_certificate_3']['actions']})==21
assert len({tuple(r['history']) for r in small['worst_certificate_4']['actions']})==85
for m in (3,4):
 actual=pop['results'][str(m)]['certificate_audit']['path']
 assert tuple(small[f'worst_certificate_{m}']['terminal_counts'])==tuple(actual.count(a) for a in range(4))
report['population_all_fields_equal_original_replay']=True
report['population_node_tables_consumed']=sum(len(v['all_ordered_node_tables']) for v in pop['results'].values())

# Both exact signed outputs include every weight and all 259 actions.
report['signed_original_replay_equal']={}
for n in ['signed_obstruction_exact.json','signed_obstruction_report.json']:
 a=(P/'tree'/n).read_bytes();b=(BASE/'replay/signed-obstruction'/n).read_bytes()
 assert a==b
 report['signed_original_replay_equal'][n]={'bytes':len(a),'sha256':hashlib.sha256(a).hexdigest()}
signed=json.loads((P/'tree/signed_obstruction_exact.json').read_text())
best=json.loads((P/'tree/signed_policy_n4_p6_b_best.json').read_text())
assert signed['strategy_actions']==best['strategy_actions']
exact={r['mask']:F(r['weight']) for r in signed['weights']}
for r in best['signed_customer_weights']:
 assert F(round(F(r['weight'])*85320),85320)==exact[r['mask']]
A={1,3,4,5};X={1,3,5}
atom=sum((w for B,w in exact.items() if {a for a in A if B>>a&1}==X),F(0))
assert atom==F(-13541,17064)
report['signed_smallest_atom']=str(atom)
report['signed_visible_cover_eight_values']={','.join(map(str,S)):str(sum((w for B,w in exact.items() if any(B>>a&1 for a in S)),F(0))) for S in [(4,),(1,4),(3,4),(4,5),(1,3,4),(1,4,5),(3,4,5),(1,3,4,5)]}

# All rows of both count-dependent certificates are consumed; no 45s MILP rerun.
report['count_joint']={}
for name in ['count_joint_selftest.json','count_joint_7_5_00112.json']:
 d=json.loads((P/'credible'/name).read_text());m=d['players'];p=d['topics'];pr=d['proof']
 rows=pr['strategy']['actions'];actions={tuple(r['history']):r['action'] for r in rows}
 expected={h for t in range(m) for h in product(range(p),repeat=t)}
 assert len(rows)==len(actions) and set(actions)==expected
 assert all(type(a) is int and 0<=a<p for a in actions.values())
 count_actions={}
 for h,a in actions.items():
  q=tuple(h.count(b) for b in range(p))
  assert q not in count_actions or count_actions[q]==a
  count_actions[q]=a
 h=()
 while len(h)<m:h=h+(actions[h],)
 assert list(h)==d['path']
 assert [h.count(a) for a in range(p)]==pr['strategy']['terminal_counts']
 clones=pr['integer_clones'];assert len(clones)==(1<<p)-1 and all(type(x) is int and x>=0 for x in clones)
 if p==7:
  assert clones==[0]*126+[1]
  assert pr['welfare']==pr['optimum']==1 and pr['ratio']=='1'
  assert pr['exact_dual_optimal'] is False and pr['dual_support']==[] and pr['dual_bound'] is None
 else:
  assert clones==[2,1,0]
  assert pr['ratio']=='3/2' and pr['dual_support']==[[0,'1']] and pr['dual_bound']=='3/2'
 report['count_joint'][name]={'ordered_actions_consumed':len(rows),'distinct_count_states':len(count_actions),'actual_path':h,'nonzero_clones':[{ 'mask':i+1,'count':x} for i,x in enumerate(clones) if x],'all_history_payoff_if_all_interest':str(F(1,m)) if p==7 else None}

# Parse every old packet scalar, counts/action/children/desired/terminal and metadata.
# The old mathematical SPE certification is explicitly reused, not rerun here.
packet=json.loads(gzip.decompress((P/'security/refined_tax_k10_packet.json.gz').read_bytes()))
node_schemas=Counter(tuple(sorted(n)) for n in packet['nodes'])
report['thirteen_packet']={'sha256':hashlib.sha256((P/'security/refined_tax_k10_packet.json.gz').read_bytes()).hexdigest(),'node_count':len(packet['nodes']),'node_field_schemas':[{ 'keys':list(k),'count':v} for k,v in node_schemas.items()],'depth_histogram':dict(sorted(Counter(sum(n['counts']) for n in packet['nodes']).items())),'distinct_count_vectors':len({tuple(n['counts']) for n in packet['nodes']}),'distinct_promised_counts':len({tuple(n['desired']) for n in packet['nodes'] if 'desired' in n}),'constructor_stats':packet['constructor_stats'],'fresh_IC_replay':False}
assert report['thirteen_packet']['sha256']=='bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce'

# Every finite exploration record, including all times, targets and roots, survives.
report['signed_searches']={}
for name in ['signed_policy_n3_p6_run.json','signed_policy_n4_p6_b_run.json','signed_policy_n5_p6_run.json']:
 d=json.loads((P/'tree'/name).read_text())
 assert all(set(x)=={'trial','value','target','root','elapsed'} for x in d)
 report['signed_searches'][name]={'records':len(d),'trials':[x['trial'] for x in d],'null_values':sum(x['value'] is None for x in d),'max_float_value':max(x['value'] for x in d if x['value'] is not None),'last_elapsed':d[-1]['elapsed'],'all_records':d}

# The exchangeable output has only floating LP optima. Compare to the displayed
# exact feasible orbit (1,1), never promote this to an exact optimum proof.
ex=json.loads((P/'background/exchangeable_probe.json').read_text())
report['exchangeable_records']=[]
for x in ex:
 m=x['m'];assert x['L']==m and len(x['all_values'])==m+1
 formula=[F(2*(m*m-r*(m-r)),m+1) for r in range(m+1)]
 assert max(abs(float(v)-w) for v,w in zip(formula,x['all_values']))<1e-10
 report['exchangeable_records'].append({'m':m,'saved_best_r':x['best']['r'],'exact_feasible_values_matching_floats':[str(v) for v in formula],'saved_best_support':x['best']['support'],'exact_LP_optimality_certified':False})
(BASE/'saved-field-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['files','signed_searches','exchangeable_records']},ensure_ascii=False,indent=2))
