"""New exact point/row audit; no RNG, numpy, MILP, or original CLI.

Three previously unaudited saved points are checked from Fraction definitions.
The old p4 twelve-customer point is reused from successful JB output, not run.
"""
from pathlib import Path
from fractions import Fraction as F
import itertools,json,sys
HERE=Path(__file__).resolve().parent
RAW=HERE/'original/research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/global'
def read(p):return json.loads(p.read_text())
def serial(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {k:serial(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [serial(v) for v in x]
 return x
def actions(d):
 a={tuple(row['history']):row['action'] for row in d['actions']};assert len(a)==len(d['actions']);return a
def count(h,p):return tuple(h.count(j) for j in range(p))
def point_audit(d,name):
 p=d['p'];m=d['m'];assert m==3 and p in (4,5)
 w={int(k):v for k,v in d['weights'].items()};assert all(isinstance(v,int) and v>0 and 1<=b<1<<p for b,v in w.items())
 a=actions(d);expected={h for depth in range(m) for h in itertools.product(range(p),repeat=depth)};assert set(a)==expected and all(0<=v<p for v in a.values())
 def finish(h):
  while len(h)<m:h=h+(a[h],)
  return h
 def U(q,t):
  assert q[t]>0
  return sum((F(v,sum(q[j] for j in range(p) if b>>j&1)) for b,v in w.items() if b>>t&1),F())
 def C(q):return sum(v for b,v in w.items() if any(q[j] and b>>j&1 for j in range(p)))
 policy=[];slacks=[]
 for h in sorted(expected,key=lambda x:(len(x),x)):
  terminals=[finish(h+(j,)) for j in range(p)];profits=[U(count(s,p),j) for j,s in enumerate(terminals)];chosen=a[h]
  ss=[profits[chosen]-v for v in profits];assert all(ss[j]>0 for j in range(p) if j!=chosen)
  slacks.extend(ss[j] for j in range(p) if j!=chosen)
  policy.append({'history':h,'chosen':chosen,'profits_by_action':profits,'terminal_branches':terminals,'slacks_including_self':ss})
 qs=sorted({count(h,p) for h in itertools.product(range(p),repeat=m)});stat=[];gainmap={}
 for q in qs:
  deviations=[]
  for j in range(p):
   if not q[j]:continue
   for b in range(p):
    if b==j:continue
    qq=list(q);qq[j]-=1;qq[b]+=1
    g=U(tuple(qq),b)-U(q,j);gainmap[q,j,b]=g;deviations.append({'from':j,'to':b,'gain':g})
  best=max(x['gain'] for x in deviations);is_pne=best<=0
  stat.append({'counts':q,'W':C(q),'is_PNE':is_pne,'all_occupied_label_nonself_deviations':deviations,'best_gain':best})
 root=finish(());rootq=count(root,p);W=C(rootq);pne=[x for x in stat if x['is_PNE']];minimum=min(x['W'] for x in pne);opt=max(x['W'] for x in stat)
 assert len(pne)==1 and minimum>W and 2*W>=opt
 if 'actual' in d:
  assert list(rootq)==d['actual'] and W==d['W'] and minimum==d['minimum_pne_W']
  assert [{'counts':list(x['counts']),'W':x['W']} for x in pne]==d['pne']
 else:assert list(pne[0]['counts'])==d['chosen_pne']
 result={'name':name,'p':p,'m':m,'unit_customers':sum(w.values()),'nonzero_types':len(w),'all_type_weights':{str(b):w.get(b,0) for b in range(1,1<<p)},'complete_ordered_histories':len(expected),'all_action_comparisons_including_self':len(expected)*p,'nonself_SPE_comparisons':len(slacks),'minimum_strict_SPE_slack':min(slacks),'all_history_rows':policy,'actual_path':root,'actual_counts':rootq,'actual_profits':[U(rootq,j) for j in root],'W':W,'OPT3':opt,'W_over_OPT':F(W,opt),'two_W_minus_OPT':2*W-opt,'static_count_states':len(qs),'static_nonself_occupied_label_comparisons':len(gainmap),'all_static_count_rows':stat,'PNE_counts':[x['counts'] for x in pne],'minimum_PNE_W':minimum,'PNE_minus_SPE':minimum-W,'minimum_PNE_strict_slack':min(-x['gain'] for x in pne for x in x['all_occupied_label_nonself_deviations'])}
 return result,{'a':a,'p':p,'qs':qs,'gainmap':gainmap,'policy':{tuple(x['history']):x for x in policy},'static':{tuple(x['counts']):x for x in stat}}

def fixed_labels_from_original_input(source,cache):
 p=source['p'];a=actions(source);pk=tuple(source['pne'][0]['counts']);labels=[]
 for h,c in sorted(a.items()):
  for j in range(p):
   if j!=c:labels.append(['spe',list(h),j])
 for q in cache['qs']:
  ds=[(cache['gainmap'][q,j,b],j,b) for j in range(p) if q[j] for b in range(p) if b!=j]
  if q==pk:labels.extend(['pne',list(q),j,b] for g,j,b in ds)
  else:
   # Original min(old payoff - new payoff), stable order by j then b.
   g,j,b=max(ds,key=lambda t:t[0]);assert g>0;labels.append(['notpne',list(q),j,b])
 labels.append(['welfaregap']);return labels

def audit_comp_rows(comp,source,source_cache,point,cache,old=None):
 assert comp['actions']==source['actions'] and comp['positive_types_required'] is False
 labels=fixed_labels_from_original_input(source,source_cache);assert labels==comp['witnesses']
 old_policy={} if old is None else {(tuple(a['history']),a['alternative']):F(a['slack']) for a in old['policy_rows']}
 old_stat={} if old is None else {tuple(a['profile']):a for a in old['static_profiles']}
 values=[]
 for lab in labels:
  kind=lab[0]
  if kind=='spe':
   h=tuple(lab[1]);alt=lab[2];val=6*(cache['policy'][h]['slacks_including_self'][alt] if old is None else old_policy[h,alt]);lower=1
  elif kind in ('pne','notpne'):
   q=tuple(lab[1]);j,b=lab[2:]
   if old is None:gain=cache['gainmap'][q,j,b]
   else:
    profile=tuple(t for t,n in enumerate(q) for _ in range(n));gain=F(old_stat[profile]['all_action_gains_including_self'][profile.index(j)*4+b])
   val=6*(gain if kind=='notpne' else -gain);lower=int(kind=='notpne')
  else:val=point['minimum_PNE_W']-point['W'];lower=1
  assert val.denominator==1 and val>=lower
  values.append({'label':lab,'scaled_or_coverage_row_value':val,'lower':lower,'row_excess':val-lower})
 assert min(x['row_excess'] for x in values)==comp['minimum_integer_margin']==0
 return {'p':comp['p'],'frozen_labels_equal_original_choice_algorithm':True,'row_count':len(labels),'minimum_exact_row_excess':min(x['row_excess'] for x in values),'row_kind_counts':{k:sum(x[0]==k for x in labels) for k in ['spe','pne','notpne','welfaregap']},'all_rows':values,'old_twelve_customer_cached_output_reused_without_new_game_audit':old is not None,'float_optimality_or_global_minimality_certified':False}

assert len(sys.argv)==2 and not sys.flags.optimize
output=Path(sys.argv[1]);assert not output.exists(),'preserve exactly one new execution'
p5=read(RAW/'strict_static_bridge_search.json');p4=read(RAW/'strict_static_bridge_search_p4.json');c5=read(RAW/'strict_static_bridge_compressed.json');c4=read(RAW/'strict_static_bridge_compressed_p4.json')
assert p5['seed']==p4['seed']==31415927 and (p5['trial'],p5['strict_count'])==(3029,3029) and (p4['trial'],p4['strict_count'])==(1190,1190)
r5,k5=point_audit(p5,'p5 frozen random discovery');r4,k4=point_audit(p4,'p4 frozen random discovery');rc5,kc5=point_audit(c5,'p5 frozen compressed16customer point')
assert r5['complete_ordered_histories']==31 and r4['complete_ordered_histories']==21 and rc5['complete_ordered_histories']==31 and rc5['unit_customers']==16
old=read(HERE/'prior-JB-success/new-coupling-and-strict-policy.json')['strict_twelve_clients']
assert {str(k):str(v) for k,v in c4['weights'].items()}==old['types'] and actions(c4)=={tuple(a['history']):a['chosen'] for a in old['policy_rows']}
oldpoint={'minimum_PNE_W':int(old['static_pne_min_welfare']),'W':int(old['root_coverage'])}
rows5=audit_comp_rows(c5,p5,k5,rc5,kc5);rows4=audit_comp_rows(c4,p4,k4,oldpoint,None,old=old)
assert rows5['row_count']==171 and rows4['row_count']==92
result={'identity':'new exact saved strict points and frozen compression rows; no discovery or MILP','new_game_points':[r5,r4,rc5],'new_game_histories':83,'new_game_action_comparisons_including_self':394,'new_game_nonself_SPE_comparisons':311,'new_game_static_count_states':90,'new_game_static_nonself_occupied_label_comparisons':720,'p5_compression_row_check':rows5,'p4_old_cached_compression_row_check':rows4,'p4_twelve_customer_new_game_audits':0,'original_search_or_compression_CLI_entries':0,'LP_MILP_RNG_calls':0,'old_successful_original_entries_rerun':0,'new_deterministic_exact_entries':1,'global_minimality_certified':False}
assert sum(x['complete_ordered_histories'] for x in result['new_game_points'])==83 and sum(x['all_action_comparisons_including_self'] for x in result['new_game_points'])==394 and sum(x['static_nonself_occupied_label_comparisons'] for x in result['new_game_points'])==720
output.write_text(json.dumps(serial(result),ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','new_saved_points':3,'ordered_histories':83,'SPE_comparisons_including_self':394,'nonself_SPE_comparisons':311,'static_count_states':90,'static_occupied_label_nonself_comparisons':720,'compression_rows_p5':171,'p4_old_cached_rows':92,'new_p4_twelve_customer_game_audit':0,'original_search_MILP_entries':0,'new_exact_entry':1}))
