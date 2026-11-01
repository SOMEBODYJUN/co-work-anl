"""One independent rational audit of three frozen PAIR records. No producer import/LP/BI."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product,combinations_with_replacement
from math import lcm
import datetime,gzip,hashlib,json,platform,sys,time
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'exact'
CASES={'pair_n4k6.json':{'prefix':[],'calibration':{4:1,59:4},'big':59},'pair_n4k6_bg001.json':{'prefix':[0,0,1],'calibration':{4:1,59:7},'big':59},'pair_n4k6_bgall.json':{'prefix':list(range(6)),'calibration':{1:2,4:2,26:7,32:2},'big':26}}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert not OUT.exists(),'one audit event; inspect prior output rather than overwrite'
 OUT.mkdir();start=time.perf_counter();when=datetime.datetime.now(datetime.timezone.utc).isoformat();summaries=[];ledgers=[]
 for name,setup in CASES.items():
  path=ROOT/'original'/name;raw=json.loads(path.read_text());dec=json.loads(path.read_text(),parse_float=F);best=raw['best'];db=dec['best'];n,k=raw['n'],raw['k'];assert(n,k)==(4,6)
  prefix=raw.get('prefix',setup['prefix']);assert prefix==setup['prefix']
  prefix_status='explicit source field'if'prefix'in raw else 'missing in original; new explicitly chosen empty-background interpretation, not historical producer recovery'
  policy={tuple(x['history']):x['action']for x in best['policy']};histories=[h for depth in range(n)for h in product(range(k),repeat=depth)]
  assert len(policy)==len(best['policy'])==259 and set(policy)==set(histories)
  assert all(0<=a<k for a in policy.values());big=setup['big'];assert all(big>>a&1 for a in policy.values())
  @lru_cache(None)
  def finish(h):
   if len(h)==n:return h
   return finish(h+(policy[h],))
  actual=finish(());assert list(actual[:2])==best['first']
  root_rivals=list(combinations_with_replacement(range(k),n-1));tail_rivals=list(combinations_with_replacement(range(k),n-3))
  assert best['rivals']==[list(x)for x in tail_rivals]
  mass=sum(setup['calibration'].values())
  interpretations={'literal_decimal':[F(x)for x in db['weights']],'literal_binary':[F(x)for x in best['weights']],
                   'explicit_integer_calibration_divided_by_mass':[F(setup['calibration'].get(j,0),mass)for j in range(1,1<<k)]}
  report={'source':name,'input_sha256':sha(path),'source_fields':list(raw),'prefix_status':prefix_status,'prefix_used':prefix,
          'n_remaining':n,'k_topics':k,'background_providers':len(prefix),'total_providers':len(prefix)+n,'completed_source':raw['completed'],'elapsed_source':raw['elapsed'],'iteration_source':best['iteration'],'reported_gap':best['gap'],
          'actual_actions':actual,'actual_first':actual[:2],'policy_actions_are_all_aliases_of_big_block':True,'big_mask':big,'calibration_integer_customers':{str(j):v for j,v in setup['calibration'].items()},'calibration_mass':mass,'interpretations':[]}
  for kind,w in interpretations.items():
   assert len(w)==63 and all(x>=0 for x in w)and w[-1]==0
   types=[(j+1,x)for j,x in enumerate(w)if x];expanded=[]
   if kind.startswith('explicit'):
    expanded=[j for j,count in setup['calibration'].items()for _ in range(count)]
   @lru_cache(None)
   def payoff(action,path):
    val=sum((x/F(sum(1 for a in prefix+list(path)if mask>>a&1))for mask,x in types if mask>>action&1),F())
    if expanded:
     unit=sum((F(1,sum(1 for a in prefix+list(path)if mask>>a&1))for mask in expanded if mask>>action&1),F())/mass
     assert val==unit
    return val
   rows=[]
   for h in histories:
    chosen=policy[h];leaf=finish(h);own=payoff(chosen,leaf)
    for action in range(k):
     alternative=finish(h+(action,));alt=payoff(action,alternative)
     rows.append({'history':h,'chosen':chosen,'deviation':action,'prescribed_terminal':leaf,'deviation_terminal':alternative,
                  'prescribed_payoff':str(own),'deviation_payoff':str(alt),'slack':str(own-alt)})
   negative=[x for x in rows if F(x['slack'])<0]
   def static_rows(extra,rivals):
    return [[sum((x/F(1+sum(1 for a in prefix+list(extra)+list(B)if mask>>a&1))for mask,x in types if mask>>query&1),F())for query in range(k)]for B in rivals]
   root=static_rows((),root_rivals);tail=static_rows(actual[:2],tail_rivals)
   a=actual[0];root_dual=root[root_rivals.index((a,)*(n-1))];tail_dual=tail[tail_rivals.index((a,)*(n-3))]
   root_lower=min(row[a]for row in root);tail_lower=min(row[a]for row in tail)
   root_upper=max(root_dual);tail_upper=max(tail_dual)
   assert root_lower==root_upper and tail_lower==tail_upper
   pay=[payoff(x,actual)for x in actual];pair=pay[0]+pay[1]
   true_gap=pair+(n-2)*tail_lower-n*root_lower
   savedp=[F(x)for x in(db['p']if kind!='literal_binary'else best['p'])]
   savedq=[F(x)for x in(db['q']if kind!='literal_binary'else best['q'])]
   ps,qs=sum(savedp),sum(savedq);assert min(savedp)>=0 and min(savedq)>=0 and ps>0 and qs>0
   def screen(p,q):
    lower=min(sum(x*y for x,y in zip(p,row))for row in root)
    upper=max(sum(qi*row[a]for qi,row in zip(q,tail))for a in range(k))
    return pair+(n-2)*upper-n*lower,lower,upper
   raw_screen,raw_lower,raw_upper=screen(savedp,savedq)
   normscreen,lower,upper=screen([x/ps for x in savedp],[x/qs for x in savedq])
   clone_scale=lcm(*(x.denominator for x in w));integer_clones={str(j):int(x*clone_scale)for j,x in types}
   item={'interpretation':kind,'positive_weights':{str(j):str(x)for j,x in types},'mass':str(sum(w)),'mass_minus_one':str(sum(w)-1),
         'clearing_denominator':clone_scale,'integer_clones':integer_clones,'total_integer_clones':sum(integer_clones.values()),
         'complete_decision_histories':259,'all_action_comparisons':len(rows),'negative_comparisons':len(negative),
         'zero_comparisons':sum(F(x['slack'])==0 for x in rows),'positive_comparisons':sum(F(x['slack'])>0 for x in rows),
         'minimum_slack':str(min(F(x['slack'])for x in rows)),'first_negative':negative[:1],
         'actual_payoffs':[str(x)for x in pay],'pair':str(pair),'root_value':str(root_lower),'tail_value':str(tail_lower),'true_PAIR_gap':str(true_gap),
         'pure_query':a,'root_pure_opponent':(a,)*(n-1),'tail_pure_opponent':(a,)*(n-3),
         'root_all_query_values_against_pure_opponent':[str(x)for x in root_dual],'tail_all_query_values_against_pure_opponent':[str(x)for x in tail_dual],
         'root_static_rows':len(root),'tail_static_rows':len(tail),'saved_p_sum':str(ps),'saved_q_sum':str(qs),
         'saved_p_legal_probability':ps==1,'saved_q_legal_probability':qs==1,
         'raw_pq_expression_not_certificate_if_nonunit':str(raw_screen),'raw_root_lower':str(raw_lower),'raw_tail_upper':str(raw_upper),
         'explicit_normalized_pq_screen':str(normscreen),'normalized_root_lower':str(lower),'normalized_tail_upper':str(upper)}
   assert not negative and true_gap==0 and normscreen==0
   report['interpretations'].append(item)
   ledgers.append({'source':name,'interpretation':kind,'all_history_comparisons':rows,'root_rivals':root_rivals,'root_payoffs':[[str(x)for x in row]for row in root],
                   'tail_rivals':tail_rivals,'tail_payoffs':[[str(x)for x in row]for row in tail]})
  summaries.append(report)
 result={'status':'PASS','scope':'Three saved records, each literal-decimal/literal-binary/explicit-unit-calibration; first source lacks prefix and is analyzed only with a declared new empty-background interpretation.',
         'original_imports':0,'original_functions':0,'original_main':0,'LP_MILP':0,'BI':0,'RNG':0,'definition_audit_events':1,
         'records':3,'interpretations':9,'stored_full_policies':3,'policy_decisions_per_interpretation_total':2331,'all_action_comparisons':13986,
         'static_rows_per_interpretation_total':558,'static_entries':3348,'explicit_calibration_unit_customers':26,'cases':summaries}
 (OUT/'exact-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 (OUT/'complete-ledger.json.gz').write_bytes(gzip.compress((json.dumps(ledgers,separators=(',',':'))+'\n').encode(),mtime=0))
 event={'started_at_utc':when,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.perf_counter()-start,'exit_code':0,'python':sys.version,'platform':platform.platform(),'assertions_enabled':__debug__,
        'inputs':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}for p in [Path(__file__)]+sorted((ROOT/'original').glob('*.json'))],
        'outputs':[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)}for p in OUT.iterdir()if p.is_file()]}
 (OUT/'execution.json').write_text(json.dumps(event,indent=2)+'\n')
 print(json.dumps({'status':'PASS','interpretations':9,'all_action_comparisons':13986,'seconds':time.perf_counter()-start}))
if __name__=='__main__':main()
