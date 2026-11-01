"""Byte/provenance and all saved-table fields only; no utility/IC/LP replay."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-fixed-policy-depth-floor-and-security-overlay-five-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==5 and [x['size'] for x in rows]==[4894,4131,3964,1596,5950] and sum(x['size'] for x in rows)==20535
for x in rows:
 checked(S/x['stage_path'],x);assert x['full_file_reviewed'] and len(x['sources'])==2
 o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
assert rows[0]['exact_prior_normal_show_reused'] and rows[0]['no_new_normal_show_for_this_source']
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim' and len(claim['ids'])==8 and {x['id'] for x in rows}<=set(claim['ids'])
assert claim['remote_tip']=='5af63eb11386c080a293d8ea43a7973603d874bb' and claim['local_sync']['status']=='needs-attention'
proof=read(E/'independent-sync-preservation.json');assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(x['same'] for x in proof['tracked']) and proof['missing']==proof['different']==[] and proof['unmerged']=='' and proof['stash_kept'] and proof['stash']=='1c5c9da6f58f76625ce2f43b65da43ce882d8836'
related=read(E/'actual-required-input-manifest.json');assert len(related)==27 and sum(x['size'] for x in related)==1436720
for x in related:checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and not x['new_primary'] and not x['new_done']
assert len([x for x in related if x['path'].startswith('examples/')])==20 and len([x for x in related if x['path'].startswith('evidence/')])==6
views=read(E/'prior-complete-reading-manifest.json');assert len(views)==6
for x in views:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
field=read(E/'stored-field-check/stored-field-check.json');run=read(E/'stored-field-check/field-check-run.json')
assert field['status']=='pass' and run['exit_code']==0 and run['script_sha256']==sha(E/'stored-field-check/check_saved_fields.py') and read(E/'stored-field-check/field-check.stdout')==field
assert field['report_sha256_before']==field['report_sha256_after'] and set(field['report_sha256_before'].values())=={rows[2]['sha256'],rows[4]['sha256']}
assert field['fixed_records']==6 and field['overlay_records']==19 and field['fixed_reported_histories']==11758 and field['fixed_reported_comparisons']==114992 and field['overlay_query_coordinates']==100
assert [x['input'] for x in field['overlay_checks'] if not x['query_exactly_normalized']]==['examples/customer_attraction/local_security_increment.json']
assert [x['input'] for x in field['overlay_checks'] if x['reported_float_gap_negative']]==['examples/customer_attraction/root_tax_failure.json','examples/customer_attraction/tax_bridge_failure.json']
cm=read(E/'formal-comparison.json');assert len(cm)==11;cmp_paths={x['path'] for x in cm}
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
receipts=read(W/'semantic-receipts.json');assert len(receipts)==5 and {x['id'] for x in receipts}=={x['id'] for x in rows} and all(x['disposition']=='retained' for x in receipts)
for x in receipts:assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all((S/t).is_file() or (R/t).is_file() or t in cmp_paths for t in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==12
candidate=S/'archives/customer-attraction/state/候选/固定完整策略全历史地板的强安全付款候选--候选.md';program=S/'archives/customer-attraction/state/程序/固定策略地板与全子局安全覆盖的原始双诊断--程序.md'
c=candidate.read_text();t=program.read_text();assert '@@' not in c+t
for term in ['tag{PF?}','OPT_m≤2ΣL_i','Jensen','调和势','647/8772','根收益≥v_m/2','OPT_m/(2m)','3Δ/2']:
 assert term in c,term
for term in ['泛用Q校验不完整','security_global','导入也会执行','0.045114352004020475','11758','114992','3452166800920648641549300488912419','没有计算query收益']:
 assert term in t,term
fixed=read(S/rows[2]['stage_path']);overlay=read(S/rows[4]['stage_path'])
def tuple_strings(s):
 assert s.startswith('(') and s.endswith(')');v=s[1:-1];return v.split(',') if v else []
def tuple_ints(s):return list(map(int,tuple_strings(s)))
names={x['instance'] for x in fixed};decoded=[];security=[];decoded_overlay=[];zone=0
for line in t.splitlines():
 if line.startswith('## 2.'):zone=2
 elif line.startswith('## 3.'):zone=3
 elif line.startswith('## 4.'):zone=4
 elif line.startswith('## 5.'):zone=5
 if not line.startswith('|'):continue
 a=[x.strip() for x in line.split('|')[1:-1]]
 if zone==2 and a[0] in names:
  if len(a)==10:
   name,m,k,H,C,L,h,total,root,u=a;decoded.append(dict(instance=name,positions=int(m),catalog=int(k),histories=int(H),comparisons=int(C),position_floors=tuple_strings(L),floor_witness_histories=[tuple_ints(v) for v in h.split('; ')],floor_sum=total,root=tuple_ints(root),root_utilities=tuple_strings(u)))
  elif len(a)==4:
   name,status,value,gap=a
   if status=='exact matched saved primal/dual':security.append(dict(instance=name,security_status=status,security_value=value,floor_security_gap=gap))
   else:
    assert status=='floating LP discovery only';security.append(dict(instance=name,security_status=status,security_value_discovery=json.loads(value),floor_security_gap_discovery=json.loads(gap)))
 if zone==4 and len(a)==5 and a[0] in {Path(x['input']).stem for x in overlay}:
  name,total,v,gap,q=a;decoded_overlay.append(dict(input='examples/customer_attraction/'+name+'.json',floor_sum=total,security_discovery=json.loads(v),floor_security_gap_discovery=json.loads(gap),query_candidate=tuple_strings(q)))
assert [dict(a,**b) for a,b in zip(decoded,security)]==fixed and len(decoded)==len(security)==6
assert decoded_overlay==overlay and len(decoded_overlay)==19
for doc in [candidate,program,E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  q=(doc.parent/target).resolve();assert q.is_file() or (q.is_relative_to(S) and ((R/q.relative_to(S)).is_file() or str(q.relative_to(S)) in cmp_paths)),(doc,target)
ex=read(E/'execution-boundaries.json');assert ex['new_stored_field_arithmetic_runs']==1
for k in ['original_entry_runs','original_module_imports','IC_replays','query_payoff_calls','static_matrix_evaluations','solver_or_LP_calls']:assert ex[k]==0
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result=dict(status='pass',scope='bytes/provenance/full6x13+19x5 saved field table roundtrip/related closure/prior fullreading hashes/receipts/links only; existing1 stored-field run reused, no utility/IC/LP',primary_files=5,primary_bytes=20535,related_files=27,related_bytes=1436720,model_files=20,certificate_files=6,prior_complete_policy_action_rows=11758,prior_complete_reading_views=6,formal_comparisons=11,new_formal_objects=2,retained=5,duplicate=0,relations=12,source_state_updates=[],raw_claim_local_sync='needs-attention',independent_sync_preservation='3 untracked+2 tracked same; stash kept; no25ZO restoration event',fixed_report_records=6,overlay_report_records=19,query_coordinates=100,one_query_not_exactly_normalized=True,two_original_tiny_negative_float_gaps_preserved=True,new_stored_field_arithmetic_runs=1,original_entry_runs=0,original_module_imports=0,IC_replays=0,static_query_payoff_evaluations=0,LP_calls=0)
(W/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
