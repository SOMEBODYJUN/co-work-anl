"""Independent reviewer checks for exact supplied-certificate implementation."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import importlib.util
import hashlib
import json
import sys

SOURCE = Path(__file__).with_name('distorted_group_joint_slot.py')
spec = importlib.util.spec_from_file_location('_review_distorted_group', SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def fixture():
    return dict(groups=[dict(w=[F(1,4)]*4,E=[0],b={0:F(1)},p={0:[F(1,4)]*4})],
                sink_count=1,macros=[{0:F(3,4)}],T=F(1),delta=F(1,4),
                kappa=F(5,4),Bbar=F(3,2),r=F(3,5),
                macro_flow=[{0:F(1)}],receiver_flow=[{0:F(1)}])

accepted=[];rejected=[]
def success(name, data):
    ans=mod.round_distorted_certificate(**data)
    rec=mod.actual_loads(data['groups'],data['sink_count'],data['macros'],
                         ans['macro_assignment'],ans['private_assignment'])
    assert rec==(ans['home_loads'],ans['sink_loads'])
    assert all(v<=(1+data['r']+data['delta'])*data['T'] for v in rec[0])
    assert all(v<=(data['kappa']+data['Bbar']*(1-data['r']))*data['T'] for v in rec[1])
    accepted.append(dict(name=name,home=list(map(str,rec[0])),sink=list(map(str,rec[1]))))

def rejection(name, mutate):
    d=fixture();mutate(d)
    try:mod.round_distorted_certificate(**d)
    except ValueError:rejected.append(name)
    else:raise AssertionError('invalid witness accepted: '+name)

success('ordinary_positive_demand',fixture())
d=fixture();d['Bbar']=F(0);d['r']=F(1,2);d['groups'][0]['b'][0]=F(0)
d['groups'][0]['p'][0]=[F(0)]*4
success('zero_Bbar_left_endpoint',d)
d=fixture();d.update(macros=[],macro_flow=[],receiver_flow=[{}],T=F(0))
d['groups']=[dict(w=[F(0),F(0)],E=[],b={},p={})]
success('T_zero_empty_macros_and_E',d)
d=fixture();d.update(groups=[],macros=[],macro_flow=[],receiver_flow=[],T=F(0))
success('empty_task_set',d)
d=fixture();d['groups'][0]=dict(w=[F(0)],E=[],b={},p={});d['receiver_flow']=[{None:F(1)}]
success('zero_demand_bypass_empty_E',d)

rejection('bad_upper_envelope',lambda d:d['groups'][0]['p'][0].__setitem__(0,F(1,2)))
rejection('bad_lower_envelope',lambda d:d['groups'][0]['p'][0].__setitem__(0,F(0)))
rejection('positive_demand_bypass',lambda d:d.__setitem__('receiver_flow',[{None:F(1)}]))
rejection('broken_common_flow',lambda d:d.__setitem__('receiver_flow',[{0:F(1,2)}]))
rejection('macro_above_pruned_target',lambda d:d['macros'][0].__setitem__(0,F(5,4)))
rejection('floating_target',lambda d:d.__setitem__('T',1.0))
rejection('boolean_sink_count',lambda d:d.__setitem__('sink_count',True))
rejection('negative_token_mass',lambda d:d.__setitem__('receiver_flow',[{0:F(-1)}]))
def no_receiver(d):
    d['groups'][0].update(E=[],b={},p={});d['receiver_flow']=[{0:F(1)}]
rejection('positive_demand_no_receiver',no_receiver)
def excessive(d):
    d.update(kappa=F(1),Bbar=F(3),r=F(1,2))
    d['groups'][0]['b'][0]=F(3);d['groups'][0]['p'][0]=[F(3,4)]*4
rejection('receiver_budget_exceeded',excessive)
print(json.dumps(dict(python=sys.version.split()[0],
                      implementation_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                      reviewer_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      accepted=accepted,rejected=rejected,
                      scope='Five valid exact certificate boundaries and ten invalid certificates; no LP backend or unknown-OPT software test.'),
                 ensure_ascii=False,indent=2))
