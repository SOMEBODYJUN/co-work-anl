"""One exact review of an explicitly specified policy, without original imports.

This is not the unpersisted MILP-selected action table. It independently checks
the all-big-topic policy on the frozen baseline input and verifies metadata.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
SUB=Path('research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/true_spe_search')
old=json.loads((HERE/'original'/SUB/'dag_baseline_fixed_m5p7.json').read_text())
summary=json.loads((HERE/'original'/SUB/'dag_search_summary.json').read_text())
new=json.loads((HERE/'replay-large-baseline/dag_baseline_fixed_m5p7.json').read_text())
assert old == summary['baseline_control']['fixed_instance']
assert len(old['integer_clones']) == 127
clones=old['integer_clones']
assert [(i+1,x) for i,x in enumerate(clones) if x] == [(1,5),(2,1),(4,1),(8,1),(16,1),(32,1),(64,1)]
p,m=7,5

def payoff(z, a):
    return sum((F(w,sum(bool(mask & (1<<b)) for b in z))
                for mask,w in enumerate(clones,1) if w and mask & (1<<a)),F(0))

def welfare(z):
    return sum(w for mask,w in enumerate(clones,1) if w and any(mask & (1<<b) for b in z))

histories=comparisons=nonself=ties=0
min_margin=None
for depth in range(m):
    for h in product(range(p),repeat=depth):
        histories+=1
        actual=h+(0,)*(m-depth)
        u=payoff(actual,0)
        for b in range(p):
            z=h+(b,)+(0,)*(m-depth-1)
            margin=u-payoff(z,b)
            assert margin>=0,(h,b,margin)
            min_margin=margin if min_margin is None else min(min_margin,margin)
            comparisons+=1
            nonself+=b!=0
            ties+=margin==0
assert histories==2801 and comparisons==19607 and nonself==16806
W=welfare((0,)*m)
OPT=max(welfare(z) for z in combinations(range(p),m))
assert (W,OPT,F(OPT,W))==(5,9,F(9,5))
assert all(old[k]==new[k] for k in old if k!='milp')
assert {k:v for k,v in old['milp'].items() if k!='seconds'} == {k:v for k,v in new['milp'].items() if k!='seconds'}
dimension_checks=[]
for r in summary['records']:
    d=r['milp'];p1=d['topics'];m1=d['players']
    Y=comb(m1+2*p1-1,2*p1-1)
    Z=p1*comb(m1+2*p1-2,2*p1-1)
    T=comb(m1+p1-1,p1);leaves=comb(m1+p1-1,p1-1)
    assert d['variables']==(1<<p1)-1+Y+2*Z+T
    assert d['binary']==Y+2*Z
    assert d['rows']==1+p1+Y-leaves+4*Z+p1*T
    nodes=sum(p1**i for i in range(m1))
    assert r['exact_candidate']['nodes']==nodes
    assert r['exact_candidate']['deviation_checks']==nodes*(p1-1)
    dimension_checks.append({'scratch_source':r['scratch_source'],'Y':Y,'Z':Z,'thresholds':T,
                             'metadata_consistent':True})
out={'status':'pass','scope':'explicit all-big-topic policy on fixed input and arithmetic metadata only',
     'original_solver_or_package_imports':False,'solver_calls':0,'original_main_runs':0,
     'new_independent_script_runs':1,'timing_recorded':False,
     'policy':{'action':0,'for_every_ordered_history_of_length_less_than':5,
               'not_the_saved_original_milp_witness':True},
     'complete_ordered_decision_histories':histories,'comparisons_including_self':comparisons,
     'comparisons_excluding_self':nonself,'ties_including_self':ties,'minimum_IC_margin':str(min_margin),
     'W':W,'OPT':OPT,'ratio':str(F(OPT,W)),'seven_historical_record_metadata':dimension_checks,
     'old_baseline_equals_summary_embedded_fixed_instance':True,
     'new_original_report_differs_only_milp_seconds':True,
     'seven_historical_candidate_feasibility_recertified':False}
(HERE/'independent-baseline-review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False))
