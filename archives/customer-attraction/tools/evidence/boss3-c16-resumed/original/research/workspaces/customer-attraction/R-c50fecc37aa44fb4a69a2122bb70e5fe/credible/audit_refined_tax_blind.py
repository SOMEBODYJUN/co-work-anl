"""Blind independent audit: no canonical solver, no imported strategy packet.

The input is the security agent's k=10 instance. Integer-scaled terminal
payoffs are computed by expanding all 36 distinct unit customers. Exact
set-valued backward induction is followed by an explicit strategy automaton
whose state includes both prefix counts AND promised terminal outcome.
Every action arc is checked. Path multiplicities prove all ordered histories
are represented; the automaton does not assert a lossless Markov reduction.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
import argparse
import json
from math import lcm
from pathlib import Path
import time

P=6;M=13
CLASSES=(({0},2),({1},2),({2},1),({2,3},1),({2,4},1),({0,3,4},3),({1,3,4},1),({5},25))
UNITS=tuple(frozenset(s) for s,n in CLASSES for _ in range(n))
SCALE=lcm(*range(1,M+1))
TARGET=(2,1,0,0,0,10)
PATH=(5,)*10+(0,0,1)

def vectors(p,total):
    if p==1:
        yield (total,);return
    for x in range(total+1):
        for tail in vectors(p-1,total-x):yield (x,)+tail

def inc(k,a):return k[:a]+(k[a]+1,)+k[a+1:]

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():raise FileExistsError(args.output)
    started=time.monotonic()
    terminals=tuple(vectors(P,M));ids={q:i for i,q in enumerate(terminals)}
    values=[]
    for q in terminals:
        u=[0]*P
        for interested in UNITS:
            load=sum(q[a] for a in interested)
            if load:
                for a in interested:
                    if q[a]:u[a]+=SCALE//load
        values.append(tuple(u))
    outcomes={};thresholds={};mins={}
    def solve(k):
        if k in outcomes:return outcomes[k]
        if sum(k)==M:
            result=frozenset({ids[k]})
        else:
            children=[solve(inc(k,a)) for a in range(P)]
            lower=[min(values[i][a] for i in child) for a,child in enumerate(children)]
            floor=max(lower);thresholds[k]=floor
            mins[k]=tuple(min(child,key=lambda i:(values[i][a],i)) for a,child in enumerate(children))
            result=frozenset(i for a,child in enumerate(children) for i in child if values[i][a]>=floor)
            assert result
        outcomes[k]=result;return result
    zero=(0,)*P;root=solve(zero);target=ids[TARGET]
    assert target in root
    forced=[];k=zero
    for depth,a in enumerate(PATH):
        assert target in solve(inc(k,a)) and values[target][a]>=thresholds[k]
        forced.append({'depth':depth,'counts':k,'action':a,'target_payoff':str(F(values[target][a],SCALE)),'required_floor':str(F(thresholds[k],SCALE))})
        k=inc(k,a)
    # Automaton uses (prefix counts, promised outcome, active root path).
    action={};arcs={};state_terminal={}
    def build(k,t,active):
        state=(k,t,active)
        if state in state_terminal:return state
        state_terminal[state]=None
        if sum(k)==M:
            assert ids[k]==t;state_terminal[state]=t;return state
        choices=[a for a in range(P) if t in solve(inc(k,a)) and values[t][a]>=thresholds[k]]
        chosen=PATH[sum(k)] if active else choices[0]
        assert chosen in choices
        action[state]=chosen;children=[]
        for a in range(P):
            childtarget=t if a==chosen else mins[k][a]
            children.append(build(inc(k,a),childtarget,active and a==chosen))
        arcs[state]=tuple(children);state_terminal[state]=t
        return state
    initial=build(zero,target,True)
    # Definition-level replay of the whole automaton, not the BI inequalities.
    # Terminal propagation, complete action arcs, and all mover deviations.
    checked=0;slack_min=None
    for state,children in arcs.items():
        k,t,active=state;chosen=action[state]
        assert len(children)==P
        for a,child in enumerate(children):assert child[0]==inc(k,a)
        actual=state_terminal[children[chosen]]
        assert actual==t
        for a,child in enumerate(children):
            deviation=state_terminal[child]
            slack=values[actual][chosen]-values[deviation][a]
            assert slack>=0,(state,a,slack)
            slack_min=slack if slack_min is None else min(slack_min,slack)
            if a!=chosen:checked+=1
    multiplicity={initial:1};depth_totals=[]
    for depth in range(M+1):
        states=[s for s in state_terminal if sum(s[0])==depth]
        total=sum(multiplicity.get(s,0) for s in states)
        assert total==P**depth
        depth_totals.append({'depth':depth,'automaton_states':len(states),'ordered_histories':total})
        if depth<M:
            for state in states:
                for child in arcs[state]:multiplicity[child]=multiplicity.get(child,0)+multiplicity.get(state,0)
    # Actual path and terminal welfare directly on the 36 expanded units.
    state=initial;actual=[]
    while state in arcs:
        a=action[state];actual.append(a);state=arcs[state][a]
    assert tuple(actual)==PATH
    welfare=sum(any(TARGET[a] for a in interested) for interested in UNITS)
    optimum=max(sum(any(q[a] for a in interested) for interested in UNITS) for q in terminals)
    alpha=F(M-1,M)
    g=tuple(sum((1/(1+alpha*sum(TARGET[b] for b in interested)) for interested in UNITS if a in interested),F(0)) for a in range(P))
    credit=sum((1/(1+alpha*sum(TARGET[b] for b in interested)) for interested in UNITS if any(TARGET[b] for b in interested)),F(0))
    gap=M*max(g)-welfare-credit
    assert g==(F(65,37),F(39,25),F(3),F(2381,925),F(2381,925),F(325,133))
    assert (welfare,optimum,credit,gap)==(33,36,F(708669,123025),F(29481,123025))
    report={'scope':'independent exact k10 finite counterexample to refined actual-load tax payment bridge; not Q-CAG-HALF','unit_customers':len(UNITS),'players':M,'topics':P,'target_counts':TARGET,'actual_ordered_path':actual,'integer_payoff_scale':SCALE,'BI_count_states':len(outcomes),'BI_terminal_states':len(terminals),'BI_root_outcomes':len(root),'strategy_automaton_states':len(state_terminal),'strategy_decision_states':len(arcs),'automaton_nontrivial_deviations_checked':checked,'all_ordered_decision_histories':sum(P**d for d in range(M)),'all_ordered_nontrivial_deviations':(P-1)*sum(P**d for d in range(M)),'all_ordered_terminal_histories':P**M,'depth_multiplicity_totals':depth_totals,'root_forced_path_admissibility':forced,'welfare':welfare,'optimum':optimum,'g':[str(x) for x in g],'G_C':str(credit),'refined_bridge_gap':str(gap),'seconds':time.monotonic()-started,'no_canonical_solver_or_security_packet_imported':True}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('root_forced_path_admissibility','depth_multiplicity_totals')}))

if __name__=='__main__':main()
