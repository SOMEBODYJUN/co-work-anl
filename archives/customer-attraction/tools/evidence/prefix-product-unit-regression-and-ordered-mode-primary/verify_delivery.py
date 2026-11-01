"""Source integrity and literal finite report topology only; no source execution, payoff, IC or OPT calculation."""
from pathlib import Path
from itertools import product
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-prefix-product-unit-regression-and-ordered-mode-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
man=read(E/'actual-source-manifest.json');rows=man['rows'];ids={x['id'] for x in rows}
assert len(rows)==2 and sum(x['size'] for x in rows)==12299
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4' and len(claim['ids'])==22 and ids<=set(claim['ids'])
assert claim['remote_tip']=='e41ac6c6d77bfd5fb71d1e8b10a30eedf56c47d3' and claim['local_sync']['status']=='synced'
assert man['raw_original_local_sync']==claim['local_sync']
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'] and x['full_file_reviewed'] is True and x['new_normal_show'] is True
 owner=read(E/'local-progress-at-read'/(x['id']+'.json'))
 assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==x['sha256']
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name)
 assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')} and cap['output']==x['local_path']
comp=read(E/'formal-comparison.json');assert len(comp)==6
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True
rel=read(E/'related-MD-manifest.json');assert len(rel)==2
for x in rel:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True
 assert x['new_primary'] is False and x['new_done'] is False
receipts=read(W/'semantic-receipts.json');assert len(receipts)==2 and {x['id'] for x in receipts}==ids
for x in receipts:
 assert x['disposition']=='retained' and all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
sc=read(E/'execution-and-domain-boundaries.json')
assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_IC_replays','current_coverage_replays','current_solver_runs','current_LP_runs','current_RNG_replays','current_parameter_scans','new_mathematical_implementation_runs'))
assert sc['historical_execution_manifest_present'] is False and sc['original_external_input_files']==0 and sc['all_report_fields_transcribed'] is True and not (E/'runs').exists()
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==8
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
page=math[0].read_text();r=read(S/rows[1]['stage_path'])
assert read(E/'stored-report-literal-transcription.json')==r and len(r)==17 and len(r['actions'])==43
expected={'source_original':'A size1,B size4, target AAB; all customers scaled2','m':3,'j':2,'bank_d':1,'customers':25,'topics':6,'full_ordered_decision_histories':43,'all_action_IC_checks':258,'minimum_IC_margin':'0','old_min_child_floor':{'1:0':'2','1:1':'8/3','2:0':'1','2:1':'4'},'Delta_after_scale':'3','s':'3','actual_joint_path':[[0,0],[0,1],[1,2]],'actual_player_payoffs':['7','7','11'],'actual_W':25,'OPT_m':25}
for k,v in expected.items():assert r[k]==v
assert r['source_original'] in page
for key,v in r['old_min_child_floor'].items():assert key in page and v in page
joint=tuple(product(range(2),range(3)))
history_keys=[tuple(tuple(a) for a in row['history']) for row in r['actions']]
assert len(set(history_keys))==43
assert set(history_keys)=={h for depth in range(3) for h in product(joint,repeat=depth)}
def hfmt(h):return '['+','.join('('+','.join(map(str,a))+')' for a in h)+']'
def afmt(a):return '('+','.join(map(str,a))+')'
for row in r['actions']:
 assert set(row)=={'history','action'} and tuple(row['action']) in joint
 assert f"|{hfmt(row['history'])}|{afmt(row['action'])}|" in page
acts={tuple(tuple(a) for a in row['history']):tuple(row['action']) for row in r['actions']}
assert acts[((0,0),(0,1))]==(1,2) and acts[((0,1),(0,0))]==(1,1)
# The above is stored topology/list validation, not a payoff or strategy replay.
links=0
for path in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(path.parent/target.split('#',1)[0]).resolve()
  if not q.is_file():assert (R/str(q.relative_to(S))).is_file(),(str(path),target)
  links+=1
for x in read(E/'content-manifest.json'):
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
p=W/'copy-files.json'
if p.exists():assert read(p)==sorted(str(q.relative_to(S)) for q in S.rglob('*') if q.is_file())
result=dict(status='PASS',scope='source/hash/blob/normal metadata/owner/fullclaim, formal/related bytes, all literal report fields and43-entry topology, receipts and links only; no mathematical strategy/payoff/IC/OPT evaluation',primary_files=2,primary_bytes=12299,new_normal_show_files=2,retained=2,duplicate=0,formal_math_files=1,comparison_snapshots=6,related_MD_files=2,report_fields=17,stored_policy_entries=43,relations=8,source_state_updates=0,original_entry_runs=0,imports=0,IC_replays=0,coverage_replays=0,solver_runs=0,LP_runs=0,RNG_replays=0,parameter_scans=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
