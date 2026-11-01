"""Delivery and saved-audit verification only. Never rerun the stored Fraction audit or an old checker."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-parent-amount-full-report-and-workspace-tail-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
man=read(E/'actual-source-manifest.json');rows=man['rows'];ids={x['id'] for x in rows}
assert len(rows)==3 and sum(x['size'] for x in rows)==37074
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4'
assert len(claim['ids'])==5 and ids<=set(claim['ids']) and claim['local_sync']['status']=='synced'
assert claim['remote_tip']=='223e1c5bb8fa9c58bd8ca5f9a0d15e4ec78b5b89'
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'] and x['full_file_reviewed'] is True
 d=read(E/'local-progress-at-read'/(x['id']+'.json'));assert d['owner']=='Boss4' and d['source_sha256']==x['sha256']
 assert (E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name).is_file()
old=read(E/'existing-related-code-manifest.json');p=S/old['snapshot']
assert old['id']=='006b849e820f86c1231f' and old['size']==4626 and p.stat().st_size==4626 and sha(p)==old['sha256']
assert old['full_file_reviewed'] is True and old['id'] not in ids
comp=read(E/'formal-comparison.json');assert len(comp)==5;available={x['path'] for x in comp}
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed'] is True
record=read(E/'stored-report-audit/execution.json')
assert record['exit_code']==0 and record['elapsed_seconds']==0.04012272399995709
assert record['original_report_unchanged'] and record['audit_script_unchanged']
assert record['before']==record['after'] and record['argv'][1:3]==['-I','-B'] and record['cwd']==str(S)
assert len(record['argv'])==6 and record['argv'][3]==str(E/'audit_stored_report_fields.py')
for k in ('original_report','audit_script'):
 x=record['after'][k];p=Path(x['path']);assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
for k in ('stdout','stderr','output'):
 x=record[k];p=Path(x['path']);assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
assert record['stderr']['bytes']==0 and record['stdout']['sha256']==record['output']['sha256']
result=read(E/'stored-report-audit/stored-fields-result.json')
assert result['status']=='PASS' and result['input_sha256']=='a1e42893824868705e64e52150f726127258ca1e80987b1e20fa00f4547b8a45'
assert sha(E/'stored-report-audit/stored-fields-result.json')=='5f2401cc306a9802d4d79730b1af889b39a7a51fb14b266e01a4d197996cd97a'
assert (result['reports'],result['columns'],result['stored_sender_rows'])==(16,50,46)
assert (result['positive_columns'],result['zero_columns'],result['lambda_gt_one_stored_rows'])==(27,23,8)
assert result['max_reported_column_ratio']=='2/3' and result['all_report_flags_false'] is True
assert (result['sum_reported_histories_not_replayed'],result['sum_reported_comparisons_not_replayed'])==(12169,117478)
assert result['arithmetic_checks']=={'budget_equalities':46,'output_products':46,'column_totals':50,'column_ratios':50,'report_flags':16}
assert all(result[k]==0 for k in ('original_checker_entry_runs','original_checker_imports','SPE_or_IC_replays','solver_or_LP_runs'))
report=read(S/next(x['stage_path'] for x in rows if x['id']=='34c68a75254ba1675fc7'))
txt=(S/'archives/customer-attraction/state/程序/父金额容量十六证书报告的逐字段合同--程序.md').read_text()
fmt=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'))
for i,o in enumerate(report['reports']):
 line='| '+str(i)+' | '+Path(o['source']).stem+' | '+fmt(o['path'])+' | '+fmt(o['profits'])+' | '+str(o['verified_histories'])+' / '+str(o['verified_comparisons'])+' | '+fmt([x['total_positive'] for x in o['columns']])+' | '+fmt([x['column_ratio'] for x in o['columns']])+' | '+str(o['violates_cap2']).lower()+' |'
 assert line in txt
 for col in o['columns']:
  for z in col['rows']:
   line='| '+' | '.join([str(i),str(col['recipient_zero_based']),str(z['sender_zero_based']),str(z['cut_zero_based']),str(z['forced']),fmt(z['leaf']),z['profit_B'],z['profit_W'],z['q_positive'],z['lambda'],z['output']])+' |'
   assert line in txt
rr=read(W/'semantic-receipts.json');assert len(rr)==3 and {x['id'] for x in rr}==ids
assert sum(x['disposition']=='retained' for x in rr)==1 and sum(x['disposition']=='duplicate' for x in rr)==2
for x in rr:
 assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() or t in available for t in x['targets'])
scope=read(E/'execution-and-domain-boundaries.json')
assert scope['new_stored_report_arithmetic_audit_runs']==scope['new_mathematical_program_runs']==1
assert all(scope[k]==0 for k in ('old_checker_entry_runs','old_checker_imports','current_SPE_or_IC_replays','current_solver_or_LP_runs','current_RNG_or_parameter_scans','new_game_or_strategy_implementation_runs'))
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==5
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
links=0
for p in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#',1)[0]).resolve()
  if not q.is_file():
   rel=str(q.relative_to(S));assert (R/rel).is_file() or rel in available,(str(p),target)
  links+=1
for x in read(E/'content-manifest.json'):
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
p=W/'copy-files.json'
if p.exists():assert read(p)==sorted(str(q.relative_to(S)) for q in S.rglob('*') if q.is_file())
out={'status':'PASS','scope':'source/raw full claim/owner, saved authorized audit execution+outputs, complete record transcription, snapshots/receipts/links only; stored arithmetic audit not rerun','primary_files':3,'primary_bytes':37074,'receipts':3,'retained':1,'duplicate':2,'formal_math_files':1,'comparison_snapshots':5,'relations':5,'source_state_updates':0,'new_stored_report_arithmetic_audit_runs':1,'old_checker_entry_runs':0,'old_checker_imports':0,'SPE_or_IC_replays':0,'solver_or_LP_runs':0,'RNG_or_parameter_scans':0,'full_reports_transcribed':16,'full_columns_transcribed':50,'full_sender_rows_transcribed':46,'links_checked':links}
(W/'self-check-result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
