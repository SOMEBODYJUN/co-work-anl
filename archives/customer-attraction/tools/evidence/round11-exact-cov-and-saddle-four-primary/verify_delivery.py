"""Metadata/hash/blob/whole JSON/link checks only; does not import NumPy/Fraction or source code."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 stage=Path(sys.argv[1]).resolve();repo=Path(sys.argv[2]).resolve();ev=stage/'archives/customer-attraction/tools/evidence/round11-exact-cov-and-saddle-four-primary';ws=stage/'cleanup/workspaces/Boss4/r3-round11-exact-cov-and-saddle-four-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();resolve=lambda p:stage/p if (stage/p).is_file() else repo/p
 for j in read(ev/'content-manifest.json')['files']:
  p=stage/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 raw=read(ev/'root-actual-claim15-receipt.json');gate=read(ev/'ownership-gate.json');proof=read(ev/'independent-sync-preservation-proof.json')
 assert raw['actor']=='Boss4' and raw['status']=='pushed' and len(raw['ids'])==15 and raw['remote_tip']==gate['remote_tip']=='aaa6b5e5ca5bd4ab2f4e2ec30473b4fd5bea8f5f'
 assert raw['local_sync']['status']=='needs-attention' and raw['local_sync']==gate['raw_local_sync_unmodified'] and gate['claim_local_sync']=='needs-attention'
 assert proof['receipt']=='boss4-resume-next15xd-claim' and proof['stash']=='25f460c713f272cabd9d161cf2c4e5ddc0e24a65' and proof['stash'] in raw['local_sync']['detail'] and proof['stash_kept']
 assert proof['untracked_count']==38 and len(proof['tracked'])==2 and all(j['same'] for j in proof['tracked']) and proof['missing']==proof['different']==[] and proof['unmerged']==''
 rows=read(ev/'source-manifest.json')['rows'];owners={j['id']:j for j in gate['owner_records']};assert len(rows)==4 and sum(j['size'] for j in rows)==12652 and {j['id'] for j in rows}==set(owners)
 assert set(gate['other_eleven_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 for j in rows:
  p=stage/j['target_path'];b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256'] and b==Path(j['local_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob']
  cap=stage/j['acquisition_target'];assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes();cj=read(cap);assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  assert j['full_file_read'] and j['current_source_imports']==j['current_source_runs']==0
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
 comps=read(ev/'comparison-bindings.json')['full_formal_objects_read'];assert len(comps)==7
 for j in comps:
  p=repo/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']
 reports=read(ev/'report-field-binding.json');cov=read(stage/next(j['target_path'] for j in rows if j['id']=='681d784e6e5e12d991e1'));sad=read(stage/next(j['target_path'] for j in rows if j['id']=='fa0a10261685ebac3429'))
 assert reports['covariance_full_report']==cov and reports['saddle_full_report']==sad and not reports['arithmetic_recomputed']
 assert len(cov)==14 and len(sad)==17 and cov['L']==sad['L'] and cov['q']==sad['q'] and cov['menu_minimum_anchor_load']==sad['menu_minimum_anchor_load']
 assert len(cov['L'])==11 and len(cov['q'])==6 and len(cov['menu_minimum_anchor_load'])==6
 assert all(len(cov['by_role'][k])==len(sad['by_role'][k])==6 for k in ['C','D','IC'])
 assert len(sad['query_values'])==30 and sad['query_values'][:5]==['14/11']*5 and sad['query_values'][5:]==['37/22']*25
 pref=read(ev/'common-controller-prefix-binding.json');src={j['id']:stage/j['target_path'] for j in rows};a=src[pref['first_source']].read_bytes().split(pref['split_marker'].encode(),1)[0];b=src[pref['second_source']].read_bytes().split(pref['split_marker'].encode(),1)[0]
 assert a==b and len(a)==pref['prefix_bytes']==1450 and hashlib.sha256(a).hexdigest()==pref['prefix_sha256']=='4a7ef2e9c6e02451e9e8f3129c44dc1f8377f75799e1e63c15c8cdeab3c69dd9'
 deps=read(ev/'dependency-bindings.json');assert deps['runtime_input_files']==deps['runtime_external_code_modules']==[] and deps['related_extra_done']==deps['source_imports']==deps['source_runs']==0
 receipts=read(ws/'semantic-receipts.json');assert {j['id'] for j in receipts}==set(owners)
 for j in receipts:
  assert j['full_file_reviewed'] and j['related_material_checked'] and j['unique_content_accounted_for'] and j['disposition']=='retained' and j['root_claim_local_sync']=='needs-attention'
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
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=4,primary_bytes=12652,formal_objects=1,semantic_receipts=4,comparison_full_objects=7,whole_reports_bound=2,all_by_role_entries_retained=36,saddle_query_values=30,identical_controller_prefix_bytes=1450,arithmetic_recomputed=False,markdown_links=links,copy_files=len(actual),raw_local_sync='needs-attention-unmodified',independent_recovery='38untracked/2tracked same, no missing/different/unmerged, stashkept',source_imports=0,CLI_runs=0,NumPy_runs=0,Fraction_verification_runs=0,LP_runs=0,IC_replays=0,menu_replays=0,new_mathematical_program_runs=0,note='Metadata/schema/literal/hash/blob/owner/capture/link checks only. No numerical or mathematical source execution.')
 (ev/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
