"""两种森林边界舍入实现的独立全分配交叉核验。"""
from fractions import Fraction as F
from random import Random
from pathlib import Path
from contextlib import redirect_stdout
import importlib.util,io,runpy,json
base=Path(__file__).resolve().parents[3]
with redirect_stdout(io.StringIO()):
    down=runpy.run_path(str(base/'tests/audits/unrelated_machines/forest_boundary_downward.py'))
spec=importlib.util.spec_from_file_location('forest_up',base/'tests/audits/unrelated_machines/forest_boundary_upward.py')
up=importlib.util.module_from_spec(spec);spec.loader.exec_module(up)
rng=Random(671244)
counts={'cases':0,'exact_feasible':0,'down_returned':0,'up_returned':0,'different_success_status':0,'different_root_load':0,'disconnected_support_cases':0}
for case in range(600):
    nv=rng.randrange(6)
    real_parent={v:rng.randrange(v) for v in range(1,nv+1) if rng.randrange(3)}
    parent={v:real_parent.get(v,0) for v in range(1,nv+1)}
    jobs=[]
    for v,p in real_parent.items():
        for _ in range(rng.randrange(1,3)):
            jobs.append({v:F(rng.randrange(6),rng.randrange(1,7)),p:F(rng.randrange(6),rng.randrange(1,7))})
    for v in range(nv+1):
        if rng.randrange(2):jobs.append({v:F(rng.randrange(5),rng.randrange(1,7))})
    T=F(rng.randrange(7),rng.randrange(1,7));eta=rng.choice([F(1),F(1,2),F(1,5)])
    exact,_=up.brute(nv+1,jobs,0,[T]*(nv+1))
    d=down['compress'](parent,jobs,T,eta)
    u=up.boundary_oracle(nv+1,jobs,0,T,eta)
    counts['cases']+=1;counts['exact_feasible']+=exact is not None
    counts['disconnected_support_cases']+=len(real_parent)<nv
    for name,out in [('down',d),('up',u)]:
        counts[name+'_returned']+=out is not None
        if out is None:assert exact is None
        else:
            b,a,_=out
            if exact is not None:assert b<=exact
            if isinstance(a,dict):a=tuple(a[j] for j in range(len(jobs)))
            loads=up.load_vector(nv+1,jobs,a)
            assert b==loads[0] and all(x<=(1+eta)*T for x in loads[1:])
    counts['different_success_status']+=(d is None)!=(u is None)
    counts['different_root_load']+=d is not None and u is not None and d[0]!=u[0]
print(json.dumps({'seed':671244,'arithmetic':'Fraction/integer','cross_comparison':counts},indent=2))
