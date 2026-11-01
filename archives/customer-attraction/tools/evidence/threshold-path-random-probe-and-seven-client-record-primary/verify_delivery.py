"""Integrity/recovery evidence and literal report transcription only; no RNG, Fraction, BI, solver or original execution."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-threshold-path-random-probe-and-seven-client-record-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
man=read(E/'actual-source-manifest.json');rows=man['rows'];ids={x['id'] for x in rows}
assert len(rows)==3 and sum(x['size'] for x in rows)==4040
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4' and len(claim['ids'])==26 and ids<=set(claim['ids'])
assert claim['remote_tip']=='1f16a464c89fc5bc36d035677e6fb39364a18bc7' and claim['local_sync']['status']=='needs-attention'
assert man['raw_original_local_sync']==claim['local_sync']
proof=read(E/'claim-sync-preservation.json')
assert proof['untracked_count']==38 and len(proof['tracked'])==2 and all(x['same'] is True for x in proof['tracked'])
assert proof['missing']==[] and proof['different']==[] and proof['unmerged']=='' and proof['stash_kept'] is True and proof['stash']=='d5b4366bfdc3be47f06d3f4384b88afdb7c9c1da'
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'] and x['full_file_reviewed'] is True and x['new_normal_show'] is True
 owner=read(E/'local-progress-at-read'/(x['id']+'.json'));assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==x['sha256']
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name)
 assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')} and cap['output']==x['local_path']
comp=read(E/'formal-comparison.json');assert len(comp)==6
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True
rel=read(E/'related-MD-manifest.json');assert len(rel)==2
for x in rel:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes()
 assert x['full_file_reviewed'] is True and x['new_primary'] is False and x['new_done'] is False
deps=read(E/'related-runtime-source-manifest.json');assert len(deps)==4 and sum(x['size'] for x in deps)==25475
prior={x['path']:x for x in read(E/'previous-full-runtime-reading-manifest.json')}
for x in deps:
 p=S/x['snapshot'];b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['actual_read_from']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
 assert x['full_file_reviewed'] is True and x['exact_previous_full_reading_reused'] is True and x['new_primary'] is False and x['new_done'] is False
 assert prior[x['path']]['sha256']==x['sha256'] and prior[x['path']]['full_file_reviewed'] is True
rec=read(W/'semantic-receipts.json');assert len(rec)==3 and {x['id'] for x in rec}==ids
for x in rec:
 assert x['disposition']=='retained' and all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note')) and all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
sc=read(E/'execution-and-domain-boundaries.json')
assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_random_replays','current_solver_runs','current_BI_replays','current_certificate_generation','current_parameter_scans','new_mathematical_implementation_runs'))
assert sc['historical_execution_manifest_present'] is False and sc['boundary_generator_present_in_primary'] is False and sc['all_report_fields_transcribed'] is True and not (E/'runs').exists()
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==8
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
page=math[0].read_text();rand=read(S/rows[1]['stage_path']);boundary=read(S/rows[2]['stage_path'])
assert read(E/'stored-reports-literal-transcription.json')==dict(random_probe=rand,seven_customer_boundary=boundary)
assert set(rand)=={'candidate','seed','runs','counterexample','min_2sumM_over_OPT'} and rand['seed']==763809 and rand['runs']==300 and rand['counterexample'] is None and rand['min_2sumM_over_OPT']=='1'
assert rand['candidate'] in page
assert set(boundary)=={'status','instance','path','sum_M','OPT','minimum_SPE_welfare','terminal_welfares','rows'} and len(boundary['rows'])==5
assert boundary['status'] in page and boundary['path']==[1,1,1,2,0] and boundary['sum_M']=='13/2' and boundary['OPT']==7 and boundary['minimum_SPE_welfare']==7 and boundary['terminal_welfares']==[7]
ins=boundary['instance'];assert set(ins)=={'topics','customers','players'} and ins['topics']==['0','1','2','3'] and ins['players']==5
assert ins['customers']==[{'topics':[1],'multiplicity':2},{'topics':[0,1,2],'multiplicity':4},{'topics':[2,3],'multiplicity':1}]
for x in ins['customers']:assert '|'+','.join(map(str,x['topics']))+'|'+str(x['multiplicity'])+'|' in page
for row in boundary['rows']:
 assert set(row)=={'prefix','M','action','child_minima'} and len(row['prefix'])==4 and set(row['child_minima'])=={'0','1','2','3'}
 line='|'+'|'.join([','.join(map(str,row['prefix'])),row['M'],str(row['action'])]+[row['child_minima'][str(i)] for i in range(4)])+'|'
 assert line in page,line
# No recurrence, customer-payoff evaluation, RNG or mathematical bound is executed.
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
result=dict(status='PASS',scope='source/hash/blob/normal metadata/owner/claim+38/2 recovery proof, prior-read dependency bytes, all literal report fields, receipts and links only; no mathematics/RNG/BI evaluation',primary_files=3,primary_bytes=4040,new_normal_show_files=3,retained=3,duplicate=0,formal_math_files=1,comparison_snapshots=6,related_MD_files=2,related_runtime_sources=4,related_runtime_bytes=25475,random_report_fields=5,boundary_report_fields=8,boundary_rows=5,boundary_child_values=20,relations=8,source_state_updates=0,original_entry_runs=0,imports=0,random_replays=0,solver_runs=0,BI_replays=0,certificate_generation=0,parameter_scans=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
