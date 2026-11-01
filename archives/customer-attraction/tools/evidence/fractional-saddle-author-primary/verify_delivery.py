"""File/provenance/link checks only; no Fraction or mathematical sources executed."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 stage=Path(sys.argv[1]).resolve();repo=Path(sys.argv[2]).resolve();ev=stage/'archives/customer-attraction/tools/evidence/fractional-saddle-author-primary';ws=stage/'cleanup/workspaces/Boss4/r3-fractional-saddle-author-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();resolve=lambda p:stage/p if (stage/p).is_file() else repo/p
 for r in read(ev/'content-manifest.json')['files']:
  p=stage/r['path'];assert p.is_file() and p.stat().st_size==r['size'] and sha(p)==r['sha256'],r['path']
 raw=read(ev/'root-actual-claim19-receipt.json');gate=read(ev/'ownership-gate.json');proof=read(ev/'independent-sync-preservation-proof.json')
 assert raw['actor']=='Boss4' and raw['status']=='pushed' and len(raw['ids'])==19 and raw['remote_tip']==gate['remote_tip']=='41c2e223127cbe5c48fcaa1f571cbb10fac8f45a'
 assert raw['local_sync']['status']=='needs-attention' and raw['local_sync']==gate['raw_local_sync_unmodified'] and gate['claim_local_sync']=='needs-attention'
 assert proof['receipt']=='boss4-resume-next19wy-claim' and proof['stash']=='75852f2c937ee082e5fa53e695ef669219da723f' and proof['stash'] in raw['local_sync']['detail'] and proof['stash_kept']
 assert proof['untracked_count']==38 and len(proof['tracked'])==2 and all(j['same'] for j in proof['tracked']) and proof['missing']==proof['different']==[] and proof['unmerged']==''
 rows=read(ev/'source-manifest.json')['rows'];owners={j['id']:j for j in gate['owner_records']};assert len(rows)==1 and rows[0]['id']=='435b7de2b9f7988b78af' and rows[0]['size']==7303 and set(owners)=={rows[0]['id']}
 assert set(gate['other_eighteen_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 for j in rows:
  p=stage/j['target_path'];b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256']
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob'] and b==Path(j['local_path']).read_bytes()
  cap=stage/j['acquisition_target'];assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes();cj=read(cap);assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  assert j['full_file_read'] and j['current_original_imports']==j['current_original_runs']==0
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
 comps=read(ev/'comparison-bindings.json')['full_formal_objects_read'];assert len(comps)==15
 for j in comps:
  p=repo/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']
 deps=read(ev/'dependency-bindings.json');assert len(deps['unacquired_raw_navigation'])==5 and not deps['raw_navigation_read'] and deps['related_extra_done']==deps['source_imports']==deps['CLI_runs']==0
 receipts=read(ws/'semantic-receipts.json');assert {j['id'] for j in receipts}==set(owners)
 for j in receipts:
  assert j['full_file_reviewed'] and j['related_material_checked'] and j['unique_content_accounted_for'] and j['disposition']=='integrated' and j['root_claim_local_sync']=='needs-attention'
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
 assert len(ids)==len(set(ids))==1
 actual=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file());assert sorted(read(ws/'copy-files.json'))==actual
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=1,primary_bytes=7303,formal_objects=1,semantic_receipts=1,comparison_full_objects=15,unacquired_raw_navigation_files=5,related_extra_done=0,markdown_links=links,copy_files=len(actual),raw_local_sync='needs-attention-unmodified',independent_recovery='38-untracked-and-2-tracked-identical; no-missing-different-unmerged; stash-kept',source_imports=0,CLI_runs=0,LP_runs=0,IC_replays=0,parameter_scans=0,new_mathematical_program_runs=0,note='Hashes/blob/normal capture/owner/proof metadata/links only. Current fixed-U bound is manual analytic reasoning in the body, not a program or original reported execution.')
 (ev/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
