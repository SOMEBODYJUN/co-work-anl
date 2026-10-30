"""Exact audit of permanent buffers and two failed path-selection contracts.

No general path constructor or approximation algorithm is implemented here.
"""
from fractions import Fraction as F
from collections import deque
import json


def loads(edges, fixed, mask):
    result = list(fixed)
    for j, (s, t, a, b) in enumerate(edges):
        result[t if mask >> j & 1 else s] += b if mask >> j & 1 else a
    return result


def activation_data(edges, fixed, C, T):
    C,T=F(C),F(T)
    fixed=[F(v) for v in fixed]
    edges=[(s,t,F(a),F(b)) for s,t,a,b in edges]
    assert fixed and 0 <= T <= C <= 2*T and all(v>=0 for v in fixed)
    assert all(0<=s<len(fixed) and 0<=t<len(fixed) and s!=t for s,t,a,b in edges)
    S = loads(edges, fixed, 0)
    Q = [F(0)] * len(fixed)
    A = [F(0)] * len(fixed)
    for s, t, a, b in edges:
        A[s] += a
        Q[t] += b
    U = max(2*T, C+T/2)
    h = [max(F(0), s+q-U) for s, q in zip(S, Q)]
    assert max(S, default=F(0)) <= C
    assert all(f+q <= T for f, q in zip(fixed, Q))
    assert all(0 <= a <= T and 0 <= b <= T for s,t,a,b in edges)
    assert all(3*x <= a for x,a in zip(h,A))
    assert all(q/3 <= U-s for q,s in zip(Q,S))
    return S,Q,A,U,h


def check_state_identities(edges, fixed, C, T):
    S,Q,A,U,h = activation_data(edges,fixed,C,T)
    for mask in range(1 << len(edges)):
        removed = [F(0)] * len(fixed)
        remaining = [F(0)] * len(fixed)
        for j,(s,t,a,b) in enumerate(edges):
            if mask >> j & 1:
                removed[s] += a
            else:
                remaining[t] += b
        actual = loads(edges,fixed,mask)
        assert actual == [s+q-d-r for s,q,d,r in zip(S,Q,removed,remaining)]
        for i in range(len(fixed)):
            assert (removed[i] >= h[i]) == (S[i]+Q[i]-removed[i] <= U)
            assert (actual[i] <= U) == (remaining[i] >= S[i]+Q[i]-U-removed[i])
    return 1 << len(edges)


def priority_instance(T, c, d, q):
    assert T > 0 and F(3,2) < c < 2 and 0 < d < F(1,3) and F(1,2) < q <= 1
    edges=[]
    for i in range(2):
        edges.extend([(i,1-i,c*T/2,(1-d)*T/2)] * 2)
    for i in range(2):
        edges.extend([(i+2,i,T,d*T),(i+2,3-i,(c-1)*T,q*T)])
    return edges,[F(0)]*4,c*T


def all_priority_terminal_states(edges, fixed, C, T, rule, inactive_only=False):
    S,Q,A,U,h=activation_data(edges,fixed,C,T)
    seen={0}; todo=[0]; terminal=[]
    while todo:
        mask=todo.pop()
        removed=[F(0)]*len(fixed)
        for j,(s,t,a,b) in enumerate(edges):
            if mask >> j & 1:
                removed[s] += a
        choices=[]
        for j,(s,t,a,b) in enumerate(edges):
            if mask >> j & 1 or (inactive_only and removed[s] >= h[s]):
                continue
            nxt=mask | (1 << j)
            if max(loads(edges,fixed,nxt)) <= U:
                score=a if rule == 'source' else a/b
                choices.append((score,nxt))
        if not choices:
            terminal.append(mask)
            continue
        score=max(v for v,nxt in choices)
        for v,nxt in choices:
            if v == score and nxt not in seen:
                seen.add(nxt); todo.append(nxt)
    for mask in terminal:
        assert mask != (1 << len(edges))-1
        assert all(max(loads(edges,fixed,mask | (1 << j))) > U
                   for j in range(4) if not mask >> j & 1)
        assert mask & 15 == 0
    return sorted(terminal)


