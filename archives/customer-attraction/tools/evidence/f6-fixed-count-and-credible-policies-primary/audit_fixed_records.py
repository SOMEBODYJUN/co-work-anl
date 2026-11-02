"""Definition-level check of four saved rational policies; no source imports/LP/BI.

Count policies are checked on every count state, with exact multinomial weights
for the logically covered ordered histories. The credible policy's 2801 ordered
keys and all seven destinations at each key are actually read and checked.
Security snapshots receive only full-key binding and the universal all-interest
single-client argument stated in the accompanying mathematical text.
"""
from pathlib import Path
from itertools import combinations, combinations_with_replacement, product
from fractions import Fraction as F
from math import lcm, factorial
from collections import Counter
import hashlib,json,time

HERE=Path(__file__).resolve().parent

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cs(p,d):
 return [tuple(z.count(a) for a in range(p)) for z in combinations_with_replacement(range(p),d)]
def counts(h,p):return tuple(h.count(a) for a in range(p))
def plus(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
def main():
 started=time.monotonic(); manifest=json.loads((HERE/'source-manifest.json').read_text()); inputs={}
 for x in manifest:
  path=HERE/'original'/x['id']/Path(x['path']).name
  assert path.stat().st_size==x['size'] and digest(path)==x['sha256']
  inputs[x['id']]=(path,json.loads(path.read_text()) if path.suffix=='.json' else None)
 result={'scope':'four fixed rational policy records; no original imports/search/LP/BI/RNG; two security snapshots structurally bound and analytically interpreted','source_hashes':{x['id']:x['sha256'] for x in manifest},'records':[],'security_snapshots':[]}
 rows_output=[]
 for sid in ['1ac9f23afe0867b2064b','8cb437875995accd295b','48f0a9b5e94805487299']:
  data=inputs[sid][1]; assert set(data)=={'scope','args','records','elapsed'}
  p,m=data['args']['topics'],data['args']['players'];scale=lcm(*range(1,m+1))
  types=[b for b in range(1,1<<p) if not data['args']['maxfreq'] or b.bit_count()<=data['args']['maxfreq']]
  terminals=cs(p,m); ti={q:i for i,q in enumerate(terminals)};layers=[cs(p,d) for d in range(m)]
  for ri,r in enumerate(data['records']):
   assert set(r)=={'iteration','ratio','root','support','weights','exact_slack','exact_W','rows','actions'}
   w=list(map(F,r['weights']));assert len(w)==len(types) and min(w)>=0
   members={a:[] for a in range(p)}
   for j,b in enumerate(types):
    for a in range(p):
     if b>>a&1:members[a].append(j)
   co={};pay={}
   for t in terminals:
    den=[sum(t[a] for a in range(p) if b>>a&1) for b in types]
    for a in range(p):
     c=tuple(scale//den[j] if types[j]>>a&1 and den[j] else 0 for j in range(len(types)))
     co[t,a]=c;pay[t,a]=sum(F(v,scale)*x for v,x in zip(c,w))
   full=data['args'].get('credible',False)
   action={};metadata={}
   for row in r['actions']:
    assert len(row)==(4 if full else 2)
    key=tuple(row[0]);assert key not in action
    a=row[1];assert type(a)==int and 0<=a<p
    action[key]=a
    if full:
     target,dests=row[2],row[3]
     assert type(target)==int and 0<=target<len(terminals) and len(dests)==p
     assert all(type(v)==int and 0<=v<len(terminals) for v in dests)
     metadata[key]=(target,dests)
   expected={h for d in range(m) for h in product(range(p),repeat=d)} if full else {q for L in layers for q in L}
   assert set(action)==expected
   term={};mult={};pernode=[];dedup=set();minslack=None;negative=0;ic=0;weighted=0;selftests=0
   if full:
    for h in product(range(p),repeat=m):term[h]=counts(h,p)
    for d in range(m-1,-1,-1):
     for h in product(range(p),repeat=d):
      a=action[h];term[h]=term[h+(a,)];target,dests=metadata[h]
      assert terminals[target]==term[h]
      assert all(terminals[dest]==term[h+(b,)] for b,dest in enumerate(dests))
      assert dests[a]==target
      # Root-independent containment of the terminal target in the prefix.
      assert all(term[h][j]>=counts(h,p)[j] for j in range(p))
    keys=sorted(expected,key=lambda h:(len(h),h));rootkey=()
   else:
    term.update({q:q for q in terminals})
    for d in range(m-1,-1,-1):
     for q in layers[d]:term[q]=term[plus(q,action[q])]
    keys=sorted(expected,key=lambda q:(sum(q),tuple(-x for x in q)));rootkey=(0,)*p
   for key in keys:
    a=action[key];actual=term[key]
    multiplicity=1 if full else factorial(sum(key))//__import__('functools').reduce(lambda x,y:x*factorial(y),key,1)
    mult[key]=multiplicity;slacks=[]
    for b in range(p):
     child=key+(b,) if full else plus(key,b)
     dest=term[child]
     slack=pay[actual,a]-pay[dest,b]
     slacks.append(str(slack))
     minslack=slack if minslack is None else min(minslack,slack)
     negative+=slack<0
     if b==a:assert slack==0;selftests+=1
     else:
      ic+=1;weighted+=multiplicity
      row=tuple(x-y for x,y in zip(co[actual,a],co[dest,b]))
      if any(row):dedup.add(row)
    pernode.append({'key':list(key),'action':a,'target_counts':list(actual),'ordered_multiplicity':multiplicity,'all_action_slacks':slacks})
   root=term[rootkey];assert root==tuple(r['root']);assert minslack==F(r['exact_slack'])>=0
   assert len(dedup)==r['rows']
   W=sum(x for b,x in zip(types,w) if any(root[a] and b>>a&1 for a in range(p)))
   assert W==F(r['exact_W'])==1
   J=tuple(r['support']);assert len(J)==min(p,m) and len(set(J))==len(J) and all(0<=a<p for a in J)
   coverage=lambda J:sum(x for b,x in zip(types,w) if any(b>>a&1 for a in J))
   chosen=coverage(J);all_supports=[(coverage(JJ),JJ) for JJ in combinations(range(p),min(p,m))];opt=max(v for v,_ in all_supports)
   assert abs(float(chosen)-r['ratio'])<1e-12
   h=();q=(0,)*p;path=[]
   for d in range(m):
    a=action[h if full else q];path.append(a);h=h+(a,);q=plus(q,a)
   assert q==root
   columns=tuple(tuple(bool(b>>a&1) for b,x in zip(types,w) if x) for a in range(p))
   groups={}
   for a,c in enumerate(columns):groups.setdefault(c,[]).append(a)
   unit=lcm(*(x.denominator for x in w));unitweights=[int(x*unit) for x in w]
   summary={'source_id':sid,'record_index':ri,'iteration':r['iteration'],'policy_domain':'ordered-history' if full else 'count-state','p':p,'m':m,'type_masks':types,'nonzero_weights':[[b,str(x)] for b,x in zip(types,w) if x], 'action_records':len(keys),'terminal_counts':len(terminals),'scale':scale,'root_counts':list(root),'actual_path':path,'W':str(W),'chosen_support':list(J),'chosen_coverage':str(chosen),'true_OPT':str(opt),'OPT_over_W':str(opt/W),'min_all_action_slack':str(minslack),'negative_comparisons':negative,'nonself_IC_actually_evaluated':ic,'self_comparisons_actually_evaluated':selftests,'ordered_decisions_logically_covered':sum(mult.values()),'ordered_nonself_IC_logically_covered':weighted,'distinct_nonzero_integer_rows':len(dedup),'original_rows':r['rows'],'coverage_alias_groups':list(groups.values()),'integer_client_scale':unit,'integer_clients':sum(unitweights),'optimal_supports':[list(JJ) for v,JJ in all_supports if v==opt]}
   rows_output.append({'source_id':sid,'record_index':ri,'records':pernode})
   result['records'].append(summary)
 for sid in ['193fdd4bfcc53f478e10','9daa2b6d250212565bde']:
  path,d=inputs[sid];dec=json.loads(path.read_text(),parse_float=str);p,m=d['parameters']['topics'],d['parameters']['players']
  w=list(map(F,d['weights']));assert len(w)==(1<<p)-1 and w[-1]==1 and all(x==0 for x in w[:-1])
  aa={}
  for row in d['actions']:
   assert set(row)=={'history','action'};h=tuple(row['history']);a=row['action'];assert h not in aa and type(a)==int and 0<=a<p;aa[h]=a
  assert set(aa)=={h for t in range(m) for h in product(range(p),repeat=t)}
  h=()
  while len(h)<m:h=h+(aa[h],)
  assert counts(h,p)==tuple(d['root_counts'])
  pb=list(map(F,d['p']));pd=list(map(F,dec['p']));assert len(pb)==len(pd)==p and min(pb)>=0 and min(pd)>=0
  result['security_snapshots'].append({'source_id':sid,'p':p,'m':m,'all_history_keys':len(aa),'actual_path':list(h),'root_counts':list(counts(h,p)),'unique_positive_interest_mask':(1<<p)-1,'W':'1','all_player_payoffs':str(F(1,m)),'true_static_security_for_legal_probability':'1/'+str(m),'literal_binary_query_sum':str(sum(pb)),'literal_decimal_query_sum':str(sum(pd)),'literal_binary_n_times_fixed_query_minus_W':str(sum(pb)-1),'literal_decimal_n_times_fixed_query_minus_W':str(sum(pd)-1),'analytic_all_node_IC':'0 identically; no numeric IC recomputation','stored_constraint_count':d['constraint_count'],'stored_report_metadata':{k:v for k,v in d.items() if k not in ('weights','p','actions')}})
 for x in manifest:assert digest(inputs[x['id']][0])==x['sha256']
 result['actual_counts']={'four_point_nonself_IC':sum(x['nonself_IC_actually_evaluated'] for x in result['records']),'four_point_self_comparisons':sum(x['self_comparisons_actually_evaluated'] for x in result['records']),'four_point_ordered_decisions_logically_covered':sum(x['ordered_decisions_logically_covered'] for x in result['records']),'four_point_ordered_nonself_logically_covered':sum(x['ordered_nonself_IC_logically_covered'] for x in result['records']),'original_entry_calls':0,'LP':0,'BI':0,'RNG':0}
 result['elapsed_seconds']=time.monotonic()-started
 (HERE/'fixed-record-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 (HERE/'all-node-slacks.json').write_text(json.dumps(rows_output,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'records':[{k:v for k,v in x.items() if k not in ('type_masks','optimal_supports')} for x in result['records']],'security':result['security_snapshots'],'actual_counts':result['actual_counts'],'elapsed_seconds':result['elapsed_seconds']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
