"""Metadata/file checks only; no source import, execution or mathematical recomputation."""
from pathlib import Path
import json,hashlib,sys,re

def main():
 stage=Path(sys.argv[1]).resolve();repo=Path(sys.argv[2]).resolve();ev=stage/'archives/customer-attraction/tools/evidence/shared-load-originals-primary-dispositions';ws=stage/'cleanup/workspaces/Boss4/r3-shared-load-originals-primary-dispositions'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 for r in read(ev/'content-manifest.json')['files']:
  p=stage/r['path'];assert p.is_file() and p.stat().st_size==r['size'] and sha(p)==r['sha256'],r['path']
 raw=read(ev/'root-actual-claim22-receipt.json');gate=read(ev/'ownership-gate.json');rows=read(ev/'source-manifest.json')['rows'];owners={j['id']:j for j in gate['owner_records']}
 assert raw['actor']=='Boss4' and raw['status']=='pushed' and len(raw['ids'])==22 and raw['remote_tip']==gate['remote_tip']=='e41ac6c6d77bfd5fb71d1e8b10a30eedf56c47d3'
 assert raw['local_sync']['status']=='synced' and raw['local_sync']==gate['raw_local_sync_unmodified']
 assert len(rows)==2 and sum(r['size'] for r in rows)==16384 and {j['id'] for j in rows}==set(owners)
 assert set(gate['other_twenty_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 deps=read(ev/'same-batch-dependencies.json');targets={j['path']:j for j in deps['rows']};published=0
 for j in deps['rows']:
  f=Path(j['prior_frozen_path']);assert f.is_file() and sha(f)==j['sha256'] and f.stat().st_size==j['size']
  p=repo/j['path']
  if p.is_file():assert p.read_bytes()==f.read_bytes(),j['path'];published+=1
 def resolve(rel):
  p=stage/rel
  if p.is_file():return p
  p=repo/rel
  if p.is_file():return p
  assert rel in targets,rel
  return Path(targets[rel]['prior_frozen_path'])
 for j in rows:
  p=resolve(j['target_path']);b=p.read_bytes();assert sha(p)==j['sha256'] and len(b)==j['size']
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob'] and b==Path(j['local_path']).read_bytes()
  cap=stage/j['acquisition_target'];assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes();cj=read(cap);assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  assert j['exact_prior_normal_show_reused'] and j['no_new_normal_show_for_this_source'] and j['current_normal_show_runs']==j['current_original_runs']==j['previous_related_done']==0 and j['primary_first_time']
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
 receipts=read(ws/'semantic-receipts.json');assert {j['id'] for j in receipts}==set(owners)
 for j in receipts:
  assert j['full_file_reviewed'] and j['related_material_checked'] and j['unique_content_accounted_for'] and j['disposition']=='duplicate'
  assert j['current_original_mathematical_entries']==j['current_new_mathematical_entries']==j['current_normal_show_runs']==0
  for p in j['targets']:assert resolve(p).is_file(),p
 links=0
 for p in stage.rglob('*.md'):
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
   if target.startswith(('https:','http:','#')):continue
   q=(p.parent/target.split('#')[0]).resolve();rel=str(q.relative_to(stage));assert resolve(rel).is_file(),(p,target);links+=1
 actual=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file());assert sorted(read(ws/'copy-files.json'))==actual
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=2,primary_bytes=16384,semantic_receipts=2,dispositions='duplicate',new_formal_objects=0,new_raw_copies=0,same_batch_dependencies=len(targets),dependency_targets_published_live=published,publication_pending_live=published<len(targets),root_actual_mathematical_tip_receipt=None,dependency_note='Root-authorized ordered same-batch dependencies checked against frozen R11 bytes; publication is separately Root responsibility before checkpoint/done.',markdown_links=links,copy_files=len(actual),current_full_source_rereads=0,new_normal_shows=0,source_imports=0,CLI_runs=0,LP_runs=0,IC_replays=0,menu_enumerations=0,new_mathematical_program_runs=0)
 (ev/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
