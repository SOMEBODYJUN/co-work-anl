"""Exact affine classification of the entire positive (a,b) family."""
from fractions import Fraction as F
from itertools import combinations_with_replacement,product
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
T=[sum(1<<((i+j)%8) for j in range(3)) for i in range(8)]
P=[(1<<i)|(1<<(i+4)) for i in range(4)]

def coef(label,z):
    def part(blocks):
        return sum((F(1,sum(mask>>q&1 for q in z)) for mask in blocks if mask>>label&1),F(0))
    return (part(T),part(P))

def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def at(x,ratio):return x[0]+x[1]*ratio

def nonnegative(x,region,strict=False):
    if region=='eq':return at(x,F(1))>0 if strict else at(x,F(1))>=0
    if region=='lt':edges=(x[0],at(x,F(1)))
    else:edges=(at(x,F(1)),x[1])
    return min(edges)>=0 and (not strict or max(edges)>0)

BRsmall={0:[3,5],1:[4,5],2:[5],3:[5,6],4:[1,2,3,5,6,7],5:[2,3],6:[3],7:[3,4]}
BRlarge={**BRsmall,1:[3,6],7:[2,5]}
BReq={**BRsmall,1:[3,4,5,6],7:[2,3,4,5]}
root={(j,c):coef(0,(0,j,c)) for j,c in product(range(8),repeat=2)}
second={(j,c):coef(j,(0,j,c)) for j,c in product(range(8),repeat=2)}
last={(j,c):coef(c,(0,j,c)) for j,c in product(range(8),repeat=2)}
L=(F(5,2),F(1));D=(F(2),F(1,2));V=(F(23,16),F(5,8))
base_feasible={(2,5),(6,3),(3,5),(5,3),(3,6),(5,2)}
classification=[]
for region,BR in [('lt',BRsmall),('eq',BReq),('gt',BRlarge)]:
    min_choices=([3,5,5,5,3,3,3,3] if region!='gt' else [3,3,5,5,3,3,3,5])
    for j in range(8):
        expected=BR[j];envelope=last[j,expected[0]]
        for c in range(8):
            diff=sub(envelope,last[j,c])
            if c in expected:
                assert (at(diff,F(1))==0 if region=='eq' else diff==(0,0))
            else:assert nonnegative(diff,region,strict=True),(region,j,c,diff)
        low=second[j,min_choices[j]]
        assert min_choices[j] in expected
        assert all(nonnegative(sub(second[j,c],low),region) for c in expected)
        assert nonnegative(sub(L,low),region)
        if j==2:assert low==L
    feasible=set()
    for j in range(8):
        for c in BR[j]:
            diff=sub(second[j,c],L)
            if nonnegative(diff,region):feasible.add((j,c))
            else:assert nonnegative(tuple(-x for x in diff),region,strict=True),(region,j,c,diff)
    expected=base_feasible|({(4,1),(4,7)} if region!='gt' else set())
    assert feasible==expected,(region,feasible,expected)
    minimum=D if region!='gt' else L
    for pair in feasible:assert nonnegative(sub(root[pair],minimum),region)
    attained=(4,1) if region!='gt' else (2,5)
    assert root[attained]==minimum
    assert nonnegative(sub(minimum,V),region,strict=True)
    classification.append(dict(region=region,BR=BR,feasible=sorted(feasible),root_min_coeff=list(map(str,minimum)),security_coeff=list(map(str,V))))

def audit_instance(a,b):
    def evaluate(cf):return cf[0]*a+cf[1]*b
    def pay(label,z):return evaluate(coef(label,z))
    def welfare(z):return sum(a for mask in T if any(mask>>q&1 for q in z))+sum(b for mask in P if any(mask>>q&1 for q in z))
    small=b<=a
    choice=4 if small else 2
    replies=[3,5,5,5,1,3,3,3] if small else [3,3,5,5,3,3,3,5]
    def action(h):
        if not h:return 0
        if len(h)==1:return (h[0]+choice)%8
        return (h[0]+replies[(h[1]-h[0])%8])%8
    def finish(h):
        h=tuple(h)
        while len(h)<3:h=(*h,action(h))
        return h
    count=0
    for depth in range(3):
        for h in product(range(8),repeat=depth):
            z=finish(h);u=pay(z[depth],z)
            for alt in range(8):
                zz=finish((*h,alt));assert u>=pay(alt,zz),(a,b,h,alt,z,zz)
                count+=1
    z=finish(());minroot=evaluate(D if small else L)
    assert pay(z[0],z)==minroot
    child=[]
    value=max(min(evaluate(second[j,c]) for c in range(8) if evaluate(last[j,c])==max(evaluate(last[j,d]) for d in range(8))) for j in range(8))
    assert value==evaluate(L)
    for j,c in product(range(8),repeat=2):
        if evaluate(last[j,c])==max(evaluate(last[j,d]) for d in range(8)) and evaluate(second[j,c])>=value:child.append((j,c))
    assert min(evaluate(root[pair]) for pair in child)==minroot
    v=evaluate(V)
    profiles=list(combinations_with_replacement(range(8),3))
    def query(label,q):return pay(label,(*q,label))
    assert min(sum((query(label,q) for label in range(8)),F(0))/8 for q in profiles)==v
    assert minroot>v
    assert min(welfare((0,j,c)) for j,c in child)==(2*b+7*a if small else 3*b+8*a)
    return dict(a=a,b=b,nodes=73,comparisons=count,terminal=z,root_min=str(minroot),v4=str(v),gap=str(minroot-v),second_floor=str(value),child_outcomes=child,min_SPE_welfare=2*b+7*a if small else 3*b+8*a,OPT3=3*b+8*a,status='Full SPE verified at all ordered histories; affine proof covers all positive parameters')

out=dict(affine_regions=classification,instances=[audit_instance(a,b) for a,b in [(2,1),(1,1),(1,2),(1,5),(4,50),(1,100)]])
(HERE/'cyclic_family_complete_spe_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['instances'],indent=2))
