#!/usr/bin/env python3
"""Exact independent finite certificate of the depth-three selector obstruction."""
from fractions import Fraction as F
from itertools import product
import json

SITES = ('A1','A2','B','C','D','R')
K = 15
CLIENTS = ((4599,(0,)),(4598,(1,)),(3045,(2,)),(2000,(3,)),
           (1451,(4,)),(1000,(5,)),(400,(0,2)),(400,(1,2)),
           (900,(2,3)),(150,(3,4)))


def greedy():
    q, totals, origins = [0]*6, [0]*6, [-1]*10
    trace, opened = [], {}
    for step in range(K):
        scores = [F(totals[t],q[t]+1) if q[t] else
                  sum((F(w) for i,(w,opts) in enumerate(CLIENTS)
                       if origins[i]<0 and t in opts), F(0)) for t in range(6)]
        maximum = max(scores)
        winners = [t for t in range(6) if scores[t]==maximum]
        assert len(winners)==1, (step, scores)
        t = winners[0]
        if not q[t]:
            opened[t] = step
            for i,(w,opts) in enumerate(CLIENTS):
                if origins[i]<0 and t in opts:
                    origins[i]=t
                    totals[t]+=w
        q[t]+=1
        trace.append((t,maximum))
    return tuple(q),tuple(totals),tuple(origins),opened,trace


def evaluate(assignment,q,gamma):
    totals,squares = [0]*6,[0]*6
    for (w,opts),t in zip(CLIENTS,assignment):
        assert t in opts
        totals[t]+=w
        squares[t]+=w*w
    potential = sum((F(totals[t]**2-squares[t],2*q[t]) for t in range(6)),F(0))
    boxed = all(q[t]*gamma<=totals[t]<=(q[t]+1)*gamma for t in range(6))
    violations = tuple((i,t,v,F(totals[t]-w,q[t]),F(totals[v],q[v]))
                       for i,((w,opts),t) in enumerate(zip(CLIENTS,assignment))
                       for v in opts if v!=t and
                       F(totals[t]-w,q[t])>F(totals[v],q[v]))
    return potential,tuple(totals),boxed,violations


def main():
    q,initial,origins,opened,trace=greedy()
    gamma=trace[-1][1]
    assert q==(4,4,3,2,1,1) and gamma==1000
    assert initial==(4999,4998,3945,2150,1451,1000)
    assert origins==tuple(range(6))+(0,1,2,3)
    assert [t for t,score in trace]==[0,1,2,0,1,3,2,0,1,4,2,0,1,3,5]
    assert [score for t,score in trace]==list(map(F,(
        4999,4998,3945,F(4999,2),2499,2150,F(3945,2),
        F(4999,3),1666,1451,1315,F(4999,4),F(2499,2),1075,1000)))
    assert all(w<gamma and len(opts)==2 for w,opts in CLIENTS[6:])
    assert all(w>=gamma and len(opts)==1 for w,opts in CLIENTS[:6])
    oriented=[tuple(sorted(opts,key=lambda t:opened[t])) for w,opts in CLIENTS[6:]]
    assert oriented==[(0,2),(1,2),(2,3),(3,4)]
    expected={
        (2,2,3,4):(F(5948950,3),(4599,4598,3845,2900,1601,1000),False),
        (0,1,2,3):(F(1983200),(4999,4998,3945,2150,1451,1000),True),
        (2,1,3,4):(F(1983450),(4599,4998,3445,2900,1601,1000),False),
        (0,2,3,4):(F(1983550),(4999,4598,3445,2900,1601,1000),False),
        (0,1,3,4):(F(2037350),(4999,4998,3045,2900,1601,1000),False),
        (0,1,2,4):(F(2050850),(4999,4998,3945,2000,1601,1000),False),
    }
    rows={}
    all_states=list(product(*(opts for w,opts in CLIENTS[6:])))
    assert len(all_states)==16
    for choices in all_states:
        p,totals,boxed,violations=evaluate(tuple(range(6))+choices,q,gamma)
        if boxed:
            rows[choices]=(p,totals,not violations)
    assert rows==expected
    minimum=min(p for p,totals,ne in rows.values())
    minima=[state for state,(p,totals,ne) in rows.items() if p==minimum]
    assert minima==[(2,2,3,4)]
    assert [state for state,(_,_,ne) in rows.items() if ne]==[(0,1,2,3)]
    assert rows[(0,1,2,3)][0]-minimum==F(650,3)
    p,totals,boxed,violations=evaluate(tuple(range(6))+(2,2,3,4),q,gamma)
    assert violations==((9,4,3,F(1451),F(1450)),)
    assert totals[3]+150==3050>(q[3]+1)*gamma==3000
    print(json.dumps({
        'status':'exact strict-greedy audit passed',
        'multiplicities':q,'gamma':str(gamma),
        'strict_greedy_trace':[(SITES[t],str(score)) for t,score in trace],
        'all_light_assignments':16,'boxed_assignments':len(rows),
        'boxed_NEs':1,'unique_box_minimum':str(minimum),
        'unique_box_NE_potential':str(rows[(0,1,2,3)][0]),
        'NE_minus_minimum_gap':str(F(650,3)),
        'minimizer_strict_violation':'Z D->C: 1451 > 1450; C would be 3050 > 3000',
        'rows':[{'state':[SITES[t] for t in state],'P':str(p),'totals':totals,'NE':ne}
                for state,(p,totals,ne) in sorted(rows.items(),key=lambda item:item[1][0])],
        'scope':'one selector-correctness counterexample; not nonexistence of a box NE or factor-two witness'
    },indent=2))


if __name__=='__main__':
    main()
