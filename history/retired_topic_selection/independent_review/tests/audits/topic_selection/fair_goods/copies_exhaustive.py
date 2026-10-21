"""Exhaust all 3-agent, 4-type strict-order copy instances up to renaming types."""
import itertools as it
import json
from pathlib import Path
import numpy as np
from toy_checks import copies_allocations

orders=list(it.permutations(range(4)))
checked=0; minimum=81; worst=None
for copies in it.product([1,2],repeat=4):
    X=copies_allocations(copies,3)
    acceptable={}
    for agent in range(3):
        for oi,order in enumerate(orders):
            counts=np.cumsum(X[:,:,order],axis=2)
            good=np.all(counts[:,agent,None,:]>=counts-1,axis=(1,2))
            bits=sum(1<<int(k) for k in np.flatnonzero(good))
            acceptable[agent,oi]=bits
    for o2,o3 in it.product(range(24),repeat=2):
        good=acceptable[0,0]&acceptable[1,o2]&acceptable[2,o3]
        count=good.bit_count(); checked+=1
        if count<minimum:
            minimum=count;worst={'copies':copies,'rankings':[orders[0],orders[o2],orders[o3]],'count':count}
        if not good: raise AssertionError(worst)
result={'scope':'3 agents; <=4 non-universal types; arbitrary multiplicities 1 or 2; strict rankings, up to simultaneous type renaming',
        'profiles_checked':checked,'minimum_witness_count':minimum,'worst':worst,
        'all_instances_have_sd_ef1':True,'boundary':'finite theorem verified by exhaustive Python, no independent formal proof; universal copies cancel pairwise counts; weak orders follow by refining ties'}
Path(__file__).with_name('copies_exhaustive_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
