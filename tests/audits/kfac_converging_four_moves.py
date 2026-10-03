"""Independent exact audit of the reviewed general four-move constructor.

This script checks abstract initial boxes and all three movable customers'
conditional costs from the model. It does not use a repository solver.
Earlier check_converging_path.py only tests tight A and equal A,C counts;
it must not be presented as checking this more general parameter class.
Finite sampling is an arithmetic check, not the universal proof.
"""
import json
import random
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


OPTIONS=((0,1),(0,2),(1,3))  # X on AB, Z on AC, T on BD.


def audit(gamma,r,p,Q,R,P_A,K,c,d,x,z,t):
    q=(r,p,R,Q);frozen=(P_A,K,c,d);weights=(x,z,t)
    state=[1,2,3]
    trace=[];events=[]
    def totals():
        W=list(frozen)
        for w,u in zip(weights,state):W[u]+=w
        return W
    def box():return all(v*gamma<=w<=(v+1)*gamma for w,v in zip(totals(),q))
    def improves(i):
        u=state[i];v=next(k for k in OPTIONS[i] if k!=u);W=totals()
        return (W[u]-weights[i])*q[v]>W[v]*q[u]
    def potential():
        W=totals();ss=[v*v for v in frozen]
        for v,u in zip(weights,state):ss[u]+=v*v
        return sum(F(v*v-vv,2*h) for v,vv,h in zip(W,ss,q))
    def move(i,event):
        assert improves(i)
        before=potential();old=state[i]
        state[i]=next(k for k in OPTIONS[i] if k!=old)
        assert box() and potential()<before
        trace.append((i,old,state[i]));events.append(event)
    assert Q>=p>=r>=1 and R>=r and 0<x<gamma and 0<z<gamma and 0<t<gamma
    assert box()
    if improves(1):move(1,'Z-first')
    if improves(2):move(2,'T-first')
    if improves(0):move(0,'X')
    if state[2]==3 and improves(2):move(2,'T-after-X')
    if state[1]==0 and improves(1):move(1,'Z-return')
    assert box() and not any(improves(i) for i in range(3))
    counts=Counter(i for i,old,new in trace)
    assert counts[0]<=1 and counts[1]<=2 and counts[2]<=1 and len(trace)<=4
    return events,len(trace)


