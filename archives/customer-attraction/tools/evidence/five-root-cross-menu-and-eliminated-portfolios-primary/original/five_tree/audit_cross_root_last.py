"""Independent direct IC expansion versus histogram coefficient on full SPEs.

Selected witnesses verify implementation/semantics only, not HALF(5).
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json, sys, hashlib
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(HERE))
from customer_attraction import Instance, ExactSPESolver
from cross_root_last import row

def check(sets):
    themes=tuple(frozenset(s) for s in sets); customers=set().union(*themes)
    solver=ExactSPESolver(Instance.from_topic_sets(themes,5))
    target=min(solver.worst_outcomes())
    sigma=solver.certificate(target,action_selector=lambda h,a:a[sum((i+1)*x for i,x in enumerate(h))%len(a)]).actions
    def finish(h):
        while len(h)<5:h=h+(sigma[h],)
        return h
    def u(z,i):
        return sum((F(1,sum(x in themes[t] for t in z)) for x in themes[z[i]]),F())
    comparisons=0
    for depth in range(5):
        for h in product(range(len(themes)),repeat=depth):
            for t in range(len(themes)):
                assert u(finish(h),depth)>=u(finish(h+(t,)),depth)
                comparisons+=1
    actual=finish(());A=actual[0]
    opt=max(combinations_with_replacement(range(len(themes)),5),key=lambda z:len(set().union(*(themes[t] for t in z))))
    roots=[finish((t,)) for t in opt]; seconds=[finish((A,t)) for t in opt]
    direct=F()
    for ri in roots:
        for sj in seconds:
            gap=u(ri,4)-u(ri[:4]+(sj[-1],),4)
            assert gap>=0
            direct+=gap
    compressed=F()
    for x in customers:
        atom={'root_hist':[0]*32,'second_hist':[0]*16}
        for z in roots:
            idx=0
            for t in z:idx=2*idx+int(x in themes[t])
            atom['root_hist'][idx]+=1
        for z in seconds:
            idx=0
            for t in z[1:]:idx=2*idx+int(x in themes[t])
            atom['second_hist'][idx]+=1
        compressed+=row(atom)
    assert compressed==direct
    return {'themes':[sorted(t) for t in themes],'actual':actual,'full_ordered_IC':comparisons,
            'expanded_new_last_IC':25,'compressed_equals_direct':True,'new_slack':str(direct)}

if __name__=='__main__':
    cases=[check(sets) for sets in [[set()],[set(),{0},{0,1},{1,2}],
           [set(range(5)),{5},{6},{7},{8}],[{0,1},{1,2},{0,2,3},{3,4},{0,2,4}]]]
    report={'scope':__doc__,'status':'passed','new_source_sha256':hashlib.sha256((HERE/'cross_root_last.py').read_bytes()).hexdigest(),
            'cases':cases,'total_full_ordered_IC':sum(c['full_ordered_IC'] for c in cases),
            'total_expanded_new_IC':sum(c['expanded_new_last_IC'] for c in cases)}
    (HERE/'audit_cross_root_last.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
