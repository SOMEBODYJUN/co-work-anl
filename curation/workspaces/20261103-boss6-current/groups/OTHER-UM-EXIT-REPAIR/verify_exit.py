from fractions import Fraction as F
from importlib.util import spec_from_file_location, module_from_spec
from itertools import product, permutations
from pathlib import Path
from shutil import copyfile
import json
from tempfile import TemporaryDirectory

ROOT=Path('/workspace/scratch/c20ae848d8c2/p25-Boss2')
OUT=Path(__file__).resolve().parent
# Relocated dependencies are staged only for this targeted replay, without changing source.
with TemporaryDirectory(prefix='exit-replay-',dir=OUT) as staged_name:
    staged=Path(staged_name)
    copyfile(ROOT/'archives/unrelated-machines/tools/evidence/agent_um-20261101/private-group-exit-pool/private_group_exit_pool.py',staged/'private_group_exit_pool.py')
    copyfile(ROOT/'archives/unrelated-machines/tools/evidence/agent_um-20261101/batch3/shared_sink_joint_assignment.py',staged/'shared_sink_joint_assignment.py')
    spec=spec_from_file_location('norm_exit_targeted',staged/'private_group_exit_pool.py')
    norm=module_from_spec(spec);spec.loader.exec_module(norm)

def opt_and_loads(H,rows,private):
    actual=[list(row) for row in rows]
    for home,a,c in private:
        actual.append([a if h==home else None for h in range(H)]+[c])
    choices=[[i for i,p in enumerate(row) if p is not None] for row in actual]
    best=None; assignments=0
    for sigma in product(*choices):
        loads=[F() for _ in range(H+1)]
        for row,i in zip(actual,sigma):loads[i]+=row[i]
        peak=max(loads,default=F())
        if best is None or peak<best:best=peak
        assignments+=1
    return best, assignments

cases=[
 ('two-macros-one-home',1,[[F(3,4),None],[F(3,4),F(1,4)]],[],F(1),F(1,8),'SCHEDULE',[F(3,4),F(1,4)]),
 ('no-home-exits',0,[[F(1,4)],[F(1,2)]],[],F(1),F(1,8),'SCHEDULE',[F(3,4)]),
 ('home-only-overfull',1,[[F(3,4),None]]*2,[],F(1),F(1,8),'REJECT_TARGET',None),
 ('real-exit-exceeds-budget',1,[[F(3,4),None],[None,F(9,4)]],[],F(1),F(1,8),'REJECT_TARGET',None),
 ('success-above-exact-target',1,[[F(3,4),None],[None,F(17,16)]],[],F(1),F(1,8),'SCHEDULE',[F(3,4),F(17,16)]),
 ('zero-target-many-macros',1,[[F(1),F(0)]]*2,[],F(0),F(1,8),'SCHEDULE',[F(0),F(0)]),
 ('forced-private-and-real-macro-exit',1,[[F(3,4),None],[None,F(1,4)]],[(0,None,F(1,8))],F(1),F(1,8),'SCHEDULE',[F(3,4),F(3,8)]),
 ('mature-three-exit-fixture',1,[[F(1),F(1,16)]]*3,[(0,F(1),None)],F(1),F(1,8),'SCHEDULE',[F(1),F(3,16)]),
]
report=[]
for label,H,rows,private,T,eta,status,loads in cases:
    result=norm.solve_shared_sink_with_exits(H,rows,private,T,eta)
    exact,n=opt_and_loads(H,rows,private)
    assert result['status']==status,(label,result)
    if status=='SCHEDULE':
        assert result['loads']==loads,(label,result)
        assert len(result['assignment'])==len(rows)+len(private)
        assert norm.single_sink_loads(H,rows,private,result['assignment'])==loads
        assert all(v<=T for v in loads[:H]) and loads[H]<=(1+eta)*T
    else:
        assert exact>T
    if exact<=T:assert status=='SCHEDULE'
    report.append(dict(case=label,status=status,exact_OPT=str(exact),assignments_enumerated=n,
                       loads=None if loads is None else list(map(str,loads))))

costs=[[F(0),None,None],[F(0),F(1,4),F(1,4)],[F(0),F(0),F(0)]]
finite=[]
for sigma in permutations(range(3)):
    if all(costs[i][j] is not None for i,j in enumerate(sigma)):
        finite.append((sigma,sum((costs[i][j] for i,j in enumerate(sigma)),F())))
assert ((0,1,2),F(1,4)) in finite
assert min(value for _,value in finite)==F(1,4)
assert norm.base.minimum_assignment(costs) in [list(sigma) for sigma,value in finite if value==F(1,4)]

# A profile example keeps the b>h path and verifies actual, rather than virtual, sink costs.
pool=norm.solve_exit_pool(1,[[F(3,4),None],[F(3,4),F(1,8)]],[],[F(1),F(2)],F(1),F(1,8),F(1,4),
                         rho=F(1),pool_times=[None,[F(1,8),F(1,4)]])
assert pool['status']=='SCHEDULE'
assert pool['loads']==[F(3,4),F(1,8),F(0)]
assert pool['pool_work']==F(1,8)
report.append(dict(case='complete-profile-b-greater-than-h',status=pool['status'],loads=list(map(str,pool['loads'])),
                   pool_work=str(pool['pool_work']),factor=str(pool['factor'])))
(OUT/'verification.json').write_text(json.dumps(dict(method='Exact Fraction; targeted source replay and separate full original-assignment enumeration',
    limitation='Only the listed fixtures; no new whole-domain or full-suite claim',cases=report,
    two_macro_perfect_matchings=[dict(columns=list(sigma),cost=str(value)) for sigma,value in finite]),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(cases=len(report),two_macro_cost=str(F(1,4)),two_macro_loads=['3/4','1/4'],
    report=str(OUT/'verification.json')),ensure_ascii=False))
