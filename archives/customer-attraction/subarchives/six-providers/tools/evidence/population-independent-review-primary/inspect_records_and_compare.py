"""Structural/source comparison only. No solver, utility, SPE/IC or audit run."""
from pathlib import Path
from itertools import product
import json,hashlib
P=Path(__file__).resolve().parent
new=json.loads((P/'original/population_audit.json').read_text())
old=json.loads((P/'comparison/population_paradox_audit.json').read_text())
assert set(new)=={'status','main_half_coverage_status','method','records','boundary_checks'}
assert new['status']=='independently_verified'
assert new['main_half_coverage_status']=='unchanged OPEN; not a target counterexample'
assert new['method']=='all ordered histories, Cartesian child menus, explicit unit clients, Fraction'
assert new['boundary_checks']=={'double_scale':True,'zero_clients':True}
label=lambda h:''.join('ABC'[a] for a in h)
compact=[];comparison=[];allhist=0;allcomp=0
for m,r in enumerate(new['records'],1):
 assert set(r)=={'players','scale','unit_clients','attainable_ordered_paths','decision_histories_per_certificate','all_action_comparisons','certificates','tables'}
 assert r['players']==m and r['scale']==1 and r['unit_clients']==12
 histories={h for d in range(m) for h in product(range(3),repeat=d)}
 assert len(histories)==r['decision_histories_per_certificate']
 assert [c['terminal'] for c in r['certificates']]==r['attainable_ordered_paths']
 counts=r['all_action_comparisons'];assert counts==len(r['certificates'])*len(histories)*3
 cs=[];non_markov=[]
 for j,c in enumerate(r['certificates']):
  assert set(c)=={'terminal','payoffs','welfare','minimum_spe_slack','actions'}
  assert c['minimum_spe_slack']=='0' and len(c['terminal'])==len(c['payoffs'])==m
  assert len(c['actions'])==len(histories)
  actions={tuple(v['history']):v['action'] for v in c['actions']}
  assert len(actions)==len(c['actions']) and set(actions)==histories
  assert all(set(v)=={'history','action'} and v['action'] in range(3) for v in c['actions'])
  grouped={}
  for h,a in actions.items():grouped.setdefault(tuple(h.count(k) for k in range(3)),set()).add(a)
  conflicts=[{'counts':q,'actions':sorted(a)} for q,a in grouped.items() if len(a)>1]
  if conflicts:non_markov.append({'certificate':j,'terminal':label(c['terminal']),'conflicts':conflicts})
  cs.append({**{k:v for k,v in c.items() if k!='actions'},'complete_actions':[[label(v['history']),v['action']] for v in c['actions']]})
  allhist+=len(actions)
 for t in r['tables']:
  assert set(t)=={'depth','rows'} and t['depth'] in range(m)
  assert all(set(v)=={'prefix_counts','attainable_terminal_counts'} for v in t['rows'])
 o=old['players'][str(m)]
 assert list(map(label,r['attainable_ordered_paths']))==o['all_ordered_spe_paths']
 assert sorted({c['welfare'] for c in r['certificates']})==o['welfare_set']
 assert r['certificates'][0]['payoffs']==o['selected_payoffs']
 assert {label(v['history']):'ABC'[v['action']] for v in r['certificates'][0]['actions']}==o['selected_strategy']
 compact.append({**{k:v for k,v in r.items() if k!='certificates'},'certificates':cs})
 comparison.append({'players':m,'paths_welfare_first_payoffs_and_first_complete_strategy_match_old':True,'certificate_count':len(cs),'actions_per_certificate':len(histories),'all_action_comparisons_as_recorded':counts,'self_comparisons_as_count_identity':len(cs)*len(histories),'nonself_comparisons_as_count_identity':2*len(cs)*len(histories),'stored_non_count_Markov_certificates':non_markov})
 allcomp+=counts
result={'status':'PASS_STRUCTURAL_AND_EXISTING_SOURCE_COMPARISON','original_audit_entries_executed':0,'new_utility_IC_or_SPE_enumeration_executions':0,'complete_source_field_read':{'root':{k:v for k,v in new.items() if k!='records'},'records':compact},'comparison':comparison,'totals':{'stored_certificates':sum(len(r['certificates']) for r in new['records']),'stored_action_entries':allhist,'stored_all_action_comparisons':allcomp,'self_comparisons_identity':allhist,'nonself_comparisons_identity':allcomp-allhist},'scope_difference':{'independent_source':[1,2,3,4],'old_source':[1,2,3,4,5],'new_scale_and_zero_clients_outputs':'only boolean summaries retained; no scale2 or zero certificates in the original JSON','old_boundary_regressions':old['boundary_regressions']},'source_sha256':{name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ['original/population_audit.json','original/population_audit.py','original/population_review.md','comparison/population_paradox_audit.json','comparison/population_paradox_audit.py']}}
print(json.dumps(result,ensure_ascii=False,indent=2))
