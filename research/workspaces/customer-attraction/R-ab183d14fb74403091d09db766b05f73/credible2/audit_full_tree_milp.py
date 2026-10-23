"""Cross-check the union model against exhaustive complete two-topic policies.

For each full action map, a separate fixed-cone LP is optimized for every query.
This independently removes every binary disjunction before comparing the MIP.
Floating agreement is an implementation regression, never an exact theorem.
"""
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from full_tree_milp import Model, StrategyCone, enumerate_vertices


def audit(m,kind,custom=None):
    p=2;histories=[h for d in range(m) for h in product(range(p),repeat=d)]
    maps=[]
    for values in product(range(p),repeat=len(histories)-1):
        actions=dict(zip(histories,(0,)+values));maps.append(StrategyCone(p,m,actions))
    records=[]
    for q in sorted({cone.root for cone in maps}):
        options={'queries':[(0,0)],'objective_rows':[custom]} if custom is not None else {}
        model=Model(p,m,q,0,kind,root_hull=True,**options);brute=-1e100;lp_count=0
        for cone in maps:
            if cone.root!=q:continue
            for objective in model.objectives:
                out=linprog(-np.array(objective,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),
                            A_eq=[np.ones((1<<p)-1)],b_eq=[1],bounds=(0,None),method='highs')
                if not out.success:raise AssertionError('zero/common type should make every policy cone nonempty')
                brute=max(brute,-out.fun);lp_count+=1
        result=model.solve(20)
        if result['status']!=0 or abs(result['floating_gap']-brute)>2e-6:raise AssertionError((q,brute,result))
        records.append({'root':q,'complete_maps':sum(cone.root==q for cone in maps),'independent_LPs':lp_count,
                        'brute_float':brute,'MIP_float':result['floating_gap'],'agreement':True})
    return {'p':p,'m':m,'kind':kind,'custom_objective':custom,'total_ordered_policy_maps_with_root_action_0':len(maps),'records':records}


if __name__=='__main__':
    results=[audit(m,kind) for m in (2,3) for kind in ('tstar','price_plus_u')]
    # Nonzero extrema catch a spurious restriction to the all-common type or a
    # missing incentive row that the zero sharp targets alone would not expose.
    results += [audit(m,'custom',c) for m in (2,3) for c in ((1,-1,-1),(-1,1,-1))]
    output={'scope':'finite implementation regression; no universal mathematical certification','results':results,'passed':True}
    path=Path(__file__).with_name('full_tree_milp_audit.json');path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
