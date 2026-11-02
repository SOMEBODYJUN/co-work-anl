"""One fixed-input audit of preserved R8 base, without author/canonical imports.

No LP, BI, random search or original entry is executed. The same pass also
produces a reversible full-field reading view of both large JSON originals.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from collections import Counter
from hashlib import sha256
import argparse,json


def digest_value(x):return sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--evidence',type=Path,required=True);args=ap.parse_args();ev=args.evidence.resolve()
 sources=json.loads((ev/'source-manifest.json').read_text());stage=ev.parents[4]
 raw={}
 for s in sources:
  p=stage/s['preserved_path'];b=p.read_bytes();assert len(b)==s['size'] and sha256(b).hexdigest()==s['sha256'];raw[Path(s['path']).name]=b
 best=json.loads(raw['best_policy.json']);results=json.loads(raw['results.json']);records=results['records']
 assert len(records)==10 and [r['step'] for r in records]==list(range(10)) and best==records[0]
 p,m,L=7,5,60
 expected=[h for d in range(m) for h in product(range(p),repeat=d)]
 actions=best['strategy']['actions'];canonical=[{'history':list(h),'action':0} for h in expected]
 assert actions==canonical and len(actions)==2801
 policy={tuple(a['history']):a['action'] for a in actions};assert len(policy)==len(expected)
 assert best['strategy']['terminal_counts']==[5,0,0,0,0,0,0]
 vectors=[]
 def encode(v,key=''):
  if key=='actions':
   assert v==canonical
   return {'$constant_policy_actions':0}
  if isinstance(v,list) and len(v)==127 and all(type(x) is int for x in v):
   if v not in vectors:vectors.append(v)
   return {'$vector':vectors.index(v)}
  if isinstance(v,dict):return {k:encode(x,k) for k,x in v.items()}
  if isinstance(v,list):return [encode(x) for x in v]
  return v
 encoded_best,encoded_results=encode(best),encode(results)
 vector_dict=[{'length':127,'default':0,'nonzero':[[i+1,n] for i,n in enumerate(v) if n]} for v in vectors]
 def decode(v):
  if isinstance(v,dict) and set(v)=={'$constant_policy_actions'}:return canonical
  if isinstance(v,dict) and set(v)=={'$vector'}:
   spec=vector_dict[v['$vector']];out=[spec['default']]*spec['length']
   for i,n in spec['nonzero']:out[i-1]=n
   return out
  if isinstance(v,dict):return {k:decode(x) for k,x in v.items()}
  if isinstance(v,list):return [decode(x) for x in v]
  return v
 assert decode(encoded_best)==best and decode(encoded_results)==results
 view={'scope':'all original fields retained; JSON-value roundtrip, not replacement for raw bytes',
  'vector_dictionary':vector_dict,'policy_dictionary':[{'topics':7,'players':5,'history_domain':'every ordered history of lengths0..4 in depth/lex order','action':0,'records':2801}],
  'best_policy':encoded_best,'results':encoded_results,'roundtrip_equal':True}
 (ev/'lossless-full-reading.json').write_text(json.dumps(view,ensure_ascii=False,indent=2)+'\n')
 @lru_cache(None)
 def finish(h):
  if len(h)==m:return h
  return finish(h+(policy[h],))
 def counts(h):return tuple(h.count(a) for a in range(p))
 @lru_cache(None)
 def payrow(q,a):
  out=[]
  for mask in range(1,1<<p):
   if mask&(1<<a):
    denominator=sum(q[t] for t in range(p) if mask&(1<<t));assert denominator>0 and L%denominator==0
    out.append(L//denominator)
   else:out.append(0)
  return tuple(out)
 clones=best['integer_clones'];assert len(clones)==127 and all(type(n) is int and n>=0 for n in clones)
 def dot(a,b):return sum(x*y for x,y in zip(a,b))
 rows=set();all_count=proper=strict=ties=0;minimum=None;minimum_strict=None;by_depth=[]
 for depth in range(m):
  dd={'depth':depth,'nodes':0,'proper':0,'strict':0,'ties':0}
  for h in product(range(p),repeat=depth):
   dd['nodes']+=1;a=policy[h];left=payrow(counts(finish(h)),a)
   for b in range(p):
    right=payrow(counts(finish(h+(b,))),b);row=tuple(x-y for x,y in zip(left,right));gap=dot(row,clones);assert gap>=0
    all_count+=1
    if b==a:continue
    proper+=1;dd['proper']+=1
    if gap>0:
     strict+=1;dd['strict']+=1;minimum_strict=gap if minimum_strict is None else min(minimum_strict,gap)
    else:ties+=1;dd['ties']+=1
    minimum=gap if minimum is None else min(minimum,gap)
    if any(row):rows.add(row)
  by_depth.append(dd)
 rows=sorted(rows);assert len(rows)==best['rows']==1260
 q=counts(finish(()));welfare=tuple(int(mask&1!=0) for mask in range(1,1<<p));W=dot(welfare,clones)
 portfolio=best['portfolio'];pmask=sum(1<<a for a in portfolio);objective=tuple(int(mask&pmask!=0) for mask in range(1,1<<p))
 portfolio_value=dot(objective,clones)
 all_cover=[]
 for support in combinations(range(p),m):
  mask=sum(1<<a for a in support);value=sum(n for b,n in enumerate(clones,1) if b&mask);all_cover.append({'support':support,'coverage':value})
 optimum=max(r['coverage'] for r in all_cover);assert (W,optimum,portfolio_value)==(5,9,9)
 assert F(optimum,W)==F(best['ratio'])==F(best['objective_value'])==F(9,5)
 beta=F(best['dual_bound']);mu={i:F(v) for i,v in best['dual_support']};assert len(mu)==4 and all(v>=0 for v in mu.values())
 assert all(0<=i<len(rows) for i in mu)
 residual=[]
 for j,(w,v) in enumerate(zip(welfare,objective)):
  r=beta*w-sum(x*F(rows[i][j],L) for i,x in mu.items())-v;assert r>=0;residual.append(r)
 assert beta==F(portfolio_value,W)
 root_indices=[]
 for a in range(1,p):
  rr=tuple(x-y for x,y in zip(payrow(q,0),payrow(counts(finish((a,))),a)))
  root_indices.append({'alternative':a,'row_index':rows.index(rr)})
 record_analysis=[]
 for r in records:
  assert r['integer_clones']==clones and r['target']==list(q)
  assert (r['portfolio'],r['objective_value'],r['ratio'],r['optimum'],r['welfare'],r['dual_bound'],r['dual_support'])==(best['portfolio'],best['objective_value'],best['ratio'],best['optimum'],best['welfare'],best['dual_bound'],best['dual_support'])
  src=r['source'];assert all(type(x) is int and x>=0 for x in src)
  assert all(n==0 or mask==1 or not(mask&1) for mask,n in enumerate(src,1))
  big=src[0];small_sizes=[sum(n for mask,n in enumerate(src,1) if mask&(1<<a)) for a in range(1,p)]
  assert big>0 and max(small_sizes)==F(big,5)
  record_analysis.append({'step':r['step'],'mode':r['mode'],'source_vector_dictionary_index':vectors.index(src),'source_clients':sum(src),'Big_size':big,'private_theme_sizes':small_sizes,'target':r['target'],'rows_reported':r['rows'],'statistics':r['statistics'],'same_optimized_proof_values':True,'has_saved_strategy':'strategy' in r})
 compact=''.join(str(policy[h]) for h in expected)
 report={
  'status':'PASS','scope':'one new fixed source audit; no LP/BI/random/original code import or execution',
  'source_hashes':{s['id']:s['sha256'] for s in sources},'lossless_json_roundtrip_equal':True,
  'native_result_records':10,'native_best_equals_record0':True,'native_unique_saved_strategies':1,
  'native_strategy_occurrences':2,'native_action_record_occurrences':5602,'unique_ordered_policy_records':2801,
  'policy_actions_sha256':digest_value(actions),'policy_strategy_sha256':digest_value(best['strategy']),
  'policy_compact_action_string_sha256':sha256(compact.encode()).hexdigest(),
  'source_vector_sha256':digest_value(best['source']),'optimized_vector_sha256':digest_value(clones),
  'full_history_comparisons_including_self':all_count,'proper_deviations':proper,'strict_proper':strict,'proper_ties':ties,
  'minimum_proper_slack':str(F(minimum,L)),'minimum_strict_proper_slack':str(F(minimum_strict,L)),'by_depth':by_depth,
  'integer_profit_scale':L,'unique_nonzero_sorted_IC_rows':len(rows),
  'actual':finish(()),'terminal_counts':q,'payoffs':[str(F(dot(payrow(q,a),clones),L)) for a in finish(())],
  'W':W,'OPT':optimum,'total_unit_clients':sum(clones),'all_21_distinct_five_label_supports':all_cover,
  'portfolio_coverage':portfolio_value,'ratio':str(F(optimum,W)),'half_margin':2*W-optimum,
  'dual_beta':str(beta),'dual_support':best['dual_support'],'dual_rows_scaled60':[{ 'index':i,'multiplier':str(v),'coefficients':rows[i]} for i,v in mu.items()],
  'root_alternative_sorted_row_indices':root_indices,'all_127_dual_residuals':list(map(str,residual)),
  'dual_minimum_residual':str(min(residual)),'dual_zero_coefficients':sum(x==0 for x in residual),'dual_positive_coefficients':sum(x>0 for x in residual),
  'record_analysis':record_analysis,'vector_dictionary_count':len(vectors),
  'limits':'dual checked against one saved complete policy; later missing-policy fields are not new exported trees; same-policy reconstruction is separate analytic argument; source16 versus report10 execution mismatch not resolved by this audit'
 }
 (ev/'fixed-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['status','native_result_records','unique_ordered_policy_records','proper_deviations','strict_proper','proper_ties','unique_nonzero_sorted_IC_rows','W','OPT','ratio','dual_minimum_residual','policy_compact_action_string_sha256']},ensure_ascii=False))


if __name__=='__main__':main()
