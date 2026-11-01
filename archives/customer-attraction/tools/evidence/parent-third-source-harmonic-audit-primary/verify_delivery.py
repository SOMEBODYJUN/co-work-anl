"""Packaging/field check only; executes neither the parent nor author math code."""
from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
P=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-third-fourth-shared-query-primary')
W=S/'cleanup/workspaces/Boss4/r3-parent-third-source-harmonic-audit-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(E/'actual-source-manifest.json');rows=m['rows'];ids={x['id'] for x in rows}
assert len(rows)==2 and sum(x['size'] for x in rows)==4655
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4'
assert len(claim['ids'])==12 and ids<=set(claim['ids']) and claim['local_sync']['status']=='synced'
assert claim['remote_tip']=='6ea3301b3b7a8606053389506f9554c380203ed4'
for row in rows:
 p=S/row['stage_path'];b=p.read_bytes()
 assert len(b)==row['size'] and sha(p)==row['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob']
 assert Path(row['local_path']).read_bytes()==b
 progress=read(E/'local-progress-at-read'/(row['id']+'.json'))
 assert progress['owner']=='Boss4' and progress['source_sha256']==row['sha256']
 assert (E/'normal-show-captures'/Path(row['actual_normal_show_capture']).name).is_file()
rr=read(W/'semantic-receipts.json');assert len(rr)==2 and {x['id'] for x in rr}==ids
for x in rr:
 assert x['disposition']=='retained'
 assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() or (P/t).is_file() for t in x['targets'])
comp=read(E/'formal-comparison.json');assert len(comp)==5
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed']
authors=read(E/'related-author-originals.json');assert len(authors)==4
for x in authors:
 p=S/x['snapshot'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and x['primary'] is False
point=E/'related-point-original/promotion_joint_atoms_exact.json'
assert point.stat().st_size==53404 and sha(point)=='9c84403826eb3d4e44d0fed55dcda180e9be80b0f07c4f464aecbe284f2015b3'
scope=read(E/'scope-and-reuse.json')
assert all(scope[k]==0 for k in ('current_parent_original_entry_runs','current_author_entry_runs','new_mathematical_implementation_runs','new_solver_runs','new_1269_row_rebuilds'))
assert scope['reused_author_run_count_from_previous_scope']==1 and scope['related_point_receipt_or_done'] is False
oldrun=E/'reused-author-run-evidence';meta=read(oldrun/'run.json')
assert meta['run_count']==1 and meta['exit_code']==0 and meta['before']==meta['after']
assert (oldrun/'stderr.txt').stat().st_size==0 and (oldrun/'stdout.txt').stat().st_size==822
assert sha(oldrun/'promotion_joint_atoms_exact.json')==sha(point)
assert sha(oldrun/'verify_third_cross_source.py')=='45196f93e463a67e0f90c4c931aa3c8d7515dedfbbf267db511b9425c22b0e04'
author=read(oldrun/'third_cross_source_exact.json')
frozen_author=S/next(x['snapshot'] for x in authors if x['id']=='09167e4b5aeb8720a0a0')
assert (oldrun/'third_cross_source_exact.json').read_bytes()==frozen_author.read_bytes()
parent=read(S/next(x['stage_path'] for x in rows if x['id']=='ccd6acebcc4834afac38'))
assert parent['raw_coefficient_states']==2048 and parent['projected_states']==256 and parent['target_status']=='OPEN'
assert parent['weights']==[44,1,7,2,6,7,1,7,2]
mapping={'point_sha256':'input_sha256','lhs':'left','rhs':'right','slack':'raw_slack','slack_divided_by_77':'slack_divided_by_77'}
assert all(parent[k]==author[v] for k,v in mapping.items())
fc=read(E/'report-field-comparison.json')
assert fc['byte_identical'] is False and all(x['equal'] is True for x in fc['fields'].values())
assert len(read(W/'relation-evidence.json'))==6 and read(W/'source-state-updates.json')==[]
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
links=0
for p in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#',1)[0]).resolve()
  if not q.exists():
   rel=q.relative_to(S);assert (R/rel).is_file() or (P/rel).is_file(),(str(p),target)
  links+=1
for x in read(E/'content-manifest.json'):
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
copy=W/'copy-files.json'
if copy.exists():assert read(copy)==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result={'status':'PASS','scope':'delivery and existing report fields only; neither math entry executed','primary_files':2,'primary_bytes':4655,'receipts':2,'retained':2,'duplicate':0,'formal_math_files':1,'comparison_snapshots':5,'relations':6,'source_state_updates':0,'new_parent_entry_runs':0,'new_author_entry_runs':0,'new_mathematical_implementation_runs':0,'reused_prior_author_run_evidence':1,'links_checked':links}
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
