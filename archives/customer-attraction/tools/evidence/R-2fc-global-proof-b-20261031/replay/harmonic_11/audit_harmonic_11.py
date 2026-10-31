from fractions import Fraction as F
from itertools import product
import json
# 11 distinct clients from rows of the published harmonic obstruction.
topics = [
 {0,1,2}, {0,1,3}, {2,3,4}, {0,1,4}, {1,2,4}, {5},
]
# clients c0,c1:{0}; c2:{1,2}; c3:{2,3}; c4:{0,1,4}; c5:{1,2,4}; c6,c7:{5}; c8,c9,c10:{3,4,5}
client_topics = [ {0}, {0}, {1,2}, {2,3}, {0,1,4}, {1,2,4}, {5}, {5}, {3,4,5}, {3,4,5}, {3,4,5} ]
def u(path, player):
    return sum((F(1, sum(path.count(t) for t in client_topics[c])) for c in range(len(client_topics)) if path[player] in client_topics[c]), F())
def prescribed(h):
    if len(h)==0:return 1
    if len(h)==1:return 1 if h[0]==5 else 5
    a,b=h
    s=tuple(sorted((a,b)))
    if s==(0,5):return 4
    if s==(2,5):return 4
    if s==(3,5):return 1
    if s==(4,5):return 2
    if s==(5,5):return 1
    return 5

def finish(h):
    h=tuple(h)
    while len(h)<3:h += (prescribed(h),)
    return h
checks=[]; strict=0; nonself=0
for depth in range(3):
  for h in product(range(6), repeat=depth):
    act=prescribed(h); term=finish(h+(act,)); val=u(term,depth)
    vals=[]
    for a in range(6):
      alt=finish(h+(a,)); v=u(alt,depth); vals.append(v)
      if a!=act: nonself += 1
      if val>v: strict += 1
      checks.append({'history':h,'player':depth,'action':a,'prescribed':act,'value':str(val),'deviation_value':str(v),'slack':str(val-v)})
    assert val==max(vals),(h,act,val,vals)
root=finish(())
loads=[sum(a in t for a in root) for t in client_topics]
W=sum(v>0 for v in loads)
# brute-force optimum among all ordered length-3 paths
opt=max(sum(v>0 for v in [sum(a in t for a in path) for t in client_topics]) for path in product(range(6),repeat=3))
H=lambda n:sum((F(1,j) for j in range(1,n+1)),F())
phi=sum(H(v) for v in loads)
psi=sum(min(H(v),F(2)) for v in loads)
assert root==(1,5,5)
assert [u(root,i) for i in range(3)]==[F(3),F(5,2),F(5,2)]
assert W==8 and opt==11 and phi==psi==F(21,2)
assert len(checks)==258 and nonself==215 and strict==188
report={'identity':'independent Fraction replay of harmonic 11-client certificate','topics':[sorted(t) for t in topics],'client_topics':[sorted(t) for t in client_topics],'root':root,'decision_histories':43,'comparisons_including_self':len(checks),'nonself':nonself,'strict':strict,'min_slack':str(min(F(x['slack']) for x in checks)),'actual_payoffs':[str(u(root,i)) for i in range(3)],'loads':loads,'W':W,'OPT':opt,'phi':str(phi),'psi':str(psi),'scope':'fixed published strategy; no claim of global minimality'}
print(json.dumps(report,indent=2))
