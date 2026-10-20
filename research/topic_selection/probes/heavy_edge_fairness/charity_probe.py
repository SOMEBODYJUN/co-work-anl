"""Exact independent tests of 3^k min-charity extension on simple graphs."""
from itertools import product
from collections import deque
from pathlib import Path
import random,json

def ef(n,edges,dec):
    rev=[0]*n;visible=[[0]*n for _ in range(n)]
    for (i,j,a,b),d in zip(edges,dec):
        if d==0:continue
        to=i if d==1 else j
        rev[to]+=a if to==i else b
        visible[i][to]+=a;visible[j][to]+=b
    return all(rev[i]>=visible[i][j] for i in range(n) for j in range(n) if i!=j)

def brute(n,edges):
    best=len(edges)+1;witness=None
    for d in product(range(3),repeat=len(edges)):
        cost=d.count(0)
        if cost<best and ef(n,edges,d):best=cost;witness=d
    return best,witness

class Flow:
    def __init__(self,n):self.a=[[] for _ in range(n)]
    def add(self,i,j,c):
        f=[j,c,None];r=[i,0,f];f[2]=r;self.a[i].append(f);self.a[j].append(r);return f
    def run(self,s,t):
        total=0
        while True:
            prev={s:None};q=deque([s])
            while q and t not in prev:
                i=q.popleft()
                for e in self.a[i]:
                    if e[1] and e[0] not in prev:prev[e[0]]=(i,e);q.append(e[0])
            if t not in prev:return total
            at=t
            while at!=s:
                i,e=prev[at];e[1]-=1;e[2][1]+=1;at=i
            total+=1

def algorithm(n,edges):
    heavy=[z for z,e in enumerate(edges) if max(e[2:])>=2 and min(e[2:])>0]
    light=[z for z,e in enumerate(edges) if e[2:]==(1,1)]
    forced={z:(1 if e[2]>0 else 2) for z,e in enumerate(edges) if min(e[2:])==0}
    adj=[[] for _ in range(n)]
    for z in light:
        i,j,*_=edges[z];adj[i].append((j,z));adj[j].append((i,z))
    components=[];seen=set()
    for r in range(n):
        if r in seen:continue
        C=[];Q=[r];Z=set();seen.add(r)
        while Q:
            i=Q.pop();C.append(i)
            for j,z in adj[i]:
                Z.add(z)
                if j not in seen:seen.add(j);Q.append(j)
        components.append((C,Z))
    best=len(edges)+1;witness=None
    for ds in product(range(3),repeat=len(heavy)):
        dec=dict(forced);dec.update(zip(heavy,ds));s=[0]*n;q=[0]*n
        for z,d in dec.items():
            if not d:continue
            i,j,a,b=edges[z]
            if d==1:s[i]+=a;q[j]=max(q[j],b)
            else:s[j]+=b;q[i]=max(q[i],a)
        keep=set(light);deleted=set()
        for C,Z in components:
            if not any(s[i] or q[i] for i in C) and len(Z)==len(C)-1:
                keep-=Z;deleted|=Z
        b=[max(0,max(q[i],int(any(z in keep for _,z in adj[i])))-s[i]) for i in range(n)]
        S=n+len(edges);T=S+1;F=Flow(T+1);arcs={}
        for i in range(n):F.add(S,i,b[i])
        for z in keep:
            i,j,*_=edges[z];arcs[z,i]=F.add(i,n+z,1);arcs[z,j]=F.add(j,n+z,1);F.add(n+z,T,1)
        if F.run(S,T)!=sum(b):continue
        for z in keep:
            i,j,*_=edges[z]
            dec[z]=1 if arcs[z,i][1]==0 else 2 if arcs[z,j][1]==0 else 1
        for z in deleted:dec[z]=0
        d=tuple(dec[z] for z in range(len(edges)))
        assert ef(n,edges,d)
        cost=d.count(0)
        if cost<best:best=cost;witness=d
    return best,witness

def main():
    rng=random.Random(37042027);cases=0
    for n in range(1,7):
        for _ in range(200):
            pairs=[(i,j) for i in range(n) for j in range(i+1,n)];rng.shuffle(pairs)
            pairs=pairs[:rng.randrange(min(8,len(pairs))+1)]
            edges=[(i,j,*rng.choice([(0,0),(0,1),(1,0),(1,1),(1,1),(1,1),(1,2),(2,1),(2,2),(2,3)])) for i,j in pairs]
            a=algorithm(n,edges);b=brute(n,edges);cases+=1
            if a[0]!=b[0]:raise AssertionError((n,edges,a,b))
    out={'seed':37042027,'cases':cases,'n':'1..6','maximum_edges':8,'edge_values':[0,1,2,3],'exact_arithmetic':True,'mismatches':0,'scope':'simple graphs; each edge independently kept to endpoint or donated'}
    Path(__file__).with_name('charity_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
