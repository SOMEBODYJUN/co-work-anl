"""Reproduce and retain all 1365 shared-B necessary-LP mode values.
Also verifies the stored rational 67/136 primal point against every model row.
This is an exact failure certificate for these necessary rows, not an SPE.
"""
import importlib.util,json,time
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
BASE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('fullprefix',BASE/'probe_shared_bc_tail_fullprefix.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def matrix(pattern):
    types,eq,ub,br=m.model(4,1)
    pairs=[(a,y) for a,y in product(range(4),repeat=2) if a!=y]
    rows=list(ub);rhs=[1.0]*5
    for j,k in enumerate(pattern):
        a,y=pairs[k];rs,bs,ns,*_=br[j,a,y]
        rows.extend(rs);rhs.extend(bs)
    return types,eq,rows,rhs

def run():
    types,eq,ub,br=m.model(4,1)
    pairs=[(a,y) for a,y in product(range(4),repeat=2) if a!=y]
    records=[];start=time.perf_counter()
    for pattern in combinations_with_replacement(range(12),4):
        rows=list(ub);rhs=[1.0]*5
        for j,k in enumerate(pattern):
            a,y=pairs[k];rs,bs,ns,*_=br[j,a,y];rows.extend(rs);rhs.extend(bs)
        obj=np.zeros(len(types)+1);obj[-1]=1
        z=linprog(obj,A_ub=np.array(rows),b_ub=np.array(rhs),A_eq=np.array(eq),b_eq=np.ones(6),bounds=[(0,None)]*(len(types)+1),method='highs')
        records.append({'pair_indices':list(pattern),'status':int(z.status),'gamma':float(z.fun) if z.success else None})
    bad=[r for r in records if r['gamma'] is not None and r['gamma']<.5-1e-8]
    result={'scope':'All 1365 pair multisets; float route diagnosis only; no lower-bound proof.',
        'pairs':pairs,'records':records,'below_half_patterns':bad,'patterns':len(records),
        'elapsed_seconds':time.perf_counter()-start}
    (BASE/'shared-B-fullprefix-1365-mode-index.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
    source=json.loads((BASE/'probe-shared-B-fullprefix-all-output.json').read_text())['best']
    pattern=tuple(pairs.index(tuple(v)) for v in source['pattern'])
    types,eq,rows,rhs=matrix(pattern)
    masses={(a['block'],tuple(a['bits'])):F(a['mass']).limit_denominator(1000000) for a in source['atoms']}
    x=[masses.get(v,F(0)) for v in types]+[F(67,136)]
    slacks=[]
    for row,b in zip(rows,rhs):
        value=F(b).limit_denominator(60)-sum((F(float(a)).limit_denominator(60)*v for a,v in zip(row,x)),F())
        assert value>=0
        slacks.append(str(value))
    for row in eq:
        assert sum((F(float(a)).limit_denominator(60)*v for a,v in zip(row,x)),F())==1
    cert={'scope':'Exact rational primal feasibility for every necessary LP row; not original-model SPE.',
        'pair_indices':pattern,'gamma':'67/136','variables':[str(v) for v in x],
        'row_slacks':slacks,'minimum_slack':str(min(map(F,slacks))),'inequality_rows':len(rows),'equality_rows':len(eq)}
    (BASE/'shared-B-67-136-necessary-row-certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({'patterns':len(records),'below_half_patterns':bad,'exact_point_rows':len(rows),'exact_point_minimum_slack':cert['minimum_slack']},indent=2))

if __name__=='__main__':run()