def strict_instance():
    """Rebuild actual greedy, four moves, full client NE, and old-class failures."""
    data=json.loads((Path(__file__).resolve().parents[2] / 'examples/multi_facility/greedy_converging_four_moves.json').read_text())
    sites=data['sites'];weights=[F(v['weight']) for v in data['clients']]
    options=[set(v['sites']) for v in data['clients']]
    q={s:0 for s in sites};assignment=[None]*len(weights);trace=[]
    def totals():
        return {s:sum((w for w,u in zip(weights,assignment) if u==s),F(0)) for s in sites}
    for _ in range(data['k']):
        W=totals()
        scores={s:W[s]/(q[s]+1) if q[s] else
                sum((w for w,u,o in zip(weights,assignment,options) if u is None and s in o),F(0))
                for s in sites}
        selected=max(sites,key=lambda s:scores[s])
        assert all(scores[selected]>scores[s] for s in sites if s!=selected)
        trace.append((selected,scores[selected]))
        if not q[selected]:
            for i,o in enumerate(options):
                if assignment[i] is None and selected in o:assignment[i]=selected
        q[selected]+=1
    assert trace==[('D',390),('B',220),('C',219),('D',195),('D',130),
                   ('B',110),('C',F(219,2)),('A',105),('R',100)]
    gamma=trace[-1][1]
    assert [q[s] for s in sites]==[1,2,2,3,1]
    assert assignment==['A','B','C','D','R','B','C','D']
    W0=totals()
    def assert_box():
        W=totals()
        assert all(q[s]*gamma<=W[s]<=(q[s]+1)*gamma for s in sites)
    assert_box()
    actual=[]
    for i,target in [(6,'A'),(7,'B'),(5,'A'),(6,'C')]:
        W=totals();source=assignment[i]
        old=(W[source]-weights[i])/q[source];new=W[target]/q[target]
        assert old>new
        actual.append((i,source,target,old,new))
        assignment[i]=target;assert_box()
    assert actual==[(6,'C','A',107,105),(7,'D','B',F(340,3),110),
                    (5,'B','A',125,110),(6,'A','C',125,107)]
    W=totals()
    assert [W[s] for s in sites]==[125,250,219,340,100]
    # Check EVERY client and every accessible occupied facility group, including
    # all frozen clients. Uniform mixing makes same-site facilities indifferent.
    for i,(w,s,o) in enumerate(zip(weights,assignment,options)):
        assert all((W[s]-w)/q[s]<=W[u]/q[u] for u in o if u!=s)
    # Final boxes are the complete BOX-TO-2 interface, not a mere potential test.
    assert_box()
    groups={h:[s for s in sites if q[s]==h] for h in set(q.values())}
    alpha={h:min(W0[s]/h for s in ss) for h,ss in groups.items()}
    beta={h:max(W0[s]/h for s in ss) for h,ss in groups.items()}
    assert alpha=={1:100,2:F(219,2),3:130}
    assert beta=={1:105,2:110,3:130}
    assert beta[2]-weights[6]/2>alpha[1]  # Z fails RANGE's cross-q certificate.
    assert beta[3]-weights[7]/3>alpha[2]  # T fails it too.
    light=[i for i,w in enumerate(weights) if len(options[i])>1 and w<gamma]
    assert light==[5,6,7] and len({weights[i] for i in light})==3
    edges=[options[i] for i in light];component=set.union(*edges)
    assert component=={'A','B','C','D'}
    assert not set.intersection(*edges)  # No common/nested initial anchor.
    assert all(len(edge)==2<len(component) for edge in edges)  # Not all-or-one.
    degrees={s:sum(s in edge for edge in edges) for s in component}
    assert sorted(degrees.values())==[1,1,2,2]  # Nonstar and larger than two sites.
    assert len({q[s] for s in component})>1  # Not constant-multiplicity light component.
    opening={s:next(j for j,(u,_) in enumerate(trace) if u==s) for s in component}
    oriented=[tuple(sorted(edge,key=lambda s:opening[s])) for edge in edges]
    assert set(oriented)=={('B','A'),('C','A'),('D','B')}
    indegree={s:sum(u==s for v,u in oriented) for s in component}
    outdegree={s:sum(v==s for v,u in oriented) for s in component}
    assert sum(indegree[s]==0 for s in component)==2  # Not a consistently directed path.
    assert max(indegree.values())==2
    # Conditions removed from the old theorem really fail on this strict input.
    assert W0['A']>q['A']*gamma and q['A']!=q['C']
    events,n=audit(100,1,2,3,2,105,200,214,340,20,5,50)
    assert events==['Z-first','T-first','X','Z-return'] and n==4
    return {'greedy_trace':[(s,str(v)) for s,v in trace],
            'moves':[(i,s,u,str(old),str(new)) for i,s,u,old,new in actual],
            'final_totals':{s:str(W[s]) for s in sites},
            'range_failures':['Z:107.5>100','T:340/3>219/2'],
            'full_on_path_client_NE':True,'all_step_boxes':True}


if __name__=='__main__':
    exact=strict_instance()
    rng=random.Random(91268);counts=Counter();lengths=Counter();tuples=set();untight=0;unequal=0
    for _ in range(20000):
        Q=rng.randint(1,12);p=rng.randint(1,Q);r=rng.randint(1,p);R=rng.randint(r,12)
        gamma=rng.randint(4,100)
        x,z,t=[rng.randint(1,gamma-1) for _ in range(3)]
        P_A=rng.randint(r*gamma,(r+1)*gamma)
        K=rng.randint(p*gamma,(p+1)*gamma)-x
        c=rng.randint(R*gamma,(R+1)*gamma)-z
        d=rng.randint(Q*gamma,(Q+1)*gamma)-t
        events,n=audit(gamma,r,p,Q,R,P_A,K,c,d,x,z,t)
        counts.update(events);lengths[n]+=1;tuples.add((r,p,Q,R))
        untight+=P_A!=r*gamma;unequal+=R!=r
    print(json.dumps({'seed':91268,'cases':20000,'q_tuples':len(tuples),
                      'A_not_tight':untight,'A_C_q_unequal':unequal,
                      'events':dict(counts),'lengths':dict(lengths)},sort_keys=True),flush=True)
    print(json.dumps({'strict_instance':exact},sort_keys=True),flush=True)
