"""File, provenance, literal JSON and links only; no mathematical source import or execution."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 stage=Path(sys.argv[1]).resolve();repo=Path(sys.argv[2]).resolve();ev=stage/'archives/customer-attraction/tools/evidence/round11-extra-fractional-plateau-primary';ws=stage/'cleanup/workspaces/Boss4/r3-round11-extra-fractional-plateau-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();resolve=lambda p:stage/p if (stage/p).is_file() else repo/p
 for r in read(ev/'content-manifest.json')['files']:
  p=stage/r['path'];assert p.is_file() and p.stat().st_size==r['size'] and sha(p)==r['sha256'],r['path']
 raw=read(ev/'root-actual-claim26-receipt.json');gate=read(ev/'ownership-gate.json');proof=read(ev/'independent-sync-preservation-proof.json')
 assert raw['actor']=='Boss4' and raw['status']=='pushed' and len(raw['ids'])==26 and raw['remote_tip']==gate['remote_tip']=='1f16a464c89fc5bc36d035677e6fb39364a18bc7'
 assert raw['local_sync']['status']=='needs-attention' and raw['local_sync']==gate['raw_local_sync_unmodified'] and gate['claim_local_sync']=='needs-attention'
 assert proof['stash']=='d5b4366bfdc3be47f06d3f4384b88afdb7c9c1da' and proof['stash'] in raw['local_sync']['detail'] and proof['stash_kept']
 assert proof['untracked_count']==38 and len(proof['tracked'])==2 and all(x['same'] for x in proof['tracked']) and proof['missing']==proof['different']==[] and proof['unmerged']==''
 rows=read(ev/'source-manifest.json')['rows'];owners={x['id']:x for x in gate['owner_records']};assert len(rows)==5 and sum(x['size'] for x in rows)==7903 and {x['id'] for x in rows}==set(owners)
 assert set(gate['other_twenty_one_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 for j in rows:
  p=stage/j['target_path'];b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256']
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob'] and b==Path(j['local_path']).read_bytes()
  cap=stage/j['acquisition_target'];assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes();cj=read(cap);assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  assert j['full_file_read'] and j['current_source_imports']==j['current_source_runs']==0
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
 comps=read(ev/'comparison-bindings.json')['full_formal_objects_read'];assert len(comps)==12
 for j in comps:
  p=repo/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']
 rf=read(ev/'report-field-binding.json');author=read(stage/next(j['target_path'] for j in rows if j['id']=='c5bc798dbff835c0e3ee'));parent=read(stage/next(j['target_path'] for j in rows if j['id']=='884ea11430f19ee6c272'))
 assert rf['author_full_report']==author and rf['parent_full_report']==parent and not rf['arithmetic_recomputed'] and not rf['producer_code_for_parent_acquired']
 assert set(author)=={'scope','checks','L','theta','local_balance','aggregate_balance'} and set(parent)=={'scope','checks','local_balance','aggregate_balance'}
 assert len(author['checks'])==9 and len(parent['checks'])==7 and all(v is True for v in author['checks'].values()) and all(v is True for v in parent['checks'].values())
 assert author['local_balance']==parent['local_balance'] and author['aggregate_balance']==parent['aggregate_balance']
 receipts=read(ws/'semantic-receipts.json');assert {j['id'] for j in receipts}==set(owners)
 for j in receipts:
  assert j['full_file_reviewed'] and j['related_material_checked'] and j['unique_content_accounted_for'] and j['root_claim_local_sync']=='needs-attention'
  assert j['current_original_mathematical_entries']==j['current_new_mathematical_entries']==0
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
   q=(p.parent/target.split('#')[0]).resolve();rel=q.relative_to(stage);assert resolve(rel).is_file(),(p,target);links+=1
 assert len(ids)==len(set(ids))==2
 actual=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file());assert sorted(read(ws/'copy-files.json'))==actual
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=5,primary_bytes=7903,formal_objects=2,semantic_receipts=5,comparison_full_objects=12,original_author_declared_true_flags=9,original_parent_declared_true_flags=7,report_balance_strings_equal=True,arithmetic_recomputed=False,markdown_links=links,copy_files=len(actual),raw_local_sync='needs-attention-unmodified',independent_recovery='38-untracked-and-2-tracked-identical; no-missing-different-unmerged; stash-kept',source_imports=0,CLI_runs=0,LP_runs=0,IC_replays=0,menu_enumerations=0,new_mathematical_program_runs=0,note='Metadata/hash/blob/owner/normal-capture/schema/literal/links only. No new Fraction verification or mathematical source run; proofs are in the two bodies.')
 (ev/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
