"""Source integrity, literal report transcription/equality and links only; no Fraction or game evaluation."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-parent-unit-expanded-optimal-prefix-bill-audit-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=read(E/'actual-source-manifest.json');rows=manifest['rows'];ids={x['id'] for x in rows}
assert len(rows)==2 and sum(x['size'] for x in rows)==28547
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4' and len(claim['ids'])==14
assert ids<=set(claim['ids']) and claim['remote_tip']=='cd907bef110ecf9ee96b79943fab8d55c114eed5'
assert claim['local_sync']['status']=='synced' and manifest['raw_original_local_sync']==claim['local_sync']
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
 assert x['full_file_reviewed'] is True and x['new_normal_show'] is True
 owner=read(E/'local-progress-at-read'/(x['id']+'.json'))
 assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==x['sha256']
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name)
 assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')} and cap['output']==x['local_path']
comp=read(E/'formal-comparison.json');assert len(comp)==8
available={x['path'] for x in comp}
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes()
 assert x['full_file_reviewed'] is True and x['publication_at_read'] in ('existing-repository-object','frozen-direct-stage-being-integrated-by-Root')
md=read(E/'related-MD-manifest.json');assert len(md)==3 and sum(x['bytes'] for x in md)==19911
for x in md:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes()
 assert x['full_file_reviewed'] is True and x['new_primary'] is False and x['new_done'] is False
fixtures=read(E/'related-fixed-fixture-manifest.json');assert len(fixtures)==2 and sum(x['bytes'] for x in fixtures)==24196
old={x['repository_path']:x for x in read(E/'previous-full-fixture-reading-manifest.json')}
source=read(E/'previous-fixed-input-source-manifest.json')['files']
for x in fixtures:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes()
 assert x['full_file_reviewed'] is True and x['exact_previous_full_reading_reused'] is True and x['new_done'] is False
 assert old[x['repository_path']]['sha256']==x['sha256'] and old[x['repository_path']]['full_file_reviewed'] is True
 assert any(y['sha256']==x['sha256'] and y['size']==x['bytes'] for y in source)
ds=read(E/'direct-related-manifest.json');assert len(ds)==2 and sum(x['size'] for x in ds)==22334
for x in ds:
 p=S/x['snapshot'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes()
 assert x['new_primary'] is False and x['new_done'] is False and x['exact_previous_full_reading_reused'] is True
receipts=read(W/'semantic-receipts.json');assert len(receipts)==2 and {x['id'] for x in receipts}==ids
for x in receipts:
 assert x['disposition']=='retained' and all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() or t in available for t in x['targets'])
sc=read(E/'execution-and-domain-boundaries.json')
assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_SPE_replays','current_IC_replays','current_coverage_replays','current_permutation_replays','current_LP_runs','current_RNG_replays','current_solver_runs','new_mathematical_implementation_runs'))
assert sc['literal_stored_record_comparison_only'] is True and sc['historical_execution_manifest_present'] is False and not (E/'runs').exists()
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==9
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
page=math[0].read_text();p=read(S/rows[1]['stage_path']);d=read(S/ds[1]['snapshot'])
assert read(E/'stored-parent-report-literal-transcription.json')==p
assert len(p)==18 and set(p)=={'candidate','status','source_sha256','players','labels','unit_customers','histories','spe_comparisons_including_self','actual','actual_payoffs','W','OPT','optimal_multisets','ordered_optima','bills_checked','minimum_bill','gap','rows'}
assert len(p['source_sha256'])==2 and len(p['rows'])==24
expected_meta={'candidate':'exists optimal multiset and ordering with forced-optimal-prefix bill <= actual W','status':'refuted; not a Q-CAG-HALF counterexample','players':4,'labels':6,'unit_customers':22,'histories':259,'spe_comparisons_including_self':1554,'actual':[1,2,2,2],'actual_payoffs':['15/4','41/12','41/12','41/12'],'W':14,'OPT':22,'optimal_multisets':[[0,3,4,5]],'ordered_optima':24,'bills_checked':24,'minimum_bill':'193/12','gap':'25/12'}
for k,v in expected_meta.items():assert p[k]==v
for key,v in p['source_sha256'].items():
 assert f'|{key}|{v}|' in page
 assert any(x['sha256']==v and x['path']==key for x in source)
 assert any(x['sha256']==v for x in fixtures)
for k in ('candidate','status'):assert p[k] in page
for r in p['rows']:
 assert set(r)=={'order','bill','steps'} and len(r['steps'])==4
 for i,z in enumerate(r['steps']):
  assert set(z)=={'prefix','terminal','charge'}
  line='|'+'|'.join([','.join(map(str,r['order'])),r['bill'],str(i+1),','.join(map(str,z['prefix'])),','.join(map(str,z['terminal'])),z['charge']])+'|'
  assert line in page,line
cross=read(E/'literal-direct-parent-comparison.json')
assert cross['ordered_records']==24 and cross['step_records']==96 and len(cross['rows'])==24
assert cross['parent_report_sha256']==rows[1]['sha256'] and cross['direct_report_sha256']==ds[1]['sha256']
assert all(cross[k] is True for k in ('all_order_lists_equal','all_bill_strings_equal','all_terminal_arrays_equal','all_charge_strings_equal','all_explicit_prefixes_equal_to_order_slices'))
assert p['actual']==d['actual'] and p['W']==d['W'] and p['OPT']==d['OPT'] and p['players']==d['m'] and p['labels']==d['p']
assert p['histories']==d['nodes'] and p['spe_comparisons_including_self']==d['comparisons'] and p['minimum_bill']==d['optimal_multisets'][0]['min']
for p0,d0,c0 in zip(p['rows'],d['optimal_multisets'][0]['all_orders'],cross['rows']):
 assert p0['order']==d0['order']==c0['order'] and p0['bill']==d0['D'] and c0['bill_string_equal'] is True
 for i,(step,out) in enumerate(zip(p0['steps'],c0['steps'])):
  assert step['prefix']==p0['order'][:i+1]==out['prefix'] and out['step']==i+1
  assert step['terminal']==d0['forced_rollouts'][i] and step['charge']==d0['forced_payoffs'][i]
  assert out['terminal_equal'] is True and out['charge_equal'] is True
links=0
for path in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(path.parent/target.split('#',1)[0]).resolve()
  if not q.is_file():
   rel=str(q.relative_to(S));assert (R/rel).is_file() or rel in available,(str(path),target)
  links+=1
for x in read(E/'content-manifest.json'):
 pth=S/x['path'];assert pth.stat().st_size==x['bytes'] and sha(pth)==x['sha256']
pth=W/'copy-files.json'
if pth.exists():assert read(pth)==sorted(str(q.relative_to(S)) for q in S.rglob('*') if q.is_file())
result=dict(status='PASS',scope='source/hash/blob/normal owner/fullclaim, prior reading and input hash closure, all literal stored record fields/cross-equality, semantic receipts and links only; no mathematical replay',primary_files=2,primary_bytes=28547,new_normal_show_files=2,retained=2,duplicate=0,formal_math_files=1,comparison_snapshots=8,related_MD_files=3,related_fixed_fixtures=2,direct_related_originals=2,parent_report_fields=18,parent_order_rows=24,parent_step_records=96,relations=9,source_state_updates=0,original_entry_runs=0,imports=0,SPE_replays=0,IC_replays=0,coverage_replays=0,permutation_replays=0,LP_runs=0,RNG_replays=0,solver_runs=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
