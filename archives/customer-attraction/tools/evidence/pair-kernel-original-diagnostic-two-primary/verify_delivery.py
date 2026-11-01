"""Byte/provenance and reversible input-table structure plus literal report verification. Never import original code, Fraction, end, payoff, IC or H logic."""
from pathlib import Path
import json,hashlib,itertools,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-pair-kernel-original-diagnostic-two-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(p):
 b=p.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
m=read(E/'actual-source-manifest.json');rows=m['rows'];ids={x['id'] for x in rows};assert len(rows)==2 and sum(x['size'] for x in rows)==12583
c=read(E/'authoritative-full-claim.json');assert c['status']=='pushed' and c['operation']=='claim' and c['actor']=='Boss4' and len(c['ids'])==19 and ids<=set(c['ids'])
assert c['remote_tip']=='05a331e2e536aec72f2c75095d00992d1c26ac11' and c['local_sync']['status']=='synced' and c['local_sync']==m['raw_original_local_sync']
for x in rows:
 p=S/x['stage_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['local_path']).read_bytes() and x['full_file_reviewed'] is True and x['new_normal_show'] is True
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name);assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')} and cap['output']==x['local_path']
 o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
assert (S/rows[0]['stage_path']).parents[5]==E/'original'
runtime=read(E/'runtime-directory-manifest.json');deps=runtime['files'];assert len(deps)==51
assert sum(x['path'].startswith('examples/customer_attraction/') for x in deps)==22 and sum(x['path'].startswith('evidence/certificates/customer_attraction/') for x in deps)==29
assert sum(x['full_file_reviewed'] for x in deps)==18 and sum(x['selection_structure_only'] for x in deps)==33 and sum(x['size'] for x in deps if x['full_file_reviewed'])==1469006
old={x['path']:x for x in read(E/'prior-runtime-source-manifest.json')['frozen_sources']}
for x in deps:
 p=S/x['snapshot'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['new_primary'] is False and x['new_done'] is False
 assert all(x[k]==old[x['path']][k] for k in ('id','blob','size','sha256','sources'))
report=read(S/rows[1]['stage_path']);assert read(E/'stored-report-literal-transcription.json')==report
assert list(report)==['candidate','status','rows'] and report['candidate']=='all pairs symmetric extra-slot entries <= W' and report['status']=='exact finite diagnostics only' and len(report['rows'])==9
names=[x['instance'] for x in report['rows']];sel=read(E/'directory-selection-structure.json')['rows'];assert len(sel)==22 and sorted(x['instance'] for x in sel if x['selected'])==names
for x in sel:
 assert (S/x['input_snapshot']).is_file()
 if 'certificate_snapshot' in x:assert (S/x['certificate_snapshot']).is_file()
 if 'dictionary_entries' in x:assert x['selected']==(x['dictionary_entries']==x['expected_entries'])
depmap={x['path']:x for x in deps};views=read(E/'dependency-reading-manifest.json');assert len(views)==9 and [x['instance'] for x in views]==names
reading_lines=[];action_rows=0;viewdata={}
for x in views:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed'] is True
 view=read(p);viewdata[x['instance']]=view;obj=read(S/depmap['examples/customer_attraction/'+x['instance']]['snapshot']);cert=read(S/depmap['evidence/certificates/customer_attraction/'+x['instance']]['snapshot'])
 assert view['input']==obj and view['domain_structure_only_no_payoff_IC_run'] is True
 extras={k:v for k,v in cert.items() if k!='strategy'};extras['strategy_non_actions']={k:v for k,v in cert['strategy'].items() if k!='actions'};assert view['certificate_non_action_fields']==extras
 records=cert['strategy']['actions'];assert all(set(r)=={'history','action'} for r in records)
 acts={tuple(r['history']):r['action'] for r in records};k=len(obj['topics']);n=obj['players'];assert len(acts)==len(records) and set(acts)=={h for d in range(n) for h in itertools.product(range(k),repeat=d)} and all(type(a) is int and 0<=a<k for a in acts.values())
 assert [z['depth'] for z in view['strategy_layers']]==list(range(n))
 for z in view['strategy_layers']:
  assert z['lex_actions']==''.join(str(acts[h]) for h in itertools.product(range(k),repeat=z['depth']))
 action_rows+=len(records)
 reading_lines.append('CASE '+Path(x['instance']).stem+'\nINPUT '+json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\nCERT_ALL_NON_ACTION_FIELDS '+json.dumps(extras,ensure_ascii=False,separators=(',',':')))
 for z in view['strategy_layers']:reading_lines.append('ACTION_LAYER depth='+str(z['depth'])+' k='+str(k)+' count='+str(len(z['lex_actions']))+'\n'+z['lex_actions'])
assert action_rows==12222 and (E/'dependency-full-reading.txt').read_text()=='\n\n'.join(reading_lines)+'\n'
cm=read(E/'formal-comparison.json');assert len(cm)==6
for x in cm:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True
md=read(E/'related-MD-manifest.json');assert len(md)==1 and md[0]['size']==4969
for x in md:
 p=S/x['snapshot'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True and x['new_primary'] is False and x['new_done'] is False
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1;page=math[0].read_text();assert 'candidate="'+report['candidate']+'"' in page and 'status="'+report['status']+'"' in page
cells=0
for x in report['rows']:
 assert list(x)==['instance','m','W','queries','sym_entry','gap','H'] and len(x['queries'])==2
 k=len(x['H']);assert k==len(viewdata[x['instance']]['input']['topics']) and x['m']==viewdata[x['instance']]['input']['players'] and all(len(t)==k for t in x['H'])
 sec=page.split('### '+x['instance'],1)[1].split('\n### ',1)[0]
 for i,t in enumerate(x['H']):assert '|'+str(i)+'|'+'|'.join(t)+'|' in sec
 cells+=sum(len(t) for t in x['H'])
 a,t=x['queries'];num=sum(len(z['lex_actions']) for z in viewdata[x['instance']]['strategy_layers'])
 line='|'+'|'.join(map(str,[x['instance'],x['m'],k,num,x['W'],','.join(map(str,x['queries'])),x['H'][a][t],x['H'][t][a],x['sym_entry'],x['gap']]))+'|';assert line in page
assert cells==381
sc=read(E/'execution-and-domain-boundaries.json');assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_SPE_IC_runs','current_end_path_replays','current_H_recomputations','current_solver_runs','current_LP_runs','new_mathematical_implementation_runs'))
assert sc['historical_execution_manifest_present'] is False and sc['all_report_fields_transcribed'] is True and sc['candidate_assertion_in_original'] is False and sc['original_strategy_domain_check_is_only_cardinality'] is True and sc['directory_filter_structure_only'] is True and sc['current_dependency_structure_checked'] is True and sc['all_SPEs_enumerated'] is False and not (E/'runs').exists()
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
result=dict(status='PASS',scope='source/hash/blob/normal metadata/owner/full19claim; runtime bytes and reversible all-field/all-action domain structure; all literal 381 H/report fields/receipts/content/links; no Fraction/payoff/end/IC/H/solver',primary_files=2,primary_bytes=12583,retained=2,duplicate=0,new_normal_show_files=2,formal_math_files=1,comparison_snapshots=6,related_MD_files=1,related_MD_bytes=4969,runtime_directory_JSON_files=51,full_read_input_certificate_files=18,full_read_input_certificate_bytes=1469006,full_read_action_rows=12222,filter_only_files=33,report_root_fields=3,report_case_rows=9,fields_per_case=7,H_string_cells=381,relations=8,source_state_updates=0,original_entry_runs=0,imports=0,SPE_IC_runs=0,end_path_replays=0,H_recomputations=0,solver_runs=0,LP_runs=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
