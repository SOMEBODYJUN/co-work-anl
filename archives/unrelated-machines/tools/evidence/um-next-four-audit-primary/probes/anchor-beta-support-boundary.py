"""One supplemental contract probe; original fixture audit/source is unchanged."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,argparse
p=argparse.ArgumentParser();p.add_argument('--origin',type=Path,required=True);a=p.parse_args()
path=a.origin/'tests/audits/unrelated_machines/anchor_deficiency_joint_rounding_audit.py'
s=importlib.util.spec_from_file_location('anchor_primary_contract_probe',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
# No anchors, two machines, one positive tiny job. All declared witness conditions hold.
p0=[[F(2)],[F(1,2)]];x=[[F(1,3)],[F(2,3)]];z=[[],[]];T=F(1);beta=F(2)
assert sum(row[0] for row in x)==1
assert all(0<=p0[i][0]<=beta*T and p0[i][0]*x[i][0]<=T for i in range(2))
try:m.round_witness(p0,[],T,F(0),beta,z,x,0)
except ValueError as e:
 assert str(e)=='Positive mass on a forbidden/pruned edge'
 result=dict(status='EXPECTED_WRAPPER_REJECTION',reason=str(e),input=dict(p=[['2'],['1/2']],anchors=[],T='1',alpha='0',beta='2',z=[[],[]],x=[['1/3'],['2/3']],d0=0),valid_declared_joint_witness=True,baseline_extra_condition='positive-support p<=T',interpretation='finitefixture wrapper does not implement the entire theoretical beta>=0 witness domain; beta<=1 satisfies this inherited guard',original_source_modified=False,not_a_counterexample_to_the_ST_mathematical_bound=True)
else:raise AssertionError('expected inherited support-cutoff rejection was not observed')
print(json.dumps(result,ensure_ascii=False,indent=2))
