"""Static publication checks only; never execute any mathematical audit/search."""
from pathlib import Path
from hashlib import sha256
from itertools import product
from fractions import Fraction
import argparse,ast,json,re

ER='archives/customer-attraction/tools/evidence/r8e450-counter-base-policy-and-ten-records'
OBJECTS=['archives/customer-attraction/state/计算/私题别名九客户的常值五人策略与索引对偶--计算.md','archives/customer-attraction/state/程序/单色目标可信策略锥的游走合同与十步保存边界--程序.md']

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--stage',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);args=ap.parse_args();stage,repo=args.stage.resolve(),args.repo.resolve();ev=stage/ER
 def read(p):return json.loads((ev/p).read_text())
 def digest(p):return sha256(p.read_bytes()).hexdigest()
 sources=read('source-manifest.json');related=read('related-source-manifest.json');assert len(sources)==3 and sum(s['size'] for s in sources)==800247
 assert len(related)==1 and related[0]['size']==2264
 byname={}
 for s in sources+related:
  p=stage/s['preserved_path'];assert p.stat().st_size==s['size'] and digest(p)==s['sha256'];byname[Path(s['path']).name]=p
  assert len(s['sources'])==2 and all(re.fullmatch('[0-9a-f]{40}',x['commit']) and x['path']==s['path'] for x in s['sources'])
  if p.suffix=='.py':ast.parse(p.read_text())
 assert 'for step in range(16)' in byname['cone_walk.py'].read_text()
 best=json.loads(byname['best_policy.json'].read_text());report=json.loads(byname['results.json'].read_text());assert best==report['records'][0]
 assert len(report['records'])==10 and report['scope'].startswith('10 ') and [r['step'] for r in report['records']]==list(range(10))
 view=read('lossless-full-reading.json');canonical=[{'history':list(h),'action':0} for d in range(5) for h in product(range(7),repeat=d)]
 def decode(v):
  if isinstance(v,dict) and set(v)=={'$constant_policy_actions'}:return canonical
  if isinstance(v,dict) and set(v)=={'$vector'}:
   spec=view['vector_dictionary'][v['$vector']];out=[spec['default']]*spec['length']
   for i,n in spec['nonzero']:out[i-1]=n
   return out
  if isinstance(v,dict):return {k:decode(x) for k,x in v.items()}
  if isinstance(v,list):return [decode(x) for x in v]
  return v
 assert decode(view['best_policy'])==best and decode(view['results'])==report
 assert len(view['vector_dictionary'])==3 and best['strategy']['actions']==canonical
 audit=read('fixed-audit.json');event=read('fixed-audit-execution.json')
 assert audit['status']=='PASS' and audit['proper_deviations']==16806 and audit['strict_proper']==16776 and audit['proper_ties']==30
 assert audit['unique_nonzero_sorted_IC_rows']==1260 and audit['W']==5 and audit['OPT']==9 and audit['ratio']=='9/5'
 assert len(audit['all_127_dual_residuals'])==127 and all(Fraction(x)>=0 for x in audit['all_127_dual_residuals'])
 assert audit['dual_zero_coefficients']==23 and audit['dual_positive_coefficients']==104
 assert [r['source_clients'] for r in audit['record_analysis']]==[11,9,9,911,11,9,9,911,11,9]
 assert event['exit_code']==0 and event['optimization_disabled'] and event['stderr_bytes']==0 and event['original_entry_executions']==event['LP_BI_random_searches']==0
 assert digest(ev/'audit-fixed-base.py')==event['script_sha256'];assert digest(ev/'audit-stdout.json')==event['stdout_sha256'];assert digest(ev/'audit-stderr.txt')==event['stderr_sha256']
 ast.parse((ev/'audit-fixed-base.py').read_text())
 deps=read('dependency-reuse-manifest.json');assert len(deps)==6 and sum(d['size'] for d in deps)==59284
 for d in deps:
  p=repo/d['reused_repo_path'];assert p.stat().st_size==d['size'] and digest(p)==d['sha256'];ast.parse(p.read_text())
 comparisons=read('comparison-bindings.json');assert len(comparisons)==8
 for b in comparisons:
  p=repo/b['path'];assert p.stat().st_size==b['bytes'] and digest(p)==b['sha256']
 units=read('semantic-units.json');assert set(units)=={s['id'] for s in sources} and set(units[sources[0]['id']]['all_fields'])==set(best)
 checked=[];table_rows=0
 for rel in OBJECTS+[ER+'/README.md']:
  body=(stage/rel).read_text()
  if rel in OBJECTS:
   assert body.startswith('---\n');fm=body.split('---',2)[1]
   for key in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+key+':',fm,re.M)
   assert len(re.findall(r'source:[0-9a-f]{40}:',fm))==[4,6][OBJECTS.index(rel)]
  columns=None
  for line in body.splitlines():
   if line.startswith('|'):
    n=len(line.split('|'))-2
    if columns is None:columns=n
    assert n==columns,(rel,line);table_rows+=1
   else:columns=None
  for target in re.findall(r'\]\(([^)]+)\)',body):
   if '://' in target or target.startswith('#'):continue
   relative=Path(rel).parent/target.split('#',1)[0];p=(stage/relative).resolve();own=p==(ev/'publication-check.json').resolve()
   if not p.exists() and not own:p=(repo/relative).resolve()
   assert p.exists() or own,(rel,target);checked.append([rel,target])
 receipts=json.loads((stage/'cleanup/workspaces/Boss2/receipts-r8e450-counter-base-three.json').read_text());required={'id','full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','disposition','targets'}
 assert {r['id'] for r in receipts}==set(units)
 for r in receipts:
  assert set(r)==required and r['disposition']=='integrated' and r['targets']==units[r['id']]['targets']
  assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
  assert all(r[k] for k in ['read_note','comparison_note','decision_note'])
 scope=read('execution-scope.json');assert scope['new_fixed_input_stdlib_audit_count']==1 and scope['original_cone_walk_execution_count']==scope['LP_BI_random_search_count']==0
 parsed=[]
 for p in sorted(stage.rglob('*.json')):
  if p==ev/'publication-check.json':continue
  json.loads(p.read_text());parsed.append(p.relative_to(stage).as_posix())
 result={'status':'PASS','scope':'static byte/structure/transcription/publication checks only; fixed mathematical audit not rerun','primary_source_count':3,'primary_source_bytes':800247,'related_source_count':1,'related_source_bytes':2264,'runtime_dependency_files':6,'runtime_dependency_bytes':59284,'full_comparison_objects':8,'lossless_roundtrip_equal':True,'original_records':10,'original_entry_planned_steps':16,'unique_saved_policies':1,'full_action_record_occurrences_read':5602,'formal_objects':2,'complete_primary_receipts':3,'prior_new_fixed_stdlib_event_bound':1,'original_entries_or_LP_BI_random_runs':0,'links_checked':len(checked),'table_rows_checked':table_rows,'parsed_json_paths':parsed,'limits':'records/static checks do not recover historical runtime, fill missing policies or prove a universal bound'}
 (ev/'publication-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');assert (ev/'publication-check.json').is_file()
 print(json.dumps({k:result[k] for k in ['status','primary_source_count','primary_source_bytes','runtime_dependency_files','original_records','formal_objects','complete_primary_receipts']},ensure_ascii=False))

if __name__=='__main__':main()
