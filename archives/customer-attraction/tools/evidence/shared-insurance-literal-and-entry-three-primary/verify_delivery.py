"""Hash/blob/whole-file provenance/JSON literal/link checks only, no literal audit or Fraction run."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 stage=Path(sys.argv[1]).resolve();repo=Path(sys.argv[2]).resolve();ev=stage/'archives/customer-attraction/tools/evidence/shared-insurance-literal-and-entry-three-primary';ws=stage/'cleanup/workspaces/Boss4/r3-shared-insurance-literal-and-entry-three-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();resolve=lambda p:stage/p if (stage/p).is_file() else repo/p
 for j in read(ev/'content-manifest.json')['files']:
  p=stage/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 raw=read(ev/'root-actual-claim19-receipt.json');gate=read(ev/'ownership-gate.json');rows=read(ev/'source-manifest.json')['rows'];owners={j['id']:j for j in gate['owner_records']}
 assert raw['actor']=='Boss4' and raw['status']=='pushed' and len(raw['ids'])==19 and raw['remote_tip']==gate['remote_tip']=='05a331e2e536aec72f2c75095d00992d1c26ac11'
 assert raw['local_sync']['status']=='synced' and raw['local_sync']==gate['raw_local_sync_unmodified'] and gate['claim_local_sync']=='synced'
 assert len(rows)==3 and sum(j['size'] for j in rows)==8283 and {j['id'] for j in rows}==set(owners)
 assert set(gate['other_sixteen_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 for j in rows:
  p=stage/j['target_path'];b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256'] and b==Path(j['local_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob']
  cap=stage/j['acquisition_target'];assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes();cj=read(cap);assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  assert j['full_file_read'] and j['current_source_imports']==j['current_source_runs']==0
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
 inp=read(ev/'runtime-input-bindings.json');assert inp['required_external_files']==2 and inp['missing_runtime_inputs']==[] and inp['external_code_modules']==[] and not inp['NumPy'] and not inp['replay_layout_prepared']
 packets={}
 for j in inp['packet_rows']:
  p=repo/j['published_path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'] and not j['current_new_show'] and not j['new_raw_copy']
  packets[j['filename']]=read(p)
 rf=read(ev/'report-field-binding.json');report=read(stage/next(j['target_path'] for j in rows if j['id']=='6b4d9484c18db7cce971'));assert rf['full_original_report']==report and not rf['arithmetic_recomputed']
 assert list(report)==['scope','all_actual_prefix_IC','reports'] and report['all_actual_prefix_IC'] is True and len(report['reports'])==2
 for row in report['reports']:
  assert list(row)==['input','KKT','F','C','D','IC','balance','saddle'] and row['KKT'] is True
  pkt=packets[row['input']];assert all(row[a]==pkt[b] for a,b in [('F','F_optimum'),('C','C'),('D','D'),('IC','IC'),('balance','W_minus_mF')])
 assert report['reports'][0]['saddle'] is False and report['reports'][1]['saddle'] is True
 comps=read(ev/'comparison-bindings.json')['full_formal_objects_read'];assert len(comps)==9
 for j in comps:
  p=repo/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']
 receipts=read(ws/'semantic-receipts.json');assert {j['id'] for j in receipts}==set(owners) and sorted(j['disposition'] for j in receipts)==['integrated','retained','retained']
 for j in receipts:
  assert j['full_file_reviewed'] and j['related_material_checked'] and j['unique_content_accounted_for'] and j['root_claim_local_sync']=='synced'
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
   q=(p.parent/target.split('#')[0]).resolve();r=q.relative_to(stage);assert resolve(r).is_file(),(p,target);links+=1
 assert len(ids)==len(set(ids))==1
 actual=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file());assert sorted(read(ws/'copy-files.json'))==actual
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=3,primary_bytes=8283,formal_objects=1,semantic_receipts=3,comparison_full_objects=9,reused_published_input_files=2,missing_runtime_inputs=0,whole_report_top_fields=3,full_cases=2,uniform_case_saddle=False,active_case_saddle=True,arithmetic_recomputed=False,markdown_links=links,copy_files=len(actual),raw_claim_sync='actual-new19XN-synced',source_imports=0,CLI_runs=0,Fraction_verification_runs=0,LP_runs=0,IC_replays=0,menu_replays=0,new_mathematical_program_runs=0,note='Metadata/hash/blob/normalcapture/owner/JSONliteral/inputhash/links only. Original literal audit not imported or rerun, no new mathematical certification.')
 (ev/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
