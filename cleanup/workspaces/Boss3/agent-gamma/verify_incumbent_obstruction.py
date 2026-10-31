"""Definition-level audit of the five-customer incumbent-value obstruction.
No import of canonical model, solver, or the exploratory LP code.
The all-k proof is the rational table and monotonic inequalities in the note;
these finite checks are regression evidence only.
"""
from fractions import Fraction as F
from itertools import product
TOPICS=({0,2},{1,2},{3,4})

def utility(action, b, final_two):
    # b counts fixed A players; final_two includes fixed P plus moving players.
    return sum((F(1,b*(x in TOPICS[0])+sum(x in TOPICS[t] for t in final_two)) for x in TOPICS[action]),F(0))

def check(k):
    last_actions={}
    for first in range(3):
        values=tuple(utility(last,k,(2,first,last)) for last in range(3))
        expected=(
            (F(2,k+2),1+F(1,k+2),F(1)),
            (F(1,k+1)+F(1,k+2),F(1,2)+F(1,k+2),F(1)),
            (F(2,k+1),1+F(1,k+1),F(2,3)),
        )[first]
        assert values==expected
        br=tuple(a for a in range(3) if values[a]==max(values))
        assert br==((1,),(2,),(1,))[first]
        last_actions[first]=br[0]
    first_values=tuple(utility(first,k,(2,first,last_actions[first])) for first in range(3))
    assert first_values==(F(1,k+1)+F(1,k+2),1+F(1,k+1),F(1))
    assert tuple(a for a in range(3) if first_values[a]==max(first_values))==(1,)
    assert utility(2,k,(2,1,2))==1
    final_values=tuple(utility(a,k+1,(2,a)) for a in range(3))
    assert final_values==(F(2,k+2),1+F(1,k+2),F(1))
    assert tuple(a for a in range(3) if final_values[a]==max(final_values))==(1,)
    assert utility(2,k+1,(2,1))==2
    assert F(1)<F(2,3)*2

if __name__=='__main__':
    ks=tuple(range(1,101))+(1000,10**6)
    for k in ks:check(k)
    print(f'PASS: all histories and payoff formulas for {len(ks)} positive background counts; ratio bridge 1 < 4/3.')
