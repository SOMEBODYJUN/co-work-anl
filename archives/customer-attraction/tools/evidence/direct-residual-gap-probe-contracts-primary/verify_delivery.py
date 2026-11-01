"""Source, fixture, raw transaction and delivery integrity only; no LP/RNG/solver execution."""
from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-direct-residual-gap-probe-contracts-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
man=read(E/'actual-source-manifest.json');rows=man['rows'];ids={x['id'] for x in rows}
assert len(rows)==4 and sum(x['size'] for x in rows)==11885
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim'
assert len(claim['ids'])==8 and ids<=set(claim['ids']) and claim['local_sync']['status']=='synced'
assert claim['remote_tip']=='4776682b6f18bddba942c29e9b6664db00c4d15d'
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes()
 assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
 assert x['full_file_reviewed'] is True
 d=read(E/'local-progress-at-read'/(x['id']+'.json'))
 assert d['owner']=='Boss4' and d['source_sha256']==x['sha256']
 assert (E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name).is_file()
old=next(x for x in rows if x['id']=='af2653758ceb36c00135')
assert old['exact_prior_normal_show_reused'] is True and old['no_new_normal_show_for_this_source'] is True
comp=read(E/'formal-comparison.json');assert len(comp)==7
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed'] is True
 assert sha(Path(x['actual_read_from']))==x['sha256']
fixtures=read(E/'related-fixed-fixture-manifest.json');assert len(fixtures)==2 and len({x['snapshot'] for x in fixtures})==2
for x in fixtures:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed'] is True
 assert p.read_bytes()==(R/x['repository_path']).read_bytes()
co=read(S/fixtures[0]['snapshot']);assert set(co)=={'terminal_counts','actions'} and len(co['actions'])==259
assert co['terminal_counts']==[0,1,3,0,0,0]
ins=read(S/fixtures[1]['snapshot']);assert set(ins)=={'topics','customers','players'}
assert ins['topics']==['L0','A','B','L1','L2','L3'] and ins['players']==4 and len(ins['customers'])==12
rr=read(W/'semantic-receipts.json');assert len(rr)==4 and {x['id'] for x in rr}==ids
assert sum(x['disposition']=='retained' for x in rr)==2 and sum(x['disposition']=='duplicate' for x in rr)==2
available={x['path']:S/x['snapshot'] for x in comp}
for x in rr:
 assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() or t in available for t in x['targets'])
scope=read(E/'execution-and-domain-boundaries.json')
assert all(scope[k]==0 for k in ('current_original_entry_runs','current_imports','current_LP_runs','current_RNG_replays','current_solver_runs','current_certificate_replays','new_mathematical_implementation_runs'))
assert scope['historical_full_stdout_or_execution_manifest_present'] is False and not (E/'runs').exists()
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==7
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
links=0
for p in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#',1)[0]).resolve()
  if not q.is_file():
   rel=str(q.relative_to(S));assert (R/rel).is_file() or rel in available,(str(p),target)
  links+=1
for x in read(E/'content-manifest.json'):
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
p=W/'copy-files.json'
if p.exists():assert read(p)==sorted(str(q.relative_to(S)) for q in S.rglob('*') if q.is_file())
result={'status':'PASS','scope':'source hashes/blob, raw claim/owner, exact reused show, all fixture bytes, comparison snapshots, receipts and links only; no original execution or mathematical solver checks','primary_files':4,'primary_bytes':11885,'new_normal_show_files':3,'exact_prior_normal_show_reused_files':1,'receipts':4,'retained':2,'duplicate':2,'formal_math_files':1,'full_fixture_files_read':2,'comparison_snapshots':7,'relations':7,'source_state_updates':0,'original_entry_runs':0,'imports':0,'LP_runs':0,'RNG_replays':0,'solver_runs':0,'certificate_replays':0,'new_mathematical_implementation_runs':0,'links_checked':links}
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
