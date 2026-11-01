"""Delivery integrity and literal stored report tables only; no Fraction/pattern/unit/IC evaluation or original import."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-beta-clone-independent-audit-two-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
man=read(E/'actual-source-manifest.json');rows=man['rows'];ids={x['id'] for x in rows}
assert len(rows)==2 and sum(x['size'] for x in rows)==8170
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4'
assert len(claim['ids'])==19 and ids<=set(claim['ids']) and claim['remote_tip']=='41c2e223127cbe5c48fcaa1f571cbb10fac8f45a'
assert claim['local_sync']['status']=='needs-attention' and man['raw_original_local_sync']==claim['local_sync']
proof=read(E/'claim-sync-preservation.json');assert proof['untracked_count']==38 and len(proof['tracked'])==2 and all(x['same'] is True for x in proof['tracked'])
assert proof['missing']==[] and proof['different']==[] and proof['unmerged']=='' and proof['stash_kept'] is True and proof['stash']=='75852f2c937ee082e5fa53e695ef669219da723f'
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'] and x['full_file_reviewed'] is True and x['new_normal_show'] is True
 owner=read(E/'local-progress-at-read'/(x['id']+'.json'));assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==x['sha256']
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name)
 assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')} and cap['output']==x['local_path']
comp=read(E/'formal-comparison.json');assert len(comp)==5
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True
rel=read(E/'related-MD-manifest.json');assert len(rel)==3 and sum(x['bytes'] for x in rel)==15826
for x in rel:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes()
 assert x['full_file_reviewed'] is True and x['new_primary'] is False and x['new_done'] is False
recs=read(W/'semantic-receipts.json');assert len(recs)==2 and {x['id'] for x in recs}==ids
for x in recs:
 assert x['disposition']=='retained' and all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note')) and all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
sc=read(E/'execution-and-domain-boundaries.json')
assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_original_subgame_replays','current_clone_unit_expansions','current_pattern_replays','current_solver_runs','current_LP_runs','current_parameter_scans','new_mathematical_implementation_runs'))
assert sc['historical_execution_manifest_present'] is False and sc['all_report_fields_transcribed'] is True and not (E/'runs').exists() and not (S/'PRE_SOURCE_MATHEMATICS.md').exists()
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==8
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
page=math[0].read_text();r=read(S/rows[1]['stage_path']);assert read(E/'stored-report-literal-transcription.json')==r and set(r)=={'original','clone'}
o=r['original'];c=r['clone']
assert set(o)=={'catalog_size','nodes','comparisons','A_B_C_last_rows','current_payoffs','max_singleton_current'}
assert (o['catalog_size'],o['nodes'],o['comparisons'],o['max_singleton_current'])==(39,40,1560,'1/4')
assert list(o['A_B_C_last_rows'])==['A','B','C'] and len(o['current_payoffs'])==39
assert set(o['current_payoffs'])=={'A','B','C'}|{'P'+str(i) for i in range(36)}
for a,x in o['A_B_C_last_rows'].items():
 assert set(x)=={'best_value','all_BR','A_B_C_values'} and set(x['A_B_C_values'])=={'A','B','C'}
 line='|'+'|'.join([a]+[x['A_B_C_values'][z] for z in ['A','B','C']]+[x['best_value'],', '.join(x['all_BR'])])+'|'
 assert line in page,line
for a,v in o['current_payoffs'].items():assert f'|{a}|{v}|' in page
assert set(c)=={'clone_catalog_size','scale','unit_customers','rows','strict_improvement','encoded_background_not_replayed'}
assert (c['clone_catalog_size'],c['scale'],c['unit_customers'],c['strict_improvement'],c['encoded_background_not_replayed'])==(40,60,5100,'25-24=1',True)
assert list(c['rows'])==['A0','A1','B0','C0']
assert sum(len(x['current_payoff_by_BR']) for x in c['rows'].values())==5
for a,x in c['rows'].items():
 assert set(x)=={'last_values','singleton_last_max','best_value','all_BR','current_payoff_by_BR'} and set(x['last_values'])=={'A0','A1','B0','C0'}
 line='|'+'|'.join([a]+[x['last_values'][z] for z in ['A0','A1','B0','C0']]+[x['singleton_last_max'],x['best_value']])+'|'
 assert line in page,line
 line='|'+'|'.join([a,', '.join(x['all_BR']),'; '.join(z+':'+v for z,v in x['current_payoff_by_BR'].items())])+'|'
 assert line in page,line
assert c['rows']['A1']['current_payoff_by_BR']=={'B0':'24','C0':'27'} and c['rows']['A0']['current_payoff_by_BR']=={'C0':'25'}
# These are literal stored fields, not regenerated customer tables or SPE checks.
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
result=dict(status='PASS',scope='source/hash/blob/normal metadata/owner/fullclaim+38/2 recovery proof, related bytes, all literal original/clone report fields, semantic receipts and links only; no pattern/unit/payoff/IC evaluation',primary_files=2,primary_bytes=8170,new_normal_show_files=2,retained=2,duplicate=0,formal_math_files=1,comparison_snapshots=5,related_MD_files=3,related_MD_bytes=15826,report_root_fields=2,original_report_fields=6,clone_report_fields=6,original_current_values=39,clone_current_rows=4,clone_regular_last_values=16,clone_BR_current_values=5,relations=8,source_state_updates=0,original_entry_runs=0,imports=0,original_subgame_replays=0,clone_unit_expansions=0,pattern_replays=0,solver_runs=0,LP_runs=0,parameter_scans=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
