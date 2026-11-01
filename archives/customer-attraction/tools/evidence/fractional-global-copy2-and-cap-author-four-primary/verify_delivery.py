"""Hash/blob/capture/prior-read/owner/publication/literal/link structure only; no original math program."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 s=Path(sys.argv[1]).resolve();r=Path(sys.argv[2]).resolve()
 e=s/'archives/customer-attraction/tools/evidence/fractional-global-copy2-and-cap-author-four-primary';w=s/'cleanup/workspaces/Boss4/r3-fractional-global-copy2-and-cap-author-four-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 resolve=lambda p:s/p if (s/p).is_file() else r/p
 for j in read(e/'content-manifest.json')['files']:
  p=s/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 raw=read(e/'root-actual-claim19-receipt.json');gate=read(e/'ownership-gate.json');proof=read(e/'independent-sync-preservation.json')
 assert (raw['actor'],raw['status'],len(raw['ids']),raw['remote_tip'])==('Boss4','pushed',19,'131a993158ac3fccb33fdc3253bfa6541b725bff')
 assert raw['local_sync']['status']==gate['claim_local_sync']=='needs-attention' and raw['local_sync']==gate['raw_local_sync_unmodified']
 assert proof['untracked_count']==1 and proof['tracked']==[] and not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept'] and proof['stash']==gate['independent_proof']['stash']=='c94434efbbbdde7d6b0cf440ee010ebc4760be70'
 src=read(e/'source-manifest.json');rows=src['rows'];owners={j['id']:j for j in gate['owner_records']}
 assert len(rows)==4 and sum(j['size'] for j in rows)==19140 and set(owners)=={j['id'] for j in rows}
 assert set(gate['other_fifteen_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 assert src['first_primary_exact_prior_related_reuses']==4 and src['previous_related_extra_done']==src['current_primary_normal_show_runs']==src['current_primary_source_body_reads']==src['current_original_program_imports']==src['current_original_program_runs']==src['new_mathematical_program_runs']==0
 for j in rows:
  p=s/j['target_path'];bb=p.read_bytes();assert len(bb)==j['size'] and sha(p)==j['sha256'] and bb==Path(j['local_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest()==j['blob']
  cap=s/j['acquisition_target'];cj=read(cap);assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes() and cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  assert j['exact_prior_normal_show_reused'] and j['no_new_normal_show_for_this_source'] and j['primary_first_time'] and j['previous_related_done']==j['current_normal_show_runs']==j['current_source_body_reads']==j['current_original_runs']==0
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
 rev=read(e/'necessary-review-related-binding.json');assert len(rev['rows'])==1 and rev['related_bytes']==5068 and rev['current_new_related_normal_show_calls']==rev['current_new_related_full_MD_reads']==1 and rev['current_extra_related_done']==0
 for j in rev['rows']:
  p=s/j['target_path'];bb=p.read_bytes();assert len(bb)==j['size']==5068 and sha(p)==j['sha256'] and hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest()==j['blob']
  cap=s/j['acquisition_target'];cj=read(cap);assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes() and cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256']
  assert j['full_file_read'] and j['current_full_read'] and j['current_normal_show_exit_code']==0 and not j['current_claim'] and not j['current_done']
 pub=read(e/'actual-diag4-and-raw-input-bindings.json');xc=read(e/'actual-diag4-math-checkpoint8YH.json');xd=read(e/'actual-diag4-source-done8YH.json')
 assert xc['status']=='pushed' and xc['remote_tip']==pub['actual_math_remote_tip']=='32f586b7cb13b85c9c3386a93e3f530879162937'
 assert xd['status']=='pushed' and xd['remote_tip']==pub['actual_done_remote_tip']=='4184b293441e7839088b89d70187709376b0ab72'
 assert set(pub['actual_done_ids'])=={'5b30a9cde6593ee61594','fa1c3c1d21076f265f1a','ff814d0018231ae46dd7','4949b0a89b1d6ca3b0fd'}<=set(xd['ids'])
 assert len(pub['published_diag4_formal_bodies'])==1 and len(pub['published_raw_originals'])==2 and pub['published_raw_bytes']==12534
 for j in pub['published_diag4_formal_bodies']:
  p=r/j['path'];a=next(z['asset'] for z in xc['assets'] if z['asset']['path']==j['path']);assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256']==a['sha256'] and a==j['actual_asset'] and a['commit']==xc['remote_tip']
 for j in pub['published_raw_originals']:
  p=r/j['published_path'];bb=p.read_bytes();a=next(z['asset'] for z in xc['assets'] if z['asset']['path']==j['published_path']);assert len(bb)==j['size'] and sha(p)==j['sha256']==a['sha256'] and a==j['actual_asset'] and a['commit']==xc['remote_tip']
  assert hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest()==j['blob'] and j['prior_full_read'] and not j['current_new_read_or_show'] and not j['new_raw_copy'] and j['original_JSON_body_not_parsed_again'] and not j['source_done_inferred']
 assert pub['current_new_raw_copies']==pub['current_new_raw_reads_or_shows']==0 and not pub['current_raw2_source_done_inferred'] and not pub['current_diag4_pending'] and pub['old_frozen_pending_notes_unchanged']
 cb=read(e/'comparison-bindings.json');assert len(cb['full_formal_objects_read'])==10 and cb['current_full_formal_reads']==4 and cb['sameSHA_prior_full_formal_reads_reused']==6
 for j in cb['full_formal_objects_read']+[cb['status_only_half5_reference']]:
  p=r/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 assert not cb['status_only_half5_reference']['full_file_read_in_this_batch']
 m=read(e/'mathematical-contracts.json');f=m['FG'];assert len(f['rows'])==3 and all(len(z)==7 for z in f['rows']) and f['sum_F']=='36019/60' and f['gap']=='199/60' and f['actual_W']==597 and f['reported_OPT3']==710 and not f['current_numeric_program_run']
 assert m['security']['badp_dual_upper']=='275/2' and m['security']['free_value_lower']=='142' and m['security']['strict_badp_optimality_gap_at_least']=='9/2'
 assert not any(m['security'][k] for k in ('p_optimal_for_t_or_v','safety_aggregate_refuted','half_refuted','R11_shared_minK_refuted_by_fixed_mean_failure'))
 assert not m['COPY2']['PCAP_or_half_refuted'] and not m['PCAP']['general_PCAPPAY_proved'] and not m['PCAP']['half_sufficiency_proved']
 scope=read(e/'original-review-and-evidence-scope.json');assert scope['primary_MD_files']==4 and scope['primary_MD_bytes']==19140 and scope['primary_current_body_rereads']==scope['primary_current_new_normal_shows']==0 and scope['necessary_related_MD_bytes']==5068
 assert scope['FG_original_report']['comparisons_including_self']==258 and scope['FG_original_report']['strict']==169 and scope['FG_original_report']['ties']==89 and scope['FG_original_report']['these_are_prior_MD_reports_not_current_run']
 assert scope['PCAP_old_named_pressure']['count']==11 and len(scope['PCAP_old_named_pressure']['names'])==11 and not scope['PCAP_old_named_pressure']['code_JSON_inputs_currently_read'] and not scope['PCAP_old_named_pressure']['current_run']
 receipts=read(w/'semantic-receipts.json');assert len(receipts)==4 and {j['id'] for j in receipts}==set(owners) and sorted(j['disposition'] for j in receipts)==['integrated']*3+['retained']
 for j in receipts:
  assert j['full_file_reviewed'] and j['related_material_checked'] and j['unique_content_accounted_for'] and j['prior_full_read_exact_reuse'] and j['root_claim_local_sync']=='needs-attention'
  assert j['previous_related_done']==j['current_normal_show_runs']==j['current_source_body_reads']==j['current_original_mathematical_entries']==j['current_new_mathematical_entries']==0
  for rp in j['targets']:assert resolve(Path(rp)).is_file(),rp
 links=0;ids=[]
 for p in s.rglob('*.md'):
  if '/original/' in str(p) or '/related-original/' in str(p):continue
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
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=4,primary_bytes=19140,firstprimary_prior_actual_fullread_reuses=4,new_primary_body_reads=0,new_primary_shows=0,formal_objects=2,semantic_receipts=4,new_necessary_related_MD_files=1,new_necessary_related_MD_bytes=5068,new_necessary_related_readonly_normal_shows=1,extra_related_done=0,already_published_raw_reuses=2,already_published_raw_bytes=12534,new_raw_packet_reads_or_shows_or_copies=0,comparison_full_objects=10,current_full_formal_reads=4,prior_sameSHA_full_formal_reuses=6,diag4_actual_math_tip=xc['remote_tip'],diag4_actual_done_tip=xd['remote_tip'],raw2_primary_resource_status='pending12YL perRootlatesttask; publishedrawbytes notsourcedone',old_frozen_pending_notes_unmodified=True,raw_local_sync='needs-attention-unmodified',independent_preservation='1untracked same; trackedempty; no missing/different/unmerged; stashkept',markdown_links=links,copy_files=len(actual),source_imports=0,CLI_runs=0,Fraction_verification_runs=0,LP_runs=0,BI_runs=0,IC_replays=0,menu_replays=0,new_mathematical_program_runs=0,note='Only metadata/hash/blob/normalcapture/priorfullread/owner/publicationassets/literal/links. Original raw bodies not parsedagain; no originalprogram or numerical/SPE/LP/Jensen audit run and no new numerical certification.')
 (e/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
