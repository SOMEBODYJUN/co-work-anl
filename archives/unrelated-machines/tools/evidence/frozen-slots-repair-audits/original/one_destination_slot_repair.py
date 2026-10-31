"""同机槽族的单目的地修复：原任务穷举与聚合整数流审计。

The exponential enumerations are only finite oracles; the general statement
is the path construction and prefix-cut proof in the current manuscript.
"""
from itertools import product
from math import comb
import json

def sigma(m):
 # job 0 big; then m-1 small at 0; m at each remaining machine
 return (0,)*m+tuple(i for i in range(1,m) for _ in range(m))

def actual(m):
 old=sigma(m);best={True:10**9,False:10**9};count={True:0,False:0};w={}
 for tau in product(range(m),repeat=m*m):
  b=tau[0];small=[0]*m
  for v in tau[1:]:small[v]+=1
  if small[b] or any(small[v]!=m+1 for v in range(m) if v!=b):continue
  good=True
  for i in range(m):
   ds={tau[j] for j in range(m*m) if old[j]==i and tau[j]!=i}
   if len(ds)>1:good=False;break
  if not good:continue
  stay=(b==0);cnt=sum(a!=b for a,b in zip(old,tau));count[stay]+=1
  if cnt<best[stay]:best[stay]=cnt;w[stay]=list(tau)
 return {'m':m,'all_assignments':m**(m*m),'min_support_big_stays':best[True],'min_support_big_moves':best[False], 'feasible_count_big_stays':count[True],'feasible_count_big_moves':count[False], 'witnesses':{str(k):v for k,v in w.items()}}

def aggregate(m,movebig):
 oldsmall=[m-1]+[m]*(m-1);best=10**9;w=None;cases=0;feasible=0
 # By symmetry choose final big machine1 if moved. The origin0 cannot send small there.
 b=1 if movebig else 0
 opts=[]
 for i in range(m):
  if i==0:
   opts.append([(0,-1)] if movebig else [(m-1,v) for v in range(1,m)])
  elif i==b:opts.append([(m,v) for v in range(m) if v!=i])
  else:opts.append([(0,-1)]+[(q,v) for q in range(1,oldsmall[i]+1) for v in range(m) if v!=i])
 for moves in product(*opts):
  cases+=1;after=oldsmall.copy()
  for i,(q,v) in enumerate(moves):
   after[i]-=q
   if q:after[v]+=q
  if after[b]!=0 or any(after[i]!=m+1 for i in range(m) if i!=b):continue
  feasible+=1;support=sum(q for q,v in moves)+int(movebig)
  if support<best:best=support;w=list(moves)
 return {'m':m,'big_moves':movebig,'aggregate_cases':cases,'feasible_count':feasible,'min_support':best,'witness':w}

rs={'actual_job_assignments':[actual(m) for m in [2,3]],'aggregate_counts':[aggregate(m,b) for m in [2,3,4,5] for b in [False,True]]}
for z in rs['actual_job_assignments']:
 m=z['m'];assert z['min_support_big_stays']==m*(m-1)//2;assert z['min_support_big_moves']==m*(m+1)//2
for z in rs['aggregate_counts']:
 m=z['m'];assert z['min_support']==m*(m+(1 if z['big_moves'] else -1))//2
print(json.dumps(rs,indent=2))
