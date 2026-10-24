"""Exact nonzero implementation audit of the new coordinate construction.
No search; the fixed optimal tuple uses the unchanged 348-unit fixture.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
from collections import defaultdict
import json,hashlib
P=Path(__file__).resolve().parent
src=P.parents[2]/'R-d22a706a03c5499d941a6a97f94128a8/representation/high_insertion_2cycle_348_exact.json'
t=json.loads(src.read_text());m=t['instance']['players'];k=len(t['instance']['topics'])
X=[set(z['topics']) for z in t['instance']['customers'] for _ in range(z['multiplicity'])]
s={tuple(z['history']):z['action'] for z in t['certificate']['actions']}
def finish(h):
 while len(h)<m:h+=(s[h],)
 return h
def count(z):return [sum(a in v for a in z) for v in X]
def pay(z,i):
 c=count(z);return sum((F(1,c[x]) for x,v in enumerate(X) if z[i] in v),F())
B=finish(());T=(5,2,4);cb=count(B);ct=count(T);u=[pay(B,i) for i in range(m)]
opt=max(sum(any(a in v for a in q) for v in X) for q in combinations_with_replacement(range(k),m))
assert sum(c>0 for c in ct)==opt==270
H=[F() for _ in B];d=[];b=[];injection=defaultdict(F);inventory=[F() for _ in X]
for i in range(m):
 W=finish(B[:i]+(T[i],));cw=count(W);rows=[];Q=F();R=F();deficit=F()
 for x,v in enumerate(X):
  if T[i] not in v:continue
  den=cb[x]+1-int(B[i] in v);p=F(1,ct[x]);pb=F();nb=F();q=F();nw=F();edges={}
  for l in range(m):
   if l!=i:
    if B[l] in v and T[l] not in v:val=F(1,ct[x]*den);pb+=val;H[l]+=val
    if T[l] in v and B[l] not in v:nb+=F(1,ct[x]*den)
   if l>i:
    if W[l] in v and B[l] not in v:edges[l]=F(1,den*cw[x]);q+=edges[l]
    if B[l] in v and W[l] not in v:nw+=F(1,den*cw[x])
  r=p-pb;assert r>=0 and p==F(1,cw[x])+pb-nb+q-nw
  assert r-q<=F(1,cw[x]);deficit+=max(F(),r-q)
  R+=r;Q+=min(r,q);rows.append((x,p,pb,r,q,edges))
 assert deficit<=pay(W,i)<=u[i]
 amount=max(F(),R-u[i]);assert amount<=Q
 for x,p,pb,r,q,edges in rows:
  a=amount/Q*min(r,q) if Q else F();current=r-a
  assert 0<=a<=min(r,q)
  delivered=F()
  for l,cap in edges.items():
   val=a*cap/q;assert val<=cap;delivered+=val;injection[W[:l]]+=val
  assert pb+current+delivered==p;inventory[x]+=p
 d.append(R-amount);b.append(amount)
assert all(y==int(c>0) for y,c in zip(inventory,ct))
assert sum(b)==10 and sum(d)+sum(H)+sum(b)==opt
assert all(d[j]<=u[j] and H[j]<=u[j] for j in range(m))
# Replay the existing forward SAFE law only, with the new future sources.
Aout=[F() for _ in B];nonzero=0
for i in range(m):
 for g in sorted(h for h in list(injection) if len(h)==i):
  mass=injection[g]
  if not mass:continue
  old=finish(g);a=old[i];new=finish(B[:i]+(a,));co=count(old);cn=count(new);v=pay(old,i);D=pay(new,i)
  assert v>0 and D<=u[i];neg=F();edges=defaultdict(F)
  for x,L in enumerate(X):
   if a not in L:continue
   Jold={l for l in range(m) if l!=i and old[l] in L};Jnew={l for l in range(m) if l!=i and new[l] in L}
   neg+=F(len(Jold-Jnew),co[x]*cn[x])
   for l in Jnew-Jold:edges[l]+=F(1,co[x]*cn[x])
  keep=D-neg;assert keep>0 and keep+sum(edges.values(),F())==v
  Aout[i]+=mass*keep/v
  for l,q in edges.items():
   nonzero+=1
   if l<i:Aout[l]+=mass*q/v
   else:injection[new[:l]]+=mass*q/v
assert sum(Aout)==sum(b)
residual=[2*u[j]-d[j]-H[j] for j in range(m)]
assert all(Aout[j]<=residual[j] for j in range(m)) # one fixture only, not a theorem
out={'scope':'One exact active-coordinate implementation audit, no general cap evidence.',
 'fixture_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'T':T,'B':B,'OPT':opt,
 'u':list(map(str,u)),'current':list(map(str,d)),'B_columns':list(map(str,H)),
 'future_source':list(map(str,b)),'SAFE_terminal':list(map(str,Aout)),
 'remaining_budget':list(map(str,residual)),'positive_SAFE_edges':nonzero,
 'each_OPT_customer_inventory':'exactly 1','status':'passed'}
with (P/'coordinate_initialization_independent.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out))
