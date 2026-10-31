"""One existing certificate: definition audit, never a new search."""
from fractions import Fraction as F
from itertools import product, permutations, combinations_with_replacement
from collections import defaultdict, deque
from pathlib import Path
import json, sys

HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
data=json.loads((BASE/'round2/global/pi_fixed_cone_counterexample.json').read_text())
raw=data['instance']; m=raw['players']; k=len(raw['topics'])
clients=[frozenset(c['topics']) for c in raw['customers'] for _ in range(c['multiplicity'])]
sigma={tuple(a['history']):a['action'] for a in data['strategy']['actions']}

def finish(h):
    z=list(h)
    while len(z)<m: z.append(sigma[tuple(z)])
    return tuple(z)

def profit(z,i,subset=None):
    return sum((F(1,sum(a in c for a in z)) for x,c in enumerate(clients)
                if z[i] in c and (subset is None or x in subset)),F())

actual=finish(()); u=[profit(actual,i) for i in range(m)]
checked=0
for d in range(m):
    for h in product(range(k),repeat=d):
        for a in range(k):
            assert profit(finish(h),d)>=profit(finish(h+(a,)),d)
            checked+=1
cover=lambda z:{x for x,c in enumerate(clients) if any(a in c for a in z)}
C=cover(actual)
opt=max(len(cover(z)) for z in combinations_with_replacement(range(k),m))
T=(1,2,4); O=cover(T); assert len(O)==opt
owner={x:next(i for i,a in enumerate(T) if a in clients[x]) for x in O}
J={x:{i for i,a in enumerate(actual) if a in clients[x]} for x in O}
R=O-C; I=O&C; G=C-O
unprotected={x for x in O if owner[x] not in J[x]}
Im=I&unprotected
menus={(i,a):finish(actual[:i]+(a,)) for i in range(m) for a in range(k)}
D={s:profit(z,s[0]) for s,z in menus.items()}

class Graph:
    def __init__(self,n): self.ad=[[] for _ in range(n)]; self.edges=[]
    def add(self,v,w,c,label):
        e=[v,w,c,c,label]; r=[w,v,0,0,None]
        e.append(r); r.append(e); self.ad[v].append(e); self.ad[w].append(r)
        self.edges.append(e); return e
    def send(self,path,amount):
        for e in path: e[2]-=amount; e[5][2]+=amount
    def maxflow(self,s,t):
        added=0
        while True:
            prev={s:None}; q=deque([s])
            while q and t not in prev:
                v=q.popleft()
                for e in self.ad[v]:
                    if e[2] and e[1] not in prev: prev[e[1]]=e; q.append(e[1])
            if t not in prev: return added
            path=[]; v=t
            while v!=s: e=prev[v]; path.append(e); v=e[0]
            a=min(e[2] for e in path); self.send(path,a); added+=a

def token(x,U):
    o=owner[x]; i=o; a=T[o]
    while True:
        z=menus[i,a]
        future=[j for j in range(i+1,m) if z[j] in clients[x] and U[j]>U[o]]
        if not future: return (i,a),u[i]/D[i,a]
        i=min(future); a=z[i]

def graph(U,kind):
    s=m; t=m+1; g=Graph(m+2); labels={}
    sources=[0]*m
    for x in G:
        j=max((j for j,a in enumerate(actual) if a in clients[x]),key=lambda j:U[j])
        sources[j]+=1
    for i,n in enumerate(sources): labels['src',i]=g.add(s,i,n,('src',i))
    order=sorted(O,key=lambda x:(x in R,x)) if '--prefer-I' in sys.argv else sorted(O)
    for x in order:
        o=owner[x]
        if x in R: labels['sink',x]=g.add(o,t,1,('sink',x)); continue
        j=max(J[x],key=lambda j:U[j])
        if kind=='B':
            if x not in unprotected: continue
            if U[o]>U[j]: labels['sink',x]=g.add(o,t,1,('sink',x)); continue
        if o!=j: labels['edge',x]=g.add(o,j,1,('edge',x))
    return g,labels,sources

