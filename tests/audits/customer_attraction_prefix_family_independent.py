"""Independent direct-type audit of CA-PREFIX-BALANCE-NO.

No imports from the construction author, canonical model, solver, or verifier.
The universal theorem is algebraic; these finite cases are supplementary.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement,product
from functools import lru_cache
from math import lcm,factorial
from pathlib import Path
import json,time,argparse
from hashlib import sha256
reports=[]
for n in range(4,9):
 start=time.time();x=n-2;p=n+2;scale=lcm(*range(1,n+1))
 types=[]
 for j in range(n):
  leaf=j+2;types += [((leaf,),x),((1,leaf),x)]
  types.append(((0,leaf),1) if j<n-1 else ((0,1,leaf),n-1))
 @lru_cache(None)
 def values(q):
  v=[0]*p
  for B,w in types:
   den=sum(q[a] for a in B)
   if den:
    for a in B:
     if q[a]:v[a]+=w*(scale//den)
  return tuple(v)
 def add(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
 def best(q):
  val=[values(add(q,a))[a] for a in range(p)];mx=max(val)
  return next(a for a in (1,0,*range(2,p)) if val[a]==mx)
 def action(q):
  t=sum(q)
  if t==0:return 0
  if t<n-1:return 0 if q[1]==t else 1
  return best(q)
 @lru_cache(None)
 def follow(q):
  if sum(q)==n:return q
  return follow(add(q,action(q)))
 def welfare(q):return sum(w for B,w in types if any(q[a] for a in B))
 def multi(q):return factorial(sum(q))//__import__('functools').reduce(lambda a,b:a*factorial(b),q,1)
 nodes=comps=orderednodes=orderedcomps=lastclasses=0;minpositive=None
 for t in range(n):
  for h in combinations_with_replacement(range(p),t):
   q=tuple(h.count(a) for a in range(p));a=action(q);own=values(follow(q))[a]
   if t==n-1:
    v=[values(add(q,b))[b] for b in range(p)];a0=q[0];ll=sum(q[2:])
    if a0 or ll>=2:assert v[1]==max(v)
    elif ll==0:assert v[0]>max(v[1:])
    elif q[-1]==1:assert v[0]==max(v)
    else:
     chosen=next(b for b in range(2,p-1) if q[b])
     fresh=[b for b in range(2,p) if b!=chosen];assert all(v[b]==max(v) for b in fresh)
    lastclasses+=1
   for b in range(p):
    alt=values(follow(add(q,b)))[b];gap=own-alt;assert gap>=0,(n,q,a,b,gap)
    if gap>0:minpositive=gap if minpositive is None else min(minpositive,gap)
   m=multi(q);nodes+=1;comps+=p;orderednodes+=m;orderedcomps+=m*p
 root=(0,)*p;end=follow(root);pay=[F(values(end)[a],scale) for a in (0,*(1 for _ in range(n-1)))];W=welfare(end);total=sum(w for _,w in types)
 assert pay[0]==F(n)-F(1,n) and all(v==F(n)-F(1,n)-F(1,n-1) for v in pay[1:])
 assert W==n*n-2 and total==2*n*n-2*n-2
 # Exhaust all n-theme supports and all n-1 theme support extensions to A.
 opt=max(welfare(tuple(int(a in S) for a in range(p))) for S in combinations_with_replacement(range(p),n))
 vals=[]
 for S in combinations_with_replacement(range(p),n-1):
  q=tuple(int(a in S or a==0) for a in range(p));vals.append(welfare(q))
 extension=max(vals);assert opt==total and extension==2*(n-1)*(n-1)
 B=pay[0]+extension-opt;assert B==F(4-n)-F(1,n)<0
 tau=F(n-1,2)+F(n*(n-2)**2,n-1)+F((n-1)**2,n)
 assert W+tau-opt==F(n-3,2)+F(1,n-1)+F(1,n)>0
 reports.append({'n':n,'customers':total,'count_decision_nodes':nodes,'count_action_comparisons':comps,'represented_ordered_nodes':orderednodes,'represented_ordered_comparisons':orderedcomps,'last_classification_states':lastclasses,'minimum_positive_slack':str(F(minpositive,scale)),'W':W,'OPT':opt,'F_after_A':extension,'u1':str(pay[0]),'B1':str(B),'root_tax_slack':str(W+tau-opt),'half_slack':2*W-opt,'elapsed_seconds':time.time()-start})
 print(reports[-1],flush=True)
result={'status':'independent exact all-n-family finite audit passed','scope':'Universal proof reviewed algebraically; count enumeration represents every ordered history of this explicitly count-based strategy, not a restriction on general SPE. Finite n4..8 audits do not prove the universal family.','cases':reports}
result['audit_sha256']=sha256(Path(__file__).read_bytes()).hexdigest()
result['totals']={key:sum(case[key] for case in reports) for key in ('count_decision_nodes','count_action_comparisons','represented_ordered_nodes','represented_ordered_comparisons')}
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path)
args=parser.parse_args()
payload=json.dumps(result,indent=2)+'\n'
if args.output:
 with args.output.open('x',encoding='utf-8') as stream:stream.write(payload)
else:
 print(payload)

