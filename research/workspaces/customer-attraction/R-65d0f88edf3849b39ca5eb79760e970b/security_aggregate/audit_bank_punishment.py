"""Definition-level Fraction audit of the analytic all-parameter bank proof.

Only checks a finite implementation of the recursive construction.  The
unbounded statement is proved in bank_punishment_blind_proof.md, not inferred
from these cases.  A (background,target) DAG retains the target memory and
unfolds to a full ordered-history strategy; it is not an SPE outcome solver.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
summary=[]
for m in range(2,8):
 for j in range(1,m):
  k=m-j;a=(2,)*j+(k,)+(1,)*(k-1);p=len(a)
  assert p==m
  nodes=rows=cases=0;mingap=None
  def add(v,d):
   x=list(v);x[d]+=1;return tuple(x)
  @lru_cache(None)
  def greedy(b,r):
   q=[0]*p
   for _ in range(r):
    d=max(range(p),key=lambda d:(F(a[d],b[d]+q[d]+1),-d))
    q[d]+=1
   return tuple(q)
  def phi(b,q):
   return sum((F(a[d],b[d]+t)for d in range(p)for t in range(1,q[d]+1)),F())
  @lru_cache(None)
  def visit(b,q):
   global nodes,rows,mingap
   nodes+=1;r=sum(q)
   assert phi(b,q)==phi(b,greedy(b,r))
   if not r:return (0,)*p
   star=max((d for d in range(p)if q[d]),key=lambda d:(F(a[d],b[d]+q[d]),-d))
   pays=[];children=[]
   for d in range(p):
    nb=add(b,d)
    if q[d]:
     nq=list(q);nq[d]-=1;nq=tuple(nq)
    else:nq=greedy(nb,r-1)
    tail=visit(nb,nq)
    pays.append(F(a[d],nb[d]+tail[d]));children.append(tail)
   for d,u in enumerate(pays):
    gap=pays[star]-u;assert gap>=0
    rows+=1;mingap=gap if mingap is None else min(mingap,gap)
   term=add(children[star],star);assert term==q
   return term
  for i in range(1,j+1):
   prefix=tuple(int(d<i-1)for d in range(p))
   for D in range(p):
    b=add(prefix,D);r=m-i
    if D<j and not prefix[D]:
     q=[0]*p
     for d in range(j):
      if b[d]==0:q[d]=1
     q[D]=1;q[j]=k-1;q=tuple(q)
    elif D==j:
     q=[0]*p
     for d in range(j):
      if b[d]==0:q[d]=1
     q[j]=k-1;q=tuple(q)
    else:q=greedy(b,r)
    assert sum(q)==r
    terminal=visit(b,q)
    current=F(a[D],b[D]+terminal[D]);assert current<=1
    cases+=1
  summary.append({'m':m,'j':j,'forced_children':cases,'construction_DAG_states':nodes,'nonterminal_action_comparisons':rows,'minimum_IC_gap':str(mingap)})
report={'status':'PASS','scope':'finite exact implementation audit of all-parameter proof; not the general proof','parameter_range':'2<=m<=7, all 1<=j<m, all 1<=i<=j, all forced bank labels','scale':'s=1; rational positive s rescales every comparison','rows':summary,'totals':{'forced_children':sum(z['forced_children']for z in summary),'construction_DAG_states':sum(z['construction_DAG_states']for z in summary),'nonterminal_action_comparisons':sum(z['nonterminal_action_comparisons']for z in summary)}}
(OUT/'bank_punishment_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
