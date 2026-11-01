"""Independent unit-customer Fraction audit of the C5 interval-floor obstruction.

No canonical solver, interval implementation, floating arithmetic, or optimizer
is imported. Both recurrences are rebuilt directly from the five unit clients.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import argparse,json

Q=5
M=6
CUSTOMERS=tuple(frozenset((a,(a+1)%Q))for a in range(Q))
ZERO=(0,)*Q
RECORDS={}


def add(b,a):return b[:a]+(b[a]+1,)+b[a+1:]


@lru_cache(None)
def payoff(z):
    return tuple(sum((F(1,sum(z[j]for j in C))for C in CUSTOMERS if a in C),F())if z[a]else F()for a in range(Q))


@lru_cache(None)
def interval(b):
    if sum(b)==M:return frozenset((b,))
    ch=[interval(add(b,a))for a in range(Q)]
    lo=[min(payoff(z)[a]for z in ch[a])for a in range(Q)]
    hi=[max(payoff(z)[a]for z in ch[a])for a in range(Q)]
    floor=max(lo);E=tuple(a for a in range(Q)if hi[a]>=floor)
    RECORDS[b]=dict(prefix=b,floor=str(floor),allowed=E,
                   child_minimum=list(map(str,lo)),child_maximum=list(map(str,hi)),
                   low_witnesses=[min(z for z in ch[a]if payoff(z)[a]==lo[a])for a in range(Q)],
                   high_witnesses=[min(z for z in ch[a]if payoff(z)[a]==hi[a])for a in range(Q)])
    return frozenset(z for a in E for z in ch[a])


@lru_cache(None)
def exact_spe(b):
    if sum(b)==M:return frozenset((b,))
    ch=[exact_spe(add(b,a))for a in range(Q)]
    floor=max(min(payoff(z)[a]for z in ch[a])for a in range(Q))
    return frozenset(z for a in range(Q)for z in ch[a]if payoff(z)[a]>=floor)


@lru_cache(None)
def budget(b):
    if sum(b)==M:return F()
    interval(b);rec=RECORDS[b]
    return F(rec['floor'])+min(budget(add(b,a))for a in rec['allowed'])


def false_path(target):
    b=ZERO;path=[];gaps=[]
    while sum(b)<M:
        rec=RECORDS[b]
        actions=[a for a in rec['allowed']if target in interval(add(b,a))]
        assert actions
        a=min(actions);final=payoff(target)[a];floor=F(rec['floor'])
        step=dict(prefix=b,action=a,node_floor=str(floor),tagged_payoff_in_target=str(final))
        if final<floor:
            witness=rec['high_witnesses'][a]
            step.update(high_witness=witness,high_witness_payoff=str(payoff(witness)[a]),strict_interval_leak=True)
            gaps.append(step)
        path.append(step);b=add(b,a)
    assert b==target and gaps
    return path,gaps


def run():
    H=interval(ZERO);S=exact_spe(ZERO)
    lo=[min(payoff(z)[a]for z in interval(add(ZERO,a)))for a in range(Q)]
    hi=[max(payoff(z)[a]for z in interval(add(ZERO,a)))for a in range(Q)]
    exactfloor=max(min(payoff(z)[a]for z in exact_spe(add(ZERO,a)))for a in range(Q))
    attainable=[sorted(set(payoff(z)[a]for z in exact_spe(add(ZERO,a))if payoff(z)[a]>=exactfloor))for a in range(Q)]
    threshold=F(2,1+F(2*M,Q))
    assert lo==[F(1,2)]*Q and exactfloor==F(2,3)
    assert threshold==F(10,17)>max(lo)
    assert attainable==[[F(2,3),F(5,6),F(1)]]*Q
    assert S<=H and len(S)==20
    assert all(sum(any(z[a]for a in C)for C in CUSTOMERS)==5 for z in S)
    target=RECORDS[ZERO]['low_witnesses'][0]
    assert target in H and target not in S and payoff(target)[0]==F(1,2)
    path,gaps=false_path(target)
    # Static lower bound, proved in the note: uniform-query payoff is
    # (2/5) sum_C 1/(1+6 q(C)); sum_C q(C)=2, so Jensen gives 10/17.
    assert sum(len(C)for C in CUSTOMERS)==10
    summary=dict(status='PASS',model='five unit customers, common C5 catalog, six unit players',
                 instance=dict(players=M,topics=list(map(str,range(Q))),customers=[dict(topics=sorted(C),multiplicity=1)for C in CUSTOMERS]),
                 interval_root_floor=str(max(lo)),extra_one_fractional_threshold=str(threshold),strict_gap=str(threshold-max(lo)),
                 true_spe_root_threshold=str(exactfloor),true_root_attainable_utilities=[list(map(str,a))for a in attainable],
                 root_interval_outcomes=len(H),root_spe_outcomes=len(S),interval_budget=str(budget(ZERO)),OPT=5,minimum_spe_welfare=5,
                 root_child_minimum=list(map(str,lo)),root_child_maximum=list(map(str,hi)),
                 root_low_witnesses=RECORDS[ZERO]['low_witnesses'],root_high_witnesses=RECORDS[ZERO]['high_witnesses'],
                 false_terminal=target,false_path=path,strict_leaks=gaps,
                 interval_nonterminal_states=len(RECORDS),scope='Only LI>=t_(r+1) fails; no SPE or half-coverage counterexample.')
    packet=dict(summary=summary,interval_witness_records=[RECORDS[b]for b in sorted(RECORDS,key=lambda b:(sum(b),b))],
                root_interval_terminal_counts=sorted(H),root_spe_terminal_counts=sorted(S))
    return summary,packet


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output');ap.add_argument('--packet');a=ap.parse_args()
    summary,packet=run()
    if a.output:
        with Path(a.output).open('x')as f:json.dump(summary,f,indent=2);f.write('\n')
    if a.packet:
        with Path(a.packet).open('x')as f:json.dump(packet,f,indent=2);f.write('\n')
    print(json.dumps(summary,indent=2))
