from pathlib import Path
from fractions import Fraction as F
import json,hashlib,ast,re
S=Path(__file__).resolve().parent;B=S.parent;R=B/'co-work-anl-boss3';D=B/'independent_cones_deliverables'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ss=json.loads((S/'source-manifest.json').read_text())
for x in ss:
 p=S/'original'/Path(x['path']).name;assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
for x in json.loads((S/'runtime-dependency-manifest.json').read_text()):
 p=S/'runtime-inputs'/x['path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
for x in json.loads((S/'related-manifest.json').read_text()):
 p=S/x['path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
for p in S.rglob('*.py'):ast.parse(p.read_text())
for p in S.rglob('*.json'):json.loads(p.read_text())
sem=json.loads((S/'source-and-report-semantics.json').read_text())
assert len(sem['reports'])==3 and sem['reported_rounds_sum']==280
assert all(x['fields_missing_from_current_final_schema']==['payoff_coefficient'] and not x['payoff_mode_bound'] for x in sem['reports'])
summary=json.loads((S/'replay/fixed-certificate-check.json').read_text())
assert summary['source_cone_calls']==1 and summary['reference_cone_calls']==1 and summary['histories']==31 and summary['nonself_deviations']==124
assert all(summary[k]==0 for k in ('ExactSPESolver_calls','attack_calls','original_CLI_calls','random_draws','LP_calls'))
assert summary['all_cone_rows_equal_negative_reference'] and summary['distinct_nonzero_cone_rows']==80 and summary['assertions_enabled']
ins=json.loads((S/'runtime-inputs/examples/customer_attraction/coverage_opportunity_failure.json').read_text())
weights=[sum(c['multiplicity']for c in ins['customers']if sum(1<<a for a in c['topics'])==mask)for mask in range(1,32)]
rows=json.loads((S/'replay/full-cone-row-comparison.json').read_text());assert rows['type_masks']==list(range(1,32)) and len(rows['all_rows'])==80
for row in rows['all_rows']:
 v=list(map(F,row['deviation_minus_chosen_coefficients']));assert len(v)==31
 q=sum((a*b for a,b in zip(v,weights)),F());assert q==F(row['exact_slack_le_zero_at_fixed_input']) and q<=0
obj=json.loads((S/'replay/all-fixed-input-objective-comparisons.json').read_text());assert len(obj)==40
assert min(F(x['exact_slack_at_fixed_input'])for x in obj if x['coefficient']==3)==F(9,2)
assert min(F(x['exact_slack_at_fixed_input'])for x in obj if x['coefficient']==2)==2
formal=D/'formal-object.md';body=formal.read_text();assert all(line.count('$')%2==0 for line in body.splitlines()) and body.count('\\[')==body.count('\\]')
fr=Path('archives/customer-attraction/state/程序/逐人覆盖缺口的随机完整锥攻击与三旧零哨兵报告--程序.md');ep=R/'archives/customer-attraction/tools/evidence/independent-cones-four-boss3';links=0
for x in re.finditer(r'\]\(([^)]+)\)',body):
 href=x.group(1)
 if '://' in href or href.startswith('#'):continue
 p=(R/fr.parent/href.split('#')[0]).resolve()
 if p.is_relative_to(ep):p=S/p.relative_to(ep)
 assert p.exists(),str(p);links+=1
receipts=json.loads((D/'receipts-20261101-independent-cones-four.json').read_text())
assert {x['id'] for x in receipts}=={x['id']for x in ss} and all(x['disposition']=='integrated'for x in receipts)
assert not any(S.rglob('__pycache__'))
out={'status':'all staged hashes/complete-report-fields/receipts/finite-coefficients/links passed','primary_sources':4,'old_reports':3,'old_report_mode_and_version_gaps_retained':True,'reported_rounds_not_replayed':280,'new_fixed_cone_function_events':1,'new_random_draws':0,'new_attack_calls':0,'new_original_CLI_calls':0,'new_LP_calls':0,'fixed_history_nodes':31,'fixed_nonself_deviations':124,'all_cone_rows':80,'type_columns_per_row':31,'fixed_objective_comparisons':40,'formal_links_checked':links,'math_delimiters_balanced':True,'stage_only':True}
(S/'package-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
