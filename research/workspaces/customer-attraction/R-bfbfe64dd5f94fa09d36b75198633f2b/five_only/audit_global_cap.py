"""Direct unit-client replay of GAP5, including every ordered history.

Uses the canonical solver only to obtain complete SPE witnesses. Recomputes
all payoffs and one-step comparisons from unit sets independently. Finite
regression validates implementation, not the universal lemma or HALF(5).
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import sys,json,hashlib,platform
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').exists())
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,ExactSPESolver

def check(themes):
    themes=tuple(frozenset(s) for s in themes);customers=set().union(*themes)
    inst=Instance.from_topic_sets(themes,5);sol=ExactSPESolver(inst)
    target=min(sol.worst_outcomes())
    cert=sol.certificate(target,action_selector=lambda h,a:a[sum((i+1)*x for i,x in enumerate(h))%len(a)])
    actions=cert.actions
    def finish(h):
        while len(h)<5:h=h+(actions[h],)
        return h
    def payoff(z,i):
        return sum((F(1,sum(x in themes[a] for a in z)) for x in themes[z[i]]),F(0))
    actual=finish(());uj=[payoff(actual,j) for j in range(5)];L=max(map(len,themes))
    assert all(5*u>=L for u in uj)
    ic=rows=0;minimum=None
    for depth in range(5):
        for h in product(range(len(themes)),repeat=depth):
            z=finish(h);u=payoff(z,depth)
            for a in range(len(themes)):
                assert u>=payoff(finish(h+(a,)),depth)
                ic+=1
            k=5-depth
            if k<2:continue
            b={x:sum(x in themes[a] for a in h) for x in customers}
            A=4*(k-1);aa=2*A+k*k
            for C,D in product(themes,repeat=2):
                s=sum((F(1,b[x]+k) for x in C),F(0))
                f=sum((F(1,b[x]+k) for x in C&D),F(0))+sum((F(1,b[x]+1) for x in D-C),F(0))
                for src in uj:
                    gap=2*A*u+5*k*src-(aa-2)*s-2*f
                    assert gap>=0,(h,C,D,src,gap)
                    rows+=1;minimum=gap if minimum is None else min(minimum,gap)
    return {'themes':[sorted(s) for s in themes],'actual':actual,'actual_utilities':list(map(str,uj)),
            'full_IC_comparisons':ic,'GAP5_rows':rows,'minimum_GAP5_slack':str(minimum)}

if __name__=='__main__':
    data=[check(x) for x in [
        [set()],
        [set(),{0},{0,1},{1,2}],
        [set(range(5)),{5},{6},{7},{8}],
        [{0,1},{1,2},{0,2,3},{3,4},{0,2,4}],
        [{0,2},{0,3},{1,2},{1,3}],
    ]]
    result={'status':'passed','scope':__doc__,'python':platform.python_version(),'cases':data,
            'total_IC':sum(c['full_IC_comparisons'] for c in data),'total_GAP5_rows':sum(c['GAP5_rows'] for c in data)}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
