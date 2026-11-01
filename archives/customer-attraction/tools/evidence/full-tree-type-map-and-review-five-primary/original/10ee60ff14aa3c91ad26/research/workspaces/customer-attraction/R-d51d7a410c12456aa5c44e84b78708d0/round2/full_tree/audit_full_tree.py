#!/usr/bin/env python3
"""Definition-level exact audit of the type-map kernel and mapped circulation.
No solver or numerical LP is used. The fixed policy JSON is input only.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from math import comb
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def rank(rows):
    if not rows:return 0
    a=[list(map(Q,r)) for r in rows]; i=0
    for j in range(len(a[0])):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i]
        s=a[i][j];a[i]=[x/s for x in a[i]]
        for k in range(i+1,len(a)):
            if a[k][j]:
                s=a[k][j];a[k]=[x-s*y for x,y in zip(a[k],a[i])]
        i+=1
        if i==len(a):break
    return i

def comps(n,p):
    if p==1:yield (n,);return
    for a in range(n+1):
        for b in comps(n-a,p-1):yield (a,)+b

def payoff(q,a):
    return tuple(Q(1,sum(q[j] for j in range(len(q)) if b>>j&1))
                 if b>>a&1 else Q(0) for b in range(1,1<<len(q)))

def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def dot(x,y):return sum(a*b for a,b in zip(x,y))

def scc(edges):
    vertices=set(x for e in edges for x in e)
    adj={x:set() for x in vertices}
    for u,v in edges:adj[u].add(v)
    def reach(x):
        found={x}; todo=[x]
        while todo:
            for y in adj[todo.pop()]:
                if y not in found:found.add(y);todo.append(y)
        return found
    reaches={x:reach(x) for x in vertices}
    remaining=set(vertices);out=[]
    while remaining:
        x=min(remaining);c=tuple(sorted(y for y in reaches[x] if x in reaches[y]))
        out.append(c);remaining.difference_update(c)
    return out

def audit_example():
    data=json.loads((HERE/'extra_lineality_exact.json').read_text())
    n,p=data['players'],data['topics'];weights=tuple(data['weights'])
    histories=[h for k in range(n) for h in product(range(p),repeat=k)]
    sigma=dict(zip(histories,data['policy']))
    assert len(sigma)==len(data['policy'])==40
    def terminal(h):
        while len(h)<n:h=h+(sigma[h],)
        return h
    def vertex(h,a):
        z=terminal(h+(a,));return tuple(z.count(j) for j in range(p)),a
    rows={};endpoints={}
    for h in histories:
        for a in range(p):
            u,v=vertex(h,a),vertex(h,sigma[h])
            rows[h,a]=sub(payoff(*v),payoff(*u));endpoints[h,a]=u,v
    slacks={key:dot(row,weights) for key,row in rows.items()}
    assert len(rows)==120 and min(slacks.values())==0
    assert all(x>=0 for x in slacks.values())
    components=scc(endpoints.values());ci={v:k for k,c in enumerate(components) for v in c}
    internal=[row for key,row in rows.items() if ci[endpoints[key][0]]==ci[endpoints[key][1]]]
    scc_rank=rank(internal)
    r,s,t=rows[(0,0),2],rows[(1,0),1],rows[(0,0,0),1]
    assert r==tuple(map(Q,(0,1,Q(1,3),-1,-Q(1,3),0,0)))
    assert s==tuple(map(Q,(0,-Q(1,2),-Q(1,3),Q(1,2),Q(1,3),0,0)))
    assert t==tuple(map(Q,(0,-1,-Q(1,4),1,Q(1,4),0,0)))
    assert all(a+Q(2,5)*b+Q(4,5)*c==0 for a,b,c in zip(r,s,t))
    assert rank([s,r])==2 and scc_rank==1 and rank(internal+[r])==2
    # s and -s are genuine graph reverse edges, not just mapped reverse edges.
    assert endpoints[((1,0),1)]==tuple(reversed(endpoints[((0,1,2),2)]))
    assert rows[((0,1,2),2)]==tuple(-x for x in s)
    # Since weights expose a nonnegative face, every lineality vector is
    # spanned by zero-slack rows; these have rank exactly two.
    zero_rows=[row for key,row in rows.items() if not slacks[key]]
    assert rank(zero_rows)==2
    assert ci[endpoints[((0,0),2)][0]]!=ci[endpoints[((0,0),2)][1]]
    path=terminal(());q=tuple(path.count(j) for j in range(p))
    welfare=sum(w for b,w in enumerate(weights,1) if any(q[j] and b>>j&1 for j in range(p)))
    utilities=[dot(payoff(q,a),weights) for a in path]
    assert path==(1,0,2,2) and q==(1,1,2)
    assert welfare==sum(weights)==24==sum(utilities)
    assert all(w>0 for w in weights)
    assert all(any(weights[b-1] and bool(b>>a&1)!=bool(b>>c&1) for b in range(1,1<<p))
               for a,c in combinations(range(p),2))
    return {'histories':len(histories),'comparisons':len(rows),
            'minimum_slack':str(min(slacks.values())), 'path':path,
            'payoffs':list(map(str,utilities)), 'welfare':welfare, 'optimum':24,
            'scc_image_rank':scc_rank,'mapped_lineality_rank':2,
            'zero_slack_row_rank':rank(zero_rows),
            'nontrivial_sccs':[[[list(q),a] for q,a in c] for c in components if len(c)>1],
            'reverse_relation':{'r':list(map(str,r)),'s':list(map(str,s)),'t':list(map(str,t)),
                                'identity':'r+(2/5)s+(4/5)t=0'}}

def audit_ranks():
    records=[]
    for n,p in [(1,1),(1,5),(2,1),(7,1),(2,2),(3,2),(2,4),(3,4),(5,3),(3,5),(5,5)]:
        verts=[(q,a) for q in comps(n,p) for a in range(p) if q[a]]
        fs=[payoff(*v) for v in verts]
        expected=sum(comb(p,k) for k in range(1,min(n,p)+1))
        assert len(verts)==p*comb(n+p-2,p-1)
        assert rank(fs)==expected
        assert rank([sub(f,fs[0]) for f in fs])==expected-1
        assert all(f[-1]==Q(1,n) for f in fs)
        records.append({'players':n,'topics':p,'vertices':len(verts),
                        'rank':expected,'difference_rank':expected-1})
    return records

if __name__=='__main__':
    report={'status':'exact_audit_passed','example':audit_example(),'rank_boundaries':audit_ranks()}
    (HERE/'full_tree_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
