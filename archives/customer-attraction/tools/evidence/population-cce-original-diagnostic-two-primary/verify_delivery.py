"""Source-byte and prior full-read reuse integrity, literal report and integer record domain only. No original import, Fraction, paths, profile enumeration, LP or CCE residual/probability arithmetic."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-population-cce-original-diagnostic-two-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(p):
 b=p.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
m=read(E/'actual-source-manifest.json');rows=m['rows'];ids={x['id'] for x in rows};assert len(rows)==2 and sum(x['size'] for x in rows)==16539
c=read(E/'authoritative-full-claim.json');assert c['status']=='pushed' and c['operation']=='claim' and c['actor']=='Boss4' and len(c['ids'])==16 and ids<=set(c['ids'])
assert c['remote_tip']=='9f40d76914d79901dfe630474f1f2448653ce815' and c['local_sync']['status']=='needs-attention' and c['local_sync']==m['raw_original_local_sync']
proof=read(E/'claim-sync-preservation.json');assert proof['untracked_count']==2 and len(proof['tracked'])==2 and all(x['same'] is True for x in proof['tracked'])
assert proof['missing']==[] and proof['different']==[] and proof['unmerged']=='' and proof['stash_kept'] is True and proof['stash']=='77db1fe5a8c3d099722e4d690877dba29daaa606'
for x in rows:
 p=S/x['stage_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['local_path']).read_bytes() and x['full_file_reviewed'] is True and x['new_normal_show'] is True
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name);assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')} and cap['output']==x['local_path']
 owner=read(E/'local-progress-at-read'/(x['id']+'.json'));assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==x['sha256']
assert (S/rows[0]['stage_path']).parents[5]==E/'original'
runtime=read(E/'runtime-directory-manifest.json');deps=runtime['files'];assert len(deps)==51
assert sum(x['full_file_reviewed'] for x in deps)==18 and sum(x['size'] for x in deps if x['full_file_reviewed'])==1469006 and sum(x['selection_structure_only'] for x in deps)==33
for x in deps:
 p=S/x['snapshot'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['new_primary'] is False and x['new_done'] is False
 assert x['review_mode'] in ['previous-full-read-exact-byte-reuse','previous-directory-filter-structure-and-bytes-only']
prev=read(E/'prior-input-structure-selfcheck.json');assert prev['status']=='PASS' and prev['full_read_action_rows']==12222 and prev['full_read_input_certificate_bytes']==1469006 and prev['SPE_IC_runs']==0 and prev['end_path_replays']==0 and prev['H_recomputations']==0
vs=read(E/'dependency-reuse-manifest.json');assert len(vs)==9
viewdata={}
for x in vs:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['previous_full_file_reviewed'] is True and x['current_math_replay'] is False
 viewdata[x['instance']]=read(p)
prior_e=Path(runtime['source_manifest']).parent
assert (E/'dependency-full-reading.txt').read_bytes()==(prior_e/'dependency-full-reading.txt').read_bytes()
cm=read(E/'formal-comparison.json');assert len(cm)==8
for x in cm:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True
md=read(E/'related-MD-manifest.json');assert len(md)==2 and sum(x['size'] for x in md)==8166
for x in md:
 p=S/x['snapshot'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True and x['new_primary'] is False and x['new_done'] is False
report=read(S/rows[1]['stage_path']);assert read(E/'stored-report-literal-transcription.json')==report and list(report)==['status','claim','rows'] and len(report['rows'])==9
assert report['status']=='finite floating LP diagnostic only' and report['claim']=='min CCE_(m+1) W/(m+1) <= SPE_m W/m'
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1;page=math[0].read_text();assert 'status="'+report['status']+'"' in page and 'claim="'+report['claim']+'"' in page
names=[x['instance'] for x in report['rows']];assert names==[x['instance'] for x in vs] and names==sorted(x['instance'] for x in read(E/'prior-directory-selection-structure.json')['rows'] if x['selected'])
keys=['instance','players','new_players','SPE_W','SPE_average','profiles','CCE_min_average_float','claim_gap_float'];support_count=0
assert [len(x['support']) for x in report['rows']]==[6,3,6,5,5,7,8,6,5]
assert [x['profiles'] for x in report['rows']]==[126,35,5005,252,126,126,462,126,252] and sum(x['profiles'] for x in report['rows'])==6510
for x in report['rows']:
 assert list(x)==keys+['support'] and x['new_players']==x['players']+1 and x['players']==viewdata[x['instance']]['input']['players']
 k=len(viewdata[x['instance']]['input']['topics']);assert 0<x['profiles']<=15000
 assert '|'+ '|'.join(str(x[q]) for q in keys)+'|'+str(len(x['support']))+'|' in page
 sec=page.split('### '+x['instance'],1)[1].split('\n### ',1)[0]
 for i,z in enumerate(x['support'],1):
  assert list(z)==['counts','probability_float','W'] and len(z['counts'])==k and all(type(q) is int and q>=0 for q in z['counts']) and sum(z['counts'])==x['new_players']
  assert type(z['probability_float']) is float and type(z['W']) is int
  assert '|'+str(i)+'|`'+json.dumps(z['counts'],separators=(',',':'))+'`|'+str(z['probability_float'])+'|'+str(z['W'])+'|' in sec
  support_count+=1
assert support_count==51
sc=read(E/'execution-and-domain-boundaries.json');assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_SPE_IC_runs','current_actual_path_replays','current_H_recomputations','current_count_profile_enumerations','current_LP_runs','current_exact_CCE_checks','current_probability_rationalizations','current_solver_runs','new_mathematical_implementation_runs'))
assert sc['historical_execution_manifest_present'] is False and sc['all_report_fields_transcribed'] is True and sc['support_renormalized_in_original'] is False and sc['original_rechecks_CCE_exactly'] is False and sc['original_rechecks_SPE'] is False and sc['original_symmetric_means_player_permutations'] is True and sc['objective_is_new_population_average'] is True and not (E/'runs').exists()
recs=read(W/'semantic-receipts.json');assert len(recs)==2 and {x['id'] for x in recs}==ids
for x in recs:
 assert x['disposition']=='retained' and all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for')) and all(x[k] for k in ('read_note','comparison_note','decision_note')) and all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
assert len(read(W/'relation-evidence.json'))==9 and read(W/'source-state-updates.json')==[]
links=0
for p in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#',1)[0]).resolve()
  if not q.is_file():assert (R/str(q.relative_to(S))).is_file(),(str(p),target)
  links+=1
for x in read(E/'content-manifest.json'):
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
p=W/'copy-files.json'
if p.exists():assert read(p)==sorted(str(q.relative_to(S)) for q in S.rglob('*') if q.is_file())
result=dict(status='PASS',scope='source/hash/blob/normal metadata/owner/full16claim+2/2proof; prior inputs/views exact-byte reuse; all nine report scalar sets and 51 support literals/integer domains; no LP/CCE/probability/payoff arithmetic',primary_files=2,primary_bytes=16539,retained=2,duplicate=0,new_normal_show_files=2,formal_math_files=1,comparison_snapshots=8,related_MD_files=2,related_MD_bytes=8166,runtime_JSON_files_reused=51,prior_full_input_certificate_files_reused=18,prior_full_input_certificate_bytes_reused=1469006,prior_full_action_rows_reused=12222,report_root_fields=3,report_case_rows=9,fields_per_case=9,stored_support_atoms=51,fields_per_support_atom=3,relations=9,source_state_updates=0,original_entry_runs=0,imports=0,SPE_IC_runs=0,actual_path_replays=0,H_recomputations=0,count_profile_enumerations=0,LP_runs=0,exact_CCE_checks=0,probability_rationalizations=0,solver_runs=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
