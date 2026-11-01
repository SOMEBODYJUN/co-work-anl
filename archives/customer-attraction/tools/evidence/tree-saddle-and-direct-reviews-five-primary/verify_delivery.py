"""Structural metadata/hash/blob/normal/owner/literal/link audit only; no mathematical source execution."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 s=Path(sys.argv[1]).resolve();r=Path(sys.argv[2]).resolve()
 e=s/'archives/customer-attraction/tools/evidence/tree-saddle-and-direct-reviews-five-primary'
 w=s/'cleanup/workspaces/Boss4/r3-tree-saddle-and-direct-reviews-five-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 resolve=lambda p:s/p if (s/p).is_file() else r/p
 for j in read(e/'content-manifest.json')['files']:
  p=s/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 raw=read(e/'root-actual-claim22-receipt.json');gate=read(e/'ownership-gate.json');proof=read(e/'independent-sync-preservation.json')
 assert (raw['actor'],raw['status'],len(raw['ids']),raw['remote_tip'])==('Boss4','pushed',22,'26ab863135a398ab834f336fec5570fb382d9b76')
 assert raw['local_sync']['status']==gate['claim_local_sync']=='needs-attention' and raw['local_sync']==gate['raw_local_sync_unmodified']
 assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(j['same'] for j in proof['tracked'])
 assert not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept']
 assert proof['stash']==gate['independent_proof']['stash']=='b9a9e41e35155d585dd528ae184ba5f5784eb5ad'
 rows=read(e/'source-manifest.json')['rows'];owners={j['id']:j for j in gate['owner_records']}
 assert len(rows)==5 and sum(j['size'] for j in rows)==22481 and set(owners)=={j['id'] for j in rows}
 assert set(gate['other_seventeen_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 for j in rows:
  p=s/j['target_path'];b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256'] and b==Path(j['local_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob']
  cap=s/j['acquisition_target'];cj=read(cap);assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes()
  assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
  assert j['full_file_read'] and j['current_source_imports']==j['current_source_runs']==0
 rb=read(e/'related-source-and-pending-bindings.json')
 assert len(rb['already_published_originals'])==len(rb['pending_direct2_originals'])==len(rb['pending_direct2_formal_bodies'])==2
 assert rb['already_published_original_bytes']==16384 and rb['pending_direct2_original_bytes']==14765
 for j in rb['already_published_originals']:
  p=r/j['published_path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']
  assert j['complete_original_previously_read'] and not j['current_new_show'] and not j['new_raw_copy'] and j['extra_done']==0
 for j in rb['pending_direct2_originals']:
  p=Path(j['frozen_source_path']);assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']
  assert j['complete_original_previously_read'] and not j['current_new_show'] and not j['new_raw_copy'] and j['extra_done']==0 and j['publication_status'].startswith('pending')
 for j in rb['pending_direct2_formal_bodies']:
  p=Path(j['frozen_path']);assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'] and j['publication_status'].startswith('pending') and j['remote_math_tip'] is None
 assert not rb['pending_source_done_inferred'] and rb['runtime_input_files_required']==0 and rb['missing_runtime_inputs']==[]
 cb=read(e/'comparison-bindings.json');assert len(cb['full_formal_objects_read'])==8 and cb['current_full_formal_reads']==2 and cb['sameSHA_prior_full_formal_reads_reused']==6 and cb['pending_direct2_full_formal_reuses']==2
 for j in cb['full_formal_objects_read']+[cb['status_only_half5_reference']]:
  p=r/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 assert cb['status_only_half5_reference']['full_file_read_in_this_batch'] is False
 c=read(e/'mathematical-contracts.json');assert not c['shared']['common_payment_proved'] and not c['demand']['customer_reweighted_IC'] and c['swap']['equality_version_retained'] and not c['swap']['mean_r_gap_paid'] and not c['potential']['changed_prefix_resets_paid']
 scope=read(e/'original-evidence-and-review-scope.json');assert scope['primary_MD_files']==5 and scope['primary_MD_bytes']==22481
 assert [j['minimum_gap'] for j in scope['named_pressure_only_MD_report']]==['11/2','650970032217399586','2']
 assert not any(scope[k] for k in ('current_named_code_read','current_named_JSON_read','current_named_policy_inputs_read','current_named_run'))
 receipts=read(w/'semantic-receipts.json');assert len(receipts)==5 and {j['id'] for j in receipts}==set(owners) and sorted(j['disposition'] for j in receipts)==['integrated']*3+['retained']*2
 for j in receipts:
  assert j['full_file_reviewed'] and j['related_material_checked'] and j['unique_content_accounted_for'] and j['root_claim_local_sync']=='needs-attention'
  assert j['current_original_mathematical_entries']==j['current_new_mathematical_entries']==0
  for rp in j['targets']:assert resolve(Path(rp)).is_file(),rp
 links=0;ids=[]
 for p in s.rglob('*.md'):
  if '/original/' in str(p):continue
  t=p.read_text()
  if '/state/' in str(p):
   assert t.startswith('---\n');front=t.split('---',2)[1]
   for k in ('id','kind','type_tag','title','status','summary','source_refs'):assert re.search('^'+k+':',front,re.M),(p,k)
   ids.append(re.search(r'^id:\s*(.+)$',front,re.M).group(1))
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
   if target.startswith(('http:','https:','#')):continue
   q=(p.parent/target.split('#')[0]).resolve();rp=q.relative_to(s);assert resolve(rp).is_file(),(p,target);links+=1
 assert len(ids)==len(set(ids))==2
 actual=sorted(str(p.relative_to(s)) for p in s.rglob('*') if p.is_file());assert sorted(read(w/'copy-files.json'))==actual
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=5,primary_bytes=22481,formal_objects=2,semantic_receipts=5,comparison_published_full_objects=8,current_full_formal_reads=2,prior_sameSHA_full_formal_reuses=6,reused_published_originals=2,pending_direct2_originals=2,pending_direct2_formal_objects=2,pending_source_done_inferred=False,status_only_half5_reference=1,runtime_input_files_required=0,missing_runtime_inputs=0,whole_named_gap_MD_literals=3,raw_local_sync='needs-attention-unmodified',independent_preservation='3untracked/2tracked same; no missing/different/unmerged; stash kept',markdown_links=links,copy_files=len(actual),source_imports=0,CLI_runs=0,Fraction_verification_runs=0,LP_runs=0,BI_runs=0,IC_replays=0,menu_replays=0,new_mathematical_program_runs=0,note='Only metadata/hash/blob/normalcaptures/owner/JSONliteral/links. No original/named/code/JSON/policy inputs or mathematical checker run; no new mathematical certification.')
 (e/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
