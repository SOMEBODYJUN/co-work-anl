"""Static source/event/report/links checks; never executes original or audit code."""
from pathlib import Path
import ast,hashlib,json,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
P='archives/customer-attraction/'
DOCS=[ROOT/P/'state/程序/两组阶段策略的两步静态安全锥筛选程序--程序.md',ROOT/P/'state/计算/两组阶段策略的保存点与大块等号校准--计算.md']
IDS=['c4616678f5d7191b9eda','6711d93cafa8986dbff9','7321941d4775384d68a5']
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fp(p):return {'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)}
manifest=load(HERE/'source-manifest.json')
assert manifest['primary_ids']==IDS and len(manifest['sources'])==7 and manifest['total_source_bytes']==463242
assert manifest['original_main_calls']==manifest['original_function_calls']==manifest['LP_calls']==manifest['full_IC_matrix_recomputations']==0
assert manifest['new_data_structure_audit_calls']==1 and manifest['new_scalar_bound_comparisons']==10
src=[];astn=jsonn=0
for row in manifest['sources']:
 p=ROOT/row['preserved_at'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
 assert len(row['sources'])==2
 if p.suffix=='.py':ast.parse(p.read_text());astn+=1
 if p.suffix=='.json':load(p);jsonn+=1
 src.append(fp(p))
assert astn==4 and jsonn==2
event=load(HERE/'execution.json');report=load(HERE/'reported-data-audit.json')
for key,p in [('script',HERE/'audit_phase_records.py'),('report',HERE/'reported-data-audit.json')]:
 row=event[key];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
assert event['data_structure_audit_calls']==1 and event['scalar_root_bound_comparisons']==10
for key in ['original_function_calls','LP_calls','new_payoff_tables','new_full_history_IC_comparisons','DP_calls']:assert event[key]==0
assert report['status']=='PASS_DATA_AND_FULL_POLICY_STRUCTURE' and len(report['records'])==2
for i,(n,k,phases,nodes,failures) in enumerate([(4,8,48,585,2),(5,7,96,2801,55)]):
 p=HERE/'original'/f'phase_n{n}k{k}.json';x=load(p);r=report['records'][i]
 assert p.stat().st_size==r['source']['bytes'] and sha(p)==r['source']['sha256']
 row=event['source_inputs'][i];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
 assert len(x)==r['top_field_count']==7 and len(x['best'])==r['best_field_count']==9
 assert x['completed']==len(x['phases'])==len(r['all_phase_rows'])==phases
 assert x['n']==r['n']==n and x['k']==r['k']==k
 assert len(x['best']['policy'])==r['full_policy_nodes']==nodes
 assert r['reported_initial_LP_unsuccessful']==failures
 assert r['all_history_keys_in_expected_order'] and r['phase_rule_matches_every_stored_action'] and r['all_prescribed_actions_cover_big_block']
 raw=json.loads(p.read_text(),parse_float=str)
 assert r['weight_literals']==raw['best']['weights']
 assert [v['recorded'] for v in r['all_phase_rows']]==raw['phases']
 assert r['saved_gap_literal']==raw['best']['gap'] and r['saved_phase']==raw['best']['phase']
 assert r['literal_total_weight_minus_one']==('0' if n==4 else '1/12500000000000000')
 assert r['binary_exact_total_weight_minus_one']=='1/18014398509481984'
 assert len(r['scalar_root_bounds'])==(1 if n==4 else 4)
 assert all(z['decimal_big_over_n_minus_private']=='0' for z in r['scalar_root_bounds'])
 assert all(z['binary_big_over_n_minus_private']==('0' if n==4 else '-1/360287970189639680') for z in r['scalar_root_bounds'])
review=load(HERE/'review-record.json')
for row in review['formal_comparisons']:
 p=ROOT/row['path'];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
receipts=[]
for sid in IDS:
 p=ROOT/'cleanup/workspaces/Boss7/receipts-round21'/f'{sid}.json';x=load(p)
 assert x['id']==sid and x['disposition']=='integrated'
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert set(x['targets'])=={str(d.relative_to(ROOT)) for d in DOCS};receipts.append(p)
links=[]
for p in DOCS+[HERE/'README.md']:
 for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
  if href.startswith(('http:','https:','#','source:')):continue
  target=(p.parent/href.split('#')[0]).resolve()
  assert target.exists() or target==HERE/'self-check.json',(str(p),href)
  links.append({'source':str(p.relative_to(ROOT)),'target':str(target.relative_to(ROOT))})
files=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='self-check.json')
for p in files+receipts:
 if p.suffix=='.py':ast.parse(p.read_text())
 if p.suffix=='.json':load(p)
result={'status':'PASS_STATIC_ONLY','sources':src,'primary_sources':3,'related_sources':4,'source_ast_files':astn,'source_json_files':jsonn,
 'source_bytes':463242,'formal_comparisons':len(review['formal_comparisons']),'phase_rows':[48,96],'policy_nodes':[585,2801],
 'literal_and_binary_scalar_bounds':'Read existing sole audit, no recomputation','links':links,'local_links':len(links),
 'artifacts':[fp(p) for p in files+DOCS+receipts],'self_hash_excluded':True,'original_runs_in_static_check':0,'audit_reruns_in_static_check':0,'new_mathematical_runs_in_static_check':0}
(HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','primary_sources','related_sources','source_bytes','local_links','new_mathematical_runs_in_static_check']}))
