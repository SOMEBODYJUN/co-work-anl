"""Independent definition regression on an already frozen complete-SPE certificate.

No search, no new fixed-size theorem, and no imports of author/solver programs.
Reads the repository only; writes its report alongside this script.
"""
from collections import defaultdict, deque
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

REPO = next(p for p in Path(__file__).resolve().parents if (p / 'customer_attraction' / '__init__.py').is_file())
HERE = Path(__file__).resolve().parent
name = 'portfolio_matching_failure'
inst = json.loads((REPO / 'examples/customer_attraction' / (name+'.json')).read_text())
raw = json.loads((REPO / 'evidence/certificates/customer_attraction' / (name+'.json')).read_text())
policy = {tuple(row['history']): row['action'] for row in raw.get('strategy',raw)['actions']}
X = [frozenset(row['topics']) for row in inst['customers'] for _ in range(row['multiplicity'])]
m, nacts = inst['players'], len(inst['topics'])
def finish(prefix):
    prefix = tuple(prefix)
    while len(prefix)<m:
        prefix += (policy[prefix],)
    return prefix
def pay(z,i):
    return sum((F(1,sum(a in likes for a in z)) for likes in X if z[i] in likes),F())
def cover(z):
    return {x for x,likes in enumerate(X) if any(a in likes for a in z)}
ic_checks = 0
for depth in range(m):
    for h in product(range(nacts),repeat=depth):
        for a in range(nacts):
            assert pay(finish(h),depth)>=pay(finish(h+(a,)),depth)
            ic_checks += 1
actual = finish(())
u = [pay(actual,i) for i in range(m)]
C = cover(actual)
T = (1,3)
O = cover(T)
assert len(O) == max(len(cover(z)) for z in product(range(nacts),repeat=m))
R,I,G = O-C,O&C,C-O
owner = {x:next(i for i,a in enumerate(T) if a in X[x]) for x in O}
g = [sum((F(1,sum(a in X[x] for a in actual)) for x in G if actual[i] in X[x]),F()) for i in range(m)]
menu = {(i,a):finish(actual[:i]+(a,)) for i in range(m) for a in range(nacts)}
D = {(i,a):pay(z,i) for (i,a),z in menu.items()}

def capture(rho):
    arrivals = defaultdict(F)
    for x in R:
        arrivals[owner[x],T[owner[x]],x] += rho[x]
    A,Asrc,Ain = defaultdict(F),defaultdict(F),defaultdict(F)
    absorbed = defaultdict(F)
    for i in range(m):
        for a in range(nacts):
            z = menu[i,a]
            for x in R:
                mass = arrivals[i,a,x]
                if not mass:
                    continue
                assert a in X[x]
                Fset = [j for j in range(i+1,m) if z[j] in X[x]]
                piece = mass/F(1+len(Fset))
                A[i,a] += piece
                (Asrc if i==owner[x] else Ain)[i,a] += piece
                absorbed[x] += piece
                for j in Fset:
                    arrivals[j,z[j],x] += piece
    for x in R:
        assert absorbed[x] == rho[x]
        for i in range(owner[x]+1,m):
            assert sum((arrivals[i,a,x] for a in range(nacts)),F())<=rho[x]/2
    def costs(Apart):
        return [sum((u[i]*Apart[i,a]/D[i,a] for a in range(nacts) if D[i,a]),F()) for i in range(m)]
    K,Ksrc,Kin = costs(A),costs(Asrc),costs(Ain)
    assert all(K[i]==Ksrc[i]+Kin[i] for i in range(m))
    assert sum(A.values(),F())==sum(rho.values(),F())
    slack = sum((A[i,a]*(u[i]-D[i,a])/D[i,a] for i,a in A if D[i,a]),F())
    assert sum(K,F())==sum(rho.values(),F())+slack
    return K,Ksrc,Kin,slack

unit_v = {}
for x in R:
    unit_v[x] = sum(capture({y:F(y==x) for y in R})[0],F())
assert all(v>=1 for v in unit_v.values())
fullK,fullsrc,fullin,fullslack=capture({x:F(1) for x in R})

# Pre-send the simultaneously allowed local delta, highest fixed-flow price first.
delta = {x:F() for x in R}
for i in range(m):
    own = sorted((x for x in R if owner[x]==i),key=lambda x:(-unit_v[x],x))
    left = min(g[i],F(len(own)))
    for x in own:
        delta[x] = min(left,F(1))
        left -= delta[x]
    assert left==0

