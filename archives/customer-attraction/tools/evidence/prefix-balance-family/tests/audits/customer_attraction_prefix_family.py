"""Exact finite audits of the analytic prefix family; no universal inference."""
from functools import lru_cache
from math import lcm,comb
from fractions import Fraction as F
from pathlib import Path
import json,time,argparse
from hashlib import sha256

def compositions(total,size):
 if size==1:
  yield (total,);return
 for first in range(total+1):
  for rest in compositions(total-first,size-1):yield (first,)+rest

def audit(n):
 x=n-2;p=n+2;scale=lcm(*range(1,n+1));types=[]
 for j in range(2,p-1):types.extend([((j,),x),((0,j),1),((1,j),x)])
 types.extend([((p-1,),x),((1,p-1),x),((0,1,p-1),n-1)])
 def add(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
 @lru_cache(None)
 def pay(q):
  out=[0]*p
  for ts,w in types:
   d=sum(q[a] for a in ts)
   if d:
    for a in ts:out[a]+=w*(scale//d)
  return out
 priority=(1,0)+tuple(range(2,p))
 @lru_cache(None)
 def action(q):
  t=sum(q)
  if t==n-1:return max(priority,key=lambda a:pay(add(q,a))[a])
  if t==0:return 0
  return 0 if q[1]==t else 1
 @lru_cache(None)
 def terminal(q):
  if sum(q)==n:return q
  return terminal(add(q,action(q)))
 checked=ties=0;minpositive=None
 for t in range(n):
  for q in compositions(t,p):
   a=action(q);actual=pay(terminal(q))[a]
   for b in range(p):
    deviation=pay(terminal(add(q,b)))[b];assert actual>=deviation,(n,q,a,b,F(actual,scale),F(deviation,scale))
    checked+=1;ties+=actual==deviation
    if actual>deviation:minpositive=(actual-deviation) if minpositive is None else min(minpositive,actual-deviation)
   if t==n-1:
    a0,b0=q[:2];leaves=sum(q[2:])
    if a0 or leaves>=2:expected=1
    elif leaves==0:expected=0
    elif q[-1]:expected=0
    else:expected=next(j for j in range(2,p-1) if q[j]==0)
    assert a==expected,(n,q,a,expected)
 q=terminal((0,)*p);assert q==(1,n-1)+(0,)*n
 us=[F(pay(q)[0],scale)]+[F(pay(q)[1],scale)]*(n-1)
 u1=F(n)-F(1,n);v=F(n)-F(1,n)-F(1,n-1)
 assert us==[u1]+[v]*(n-1)
 W=n*n-2;OPT=2*n*n-2*n-2;assert sum(us)==W
 rootB=u1-2*x;tax=F(n-1,2)+F(n*x*x,n-1)+F((n-1)**2,n)
 assert rootB==F(4-n)-F(1,n)<0
 assert W+tax-OPT==F(n-3,2)+F(1,n-1)+F(1,n)>0
 return {'n':n,'topics':p,'customers':sum(w for ts,w in types),'count_history_states':checked//p,'exact_action_comparisons':checked,'ordered_history_nodes_represented':sum(p**t for t in range(n)),'minimum_positive_slack':str(F(minpositive,scale)),'u1':str(u1),'follower_payoff':str(v),'W':W,'OPT':OPT,'F_after_root':OPT-2*x,'B1':str(rootB),'required_first_payoff_multiplier':str(F(2*x)/u1),'root_tax':str(tax),'root_tax_margin':str(W+tax-OPT),'half_coverage_margin':2*W-OPT}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output',type=Path)
 args=parser.parse_args()
 start=time.time();results=[]
 for n in range(4,9):
  result=audit(n);results.append(result);print(json.dumps(result),flush=True)
 report={'claim':'CA-PREFIX-BALANCE-NO','audit_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite family members n4..8. Count states cover all ordered histories because this explicitly constructed policy is count-based. Universal all-n claim relies on analytic Lemmas1/2, not these checks.','cases':results,'elapsed_seconds':time.time()-start}
 encoded=json.dumps(report,indent=2)+'\n'
 if args.output:
  args.output.parent.mkdir(parents=True,exist_ok=True)
  with args.output.open('x',encoding='utf-8') as handle:handle.write(encoded)
 print(encoded,end='')
