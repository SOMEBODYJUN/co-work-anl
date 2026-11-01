"""Static package/source/event/ledger validation only; no mathematical program execution."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import ast,gzip,hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BODY=ROOT/'archives/customer-attraction/state/程序/合法背景首两人安全比的有限探针与三个取等点--程序.md'
IDS=['56a9a59d1fbb6e4fc251','a2fa48f528a1ebd057f9','4607167ef0609cb55fe5','edc7c24d9b8845dae698']
def read(p):return json.loads(p.read_text())
def verify(p,row):
 b=p.read_bytes();assert len(b)==row.get('bytes',row.get('size')),str(p)
 assert hashlib.sha256(b).hexdigest()==row['sha256'],str(p)
def main():
 own=read(HERE/'artifact-manifest.json')['files']
 for item in own:verify(ROOT/item['path'],item)
 sources=read(HERE/'source-manifest.json')['sources']
 assert sorted(x['id']for x in sources if x['role']=='primary')==sorted(IDS)
 for item in sources:
  verify(ROOT/item['preserved_path'],item);assert item['full_file_reviewed'] is True
 compared=read(HERE/'comparison-manifest.json')['files']
 for item in compared:verify(ROOT/item['path'],item)
 sibling=read(HERE/'review-record.json')['sibling_source_read'];verify(ROOT/sibling['preserved_path'],sibling)
 jsons=sorted(x for x in HERE.rglob('*.json')if x.name!='self-check.json')
 for p in jsons:read(p)
 pys=sorted(HERE.rglob('*.py'))
 for p in pys:ast.parse(p.read_text(),filename=str(p))
 header=BODY.read_text().split('---',2)[1]
 for name in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+name+':',header,re.M),name
 links=[]
 for p in [BODY,HERE/'README.md']:
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
   target=target.strip('<>').split('#',1)[0]
   if not target or re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',target):continue
   assert (p.parent/target).resolve().exists() or (p.parent/target).resolve()==HERE/'self-check.json',(str(p),target)
   links.append({'document':str(p.relative_to(ROOT)),'target':target})
 event=read(HERE/'replay/execution.json');exact_event=read(HERE/'exact/execution.json')
 mapping={'run_saved_points.py':HERE/'run_saved_points.py','audit_saved_points.py':HERE/'audit_saved_points.py','background_pair_probe.py':HERE/'original/background_pair_probe.py','search_background.py':ROOT/next(x['preserved_path']for x in sources if x['role']=='actual-runtime-dependency-only'),'saved-point-capture.json':HERE/'replay/saved-point-capture.json'}
 for p in (HERE/'original').glob('*.json'):mapping[p.name]=p
 for row in event['bindings']+exact_event['inputs']:verify(mapping[Path(row['path']).name],row)
 for row in event['outputs']:verify(HERE/'replay'/row['path'],row)
 for row in exact_event['outputs']:verify(HERE/'exact'/row['path'],row)
 assert event['exit_code']==exact_event['exit_code']==0
 assert event['assertions_enabled'] is exact_event['assertions_enabled'] is True
 assert event['counts']=={'original_main':0,'random_trials':0,'BackgroundSolver':3,'minimum_pair':3,'security':3,'linprog':3,'new_complete_strategy_extractions':3}
 captures=read(HERE/'replay/saved-point-capture.json');lps=read(HERE/'replay/lp-capture.json');audit=read(HERE/'exact/exact-audit.json')
 ledgers=json.loads(gzip.decompress((HERE/'exact/full-history-ledger.json.gz').read_bytes()))
 assert audit['status']=='PASS'and len(captures)==len(lps)==len(audit['cases'])==len(ledgers)==3
 assert audit['counts']=={'original_imports':0,'original_helpers':0,'BI':0,'LP':0,'RNG':0,'fixed_inputs':3,'unit_customers':291,'all_action_comparisons':21419,'ordered_decision_histories':3103,'static_opponent_rows':3,'static_query_entries':19}
 fractions=0;history_count=0;comparison_count=0;state_count=0
 expected_fields={'trial','q','r','seed','prefix','weights','pair','witness','v','p','ratio','status'}
 for cap,point,lp,ledger in zip(captures,audit['cases'],lps,ledgers):
  raw=read(HERE/'original'/cap['source']);assert set(raw)==expected_fields
  assert cap['source']==point['source']==ledger['source']
  assert all(cap[k]==raw[k]for k in ['pair','witness','v','p','ratio'])
  assert cap['initial_solve_cache']['misses']==cap['initial_solve_cache']['currsize']==len(cap['count_states'])
  assert len(cap['terminals'])==len(cap['scaled_topic_payoffs'])==len(cap['remaining_total_profits'])==point['terminal_count_vectors']
  state_count+=len(cap['count_states'])
  assert cap['count_states'][0]['counts']==[0]*raw['q']and int(cap['count_states'][0]['outcomes_bitset_hex'],16).bit_count()==1
  policy={tuple(h):a for h,a in cap['strategy']}
  assert len(policy)==len(cap['strategy'])==point['ordered_decision_histories']
  assert set(policy.values())=={point['pure_query']}
  assert raw['p'][point['pure_query']]==1 and sum(raw['p'])==1
  rows=ledger['all_ordered_history_checks'];assert len(rows)==point['all_action_comparisons']
  assert set(tuple(x['history'])for x in rows)==set(policy)
  assert Counter(tuple(x['history'])for x in rows)==Counter({h:raw['q']for h in policy})
  zero=positive=0
  for row in rows:
   assert row['chosen']==policy[tuple(row['history'])]
   for key in ['prescribed_payoff','deviation_payoff','slack']:
    assert str(Fraction(row[key]))==row[key];fractions+=1
   slack=Fraction(row['slack']);assert slack>=0
   if slack==0:zero+=1;assert row['deviation']==row['chosen']
   else:positive+=1
  assert zero==point['zero_slack']==len(policy)and positive==point['positive_slack']==point['nonself_comparisons']
  assert all(Fraction(x)>0 for i,x in enumerate(point['static_pure_dual_slacks'])if i!=point['pure_query'])
  assert point['static_pure_dual_slacks'][point['pure_query']]=='0'
  assert point['exact_ratio']=='1'and point['exact_minimum_first_pair']==raw['pair']
  assert lp['result']['status']==0 and lp['result']['success']is True
  assert lp['result']['x'][:-1]==cap['p']and lp['result']['x'][-1]==cap['v']
  assert len(lp['c'])==raw['q']+1 and len(lp['A_ub'])in [21,56,210]
  history_count+=len(policy);comparison_count+=len(rows)
 assert (history_count,comparison_count,state_count,fractions)==(3103,21419,1086,64257)
 scope=read(HERE/'execution-scope.json');assert scope['extra_mathematical_reruns']==scope['mature_counterexample_reruns']==0
 receipt_targets=0
 for source_id in IDS:
  receipt=read(ROOT/f'cleanup/workspaces/Boss7/receipts-round20/{source_id}.json')
  assert receipt['id']==source_id and receipt['disposition']=='integrated'
  for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert receipt[k]is True
  for target in receipt['targets']:
   assert (ROOT/target).exists()or Path(target).name=='self-check.json',target
  receipt_targets+=len(receipt['targets'])
 result={'status':'PASS','scope':'Static source hashes, recorded event binding, complete serialized strategy/ledger coverage, JSON/AST, frontmatter, links and receipts. No original program, LP, BI, random scan or independent payoff audit rerun.',
  'own_fingerprints':len(own),'primary_and_dependency_bindings':len(sources),'comparison_bindings':len(compared),'sibling_source_bindings':1,'JSON_files':len(jsons),'Python_AST_files':len(pys),'local_links':len(links),'receipts':4,'receipt_targets_with_duplicates':receipt_targets,'saved_count_states':state_count,'saved_ordered_decisions':history_count,'saved_comparisons':comparison_count,'canonical_fraction_strings':fractions,'new_mathematical_runs':0,'links':links}
 (HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k!='links'},ensure_ascii=False))
if __name__=='__main__':main()
