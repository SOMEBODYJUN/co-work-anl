"""New exact definition check ONLY for the previously unaudited raw72 input.

For the13 input, compare old sufficient evidence to acquired originals only.
No canonical package, random search, minimizer, LP or MILP is imported.
"""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--repository-root',type=Path,required=True);args=ap.parse_args()
inputs=[]


def read(path):
    b=path.read_bytes();inputs.append(dict(path=str(path),size=len(b),sha256=hashlib.sha256(b).hexdigest()))
    return json.loads(b)


raw=read(HERE/'original/kernel_no_common_parameter_raw.json')
small=read(HERE/'original/kernel_no_common_parameter.json')
original_report=read(HERE/'original/audit_thinning_obstruction.json')
oldbase=args.repository_root/'archives/customer-attraction/tools/evidence/rank-one-thinning-and-aligned-closure-primary'
old=read(oldbase/'new-thinning-definition-check.json');old_event=read(oldbase/'runtime-record.json')
assert old_event['output_sha256']==hashlib.sha256((oldbase/'new-thinning-definition-check.json').read_bytes()).hexdigest()
assert old_event['entry_sha256']==hashlib.sha256((oldbase/'check_thinning_from_definitions.py').read_bytes()).hexdigest()
assert raw['p']==4 and raw['n']==3 and small['players']==3 and small['topics']==list('ABCD')
expected={h for d in range(3)for h in itertools.product(range(4),repeat=d)}
actions={tuple(h):a for h,a in raw['actions']}
assert len(actions)==len(raw['actions'])==21 and set(actions)==expected
assert all(type(a)is int and 0<=a<4 for a in actions.values())
assert raw['actions']==small['actions']
assert actions=={tuple(row['history']):row['action']for row in old['full_policy_actions']}
types={tuple(B):w for B,w in raw['types']}
assert len(types)==len(raw['types'])==13 and sum(types.values())==72
assert all(B==tuple(sorted(set(B)))and B and all(type(a)is int and 0<=a<4 for a in B)and type(w)is int and w>0 for B,w in types.items())
small_types={tuple(c['topics']):c['multiplicity']for c in small['customers']}
assert sorted(small_types.items())==sorted((tuple(B),w)for B,w in old['types'])
assert sum(small_types.values())==13 and all(small_types.get(B,0)<=w for B,w in types.items())


def follow(h):
    while len(h)<3:h+=(actions[h],)
    return h


def poly(z,i):
    out=[0]*3
    for B,w in types.items():
        if z[i]in B:out[sum(a in B for a in z)-1]+=w
    return out


def integrate(c):return sum((F(a,i+1)for i,a in enumerate(c)),F(0))


def coverage(z):return sum(w for B,w in types.items()if any(a in B for a in z))


rows=[];lookup={}
for d in range(3):
    for h in itertools.product(range(4),repeat=d):
        z=follow(h);chosen_poly=poly(z,d);chosen=integrate(chosen_poly);alt=[]
        for a in range(4):
            zz=follow(h+(a,));pp=poly(zz,d);value=integrate(pp);delta=[x-y for x,y in zip(chosen_poly,pp)];gap=chosen-value
            assert gap>=0 and integrate(delta)==gap
            v=dict(action=a,terminal=list(zz),kernel_coefficients=pp,harmonic_value=str(value),component_slack_coefficients=delta,harmonic_slack=str(gap))
            alt.append(v);lookup[h,a]=v
        rows.append(dict(history=list(h),chosen=actions[h],terminal=list(z),kernel_coefficients=chosen_poly,harmonic_value=str(chosen),alternatives=alt))
special=[]
for h,a,c in raw['rows']:
    r=lookup[tuple(h),a];assert r['component_slack_coefficients']==c
    special.append(dict(history=h,deviation=a,coefficients=c,harmonic_integral=r['harmonic_slack']))
assert [s['coefficients']for s in special]==[[0,-4,6],[-1,2,2],[2,0,-5]]
assert [s['harmonic_integral']for s in special]==['0','2/3','1/3']
# For t>0, first nonnegative forces t>=2/3; third then <=-2/9.
# t=0 is excluded by the negative constant of the second row.
assert F(2)-5*F(2,3)**2==F(-2,9)
actual=follow(());pay=[integrate(poly(actual,i))for i in range(3)]
terminal_coverages=[dict(terminal=list(z),coverage=coverage(z))for z in itertools.product(range(4),repeat=3)]
W=coverage(actual);OPT=max(r['coverage']for r in terminal_coverages)
assert actual==(1,2,3)and pay==[25,F(49,2),F(45,2)]and W==OPT==72

# Data-only reconciliation of13; do not evaluate its payoffs again.
assert original_report['ordered_decision_histories']==old['nodes']==21
assert original_report['exact_one_step_comparisons']==old['including_self_comparisons']==84
assert original_report['unit_customers']==old['unit_customers']==13
assert original_report['root_path']==['ABCD'[a]for a in old['actual']]
assert original_report['root_payoffs']==old['profits']
assert original_report['root_welfare']==old['W']==13 and original_report['OPT']==old['OPT']==13
for row,prev in zip(original_report['all_history_payoff_table'],old['all_rows']):
    assert row['history']==['ABCD'[a]for a in prev['history']]
    assert row['action']=='ABCD'[prev['chosen']]
    assert row['deviation_payoffs']==[a['harmonic_value']for a in prev['alternatives']]
assert [r['coefficients']for r in original_report['incompatible_component_rows']]==[r['coefficients']for r in old['three_zero_integral_obstructions']]
small_special=[r['coefficients']for r in old['three_zero_integral_obstructions']]
a,b,c=small_special
assert a[0]==0 and 3*a[1]+2*a[2]==0 and c[1]==0 and 3*c[0]+c[2]==0
assert a[1]<=-2 and c[0]>=1 and b[0]<=-1
out=dict(kind='raw72 new exact definition audit plus13 original/old-evidence data correspondence',inputs=inputs,raw72=dict(unit_customers=72,full_actions=raw['actions'],all_rows=rows,including_self_comparisons=84,nonself_comparisons=63,minimum_including_self_slack='0',special_rows=special,actual=list(actual),payoffs=list(map(str,pay)),W=W,OPT=OPT,all64_terminal_coverages=terminal_coverages,no_common_t_exact='t=0 fails DA constant -1; t>0 and BA>=0 force t>=2/3; DD<=-2/9<0'),relation_raw_to_small=dict(full_action_arrays_identical=True,raw_customers=72,small_customers=13,small_type_counts_componentwise_at_most_raw=True,removed_customer_count=59,universal_customer_deletion_preservation_claim=False),small13_data_correspondence=dict(instance_types_actions_equal_old_MD_definition_input=True,all84_deviation_payoffs_equal_old=True,special_coefficients_equal_old=True,minimizer_four_equalities_and_three_sign_bounds_hold_at_saved_small=True,small_payoff_recomputations_by_this_entry=0,old_definition_entry_runs_this_batch=0),random_search_minimizer_graph_LP_runs=0,original_audit_runs_by_this_entry=0)
(HERE/'raw-and-comparison.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(status='passed',raw_customers=72,raw_nodes=21,raw_comparisons=84,raw_payoffs=list(map(str,pay)),raw_W=W,raw_OPT=OPT,small13_recomputed=False,random_MILP_graph_LP_runs=0)))
