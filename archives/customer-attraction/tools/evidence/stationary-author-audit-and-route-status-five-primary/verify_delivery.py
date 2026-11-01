"""Only provenance/bytes/eighteen-field table and saved shared literals/links; no math replay."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-stationary-author-audit-and-route-status-five-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==5 and [x['size'] for x in rows]==[3586,1031,2008,1856,2043] and sum(x['size'] for x in rows)==10524
for x in rows:
 check(S/x['stage_path'],x);assert x['full_file_reviewed'] and len(x['sources'])==2
 p=read(E/'local-progress-at-read'/(x['id']+'.json'));assert p['owner']=='Boss4' and p['disposition']=='in-progress' and p['source_sha256']==x['sha256']
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim' and len(claim['ids'])==16 and {x['id'] for x in rows}<=set(claim['ids']) and claim['remote_tip']=='6de60d42591d29316d08e963bb70de4730fa0998' and claim['local_sync']['status']=='synced'
related=read(E/'related-source-manifest.json');assert len(related)==3 and sum(x['size'] for x in related)==1459171
for x in related:check(S/x['snapshot'],x);assert not x['new_primary'] and not x['new_done']
dag=next(x for x in related if 'pure_menu_two_block_dag' in x['path']);assert dag['prior_full_DAG_verification_reused'] and not dag['full_literal_DAG_read_current']
oldreport=next(x for x in related if x['id']=='8ea28e38a64787bd83d3');oldcode=next(x for x in related if x['id']=='5b9cbb2aed181ff8e8bf');run=read(E/'prior-sufficient-audit/execution.json');assert run['returncode']==0 and run['source_invocations']==1 and run['output']['sha256']==oldreport['sha256']
assert run['source_inputs'][0]['sha256_before']==run['source_inputs'][0]['sha256_after']==dag['sha256'] and run['source_inputs'][1]['sha256_before']==run['source_inputs'][1]['sha256_after']==oldcode['sha256']
for fn,key in [('stdout.txt','stdout'),('stderr.txt','stderr')]:assert sha(E/'prior-sufficient-audit'/fn)==run[key]['sha256'] and (E/'prior-sufficient-audit'/fn).stat().st_size==run[key]['bytes']
cm=read(E/'formal-comparison.json');assert len(cm)==11;cmp_paths={x['path'] for x in cm}
for x in cm:assert sha(S/x['snapshot'])==x['sha256'] and (S/x['snapshot']).stat().st_size==x['bytes'] and x['full_file_reviewed']
rec=read(W/'semantic-receipts.json');assert len(rec)==5 and [x['disposition'] for x in rec]==['retained','retained','duplicate','duplicate','retained']
for x in rec:assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all((S/p).is_file() or (R/p).is_file() or p in cmp_paths for p in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==11
program=S/'archives/customer-attraction/state/程序/八人平稳来源作者原审计的目标自洽与十八字段合同--程序.md';resource=S/'archives/customer-attraction/state/资源/平稳来源审计的分层证据与静态路线撤回--资源.md';t=program.read_text();r=resource.read_text();assert '@@' not in t+r
report=read(S/rows[1]['stage_path']);assert len(report)==18;decoded={}
for line in t.splitlines():
 if not line.startswith('|'):continue
 a=[x.strip() for x in line.split('|')[1:-1]]
 if len(a)==2 and a[0] in report:decoded[a[0]]=json.loads(a[1])
assert decoded==report
old=read(S/oldreport['snapshot'])
mapping={'source':'source','customers':'unit_clients','players':'players','dag_nodes':'reachable_DAG_nodes','all_ordered_decision_histories':'expanded_ordered_decision_histories','local_comparisons':'comparisons_including_self','minimum_IC_slack':'minimum_SPE_slack','root_u':'root_utility','Q':'unique_stationary_Q','query':'stationary_queries','cap':'stationary_cap','cap_minus_u':'stationary_gap','free_Q':'free_Q','free_query':'free_queries','free_cap':'free_menu_value'}
assert all(report[a]==old[b] for a,b in mapping.items()) and report['topics']==len(old['topics'])
assert 'target逐边不变' in t and '未给自由菜单的匹配行对偶' in t and '十八字段' in t
for word in ['tag{FQ}','tag{AMP}','KKT','撤回的是M≤v_m','不是新发现','FF-LEADER','635','4095','343']:
 assert word in r,word
for doc in [program,resource]:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  p=(doc.parent/target).resolve();assert p.is_file() or (p.is_relative_to(S) and ((R/p.relative_to(S)).is_file() or str(p.relative_to(S)) in cmp_paths)),(doc,target)
ex=read(E/'execution-boundaries.json');assert ex['raw_claim_local_sync']=='synced' and not ex['old_stash_event_inherited']
for k in ['original_entry_runs','module_imports','IC_replays','DAG_node_scans','LP_or_SPE_calls','query_or_matrix_evaluations','new_scientific_runs']:assert ex[k]==0
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
out=dict(status='pass',scope='provenance/byte+blob hashes/full18report table roundtrip and15 shared fields literal equality to old39field audit/topic count/receipts/links only; no utility/IC/DAG or matrix replay',primary_files=5,primary_bytes=10524,retained=3,duplicate=2,new_formal_objects=2,related_files=3,related_bytes=1459171,formal_comparisons=11,relations=11,report_fields=18,source_state_updates=[],raw_claim_local_sync='synced',prior_sufficient_same_SHA_independent_audit_runs_reused=1,new_original_entry_runs=0,new_IC_or_DAG_scans=0,new_LP_or_SPE_calls=0,new_query_or_matrix_runs=0,new_scientific_runs=0)
(W/'selfcheck-result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
