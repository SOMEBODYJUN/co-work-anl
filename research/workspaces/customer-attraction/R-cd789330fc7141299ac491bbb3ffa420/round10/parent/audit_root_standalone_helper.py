"""One exact candidate counterexample, complete ordered-history certificate.
Refutes root query row >= comparison union - largest topic, even q=m.
Does not refute net ROW or HALF. No instance or parameter search.
"""
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
P=Path(__file__).resolve().parent
m=k=6;sizes=(3,3,1,1,1,1)
def add(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
@lru_cache(None)
def solve(q):
 if sum(q)==m:return q,None
 options=[]
 for a in range(k):
  terminal,_=solve(add(q,a))
  options.append((F(sizes[a],terminal[a]),a,terminal))
 best=max(v for v,a,z in options)
 _,a,z=next(record for record in options if record[0]==best)
 return z,a
expected=[h for n in range(m) for h in product(range(k),repeat=n)]
sigma={h:solve(tuple(h.count(a) for a in range(k)))[1] for h in expected}
def finish(h):
 while len(h)<m:h+=(sigma[h],)
 return h
def pay(z,i):return F(sizes[z[i]],z.count(z[i]))
slacks=[]
for h in expected:
 i=len(h);u=pay(finish(h),i)
 for a in range(k):
  gap=u-pay(finish(h+(a,)),i);assert gap>=0,(h,a)
  slacks.append(gap)
z=finish(()); W=sum(sizes[a] for a in set(z)); OPT=sum(sizes)
D=[pay(finish((a,)),0) for a in range(k)];row=sum(D,F())
assert W==6 and OPT==10 and max(sizes)==3 and D==[F(1)]*k and row<OPT-max(sizes)
I={'players':m,'topics':[f'S{a}' for a in range(k)],'customers':[{'topics':[a],'multiplicity':size} for a,size in enumerate(sizes)]}
output={'scope':'Counterexample to stronger standalone-K root-row helper only; original net ROW and HALF hold here.',
 'instance':I,'certificate':{'actions':[{'history':list(h),'action':sigma[h]} for h in expected]},
 'actual':z,'actual_profits':[str(pay(z,i)) for i in range(m)],'W':W,'OPT':OPT,'largest_topic':max(sizes),
 'comparison_tuple':list(range(k)),'root_true_query_payoffs':list(map(str,D)),'root_query_sum':str(row),
 'helper_gap':str(row-(OPT-max(sizes))),'net_ROW_gap':str(row-(OPT-W)),
 'ordered_histories':len(expected),'IC_including_self':len(slacks),'minimum_IC_slack':str(min(slacks)),
 'construction':'Full backward induction on count states, lowest-label equilibrium tie; not myopic greedy.',
 'status':'passed','original_HALF':'not_refuted'}
with (P/'root_standalone_helper_exact_counterexample.json').open('x') as f:json.dump(output,f,indent=2);f.write('\n')
print(json.dumps({x:output[x] for x in ('status','W','OPT','root_query_sum','helper_gap','net_ROW_gap','ordered_histories','IC_including_self')}))
