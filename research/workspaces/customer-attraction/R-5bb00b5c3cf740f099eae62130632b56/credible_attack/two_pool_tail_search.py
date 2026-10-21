"""Exact integer BI for a three-mover tail of the two-pool star candidate.

Three old groups C and one fresh group, with A_i=X_i+a_i,
B_ir=X_i+b_r, C_i=X_i, D_r=b_r+d_r. All pools disjoint.
This is a necessary tail condition, not a full initial-game SPE search.
"""
from itertools import product
from pathlib import Path
import json
import numpy as np


def coefficient_tables(old_groups=3):
    k = old_groups + 1
    topics = [(i, kind) for i in range(k) for kind in range(4)] + [(None, 0), (None, 1)]
    p = len(topics)
    # kinds A,B1,B2,C. Last labels D1,D2. The common multiplier
    # 12 clears every possible load (old 1 plus at most 3 movers).
    coeff = np.zeros((3,p,p,p,6), dtype=np.int16)
    for root, nxt, last in product(range(p), repeat=3):
        path=(root,nxt,last)
        group_load = [int(i < old_groups) for i in range(k)]
        acount = [0]*k
        bcount = [0,0]
        dcount = [0,0]
        for t in path:
            i,kind=topics[t]
            if i is None:
                bcount[kind]+=1
                dcount[kind]+=1
            else:
                group_load[i]+=1
                if kind==0: acount[i]+=1
                if kind in (1,2): bcount[kind-1]+=1
        for pos,t in enumerate(path):
            i,kind=topics[t]
            row=coeff[pos,root,nxt,last]
            if i is not None:
                row[0]=12//group_load[i]
                if kind==0: row[1]=12//acount[i]
                if kind in (1,2): row[2+2*(kind-1)]=12//bcount[kind-1]
            else:
                row[2+2*kind]=12//bcount[kind]
                row[3+2*kind]=12//dcount[kind]
    return topics,coeff


def test_parameters(parameters, tables):
    topics,coeff=tables
    pars=np.asarray(parameters,dtype=np.int64)
    values=np.einsum('rabcv,nv->rnabc',coeff,pars,optimize=True)
    root,nextv,last=values
    best_last=last.max(axis=-1,keepdims=True)
    last_ok=last==best_last
    next_min=np.where(last_ok,nextv,10**12).min(axis=-1)
    next_floor=next_min.max(axis=-1)
    next_ok=last_ok & (nextv>=next_floor[:,:,None,None])
    root_min=np.where(next_ok,root,10**12).min(axis=(-1,-2))
    root_floor=root_min.max(axis=-1)
    fresh_c=len(topics)-3
    d1,d2=len(topics)-2,len(topics)-1
    tail_ok=next_ok[:,fresh_c,d1,d2]
    root_ok=root_floor<=12*pars[:,0]
    return root_ok & tail_ok,root_floor,tail_ok


def main():
    tables=coefficient_tables(3)
    survivors=[]
    eligible=0
    checked=0
    # Search is deterministic. x=6, a=4 is the first targeted 5/3 row.
    # Pool sizes 0..18 include asymmetric terminal supports and zero blocks.
    params=[(6,4,b1,d1,b2,d2) for b1,d1,b2,d2 in product(range(19),repeat=4)
            if 2*(b2+d2)>=6+b1 and d2>=3]
    for start in range(0,len(params),128):
        batch=params[start:start+128]
        ok,floor,tail=test_parameters(batch,tables)
        checked+=len(batch)
        eligible+=int(tail.sum())
        for i in np.flatnonzero(ok):
            survivors.append({'parameters':batch[i], 'root_floor_times_12':int(floor[i])})
    out={'scope':'necessary final-C three-mover tail, not complete initial-game SPE',
         'old_groups':3,'fresh_groups':1,'x':6,'a':4,'pool_range':[0,18],
         'parameter_order':['x','a','b1','d1','b2','d2'],
         'pre_filter':'actual last D2 vs B1 and B2',
         'prefilter_pass':len(params),'exact_BI_checked':checked,
         'actual_D1_D2_tail_supported':eligible,'survivors':survivors}
    path=Path(__file__).with_name('two_pool_tail_search.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='survivors'},indent=2))
    print('survivors',len(survivors),survivors[:5])


if __name__=='__main__': main()
