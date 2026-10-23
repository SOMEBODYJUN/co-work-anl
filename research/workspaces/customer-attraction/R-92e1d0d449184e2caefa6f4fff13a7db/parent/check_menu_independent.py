"""Independent rational zero-sum LP vertex enumeration for the 10-customer menu."""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
import json

TYPES={3:2,4:3,8:2,9:3}
MENU={0:(0,0,3),1:(1,0,3),2:(2,2,0),3:(3,3,0)}

def pay(a,z):
    return sum((F(w,sum(bool(mask>>j&1) for j in z)) for mask,w in TYPES.items() if mask>>a&1),F(0))

def value_query(a, fixed, competitors):
    return sum((F(w,1+sum(bool(mask>>j&1) for j in fixed+competitors)) for mask,w in TYPES.items() if mask>>a&1),F(0))

def solve(A,b):
    a=[list(map(F,row))+[F(y)] for row,y in zip(A,b)]
    n=len(b)
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]),None)
        if k is None:return None
        a[j],a[k]=a[k],a[j]
        d=a[j][j];a[j]=[v/d for v in a[j]]
        for i in range(n):
            if i!=j:
                d=a[i][j]
                a[i]=[x-d*y for x,y in zip(a[i],a[j])]
    return [row[-1] for row in a]

def minimax(fixed,slots):
    backgrounds=list(combinations_with_replacement(range(4),slots))
    cols=[[value_query(a,tuple(fixed),q) for a in range(4)] for q in backgrounds]
    # variables p0,p1,p2,p3,v. Constraints p>=0 and every col.p-v>=0.
    constraints=[[F(i==j) for i in range(4)]+[F(0)] for j in range(4)]
    constraints += [c+[F(-1)] for c in cols]
    best=None
    for active in combinations(range(len(constraints)),4):
        rows=[[F(1)]*4+[F(0)]]+[constraints[j] for j in active]
        x=solve(rows,[1,0,0,0,0])
        if x is None:continue
        if any(sum(a*y for a,y in zip(row,x))<0 for row in constraints):continue
        if best is None or x[-1]>best[-1]:best=x
    assert best is not None
    return best[-1],best[:4],backgrounds,cols

v,p,qs,cols=minimax((),2)
assert v==F(12,5)
P=[F(3,10),F(0),F(2,5),F(3,10)]
assert min(sum(p*x for p,x in zip(P,c)) for c in cols)==v
Q={(0,3):F(3,5),(0,2):F(1,5),(2,3):F(1,5)}
assert sum(Q.values())==1
assert max(sum(w*value_query(a,(),q) for q,w in Q.items()) for a in range(4))==v
roots=[pay(a,z) for a,z in MENU.items()]
assert roots==[F(2),F(1),F(3,2),F(2)]
branches=[]
for a,z in MENU.items():
    v2,p2,_,_=minimax((a,),1)
    tail=sum(pay(j,z) for j in z[1:])
    assert tail>=2*v2
    last=z[-1]
    last_actions=[pay(j,z[:-1]+(j,)) for j in range(4)]
    assert pay(last,z)==max(last_actions)
    branches.append({'root':a,'z':z,'root_payoff':str(pay(a,z)),'tail_sum':str(tail),'v2_fixed_root':str(v2),'last_best_payoffs':[str(x) for x in last_actions]})
W=sum(w for mask,w in TYPES.items() if any(mask>>a&1 for a in MENU[0]))
OPT=max(sum(w for mask,w in TYPES.items() if any(mask>>a&1 for a in z)) for z in product(range(4),repeat=3))
assert W==7 and OPT==10 and 3*v-W==F(1,5)
# Root menu cannot be a full SPE: after root0, prescribed player2 action0 earns2.
# Deviating player2 to2 leaves unique player3 best response3.
lasts=[pay(j,(0,2,j)) for j in range(4)]
assert lasts.index(max(lasts))==3 and lasts.count(max(lasts))==1
assert pay(2,(0,2,3))==3>pay(0,MENU[0])==2
print(json.dumps({'status':'passed','types':TYPES,'v3':str(v),'root_query':[str(x) for x in P],'root_payoffs':[str(x) for x in roots],'W':W,'OPT':OPT,'three_v_minus_W':str(3*v-W),'branches':branches,'fatal_SPE_objection':{'history':[0],'prescribed_action':0,'prescribed_payoff':'2','deviation_action':2,'unique_last_BR':3,'deviation_payoff':'3'}},ensure_ascii=False,indent=2))
