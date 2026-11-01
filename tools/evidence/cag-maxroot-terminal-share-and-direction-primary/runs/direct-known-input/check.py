from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
import json,hashlib,ast
HERE=Path(__file__).resolve().parent
raw=json.loads((HERE/'root_source_relaxation_exact.json').read_text());out=[]
for o in raw:
 m,p=o['m'],o['p'];weights={mask:F(w) for mask,w in o['positive_normalized_types']};actual=o['actual_path'];source=o['source_path'];masks=list(range(1,1<<p))
 assert actual==list(range(m)) and source==[m-1]+list(range(m,p))
 def u(path,i,ww=weights):return sum((v/F(sum((mask>>a)&1 for a in path)) for mask,v in ww.items() if (mask>>path[i])&1),F())
 def floor(path,i,a):return sum((v/F(m-i+sum((mask>>b)&1 for b in path[:i])) for mask,v in weights.items() if (mask>>a)&1),F())
 au=[u(actual,i) for i in range(m)];su=[u(source,i) for i in range(m)];assert list(map(str,au))==o['actual_payoffs_normalized'] and list(map(str,su))==o['source_payoffs_normalized'];assert sum(au)==1
 rows=[]
 for label,path,uu,start in [('actual',actual,au,0),('source',source,su,1)]:
  for i in range(start,m):
   for a in range(p):rows.append({'path':label,'role':i,'query':a,'slack':str(uu[i]-floor(path,i,a))})
 rows.append({'path':'root-source','slack':str(au[0]-su[0])});assert all(F(r['slack'])>=0 for r in rows) and min(F(r['slack']) for r in rows)==F(o['minimum_slack'])==0
 assert str((m+1)*au[-1]-2)==o['candidate_violation'] and str(au[-1])==o['last_share']
 inst=o['integer_instance'];assert inst['players']==m and inst['topics']==['T'+str(i) for i in range(p)]
 iw={sum(1<<a for a in c['topics']):c['multiplicity'] for c in inst['customers']};assert len(iw)==len(inst['customers']) and set(iw)==set(weights) and all(isinstance(v,int) and v>0 for v in iw.values())
 scale=next(iter(F(iw[k])/weights[k] for k in weights));assert all(F(iw[k])==scale*weights[k] for k in weights)
 tails=[]
 for saved,path in zip(o['two_player_tail_checks'],[actual,source]):
  prefix=path[:-2];assert prefix==saved['prefix'];tables=[];thresholds=[]
  for a in range(p):
   last_values=[u(prefix+[a,b],len(prefix)+1,iw) for b in range(p)];best=max(last_values);br=[b for b,v in enumerate(last_values) if v==best];first=[u(prefix+[a,b],len(prefix),iw) for b in br];lower=min(first);thresholds.append(lower)
   tables.append({'first_action':a,'last_all_query_values':list(map(str,last_values)),'last_best_responses':br,'first_values_at_those_BR':list(map(str,first)),'min_first_over_BR':str(lower)})
  M=max(thresholds);current=u(path,m-2,iw);assert str(M)==saved['exact_tail_threshold_M'] and str(current)==saved['tail_current_payoff'];assert (current>=M)==saved['passes_threshold']==False
  tails.append({'prefix':prefix,'threshold':str(M),'candidate_first_payoff':str(current),'maximizing_first_actions':[a for a,v in enumerate(thresholds) if v==M],'all_first_and_last_comparisons':tables,'candidate_rejected':True})
 out.append({'m':m,'p':p,'types_in_coefficient_domain':len(masks),'positive_types':len(weights),'scale':str(scale),'actual_payoffs':list(map(str,au)),'source_payoffs':list(map(str,su)),'welfare':'1','violation':o['candidate_violation'],'all_necessary_rows':rows,'two_tails':tails,'all_original_JSON_fields_checked':True,'input_status_label':'original descriptive status preserved; not a mathematical predicate'})
# The already-verified first layer of current coupling_layers is a different physical resource.
# Read only its header/actions/root/portfolio/first-layer values; do not certify remaining layers.
o=json.loads((HERE/'current-coupling-layers.json').read_text());first=o['layers'][0];assert o['n']==3 and o['p']==6 and first['lower_bound']==first['upper_bound']=='9/4'
y={ast.literal_eval(k):F(v) for k,v in first['positive_values'].items()};cycles=[]
for a,b in combinations(range(6),2):
 q=[0]*6;r=[0]*6;q[a]=2;q[b]=1;r[a]=1;r[b]=2
 val=sum((F(r[j]-q[j])*(y.get((tuple(q),j),F())-y.get((tuple(r),j),F())) for j in [a,b]),F());assert val>=0
 cycles.append({'support':[a,b],'remainder':str(val)})
counts={}
for row in cycles:counts[row['remainder']]=counts.get(row['remainder'],0)+1
assert counts=={'0':1,'1/8':9,'3/16':2,'1/4':3}
assert len(y)==126 and len(o['strategy_actions'])==43
result={'scope':'own known-input Fraction algebra; no original solver/auditor/model imported; not blind or new independent full-SPE audit','point_records':out,'same_support_cycle_check':{'input_resource':'current coupling_layers first-layer primal','full_JSON_read_claimed':False,'specified_consumed_fields':['n','p','strategy_actions','root','portfolio','layers[0].positive_values','layers[0].lower_bound','layers[0].upper_bound'],'remaining_layers_not_reviewed':True,'original_support_conservation_JSON_not_byte_compared':True,'all15_generator_cycles':cycles,'remainder_distribution':counts,'previous_full_graph_dilution_conservation_certification_reused_not_rerun':True}}
(HERE/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'point_rows':[len(x['all_necessary_rows']) for x in out],'all_four_tail_thresholds':[t['threshold'] for x in out for t in x['two_tails']],'cycle_distribution':counts},ensure_ascii=False))
