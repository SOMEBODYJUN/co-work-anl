"""Static package checks only. Does not import producer or rerun the rational audit."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import ast,gzip,hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BODY=ROOT/'archives/customer-attraction/state/程序/两步安全链的自适应策略锥攻击与三份四人记录--程序.md'
IDS=['9820670d2bbb41abe49e','17d22c962046911e6312','455e0a7134ad7d26dad6','5947f6431f86460d8b9c']
def read(p):return json.loads(p.read_text())
def verify(p,r):
 b=p.read_bytes();assert len(b)==r.get('bytes',r.get('size')),str(p)
 assert hashlib.sha256(b).hexdigest()==r['sha256'],str(p)
def main():
 own=read(HERE/'artifact-manifest.json')['files']
 for r in own:verify(ROOT/r['path'],r)
 sources=read(HERE/'source-manifest.json')['sources']
 assert sorted(r['id']for r in sources if r['role']=='primary')==sorted(IDS)
 for r in sources:verify(ROOT/r['preserved_path'],r);assert r['full_file_reviewed']is True
 comparisons=read(HERE/'comparison-manifest.json')['files']
 for r in comparisons:verify(ROOT/r['path'],r)
 sibling=read(HERE/'review-record.json')['sibling_joint_source_read'];verify(ROOT/sibling['preserved_path'],sibling)
 jsonfiles=sorted(p for p in HERE.rglob('*.json')if p.name!='self-check.json')
 for p in jsonfiles:read(p)
 pyfiles=sorted(HERE.rglob('*.py'))
 for p in pyfiles:ast.parse(p.read_text(),filename=str(p))
 header=BODY.read_text().split('---',2)[1]
 for name in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+name+':',header,re.M),name
 links=[]
 for doc in [BODY,HERE/'README.md']:
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text()):
   target=target.strip('<>').split('#',1)[0]
   if not target or re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',target):continue
   path=(doc.parent/target).resolve();assert path.exists()or path==HERE/'self-check.json',(str(doc),target)
   links.append({'document':str(doc.relative_to(ROOT)),'target':target})
 original={p.name:read(p)for p in(HERE/'original').glob('*.json')}
 view=read(HERE/'all-fields-reading-view.json')
 for row in view:
  reconstructed=dict(row['complete_root_fields']);reconstructed['best']=dict(row['complete_best_except_policy']);reconstructed['best']['policy']=[{'history':h,'action':a}for h,a in row['complete_policy_history_action_pairs']]
  assert json.dumps(reconstructed,sort_keys=True)==json.dumps(original[row['source']],sort_keys=True)
  assert len(original[row['source']]['best'])==8 and len(original[row['source']]['best']['weights'])==63
 assert 'prefix'not in original['pair_n4k6.json']
 assert original['pair_n4k6_bg001.json']['prefix']==[0,0,1]and original['pair_n4k6_bgall.json']['prefix']==list(range(6))
 event=read(HERE/'exact/execution.json');assert event['exit_code']==0 and event['assertions_enabled']is True
 for row in event['inputs']:
  basename=Path(row['path']).name;p=HERE/basename if basename=='audit_saved_points.py'else HERE/'original'/basename;verify(p,row)
 for row in event['outputs']:verify(HERE/'exact'/row['path'],row)
 audit=read(HERE/'exact/exact-audit.json');ledger=json.loads(gzip.decompress((HERE/'exact/complete-ledger.json.gz').read_bytes()))
 assert audit['status']=='PASS'and len(audit['cases'])==3 and len(ledger)==9
 for key in ['original_imports','original_functions','original_main','LP_MILP','BI','RNG']:assert audit[key]==0
 assert audit['definition_audit_events']==1
 keyed={(x['source'],x['interpretation']):x for x in ledger};histories=comparisons_saved=fraction_strings=static_rows=0
 for case in audit['cases']:
  data=original[case['source']];policy={tuple(x['history']):x['action']for x in data['best']['policy']}
  assert len(policy)==len(data['best']['policy'])==259
  assert Counter(map(len,policy))==Counter({0:1,1:6,2:36,3:216})
  assert case['reported_gap']==data['best']['gap']==0.0
  assert case['completed_source']==data['completed']and case['elapsed_source']==data['elapsed']
  assert all(case['big_mask']>>a&1 for a in policy.values())
  for point in case['interpretations']:
   saved=keyed[case['source'],point['interpretation']];rows=saved['all_history_comparisons']
   assert len(rows)==point['all_action_comparisons']==1554
   assert Counter(tuple(x['history'])for x in rows)==Counter({h:6 for h in policy})
   counts=Counter()
   for row in rows:
    assert row['chosen']==policy[tuple(row['history'])]
    for key in ['prescribed_payoff','deviation_payoff','slack']:
     assert str(Fraction(row[key]))==row[key];fraction_strings+=1
    val=Fraction(row['slack']);counts['negative'if val<0 else'zero'if val==0 else'positive']+=1
   assert counts['negative']==point['negative_comparisons']==0
   assert counts['zero']==point['zero_comparisons']and counts['positive']==point['positive_comparisons']
   assert point['true_PAIR_gap']==point['explicit_normalized_pq_screen']=='0'
   assert point['root_value']==point['tail_value']
   for family,expected in [('root',56),('tail',6)]:
    assert len(saved[family+'_rivals'])==len(saved[family+'_payoffs'])==expected
    for row in saved[family+'_payoffs']:
     assert len(row)==6
     for value in row:assert str(Fraction(value))==value;fraction_strings+=1
    static_rows+=expected
   histories+=259;comparisons_saved+=1554
 assert(histories,comparisons_saved,static_rows)==(2331,13986,558)
 assert fraction_strings==45306
 first=audit['cases'][0]['interpretations'];assert first[0]['saved_p_sum']=='50000000000000001/50000000000000000'and first[1]['saved_p_sum']=='36028797018963969/36028797018963968'
 assert first[0]['raw_pq_expression_not_certificate_if_nonunit']=='-1/62500000000000000'
 third=audit['cases'][2]['interpretations'];assert[point['zero_comparisons']for point in third]==[777,777,897]
 scope=read(HERE/'execution-scope.json');assert scope['original_program_runs']==scope['original_helper_calls']==scope['LP_MILP_runs']==scope['new_math_reruns']==0 and scope['independent_definition_events']==1
 target_count=0
 for source_id in IDS:
  receipt=read(ROOT/f'cleanup/workspaces/Boss7/receipts-round21/{source_id}.json')
  assert receipt['id']==source_id and receipt['disposition']=='integrated'
  for key in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert receipt[key]is True
  for target in receipt['targets']:assert(ROOT/target).exists()or Path(target).name=='self-check.json',target
  target_count+=len(receipt['targets'])
 result={'status':'PASS','scope':'Static fingerprints, event bindings, all saved fields and serialized history/static-matrix ledgers; zero original mathematical calls or independent-audit reruns.','own_fingerprints':len(own),'source_bindings':len(sources),'comparison_bindings':len(comparisons),'sibling_source_bindings':1,'JSON_files':len(jsonfiles),'Python_AST_files':len(pyfiles),'local_links':len(links),'receipts':4,'receipt_targets_with_duplicates':target_count,'saved_history_interpretations':histories,'saved_comparisons':comparisons_saved,'saved_static_rows':static_rows,'canonical_fraction_strings':fraction_strings,'new_mathematical_runs':0,'links':links}
 (HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k!='links'},ensure_ascii=False))
if __name__=='__main__':main()
