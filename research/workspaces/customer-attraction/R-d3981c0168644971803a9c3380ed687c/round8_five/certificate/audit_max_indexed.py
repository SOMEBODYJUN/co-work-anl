"""Original unit-client/history replay, with independent pair expansion.

Finite implementation audit only. The general necessity proof is in
max_indexed_coupling.md and the cited original tail theorems.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json, sys, hashlib
import max_indexed_coupling as cm
sys.path.insert(0,str(cm.ROOT))
from customer_attraction import Instance, ExactSPESolver


def check(sets):
    topics=tuple(frozenset(s) for s in sets);clients=set().union(*topics)
    solver=ExactSPESolver(Instance.from_topic_sets(topics,5))
    target=min(solver.worst_outcomes())
    sigma=solver.certificate(target,action_selector=lambda h,a:a[sum((j+1)*t for j,t in enumerate(h))%len(a)]).actions
    def finish(h):
        while len(h)<5:h=h+(sigma[h],)
        return h
    def util(z,i):
        return sum((F(1,sum(x in topics[t] for t in z)) for x in topics[z[i]]),F(0))
    ic=0
    for depth in range(5):
        for h in product(range(len(topics)),repeat=depth):
            for q in range(len(topics)):
                assert util(finish(h),depth)>=util(finish(h+(q,)),depth)
                ic+=1
    actual=finish(());A,B,C,D,E=actual
    second=finish((A,E));third=finish((A,B,E))
    labels=dict(zip(cm.mp.LABELS,(*actual,*second[2:],*third[3:])))
    optimum=max(combinations_with_replacement(range(len(topics)),5),key=lambda z:len(set().union(*(topics[t] for t in z))))
    branches={'AB':[finish((A,B,q)) for q in optimum],
              'AE':[finish((A,E,q)) for q in optimum],
              'Sbranch':[finish((A,q)) for q in optimum]}
    menus={g:{'opt':optimum,**{m:tuple(z[pos] for z in branches[g])
                               for m,pos in zip(cm.mp.MENUS[g],(3,4) if g!='Sbranch' else (2,3,4))}}
           for g in branches}
    maximum=max(range(len(topics)),key=lambda t:len(topics[t]));mz=finish((maximum,))
    compressed={s[0]:F(0) for s in cm.SPECS}
    for x in clients:
        bit=lambda t:int(x in topics[t])
        atom={'bits':''.join(str(bit(labels[t])) for t in cm.mp.LABELS)}
        for g,field in cm.mp.FIELDS.items():
            ty=cm.mp.TYPES[4 if g=='Sbranch' else 3];hist=[0]*len(ty)
            for j,t in enumerate(optimum):
                state=(bit(t),)+tuple(bit(menus[g][m][j]) for m in cm.mp.MENUS[g])
                hist[ty.index(state)]+=1
            atom[field]=hist
        for n,v in cm.coupled_rows(atom,tuple(bit(t) for t in mz)).items():compressed[n]+=v
    raw_pairs=0;raw_tuples=0;checked=0
    for name,g,kind,i,c,d in cm.SPECS:
        def query(t):
            if t in menus[g]:return menus[g][t]
            if t.startswith('z'):return (mz[int(t[1:])],)
            return (labels[t],)
        cs=query(c)
        if kind=='Tuple':
            rem=i;n,qs=d;prefix=mz[:5-rem]
            p={x:sum(x in topics[t] for t in prefix) for x in clients}
            beta=F(5,3) if rem==3 else F(1499,750)
            tail=sum((util(mz,j) for j in range(5-rem,5)),F(0))
            rho=sum((cm.mj.RHOMIN[int(x in topics[mz[0]]),tuple(int(x in topics[t]) for t in mz[1:])] for x in clients),F(0)) if rem==4 else F(0)
            value=F(0)
            for q in cs:
                choices=(q,)*n+tuple(mz[j] for j in qs)
                comparison=F(0)
                for x in clients:
                    e=sum(x in topics[t] for t in choices)
                    if e:comparison+=F(e,p[x]+e)
                gap=beta*tail-comparison-rho
                assert gap>=0,(name,choices,gap)
                value+=gap;raw_tuples+=1
        else:
            prefix=mz[:i];k=5-i;u=util(mz,i)
            p={x:sum(x in topics[t] for t in prefix) for x in clients}
            value=F(0)
            if kind=='K':
                for q in cs:
                    gap=u-sum((F(1,p[x]+k) for x in topics[q]),F(0))
                    assert gap>=0,(name,q,gap)
                    value+=gap;raw_pairs+=1
            else:
                ds=query(d)
                h=util(mz,3)+util(mz,4)+sum((F(1,(p[x]+1)*(p[x]+2)) for x in topics[mz[3]]),F(0)) if kind=='Tax' else None
                for q,r in product(cs,ds):
                    Q,R=topics[q],topics[r]
                    if kind=='AP':
                        a=cm.mp.aa(k)
                        cost=(a-2)*sum((F(1,p[x]+k) for x in Q),F(0))
                        cost+=2*sum((F(1,p[x]+k) for x in Q&R),F(0))
                        cost+=2*sum((F(1,p[x]+1) for x in R-Q),F(0))
                        gap=a*u-cost
                    else:
                        comparison=sum((F(int(x in Q)+int(x in R),p[x]+int(x in Q)+int(x in R)) for x in Q|R),F(0))
                        gap=h-comparison
                    assert gap>=0,(name,q,r,gap)
                    value+=gap;raw_pairs+=1
        assert value==compressed[name],(name,value,compressed[name])
        checked+=1
    return {'themes':[sorted(t) for t in topics],'actual':actual,'maximum_true_path':mz,
            'full_ordered_history_IC':ic,'rows':checked,'expanded_legal_pairs':raw_pairs,
            'expanded_legal_tuples':raw_tuples,'minimum_exact_slack':str(min(compressed.values()))}


if __name__=='__main__':
    cases=[check(sets) for sets in [[set()],[set(),{0},{0,1},{1,2}],
                                   [set(range(5)),{5},{6},{7},{8}],
                                   [{0,1},{1,2},{0,2,3},{3,4},{0,2,4}]]]
    report={'status':'passed','scope':__doc__,'cases':cases,
            'total_full_ordered_history_IC':sum(c['full_ordered_history_IC'] for c in cases),
            'total_expanded_pairs':sum(c['expanded_legal_pairs'] for c in cases),
            'total_expanded_tuples':sum(c['expanded_legal_tuples'] for c in cases),
            'audited_code_sha256':hashlib.sha256((cm.HERE/'max_indexed_coupling.py').read_bytes()).hexdigest()}
    (cm.HERE/'audit_max_indexed.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
