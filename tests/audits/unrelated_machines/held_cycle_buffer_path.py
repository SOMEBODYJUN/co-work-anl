"""Given-target path constructor using protected bad cycles, plus exact audits.

The polynomial constructor is held_cycle_path; audit enumeration is separate.
No target solver or approximation algorithm is supplied.
"""
from fractions import Fraction as F
from collections import deque
import json

from permanent_buffer_activation import activation_data, path_peak, priority_instance


def held_cycle_path(edges, fixed, C, T):
    C,T=F(C),F(T)
    fixed=[F(v) for v in fixed]
    edges=[(s,t,F(a),F(b)) for s,t,a,b in edges]
    S,Q,A,U,h=activation_data(edges,fixed,C,T)
    H={i for i,v in enumerate(h) if v>0}
    selected={}
    for i in sorted(H):
        ids=[j for j,(s,t,a,b) in enumerate(edges) if s==i and a>=h[i]]
        if not ids:
            return None
        selected[i]=ids[0]
    complete=set();good=[];bad=[]
    for start in sorted(H):
        chain=[];position={};v=start
        while v in H and v not in complete and v not in position:
            position[v]=len(chain);chain.append(v);v=edges[selected[v]][1]
        if v in position:
            cycle=chain[position[v]:]
            if any(edges[selected[i]][3]<=U-S[edges[selected[i]][1]] for i in cycle):
                good.append(cycle)
            else:
                bad.append(cycle)
        complete.update(chain)
    protected={i for cycle in bad for i in cycle}
    order=[];permanent=set(range(len(fixed)))-H
    # Complete safe cycles before any attached tree enters their vertices.
    for cycle in good:
        k=next(k for k,v in enumerate(cycle)
               if edges[selected[v]][3]<=U-S[edges[selected[v]][1]])
        order.extend(selected[cycle[(k-r)%len(cycle)]] for r in range(len(cycle)))
        permanent.update(cycle)
    # Protected receivers are conditional roots, not permanently active yet.
    roots=permanent|protected;pending=H-roots
    pred={i:[] for i in range(len(fixed))}
    for s in pending:
        pred[edges[selected[s]][1]].append(s)
    todo=deque(sorted(roots))
    while todo:
        t=todo.popleft()
        for s in sorted(pred[t]):
            assert s in pending
            pending.remove(s);permanent.add(s);order.append(selected[s]);todo.append(s)
    assert not pending
    # Hold all selected bad-cycle edges, evacuate their full source complements.
    selected_ids=set(selected.values())
    order.extend(j for j in range(len(edges)) if j not in selected_ids)
    for i in protected:
        assert A[i]-edges[selected[i]][2]>=h[i]
    phase2_end=len(order)
    order.extend(selected[i] for i in sorted(protected))
    assert len(order)==len(edges) and len(set(order))==len(edges)
    # Each actual step and machine is checked; these are not search operations.
    current=list(S);removed=[F(0)]*len(fixed);peak=max(current)
    for k,j in enumerate(order):
        s,t,a,b=edges[j];current[s]-=a;current[t]+=b;removed[s]+=a
        assert min(current)>=0 and max(current)<=U
        peak=max(peak,max(current))
        if k+1==phase2_end:
            assert all(removed[i]>=h[i] for i in H)
    assert current==[f+q for f,q in zip(fixed,Q)]
    return {'order':order,'peak':str(peak),'protected_vertices':sorted(protected)}


def audit():
    records=[]
    split=[(i,1-i,1,F(3,5)) for i in range(2)]
    for i in range(2):split.extend([(i,1-i,F(1,4),F(1,10))]*4)
    r=held_cycle_path(split,[0,0],2,1)
    assert r['protected_vertices']==[0,1] and r['peak']=='12/5'
    records.append({'name':'protected_two_cycle',**r})
    tree=[(0,1,1,F(3,5)),(1,0,1,F(3,5))]
    for i in range(2):tree.extend([(i,1-i,F(1,4),F(1,20))]*4)
    tree.extend([(2,0,1,F(1,10)),(2,3,1,F(3,5)),
                 (3,2,1,F(3,10)),(3,2,1,F(3,10))])
    r=held_cycle_path(tree,[0]*4,2,1)
    assert r['protected_vertices']==[0,1]
    records.append({'name':'shared_protected_receivers_and_trees',**r})
    for args in [([], [0],0,0), ([(0,1,0,0)],[0,0],0,0),
                 ([],[1],1,1), (split,[F(0),F(0),F(1)],2,1)]:
        assert held_cycle_path(*args) is not None
    for c,d,q in [(F(19,10),F(1,10),F(3,5)),
                  (F(151,100),F(1,1000),F(1))]:
        edges,fixed,C=priority_instance(F(1),c,d,q)
        r=held_cycle_path(edges,fixed,C,F(1))
        assert r is not None
        records.append({'name':'priority_family','c':str(c),'d':str(d),'q':str(q),**r})
    # No eligible edge does not mean no path. The source-side local promise
    # fails here: S=3/2 > 1+3/8, while all source sizes are below h=1/2.
    tiny=[(0,1,F(3,8),F(1,4))]*4+[(1,0,F(3,8),F(1,4))]*4
    assert held_cycle_path(tiny,[0,0],F(3,2),F(1)) is None
    peak,_=path_peak(tiny,[F(0)]*2,[0,4,1,5,2,6,3,7])
    assert peak==F(7,4)<2
    # Uniform upper bound is sharp on the assigned-max promise class.
    sharp=[]
    for C in [F(1),F(5,4),F(3,2),F(7,4),F(2)]:
        if C<=F(3,2):
            edges=[(0,1,F(1),2-C),(1,0,F(1),2-C)]
            fixed=[C-1]*2
        else:
            edges=[(0,1,C/2,F(1,2))]*2+[(1,0,C/2,F(1,2))]*2
            fixed=[F(0)]*2
        r=held_cycle_path(edges,fixed,C,F(1));U=max(F(2),C+F(1,2))
        assert r is not None and F(r['peak'])==U
        for i in range(2):
            actual_max=max([fixed[i]]+[a for s,t,a,b in edges if s==i])
            assert fixed[i]+sum((a for s,t,a,b in edges if s==i),F(0))<=1+actual_max
        sharp.append({'C':str(C),'peak':str(U)})
    # Very long rational scale remains exact; no pseudo-polynomial loop.
    scale=F(1,2**263+9)
    scaled=[(s,t,F(a)*scale,F(b)*scale) for s,t,a,b in split]
    assert held_cycle_path(scaled,[0,0],2*scale,scale) is not None
    return {'status':'passed','arithmetic':'fractions.Fraction','cases':records,
            'degenerate_cases':4,'long_rational_scale':str(scale),
            'no_eligible_but_path_peak':str(peak),'sharp_local_promise_cases':sharp,
            'scope':'Finite constructor audits only. Actual tau is given. No general U path or target solver.'}


if __name__=='__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