def path_peak(edges,fixed,order):
    mask=0; peak=max(loads(edges,fixed,mask)); trace=[loads(edges,fixed,mask)]
    for j in order:
        assert not mask >> j & 1
        mask |= 1 << j
        state=loads(edges,fixed,mask)
        peak=max(peak,max(state)); trace.append(state)
    assert mask == (1 << len(edges))-1
    return peak,trace


def all_endpoint_optimum(edges,fixed):
    return min(max(loads(edges,fixed,mask)) for mask in range(1 << len(edges)))


def static_instance():
    edges=[(0,1,F(1),F(3,5)),(0,2,F(1),F(3,5)),
           (1,0,F(1),F(3,10)),(1,2,F(1),F(1,5)),
           (2,0,F(1),F(3,10)),(2,1,F(1),F(1,5))]
    return edges,[F(0),F(0),F(0),F(1)]


def single_unlock_path(edges, fixed, C, T):
    """Given the actual target, return a certified path or certificate failure.

    None never means OPT>T or that no capacity-U path exists.
    """
    C,T=F(C),F(T)
    fixed=[F(v) for v in fixed]
    edges=[(s,t,F(a),F(b)) for s,t,a,b in edges]
    S,Q,A,U,h=activation_data(edges,fixed,C,T)
    H={i for i,v in enumerate(h) if v>0}
    eligible={i:[] for i in H}
    for j,(s,t,a,b) in enumerate(edges):
        if s in H and a>=h[s]:
            eligible[s].append(j)
    witness={}
    reverse={i:[] for i in H}
    for i,ids in eligible.items():
        for j in ids:
            s,t,a,b=edges[j]
            if t not in H or b<=U-S[t]:
                witness.setdefault(i,j)
            if t in H:
                reverse[t].append(i)
    distance={i:0 for i in witness}
    todo=deque(sorted(distance))
    while todo:
        t=todo.popleft()
        for s in sorted(reverse[t]):
            if s not in distance:
                distance[s]=distance[t]+1; todo.append(s)
    if len(distance)!=len(H):
        return None
    selected={}
    for s in sorted(H):
        if s in witness:
            selected[s]=witness[s]
        else:
            selected[s]=next(j for j in eligible[s]
                             if edges[j][1] in distance and
                             distance[edges[j][1]]==distance[s]-1)
    # Each function component has one directed cycle or ends outside H.
    complete=set(); cycles=[]
    for start in sorted(H):
        chain=[]; index={}; v=start
        while v in H and v not in complete and v not in index:
            index[v]=len(chain); chain.append(v); v=edges[selected[v]][1]
        if v in index:
            cycles.append(chain[index[v]:])
        complete.update(chain)
    order=[]; safe=set(range(len(fixed)))-H
    for cycle in cycles:
        k=next(k for k,v in enumerate(cycle)
               if edges[selected[v]][3] <= U-S[edges[selected[v]][1]])
        rotation=[cycle[(k-r)%len(cycle)] for r in range(len(cycle))]
        order.extend(selected[v] for v in rotation); safe.update(cycle)
    pending=H-safe
    pred={i:[] for i in range(len(fixed))}
    for s in pending:
        pred[edges[selected[s]][1]].append(s)
    todo=deque(sorted(safe))
    while todo:
        t=todo.popleft()
        for s in sorted(pred[t]):
            if s in pending:
                pending.remove(s); safe.add(s); order.append(selected[s]); todo.append(s)
    assert not pending
    used=set(order)
    order.extend(j for j in range(len(edges)) if j not in used)
    peak,trace=path_peak(edges,fixed,order)
    assert peak<=U
    return order


