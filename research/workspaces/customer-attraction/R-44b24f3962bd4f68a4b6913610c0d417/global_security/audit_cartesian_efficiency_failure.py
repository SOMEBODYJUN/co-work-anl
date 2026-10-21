"""Unit-customer Fraction audit; independent of discovery and canonical solvers."""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from functools import lru_cache
import json

def unit_topics(a,q):
 rows=[frozenset(('R',i,x)for x in range(a))for i in range(3)]
 cols=[frozenset(('C',c,x)for x in range(q))for c in range(2)]
 return rows,cols,[r|c for r,c in product(rows,cols)]

def action(h):
 if not h:return 0
 i,c=divmod(h[0],2)
 if len(h)==1:return 2*i+1-c
 j,d=divmod(h[1],2)
 k=min(set(range(3))-{i,j})
 e=1-c if c==d else (c if i==j else d)
 return 2*k+e

def utility(topics,z,i):
 return sum((F(1,sum(x in topics[b]for b in z))for x in topics[z[i]]),F())

def term(h):
 while len(h)<3:h=h+(action(h),)
 return h

def full_outcomes(topics):
 # Ordered history, retaining the complete realizable terminal set. This is
 # written here independently; no count cache or imported SPE oracle.
 k=len(topics)
 @lru_cache(None)
 def walk(h):
  if len(h)==3:return {h}
  cc=[walk(h+(a,))for a in range(k)]
  floor=max(min(utility(topics,z,len(h))for z in ch)for ch in cc)
  return {z for ch in cc for z in ch if utility(topics,z,len(h))>=floor}
 return walk(())

def welfare(topics,z):return len(frozenset().union(*(topics[x]for x in z)))

def security_certificate(a,q,topics):
 # Product primal query uses independent uniform row/colour choices. Opponent
 # upper bound chooses two distinct rows uniformly and opposite colours.
 p={s:F(1,6)for s in range(6)}
 backgrounds=list(combinations_with_replacement(range(6),2))
 def payoff(s,b):return sum((F(1,1+sum(x in topics[t]for t in b))for x in topics[s]),F())
 lower=min(sum(p[s]*payoff(s,b)for s in p)for b in backgrounds)
 Q={}
 for i,j in product(range(3),repeat=2):
  if i==j:continue
  for c in range(2):
   b=(2*i+c,2*j+1-c);Q[b]=F(1,12)
 upper=max(sum(prob*payoff(s,b)for b,prob in Q.items())for s in p)
 assert lower==upper==F(2*a,3)+F(q,2)
 return lower

def check(a,q):
 rr,cc,ss=unit_topics(a,q);checks=0
 for length in range(3):
  for h in product(range(6),repeat=length):
   own=utility(ss,term(h),length)
   for s in range(6):
    assert own>=utility(ss,term(h+(s,)),length),(a,q,h,s)
    checks+=1
 z=term(());W=welfare(ss,z)
 assert z==(0,1,2)
 assert [utility(ss,z,i)for i in range(3)]==[F(a+q,2),F(a,2)+q,a+F(q,2)]
 assert W==2*a+2*q
 O=max(welfare(ss,z)for z in product(range(6),repeat=3));assert O==3*a+2*q
 er=full_outcomes(rr);ec=full_outcomes(cc)
 assert {welfare(rr,z)for z in er}=={3*a}
 assert {welfare(cc,z)for z in ec}=={2*q}
 v=security_certificate(a,q,ss);assert W>3*v
 return {'a':a,'q':q,'W':W,'OPT':O,'component_SPE_welfares':[3*a,2*q],'actual':z,'nodes':43,'comparisons_including_self':checks,'v3':str(v),'status':'exact_pass'}

if __name__=='__main__':
 out=[check(a,q)for a,q in [(1,1),(1,2),(1,9),(2,2),(2,7),(7,7),(7,100)]]
 print(json.dumps(out,indent=2))
