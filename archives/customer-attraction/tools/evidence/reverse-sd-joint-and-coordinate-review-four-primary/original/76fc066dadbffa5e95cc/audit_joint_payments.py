"""Independent exact audit of stated joint bounds, never a welfare proof.
Uses an unchanged complete SPE fixture; imports no solver/author audit.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import hashlib,json,platform
P=Path(__file__).resolve().parent
src=P.parents[2]/'R-d22a706a03c5499d941a6a97f94128a8/representation/high_insertion_2cycle_348_exact.json'
f=json.loads(src.read_text());ins=f['instance']; m=ins['players'];k=len(ins['topics'])
likes=[set(t['topics']) for t in ins['customers'] for _ in range(t['multiplicity'])]
sigma={tuple(z['history']):z['action'] for z in f['certificate']['actions']}
def finish(h):
 h=tuple(h)
 while len(h)<m:h+=sigma[h],
 return h
def counts(z):return [sum(a in X for a in z) for X in likes]
def profit(z,j):
 c=counts(z)
 return sum((Q(1,c[x]) for x,X in enumerate(likes) if z[j] in X),Q())
Z=finish(());cz=counts(Z);nodes=ics=pairs=pos_prefix=pos_columns=projections=0
for i in range(m):
 for h in product(range(k),repeat=i):
  nodes+=1;B=finish(h);cb=counts(B);v=profit(B,i)
  for a in range(k):
   W=finish(h+(a,));cw=counts(W);assert v>=profit(W,i);ics+=1;pairs+=1
   # Joint prefix claims onto a single parent B, signs independent of sigma.
   matrix=[[Q() for l in range(m)] for j in range(i)]
   for j in range(i):
    Nj=Q()
    for x,X in enumerate(likes):
     if B[j] not in X:continue
     old={l for l in range(i,m) if B[l] in X}
     new={l for l in range(i,m) if W[l] in X}
     Nj+=Q(len(new-old),cb[x]*cw[x])
     for l in old-new:matrix[j][l]+=Q(1,cb[x]*cw[x])
    base=profit(B,j)-Nj
    assert base>=0 and base+sum(matrix[j],Q())==profit(W,j)
   for l in range(i,m):
    col=sum((matrix[j][l] for j in range(i)),Q())
    assert col<=profit(B,l)
    pos_prefix+=col>0
  # Static denominator SD and first-positive column cap on this fixed B.
  tax=[[Q() for l in range(m)] for ii in range(m)]
  for ii in range(m):
   W=finish(B[:ii]+(Z[ii],));cw=counts(W)
   # This theta identity holds for any B, even if B is not prescribed at ii.
   theta=tb=tw=Q()
   for x,X in enumerate(likes):
    if Z[ii] not in X:continue
    d=cb[x]+1-int(B[ii] in X);assert d>=1
    theta+=Q(1,d)
    tb+=Q(sum(int(B[l] in X)-int(Z[l] in X) for l in range(m) if l!=ii),cz[x]*d)
    tw+=Q(sum(int(W[l] in X)-int(B[l] in X) for l in range(ii+1,m)),d*cw[x])
    for l in range(m):
     if l!=ii and B[l] in X and Z[l] not in X:tax[ii][l]+=Q(1,cz[x]*d)
   assert profit(Z,ii)==theta+tb
   assert theta==profit(W,ii)+tw
  for l in range(m):
   col=sum((tax[ii][l] for ii in range(m)),Q());assert col<=profit(B,l)
   pos_columns+=col>0
# Arbitrary synthetic leaves: current profit need not be a prescribed completion.
for F in product(range(k),repeat=m):
 cf=counts(F)
 for j in range(m):
  R=finish(F[:j+1]);cr=counts(R);V=profit(finish(F[:j]),j);d=profit(R,j)
  assert V>=d
  q=[Q() for _ in range(m)];N=Q()
  for x,X in enumerate(likes):
   if F[j] not in X:continue
   old={l for l in range(m) if l!=j and F[l] in X}
   new={l for l in range(m) if l!=j and R[l] in X}
   N+=Q(len(old-new),cf[x]*cr[x])
   for l in new-old:
    assert l>j;q[l]+=Q(1,cf[x]*cr[x])
  absorb=d-N
  assert absorb>=0 and absorb+sum(q,Q())==profit(F,j)
  assert absorb<=V and all(x<=absorb for x in q)
  projections+=1
out={'scope':'Implementation and algebra checks only; no HALF or role-wallet-cap evidence.',
 'python':platform.python_version(),'fixture_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
 'unit_customers':len(likes),'ordered_nodes':nodes,'IC_including_self':ics,
 'parent_child_pairs':pairs,'nonzero_prefix_columns':pos_prefix,
 'nonzero_static_tax_columns':pos_columns,'synthetic_role_projections':projections,
 'status':'passed'}
output=P/'joint_payments_independent.json'
with output.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out))
