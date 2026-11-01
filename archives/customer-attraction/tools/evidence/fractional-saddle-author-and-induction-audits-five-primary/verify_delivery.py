"""Hash/blob/metadata/JSON literal/link checks only; no mathematical sources or Fraction run."""
from pathlib import Path
import json,hashlib,re,sys

def main():
 stage=Path(sys.argv[1]).resolve();repo=Path(sys.argv[2]).resolve();ev=stage/'archives/customer-attraction/tools/evidence/fractional-saddle-author-and-induction-audits-five-primary';ws=stage/'cleanup/workspaces/Boss4/r3-fractional-saddle-author-and-induction-audits-five-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();resolve=lambda p:stage/p if (stage/p).is_file() else repo/p
 for j in read(ev/'content-manifest.json')['files']:
  p=stage/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 raw=read(ev/'root-actual-claim9-receipt.json');gate=read(ev/'ownership-gate.json');rows=read(ev/'source-manifest.json')['rows'];owners={j['id']:j for j in gate['owner_records']}
 assert raw['status']=='pushed' and raw['actor']=='Boss4' and len(raw['ids'])==9 and raw['remote_tip']==gate['remote_tip']=='413fb760a46bc7476f514dd55bcec041cc4db103'
 assert raw['local_sync']['status']=='synced' and raw['local_sync']==gate['raw_local_sync_unmodified'] and gate['claim_local_sync']=='synced'
 assert len(rows)==5 and sum(j['size'] for j in rows)==15714 and {j['id'] for j in rows}==set(owners)
 assert set(gate['other_four_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 for j in rows:
  p=stage/j['target_path'];b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256'] and b==Path(j['local_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob']
  cap=stage/j['acquisition_target'];assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes();cj=read(cap);assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  assert j['full_file_read'] and j['current_source_imports']==j['current_source_runs']==0
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
 comps=read(ev/'comparison-bindings.json')['full_formal_objects_read'];assert len(comps)==16
 for j in comps:
  p=repo/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']
 rf=read(ev/'report-field-binding.json');author=read(stage/next(j['target_path'] for j in rows if j['id']=='2ce90089cd388ff878da'));ind=read(stage/next(j['target_path'] for j in rows if j['id']=='0a5d543ca262cd481791'))
 assert rf['author_full_report']==author and rf['induction_full_report']==ind and not rf['arithmetic_recomputed']
 assert len(author)==12 and len(author['parameters'])==8 and len(author['checks'])==15 and all(v is True for v in author['checks'].values())
 assert len(ind)==14 and len(ind['parameters'])==7 and len(ind['checks'])==15 and all(v is True for v in ind['checks'].values()) and ind['author_audit_imported'] is False
 assert len(ind['plateau_load_checks'])==4 and [j['real_prefix_copies'] for j in ind['plateau_load_checks']]==[0,1,2,3]
 for j in ind['plateau_load_checks']:
  assert len(j)==11 and all(j[k] is True for k in ['mixture_probability_legal','enough_distinct_outside_blocks','total_real_mass_exact','all_real_loads_match_L'])
 assert all(author[a]==ind[b] for a,b in rf['common_literal_field_map']) and author['theta']==ind['plateau_load_checks'][1]['theta']
 deps=read(ev/'dependency-bindings.json');assert deps['runtime_input_files']==deps['external_code_imports']==[] and deps['related_extra_done']==deps['current_original_imports']==deps['current_original_runs']==0 and not deps['producer_outputs_recreated']
 receipts=read(ws/'semantic-receipts.json');assert {j['id'] for j in receipts}==set(owners)
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
   q=(p.parent/target.split('#')[0]).resolve();rel=q.relative_to(stage);assert resolve(rel).is_file(),(p,target);links+=1
 assert len(ids)==len(set(ids))==1
 actual=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file());assert sorted(read(ws/'copy-files.json'))==actual
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=5,primary_bytes=15714,formal_objects=1,semantic_receipts=5,comparison_full_objects=16,author_original_declared_checks=15,induction_original_declared_checks=15,induction_full_rows=4,common_literal_fields_equal=True,arithmetic_recomputed=False,markdown_links=links,copy_files=len(actual),raw_claim_sync='synced-actual-new9XB',source_imports=0,CLI_runs=0,LP_runs=0,IC_replays=0,new_mathematical_program_runs=0,note='Metadata/whole-file hashes/blob/owner/normal capture/literal report fields/links only. Original true flags not independently recomputed; no original program or Fraction verification executed.')
 (ev/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
