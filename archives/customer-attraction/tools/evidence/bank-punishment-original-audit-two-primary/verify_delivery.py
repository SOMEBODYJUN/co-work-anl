"""Metadata/byte integrity and stored report counter sums only. No Fraction/greedy/phi/visit/solver import or evaluation."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-bank-punishment-original-audit-two-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(p):
 b=p.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
m=read(E/'actual-source-manifest.json');rows=m['rows'];ids={x['id'] for x in rows};assert len(rows)==2 and sum(x['size'] for x in rows)==7082
c=read(E/'authoritative-full-claim.json');assert c['status']=='pushed' and c['operation']=='claim' and c['actor']=='Boss4' and len(c['ids'])==15 and ids<=set(c['ids'])
assert c['remote_tip']=='195f7f40ae8fe9d2c00451b3ab9d22f419b94f1b' and c['local_sync']['status']=='needs-attention' and c['local_sync']==m['raw_original_local_sync']
proof=read(E/'claim-sync-preservation.json');assert proof['untracked_count']==2 and len(proof['tracked'])==2 and all(x['same'] is True for x in proof['tracked'])
assert proof['missing']==[] and proof['different']==[] and proof['unmerged']=='' and proof['stash_kept'] is True and proof['stash']=='af8e0e4651193e50c196fe01339890ddc651a36e'
for x in rows:
 p=S/x['stage_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['local_path']).read_bytes() and x['full_file_reviewed'] is True and x['new_normal_show'] is True
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name);assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')} and cap['output']==x['local_path']
 owner=read(E/'local-progress-at-read'/(x['id']+'.json'));assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==x['sha256']
cm=read(E/'formal-comparison.json');assert len(cm)==7
for x in cm:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True
md=read(E/'related-MD-manifest.json');assert len(md)==2 and sum(x['size'] for x in md)==12559
for x in md:
 p=S/x['snapshot'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True and x['new_primary'] is False and x['new_done'] is False
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1;page=math[0].read_text()
r=read(S/rows[1]['stage_path']);assert read(E/'stored-report-literal-transcription.json')==r
assert list(r)==['status','scope','parameter_range','scale','rows','totals'] and len(r['rows'])==21 and r['status']=='PASS'
assert r['scope']=='finite exact implementation audit of all-parameter proof; not the general proof' and r['parameter_range']=='2<=m<=7, all 1<=j<m, all 1<=i<=j, all forced bank labels' and r['scale']=='s=1; rational positive s rescales every comparison'
for k in ['status','scope','parameter_range','scale']:assert '|'+k+'|`'+json.dumps(r[k],ensure_ascii=False)+'`|' in page
keys=['m','j','forced_children','construction_DAG_states','nonterminal_action_comparisons','minimum_IC_gap']
assert [(x['m'],x['j']) for x in r['rows']]==[(2,1),(3,1),(3,2),(4,1),(4,2),(4,3),(5,1),(5,2),(5,3),(5,4),(6,1),(6,2),(6,3),(6,4),(6,5),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6)]
for x in r['rows']:
 assert list(x)==keys and x['minimum_IC_gap']=='0' and '|'+ '|'.join(str(x[k]) for k in keys)+'|' in page
assert r['totals']=={'forced_children':322,'construction_DAG_states':27061,'nonterminal_action_comparisons':92788}
for k,v in r['totals'].items():
 assert f'|{k}|{v}|' in page
 assert sum(x[k] for x in r['rows'])==v  # Sum of stored counters, never original construction/IC.
sc=read(E/'execution-and-domain-boundaries.json');assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_solver_runs','current_DAG_replays','current_original_IC_runs','current_LP_runs','current_unit_expansions','new_mathematical_implementation_runs'))
assert sc['historical_execution_manifest_present'] is False and sc['assert_enabled_execution_binding_present'] is False and sc['all_report_fields_transcribed'] is True and sc['minimums_include_prescribed_self_comparisons'] is True and sc['DAG_states_include_terminals'] is True and sc['caches_shared_across_i_D_within_pair'] is True and sc['all_SPE_outcomes_enumerated'] is False and sc['full_ordered_policy_serialized_in_report'] is False and sc['normal_reward_product_or_static_security_audited'] is False and not (E/'runs').exists()
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
result=dict(status='PASS',scope='source/hash/blob/normal metadata/owner/full15claim+2/2preservation, related full bytes, all report literal fields and three stored counter sums, receipts/content/links only; no Fraction/greedy/phi/visit/IC/solver',primary_files=2,primary_bytes=7082,retained=2,duplicate=0,new_normal_show_files=2,formal_math_files=1,comparison_snapshots=7,related_MD_files=2,related_MD_bytes=12559,report_root_fields=6,parameter_rows=21,fields_per_parameter_row=6,totals_fields=3,stored_counter_sums_checked=3,relations=9,source_state_updates=0,original_entry_runs=0,imports=0,solver_runs=0,DAG_replays=0,original_IC_runs=0,LP_runs=0,unit_expansions=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
