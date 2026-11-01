"""Frozen bytes, full JSON-view roundtrip, literal fields, and provenance only."""
from pathlib import Path
import json,hashlib,re,copy
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-disjoint-reservation-literal-audit-four-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==4 and [x['size'] for x in rows]==[6384,962,43455,8468] and sum(x['size'] for x in rows)==59269
for x in rows:
 checked(S/x['stage_path'],x);assert x['full_file_reviewed'] and len(x['sources'])==2
 o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
assert rows[3]['exact_prior_normal_show_reused'] and rows[3]['no_new_normal_show_for_this_source']
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim' and len(claim['ids'])==25 and {x['id'] for x in rows}<=set(claim['ids'])
assert claim['remote_tip']=='60de7e55e68b1baace6ae3c4e5ee1743cd82d52f' and claim['local_sync']['status']=='needs-attention'
proof=read(E/'claim-sync-preservation.json');initial=read(E/'sync-preservation-process/initial-sync-preservation.json');restoration=read(E/'claim-tracked-restoration.json')
assert proof['untracked_count']==1 and len(proof['tracked'])==284 and all(x['same'] for x in proof['tracked']) and proof['missing']==proof['different']==[] and not proof['unmerged'] and proof['stash_kept']
assert proof['stash']=='6e6bae58637cd22107d85dc3d1c8c7169281c556' and initial['stash']==proof['stash'] and len(initial['tracked'])==284 and sum(bool(x['same']) for x in initial['tracked'])==281
assert restoration['raw_sync_status']=='needs-attention' and restoration['stash_kept'] and len(restoration['restored_tracked_local_drafts'])==3
for x in restoration['restored_tracked_local_drafts']:
 assert sha(E/'sync-preservation-process'/Path(x['stash_before']).name)==x['stash_sha256']==x['restored_sha256']
 assert sha(E/'sync-preservation-process'/Path(x['live_before_restore']).name)==x['live_before_restore_sha256']
process=read(E/'sync-process-manifest.json');assert len(process)==13
for x in process:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256']
related=read(E/'related-source-manifest.json');assert len(related)==6 and sum(x['size'] for x in related)==84333;ri={x['id']:x for x in related}
for x in related:checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and not x['new_primary'] and not x['new_done']
values=dict(literal=read(S/rows[2]['stage_path']),input_BI=read(S/ri['e0c5edd8647cbfbf42c0']['snapshot']),previous_canonical=read(S/ri['2cd505cd05ed8ab77f21']['snapshot']))
view=read(E/'reading/reversible-action-view.json')
for label,v in values.items():
 decoded={}
 for depth,block in view['blocks'].items():
  for row in block:
   if depth=='0':decoded[()]=int(row[label])
   else:
    for a,ch in enumerate(row[label]):decoded[tuple(row['prefix'])+(a,)]=int(ch)
 restored=copy.deepcopy(view['metadata'][label]);actions=[dict(history=h,action=decoded[tuple(h)]) for h in view['original_row_order'][label]]
 if 'strategy' in restored:restored['strategy']['actions']=actions
 else:restored['actions']=actions
 assert len(decoded)==400 and restored==v
struct=read(E/'reading/structural-comparison.json');assert struct['input_BI_equals_previous_canonical_policy'] and not struct['literal_equals_previous_canonical_policy'] and struct['count']==14 and struct['all_changes_in_root6_noextra6_domain']
inp=read(E/'reading/input-structural-comparison.json');assert inp['players_equal'] and inp['customer_rows_equal'] and inp['first13_new_customer_rows_equal_old'] and not inp['topic_labels_equal'] and not inp['new_input_same_bytes']
assert values['literal']['security']==values['input_BI']['security']
expected=dict(status='PASS',method='expanded distinct unit clients, direct ordered-history policy replay, and exact saddle verification',old_histories=43,old_action_comparisons=258,eta='29/3',old_sizes=[23,23,21,23,23,21],delta=[11,11,11,11,11,11],J='19',tail_B_deviation_cap='19/2',root_old_upper_bound='35/2',minimum_last_old_alternative='21/2',all_B_last_payoff='19/3',new_histories=400,nice_histories=43,sibling_nice_ties_overridden=14,new_action_comparisons=2800,actual_path=[6,0,3,4],utilities=['19','29/3','67/6','67/6'],W=51,OPT=53,static_backgrounds=343,v4='28481/2924',v4_minus_u2='647/8772',scope='general lift proof audited separately; concrete finite SPE and saddle point exact; Q-CAG-HALF remains OPEN')
assert len(expected)==24 and read(S/rows[1]['stage_path'])==expected
cm=read(E/'formal-comparison.json');assert len(cm)==5
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
rec=read(W/'semantic-receipts.json');assert len(rec)==4 and [x['disposition'] for x in rec]==['retained','retained','retained','duplicate'] and {x['id'] for x in rec}=={x['id'] for x in rows}
for x in rec:assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==8
formal=S/'archives/customer-attraction/state/程序/不交保留字面策略的原始单位审计与十四处平局恢复--程序.md';t=formal.read_text()
for term in ['全部400动作','14个实际差异','全部24字段','343','210','无main guard','普通Python assert','不是同字节','B/P','386','281已same','284tracked','literal σ₁','不重扫IC','0次']:
 assert term in t,term
for doc in [formal,E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  q=(doc.parent/target).resolve();assert q.is_file() or (q.is_relative_to(S) and (R/q.relative_to(S)).is_file()),(doc,target)
ex=read(E/'execution-boundaries.json')
for k in ['original_entry_runs','original_imports','utility_calls','IC_replays','OPT_searches','static_payoff_replays','LP_runs','solver_runs','new_mathematical_program_runs']:assert ex[k]==0
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result=dict(status='pass',scope='bytes/provenance/all400-action JSON-object roundtrip/report24field literals/metadata declarations/links only; no utility/IC/OPT/static calculations',primary_files=4,primary_bytes=59269,related_files=6,related_bytes=84333,formal_comparisons=5,action_maps_fully_read=3,actions_per_map=400,new_formal_objects=1,retained=3,duplicate=1,relations=8,source_state_updates=[],raw_sync='needs-attention',preservation='initial1u284t281same3notrestored; Root restored3; final1u284tallsame/stash kept',original_entry_runs=0,original_imports=0,utility_calls=0,IC_replays=0,OPT_searches=0,static_payoff_replays=0,LP_runs=0,solver_runs=0,new_mathematical_program_runs=0)
(W/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
