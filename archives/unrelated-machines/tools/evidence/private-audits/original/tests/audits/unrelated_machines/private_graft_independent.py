"""Independent edge-subset oracle; no repository module imports."""
from fractions import Fraction as Q
from itertools import product
from random import Random
import json, hashlib

def optimum(g):
    k, edges = g
    n=len(k); best=Q(int(k[0]==0))
    # Enumerate all possible parent choices, then retain root-connected nodes.
    inc=[[-1] for _ in k]
    for u,v in edges: inc[v].append(u)
    for parents in product(*inc[1:]):
        p=(-1,)+parents; active={0}; d=[0]*n
        for v in range(1,n):
            if p[v] in active: active.add(v); d[p[v]]+=1
        score=min([Q(1)]+[Q(d[v],k[v]) for v in active if k[v]])
        best=max(best,score)
    return best

def topo(g):
    k,e=g; pending=set(range(len(k))); order=[]
    while pending:
        ready=sorted(v for v in pending if all(u not in pending for u,w in e if w==v))
        assert ready
        order.extend(ready); pending.difference_update(ready)
    assert order[0]==0
    remap={v:i for i,v in enumerate(order)}
    return tuple(k[v] for v in order),tuple((remap[u],remap[v]) for u,v in e)

def substitute(g,h):
    k=list(g[0]); e=list(g[1]); terminals=[v for v,x in enumerate(k) if x==0]
    for v in terminals:
        ids={0:v}
        for w in range(1,len(h[0])): ids[w]=len(k); k.append(h[0][w])
        k[v]=h[0][0]
        e.extend((ids[u],ids[w]) for u,w in h[1])
    return topo((k,e))

def gate(k,modules):
    ks=[k]; es=[]
    for h in modules:
        off=len(ks); ks.extend(h[0]); es.append((0,off))
        es.extend((u+off,v+off) for u,v in h[1])
    return tuple(ks),tuple(es)

def graphs(n):
    potential=[(u,v) for u in range(n) for v in range(u+1,n)]
    for mask in product([0,1],repeat=len(potential)):
        e=tuple(x for x,b in zip(potential,mask) if b)
        for k in product([0,1,2,7,2**60],repeat=n):
            if any(k[u]==0 for u,v in e): continue
            yield tuple(k),e

def run():
    rng=Random(20261017); base=list(graphs(1))+list(graphs(2))+list(graphs(3))
    vals={g:optimum(g) for g in base}; serial=0; gates=0
    # Exhaustive small pairs and deterministic wider sampled pairs.
    tiny=list(graphs(1))+list(graphs(2))
    for g,h in list(product(tiny,repeat=2))+[(rng.choice(base),rng.choice(base)) for _ in range(2000)]:
        out=substitute(g,h)
        assert optimum(out)==min(vals[g],vals[h]),(g,h,out)
        serial+=1
    for _ in range(2000):
        ms=[rng.choice(base) for _ in range(rng.randrange(4))]
        k=rng.choice([1,2,3,7,2**60]); beta=sorted([vals[h] for h in ms],reverse=True)
        expected=max([Q(0)]+[min(Q(1),Q(s,k),b) for s,b in enumerate(beta,1)])
        assert optimum(gate(k,ms))==expected,(k,ms,expected)
        gates+=1
    shared=((2,1,1,0),((0,1),(0,2),(1,3),(2,3)))
    private=gate(2,[((1,0),((0,1),))]*2)
    assert optimum(shared)==Q(1,2) and optimum(private)==1
    assert optimum(substitute(shared,shared))==Q(1,2)
    out={'oracle':'parent-choice exhaustive; exact Fraction; no repository imports',
         'base_graphs':len(base),'terminal_substitution_cases':serial,'private_gate_cases':gates,
         'demand_set':[0,1,2,7,2**60],'seed':20261017,
         'shared_leaf_counterexample':'private modules each 1, merged single leaf gives 1/2',
         'self_composition_half':'1/2, not 1/4','all_passed':True,
         'script_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    print(json.dumps(out,indent=2))

if __name__=='__main__': run()
