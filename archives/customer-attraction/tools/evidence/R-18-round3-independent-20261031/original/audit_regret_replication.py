"""Independent unit-customer tree audit of the replicated four-client gadget.

No imports from the author's audit, model, solver, or certificate verifier.
Every ordered history is visited with an explicit canonical/BI mode. Entering
BI mode is permanent, so coincidentally good descendant counts never re-enter
the hand-designed protocol. General k rests on the mathematical review.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

STATES={(0,0,0):'E',(0,1,0):'Y',(1,1,0):'XY',(0,0,1):'Z',(0,0,2):'ZZ'}

def audit(k):
    m,p=2*k,3*k
    themes=[]
    for j in range(k):
        a,b,c,d=range(4*j,4*j+4)
        themes.extend([frozenset((a,b)),frozenset((c,d)),frozenset((b,c,d))])
    def utilities(h):
        loads=[sum(x in themes[a] for a in h) for x in range(4*k)]
        return tuple(sum((F(1,loads[x]) for x in themes[a]),F(0)) for a in h)
    nodes=comparisons=0
    actions={}
    def walk(h,mode):
        nonlocal nodes,comparisons
        if len(h)==m:return h
        counts=[tuple(h.count(3*j+a) for a in range(3)) for j in range(k)]
        labels=[STATES.get(q) for q in counts]
        if mode:
            assert all(x is not None for x in labels)
            assert m-len(h)==2*labels.count('E')+labels.count('Y')+labels.count('Z')
            phase=next(x for x in ('E','Y','Z') if x in labels)
            block=labels.index(phase)
            choice=3*block+{'E':1,'Y':0,'Z':2}[phase]
        terminals=[]
        for action in range(p):
            child=h+(action,)
            good=all(tuple(child.count(3*j+a) for a in range(3)) in STATES for j in range(k))
            terminals.append(walk(child,mode and good))
        pay=[utilities(t)[len(h)] for t in terminals]
        if not mode:choice=max(range(p),key=lambda a:(pay[a],-a))
        assert pay[choice]==max(pay),(k,h,mode,choice,pay)
        nodes+=1;comparisons+=p
        actions[h]=choice
        return terminals[choice]
    terminal=walk((),True)
    expected=tuple(3*j+1 for j in range(k))+tuple(3*j for j in range(k))
    assert terminal==expected,(terminal,expected)
    base=utilities(terminal);assert base==(F(2),)*m
    regret=[]
    for i in range(m):
        best=max(utilities(terminal[:i]+(a,)+terminal[i+1:])[i] for a in range(p))
        regret.append(max(F(0),best-base[i]))
    assert regret==( [F(1,2)]*k+[F(0)]*k )
    return {'k':k,'ordered_nodes':nodes,'all_action_comparisons':comparisons,
            'actual_path':terminal,'utilities':list(map(str,base)),
            'regrets':list(map(str,regret)),'total_regret':str(sum(regret))}

if __name__=='__main__':
    result={'independent':True,'results':[audit(k) for k in (1,2)],
            'scope':'Complete ordered trees for k=1,2; arbitrary k proved by symbolic phase reasoning in review.'}
    path=Path(__file__).with_suffix('.json')
    if path.exists():raise FileExistsError(path)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
