"""Delivery and literal stored-report checks only: no Fraction, game, IC or permutation evaluation."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-optimal-prefix-bill-code-and-two-report-contracts-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=read(E/'actual-source-manifest.json')['rows'];ids={x['id'] for x in rows}
assert len(rows)==3 and sum(x['size'] for x in rows)==33708
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4'
assert len(claim['ids'])==13 and ids<=set(claim['ids'])
assert claim['remote_tip']=='d5e6cfc460bde7c98fbb655a27ceb0f884df4dd7' and claim['local_sync']['status']=='synced'
assert read(E/'actual-source-manifest.json')['raw_original_local_sync']==claim['local_sync']
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes()
 assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
 assert x['full_file_reviewed'] is True and x['new_normal_show'] is True
 d=read(E/'local-progress-at-read'/(x['id']+'.json'))
 assert d['owner']=='Boss4' and d['disposition']=='in-progress' and d['source_sha256']==x['sha256']
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name)
 assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')}
 assert cap['output']==x['local_path']
com=read(E/'formal-comparison.json');assert len(com)==8
for x in com:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed'] is True
 assert p.read_bytes()==Path(x['actual_read_from']).read_bytes()
rel=read(E/'related-MD-manifest.json');assert len(rel)==3 and sum(x['bytes'] for x in rel)==9116
for x in rel:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes()
 assert x['full_file_reviewed'] is True and x['new_primary'] is False and x['new_done'] is False
fixtures=read(E/'related-fixed-fixture-manifest.json');assert len(fixtures)==2 and sum(x['bytes'] for x in fixtures)==24196
prior={x['repository_path']:x for x in read(E/'previous-full-fixture-reading-manifest.json')}
for x in fixtures:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes()
 assert x['full_file_reviewed'] is True and x['exact_previous_full_reading_reused'] is True and x['new_done'] is False
 assert prior[x['repository_path']]['sha256']==x['sha256'] and prior[x['repository_path']]['full_file_reviewed'] is True
 sourcepath='/'.join(x['repository_path'].split('/')[5:])
 # The copied authoritative earlier source manifest is the metadata authority.
 assert any(y['sha256']==x['sha256'] and y['size']==x['bytes'] for y in read(E/'previous-fixed-input-source-manifest.json')['files'])
receipts=read(W/'semantic-receipts.json');assert len(receipts)==3 and {x['id'] for x in receipts}==ids
for x in receipts:
 assert x['disposition']=='retained' and all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
sc=read(E/'execution-and-domain-boundaries.json')
assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_SPE_replays','current_IC_replays','current_permutation_enumeration_runs','current_LP_runs','current_RNG_replays','current_solver_runs','new_mathematical_implementation_runs'))
assert sc['historical_execution_manifest_present'] is False and sc['all_report_fields_transcribed'] is True and not (E/'runs').exists()
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==9
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
page=math[0].read_text()
current=read(S/next(x['stage_path'] for x in rows if x['id']=='90a08a586d192ec52e96'))
old=read(S/next(x['stage_path'] for x in rows if x['id']=='f3342bd277affb050bf7'))
assert read(E/'stored-reports-literal-transcription.json')==dict(source_only=current,old_nine=old)
v=read(E/'report-version-comparison.json')
assert set(current)==set(v['current_code_return_keys']) and len(current)==10
assert current['compact_source_rule_matched'] is True and len(current['optimal_multisets'])==1
assert current['instance']=='examples/customer_attraction/prefix_balance_failure.json'
assert (current['m'],current['p'],current['actual'],current['W'],current['OPT'],current['nodes'],current['comparisons'])==(4,6,[1,2,2,2],14,22,259,1554)
assert len(old)==9 and all(len(x)==9 and 'compact_source_rule_matched' not in x for x in old)
assert sum(len(x['optimal_multisets']) for x in old)==25
common={'multiset','min','min_order','max','max_order','low_failure','fixed_multiset_up_failure'}
def groupcells(a):return [','.join(map(str,a['multiset'])),a['min'],','.join(map(str,a['min_order'])),a['max'],','.join(map(str,a['max_order'])),str(a['low_failure']).lower(),str(a['fixed_multiset_up_failure']).lower()]
a=current['optimal_multisets'][0];assert set(a)==common|{'all_orders'} and len(a['all_orders'])==24
assert '|'+'|'.join(groupcells(a))+'|' in page
for r in a['all_orders']:
 assert set(r)=={'order','D','forced_payoffs','forced_rollouts'}
 assert len(r['forced_payoffs'])==4 and len(r['forced_rollouts'])==4
 line='|'+'|'.join([','.join(map(str,r['order'])),r['D'],', '.join(r['forced_payoffs'])]+[','.join(map(str,z)) for z in r['forced_rollouts']])+'|'
 assert line in page,line
for i,r in enumerate(old):
 assert set(r)==set(v['current_code_return_keys'])-{'compact_source_rule_matched'}
 line=f"|{i}|{Path(r['instance']).stem}|{r['m']}|{r['p']}|{','.join(map(str,r['actual']))}|{r['W']}|{r['OPT']}|{r['nodes']}|{r['comparisons']}|"
 assert line in page,line
 for a in r['optimal_multisets']:
  assert set(a)==common
  assert '|'+'|'.join([str(i)]+groupcells(a))+'|' in page
prefix=next(x for x in old if x['instance'].endswith('/prefix_balance_failure.json'))
assert 'all_orders' not in prefix['optimal_multisets'][0]
assert v['observed_schema_difference'] is True and v['exact_code_version_or_processing_history_unknown'] is True
links=0
for p in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#',1)[0]).resolve()
  if not q.is_file():assert (R/str(q.relative_to(S))).is_file(),(str(p),target)
  links+=1
for x in read(E/'content-manifest.json'):
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
p=W/'copy-files.json'
if p.exists():assert read(p)==sorted(str(q.relative_to(S)) for q in S.rglob('*') if q.is_file())
result=dict(status='PASS',scope='source/hash/blob/normal metadata/owner/fullclaim, snapshot/fixture preservation, exact stored report fields and version absence, semantic receipts and links; no mathematical evaluation',primary_files=3,primary_bytes=33708,new_normal_show_files=3,retained=3,duplicate=0,formal_math_files=1,comparison_snapshots=8,related_MD_files=3,related_fixed_fixtures=2,old_report_cases=9,old_report_multiset_records=25,source_only_order_records=24,relations=9,source_state_updates=0,original_entry_runs=0,imports=0,SPE_replays=0,IC_replays=0,permutation_enumeration_runs=0,LP_runs=0,RNG_replays=0,solver_runs=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
