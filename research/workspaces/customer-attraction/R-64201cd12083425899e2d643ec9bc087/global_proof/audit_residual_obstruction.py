"""Independent definition-level exact audit of the explicit 27-customer game."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json
from pathlib import Path

names='ABTSQR'
blocks=[('A',4),('AQR',2),('B',5),('BQR',2),('T',3),('TQ',2),('TR',2),('S',3),('SQ',2),('SR',2)]
themes={a:set() for a in names}
for likes,count in blocks:
    for k in range(count):
        customer=(likes,k)
        for a in likes:themes[a].add(customer)
def utility(a,b):
    return sum((F(1,1+int(x in themes[b])) for x in themes[a]),F(0))
reply=dict(zip(names,'BQQRRQ'))
expected=[
 [3,7,7,7,7,7],
 [6,F(7,2),7,7,7,7],
 [6,7,F(7,2),7,7,7],
 [6,7,7,F(7,2),7,7],
 [5,6,6,6,4,6],
 [5,6,6,6,6,4],
]
for a,row in zip(names,expected):
    observed=[utility(b,a) for b in names]
    assert observed==row,(a,observed,row)
    assert utility(reply[a],a)==max(observed)
    assert utility(a,reply[a])==6
C=themes['A']|themes['B']
assert len(C)==13
pairs=list(combinations_with_replacement(names,2))
opt=max(len(themes[a]|themes[b]) for a,b in pairs)
residual_opt=max(len((themes[a]|themes[b])-C) for a,b in pairs)
assert opt==residual_opt==14
assert themes['T'].isdisjoint(C) and themes['S'].isdisjoint(C)
assert themes['T'].isdisjoint(themes['S'])
report={'customers':sum(n for _,n in blocks),'players':2,'themes':6,
        'decision_histories':7,'action_comparisons':42,'actual_path':['A','B'],
        'payoffs':[6,7],'welfare':13,'optimum':opt,'residual_optimum':residual_opt,
        'original_half_coverage_holds':2*len(C)>=opt,
        'residual_portfolio_budget_holds':residual_opt<=len(C)}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,sort_keys=True))
