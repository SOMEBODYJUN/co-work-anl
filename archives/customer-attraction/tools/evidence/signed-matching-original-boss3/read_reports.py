"""Read every frozen record; reconcile descriptors and report geometry only.
No original import/entry, strategy or payoff evaluation, LP, or rational recovery.
"""
from pathlib import Path
from decimal import Decimal
from itertools import combinations
from math import comb, factorial
import ast
import hashlib
import json

HERE=Path(__file__).resolve().parent
files=[]


def read(name):
    p=HERE/'original'/name
    b=p.read_bytes()
    files.append(dict(path=str(p),size=len(b),sha256=hashlib.sha256(b).hexdigest()))
    return json.loads(b,parse_float=Decimal)


net=read('signed_matching_net_report.json')
uniform=read('signed_matching_uniform_report.json')
for r in [net,uniform]:
    assert set(r)=={'found','scope','records'}
    assert r['found'] is False and r['scope']=='Finite archived policies only; no universal assertion'
    assert len(r['records'])==192
    for x in r['records']:
        assert isinstance(x['source'],str) and x['source']
        assert all(type(v)is int and v>=0 for v in x['actual'])
        k=len(x['actual']);m=sum(x['actual'])
        assert 1<=m<=4 and m<=k<=6
        assert x['comparison']==sorted(set(x['comparison']))
        assert len(x['comparison'])==m and all(type(v)is int and 0<=v<k for v in x['comparison'])
        assert isinstance(x['max_min_gap_float'],Decimal) and x['max_min_gap_float'].is_finite()
for x in net['records']:assert set(x)=={'source','actual','comparison','max_min_gap_float'}
for x in uniform['records']:assert set(x)=={'uniform','source','actual','comparison','max_min_gap_float'} and x['uniform'] is True


def key(x):return x['source'],tuple(x['actual']),tuple(x['comparison'])


N={key(x):x for x in net['records']};U={key(x):x for x in uniform['records']}
assert len(N)==len(U)==192 and set(N)==set(U)
names=list(dict.fromkeys(x['source']for x in net['records']))
assert len(names)==18
summary=[];pairs=[]
for name in names:
    a=[r for r in net['records']if r['source']==name]
    b=[U[key(r)]for r in a]
    actuals={tuple(r['actual'])for r in a};assert len(actuals)==1
    actual=next(iter(actuals));k=len(actual);m=sum(actual)
    assert [tuple(r['comparison'])for r in a]==list(combinations(range(k),m))
    assert len(a)==comb(k,m)
    summary.append(dict(source=name,topics=k,players=m,actual=list(actual),records_each_mode=len(a),matching_permutations_per_net_case=factorial(m),net_min=min(x['max_min_gap_float']for x in a),net_max=max(x['max_min_gap_float']for x in a),uniform_min=min(x['max_min_gap_float']for x in b),uniform_max=max(x['max_min_gap_float']for x in b)))
    for x,y in zip(a,b):
        pairs.append(dict(source=name,actual=x['actual'],comparison=x['comparison'],net=x['max_min_gap_float'],uniform=y['max_min_gap_float'],uniform_minus_net=y['max_min_gap_float']-x['max_min_gap_float']))
assert all(x['max_min_gap_float']<0 for x in net['records']+uniform['records'])
dif=[x['uniform_minus_net']for x in pairs]
assert min(dif)>=Decimal('-1e-12')
src=(HERE/'original/signed_matching_net_probe.py').read_bytes();files.append(dict(path=str(HERE/'original/signed_matching_net_probe.py'),size=len(src),sha256=hashlib.sha256(src).hexdigest()))
tree=ast.parse(src)
rec_assign=[n for n in ast.walk(tree)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='rec'for t in n.targets)]
assert len(rec_assign)==1 and isinstance(rec_assign[0].value,ast.Dict)
assert 'uniform'in [k.value for k in rec_assign[0].value.keys if isinstance(k,ast.Constant)]
out=dict(kind='complete record/data/AST review only; not a numerical LP replay',inputs=files,rows_each_mode=192,unique_descriptor_pairs=192,source_count=18,sources=summary,all_descriptor_pairs=pairs,all_saved_objectives_strictly_negative=True,net_max=max(x['max_min_gap_float']for x in net['records']),uniform_max=max(x['max_min_gap_float']for x in uniform['records']),current_source_rec_always_contains_uniform=True,frozen_net_missing_uniform_field_records=192,frozen_uniform_true_records=192,objective_order_checks=dict(minimum_uniform_minus_net=min(dif),strict_negative_decimal_differences=sum(x<0 for x in dif),largest_small_negative_magnitude=max([-x for x in dif if x<0],default=Decimal(0)),all_differences_ge_minus_1e_12=True),total_net_permutation_constraint_rows_if_current_semantics=sum(x['records_each_mode']*x['matching_permutations_per_net_case']for x in summary),original_entry_executions=0,LP_executions=0,payoff_or_strategy_executions=0,limitations=['No report stores LP primal vectors, exact duals, policy actions, dependency hashes, failed/skipped LP counts, or solver versions.','Every listed source has all m-distinct comparisons, but unnamed skipped input pairs and overall solver failures are not logged.','The frozen net schema differs from current unconditional rec construction; no claim of byte replay or sole code difference.'])
(HERE/'record-review.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps(dict(status='passed',rows_each_mode=192,sources=18,full_descriptor_pairs=192,net_max=str(out['net_max']),uniform_max=str(out['uniform_max']),net_schema_differs_from_current_code=True,LP_executions=0)))