def audit():
    cases=[(F(1),F(19,10),F(1,10),F(3,5)),
           (F(3,7),F(151,100),F(1,1000),F(501,1000)),
           (F(7,3),F(1999,1000),F(333,1000),F(1)),
           (F(1,2**257+1),F(7,4),F(1,7),F(4,5))]
    records=[]
    for T,c,d,q in cases:
        edges,fixed,C=priority_instance(T,c,d,q)
        states=check_state_identities(edges,fixed,C,T)
        assert all_endpoint_optimum(edges,fixed)==T
        peak,trace=path_peak(edges,fixed,[0,2,1,3,4,6,5,7])
        assert peak == C+(1-d)*T/2
        rules={}
        for rule in ['source','ratio']:
            for inactive in [False,True]:
                terminal=all_priority_terminal_states(edges,fixed,C,T,rule,inactive)
                rules[rule+('_inactive' if inactive else '')]=terminal
                for mask in terminal:
                    assert loads(edges,fixed,mask)[:2] == [C+d*T]*2
                    assert C+d*T+(1-d)*T/2 > C+T/2
                    if not inactive:
                        assert all(max(loads(edges,fixed,mask|(1 << j))) > C+T/2
                                   for j in range(len(edges)) if not mask >> j & 1)
        records.append({'T':str(T),'c':str(c),'d':str(d),'q':str(q),
                        'state_identity_checks':states,'optimum':str(T),
                        'good_path_peak':str(peak),'all_tie_terminals':rules})
        selected_order=single_unlock_path(edges,fixed,C,T)
        assert selected_order is not None
        records[-1]['unlock_selector_peak']=str(path_peak(edges,fixed,selected_order)[0])
    edges,fixed=static_instance()
    S,Q,A,U,h=activation_data(edges,fixed,F(2),F(1))
    feasible=[]
    for mask in range(1 << len(edges)):
        removed=[F(0)]*4; received=[F(0)]*4
        for j,(s,t,a,b) in enumerate(edges):
            if mask >> j & 1:
                removed[s]+=a; received[t]+=b
        if all(removed[i]>=h[i] and received[i]<=U-S[i] for i in range(4)):
            feasible.append(mask)
    assert not feasible
    peak,trace=path_peak(edges,fixed,[2,0,3,4,1,5])
    assert peak==F(23,10)
    assert all_endpoint_optimum(edges,fixed)==1
    static_states=check_state_identities(edges,fixed,F(2),F(1))
    sharp=[(0,1,F(3,4),F(1,2))]*2+[(1,0,F(3,4),F(1,2))]*2
    S,Q,A,U,h=activation_data(sharp,[F(0)]*2,F(3,2),F(1))
    assert h[0]/A[0]==h[1]/A[1]==F(1,3)
    # Degenerate domains: no jobs, zero jobs, fixed jobs, and mixed zero endpoints.
    degenerate=[([], [F(0)], F(0),F(0)),
                ([(0,1,F(0),F(0))], [F(0)]*2,F(0),F(0)),
                ([],[F(1)],F(1),F(1)),
                ([(0,1,F(1),F(0)),(1,0,F(0),F(1))], [F(0)]*2,F(1),F(1))]
    for args in degenerate:
        check_state_identities(*args)
        assert single_unlock_path(*args) is not None
    int_edges=[(0,1,1,F(1,2))]*2+[(1,0,1,F(1,2))]*2
    assert single_unlock_path(int_edges,[0,0],2,1) is not None
    assert single_unlock_path(*static_instance(),F(2),F(1)) is not None
    # Certificate failure can coexist with an explicit capacity-U path.
    split=[(i,1-i,F(1),F(3,5)) for i in range(2)]
    for i in range(2):
        split.extend([(i,1-i,F(1,4),F(1,10))]*4)
    assert single_unlock_path(split,[F(0)]*2,F(2),F(1)) is None
    split_peak,_=path_peak(split,[F(0)]*2,list(range(2,10))+[0,1])
    assert split_peak==F(12,5)<F(5,2)
    return {'status':'passed','arithmetic':'fractions.Fraction',
            'scope':'Finite audits only; universal claims use the separate proof.',
            'priority_cases':records,
            'static_obstruction':{'subsets':64,'feasible_subsets':0,
                                  'optimum':'1','good_path_peak':str(peak),
                                  'state_identity_checks':static_states},
            'sharp_source_fraction':'1/3','degenerate_cases':len(degenerate)}


if __name__ == '__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
