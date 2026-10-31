"""Additional data-only root7 check + interpretation of original observed tests; no original imports/reruns."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json
E=Path(__file__).resolve().parent;D=json.loads((E/'dependency-manifest.json').read_text());tax=json.loads((E/'replay/tree-tax/passive-observation.json').read_text());pi=json.loads((E/'replay/pi-review/passive-observation.json').read_text());M=json.loads((E/'source-manifest.json').read_text())
def readid(i):return json.loads((E/'dependencies'/next(x['path']for x in D if x['id']==i)).read_text())
ins=readid('0ebc828733fab492d2a5');cert=readid('2cd505cd05ed8ab77f21');actions={tuple(x['history']):x['action']for x in cert['actions']};clients=[set(x['topics'])for x in ins['customers']for _ in range(x['multiplicity'])];assert ins['players']==4 and len(ins['topics'])==7 and len(clients)==53 and len(cert['actions'])==len(actions)==400 and set(actions)=={h for d in range(4)for h in product(range(7),repeat=d)}
def finish(h):
 while len(h)<4:h=h+(actions[h],)
 return h
def pay(z,i):return sum((F(1,sum(a in x for a in z))for x in clients if z[i]in x),F())
rootleaves=[finish((a,))for a in range(7)];rootprofits=[pay(z,0)for z in rootleaves];assert rootprofits==[F(29,3)]*6+[F(19)]and actions[()]==6
rootgaps=[rootprofits[6]-v for v in rootprofits];assert min(rootgaps)==0
assert all(list(rootleaves[x['root_action']])==x['leaf']for x in tax['forced_root_leaves'])and len(tax['forced_root_leaves'])==42
actual=rootleaves[6];assert [actual.count(a)for a in range(7)]==cert['terminal_counts'];actualu=list(map(str,[pay(actual,i)for i in range(4)]));coverage=sum(any(a in x for a in actual)for x in clients);witness=(2,4,5,6);assert coverage==51 and all(any(a in x for a in witness)for x in clients)
ns={(x['core'],x['lambda'],tuple(x['history'])):x for x in tax['unique_node_records']};ps={(x['core'],x['lambda'],tuple(x['history'])):x for x in tax['unique_prescribed_path_records']};assert len(ns)==len(ps)==2394
rows=[]
for core in [0,7]:
 for lam in ['1/2','3/4','84796/85443']:
  nodes=[x for x in tax['unique_node_records']if x['core']==core and x['lambda']==lam];paths=[x for x in tax['unique_prescribed_path_records']if x['core']==core and x['lambda']==lam];assert len(nodes)==len(paths)==399
  assert all(F(x['regret'])<=F(x['current_tax'])and F(x['regret'])==max(map(F,x['candidate_nonnegative_regrets']))for x in nodes)
  assert all(0<=F(x['path_regret'])<=F(x['noncore_future_tax'])<=F(x['future_tax'])<=F(x['full_tax'])and F(x['refund_minus_path_regret'])==F(x['full_tax'])-F(x['path_regret'])and 0<=F(x['HJ'])<=F(x['H'])and F(x['full_tax'])<=F(x['H'])for x in paths)
  match=next(x for x in tax['source_original_report']['rows']if x['core']==core and x['lambda']==lam);assert sum(F(x['regret'])>0 for x in nodes)==match['strict_regret_nodes']and max(F(x['regret'])for x in nodes)==F(match['maximum_local_regret'])and max(F(x['refund_minus_path_regret'])for x in paths)==F(match['maximum_refund_minus_prescribed_path_regret'])
  rows.append({'core':core,'lambda':lam,'unit_customers':53+core,'original_tail_nodes':399,'original_tail_action_assertions':2793,'positive_regret_nodes':match['strict_regret_nodes'],'max_local_regret':match['maximum_local_regret'],'min_refund_minus_path_regret':str(min(F(x['refund_minus_path_regret'])for x in paths)),'max_refund_minus_path_regret':match['maximum_refund_minus_prescribed_path_regret'],'min_noncore_future_tax_minus_path_regret':str(min(F(x['noncore_future_tax'])-F(x['path_regret'])for x in paths)),'min_H_minus_HJ':str(min(F(x['H'])-F(x['HJ'])for x in paths)),'min_H_minus_refund':str(min(F(x['H'])-F(x['full_tax'])for x in paths))})
core_equal=[]
for lam in ['1/2','3/4','84796/85443']:
 k=F(7)*(1-F(lam))/(4*(1+3*F(lam)))
 for h in [tuple(x['history'])for x in tax['unique_node_records']if x['core']==0 and x['lambda']==lam]:
  a=ns[0,lam,h];b=ns[7,lam,h];p=ps[0,lam,h];q=ps[7,lam,h];assert a['leaf']==b['leaf']and a['regret']==b['regret']and a['candidate_nonnegative_regrets']==b['candidate_nonnegative_regrets']and F(b['current_tax'])-F(a['current_tax'])==k and F(q['future_tax'])-F(p['future_tax'])==(4-len(h))*k and F(q['full_tax'])-F(p['full_tax'])==3*k
 core_equal.append({'lambda':lam,'tail_core_tax_per_role':str(k),'full_refund_increase':str(3*k),'regret_vectors_identical_at_all399_nodes':True,'source_count_of_nonzero_core_scenario_nodes':399})
# Only group existing original report data; no recomputation of PI utility or potentials.
report=json.loads((E/'original'/next(x['path']for x in M if x['id']=='7a790f8a0eac4c54cd9a')).read_text());buckets=[]
for slots,table in report['potential_tables'].items():
 grouped={}
 for row in table:
  q=row['counts'];key=(tuple(sorted([q[0],q[3]],reverse=True)),tuple(sorted([q[i]for i in [1,2,4,5]],reverse=True)))
  if key in grouped:assert grouped[key]['potential']==row['potential']and grouped[key]['coverage']==row['coverage'];grouped[key]['profiles']+=1
  else:grouped[key]={'potential':row['potential'],'coverage':row['coverage'],'profiles':1}
 for (center,leaf),g in sorted(grouped.items(),reverse=True):buckets.append({'slots':int(slots),'sorted_centers':list(center),'sorted_leaves':list(leaf),**g})
assert len(buckets)==26 and pi['main_calls']==1 and pi['source_packet_subscript_fields']==['instance','strategy']
stdout=(E/'replay/pi-review/stdout.txt').read_bytes();expected=(json.dumps({k:v for k,v in report.items()if k!='potential_tables'},ensure_ascii=False,indent=2)+'\n').encode();assert stdout==expected
security=json.loads(next((E/'related-original').rglob('endogenous_53_security.json')).read_text());assert F(29,3)/F(security['value'])==F(84796,85443)
out={'scope':'additional53-unit root7 comparisons only, plus arithmetic/grouping of original passive observations/report; no original, LP or SPE-oracle call','root_complement':{'comparison_count_including_self':7,'new_full_tree_scan':False,'was_not_checked_by_original_tax_entry':True,'source_complete_key_count':400,'root_action':6,'root_leaves':[list(z)for z in rootleaves],'root_payoffs':list(map(str,rootprofits)),'root_IC_gaps':list(map(str,rootgaps)),'actual':list(actual),'actual_unit_payoffs':actualu,'actual_W53':coverage,'OPT53_coverage_witness':list(witness),'OPT53':53,'actual_W60':58,'OPT60':60,'constructor_not_executed':True},'tax_original_scope':{'parameter_rows':rows,'tail_action_assertions_per_row':2793,'actual_tail_IC_assertions_six_rows':16758,'unique_nonempty_histories':399,'empty_root_assertions_in_original':0,'extra_original_calls':0,'raw_passive_events':tax['raw_observed_line_events']},'core_credit_check':core_equal,'pi_original_scope':{'main_calls':pi['main_calls'],'packet_fields_used':pi['source_packet_subscript_fields'],'IC_checks':len(pi['exact_IC_gaps']),'static_profile_rows':182,'source_stdout4132_equals_non_table_summary':True,'coverage_potential_orbits':buckets},'endogenous_lambda_provenance':{'reported_static_t':security['value'],'forced_old_topic_root_payoff':'29/3','literal_ratio':'84796/85443','actual_root_P_payoff':'19','static_security_optimality_not_reverified':True,'security_file_not_read_by_original_tax':True},'new_original_calls':0,'new_LP_calls':0,'new_solver_calls':0}
(E/'root-complement-and-scope-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'root_comparisons':7,'root_payoffs':out['root_complement']['root_payoffs'],'tax_rows':rows,'core_equal':core_equal,'pi_buckets':len(buckets),'new_original_calls':0},ensure_ascii=False))
