"""Independent exact definition-level checks of optimizer-deletion boundaries.
Only standard library; does not import the canonical CAG solver or LP code.
The all-k proof lives in optimizer_deletion_budget.md, not in finite checks.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import factorial
from pathlib import Path
import json

def H(k):return sum((F(1,j) for j in range(1,k+1)),F(0))
def vectors(p,k):
 for z in combinations_with_replacement(range(p),k):
  yield tuple(z.count(a) for a in range(p))
def add(q,b):return tuple(x+y for x,y in zip(q,b))
def phi(rows,z):
 return sum((mult*H(sum(z[a] for a in likes)) for likes,mult in rows),F(0))
def sharp(k,a,t,g):
 p=2*k+1
 A=0;old=range(1,k+1);new=range(k+1,2*k+1)
 rows=[(frozenset([A,*new]),a)]
 rows.extend((frozenset([b]),t) for b in old)
 rows.extend((frozenset([b,d]),g) for b in old for d in new)
 q=(1,)+(0,)*(p-1);empty=(0,)*p
 B=tuple(int(a in old) for a in range(p));D=tuple(int(a in new) for a in range(p))
 responses=list(vectors(p,k))
 valsq={z:phi(rows,add(q,z)) for z in responses}
 vals0={z:phi(rows,z) for z in responses}
 Mq=max(valsq.values());M0=max(vals0.values())
 assert Mq==k*k*g+a*H(k+1)
 assert M0==k*k*g+a*H(k)
 assert valsq[B]==valsq[D]==Mq
 assert vals0[D]==M0 and vals0[B]==k*k*g+k*t
 assert M0-vals0[B]==F(a*k,k+1)
 # Prefix A clients are liked by no selected old responder.
 assert phi(rows,add(q,B))-phi(rows,B)==a
 assert Mq-M0==F(a,k+1)
 return {'k':k,'a':a,'t':t,'g':g,'unit_clients':sum(mult for _,mult in rows),
  'response_multisets':len(responses),'Mq':str(Mq),'M0':str(M0),
  'bonus':str(M0-vals0[B]),'prefix_payoff':str(F(a)),
  'bonus_ratio':str(F(k,k+1)),
  'maximizing_counts_with_prefix':[list(z) for z,v in valsq.items() if v==Mq],
  'maximizing_counts_without_prefix':[list(z) for z,v in vals0.items() if v==M0]}

def nonsubmod():
 rows=[(frozenset([0]),2),(frozenset([1,2]),1),(frozenset([1,3]),1)]
 q=(1,0,0,1)
 def inc(q,a):return tuple(x+int(i==a) for i,x in enumerate(q))
 def M(q):return max(phi(rows,inc(q,a)) for a in range(4))
 vals=[M(q),M(inc(q,2)),M(inc(q,3)),M(inc(inc(q,2),3))]
 assert vals==[F(9,2),F(5),F(29,6),F(11,2)]
 assert vals[0]+vals[3]-vals[1]-vals[2]==F(1,6)
 return {'unit_clients':4,'values':list(map(str,vals)),'submodularity_deficit':'1/6'}

if __name__=='__main__':
 result={'scope':'Finite exact audits of stated central-optimizer examples; not SPE counterexamples',
  'small_sharp_example':sharp(2,12,5,3),
  'general_family_regressions':[], 'envelope_non_submodular':nonsubmod(),'status':'pass'}
 for k in range(1,6):
  a=k*factorial(k+1);t=F(a,k)*(H(k+1)-1);assert t.denominator==1
  t=int(t);g=2*k*t+1
  result['general_family_regressions'].append(sharp(k,a,t,g))
 text=json.dumps(result,indent=2)+'\n'
 print(text)
 Path(__file__).with_name('optimizer_deletion_verified.json').write_text(text)
