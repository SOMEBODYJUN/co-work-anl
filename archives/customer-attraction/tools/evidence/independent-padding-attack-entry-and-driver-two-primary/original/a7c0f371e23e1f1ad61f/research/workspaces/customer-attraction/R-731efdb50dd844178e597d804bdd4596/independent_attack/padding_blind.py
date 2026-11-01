"""Blind finite reconstruction of the supplied six-topic padding statement."""
from pathlib import Path
import sys,json
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver
def game(k):
    d={1:4,2:4,4:2,12:2,20:2,25:6,26:2,32:5*k}
    return Instance(tuple('ABTDEP'),tuple(CustomerType(frozenset(i for i in range(6) if mask>>i&1),r) for mask,r in d.items()),k+3)
def run(k):
    g=game(k);s=ExactSPESolver(g);q=(2,1,0,0,0,k)
    print('k',k,'start',flush=True)
    feasible=q in s.outcomes();print('k',k,'target',feasible,'stats',s.stats,flush=True)
    for a in range(5):
        b=tuple(int(i==a) for i in range(6));r=s.outcomes(b);v=min(s._utility(t,a) for t in r)
        choices=[t for t in r if s._utility(t,a)==v]
        print('child',a,'minimum',str(v),'outcomes',choices[:12],flush=True)
    return feasible
if __name__=='__main__':run(int(sys.argv[1]))
