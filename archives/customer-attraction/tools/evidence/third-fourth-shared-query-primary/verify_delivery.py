"""Structural delivery check only. Never executes/imports the original math entry."""
from pathlib import Path
import hashlib,json,re

E=Path(__file__).resolve().parent
S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-third-fourth-shared-query-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=read(E/'actual-source-manifest.json')
rows=manifest['rows'];ids={r['id'] for r in rows}
assert len(rows)==4 and sum(r['size'] for r in rows)==8795
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4'
assert len(claim['ids'])==9 and ids<=set(claim['ids'])
assert claim['local_sync']['status']=='synced'
assert claim['remote_tip']=='fea0bd38ffeabe0603a114e1b9bf5ce1bf73db52'
for r in rows:
 p=S/r['stage_path'];b=p.read_bytes()
 assert len(b)==r['size'] and sha(p)==r['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob']
 old=Path(r['local_path']);assert old.read_bytes()==b
 progress=read(E/'local-progress-at-read'/(r['id']+'.json'))
 assert progress['owner']=='Boss4' and progress['source_sha256']==r['sha256']
 assert (E/'normal-show-captures'/Path(r['actual_normal_show_capture']).name).is_file()
receipts=read(W/'semantic-receipts.json');assert len(receipts)==4 and {x['id'] for x in receipts}==ids
for x in receipts:
 assert x['disposition']=='retained'
 assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
comp=read(E/'formal-comparison.json');assert len(comp)==6
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed']
assert len(read(W/'relation-evidence.json'))==8
assert read(W/'source-state-updates.json')==[]
point=E/'related-point-original/promotion_joint_atoms_exact.json'
assert point.stat().st_size==53404 and sha(point)=='9c84403826eb3d4e44d0fed55dcda180e9be80b0f07c4f464aecbe284f2015b3'
d=read(point);assert [len(d[k]) for k in ('histograms','groups','RZ_atoms','promotion_states')]==[16,16,29,21]
run=E/'runs/one-original-cli';meta=read(run/'run.json')
assert meta['run_count']==1 and meta['exit_code']==0 and meta['before']==meta['after']
assert meta['all_inputs_and_primary_originals_unchanged'] is True
assert meta['argv'][1:3]==['-I','-B'] and meta['stdin']=='DEVNULL'
assert (run/'stdout.txt').stat().st_size==meta['stdout_bytes']==822
assert (run/'stderr.txt').stat().st_size==meta['stderr_bytes']==0
for p,fp in meta['after'].items():
 pp=Path(p);assert pp.stat().st_size==fp['bytes'] and sha(pp)==fp['sha256']
code=run/'verify_third_cross_source.py'
assert sha(code)=='45196f93e463a67e0f90c4c931aa3c8d7515dedfbbf267db511b9425c22b0e04'
frozen=S/next(r['stage_path'] for r in rows if r['id']=='09167e4b5aeb8720a0a0')
output=run/'third_cross_source_exact.json';assert output.read_bytes()==frozen.read_bytes()
report=read(output);stdout=read(run/'stdout.txt')
assert stdout=={k:v for k,v in report.items() if k!='coefficients'}
assert report['local_identity_checks']==15360 and report['source_remaining']==4
assert report['input_sha256']==sha(point)
assert len(report['coefficients'])==11
assert read(run/'third_cross_source_integer_row.json')['integer_weights']==[44,1,7,2,6,7,1,7,2]
assert read(E/'run-discovery-and-scope.json')['original_cli_runs']==1
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==2
link_count=0
for p in math+[E/'README.md']:
 text=p.read_text()
 for target in re.findall(r'\]\(([^)]+)\)',text):
  if '://' in target or target.startswith('#'):continue
  target=target.split('#',1)[0]
  q=(p.parent/target).resolve()
  if not q.exists():
   rel=q.relative_to(S)
   assert (R/rel).is_file(),(str(p),target)
  link_count+=1
for x in read(E/'content-manifest.json'):
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
copy=W/'copy-files.json'
if copy.exists():
 listed=read(copy)
 assert listed==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result={'status':'PASS','checks':'structural fingerprints, raw claim/owner, receipts, comparisons, existing run/output binding, links, manifest; no math entry execution','primary_files':4,'primary_bytes':8795,'related_point_bytes':53404,'comparison_snapshots':6,'formal_math_files':2,'receipts':4,'retained':4,'duplicates':0,'relations':8,'source_state_updates':0,'original_math_entry_runs_recorded':1,'new_mathematical_program_runs':0,'markdown_links_checked':link_count}
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
