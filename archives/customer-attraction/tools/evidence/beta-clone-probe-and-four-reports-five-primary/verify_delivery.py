"""Integrity and literal stored report fields only. No original imports, Fraction, payoff, BI, random or LP."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-beta-clone-probe-and-four-reports-five-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(p):
 b=p.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
m=read(E/'actual-source-manifest.json');rows=m['rows'];ids={x['id'] for x in rows}
assert len(rows)==5 and sum(x['size'] for x in rows)==4796 and [x['size'] for x in rows]==[3048,128,1379,120,121]
c=read(E/'authoritative-full-claim.json');assert c['status']=='pushed' and c['operation']=='claim' and c['actor']=='Boss4' and len(c['ids'])==20 and ids<=set(c['ids'])
assert c['remote_tip']=='e6219d33a7cf892816a8195f0984e9c110f4d41a' and c['local_sync']['status']=='synced' and c['local_sync']==m['raw_original_local_sync']
assert rows[0]['exact_prior_normal_show_reused'] is True and rows[0]['no_new_normal_show_for_this_source'] is True and rows[0]['new_normal_show'] is False
assert sum(x['new_normal_show'] for x in rows)==4
for x in rows:
 p=S/x['stage_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and blob(p)==x['blob'] and p.read_bytes()==Path(x['local_path']).read_bytes() and x['full_file_reviewed'] is True
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name);assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')} and cap['output']==x['local_path']
 o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
prior=read(E/'prior-related-helper-manifest.json')['rows'];assert len(prior)==1
h=prior[0];assert h['id']==rows[0]['id'] and h['sha256']==rows[0]['sha256'] and h['full_file_reviewed'] is True and h['new_primary'] is False and h['new_done'] is False
assert read(E/'prior-related-normal-capture.json')==read(E/'normal-show-captures'/Path(rows[0]['actual_normal_show_capture']).name)
cm=read(E/'formal-comparison.json');assert len(cm)==10
for x in cm:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True
md=read(E/'related-MD-manifest.json');assert len(md)==3 and sum(x['bytes'] for x in md)==15826
for x in md:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True and x['new_primary'] is False and x['new_done'] is False
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
page=math[0].read_text();rs=read(E/'stored-reports-literal-transcription.json');assert len(rs)==4
assert [len(x['fields']) for x in rs]==[3,9,5,5] and sum(x['bytes'] for x in rs)==1748
for x,r in zip(rows[1:],rs):
 assert r['id']==x['id'] and r['fields']==read(S/x['stage_path']) and r['file']==Path(x['path']).name
 sec=page.split('### '+r['file']+'（'+str(r['bytes'])+'B）',1)[1].split('\n### ',1)[0]
 for k,v in r['fields'].items():assert '|'+k+'|`'+json.dumps(v,ensure_ascii=False,separators=(',',':'))+'`|' in sec
assert rs[0]['fields']=={'status':'no_candidate_in_finite_batch','checked':300,'scope':'No general conclusion; fixed candidate test only.'}
mix=rs[1]['fields'];assert list(mix)==['status','n','m','clones','types','original_spe','fresh_lift_failures','repeated_clone_spe','checked']
assert (mix['status'],mix['n'],mix['m'],mix['clones'],mix['checked'])==('candidate_found',3,3,3,141)
assert mix['types']==[[1,0,20],[2,1,3],[3,0,13],[4,2,12],[5,1,9],[6,1,14],[7,1,19]] and mix['original_spe']==[[2,0,1],[3,0,0]] and mix['fresh_lift_failures']==[]
assert mix['repeated_clone_spe']==[[0,0,2,0,0,0,0,0,1],[0,0,2,0,0,0,0,1,0],[0,0,2,0,0,0,1,0,0],[0,2,0,0,0,0,0,0,1],[0,2,0,0,0,0,0,1,0],[0,2,0,0,0,0,1,0,0],[2,0,0,0,0,0,0,0,1],[2,0,0,0,0,0,0,1,0],[2,0,0,0,0,0,1,0,0]]
names={1:'A',2:'B',3:'A,B',4:'C',5:'A,C',6:'B,C',7:'A,B,C'}
for b,old,w in mix['types']:assert f'|{b}|{names[b]}|{old}|{w}|' in page
for i,q in enumerate(mix['repeated_clone_spe'],1):assert '|'+str(i)+'|`'+json.dumps(q,separators=(',',':'))+'`|' in page
assert rs[2]['fields']=={'status':'no_candidate_in_finite_batch','n':3,'m':4,'checked':60,'scope':'No general conclusion.'}
assert rs[3]['fields']=={'status':'no_candidate_in_finite_batch','n':2,'m':4,'checked':100,'scope':'No general conclusion.'}
sc=read(E/'execution-and-version-boundaries.json');assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_BI_runs','current_random_samples','current_LP_runs','current_IC_runs','current_pattern_replays','current_unit_expansions','new_mathematical_implementation_runs'))
assert sc['historical_execution_manifest_present'] is False and sc['all_report_fields_transcribed'] is True and sc['primary_bytes']==4796 and sc['mixed_generated_by_current_default'] is False and sc['r4_generated_by_current_default'] is False and sc['default_negative_schema_compatible'] is True and sc['default_negative_historical_hash_binding'] is False and not (E/'runs').exists()
recs=read(W/'semantic-receipts.json');assert len(recs)==5 and {x['id'] for x in recs}==ids
for x in recs:
 assert x['disposition']=='retained' and all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for')) and all(x[k] for k in ('read_note','comparison_note','decision_note')) and all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
assert len(read(W/'relation-evidence.json'))==10 and read(W/'source-state-updates.json')==[]
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
result=dict(status='PASS',scope='source/metadata/blob/owner/full20claim, prior normal/fullread helper and comparison bytes, all 22 report literal fields/7types/2original/9repeated, receipts/content/links only; no payoff/BI/random/IC/LP',primary_files=5,primary_bytes=4796,retained=5,duplicate=0,new_normal_show_files=4,prior_normal_show_reused_files=1,formal_math_files=1,comparison_snapshots=10,related_MD_files=3,related_MD_bytes=15826,report_files=4,report_bytes=1748,total_report_fields=22,mixed_types=7,mixed_original_counts=2,mixed_repeated_counts=9,relations=10,source_state_updates=0,original_entry_runs=0,imports=0,BI_runs=0,random_samples=0,LP_runs=0,IC_runs=0,pattern_replays=0,unit_expansions=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
