"""File/hash/blob/publication receipt/owner/link checks only; no original code or mathematical solver run."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 stage=Path(sys.argv[1]).resolve();repo=Path(sys.argv[2]).resolve();ev=stage/'archives/customer-attraction/tools/evidence/insurance-transport-module-report-and-interface-primary';ws=stage/'cleanup/workspaces/Boss4/r3-insurance-transport-module-report-and-interface-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();resolve=lambda p:stage/p if (stage/p).is_file() else repo/p
 for j in read(ev/'content-manifest.json')['files']:
  p=stage/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 raw=read(ev/'root-actual-claim15-receipt.json');gate=read(ev/'ownership-gate.json');proof=read(ev/'independent-sync-preservation-proof.json')
 assert raw['actor']=='Boss4' and raw['status']=='pushed' and len(raw['ids'])==15 and raw['remote_tip']==gate['remote_tip']=='195f7f40ae8fe9d2c00451b3ab9d22f419b94f1b'
 assert raw['local_sync']['status']=='needs-attention' and raw['local_sync']==gate['raw_local_sync_unmodified'] and gate['claim_local_sync']=='needs-attention'
 assert proof['receipt']=='boss4-resume-next15xl-claim' and proof['stash']=='af8e0e4651193e50c196fe01339890ddc651a36e' and proof['stash'] in raw['local_sync']['detail'] and proof['stash_kept']
 assert proof['untracked_count']==2 and len(proof['tracked'])==2 and all(j['same'] for j in proof['tracked']) and proof['missing']==proof['different']==[] and proof['unmerged']==''
 prereq=read(ev/'published-prerequisite-bindings.json');ck=read(ev/'matching-prerequisite-math-checkpoint.json');assert prereq['status']==ck['status']=='pushed' and not prereq['pending'] and not prereq['source_done_inferred']
 assert prereq['batch']=='R3_RESUME6XM' and prereq['initial_commit']==ck['commit']=='9a680b6fb33b2c95e0021863f6b82d45a1b5a715'
 assert prereq['remote_math_tip']==ck['remote_tip']==ck['pushed_head']==ck['checked_head']=='4ddfa8f84fe10982e5f6456d064f92ed3ff48a0d'
 assets={j['asset']['path']:j['asset'] for j in ck['assets']};assert len(prereq['rows'])==4
 for j in prereq['rows']:
  p=repo/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'] and p.read_bytes()==Path(j['prior_frozen_path']).read_bytes()
  assert assets[j['path']]['sha256']==j['sha256'] and assets[j['path']]['commit']==j['published_math_commit']==ck['remote_tip']
 sm=read(ev/'source-manifest.json');rows=sm['rows'];owners={j['id']:j for j in gate['owner_records']};assert len(rows)==3 and sum(j['size'] for j in rows)==15575 and {j['id'] for j in rows}==set(owners)
 assert sm['reused_original_bytes']==10055 and sm['new_original_files']==1 and sm['new_original_bytes']==5520 and sm['old_related_extra_done']==0
 assert set(gate['other_twelve_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 for j in rows:
  p=resolve(Path(j['target_path']));b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256'] and b==Path(j['local_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob']
  cap=stage/j['acquisition_target'];assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes();cj=read(cap);assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  assert j['full_file_read'] and j['primary_first_time'] and j['current_original_imports']==j['current_original_runs']==0
  if j['id']!='2a8e91c3f73c3ca0fa51':assert j['exact_prior_normal_show_reused'] and j['no_new_normal_show_for_this_source'] and not j['current_full_source_read'] and not j['new_raw_copy'] and j['previous_related_extra_done']==0
  else:assert j['current_full_source_read'] and j['new_raw_copy']
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
 comps=read(ev/'comparison-bindings.json')['full_formal_objects_read'];assert len(comps)==8
 for j in comps:
  p=repo/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']
 deps=read(ev/'dependency-bindings.json');assert deps['current_program_inputs_missing']==[] and deps['related_extra_done']==0 and not deps['new_normal_show_for_reused_two'] and not deps['new_raw_copy_for_reused_two']
 for j in deps['packet_reuse_rows']:
  p=repo/j['published_path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']
 receipts=read(ws/'semantic-receipts.json');assert {j['id'] for j in receipts}==set(owners)
 assert sorted(j['disposition'] for j in receipts)==['duplicate','duplicate','integrated']
 for j in receipts:
  assert j['full_file_reviewed'] and j['related_material_checked'] and j['unique_content_accounted_for'] and j['root_claim_local_sync']=='needs-attention' and not j['prior_source_done_inferred']
  assert j['prerequisite_math_commit']==ck['remote_tip'] and j['current_original_mathematical_entries']==j['current_new_mathematical_entries']==0
  for rp in j['targets']:assert resolve(Path(rp)).is_file(),rp
 links=0;ids=[]
 for p in stage.rglob('*.md'):
  if '/original/' in str(p):continue
  t=p.read_text()
  if '/state/' in str(p):
   assert t.startswith('---\n');front=t.split('---',2)[1]
   for k in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+k+':',front,re.M),(p,k)
   ids.append(re.search(r'^id:\s*(.+)$',front,re.M).group(1))
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
   if target.startswith(('https:','http:','#')):continue
   q=(p.parent/target.split('#')[0]).resolve();r=q.relative_to(stage);assert resolve(r).is_file(),(p,target);links+=1
 assert len(ids)==len(set(ids))==1
 actual=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file());assert sorted(read(ws/'copy-files.json'))==actual
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=3,primary_bytes=15575,reused_published_original_files=2,reused_original_bytes=10055,new_original_files=1,new_original_bytes=5520,formal_objects=1,semantic_receipts=3,comparison_full_objects=8,prerequisite_status='actual6XM-pushed4ddfa8f',prerequisite_done_inferred=False,dispositions=['duplicate','duplicate','integrated'],markdown_links=links,copy_files=len(actual),raw_local_sync='needs-attention-unmodified',independent_recovery='2untracked/2tracked same bytes, no missing/different/unmerged, stashkept',source_imports=0,CLI_runs=0,Hungarian_runs=0,solver_runs=0,menu_replays=0,new_mathematical_program_runs=0,note='Only file/hash/blob/actualcheckpointasset/normalcapture/owner/links; no transport LP or original program executed.')
 (ev/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
