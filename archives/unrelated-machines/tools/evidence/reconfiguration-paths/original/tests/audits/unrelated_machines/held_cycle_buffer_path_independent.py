"""Independent constructive check of the pruned single-eligible path claim.

Given an actual target schedule; not an unknown-target algorithm.
"""
from fractions import Fraction as F
from collections import deque
import json


def construct(edges, fixed, C, T):
    C,T=F(C),F(T);fixed=list(map(F,fixed))
    edges=[(s,t,F(a),F(b)) for s,t,a,b in edges]
    m=len(fixed);assert m and 0<=T<=C<=2*T
    assert all(f>=0 for f in fixed)
    assert all(0<=s<m and 0<=t<m and s!=t and 0<=a<=T and 0<=b<=T for s,t,a,b in edges)
    A=[F(0)]*m;Q=[F(0)]*m
    for s,t,a,b in edges:A[s]+=a;Q[t]+=b
    S=[f+a for f,a in zip(fixed,A)]
    assert max(S)<=C and all(f+q<=T for f,q in zip(fixed,Q))
    U=max(2*T,C+T/2);h=[max(F(0),s+q-U) for s,q in zip(S,Q)]
    H={i for i in range(m) if h[i]>0}
    selected={}
    for i in sorted(H):
        candidates=[j for j,(s,t,a,b) in enumerate(edges) if s==i and a>=h[i]]
        if not candidates:return None
        selected[i]=candidates[0]
    complete=set();good=[];bad=[]
    for i in sorted(H):
        chain=[];position={};v=i
        while v in H and v not in complete and v not in position:
            position[v]=len(chain);chain.append(v);v=edges[selected[v]][1]
        if v in position:
            cycle=chain[position[v]:]
            anchors=[i for i in cycle if edges[selected[i]][3]<=U-S[edges[selected[i]][1]]]
            if anchors:good.append((cycle,anchors[0]))
            else:bad.append(cycle)
        complete.update(chain)
    Z={i for cycle in bad for i in cycle}
    order=[];safe=set(range(m))-H
    for cycle,anchor in good:
        pred={edges[selected[i]][1]:i for i in cycle}
        v=anchor
        for _ in cycle:
            order.append(selected[v]);safe.add(v);v=pred[v]
    # Bad-cycle vertices are protected receivers, not yet activated machines.
    roots=safe|Z;pending=H-roots
    predecessors={i:[] for i in range(m)}
    for s in pending:predecessors[edges[selected[s]][1]].append(s)
    queue=deque(sorted(roots))
    while queue:
        t=queue.popleft()
        for s in sorted(predecessors[t]):
            assert s in pending
            pending.remove(s);safe.add(s);order.append(selected[s]);queue.append(s)
    assert not pending
    selected_ids=set(selected.values())
    order.extend(j for j in range(len(edges)) if j not in selected_ids)
    phase2_end=len(order)
    # At phase 2 end, every Z source has lost its full selected-job complement.
    for i in Z:
        assert A[i]-edges[selected[i]][2]>=h[i]
    order.extend(selected[i] for i in sorted(Z))
    assert len(order)==len(edges) and len(set(order))==len(edges)
    load=S[:];peak=max(load);removed=[F(0)]*m
    for k,j in enumerate(order):
        s,t,a,b=edges[j];load[s]-=a;load[t]+=b;removed[s]+=a
        assert min(load)>=0 and max(load)<=U
        peak=max(peak,max(load))
        if k+1==phase2_end:assert all(removed[i]>=h[i] for i in H)
    assert load==[f+q for f,q in zip(fixed,Q)]
    return {'order':order,'peak':str(peak),'bad_vertices':sorted(Z)}


def audit():
    split=[(i,1-i,1,F(3,5)) for i in range(2)]
    for i in range(2):split.extend([(i,1-i,F(1,4),F(1,10))]*4)
    result=construct(split,[0,0],2,1)
    assert result['bad_vertices']==[0,1] and result['peak']=='12/5'
    # A bad cycle with selected trees feeding into it.
    tree=[(0,1,1,F(3,5)),(1,0,1,F(3,5))]
    for i in range(2):tree.extend([(i,1-i,F(1,4),F(1,20))]*4)
    tree.extend([(2,0,1,F(1,10)),(2,3,1,F(3,5)),(3,2,1,F(3,10)),(3,2,1,F(3,10))])
    assert construct(tree,[0]*4,2,1)['bad_vertices']==[0,1]
    assert construct([], [0],0,0)
    assert construct([(0,1,0,0)],[0,0],0,0)
    assert construct([], [1],1,1)
    return {'status':'passed','arithmetic':'fractions.Fraction','split_cycle':result,'tree_case':True,'degenerate_cases':3,'scope':'Named exact checks only; the independent constructor does not import the canonical implementation.'}

if __name__=='__main__':print(json.dumps(audit(),ensure_ascii=False,indent=2))
