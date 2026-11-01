"""Independent Fraction audit; no SPE oracle, numerical LP, or discovery code."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json
from pathlib import Path
ROOT=Path(__file__).parent

def topics(k):
 return [frozenset(((i-1)%k,i)) for i in range(k)]
def u(s,a,q):
 return sum((F(1,sum(x in s[v] for v in q)) for x in s[a]),F(0))
def entrant(s,a,q):
 return sum((F(1,1+sum(x in s[v] for v in q)) for x in s[a]),F(0))
report=[]
for k in (7,8,9,13):
 s=topics(k);menus=[]
 for a in range(k):
  q=(a,(a-1)%k,(a+1)%k)
  vals=[u(s,v,q) for v in q]
  assert vals==[F(1),F(3,2),F(3,2)]
  last=(a+1)%k
  better=next(v for v in range(k) if entrant(s,v,q[:2])>u(s,last,q))
  menus.append({'root':a,'profile':q,'utilities':list(map(str,vals)),'last_profitable_action':better,'last_profit':str(entrant(s,better,q[:2])-u(s,last,q))})
 vals=[]
 for n in range(2,min(5,k//2+2)):
  target=F(2)-F(2*(n-1),k)
  count=0;min_uniform=None
  for q in combinations_with_replacement(range(k),n-1):
   x=sum((entrant(s,a,q) for a in range(k)),F(0))/k
   assert x>=target
   min_uniform=x if min_uniform is None else min(min_uniform,x)
   count+=1
  base=tuple(2*j for j in range(n-1))
  mixed_query=[sum((entrant(s,a,tuple((v+z)%k for v in base)) for z in range(k)),F(0))/k for a in range(k)]
  assert all(v==target for v in mixed_query)
  assert min_uniform==target
  vals.append({'n':n,'backgrounds':count,'v_n':str(target),'cap_minus_u':str(target-1),'query_payoffs':list(map(str,mixed_query))})
 report.append({'k':k,'menus':menus,'security':vals})
odd=[]
for h in range(1,6):
 r=2*h+1;n=r+1;k=(h+1)*(2*h+1)+1
 assert k>=7 and k>=2*(n-1)
 s=topics(k);root_value=F(2,h+1);tail_value=F(1,h)+F(1,h+1)
 assert tail_value-root_value==F(1,h*(h+1))>0
 for a in range(k):
  q=(a,)+((a-1)%k,)*h+((a+1)%k,)*h
  assert u(s,a,q)==root_value
  assert all(u(s,v,q)==tail_value for v in q[1:])
  far=(a+3)%k
  assert entrant(s,far,q[:-1])==2>tail_value
 for c in range(n):assert F(1,1+c)>=1-F(c,2)
 base=tuple(2*j for j in range(n-1));target=F(2)-F(2*(n-1),k)
 caps=[sum((entrant(s,a,tuple((v+z)%k for v in base)) for z in range(k)),F(0))/k for a in range(k)]
 assert all(v==target for v in caps)
 assert target/root_value>h
 odd.append({'h':h,'r':r,'n':n,'k':k,'menus':k,'root':str(root_value),'tail':str(tail_value),'tail_gap':str(tail_value-root_value),'v_n':str(target),'ratio_v_n_over_root':str(target/root_value),'last_deviation_value':'2','static_check':'integer scalar lower bound plus all query rotation caps; no full background enumeration for this block'})
result={'claim':'abstract menu bridge false with unbounded odd-r multiplicative loss','method':'all exact Fraction; full enumeration only in cases; odd_r uses proved scalar lower bound and all rotation caps','cases':report,'odd_r':odd}
(ROOT/'cycle_threshold_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'base_menus':sum(len(x['menus']) for x in report),'static_cases':sum(len(x['security']) for x in report),'backgrounds':sum(y['backgrounds'] for x in report for y in x['security']),'odd_menus':sum(x['menus'] for x in odd),'odd_r':odd,'k7_v4':next(y['v_n'] for y in report[0]['security'] if y['n']==4),'all_checks':True}))
