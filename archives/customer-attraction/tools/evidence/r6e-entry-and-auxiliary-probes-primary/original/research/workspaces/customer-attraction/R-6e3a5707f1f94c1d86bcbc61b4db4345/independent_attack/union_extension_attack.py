"""Test missed-union <= actual welfare in fixed complete-history SPE cones.

Floating LP proposes only. A positive witness is recovered and checked over
integer customer clones and the canonical complete-history verifier.
"""
from __future__ import annotations
import importlib.util, itertools, json, math, sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT))
source=ROOT/'tests/audits/customer_attraction_strategy_lp.py'
spec=importlib.util.spec_from_file_location('cone_audit',source)
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
from customer_attraction import Instance,CustomerType,StrategyCertificate,verify_certificate

def attack(path):
    obj=json.loads(path.read_text())
    if 'actions' not in obj or not isinstance(obj['actions'],list):return None
    if not obj['actions'] or not all(isinstance(x,dict) and 'history' in x and 'action' in x for x in obj['actions']):return None
    actions={tuple(x['history']):x['action'] for x in obj['actions']}
    m=max(map(len,actions))+1
    p=max([a for h,a in actions.items()]+[a for h in actions for a in h])+1
    if p>7 or m>5:return None
    cone=module.StrategyCone(p,m,actions)
    covered=np.array(cone.welfare,dtype=float)
    comparison=list(itertools.combinations(range(p),min(m,p)))
    best=None
    for J in comparison:
        objective=np.array(module.coverage_row(p,J),dtype=float)*(1-covered)
        lp=linprog(-objective,A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),
                   A_eq=[covered],b_eq=[1],bounds=(0,None),method='highs')
        if not lp.success:continue
        val=float(-lp.fun)
        if best is None or val>best['proposal']+1e-9:
            values=tuple(F(float(x)).limit_denominator(10**7) for x in lp.x)
            if not cone.verify(values) or module.dot(cone.welfare,values)!=1:
                values=cone.recover_vertex(lp.x)
            exact=None
            if values is not None and cone.verify(values) and module.dot(cone.welfare,values)==1:
                exact=module.dot(tuple(F(int(x)) for x in objective),values)
            best={'source':str(path.relative_to(ROOT)),'players':m,'topics':p,
                  'comparison':J,'proposal':val,'exact_ratio':str(exact) if exact is not None else None}
            if exact is not None and exact>1:
                scale=math.lcm(*(x.denominator for x in values))
                clones=[int(v*scale) for v in values]
                inst=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if mask&(1<<a)),n)
                    for mask,n in enumerate(clones,1) if n),m)
                cert=StrategyCertificate(actions,cone.root)
                report=verify_certificate(inst,cert);report.assert_valid()
                witness={'scope':'auxiliary union-extension counterexample, not Q-CAG-HALF counterexample',
                         **best,'instance':inst.to_dict(),'strategy':cert.to_dict(),
                         'W':inst.welfare(cone.root),'OPT':inst.optimal_welfare(),
                         'verified_histories':report.checked_histories}
                (HERE/'union_extension_counterexample.json').write_text(json.dumps(witness,indent=2)+'\n')
                return best
    return best

if __name__=='__main__':
    records=[]
    for path in sorted((ROOT/'evidence/certificates/customer_attraction').glob('*.json')):
        result=attack(path)
        if result:
            records.append(result);print(json.dumps(result),flush=True)
            (HERE/'union_extension_run.json').write_text(json.dumps(records,indent=2)+'\n')
            if result['exact_ratio'] and F(result['exact_ratio'])>1:break
