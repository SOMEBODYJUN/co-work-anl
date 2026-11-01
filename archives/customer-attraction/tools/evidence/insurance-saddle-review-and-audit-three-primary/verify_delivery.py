"""File/metadata/JSON literal/order/link checks only; no source import or mathematical program run."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 stage=Path(sys.argv[1]).resolve();repo=Path(sys.argv[2]).resolve();ev=stage/'archives/customer-attraction/tools/evidence/insurance-saddle-review-and-audit-three-primary';ws=stage/'cleanup/workspaces/Boss4/r3-insurance-saddle-review-and-audit-three-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();resolve=lambda p:stage/p if (stage/p).is_file() else repo/p
 for j in read(ev/'content-manifest.json')['files']:
  p=stage/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 raw=read(ev/'root-actual-claim20-receipt.json');gate=read(ev/'ownership-gate.json');rows=read(ev/'source-manifest.json')['rows'];owners={j['id']:j for j in gate['owner_records']};deps=read(ev/'dependency-bindings.json')
 assert raw['actor']=='Boss4' and raw['status']=='pushed' and len(raw['ids'])==20 and raw['remote_tip']==gate['remote_tip']=='e6219d33a7cf892816a8195f0984e9c110f4d41a'
 assert raw['local_sync']['status']=='synced' and raw['local_sync']==gate['raw_local_sync_unmodified'] and gate['claim_local_sync']=='synced'
 assert len(rows)==3 and sum(j['size'] for j in rows)==9545 and {j['id'] for j in rows}==set(owners)
 assert set(gate['other_seventeen_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 rel=deps['actual_normal_related_rows'];assert len(rel)==2 and sum(j['size'] for j in rel)==10055 and deps['related_extra_done']==gate['related_extra_done']==0
 assert set(gate['related_ids_not_primary'])=={j['id'] for j in rel} and not ({j['id'] for j in rel}&set(owners))
 for j in rows+rel:
  p=stage/j['target_path'];b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256'] and b==Path(j['local_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob']
  cap=stage/j['acquisition_target'];assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes();cj=read(cap);assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  assert j['full_file_read'] and j['current_source_imports']==j['current_source_runs']==0
  if j['primary']:
   o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
 assert len(deps['packet_reuse_rows'])==2 and deps['missing_runtime_inputs']==[] and not deps['replay_layout_prepared']
 for j in deps['packet_reuse_rows']:
  p=repo/j['published_path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'] and j['exact_published_bytes_reused'] and not j['current_new_show']
 comps=read(ev/'comparison-bindings.json')['full_formal_objects_read'];assert len(comps)==8
 for j in comps:
  p=repo/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']
 rf=read(ev/'report-field-binding.json');audit=read(stage/next(j['target_path'] for j in rows if j['id']=='fe8dd6d9ec7d7e4eae7f'));transport=read(stage/next(j['target_path'] for j in rel if j['id']=='ddf81da1443ff966461e'))
 assert rf['primary_full_report']==audit and rf['related_transport_full_report']==transport and not rf['arithmetic_recomputed']
 assert len(audit)==24 and len(audit['optimizer_L'])==11 and len(audit['C_by_role'])==6 and audit['source_sha256']=='a0c796fa2ec4f4c442db0662f2ebfd8046230a7f4e7fc013827c9ad49433e831'
 assert len(transport)==23 and len(transport['role_queries'])==6 and all(len(j)==5 for j in transport['role_queries']) and len(transport['dual_alpha'])==6 and len(transport['dual_beta'])==30
 order=read(ev/'source-report-order-binding.json');assert order['original_report_top_level_order']==list(audit) and set(order['producer_declared_top_level_order'])==set(audit) and order['producer_declared_top_level_order']!=list(audit)
 assert order['code_key_index']==20 and order['report_key_index']==23 and not order['source_or_report_modified'] and not order['producer_rerun']
 code=(stage/next(j['target_path'] for j in rows if j['id']=='f343208cf29eefced8dc')).read_text();assert code.index('unique_primal_minimax_load=')<code.index('shared_load_cap=')
 receipts=read(ws/'semantic-receipts.json');assert {j['id'] for j in receipts}==set(owners)
 for j in receipts:
  assert j['full_file_reviewed'] and j['related_material_checked'] and j['unique_content_accounted_for'] and j['root_claim_local_sync']=='synced'
  assert j['current_original_mathematical_entries']==j['current_new_mathematical_entries']==0
  for rp in j['targets']:assert resolve(Path(rp)).is_file(),rp
 links=0;ids=[]
 for p in stage.rglob('*.md'):
  if '/original/' in str(p) or '/related-original/' in str(p):continue
  t=p.read_text()
  if '/state/' in str(p):
   assert t.startswith('---\n');front=t.split('---',2)[1]
   for k in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+k+':',front,re.M),(p,k)
   ids.append(re.search(r'^id:\s*(.+)$',front,re.M).group(1))
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
   if target.startswith(('https:','http:','#')):continue
   q=(p.parent/target.split('#')[0]).resolve();r=q.relative_to(stage);assert resolve(r).is_file(),(p,target);links+=1
 assert len(ids)==len(set(ids))==2
 actual=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file());assert sorted(read(ws/'copy-files.json'))==actual
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=3,primary_bytes=9545,related_files=2,related_bytes=10055,related_extra_done=0,reused_published_packet_files=2,missing_runtime_inputs=0,formal_objects=2,semantic_receipts=3,comparison_full_objects=8,full_assignment_topics=30,dual_beta_entries=30,source_report_insertion_order_difference_preserved=True,arithmetic_recomputed=False,markdown_links=links,copy_files=len(actual),raw_claim_sync='synced-actual20XH',source_imports=0,CLI_runs=0,Hungarian_runs=0,Fraction_verification_runs=0,IC_replays=0,menu_replays=0,new_mathematical_program_runs=0,note='Hashes/blob/owner/captures/fullJSONliterals/order/links only. No original producer/reviewer rerun or mathematical program executed.')
 (ev/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
