"""Packaging/source/log-field verification only. Never import or run an attack/solver."""
from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-uncovered-reset-and-frozen-attack-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
man=read(E/'actual-source-manifest.json');rows=man['rows'];ids={x['id'] for x in rows}
assert len(rows)==4 and sum(x['size'] for x in rows)==10609
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim'
assert len(claim['ids'])==22 and ids<=set(claim['ids'])
assert claim['remote_tip']=='241d1f6927a54ba5b637051935c5fee10b2a72ce' and claim['local_sync']['status']=='synced'
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes()
 assert len(b)==x['size'] and sha(p)==x['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
 assert b==Path(x['local_path']).read_bytes() and x['full_file_reviewed'] is True
 progress=read(E/'local-progress-at-read'/(x['id']+'.json'))
 assert progress['owner']=='Boss4' and progress['source_sha256']==x['sha256']
 assert (E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name).is_file()
rel=read(E/'actual-related-source-manifest.json')
assert rel['related_only_no_extra_done'] is True and len(rel['rows'])==1
x=rel['rows'][0];assert x['id']=='af2653758ceb36c00135' and x['size']==6130 and x['full_file_reviewed'] is True
p=S/x['stage_path'];b=p.read_bytes()
assert len(b)==6130 and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
assert (E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name).is_file()
logs=[json.loads(z) for z in (S/next(x['stage_path'] for x in rows if x['id']=='4602f34157125bda6233')).read_text().splitlines()]
assert len(logs)==4
for z,n,k,m,p in zip(logs[:3],[400,520,600],[445,569,652],[4,5,6],[5,6,6]):
 assert set(z)=={'m','p','examined','outcomes','maxratio','elapsed'}
 assert (z['examined'],z['outcomes'],z['m'],z['p'])==(n,k,m,p)
assert set(logs[3])=={'status','seed','examined','outcomes','maxratio','elapsed'}
assert (logs[3]['status'],logs[3]['seed'],logs[3]['examined'],logs[3]['outcomes'])==('FINITE_ATTACK_ONLY',20261024,600,652)
assert [x['elapsed'] for x in logs]==[1.1472375392913818,3.4735264778137207,7.185589551925659,7.185941696166992]
best=[0.21875,{'m':4,'p':5,'trial':352,'W':32,'optU':7,'counts':[1,3,0,0,0],'weights':{'1':6,'4':0,'5':0,'6':4,'7':6,'8':0,'10':7,'11':4,'12':2,'13':0,'16':5,'19':0,'23':3,'24':0,'30':2}}]
assert all(z['maxratio']==best for z in logs)
rr=read(W/'semantic-receipts.json')
assert {x['id'] for x in rr}==ids and len(rr)==4
assert sum(x['disposition']=='retained' for x in rr)==3 and sum(x['disposition']=='duplicate' for x in rr)==1
assert rel['rows'][0]['id'] not in ids
for x in rr:
 assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
comp=read(E/'formal-comparison.json');assert len(comp)==8
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed'] is True
scope=read(E/'execution-and-domain-boundaries.json')
assert all(scope[k]==0 for k in ('current_original_entry_runs','current_imports','current_solver_runs','current_RNG_replays','new_mathematical_implementation_runs','old_counterexample_replays'))
assert scope['historical_runtime_manifest_present'] is False
assert not (E/'runs').exists() and read(W/'source-state-updates.json')==[]
assert len(read(W/'relation-evidence.json'))==8
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==2
links=0
for p in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#',1)[0]).resolve()
  if not q.is_file():assert (R/q.relative_to(S)).is_file(),(str(p),target)
  links+=1
for x in read(E/'content-manifest.json'):
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
copy=W/'copy-files.json'
if copy.exists():assert read(copy)==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result={'status':'PASS','scope':'source hashes/blob, actual claim/owner, full frozen log fields, related source, comparison snapshots, receipts and links only; no original import/attack/solver execution','primary_files':4,'primary_bytes':10609,'related_only_files':1,'related_only_bytes':6130,'receipts':4,'retained':3,'duplicate':1,'formal_math_files':2,'comparison_snapshots':8,'relations':8,'source_state_updates':0,'original_entry_runs':0,'imports':0,'RNG_replays':0,'solver_runs':0,'new_mathematical_implementation_runs':0,'old_counterexample_replays':0,'links_checked':links}
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
