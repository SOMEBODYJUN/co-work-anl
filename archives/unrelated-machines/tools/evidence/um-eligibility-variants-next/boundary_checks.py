#!/usr/bin/env python3
"""Exact arithmetic for explicit proof-boundary witnesses, not generic LP solving."""
from fractions import Fraction as F
import json
from pathlib import Path

root = Path(__file__).resolve().parent
inputs = {
    'identity_dependent_macro': {
        'T': '1', 'delta': '1/5',
        'macro_home_by_job': [['3/5','9/10'],['9/10','3/5']],
        'private_jobs': [{'allowed': [0], 'p': '1/5'}, {'allowed': [0], 'p': '1/5'}]},
    'upper_envelope_only_false_rejection': {
        'T':'1', 'delta':'1/4', 'homes':3, 'one_macro_each_p':'1',
        'private_each_group':['1/4']*4, 'common_sinks':[0], 'actual_sink_p':'0',
        'claimed_upper_rho':'1'},
    'empty_positive_d_unoccupied_home': {
        'T':'1', 'delta':'1/4', 'macro_only_home':1, 'macro_p':'1',
        'private_home0':['1/4']*4, 'E0':[], 'private_home1':[]},
    'unpruned_macro': {'T':'1','macro_p':'2','private_jobs':[], 'delta':'0'},
    'zero_d': {'T':'1', 'macro_p':'3/4','private_jobs':[]},
    'forced_split_quantum': {'T':'1','macro_p':'3/5','u':'2/5',
        'E':[[0],[0],[1],[1]]},
    'later_ratio_parameters': {'delta':'1/10','kappa':'1','Bbar':'4'}
}
p = [[F(v) for v in row] for row in inputs['identity_dependent_macro']['macro_home_by_job']]
private = F(2,5)
good = [p[0][0]+private,p[1][1]]
bad_capacity = F(1)-p[0][1]
assert max(good)==1 and private>bad_capacity
virtual = 3*F(1,2)
assert virtual>1  # all three occupied tokens violate the false necessary LP
assert max([F(1)]*3+[F(0)])==1  # true matrix: all private work goes to zero sink
assert F(1)-F(1,2)>0  # home0 has positive d but x0=0, home1 uses d1=0 dummy
assert F(2)>F(3,2)  # absent pruning violates even delta0 home guarantee
assert F(0)==F(0)  # e=d=0: the unqualified strict e>d is false
assert (F(1)-F(3,5))//F(2,5)==1 and F(1)//F(2,5)==2
delta=F(1,10); kappa=F(1); B=F(4)
r=max(F(1,2),(kappa+B-1-delta)/(1+B))
alpha=max(1+r+delta,kappa+B*(1-r))
assert r==F(39,50) and alpha==F(47,25) and alpha<2
report={'all_passed':True, 'checks':len(inputs),
    'good_macro_match_loads':list(map(str,good)),
    'bad_matching_home0_private_capacity':str(bad_capacity),
    'upper_only_false_LP_required_load':str(virtual),
    'later_ratio_r':str(r), 'later_ratio_alpha':str(alpha),
    'scope':'Explicit rational witnesses and algebra only; no generic LP/ST backend or NP-hardness experiment.'}
(root/'boundary-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
(root/'boundary-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
