"""Structural metadata/hash/blob/normal/owner/literal/link checks; no mathematical program execution."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 s=Path(sys.argv[1]).resolve();r=Path(sys.argv[2]).resolve()
 e=s/'archives/customer-attraction/tools/evidence/reserve-refund-induction-three-primary'
 w=s/'cleanup/workspaces/Boss4/r3-reserve-refund-induction-three-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 resolve=lambda p:s/p if (s/p).is_file() else r/p
 for j in read(e/'content-manifest.json')['files']:
  p=s/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 raw=read(e/'root-actual-claim13-receipt.json');gate=read(e/'ownership-gate.json');proof=read(e/'independent-sync-preservation.json')
 assert (raw['actor'],raw['status'],len(raw['ids']),raw['remote_tip'])==('Boss4','pushed',13,'60805cd6babdf1454eadda4c113896b864fcf6f6')
 assert raw['local_sync']['status']==gate['claim_local_sync']=='needs-attention' and raw['local_sync']==gate['raw_local_sync_unmodified']
 assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(j['same'] for j in proof['tracked'])
 assert not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept']
 assert proof['stash']==gate['independent_proof']['stash']=='c03c3aa204594167fe2f486215c55a1bdb9e7db4'
 rows=read(e/'source-manifest.json')['rows'];owners={j['id']:j for j in gate['owner_records']}
 assert len(rows)==3 and sum(j['size'] for j in rows)==11359 and set(owners)=={j['id'] for j in rows}
 assert set(gate['other_ten_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 for j in rows:
  p=s/j['target_path'];b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256'] and b==Path(j['local_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob']
  cap=s/j['acquisition_target'];cj=read(cap);assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes()
  assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
  assert j['full_file_read'] and j['current_source_imports']==j['current_source_runs']==0
 cb=read(e/'comparison-bindings.json');assert len(cb['full_formal_objects_read'])==10 and cb['current_full_formal_reads']==8 and cb['sameSHA_prior_full_formal_reads_reused']==2
 for j in cb['full_formal_objects_read']+[cb['status_only_half5_reference']]:
  p=r/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 assert cb['status_only_half5_reference']['full_file_read_in_this_batch'] is False and cb['runtime_input_files_required']==0 and cb['missing_runtime_inputs']==[]
 pb=read(e/'prior-full-original-bindings.json');pbr=pb['PB_review'];p=r/pbr['published_path'];assert p.is_file() and p.stat().st_size==4908 and sha(p)==pbr['sha256']
 tr=pb['tree_entry'];p=Path(tr['prior_frozen_path']);assert p.is_file() and p.stat().st_size==2731 and sha(p)==tr['sha256'] and tr['original_frozen_pending_notes_unchanged']
 assert not pbr['current_new_show'] and not pbr['new_raw_copy'] and not pbr['new_run'] and not tr['current_new_show'] and not tr['new_raw_copy'] and pb['new_related_done']==0
 pub=read(e/'direct2-actual-publication-binding.json');xc=read(e/'actual-direct2-math-checkpoint16XS.json');xd=read(e/'actual-direct2-source-done16XS.json')
 assert xc['status']=='pushed' and xc['remote_tip']==pub['actual_math_remote_tip']=='e6fe0dac2d217b365111a1e13f6a346bc82dfc97'
 assert xd['status']=='pushed' and xd['remote_tip']==pub['actual_done_remote_tip']=='8c93f752cf0eece9c56789af887a292dbb9c623b'
 assert set(pub['actual_done_ids'])=={'7058de1eadbe32d2f225','76d2b734847964da8011'}<=set(xd['ids'])
 assert pub['previous_frozen_tree5_pending_is_historical'] and pub['prior_package_unmodified'] and not pub['current_direct2_pending'] and pub['no_other_done_inferred']
 assert len(pub['published_formal_bodies'])==2
 for j in pub['published_formal_bodies']:
  p=r/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']
  a=next(z['asset'] for z in xc['assets'] if z['asset']['path']==j['path']);assert a==j['actual_asset'] and a['sha256']==j['sha256'] and a['commit']==xc['remote_tip']
 c=read(e/'mathematical-contracts.json');v=c['reserve']['old52']
 assert [v[k] for k in ('clients','players','old_coverage','W','Upast','U','Wnew','Mnew','F','RHS')]==[52,4,34,34,17,17,0,18,52,51]
 assert c['reserve']['current_truth'].startswith('false') and c['reserve']['weaker_Hres_refuted_by_samecase'] is False
 assert c['bank']['family_necessary_lambda_upper']=='1' and c['bank']['global_feasibility_at_lambda1'] is False and c['bank']['old52_further_necessary_lambda_upper']=='16/17' and c['bank']['no_sufficiency_at_16over17']
 assert not c['refund']['all_new_history_taxremoval_proved'] and not c['repair']['general_upper_repair_paid'] and c['conservation']['D_empty_or_all_and_c0_handled']
 scope=read(e/'original-evidence-scope.json');assert scope['primary_MD_files']==3 and scope['primary_MD_bytes']==11359
 assert scope['saved_pressure_only_MD']['full_prefix_nodes']==[43,259,43,31] and scope['cone_only_MD']['cones']==72
 assert not scope['saved_pressure_only_MD']['current_JSON_or_code_or_inputs_read'] and not scope['cone_only_MD']['current_JSON_or_code_read'] and not scope['saved_pressure_only_MD']['current_run'] and not scope['cone_only_MD']['current_run']
 receipts=read(w/'semantic-receipts.json');assert len(receipts)==3 and {j['id'] for j in receipts}==set(owners) and all(j['disposition']=='integrated' for j in receipts)
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
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=3,primary_bytes=11359,formal_objects=2,semantic_receipts=3,comparison_full_objects=10,current_full_formal_reads=8,prior_sameSHA_full_formal_reuses=2,prior_full_original_reuses=2,RESERVE_current_truth='false-same-existing-GLOBAL-claim',old52_mapping_literals_verified=True,global_lambda1_feasibility=False,new_lambda16over17_sufficiency=False,direct2_actual_math_remote_tip=xc['remote_tip'],direct2_actual_done_remote_tip=xd['remote_tip'],prior_frozen_pending_not_modified=True,runtime_input_files_required=0,missing_runtime_inputs=0,raw_local_sync='needs-attention-unmodified',independent_preservation='3untracked/2tracked same; no missing/different/unmerged; stash kept',markdown_links=links,copy_files=len(actual),source_imports=0,CLI_runs=0,Fraction_verification_runs=0,LP_runs=0,BI_runs=0,IC_replays=0,menu_replays=0,new_mathematical_program_runs=0,note='Only metadata/hash/blob/normalcaptures/owner/JSONliteral/currentpublicationasset/links; no original/mathprogram/old52SPE/diagnostic run or numerical theorem certification.')
 (e/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
