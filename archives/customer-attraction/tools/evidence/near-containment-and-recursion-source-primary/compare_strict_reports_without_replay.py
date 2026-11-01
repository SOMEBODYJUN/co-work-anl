"""Passive comparison of two already computed exact data sets; no game utilities recalculated."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
E=Path(__file__).resolve().parent;OUT=E/'strict-frozen-and-JB-comparison.json';assert not OUT.exists()
orig=E/'original-programs/research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/global/audit_strict_static_gap.json';prior=E/'reused-JB-exact/archives/customer-attraction/tools/evidence/global-customer-cone-and-background-circuit-primary/new-coupling-and-strict-policy.json';a=json.loads(orig.read_text());b=json.loads(prior.read_text());records=[]
for old,new in [('base','strict_twelve_clients'),('all_types_positive_M100','strict_full_support_1215_clients')]:
 x,y=a[old],b[new];assert x['actual']==y['root_leaf'] and x['utilities']==y['root_utilities'] and str(x['W'])==y['root_coverage'] and str(x['OPT3'])==y['actual_catalog_OPT'];assert x['minimum_nonself_SPE_margin']==y['minimum_nonself_slack'];n=0
 for r in y['policy_rows']:
  tag=''.join('ABCD'[i] for i in r['history']) or 'root';values=list(map(F,x['actual_node_payoff_tables'][tag]));assert values[r['chosen']]-values[r['alternative']]==F(r['slack']);n+=1
 assert n==84 and len(x['actual_node_payoff_tables'])==21
 assert {tuple(z['terminal']) for z in x['static_PNE']}=={tuple(z) for z in y['static_pne_profiles']}
 neg=[-F(g) for z in y['static_profiles'] if z['is_PNE'] for g in z['all_action_gains_including_self'] if F(g)<0];best=[max(map(F,z['all_action_gains_including_self'])) for z in y['static_profiles'] if not z['is_PNE']];assert str(min(neg))==x['minimum_static_PNE_strict_margin'] and str(min(best))==x['minimum_best_profitable_static_deviation_for_nonPNE']
 records.append({'frozen_case':old,'JB_case':new,'table_comparison_differences_equal':n,'nodes':21,'root_absolute_utilities_equal':True,'all_static_PNE_profiles_equal':True,'three_minimum_margin_fields_equal':True})
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
res={'status':'passed','frozen_report_sha256':sha(orig),'prior_JB_output_sha256':sha(prior),'cases':records,'original_strict_CLI_new_runs':0,'prior_JB_entry_reruns':0,'new_game_utility_computations':0,'scope':'Passive equality of existing root values/PNE profiles/minimum margins and all 168 action comparison differences from frozen21node tables. Does not recalculate every offpath absolute payoff from customers.'};OUT.write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'passed','existing_comparison_differences':168,'original_strict_runs':0,'JB_reruns':0}))
