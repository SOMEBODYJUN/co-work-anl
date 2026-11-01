"""Frozen bytes, report-table roundtrip and provenance only; no DP replay."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-positive-depth-floor-direct-working-and-checks-four-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==4 and [x['size'] for x in rows]==[6238,2422,11581,1957] and sum(x['size'] for x in rows)==22198
for x in rows:
 checked(S/x['stage_path'],x);assert x['full_file_reviewed'] and len(x['sources'])==2
 o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim' and len(claim['ids'])==7 and {x['id'] for x in rows}<=set(claim['ids'])
assert claim['remote_tip']=='c8da98edfbe9483c455f65966a085fb5d9e233bd' and claim['local_sync']['status']=='synced'
models=read(E/'models-source-manifest.json');runtime=read(E/'runtime-source-manifest.json');assert len(models)==19 and sum(x['size'] for x in models)==30190 and len(runtime)==4 and sum(x['size'] for x in runtime)==25475
for x in models+runtime:checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and not x['new_primary'] and not x['new_done']
related_md=read(E/'related-MD-manifest.json');assert len(related_md)==1 and related_md[0]['id']=='5ae33455374f43989327' and related_md[0]['size']==4894
for x in related_md:checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and not x['new_primary'] and not x['new_done']
normal=read(E/'related-MD-acquisition/normal-show-run.json');assert normal['exit_code']==0 and normal['argv'][1:5]==['work.py','clean','show','5ae33455374f43989327']
view=read(E/'stored-field-check-and-reading/models-full-reading.json');assert len(view)==19
for x,v in zip(models,view):assert x['id']==v['source_id'] and x['path']==v['path'] and read(S/x['snapshot'])==v['data']
report=read(S/rows[2]['stage_path']);assert set(report)=={'candidate','scope','records'} and len(report['records'])==19
field=read(E/'stored-field-check-and-reading/stored-report-field-check.json');run=read(E/'stored-field-check-and-reading/field-check-run.json')
assert field['status']=='pass' and run['exit_code']==0 and field['report_sha256_before']==field['report_sha256_after']==rows[2]['sha256']
assert field['record_count']==19 and field['depth_values']==field['witness_vectors']==61 and field['witness_integer_slots']==329 and field['model_or_solver_imports']==field['threshold_calls']==field['IC_replays']==0
assert len(field['records'])==19 and all(x['stored_sum_consistent'] and x['stored_gap_consistent'] and x['witness_count_vectors_legal'] for x in field['records'])
assert run['script_sha256']==sha(E/'stored-field-check-and-reading/check_stored_report_fields.py') and read(E/'stored-field-check-and-reading/field-check.stdout')==field
cm=read(E/'formal-comparison.json');assert len(cm)==8;cmp_paths={x['path'] for x in cm}
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
rec=read(W/'semantic-receipts.json');assert len(rec)==4 and [x['disposition'] for x in rec]==['retained','retained','retained','duplicate'] and {x['id'] for x in rec}=={x['id'] for x in rows}
for x in rec:assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all((S/t).is_file() or (R/t).is_file() or t in cmp_paths for t in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==9
candidate=S/'archives/customer-attraction/state/候选/全部子局深度保底和的半覆盖充分候选--候选.md';resource=S/'archives/customer-attraction/state/资源/直接归属付款的同叶账与十九份深度报告--资源.md'
c=candidate.read_text();t=resource.read_text()
for term in ['DEPTH-ALL?','互不兼容的前缀','缓存的是','widehat','最小当前收益','theta_m','0原入口']:
 assert term in c,term
assert 'tag{PF?}' in c and '它不是原security分支PF?的准确原式' in c and '4894B' in c
for term in ['36>35','0/0','fixed','固定j主题','不能把这种关联','19行','61个向量','329','一次标准库存储字段核','没有CLI','main guard']:
 if term in ['fixed','没有CLI']:continue
 assert term in t,term
# Decode every visual table row back into the eight original JSON fields.
names={Path(x['input']).stem for x in report['records']};decoded=[]
for line in t.splitlines():
 if not line.startswith('|'):continue
 cells=[x.strip() for x in line.split('|')[1:-1]]
 if not cells or cells[0] not in names:continue
 name,mk,opt,L,total,gap,witness=cells;m,k=map(int,mk.split('/'))
 decoded.append(dict(input='examples/customer_attraction/'+name+'.json',players=m,topics=k,opt=int(opt),depth_floors=L.split(','),floor_sum=total,candidate_gap=gap,prefix_witnesses=[[int(d) for d in w] for w in witness.split(';')]))
assert decoded==report['records']
for doc in [candidate,resource,E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  q=(doc.parent/target).resolve();assert q.is_file() or (q.is_relative_to(S) and ((R/q.relative_to(S)).is_file() or str(q.relative_to(S)) in cmp_paths)),(doc,target)
ex=read(E/'execution-boundaries.json');assert ex['new_stored_field_arithmetic_runs']==1
for k in ['original_entry_runs','project_module_imports','solver_calls','threshold_calls','IC_replays','OPT_recomputations']:assert ex[k]==0
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result=dict(status='pass',scope='bytes/provenance/19-model JSON lossless view/full19report table eight-field roundtrip/exact sibling PF amount/receipts/links only; stored-arithmetic log reused, no DP',primary_files=4,primary_bytes=22198,related_models=19,model_bytes=30190,runtime_files=4,runtime_bytes=25475,related_MDs=1,related_MD_bytes=4894,formal_comparisons=8,new_formal_objects=2,retained=3,duplicate=1,relations=9,source_state_updates=[],raw_claim_local_sync='synced',report_records=19,depth_values=61,witness_vectors=61,witness_integer_slots=329,new_stored_field_arithmetic_runs=1,original_entry_runs=0,project_module_imports=0,solver_calls=0,threshold_calls=0,IC_replays=0,OPT_recomputations=0)
(W/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
