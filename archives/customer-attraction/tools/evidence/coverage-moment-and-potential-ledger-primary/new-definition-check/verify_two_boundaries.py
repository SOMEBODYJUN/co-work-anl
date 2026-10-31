from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import json
base=Path(__file__).resolve().parent
raw=json.loads((base/'dr-potential-input.json').read_text());phi={():F(0)}
for k,v in raw['phi'].items():phi[tuple(map(int,k))]=F(v)
assert len(phi)==84
get=lambda q:phi[tuple(sorted(q))]
mono=[];dr=[]
for size in range(3):
 for q in combinations_with_replacement(range(6),size):
  for a in range(6):
   value=get(q+(a,))-get(q);assert value>=0;mono.append(dict(q=list(q),a=a,value=str(value)))
for size in range(2):
 for q in combinations_with_replacement(range(6),size):
  for a,b in product(range(6),repeat=2):
   value=get(q+(a,))-get(q)-get(q+(a,b))+get(q+(b,));assert value>=0;dr.append(dict(q=list(q),a=a,b=b,value=str(value)))
assert len(mono)==168 and len(dr)==252

def dr_action(h):
 if not h:return 0
 if len(h)==1:return 3 if h[0]<3 else 0
 group=range(3) if h[1]<3 else range(3,6)
 return min(a for a in group if a not in h)
def dr_pay(path,i):return get(path)-get(path[:i]+path[i+1:])
def audit_policy(action,pay):
 def leaf(h):
  while len(h)<3:h=h+(action(h),)
  return h
 rows=[];strict=0
 for size in range(3):
  for h in product(range(6),repeat=size):
   values=[pay(leaf(h+(a,)),size) for a in range(6)];choice=action(h);assert values[choice]==max(values),(h,values,choice)
   strict+=sum(values[choice]>v for v in values)
   rows.append(dict(history=list(h),action=choice,values=list(map(str,values)),leaves=[list(leaf(h+(a,))) for a in range(6)]))
 assert len(rows)==43
 actual=leaf(())
 return dict(histories=43,including_self_comparisons=258,nonself_comparisons=215,strict_comparisons=strict,rows=rows,actual=list(actual),actual_payoffs=[str(pay(actual,i)) for i in range(3)])
da=audit_policy(dr_action,dr_pay);assert da['actual']==[0,3,4] and da['actual_payoffs']==['0','105','56']
p=[F(x,15) for x in [4,0,4,0,3,4]];safety=[]
for bg in combinations_with_replacement(range(6),2):
 values=[get(bg+(a,))-get(bg) for a in range(6)];mean=sum((p[a]*values[a] for a in range(6)),F(0));assert mean>=56
 safety.append(dict(background=list(bg),query_values=list(map(str,values)),query_mean=str(mean)))
assert min(F(x['query_mean']) for x in safety)==56
upper=[get((0,3,a))-get((0,3)) for a in range(6)];assert upper==list(map(F,[56,56,56,0,56,56]));assert get((1,1))==get((1,))==161

# Eleven distinct unit customers from the complete Markdown table, no author imports.
types=[({0},2),({1,2},1),({2,3},1),({0,1,4},1),({1,2,4},1),({5},2),({3,4,5},3)]
clients=[set(s) for s,n in types for _ in range(n)];assert len(clients)==11
exceptions={frozenset([0,5]):4,frozenset([2,5]):4,frozenset([3,5]):1,frozenset([4,5]):2,frozenset([5]):1}
def cag_action(h):
 if not h:return 1
 if len(h)==1:return 1 if h[0]==5 else 5
 return exceptions.get(frozenset(h),5)
def loads(path):return [sum(a in x for a in path) for x in clients]
def cag_pay(path,i):
 q=loads(path);return sum((F(1,q[j]) for j,x in enumerate(clients) if path[i] in x),F(0))
ca=audit_policy(cag_action,cag_pay);assert ca['actual']==[1,5,5] and ca['actual_payoffs']==['3','5/2','5/2'] and ca['strict_comparisons']==188
profile=tuple(ca['actual']);q=loads(profile);spectrum={str(k):q.count(k) for k in sorted(set(q))};assert spectrum=={'0':3,'1':3,'2':5}
harmonic=lambda k:sum((F(1,j) for j in range(1,k+1)),F(0))
potential=sum((harmonic(k) for k in q),F(0));truncated=sum((min(harmonic(k),F(2)) for k in q),F(0));covers=[sum(k>0 for k in loads(path)) for path in product(range(6),repeat=3)];assert len(covers)==216 and max(covers)==11 and potential==truncated==F(21,2)
result=dict(status='pass',original_program_calls=0,new_execution_scope='Two independent exact fixed-definition boundary checks; no LP/MIP/SPE solver discovery or author implementation imports.',expanded_DR_model=dict(phi_values=84,monotonicity_checks=168,DR_checks=252,monotonicity_rows=mono,DR_rows=dr,complete_policy=da,security_p=list(map(str,p)),static_backgrounds=safety,dual_background=[0,3],dual_query_values=list(map(str,upper)),exact_security_value='56',actual_total_payoff='161',strong_gap='-7',weak_gap='21',pure_diagonal_2phi11_minus3phi1='-161',same_support_P1='161',same_support_P11='0',not_a_CAG_input=True),unit_CAG=dict(customers=11,types=[dict(labels=sorted(s),units=n) for s,n in types],complete_policy=ca,actual_load_spectrum=spectrum,actual_coverage=8,all_216_terminal_coverages=covers,OPT3=11,harmonic_potential=str(potential),truncated_potential=str(truncated),potential_minus_OPT='-1/2',half_slack=5))
print(json.dumps(result,ensure_ascii=False,indent=2))
