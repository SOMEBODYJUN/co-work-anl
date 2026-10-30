"""Exact full-history audit; fixed uniform fractional background is insufficient.
This does not refute freely optimized fractional security or Q-CAG-HALF.
"""
from fractions import Fraction as F
from itertools import product
base={2:1,9:2,16:1,36:1}
w34={4:1,27:4,29:3,30:3,31:2,32:1,43:3,45:3,46:3,51:3,53:3,54:3,59:2}
def policy(h):
 if not h:return 0
 if len(h)==1:return 3 if h[0]<3 else 0
 grp=range(3) if h[1]<3 else range(3,6)
 return next(a for a in grp if a not in h)
def terminal(h):
 while len(h)<3:h=(*h,policy(h))
 return h
def utility(w,z,i):
 return sum((F(v,sum((mask>>a)&1 for a in z)) for mask,v in w.items() if (mask>>z[i])&1),F())
def run(w,distinct):
 sizes=[frozenset((mask,j) for mask,v in w.items() for j in range(v) if mask>>a&1) for a in range(6)]
 if distinct:assert len(set(sizes))==6
 comparisons=0
 for l in range(3):
  for h in product(range(6),repeat=l):
   chosen=terminal(h);chosen_u=utility(w,chosen,l)
   for a in range(6):
    assert chosen_u>=utility(w,terminal((*h,a)),l),(h,a)
    comparisons+=1
 z=terminal(());u=tuple(utility(w,z,i) for i in range(3))
 g=sum((F(v,1+F(mask.bit_count(),3)) for mask,v in w.items() if mask&1),F())
 assert g>u[0]
 print({'clients':sum(w.values()),'all_labels_distinct':len(set(sizes))==6,'histories':43,'comparisons':comparisons,'path':z,'u':tuple(map(str,u)),'query0_uniform_q_g':str(g),'g_minus_root':str(g-u[0])})
run(base,False)
w=dict(w34)
for mask,v in base.items():w[mask]=w.get(mask,0)+10*v
run(w,True)
q=(F(1,4),F(1,8),F(1,8),F(1,4),F(1,8),F(1,8))
g=tuple(sum((F(v)/(1+2*sum(q[b] for b in range(6) if mask>>b&1)) for mask,v in w.items() if mask>>a&1),F()) for a in range(6))
assert max(g)==F(3188,165)<F(59,3)
print({'free_q':tuple(map(str,q)),'query_values':tuple(map(str,g)),'cap':str(max(g)),'root_minus_cap':str(F(59,3)-max(g))})
