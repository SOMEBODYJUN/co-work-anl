"""File/metadata/link checks only. Does not import or run mathematical sources."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 stage=Path(sys.argv[1]).resolve(); repo=Path(sys.argv[2]).resolve()
 ev=stage/'archives/customer-attraction/tools/evidence/round8-origin-density-and-joint-payment-root-primary'
 ws=stage/'cleanup/workspaces/Boss4/r3-round8-origin-density-and-joint-payment-root-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 resolve=lambda p:stage/p if (stage/p).is_file() else repo/p
 for r in read(ev/'content-manifest.json')['files']:
  p=stage/r['path'];assert p.is_file() and p.stat().st_size==r['size'] and sha(p)==r['sha256'],r['path']
 raw=read(ev/'root-actual-claim13-receipt.json');gate=read(ev/'ownership-gate.json')
 assert raw['status']=='pushed' and raw['actor']=='Boss4' and len(raw['ids'])==13
 assert raw['local_sync']['status']=='needs-attention' and raw['local_sync']==gate['raw_local_sync_unmodified']
 assert raw['remote_tip']==gate['remote_tip']=='d9c4518fcbf32737039021008b59bf58592fe58c'
 assert gate['claim_local_sync']=='needs-attention'
 proof=read(ev/'root-independent-sync-preservation.json')
 assert (ev/'root-independent-sync-preservation.json').read_bytes()==Path(gate['separate_preservation_original']).read_bytes()
 assert proof['untracked_count']==11 and len(proof['tracked'])==2 and all(r['same'] for r in proof['tracked'])
 assert proof['missing']==proof['different']==[] and proof['unmerged']=='' and proof['stash_kept'] is True
 assert proof['stash'] in raw['local_sync']['detail']
 rows=read(ev/'source-manifest.json')['rows'];owners={r['id']:r for r in gate['owner_records']}
 assert {r['id'] for r in rows}==set(owners)
 assert set(gate['other_twelve_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 assert len(rows)==1 and sum(r['size'] for r in rows)==5560
 for r in rows:
  p=resolve(Path(r['target_path']));b=p.read_bytes()
  assert len(b)==r['size'] and sha(p)==r['sha256']
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob']
  assert b==Path(r['local_path']).read_bytes()
  cap=stage/r['acquisition_target'];assert cap.read_bytes()==Path(r['actual_normal_show_capture']).read_bytes()
  cj=read(cap);assert cj['source']['id']==r['id'] and cj['source']['sha256']==r['sha256'] and cj['source']['blob']==r['blob']
  o=owners[r['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',r['sha256'])
  assert r['full_file_read'] and r['source_imports']==r['source_runs']==0
 deps=read(ev/'dependency-bindings.json')['rows']
 for r in deps:
  p=repo/r['published_path'];assert p.stat().st_size==r['size'] and sha(p)==r['sha256']
 comps=read(ev/'comparison-bindings.json')['full_formal_objects_read']
 for r in comps:
  p=repo/r['path'];assert p.stat().st_size==r['size'] and sha(p)==r['sha256']
 receipts=read(ws/'semantic-receipts.json');assert {r['id'] for r in receipts}==set(owners)
 for r in receipts:
  assert r['full_file_reviewed'] and r['related_material_checked'] and r['unique_content_accounted_for']
  assert r['current_original_mathematical_entries']==r['current_new_mathematical_entries']==0
  for p in r['targets']:assert resolve(Path(p)).is_file(),p
 links=0;ids=[]
 for p in stage.rglob('*.md'):
  if '/original/' in str(p):continue
  t=p.read_text()
  if '/state/' in str(p):
   assert t.startswith('---\n');front=t.split('---',2)[1]
   for k in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+k+':',front,re.M),(p,k)
   ids.append(re.search(r'^id:\s*(.+)$',front,re.M).group(1))
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
   if target.startswith(('http:','https:','#')):continue
   q=(p.parent/target.split('#')[0]).resolve();rel=q.relative_to(stage);assert resolve(rel).is_file(),(p,target);links+=1
 assert len(ids)==len(set(ids))==1
 actual=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file())
 assert sorted(read(ws/'copy-files.json'))==actual
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=1,primary_bytes=5560,new_original_files=1,new_original_bytes=5560,comparison_full_objects=len(comps),dependency_files=len(deps),semantic_receipts=len(receipts),formal_objects=len(ids),checked_markdown_links=links,copy_files=len(actual),source_imports=0,source_CLI_runs=0,LP_runs=0,IC_replays=0,bank_enumerations=0,new_mathematical_program_runs=0,note='Hashes/blob/owner snapshots/copy list/links only. Mathematical reasoning is documented separately; no new blind audit or numerical proof.')
 (ev/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
