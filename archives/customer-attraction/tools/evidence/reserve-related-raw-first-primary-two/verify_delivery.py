"""Hashes/old full-read bindings/normal captures/owner/publication/links only; never parse original raw packets."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 s=Path(sys.argv[1]).resolve();r=Path(sys.argv[2]).resolve()
 e=s/'archives/customer-attraction/tools/evidence/reserve-related-raw-first-primary-two';w=s/'cleanup/workspaces/Boss4/r3-reserve-related-raw-first-primary-two'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 pending=read(e/'pending-diag4-prerequisite.json');forwards={j['target_path']:Path(j['frozen_path']) for j in pending['original_rows']}
 resolve=lambda p:s/p if (s/p).is_file() else (r/p if (r/p).is_file() else forwards.get(str(p),r/p))
 for j in read(e/'content-manifest.json')['files']:
  p=s/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 raw=read(e/'root-actual-claim12-receipt.json');gate=read(e/'ownership-gate.json');proof=read(e/'independent-sync-preservation.json')
 assert (raw['actor'],raw['status'],len(raw['ids']),raw['remote_tip'])==('Boss4','pushed',12,'3d6d8f7832584460e2654c53ca6ca6d7bc446e04')
 assert raw['local_sync']['status']==gate['claim_local_sync']=='needs-attention' and raw['local_sync']==gate['raw_local_sync_unmodified']
 assert proof['untracked_count']==1 and proof['tracked']==[] and not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept']
 assert proof['stash']==gate['independent_proof']['stash']=='1e02ed40671d211709351e725373e4c3185803e3'
 src=read(e/'source-manifest.json');rows=src['rows'];owners={j['id']:j for j in gate['owner_records']}
 assert len(rows)==2 and sum(j['size'] for j in rows)==12534 and set(owners)=={j['id'] for j in rows}
 assert set(gate['other_ten_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 assert src['first_primary_only'] and src['previous_related_extra_done']==src['new_raw_copies']==src['new_normal_show_runs']==src['current_source_body_reads']==src['original_program_imports']==src['original_program_runs']==src['new_mathematical_program_runs']==0
 for j in rows:
  p=Path(j['prior_frozen_path']);b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256'] and b==Path(j['local_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob']
  cap=s/j['acquisition_target'];cj=read(cap);assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes()
  assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  assert j['exact_prior_normal_show_reused'] and j['no_new_normal_show_for_this_source'] and j['primary_first_time'] and not j['new_raw_copy'] and j['previous_related_done']==j['current_normal_show_runs']==j['current_source_body_reads']==j['current_original_runs']==0
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
 pf=read(e/'packet-field-routing.json');assert len(pf['rows'])==2 and pf['total_original_top_fields']==30 and pf['total_original_policy_actions']==74 and pf['new_raw_body_reads']==pf['new_original_JSON_parses']==0 and not pf['new_mathematical_program_computation']
 assert sorted(j['original_field_count'] for j in pf['rows'])==[9,21] and sorted(j['policy_action_rows'] for j in pf['rows'])==[31,43]
 for j in pf['rows']:
  old=read(Path(j['field_inventory_provider']));q=next(x for x in old['rows'] if x['id']==j['id']);assert q['full_file_read'] and q['all_original_top_fields']==j['original_top_fields'] and q['policy_action_rows']==j['policy_action_rows']
  assert j['all_prior_full_read'] and j['original_body_not_parsed_or_read_again']
 assert not pf['raw817']['fractional_sum_full_definition_present_in_packet'] and not pf['raw817']['new_proof_of_199over60'] and pf['raw817']['claimed_fractional_sum_minus_W']=='199/60'
 assert pf['raw35']['reported_COPY2_gap']==pf['raw35']['reported_wholeprofit_ratio2_gap']=='2' and not pf['raw35']['prefix_request_cap2_refuted'] and not pf['raw35']['half_refuted']
 assert pending['original_single_copies']==2 and pending['new_original_copies']==0 and not pending['source_done_inferred'] and pending['prior_frozen_package_unchanged']
 assert len(pending['formal_bodies'])==1
 for j in pending['formal_bodies']:
  p=Path(j['frozen_path']);assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'] and j['publication_status'].startswith('pending') and j['remote_math_tip'] is None
 pub=read(e/'reserve3-actual-publication-binding.json');xc=read(e/'actual-reserve3-math-checkpoint9XZ.json');xd=read(e/'actual-reserve3-source-done9XZ.json')
 assert xc['status']=='pushed' and xc['remote_tip']==pub['actual_math_remote_tip']=='0d2ae3adb75a6cd1d3cf34f45b7f8153ca65febd'
 assert xd['status']=='pushed' and xd['remote_tip']==pub['actual_done_remote_tip']=='b60b8fef4bd14c53b48a8e844beadf5708d6dc56'
 assert set(pub['actual_done_ids'])=={'8339b3d5f05b29cf3d2d','a4eefef15437061fe434','7812a260f3916e0ff62b'}<=set(xd['ids'])
 assert not pub['current_reserve3_pending'] and pub['prior_frozen_diag4_pending_is_historical'] and pub['prior_package_unmodified'] and pub['no_current2_done_inferred']
 assert len(pub['published_formal_bodies'])==2
 for j in pub['published_formal_bodies']:
  p=r/j['path'];a=next(z['asset'] for z in xc['assets'] if z['asset']['path']==j['path']);assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']==a['sha256'] and a==j['actual_asset'] and a['commit']==xc['remote_tip']
 cb=read(e/'comparison-bindings.json');assert len(cb['full_formal_objects_read'])==8 and cb['current_new_full_formal_reads']==0 and cb['sameSHA_prior_full_formal_reads_reused']==8
 for j in cb['full_formal_objects_read']+[cb['status_only_half5_reference']]:
  p=r/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 assert not cb['status_only_half5_reference']['full_file_read_in_this_batch'] and cb['new_original_body_reads']==cb['new_shows']==cb['new_original_runs']==0
 receipts=read(w/'semantic-receipts.json');assert len(receipts)==2 and {j['id'] for j in receipts}==set(owners) and all(j['disposition']=='retained' for j in receipts)
 for j in receipts:
  assert j['full_file_reviewed'] and j['related_material_checked'] and j['unique_content_accounted_for'] and j['prior_full_read_exact_reuse'] and j['root_claim_local_sync']=='needs-attention'
  assert j['previous_related_done']==j['current_normal_show_runs']==j['current_source_body_reads']==j['current_original_mathematical_entries']==j['current_new_mathematical_entries']==0
  for rp in j['targets']:assert resolve(Path(rp)).is_file(),rp
 links=0;ids=[]
 for p in s.rglob('*.md'):
  t=p.read_text()
  if '/state/' in str(p):
   assert t.startswith('---\n');front=t.split('---',2)[1]
   for k in ('id','kind','type_tag','title','status','summary','source_refs'):assert re.search('^'+k+':',front,re.M),(p,k)
   ids.append(re.search(r'^id:\s*(.+)$',front,re.M).group(1))
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
   if target.startswith(('http:','https:','#')):continue
   q=(p.parent/target.split('#')[0]).resolve();rp=q.relative_to(s);assert resolve(rp).is_file(),(p,target);links+=1
 assert len(ids)==len(set(ids))==1
 actual=sorted(str(p.relative_to(s)) for p in s.rglob('*') if p.is_file());assert sorted(read(w/'copy-files.json'))==actual
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=2,primary_bytes=12534,first_primary_exact_prior_related_reuses=2,previous_related_done=0,new_raw_copies=0,new_normal_show_runs=0,new_original_body_reads=0,new_original_JSON_parses=0,formal_objects=1,semantic_receipts=2,prior_full_formal_sameSHA_reuses=8,original_top_fields_retained=30,original_policy_action_rows_retained=74,pending_diag4_formal_objects=1,pending_diag4_originals=2,reserve3_actual_math_tip=xc['remote_tip'],reserve3_actual_done_tip=xd['remote_tip'],prior_frozen_pending_notes_unmodified=True,current_source_done_inferred=False,raw_local_sync='needs-attention-unmodified',independent_preservation='1untracked same, trackedempty, no missing/different/unmerged, stashkept',markdown_links=links,copy_files=len(actual),source_imports=0,CLI_runs=0,Fraction_verification_runs=0,LP_runs=0,BI_runs=0,IC_replays=0,menu_replays=0,new_mathematical_program_runs=0,note='Only hash/blob/priorfullread/fieldinventory/normalcapture/owner/publicationasset/links; original raw JSON bodies neverparsed orreviewedagain; no original mathematical program or newnumericcertification.')
 (e/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
