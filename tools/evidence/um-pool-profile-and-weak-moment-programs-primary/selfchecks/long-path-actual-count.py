from collections import deque
from fractions import Fraction
import json

def height(k):
    h=1;a=Fraction(1,k-1)
    while a<Fraction(1,2):h+=1;a*=Fraction(k,k-1)
    return h

def graph(k,ell):
    h=height(k);adj=[]
    def vertex():adj.append(set());return len(adj)-1
    def edge(a,b):assert a!=b and b not in adj[a];adj[a].add(b);adj[b].add(a)
    roots=[]
    for side in range(2):
        root=vertex();roots.append(root);layer=[root]
        for depth in range(h-1):
            nxt=[]
            for v in layer:
                for j in range(k):w=vertex();edge(v,w);nxt.append(w)
            layer=nxt
        for v in layer:
            terminal=vertex()
            for j in range(k):
                last=v
                for x in range(ell-1):w=vertex();edge(last,w);last=w
                edge(last,terminal)
    edge(*roots)
    return adj

def girth(adj):
    answer=len(adj)+1
    for root in range(len(adj)):
        dist={root:0};parent={root:None};queue=deque([root])
        while queue:
            v=queue.popleft()
            for w in adj[v]:
                if w not in dist:dist[w]=dist[v]+1;parent[w]=v;queue.append(w)
                elif parent[v]!=w:answer=min(answer,dist[v]+dist[w]+1)
    return answer

k=4;ell=2;h=height(k);I=(k**h-1)//(k-1);L=k**(h-1)
a=graph(k,ell);M=len(a);N=sum(map(len,a))//2
seen={0};queue=deque([0])
while queue:
    for w in a[queue.popleft()]:
        if w not in seen:seen.add(w);queue.append(w)
assert len(seen)==M
assert M==2*(I+L+k**h*(ell-1))==202
assert N==1+2*(I-1+k**h*ell)==297
assert girth(a)==2*ell==4
old_M=2*(I+k**h*ell)
assert old_M==298 and old_M-M==2*(k-1)*L==96
assert N-M+1==96 and N==old_M-1
print(json.dumps({'status':'passed','k':k,'h':h,'ell':ell,'nonterminal_per_tree':I,'shared_terminal_per_tree':L,'actual_machines':M,'actual_jobs':N,'connected':True,'actual_girth':girth(a),'cycle_rank':N-M+1,'historical_reported_machine_formula':old_M,'overcount':old_M-M,'scope':'one independent explicit unpadded graph; general formulas follow by counting, not this finite run'},indent=2))
