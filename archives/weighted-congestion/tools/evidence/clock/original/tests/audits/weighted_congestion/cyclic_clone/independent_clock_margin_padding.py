"""Independent literal audit: fixed-structure clock margin padding obstruction.

No imports from project scripts or author input. The finite audit does not
replace the universal nonnegative-column argument for arbitrary degree caps.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import argparse
import hashlib
import json
import platform
import sys

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
a=parser.parse_args()
w=(F(1),F(1,2),F(1,4),F(1,8)); alpha=F(21,20)
columns=[((0,0,1,1),F(1593928,421875)),((0,1,1,0),F(452978,421875)),((1,-1,-1,-1),F(23816,5859375)),((1,1,-1,-1),F(855968,17578125))]
# A single resource is a tuple (per-player permitted actions, coefficient,degree).
def pair(v,z,p):
 return [(tuple(frozenset({(int(v[i]<0)^side)}) if v[i] else frozenset() for i in range(4)),z,p) for side in (0,1)]
base=[r for v,z in columns for r in pair(v,z,3)]
def costs(resources,s):
 out=[F(0)]*4
 for users,z,p in resources:
  selected=[i for i in range(4) if s[i] in users[i]]
  x=sum((w[i] for i in selected),F(0))
  for i in selected:out[i]+=z*x**p
 return out
def margin(resources,s,i):
 t=list(s);t[i]^=1
 return costs(resources,s)[i]-alpha*costs(resources,t)[i]
S=list(product((0,1),repeat=4));b=(0,1,0,1)
ring=[];s=[0]*4
for _ in range(2):
 for i in range(4):
  ring.append((tuple(s),i));s[i]^=1
assert s==[0]*4
gamma=[margin(base,ring[i][0],i) for i in range(4)]
assert min(gamma)>0
assert [margin(base,s,i) for s,i in ring]==gamma*2
K=[-margin(base,b,i) for i in range(4)];assert min(K)>0
assert gamma==[F(55201793,7500000000),F(1725121,234375000),F(248398189,33750000000),F(49676111,6750000000)]
assert K==[F(122240519,625000000),F(17706129787,33750000000),F(234206903,312500000),F(1009308211,6750000000)]
rows=[];literal_checks=0;column_checks=0
for D in [0,1,3,43,100,1000]:
 U=F(3,2)**D
 # Different from the author's epsilon: this formula was derived independently.
 eps=(alpha-1)*min(gamma)/(2*((alpha-1)+4*U))
 h=[(g-eps)/(alpha-1) for g in gamma]
 assert min(h)>0
 common=[]; separated=[]
 for i in range(4):
  users=tuple(frozenset({0,1}) if j==i else frozenset() for j in range(4))
  common.append((users,h[i]/w[i]**3,3))
  for bit in (0,1):
   users=tuple(frozenset({bit}) if j==i else frozenset() for j in range(4))
   separated.append((users,h[i]/w[i]**3,3))
 padded=base+common
 for s in S:
  comp=tuple(1-x for x in s)
  assert costs(common,s)==h
  assert costs(common,s)==costs(separated,s)
  assert costs(base+common,s)==costs(base+separated,s)
  assert costs(padded,s)==costs(padded,comp)
  for i in range(4):
   assert margin(padded,s,i)==margin(base,s,i)-(alpha-1)*h[i]
   literal_checks+=1
 assert [margin(padded,s,i) for s,i in ring]==[eps]*8
 budget=4*eps/(alpha-1)
 assert all(K[i]+gamma[i]-eps>U*budget for i in range(4))
 # Exact literal monomial budget audit includes all columns through min(D,100).
 for i,j in combinations(range(1,4),2):
  v=tuple(-1 if t==i else (1 if t in (0,j) else 0) for t in range(4))
  W=w[0]+w[i]+w[j];loads=(w[0]+w[i],w[0]+w[j],w[i]+w[j])
  assert W/max(loads)<=F(3,2)
  for k in range(min(D,100)+1):
   resources=pair(v,F(1),k);Sk=sum((x**k for x in loads),F(0))
   gs=[margin(resources,ring[t][0],t) for t in range(4)]
   assert sum(gs)==-(alpha-1)*Sk
   for t in (0,i,j):
    assert margin(resources,b,t)<=U*Sk
    column_checks+=1
 rows.append({'degree_cap':D,'monomial_degrees_checked':[0,min(D,100)],'epsilon':str(eps),'total_S_budget_cap':str(budget),'coarse_efficiency':str(U),'padding_positive':True,'two_private_realization_cost_equivalent':True,'b_survives_every_clock_obeying_budget':True})
result={'scope':'independent finite literal audit supporting all-D fixed-structure padding proof','arithmetic':'fractions.Fraction','seed':None,'python':platform.python_version(),'command':' '.join(sys.argv),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'independence':'hardcoded literal base; no author/repository script or input imports','weights':list(map(str,w)),'alpha':str(alpha),'gamma':list(map(str,gamma)),'K':list(map(str,K)),'literal_state_player_checks':literal_checks,'monomial_player_checks':column_checks,'cases':rows,'result':'PASS'}
text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
if a.output:
 with a.output.open('x') as f:f.write(text)
 print(json.dumps({'output':str(a.output),'result':result['result']}))
else:print(text,end='')
