"""Stored-byte, metadata and literal report verification only; no original import/Fraction/payoff/LP/IC."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-beta-clone-author-local-discovery-two-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(p):
 b=p.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
m=read(E/'actual-source-manifest.json');rows=m['rows'];ids={x['id'] for x in rows}
assert len(rows)==2 and sum(x['size'] for x in rows)==4079
c=read(E/'authoritative-full-claim.json');assert c['status']=='pushed' and c['operation']=='claim' and c['actor']=='Boss4' and len(c['ids'])==15 and ids<=set(c['ids'])
assert c['remote_tip']=='aaa6b5e5ca5bd4ab2f4e2ec30473b4fd5bea8f5f' and c['local_sync']['status']=='needs-attention' and m['raw_original_local_sync']==c['local_sync']
proof=read(E/'claim-sync-preservation.json');assert proof['untracked_count']==38 and len(proof['tracked'])==2 and all(x['same'] is True for x in proof['tracked'])
assert proof['missing']==[] and proof['different']==[] and proof['unmerged']=='' and proof['stash_kept'] is True and proof['stash']=='25f460c713f272cabd9d161cf2c4e5ddc0e24a65'
for x in rows:
 p=S/x['stage_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['local_path']).read_bytes()
 assert x['full_file_reviewed'] is True and x['new_normal_show'] is True
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name);assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')} and cap['output']==x['local_path']
 owner=read(E/'local-progress-at-read'/(x['id']+'.json'));assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==x['sha256']
helper=read(E/'required-helper-manifest.json')['rows'];assert len(helper)==1
h=helper[0];assert h['id']=='8ef2bf0e6d9fef6e4d5e' and h['size']==3048 and h['new_primary'] is False and h['new_done'] is False and h['full_file_reviewed'] is True
p=S/h['snapshot'];assert p.stat().st_size==h['size'] and sha(p)==h['sha256'] and blob(p)==h['blob'] and p.read_bytes()==Path(h['local_path']).read_bytes()
cap=read(E/'related-normal-show-captures'/Path(h['actual_normal_show_capture']).name);assert cap['source']=={k:h[k] for k in ('blob','id','mode','path','sha256','size','sources')} and cap['output']==h['local_path']
comps=read(E/'formal-comparison.json');assert len(comps)==8 and len([x for x in comps if x['source_location_at_read']=='earlier-frozen-stage-not-yet-seen-in-R'])==1
for x in comps:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True
md=read(E/'related-MD-manifest.json');assert len(md)==3 and sum(x['bytes'] for x in md)==15826
for x in md:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True and x['new_primary'] is False and x['new_done'] is False
dr=read(E/'related-direct-manifest.json');assert len(dr)==2 and sum(x['size'] for x in dr)==8170
for x in dr:
 p=S/x['snapshot'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True and x['new_primary'] is False and x['new_done'] is False
 cap=read(E/'related-previous-normal-captures'/Path(x['actual_normal_show_capture']).name);assert cap['source']=={k:x[k] for k in ('blob','id','path','sha256','size','sources')}|{'mode':'100644'} and cap['output']==x['local_path']
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
page=math[0].read_text();report=read(S/rows[1]['stage_path']);assert read(E/'stored-report-literal-transcription.json')==report
assert list(report)==['status','types','prefix_original','original_last_reply_after_current','original_current_action','clone_last_reply_original','original_current_payoffs','clone_repeat_payoff','minimum_original_IC','minimum_strict_gain_or_reply_margin']
assert report=={'status':'exact_local_fresh_lift_counterexample','types':[[3,0,36],[4,0,3],[5,1,36],[6,0,10]],'prefix_original':0,'original_last_reply_after_current':[1,0,0],'original_current_action':0,'clone_last_reply_original':2,'original_current_payoffs':['24','22','22'],'clone_repeat_payoff':'25','minimum_original_IC':'0','minimum_strict_gain_or_reply_margin':'1'}
for k,v in report.items():assert '|'+k+'|`'+json.dumps(v,ensure_ascii=False,separators=(',',':'))+'`|' in page
for B,b,n in report['types']:
 lab={3:'A,B',4:'C',5:'A,C',6:'B,C'}[B];assert f'|{B}|{lab}|{b}|{n}|' in page
sc=read(E/'execution-and-domain-boundaries.json')
assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_LP_runs','current_exact_postcheck_replays','current_original_IC_runs','current_solver_runs','current_pattern_replays','current_unit_expansions','current_random_batches','new_mathematical_implementation_runs'))
assert sc['historical_execution_manifest_present'] is False and sc['all_report_fields_transcribed'] is True and sc['maximum_LPs_is_actual_count'] is False and sc['helper_new_primary'] is False and sc['helper_new_done'] is False and not (E/'runs').exists() and not (S/'PRE_SOURCE_MATHEMATICS.md').exists()
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
result=dict(status='PASS',scope='stored source/hash/blob/normal metadata/owner/full15claim and 38+2 preservation, helper and prior related bytes, all ten report literal fields, receipts/content/links; no coefficient/payoff/IC/LP evaluation',primary_files=2,primary_bytes=4079,retained=2,duplicate=0,new_normal_primary_files=2,new_normal_related_files=1,formal_math_files=1,comparison_snapshots=8,related_MD_files=3,related_MD_bytes=15826,related_direct_files=2,related_direct_bytes=8170,related_helper_bytes=3048,report_fields=10,nonzero_types=4,relations=9,source_state_updates=0,original_entry_runs=0,imports=0,LP_runs=0,original_exact_postcheck_replays=0,original_IC_runs=0,solver_runs=0,pattern_replays=0,unit_expansions=0,random_batches=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
