"""Definition-level blind audit: no canonical solver or parent discovery imported."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
A,B,C=range(3)
clients=[{A,B}]*3+[{A,C}]*3+[{B}]+[{C}]
actions={():A,(A,):A,(B,):A,(C,):A,
 (A,A):C,(A,B):C,(A,C):B,(B,A):C,(B,B):A,(B,C):A,
 (C,A):B,(C,B):A,(C,C):A}
def complete(h):
 while len(h)<3:h=h+(actions[h],)
 return h
def utility(h,i):
 return sum((F(1,sum(a in x for a in h)) for x in clients if h[i] in x),F(0))
def welfare(h):return sum(any(a in x for a in h) for x in clients)
rows=[]
for k in range(3):
 for h in product(range(3),repeat=k):
  out=complete(h);pay=utility(out,k)
  comparisons=[]
  for a in range(3):
   dev=complete(h+(a,));v=utility(dev,k)
   assert pay>=v
   comparisons.append({'action':a,'outcome':dev,'utility':str(v)})
  rows.append({'history':h,'chosen':actions[h],'actual_utility':str(pay),'comparisons':comparisons})
actual=complete(());W=welfare(actual);OPT=max(welfare(h) for h in product(range(3),repeat=3))
menu=[complete((a,))[1:] for a in range(3)]
M=[[utility((t,)+q,0) for q in menu] for t in range(3)]
cap=F(5,2)
assert all(v==cap for v in M[A])
assert all(v<=cap for row in M for v in row)
# A guarantees 2 against every deterministic two-opponent tuple.
assert min(utility((A,)+q,0) for q in product(range(3),repeat=2))==2
assert all(utility((t,A,A),0)==2 for t in range(3))
result={'status':'exact finite full strategy audit; analytic cap and security certificate supplied',
 'histories':len(rows),'comparisons_including_self':sum(len(r['comparisons']) for r in rows),
 'actual':actual,'W':W,'OPT':OPT,'menu':menu,
 'menu_query_matrix':[[str(v) for v in row] for row in M],
 'menu_cap':str(cap),'static_security':'2','strong_threshold_W_over_3':str(F(W,3)),
 'weak_threshold_W_over_2.5':str(F(2*W,5)), 'rows':rows}
print(json.dumps(result,indent=2))
