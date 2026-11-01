"""Static archive checks only: no research imports, solver, payoff or Fraction calls."""
from pathlib import Path
import ast,hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
DOC=ROOT/'archives/customer-attraction/state/程序/三人笛卡尔编译菜单的固定种子客户锥--程序.md'
IDS=['efa605cb5b3bb7506f54','fc3fb90ca9e58f0da046']
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return {'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)}
manifest=load(HERE/'source-manifest.json')
assert manifest['primary_ids']==IDS
assert len(manifest['sources'])==6 and manifest['total_source_bytes']==27732
sourcebindings=[];names={};astcount=jsoncount=0
for row in manifest['sources']:
 p=ROOT/row['preserved_at'];names[p.name]=p
 assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
 assert len(row['sources'])==2
 if p.suffix=='.py':ast.parse(p.read_text());astcount+=1
 if p.suffix=='.json':load(p);jsoncount+=1
 sourcebindings.append(bind(p))
assert astcount==2 and jsoncount==2
data=load(names['cartesian_compiler_cone_k4.json'])
inputdata=load(names['cartesian_convexification_k4.json'])
assert len(data)==12 and len(data['seed'])==18
assert data['seed']==inputdata['analysis']
assert data['k']==4 and data['rows']==108 and data['success'] is True
assert len(data['weights'])==15 and len(data['second_floors'])==4
assert len(data['seed']['weights'])==15 and len(data['seed']['root_minimizers'])==4
assert [len(m) for m in data['seed']['root_minimizers']]==[1,1,2,2]
assert len(data['seed']['actual_mix'])==3 and len(data['seed']['query'])==4 and len(data['seed']['opponent'])==3
assert (HERE/'original/cartesian_compiler_cone_k4.json').read_bytes()==(HERE/'replay/cartesian_compiler_cone_k4.json').read_bytes()
execution=load(HERE/'replay/execution.json')
assert execution['original_call_counts']=={'cone_main':1,'cone_function':1,'linprog':1,'limit_analyze':0,'limit_main':0}
assert execution['error'] is None and execution['assertions_enabled'] is True
assert execution['finite_calls']==execution['independent_mathematical_audits']==execution['normalization_or_helper_replacements']==0
assert execution['inputs_before']==execution['inputs_after']
for row in execution['inputs_before']:
 p=names[Path(row['path']).name]
 assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
for field,target in [('observer',HERE/'run_original_once.py'),('capture',HERE/'replay/capture.json'),('stdout',HERE/'replay/stdout.txt'),('stderr',HERE/'replay/stderr.txt'),('new_report',HERE/'replay/cartesian_compiler_cone_k4.json')]:
 row=execution[field];assert target.stat().st_size==row['bytes'] and sha(target)==row['sha256']
assert (HERE/'replay/stderr.txt').read_bytes()==b''
cap=load(HERE/'replay/capture.json');model=cap['model'];lp=cap['linprog_inputs']
assert cap['cone_return']==data
assert model['k']==4 and model['d']==15
assert len(model['rows'])==108 and all(len(r)==21 for r in model['rows'])
assert len(model['obj'])==len(model['eq'])==len(model['bounds'])==21
assert lp['A_ub']==model['rows'] and lp['c']==model['obj'] and lp['A_eq']==[model['eq']]
assert len(cap['needed_iteration_order'])==18 and len(cap['last_replies'])==16
assert len(cap['payoff_coefficients'])==len(cap['seed_payoffs'])==64
assert all(len(r['matrix'])==4 and all(len(v)==15 for v in r['matrix']) for r in cap['payoff_coefficients'])
assert len(cap['linprog_return']['x'])==21 and cap['linprog_return']['status']==0
assert cap['linprog_return']['nit']==28
assert load(HERE/'replay/process-observation.json')['tool_observed_exit_code']==0
review=load(HERE/'review-record.json')
for key in ['formal_comparisons','shared_core_assets']:
 for row in review[key]:
  p=ROOT/row['path'];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
receipts=[]
for sid in IDS:
 p=ROOT/'cleanup/workspaces/Boss7/receipts-round20'/f'{sid}.json';r=load(p)
 assert r['id']==sid and r['disposition']=='integrated'
 assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert r['targets']==[str(DOC.relative_to(ROOT))];receipts.append(p)
links=[]
for p in [DOC,HERE/'README.md']:
 for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
  if href.startswith(('http:','https:','#','source:')):continue
  target=(p.parent/href.split('#')[0]).resolve()
  assert target.exists() or target==HERE/'self-check.json',(str(p),href)
  links.append({'source':str(p.relative_to(ROOT)),'target':str(target.relative_to(ROOT))})
own=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='self-check.json')
for p in own+receipts:
 if p.suffix=='.py':ast.parse(p.read_text())
 if p.suffix=='.json':load(p)
result={'status':'PASS_STATIC_ONLY','source_bindings':sourcebindings,'primary_sources':2,'related_sources':4,
 'source_ast_files':astcount,'source_json_files':jsoncount,'top_fields':12,'seed_fields':18,
 'capture_dimensions':[108,21],'original_call_counts':execution['original_call_counts'],
 'original_output_byte_identical':True,'formal_comparisons':len(review['formal_comparisons']),
 'shared_core_assets':len(review['shared_core_assets']),'links':links,'local_links':len(links),
 'artifacts':[bind(p) for p in own+[DOC]+receipts],'self_hash_excluded':True,
 'new_original_runs_in_static_check':0,'new_math_runs_in_static_check':0}
(HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','primary_sources','related_sources','capture_dimensions','original_output_byte_identical','local_links','new_math_runs_in_static_check']}))
