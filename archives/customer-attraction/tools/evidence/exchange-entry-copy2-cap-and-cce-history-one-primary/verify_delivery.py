from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-exchange-entry-copy2-cap-and-cce-history-one-primary'
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,a):
 b=p.read_bytes();assert sha(p)==a['sha256']
 if 'size' in a:assert len(b)==a['size']
 if 'blob' in a:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob']
def resolve(rp):return S/rp if (S/rp).is_file() else R/rp
sm=j(E/'source-manifest.json');a=sm['rows'][0];og=j(E/'ownership-gate.json');raw=j(E/'acquisition/root-actual-full25-claim.json')
assert (sm['primary_sources'],sm['primary_bytes'],a['id'])==(1,2552,'3cba6a3a2f7ce4898612')
assert (raw['status'],raw['actor'],len(raw['ids']),raw['remote_tip'],raw['local_sync']['status'])==('pushed','Boss4',25,'60de7e55e68b1baace6ae3c4e5ee1743cd82d52f','needs-attention')
assert og['raw_original_local_sync']==raw['local_sync'] and og['remote_tip']==raw['remote_tip'] and set(og['other_24_ids_not_processed'])==set(raw['ids'])-{a['id']}
assert (og['current_source_owner_record']['owner'],og['current_source_owner_record']['disposition'],og['current_source_owner_record']['source_sha256'])==('Boss4','in-progress',a['sha256'])
check(S/a['target_path'],a);sc=j(E/'acquisition/normal-show-original.json')['source'];assert (sc['id'],sc['sha256'],sc['blob'])==(a['id'],a['sha256'],a['blob'])
assert a['first_primary'] and a['current_full_body_read'] and a['current_first_full_body_reads']==1 and a['current_source_body_rereads']==a['current_imports']==a['current_runs']==0
assert sm['Root_actual_normal_shows']==1 and sm['worker_actual_normal_shows']==sm['original_math_runs']==sm['new_math_runs']==0
proof=j(E/'independent-final-sync-preservation.json');rest=j(E/'root-tracked-restoration-original.json');pb=j(E/'complete-claim-restoration-binding.json')
assert proof['stash']==rest['stash']==pb['stash']=='6e6bae58637cd22107d85dc3d1c8c7169281c556' and proof['stash_kept'] and rest['stash_kept'] and pb['stash_kept']
assert proof['untracked_count']==1 and len(proof['tracked'])==284 and all(x['same'] for x in proof['tracked']) and not proof['missing'] and not proof['different'] and not proof['unmerged']
initial=j(S/pb['initial_report_original_target']);assert len(initial['tracked'])==284 and sum(x['same'] for x in initial['tracked'])==281 and len(pb['initial_different_same_flag_rows'])==3
assert pb['raw_sync_status']=='needs-attention' and len(pb['preserved_all_13_file_bindings'])==13 and sum(x['size'] for x in pb['preserved_all_13_file_bindings'])==929966 and pb['deduplicated_content_payloads']==7
for x in pb['preserved_all_13_file_bindings']:check(S/x['target_path'],x)
assert {x['path'] for x in initial['tracked'] if not x['same']}=={x['path'] for x in rest['restored_tracked_local_drafts']}
for x in pb['restoration_rows']:
 st=S/x['stash_snapshot_target'];li=S/x['live_snapshot_target'];assert sha(st)==x['stash_sha256']==x['restored_sha256'] and sha(li)==x['live_before_restore_sha256']
 assert st.read_bytes().startswith(li.read_bytes())==x['worker_observed_live_is_prefix_of_stash']
assert [x['worker_observed_live_is_prefix_of_stash'] for x in pb['restoration_rows']]==[False,True,False]
links=j(E/'eight-original-link-bindings.json');assert len(links['rows'])==links['original_links']==8 and links['all_eight_existing_single_originals_sha_blob_verified'] and links['new_copies']==links['new_fullreads_of_eight']==links['new_runs']==0
for x in links['rows']:
 check(R/x['existing_single_original_path'],x);assert not x['current_original_copy'] and not x['current_fullread'] and not x['current_run'] and x['published_disposition'] in ['integrated','retained','duplicate']
cp=j(E/'full-mathematical-comparison-bindings.json');assert len(cp['rows'])==5 and cp['new_formal_fullreads']==2 and cp['prior_complete_formal_reuses']==3 and cp['current_source_imports']==cp['current_original_math_runs']==cp['current_new_math_runs']==0
for x in cp['rows']:check(R/x['path'],x)
pub=j(E/'PCAP2-actual-publication-binding.json');xc=j(E/'actual20ZP-math-checkpoint.json');xd=j(E/'actual20ZP-source-done.json')
assert xc['status']=='pushed' and xc['remote_tip']==pub['actual_math_tip']=='74b61ca312df8cc8ee2d03db1da2ed45c44c8bfe' and xd['status']=='pushed' and xd['remote_tip']==pub['actual_done_tip']=='d12347b8123a7c40495af8216e33ac451ca92769'
assert {'1990d9140791350ba8da','ce434cd1722c392c35d5'}<=set(xd['ids']) and pub['asset'] in [x['asset'] for x in xc['assets']];check(R/pub['asset']['path'],pub['asset'])
rc=j(W/'semantic-receipts.json');assert len(rc)==1 and rc[0]['id']==a['id'] and rc[0]['full_file_reviewed'] and rc[0]['related_material_checked'] and rc[0]['unique_content_accounted_for']
for x in rc[0]['targets']:assert resolve(x).is_file(),x
assert rc[0]['current_source_body_rereads']==rc[0]['current_source_imports']==rc[0]['current_original_mathematical_entries']==rc[0]['current_new_mathematical_entries']==rc[0]['additional_primary_done']==0
missing=[]
for f in S.rglob('*.md'):
 if '/original/' in str(f):continue
 for link in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if '://' in link or link.startswith('#'):continue
  q=(f.parent/link.split('#')[0]).resolve()
  if q.is_file():continue
  try:rp=q.relative_to(S)
  except ValueError:missing.append([str(f.relative_to(S)),link]);continue
  if not (R/rp).is_file():missing.append([str(f.relative_to(S)),link])
assert not missing,missing
mf=j(E/'content-manifest.json')
for x in mf['files']:check(S/x['path'],x)
paths={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()};assert set(j(W/'copy-files.json')['files'])==paths
result={'status':'PASS-STRUCTURE-ONLY','primary_sources':1,'primary_bytes':2552,'formal_objects':1,'source_imports':0,'source_runs':0,'new_math_runs':0,'existing_original_link_targets':8,'preserved_original_snapshot_files':13,'deduplicated_snapshot_payloads':7,'initial_tracked_same':281,'initial_tracked_total':284,'final_tracked_same':284,'final_tracked_total':284,'raw_claim_status':'pushed','raw_local_sync_status':'needs-attention','missing_links':0,'content_manifest_files':len(mf['files']),'copy_files':len(paths),'not_new_IC_BI_CCE_or_request_verification':True}
(E/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