absorb=defaultdict(int); credit=defaultdict(int); edge_count=defaultdict(int)
sink_count=defaultdict(int); src_count=[0]*m; reports=[]; cuts=0
for U in permutations(range(m)):
    ends={}; prices={}
    for x in unprotected:
        if J[x] and max(U[j] for j in J[x])>U[owner[x]]:
            j=max(J[x],key=lambda j:U[j]); credit[x,j]+=1
        else:
            s0,v=token(x,U); ends[x]=s0; prices[x]=v
            absorb[x,s0]+=1; assert v>=1
    B,lb,src=graph(U,'B'); A,la,_=graph(U,'A')
    for i in range(m): src_count[i]+=src[i]
    for tag,e in lb.items():
        if tag[0]=='sink': sink_count[tag[1]]+=1; assert tag[1] in ends
        if tag[0]=='edge': edge_count[tag[1],e[1]]+=1; assert U[e[1]]>U[e[0]]
    for gr in (B,A):
        for bits in product((0,1),repeat=m):
            subset={i for i,b in enumerate(bits) if b}
            demand=sum(src[i] for i in subset)
            cap=sum(e[3] for e in gr.edges if e[0] in subset and e[1] not in subset)
            assert cap>=demand; cuts+=1
    assert B.maxflow(m,m+1)==len(G)
    canceled_B={x:lb['sink',x][3]-lb['sink',x][2]
                for x in unprotected if ('sink',x) in lb}
    flow={id(e):e[3]-e[2] for e in B.edges}
    outgoing=defaultdict(list)
    for e in B.edges: outgoing[e[0]].append(e)
    for _ in range(len(G)):
        prev={m:None}; q=deque([m])
        while q and m+1 not in prev:
            v=q.popleft()
            for e in outgoing[v]:
                if flow[id(e)] and e[1] not in prev: prev[e[1]]=e; q.append(e[1])
        assert m+1 in prev
        path=[]; v=m+1
        while v!=m: e=prev[v]; path.append(e); v=e[0]
        last=path[0][4][1]
        for e in path: flow[id(e)]-=1
        if last in R: A.send([la[e[4]] for e in path],1)
    before=sum(la['sink',x][3]-la['sink',x][2] for x in R)
    assert A.maxflow(m,m+1)==len(G)-before
    canceled_A={x:la['sink',x][3]-la['sink',x][2] for x in R}
    assert all(canceled_A[x]>=canceled_B.get(x,0) for x in R)
    joint=sum((prices[x]*(1-canceled_B.get(x,0)) for x in ends),F())
    onlyR=sum((prices[x]*(1-canceled_A[x]) for x in R),F())
    numI=len(ends.keys()&Im)
    assert onlyR<=joint-numI
    reports.append({'rank':U,'query_I':numI,'canceled_I':sum(canceled_B.get(x,0) for x in Im),
                    'joint_cost':str(joint),'R_only_cost':str(onlyR),
                    'projection_margin':str(joint-numI-onlyR)})

n=len(reports); marginal_checks=0
for i in range(m): assert F(src_count[i],n)==profit(actual,i,G)
for x in unprotected:
    c0=len(J[x]); beta=F(1,c0+1)
    assert F(sink_count[x],n)==beta
    for j in J[x]:
        assert F(edge_count[x,j],n)==beta
        assert F(credit[x,j],n)==beta
    total=sum(F(v,n) for (y,s),v in absorb.items() if y==x)
    assert total==beta
    for s,z in menus.items():
        if s[1] not in clients[x]: continue
        c=sum(a in clients[x] for a in z)
        bound=F(1,c) if s[0]==owner[x] else (
            F(1,c*(c+1)) if s[0]>owner[x] else F(0))
        assert F(absorb[x,s],n)<=bound; marginal_checks+=1

out={'scope':'one old certificate; exact definition regression, not general evidence',
     'unit_customers':len(clients),'ordered_histories':len(sigma),'IC_comparisons':checked,
     'actual':actual,'actual_u':list(map(str,u)),'W':len(C),'OPT':opt,
     'R':len(R),'I':len(I),'G':len(G),'I_unprotected':len(Im),
     'priority_worlds':n,'all_cut_checks':cuts,'marginal_state_checks':marginal_checks,
     'worlds':reports}
if '--prefer-I' in sys.argv:
    assert any(z['canceled_I']>0 for z in reports)
target=HERE/('joint_rank_audit_prefer_I.json' if '--prefer-I' in sys.argv else 'joint_rank_audit.json')
if target.exists(): raise FileExistsError(target)
target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({key:value for key,value in out.items() if key!='worlds'},ensure_ascii=False))
