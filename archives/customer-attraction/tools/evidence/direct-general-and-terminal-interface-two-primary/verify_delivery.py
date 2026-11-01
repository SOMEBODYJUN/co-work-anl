"""Metadata/hash/blob/normal-capture/owner/link checks only; no original mathematical program."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 s=Path(sys.argv[1]).resolve();r=Path(sys.argv[2]).resolve()
 e=s/'archives/customer-attraction/tools/evidence/direct-general-and-terminal-interface-two-primary'
 w=s/'cleanup/workspaces/Boss4/r3-direct-general-and-terminal-interface-two-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 resolve=lambda p:s/p if (s/p).is_file() else r/p
 for j in read(e/'content-manifest.json')['files']:
  p=s/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 raw=read(e/'root-actual-claim16-receipt.json');gate=read(e/'ownership-gate.json');proof=read(e/'independent-sync-preservation.json')
 assert (raw['actor'],raw['status'],len(raw['ids']),raw['remote_tip'])==('Boss4','pushed',16,'9f40d76914d79901dfe630474f1f2448653ce815')
 assert raw['local_sync']['status']==gate['claim_local_sync']=='needs-attention' and raw['local_sync']==gate['raw_local_sync_unmodified']
 assert proof['untracked_count']==2 and len(proof['tracked'])==2 and all(j['same'] for j in proof['tracked'])
 assert not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept']
 assert proof['stash']==gate['independent_proof']['stash']=='77db1fe5a8c3d099722e4d690877dba29daaa606'
 rows=read(e/'source-manifest.json')['rows'];owners={j['id']:j for j in gate['owner_records']}
 assert len(rows)==2 and sum(j['size'] for j in rows)==14765 and set(owners)=={j['id'] for j in rows}
 assert set(gate['other_fourteen_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 for j in rows:
  p=s/j['target_path'];b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256'] and b==Path(j['local_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob']
  cap=s/j['acquisition_target'];cj=read(cap);assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes()
  assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
  assert j['full_file_read'] and j['current_source_imports']==j['current_source_runs']==0
 cb=read(e/'comparison-bindings.json');assert len(cb['full_formal_objects_read'])==13 and cb['current_full_formal_reads']==10 and cb['sameSHA_prior_full_formal_reads_reused']==3
 for j in cb['full_formal_objects_read']+[cb['status_only_reference']]:
  p=r/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 assert cb['status_only_reference']['full_file_read_in_this_batch'] is False and cb['missing_runtime_inputs']==[]
 contract=read(e/'mathematical-contracts.json');assert not contract['terminal']['cross_branch_bank_charge_proved'] and not contract['saddle']['payment_proved']
 assert contract['actual_load']['later_Bact_exists'] and not contract['actual_load']['later_TPAY_proved'] and not contract['endpoint']['global_reachability_of_all_local_endpoints']
 scope=read(e/'original-evidence-scope.json');assert scope['original_main_sections']==7 and scope['original_review_bytes']==2057 and len(scope['only_MD_claims_not_new_logs'])==4
 assert [j.get('floating_HiGHS_optimizations') for j in scope['only_MD_claims_not_new_logs'][1:3]]==[861,861]
 assert scope['current_imports']==scope['current_runs']==0
 receipts=read(w/'semantic-receipts.json');assert len(receipts)==2 and {j['id'] for j in receipts}==set(owners)
 assert sorted(j['disposition'] for j in receipts)==['integrated','retained']
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
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=2,primary_bytes=14765,formal_objects=2,semantic_receipts=2,comparison_full_objects=13,current_full_formal_reads=10,prior_sameSHA_full_formal_reuses=3,status_only_half5_reference=1,missing_runtime_inputs=0,raw_local_sync='needs-attention-unmodified',independent_preservation='2untracked/2tracked same, no missing/different/unmerged, stash kept',markdown_links=links,copy_files=len(actual),source_imports=0,CLI_runs=0,Fraction_verification_runs=0,LP_runs=0,BI_runs=0,IC_replays=0,menu_replays=0,new_mathematical_program_runs=0,note='Only metadata/hash/blob/normalcaptures/owner/JSON literal boundaries/links. No original code, numerical diagnostic, or theorem checker imported/run; no new mathematical certification.')
 (e/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
