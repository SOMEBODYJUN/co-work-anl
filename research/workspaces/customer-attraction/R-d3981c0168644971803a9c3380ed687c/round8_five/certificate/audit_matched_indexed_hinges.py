"""Independent original-history replay of the 161 matched-indexed hinges.

The direct side uses original topics, full ordered histories and terminal
utilities. It does not call the target hinge/scalar implementation.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json,sys,hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'maxroot'))
import indexed_hinge_pricing as target
sys.path.insert(0,str(target.cm.ROOT))
from customer_attraction import Instance, ExactSPESolver


def check(sets):
    topics=tuple(frozenset(s) for s in sets);clients=set().union(*topics)
    solver=ExactSPESolver(Instance.from_topic_sets(topics,5));chosen=min(solver.worst_outcomes())
    sigma=solver.certificate(chosen,action_selector=lambda h,a:a[sum((j+1)*v for j,v in enumerate(h))%len(a)]).actions
    def finish(h):
        while len(h)<5:h=h+(sigma[h],)
        return h
    def util(path,i):return sum((F(1,sum(x in topics[t] for t in path)) for x in topics[path[i]]),F(0))
    ic=0
    for depth in range(5):
        for h in product(range(len(topics)),repeat=depth):
            for q in range(len(topics)):
                assert util(finish(h),depth)>=util(finish(h+(q,)),depth);ic+=1
    actual=finish(());A,B,C,D,E=actual;second=finish((A,E));third=finish((A,B,E))
    labels=dict(zip(target.cm.mp.LABELS,(*actual,*second[2:],*third[3:])))
    opt=max(combinations_with_replacement(range(len(topics)),5),key=lambda ts:len(set().union(*(topics[t] for t in ts))))
    branches={'AB':[finish((A,B,q)) for q in opt],
              'AE':[finish((A,E,q)) for q in opt],
              'Sbranch':[finish((A,q)) for q in opt]}
    menus={tag:{m:tuple(path[pos] for path in branches[tag])
                 for m,pos in zip(target.cm.mp.MENUS[tag],(3,4) if tag!='Sbranch' else (2,3,4))}
           for tag in branches}
    compressed={n:F(0) for n,*_ in target.SPECS}
    for x in clients:
        bit=lambda t:int(x in topics[t]);atom={'bits':''.join(str(bit(labels[t])) for t in target.cm.mp.LABELS)}
        for tag,field in target.cm.mp.FIELDS.items():
            types=list(product((0,1),repeat=4 if tag=='Sbranch' else 3));hist=[0]*len(types)
            for i,t in enumerate(opt):
                typ=(bit(t),)+tuple(bit(menus[tag][m][i]) for m in target.cm.mp.MENUS[tag]);hist[types.index(typ)]+=1
            atom[field]=hist
        for n,v in target.rows(atom).items():compressed[n]+=v
    source_histories=0
    for name,tag,pos,menu,c in target.SPECS:
        nodepos=(1 if tag=='Sbranch' else 2)+pos;k=5-nodepos;L=4*(k-1)
        direct=F(0)
        for path in branches[tag]:
            direct+=5*L*util(path,nodepos);source_histories+=1
            for x in clients:
                p=sum(x in topics[t] for t in path[:nodepos])
                d=sum(x in topics[t] for t in opt)
                j=sum(x in topics[t] for t in menus[tag][menu])
                direct-=c*F(j,p+k)+F(d,p+1)
                numerator=(k-1)*d-5*(L-1-c)*(p+1)
                direct+=max(F(0),numerator)/((p+1)*(p+k))
        assert direct==compressed[name],(name,direct,compressed[name])
        assert direct>=0,(name,direct)
    return {'topics':[sorted(t) for t in topics],'actual':actual,'full_ordered_history_IC':ic,
            'rows':len(compressed),'original_source_histories_used':source_histories,
            'minimum_exact_slack':str(min(compressed.values()))}


if __name__=='__main__':
    cases=[check(sets) for sets in [[set()],[set(),{0},{0,1},{1,2}],
                                   [set(range(5)),{5},{6},{7},{8}],
                                   [{0,1},{1,2},{0,2,3},{3,4},{0,2,4}]]]
    report={'status':'passed','scope':__doc__,'cases':cases,
            'full_ordered_history_IC':sum(c['full_ordered_history_IC'] for c in cases),
            'original_source_histories_used':sum(c['original_source_histories_used'] for c in cases),
            'target_code_sha256':hashlib.sha256(Path(target.__file__).read_bytes()).hexdigest()}
    (HERE/'audit_matched_indexed_hinges.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
