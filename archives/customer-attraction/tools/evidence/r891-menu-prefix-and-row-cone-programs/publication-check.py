"""Static publication checks only; no original import, LP, BI or SPE run."""
from pathlib import Path
from hashlib import sha256
from math import comb
import argparse, ast, json, re

ER='archives/customer-attraction/tools/evidence/r891-menu-prefix-and-row-cone-programs'
OBJECTS=[
 'archives/customer-attraction/state/程序/逐人完整菜单的集合续局与计数策略客户锥探针--程序.md',
 'archives/customer-attraction/state/程序/全前缀残余覆盖与尾部利润的精确有限探针--程序.md',
 'archives/customer-attraction/state/程序/真实查询行固定客户锥的比较极点与有限阴性账--程序.md']

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--stage',type=Path,required=True);parser.add_argument('--repo',type=Path,required=True);args=parser.parse_args()
 stage,repo=args.stage.resolve(),args.repo.resolve();ev=stage/ER
 def read(p):return json.loads((ev/p).read_text())
 def digest(p):return sha256(p.read_bytes()).hexdigest()
 sources=read('source-manifest.json');related=read('related-source-manifest.json')
 assert len(sources)==5 and sum(s['size'] for s in sources)==15660
 assert len(related)==2 and sum(s['size'] for s in related)==2850
 for s in sources+related:
  p=stage/s['preserved_path'];assert p.stat().st_size==s['size'] and digest(p)==s['sha256']
  assert len(s['sources'])==2 and all(re.fullmatch('[0-9a-f]{40}',x['commit']) and x['path']==s['path'] for x in s['sources'])
  if p.suffix=='.py':ast.parse(p.read_text())
 deps=read('dependency-reuse-manifest.json')['files'];assert len(deps)==14 and sum(d['size'] for d in deps)==1417104
 for d in deps:
  p=repo/d['reused_repo_path'];assert p.stat().st_size==d['size'] and digest(p)==d['sha256']
  if p.suffix=='.py':ast.parse(p.read_text())
  else:json.loads(p.read_text())
 for b in read('comparison-bindings.json'):
  p=repo/b['path'];assert p.stat().st_size==b['bytes'] and digest(p)==b['sha256']
 units=read('semantic-units.json');assert set(units)=={s['id'] for s in sources}
 assert all(len(v['units'])>=6 and (stage/v['target']).is_file() for v in units.values())
 report=json.loads((stage/next(s['preserved_path'] for s in sources if s['id']=='4a0117aafc16525bb945')).read_text())
 assert len(report)==5 and sum(r.get('tested',0) for r in report)==520
 assert [r.get('tested') for r in report]==[56,222,222,None,20]
 assert report[3]['status']=='not_run_resource_bound' and set(report[3])=={'fixture','status','reason'}
 assert all(r['maximum_proposal']<0 for r in report if 'maximum_proposal' in r)
 fixtures=read('fixture-input-reading.json');assert [f['policy_records'] for f in fixtures]==[43,259,259,11111,21]
 assert [f['unit_clients'] for f in fixtures]==[34,89,61,86,8]
 for f in fixtures:
  k,m=f['topic_count'],f['players'];assert f['policy_depth_counts']==[k**d for d in range(m)]
  assert f['proper_IC_rows_if_cone_built']==(k-1)*sum(f['policy_depth_counts'])
  expected=(m-2)*(sum(s*comb(k,s) for s in range(1,min(m-1,k)+1))+(comb(k,m) if m<=k else 0))
  record=next(r for r in report if r['fixture']==f['fixture'])
  if k<=6:assert record['tested']==expected and record['actual']==f['actual_from_original_policy']
 checked_links=[];table_rows=0
 for rel in OBJECTS+[ER+'/README.md']:
  body=(stage/rel).read_text()
  if rel in OBJECTS:
   assert body.startswith('---\n');fm=body.split('---',2)[1]
   for key in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+key+':',fm,re.M)
   assert len(re.findall(r'source:[0-9a-f]{40}:',fm))==([4,2,4][OBJECTS.index(rel)])
  columns=None
  for line in body.splitlines():
   if line.startswith('|'):
    n=len(line.split('|'))-2
    if columns is None:columns=n
    assert n==columns,(rel,line);table_rows+=1
   else:columns=None
  for target in re.findall(r'\]\(([^)]+)\)',body):
   if '://' in target or target.startswith('#'):continue
   relative=Path(rel).parent/target.split('#',1)[0];p=(stage/relative).resolve();self_result=p==(ev/'publication-check.json').resolve()
   if not p.exists() and not self_result:p=(repo/relative).resolve()
   assert p.exists() or self_result,(rel,target);checked_links.append([rel,target])
 receipts=json.loads((stage/'cleanup/workspaces/Boss2/receipts-r891-menu-five.json').read_text())
 required={'id','full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','disposition','targets'}
 assert {r['id'] for r in receipts}==set(units)
 for r in receipts:
  assert set(r)==required and r['disposition']=='integrated' and r['targets']==[units[r['id']]['target']]
  assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
  assert all(r[k] for k in ['read_note','comparison_note','decision_note'])
 scope=read('execution-and-output-scope.json');assert scope['original_entry_executions']==scope['original_imports']==scope['LP_BI_random_SPE_replays']==0
 parsed=[]
 for p in sorted(stage.rglob('*.json')):
  if p==ev/'publication-check.json':continue
  json.loads(p.read_text());parsed.append(p.relative_to(stage).as_posix())
 result={'status':'PASS','scope':'static publication/byte/transcription check; no original or canonical execution','primary_source_count':5,'primary_source_bytes':15660,'related_source_count':2,'related_source_bytes':2850,'reused_dependencies':14,'reused_dependency_bytes':1417104,'comparison_bindings':10,'original_Python_AST_only':4,'canonical_dependency_Python_AST_only':4,'formal_objects':3,'native_row_records':5,'reported_float_LP_total':520,'reported_dense_cone_skips':1,'native_results_other_three_supplied':False,'new_mathematical_executions':0,'complete_primary_receipts':5,'links_checked':len(checked_links),'table_rows_checked':table_rows,'parsed_json_paths':parsed,'limits':'byte/record consistency does not prove all cones, certify missing outputs, repeat old SPE audits or satisfy parent remote gate'}
 (ev/'publication-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');assert (ev/'publication-check.json').is_file()
 print(json.dumps({k:result[k] for k in ['status','primary_source_count','primary_source_bytes','reused_dependencies','formal_objects','reported_float_LP_total','new_mathematical_executions','complete_primary_receipts']},ensure_ascii=False))

if __name__=='__main__':main()
