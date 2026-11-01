"""Delivery/hash/report transcription only. No LP, payoff, IC, RNG or solver execution."""
from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-last-menu-background-accounting-and-fixed-cone-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
man=read(E/'actual-source-manifest.json');rows=man['rows'];ids={x['id'] for x in rows}
assert len(rows)==5 and sum(x['size'] for x in rows)==21646
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim'
assert len(claim['ids'])==13 and ids<=set(claim['ids']) and claim['local_sync']['status']=='synced'
assert claim['remote_tip']=='2a508218adffb99c77dfad21763a4c74591a5473'
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes()
 assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'] and x['full_file_reviewed'] is True
 d=read(E/'local-progress-at-read'/(x['id']+'.json'));assert d['owner']=='Boss4' and d['source_sha256']==x['sha256']
 assert (E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name).is_file()
rel=read(E/'actual-related-source-manifest.json');assert rel['related_only_no_extra_done'] is True and len(rel['rows'])==1
x=rel['rows'][0];assert x['id']=='6db461bb0f67ec447bf0' and x['id'] not in ids and x['size']==8302
p=S/x['stage_path'];b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'] and x['full_file_reviewed'] is True
assert (E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name).is_file()
old=read(p);assert old['instance']['players']==3 and len(old['instance']['topics'])==6 and len(old['instance']['customers'])==21
assert len(old['certificate']['actions'])==43 and old['certificate']['terminal_counts']==[1,0,0,1,1,0]
report=read(S/next(x['stage_path'] for x in rows if x['id']=='2cf1cd8a7bd7e3cd16ab'))
assert set(report)=={'scope','source','players','topics','actual','IC_rows','queries','best'}
assert report['source']=='research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_coupling/stationary_full_slot_counterexample_6286.json'
assert (report['players'],report['topics'],report['actual'],report['IC_rows'],report['queries'])==(3,6,[0,3,4],258,63)
best=report['best'];assert set(best)=={'gap','query','weights','price_rows'}
assert best['gap']==-0.04166666666666666 and best['query']==['0','1/4','1/4','0','1/4','1/4']
assert len(best['weights'])==63 and len(best['price_rows'])==6 and all(len(x)==63 for x in best['price_rows'])
program=S/'archives/customer-attraction/state/程序/三人完整策略末位锥的六十三均匀查询原诊断--程序.md'
txt=program.read_text()
for j in range(63):
 expected='| '+str(j+1)+' | '+repr(best['weights'][j])+' | '+' | '.join(row[j] for row in best['price_rows'])+' |'
 assert expected in txt,'report transcription row missing'
comp=read(E/'formal-comparison.json');assert len(comp)==12
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed'] is True
raw=read(E/'existing-related-full-read-manifest.json');assert len(raw)==3
for x in raw:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed'] is True
rr=read(W/'semantic-receipts.json');assert len(rr)==5 and {x['id'] for x in rr}==ids
assert sum(x['disposition']=='retained' for x in rr)==3 and sum(x['disposition']=='duplicate' for x in rr)==2
for x in rr:
 assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
scope=read(E/'execution-and-domain-boundaries.json')
assert all(scope[k]==0 for k in ('current_original_entry_runs','current_imports','current_LP_runs','current_RNG_replays','current_solver_runs','current_certificate_or_IC_replays','new_mathematical_implementation_runs','current_parameter_scans'))
assert scope['historical_full_runtime_manifest_present'] is False and scope['related_only_ids_not_done']==[rel['rows'][0]['id']]
assert not (E/'runs').exists() and read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==10
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
p=W/'copy-files.json'
if p.exists():assert read(p)==sorted(str(q.relative_to(S)) for q in S.rglob('*') if q.is_file())
result={'status':'PASS','scope':'raw claim/owner/source hashes/blob, related bytes/fields, complete frozen report transcription, comparison snapshots, receipts and links only; no mathematical replay','primary_files':5,'primary_bytes':21646,'normal_related_only_files':1,'normal_related_only_bytes':8302,'existing_related_full_read_files':3,'receipts':5,'retained':3,'duplicate':2,'formal_math_files':2,'comparison_snapshots':12,'relations':10,'source_state_updates':0,'original_entry_runs':0,'imports':0,'LP_runs':0,'RNG_replays':0,'solver_runs':0,'certificate_or_IC_replays':0,'new_mathematical_implementation_runs':0,'parameter_scans':0,'all_report_weights_transcribed':63,'all_report_price_strings_transcribed':378,'links_checked':links}
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
