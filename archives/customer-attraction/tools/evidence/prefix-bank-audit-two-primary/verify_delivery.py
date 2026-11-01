"""Source integrity, literal whole report and integer record structure only; never import original audit/run/bi or Fraction/pay/IC."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-prefix-bank-audit-two-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(p):
 b=p.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
m=read(E/'actual-source-manifest.json');rows=m['rows'];ids={x['id'] for x in rows};assert len(rows)==2 and sum(x['size'] for x in rows)==77510
c=read(E/'authoritative-full-claim.json');assert c['status']=='pushed' and c['operation']=='claim' and c['actor']=='Boss4' and len(c['ids'])==22 and ids<=set(c['ids'])
assert c['remote_tip']=='26ab863135a398ab834f336fec5570fb382d9b76' and c['local_sync']['status']=='needs-attention' and c['local_sync']==m['raw_original_local_sync']
proof=read(E/'claim-sync-preservation.json');assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(x['same'] is True for x in proof['tracked'])
assert proof['missing']==[] and proof['different']==[] and proof['unmerged']=='' and proof['stash_kept'] is True and proof['stash']=='b9a9e41e35155d585dd528ae184ba5f5784eb5ad'
for x in rows:
 p=S/x['stage_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['local_path']).read_bytes() and x['full_file_reviewed'] is True and x['new_normal_show'] is True
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name);assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')} and cap['output']==x['local_path']
 owner=read(E/'local-progress-at-read'/(x['id']+'.json'));assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==x['sha256']
cm=read(E/'formal-comparison.json');assert len(cm)==7
for x in cm:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True
md=read(E/'related-MD-manifest.json');assert len(md)==2 and sum(x['size'] for x in md)==14946
for x in md:
 p=S/x['snapshot'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True and x['new_primary'] is False and x['new_done'] is False
r=read(S/rows[1]['stage_path']);assert read(E/'stored-report-literal-transcription.json')==r
assert list(r)==['scope','parameters','nodes_checked','all_action_comparisons','records'] and r['scope']=='finite implementation audit only, m=2,...,7 and 1<=j<m; no theorem inferred from no failures'
assert r['parameters']==len(r['records'])==21 and r['nodes_checked']==10713 and r['all_action_comparisons']==19470
assert sum(x['nodes_checked'] for x in r['records'])==r['nodes_checked'] and sum(x['all_action_comparisons'] for x in r['records'])==r['all_action_comparisons']
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1;page=math[0].read_text()
for k in ['scope','parameters','nodes_checked','all_action_comparisons']:assert '|'+k+'|`'+json.dumps(r[k],ensure_ascii=False)+'`|' in page
keys=['m','j','d','nodes_checked','all_action_comparisons'];expected=[(n,j) for n in range(2,8) for j in range(1,n)];assert [(x['m'],x['j']) for x in r['records']]==expected
lines=['ROOT '+json.dumps({k:v for k,v in r.items() if k!='records'},ensure_ascii=False,separators=(',',':'))];punishments=0
for x in r['records']:
 assert list(x)==keys+['punishments'] and x['d']==x['m']-x['j']
 assert '|'+ '|'.join(str(x[k]) for k in keys)+'|'+str(len(x['punishments']))+'|' in page
 assert [(z['i'],z['action']) for z in x['punishments']]==[(i,t) for i in range(1,x['j']+1) for t in range(x['m'])]
 sec=page.split(f"### m={x['m']}, j={x['j']}, d={x['d']}",1)[1].split('\n### ',1)[0]
 lines.append('PARAMETER '+json.dumps({k:v for k,v in x.items() if k!='punishments'},ensure_ascii=False,separators=(',',':')))
 for z in x['punishments']:
  assert list(z)==['i','action','terminal','deviator_payoff'] and len(z['terminal'])==x['m'] and all(type(t) is int and t>=0 for t in z['terminal']) and sum(z['terminal'])==x['m'] and z['terminal'][z['action']]>0 and z['deviator_payoff']=='1'
  assert '|'+str(z['i'])+'|'+str(z['action'])+'|`'+json.dumps(z['terminal'],separators=(',',':'))+'`|`'+json.dumps(z['deviator_payoff'])+'`|' in sec
  lines.append(json.dumps(z,ensure_ascii=False,separators=(',',':')));punishments+=1
assert punishments==322 and (E/'report-full-reading.txt').read_text()=='\n'.join(lines)+'\n'
sc=read(E/'execution-and-counter-boundaries.json');assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_audit_runs','current_BI_replays','current_run_mode_replays','current_payoff_or_IC_rechecks','current_solver_runs','current_LP_runs','new_mathematical_implementation_runs'))
assert sc['historical_execution_manifest_present'] is False and sc['all_report_fields_transcribed'] is True and sc['run_states_include_terminal_and_BI_entries'] is True and sc['run_states_exclude_internal_bi_states'] is True and sc['explicit_comparisons_exclude_internal_bi'] is True and sc['explicit_comparisons_include_self'] is True and sc['H_tail_included'] is True and sc['full_ordered_action_policy_serialized'] is False and sc['original_has_main_guard'] is True and not (E/'runs').exists()
recs=read(W/'semantic-receipts.json');assert len(recs)==2 and {x['id'] for x in recs}==ids
for x in recs:
 assert x['disposition']=='retained' and all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for')) and all(x[k] for k in ('read_note','comparison_note','decision_note')) and all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
assert len(read(W/'relation-evidence.json'))==8 and read(W/'source-state-updates.json')==[]
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
result=dict(status='PASS',scope='source/hash/blob/normal metadata/owner/full22claim+3/2proof; comparison bytes/all report literals/322 integer vector domains and stored counter sums/receipts/content/links only; no audit/run/bi/pay/IC',primary_files=2,primary_bytes=77510,retained=2,duplicate=0,new_normal_show_files=2,formal_math_files=1,comparison_snapshots=7,related_MD_files=2,related_MD_bytes=14946,report_root_fields=5,parameter_records=21,fields_per_parameter=6,punishment_records=322,fields_per_punishment=4,stored_total_count_fields_checked=3,relations=8,source_state_updates=0,original_entry_runs=0,imports=0,audit_runs=0,BI_replays=0,run_mode_replays=0,payoff_or_IC_rechecks=0,solver_runs=0,LP_runs=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
