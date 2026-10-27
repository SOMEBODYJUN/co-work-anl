"""Independent integer audit: all 12-theme six-slot potential comparisons.

Does not import the discovery code or use the balancing reduction.  This is a
static implication counterexample and an exact fatal SPE objection, not a
counterexample to half coverage in SPE.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import lcm
from pathlib import Path
import json

MASS = {0:F(159279,300121),27:F(156842,4501815),29:F(103968,1500605),
        30:F(103968,1500605),31:F(64046,6302541),32:F(717646,31512705),
        33:F(13112,1086645),34:F(12440,2100847),35:F(1328018,10504235),
        37:F(148268,4501815),38:F(148268,4501815),42:F(27664,4501815),
        44:F(1465682,31512705)}
H60=(0,60,90,110,125,137,147)


def main():
    scale=lcm(*(6*v.denominator for v in MASS.values()))
    clients=[]
    for mask,mass in MASS.items():
        count=mass*scale/6
        assert count.denominator==1 and count>0
        for j in range(6):
            clients.append((mask|(1<<(6+j)),int(count)))
    total=sum(n for mask,n in clients)
    assert total==scale
    actual=tuple(range(6))
    welfare=sum(n for mask,n in clients if mask&63)
    def payoff60(actions, pos):
        return sum(n*(60//sum((mask>>a)&1 for a in actions))
                   for mask,n in clients if (mask>>actions[pos])&1)
    u=[payoff60(actual,i) for i in range(6)]
    copy60=0
    for mask,n in clients:
        p=0
        for i in range(6):
            if (mask>>i)&1:
                copy60+=n*(60//(p+1)-60//(p+6-i))
                p+=1
    assert 60*welfare+copy60==60*total
    min_gap=None
    maximizer=None
    checked=0
    for actions in combinations_with_replacement(range(12),6):
        pot=sum(n*H60[sum((mask>>a)&1 for a in actions)] for mask,n in clients)
        gap=60*welfare+copy60-pot
        assert gap>=0
        if min_gap is None or gap<min_gap:
            min_gap,maximizer=gap,actions
        checked+=1
    prices=[]
    for a in range(12):
        price=sum(n*(60//(1+sum((mask>>j)&1 for j in range(5))))
                  for mask,n in clients if (mask>>a)&1)
        assert price<=u[5]
        prices.append(str(F(u[5]-price,60*scale)))
    forced=[]
    prefix=tuple(range(4))
    for a in range(12):
        replies=[payoff60(prefix+(a,b),5) for b in range(12)]
        best=max(replies)
        br=[b for b,z in enumerate(replies) if z==best]
        first=[payoff60(prefix+(a,b),4) for b in br]
        forced.append(dict(action=a,last_best_replies=br,
                           source_min=str(F(min(first),60*scale)),
                           source_max=str(F(max(first),60*scale)),
                           guaranteed_gain=str(F(min(first)-u[4],60*scale))))
    assert all(F(forced[a]['guaranteed_gain'])>0 for a in range(6,12))
    report=dict(status='OPEN',scope='static implication failure; not an SPE',
                integer_customer_count=total,customer_types=len(clients),
                normalized_W=str(F(welfare,scale)),normalized_OPT6='1',
                normalized_copy_tax=str(F(copy60,60*scale)),
                potential_multisets_checked=checked,
                normalized_min_potential_slack=str(F(min_gap,60*scale)),
                potential_maximizer=maximizer,terminal_quote_slacks=prices,
                actual_payoffs=[str(F(v,60*scale)) for v in u],
                penultimate_deviations=forced)
    assert checked==12376
    print(json.dumps(report,indent=2))
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    main()