# Independently construct the residual Hall-A graph and send all residual sources.
caps = defaultdict(F)
S,Z = 'source','sink'
def add(a,b,c):
    caps[a,b] += c
for i in range(m):
    add(S,('r',i),g[i]-sum((delta[x] for x in R if owner[x]==i),F()))
for x in I:
    covering = [i for i,a in enumerate(actual) if a in X[x]]
    for i in covering:
        if i!=owner[x]:
            add(('r',owner[x]),('r',i),F(1,len(covering)))
for x in R:
    add(('r',owner[x]),('x',x),1-delta[x])
    add(('x',x),Z,1-delta[x])
vertices = {node for edge in caps for node in edge}
res = dict(caps)
for a,b in tuple(res):
    res.setdefault((b,a),F())
flow_value = F()
while True:
    parent={S:None};queue=deque([S])
    while queue and Z not in parent:
        a=queue.popleft()
        for b in vertices:
            if b not in parent and res.get((a,b),F())>0:
                parent[b]=a;queue.append(b)
    if Z not in parent:
        break
    path=[];v=Z
    while parent[v] is not None:
        a=parent[v];path.append((a,v));v=a
    amount=min(res[e] for e in path)
    for a,b in path:
        res[a,b]-=amount;res[b,a]+=amount
    flow_value+=amount
assert flow_value==sum(g,F())-sum(delta.values(),F())
gamma={x:delta[x]+caps[('x',x),Z]-res[('x',x),Z] for x in R}
assert all(0<=gamma[x]<=1 and gamma[x]>=delta[x] for x in R)
assert sum(gamma.values(),F())==len(G)
gamma_role=[sum((gamma[x] for x in R if owner[x]==i),F()) for i in range(m)]
eta=[u[i]-g[i]+gamma_role[i] for i in range(m)]
rho={x:1-gamma[x] for x in R}
K,Ksrc,Kin,slack=capture(rho)
assert sum(eta,F())==len(C)
assert all(0<=Ksrc[i]<=eta[i] for i in range(m))
assert Kin[0]==0
assert sum(K,F())==sum((rho[x]*unit_v[x] for x in R),F())

# Free-query Bellman, independently compared with exhaustive deterministic policies.
kappa={}
bell_checks=0
for x in R:
    V={}
    actions=[a for a in range(nacts) if a in X[x]]
    for i in reversed(range(m)):
        vals=[]
        for a in actions:
            followers=[j for j in range(i+1,m) if menu[i,a][j] in X[x]]
            vals.append((u[i]/D[i,a]+sum((V[j] for j in followers),F()))/F(1+len(followers)))
        V[i]=min(vals)
    kappa[x]=min(V.values())
    for start in range(m):
        best=None
        for queries in product(actions,repeat=m-start):
            incoming=defaultdict(F);incoming[start]=F(1);price=F();absorb=F()
            for i in range(start,m):
                a=queries[i-start]
                followers=[j for j in range(i+1,m) if menu[i,a][j] in X[x]]
                part=incoming[i]/F(1+len(followers))
                price+=part*u[i]/D[i,a];absorb+=part
                for j in followers:incoming[j]+=part
            assert absorb==1
            best=price if best is None else min(best,price)
        assert best==V[start]
        bell_checks+=1
    assert 1<=kappa[x]<=unit_v[x]

def strlist(xs):return list(map(str,xs))
report={'scope':'formula regression on one existing complete SPE, not a universal proof',
        'source':name,'full_history_IC_checks':ic_checks,'actual':list(actual),'optimum':list(T),
        'W':len(C),'OPT':len(O),'R':len(R),'I':len(I),'G':len(G),
        'u':strlist(u),'g':strlist(g),'gamma_by_role':strlist(gamma_role),'eta':strlist(eta),
        'source_cost':strlist(Ksrc),'incoming_cost':strlist(Kin),'residual_by_role':strlist([eta[i]-Ksrc[i] for i in range(m)]),
        'total_cost':str(sum(K,F())),'absorbed':str(sum(rho.values(),F())),
        'paid_original_IC_slack':str(slack),'fixed_flow_unit_prices':sorted(set(map(str,unit_v.values()))),
        'uncancelled_flow':{'cost':str(sum(fullK,F())),'source_cost':strlist(fullsrc),
                            'incoming_cost':strlist(fullin),'paid_slack':str(fullslack)},
        'free_query_unit_prices':sorted(set(map(str,kappa.values()))),'bellman_exhaustive_checks':bell_checks,
        'claim':'PASS; no new range, no no-counterexample inference'}
(HERE/'incoming_payment_regression.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
