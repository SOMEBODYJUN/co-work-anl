#!/usr/bin/env python3
"""One fixed saved-point audit; stdlib only, no discovery/BI/MILP imports."""
import argparse,ast,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from itertools import product

def rank(A):
 A=[row[:] for row in A];r=0
 for c in range(len(A[0])):
  pivot=next((i for i in range(r,len(A)) if A[i][c]),None)
  if pivot is None:continue
  A[r],A[pivot]=A[pivot],A[r];s=A[r][c];A[r]=[x/s for x in A[r]]
  for i in range(len(A)):
   if i!=r:
    s=A[i][c];A[i]=[x-s*y for x,y in zip(A[i],A[r])]
  r+=1
 return r

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,required=True);ap.add_argument('--author-code',type=Path,required=True);a=ap.parse_args()
 raw=a.point.read_bytes();doc=json.loads(raw)
 code=a.author_code.read_bytes();tree=ast.parse(code.decode())
 bc=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='bc' for x in n.targets))
 assert bc==[(1,2),(0,3),(0,3),(1,2)]
 weights={int(k):v for k,v in doc['weights'].items()};assert weights=={3:1,12:1}
 assert all(type(v) is int and v>0 for v in weights.values())
 selectors={ast.literal_eval(k):v for k,v in doc['terminal_actions'].items()};assert set(selectors)==set(product(range(4),repeat=2))
 sigma={():0};sigma.update({(i,):bc[i][0] for i in range(4)});sigma.update(selectors)
 assert len(sigma)==21 and all(0<=v<4 for v in sigma.values())
 customers=[mask for mask,count in weights.items() for _ in range(count)]
 def pay(z):
  out=[F(0)]*len(z)
  for mask in customers:
   hit=[i for i,t in enumerate(z) if mask&(1<<t)]
   for i in hit:out[i]+=F(1,len(hit))
  return out
 def finish(h):
  while len(h)<3:h=h+(sigma[h],)
  return h
 def coverage(z):return sum(any(mask&(1<<t) for t in z) for mask in customers)
 table=[];strict=ties=proper=0;minimum=None
 for h in sorted(sigma,key=lambda z:(len(z),z)):
  chosen=sigma[h];base=finish(h);u=pay(base)[len(h)];values=[]
  for alt in range(4):
   leaf=finish(h+(alt,));val=pay(leaf)[len(h)];gap=u-val
   assert gap>=0
   values.append(str(val))
   if alt!=chosen:
    proper+=1
    if gap:strict+=1
    else:ties+=1
    minimum=gap if minimum is None else min(minimum,gap)
  table.append({'history':list(h),'action':chosen,'leaf':list(base),'chosen_payoff':str(u),'all_action_payoffs':values})
 assert proper==63
 branches=[];P=[[F(0) for _ in range(4)] for _ in range(4)]
 for i in range(4):
  z=finish((i,));assert z==(i,*bc[i]);u=pay(z)
  for t in z[1:]:P[t][i]+=F(1,2)
  branches.append({'root':i,'leaf':list(z),'payoffs':list(map(str,u)),'root_minus_average_tail':str(u[0]-(u[1]+u[2])/2)})
 pi=[F(1,4)]*4
 assert all(sum(P[j][i]*pi[i] for i in range(4))==pi[j] for j in range(4))
 assert rank([[P[j][i]-int(j==i) for i in range(4)] for j in range(4)])==3
 defect=sum(pi[r['root']]*F(r['root_minus_average_tail']) for r in branches)
 assert defect==F(-1,4) and all(F(r['root_minus_average_tail'])==defect for r in branches)
 normalized=defect/sum(weights.values());assert normalized==F(-1,8)
 assert F(str(doc['objective']))==F(str(doc['fixed_selector_objective']))==normalized
 assert F(doc['stationary_defect'])==defect
 actual=finish(());u=pay(actual);W=coverage(actual);opt_witness=(0,2,0);assert coverage(opt_witness)==len(customers)==W==2
 static=[]
 for opponents in product(range(4),repeat=2):
  vals=[pay((t,*opponents))[0] for t in range(4)]
  static.append({'opponents':list(opponents),'query_values':list(map(str,vals)),'max_query':str(max(vals))})
 v=min(F(r['max_query']) for r in static);assert v==u[0]==F(1,2)
 pertype={}
 for mask in customers:
  val=F(0)
  for i in range(4):
   z=finish((i,));I=int(bool(mask&(1<<i)));K=sum(bool(mask&(1<<t)) for t in z[1:])
   val+=pi[i]*(F(2*I-K,2*(I+K)) if I+K else 0)
  assert val==F(-1,8);pertype[str(mask)]=str(val)
 out={'status':'passed','scope':'One frozen two-unit-client, four-label saved strategy, not original MILP/LP replay or all-SPE search.','point_sha256':hashlib.sha256(raw).hexdigest(),'author_code_sha256':hashlib.sha256(code).hexdigest(),'players':3,'labels':4,'distinct_cover_sets':2,'unit_customers':2,'weights':doc['weights'],'full_ordered_decision_histories':21,'comparisons_including_self':84,'proper_comparisons':proper,'proper_strict':strict,'proper_ties':ties,'minimum_proper_slack':str(minimum),'full_strategy_and_IC_rows':table,'fixed_root_menu':branches,'P_rows_destination_columns_forced_root':[[str(x) for x in r] for r in P],'unique_stationary_pi':list(map(str,pi)),'rank_P_minus_I':3,'single_customer_defects':pertype,'integer_stationary_defect':str(defect),'normalized_total_weight_one_defect':str(normalized),'integer_clone_scale':2,'actual':list(actual),'actual_payoffs':list(map(str,u)),'W':W,'OPT':W,'opt_witness':list(opt_witness),'static_two_opponent_query_profiles':static,'static_safety_value_v3':str(v),'root_deficiency_v_minus_u':str(v-u[0]),'tail_surplus_over_2v':str(u[1]+u[2]-2*v),'half_margin_2W_minus_OPT':2*W-W,'no_original_audit_import_or_execution':True}
 print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
