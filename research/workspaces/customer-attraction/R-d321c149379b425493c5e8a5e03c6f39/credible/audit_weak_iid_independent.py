"""Definition-level independent all-history audit and rational iid certificates."""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from functools import lru_cache
from pathlib import Path
from math import factorial
import json


def audit_strategy(m,J):
 p=J+2
 topics=[{0,1},set(range(2,2*m))]+[{0,1,2*m+j}for j in range(J)]
 def action(h):
  if not h:return 0
  if len(h)<m-1:return 1
  nb=[a for a in h if a!=1]
  if len(nb)==0:return 2
  if len(nb)==1:return 1 if nb[0]==0 else 2+(nb[0]-2+1)%J
  return 1
 @lru_cache(None)
 def finish(h):
  return h if len(h)==m else finish(h+(action(h),))
 def utility(path,i):
  return sum((F(1,sum(x in topics[a]for a in path))for x in topics[path[i]]),F())
 comparisons=histories=0
 for d in range(m):
  for h in product(range(p),repeat=d):
   actual=finish(h);own=utility(actual,d)
   for a in range(p):
    alt=finish(h+(a,))
    assert own>=utility(alt,d),(m,J,h,a,actual,alt)
    comparisons+=1
   histories+=1
 path=finish(())
 assert path==(0,)+(1,)*(m-1)
 assert [utility(path,i)for i in range(m)]==[F(2)]*m
 W=len(set().union(*(topics[a]for a in path)))
 OPT=max(len(set().union(*(topics[a]for a in q)))for q in combinations_with_replacement(range(p),m))
 assert W==2*m and OPT==2*m+min(J,m-1)
 return {'m':m,'J':J,'histories':histories,'comparisons_including_self':comparisons,'W':W,'OPT':OPT,'all_ordered_histories_verified':True}


def f(m,p):return (1-(1-p)**m)/(m*p)if p else F(1)
def D(m,b,J=100):return 2*(m-1)*f(m,b)-2*f(m,1-b)-f(m,(1-b)/J)
def iid_certificate():
 m=20;J=100;lo=F(92579,100000);hi=F(4629,5000)
 assert D(m,lo)>F(1,20000)
 assert D(m,hi)<-F(1,25000)
 lower=2*(m-1)*(1-(1-lo)**m)+2*(1-hi**m)+J*(1-(1-(1-hi)/J)**m)
 assert lower>F(8209,200)
 assert F(39,40)*F(8209,200)-40==F(151,8000)>0
 assert sum((F(3,2)**j/F(factorial(j))for j in range(6)),F())==F(5711,1280)>F(40,9)
 assert F(31,1200)>F(2,79)
 assert F(80,2**41)<F(1,100)
 assert F(823,800)>F(82,81)
 return {'m':m,'J':J,'b_lower':str(lo),'b_upper':str(hi),'D_lower_strict_bound':'1/20000','D_upper_strict_bound':'-1/25000','Z_lower_strict_bound':'8209/200','weak_bridge_gap_lower_strict_bound':'151/8000','infinite_m_threshold':41,'all_rational_comparisons_verified':True}

if __name__=='__main__':
 report={'identity':'blind independent definition-level audit of weak-iid family','strategy_cases':[audit_strategy(m,J)for J in (2,3)for m in range(2,7)],'iid_certificate':iid_certificate(),'scope':'finite replay audits symbolic all-m proof; not a half counterexample'}
 out=Path(__file__).with_name('audit_weak_iid_independent.json');out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
