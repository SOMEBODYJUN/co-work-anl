"""Integrity and complete literal transcription only; no game/IC/Fraction evaluation."""
from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-net-residual-fixed-certificate-diagnostic-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
man=read(E/'actual-source-manifest.json');rows=man['rows'];ids={x['id'] for x in rows}
assert len(rows)==2 and sum(x['size'] for x in rows)==9487
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4'
assert len(claim['ids'])==13 and ids<=set(claim['ids'])
assert claim['remote_tip']=='d9c4518fcbf32737039021008b59bf58592fe58c'
assert claim['local_sync']['status']=='needs-attention' and man['raw_original_local_sync']==claim['local_sync']
proof=read(E/'claim-sync-preservation.json')
assert proof['untracked_count']==11 and not proof['missing'] and not proof['different'] and not proof['unmerged']
assert len(proof['tracked'])==2 and all(x['same'] is True for x in proof['tracked']) and proof['stash_kept'] is True
assert proof['stash']=='1250fa5ec8810175e73ef1b02371150fe0086a4f'
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes()
 assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
 assert x['full_file_reviewed'] is True and x['new_normal_show'] is True
 d=read(E/'local-progress-at-read'/(x['id']+'.json'))
 assert d['owner']=='Boss4' and d['disposition']=='in-progress' and d['source_sha256']==x['sha256']
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name)
 assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')}
 assert cap['output']==x['local_path']
comp=read(E/'formal-comparison.json');assert len(comp)==8
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed'] is True
 assert p.read_bytes()==Path(x['actual_read_from']).read_bytes()
related=read(E/'related-source-manifest.json');assert len(related)==1
for x in related:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes']==4244 and sha(p)==x['sha256']
 assert x['full_file_reviewed'] is True and x['new_primary'] is False and x['new_done'] is False
 assert p.read_bytes()==Path(x['actual_read_from']).read_bytes()
receipts=read(W/'semantic-receipts.json');assert len(receipts)==2 and {x['id'] for x in receipts}==ids
for x in receipts:
 assert x['disposition']=='retained'
 assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
sc=read(E/'execution-and-domain-boundaries.json')
assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_certificate_replays','current_IC_replays','current_LP_runs','current_RNG_replays','current_solver_runs','new_mathematical_implementation_runs'))
assert sc['historical_execution_manifest_present'] is False and sc['all_report_fields_transcribed'] is True
assert not (E/'runs').exists() and read(W/'source-state-updates.json')==[]
assert len(read(W/'relation-evidence.json'))==8
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
page=math[0].read_text()
raw=read(S/next(x['stage_path'] for x in rows if x['id']=='2cbbe2b31bdb17a315d2'))
assert read(E/'stored-report-literal-transcription.json')==raw
assert set(raw)==set(sc['root_keys']) and len(raw['reports'])==7
assert raw['status'] in page
hs=[6,259,31,43,259,43,7] # literal loop-domain transcription, not IC evaluation
for i,(r,h) in enumerate(zip(raw['reports'],hs)):
 assert set(r)==set(sc['report_fields'])
 line=f"|{i}|{r['name']}|{r['m']}|{r['q']}|{h}|{r['checked_IC']}|{','.join(map(str,r['actual']))}|{r['welfare']}|{r['optimum']}|"
 assert line in page,line
 for k in ('NRMAX','NRAVG'):
  d=r[k];assert set(d)==set(sc['winner_fields'])
  line=f"|{i}|{k}|{','.join(map(str,d['comparison']))}|{d['R']}|{d['G']}|{d['net']}|{', '.join(d['max_values'])}|{d['max_gap']}|{d['avg_gap']}|"
  assert line in page,line
links=0
for p in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#',1)[0]).resolve()
  if not q.is_file():
   rel=str(q.relative_to(S));assert (R/rel).is_file(),(p,target)
  links+=1
for x in read(E/'content-manifest.json'):
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
p=W/'copy-files.json'
if p.exists():assert read(p)==sorted(str(q.relative_to(S)) for q in S.rglob('*') if q.is_file())
result=dict(status='PASS',scope='source/hash/blob/normal metadata, raw needs-attention+preservation, local owner, comparison snapshots, all literal report fields, receipts and links only; no mathematical run',primary_files=2,primary_bytes=9487,new_normal_show_files=2,retained=2,duplicate=0,formal_math_files=1,comparison_snapshots=8,related_old_MD_files=1,report_cases=7,winner_records=14,relations=8,source_state_updates=0,original_entry_runs=0,imports=0,certificate_replays=0,IC_replays=0,LP_runs=0,RNG_replays=0,solver_runs=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
