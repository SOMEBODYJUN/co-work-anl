"""Definition-level Fraction audit of saved first-loop data; no original imports/LP."""
import argparse
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import hashlib
import json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
x = json.loads(args.input.read_text())
n, k, masks = x['n'], x['k'], x['masks']
assert (n,k) == (4,6) and masks == list(range(1,64))
policy = {tuple(r['history']): r['action'] for r in x['sigma']}
expected = {h for d in range(n) for h in product(range(k), repeat=d)}
assert set(policy) == expected and len(policy) == len(x['sigma']) == 259
assert all(0 <= a < k for a in policy.values())

def finish(prefix):
    z = list(prefix)
    while len(z) < n:
        z.append(policy[tuple(z)])
    return tuple(z)

def share(action, terminal, mask):
    if not mask & (1 << action):
        return Q(0)
    count = len([a for a in terminal if mask & (1 << a)])
    assert count > 0
    return Q(1, count)

root = finish(())
assert list(root) == x['root']
weights = {int(m): Q(v) for m,v in x['seed_weights'].items()}
assert 6 <= len(weights) <= 23 and all(v.denominator == 1 and 1 <= v <= 7 for v in weights.values())
slacks, nonself, row = [], [], 0
for item in x['sigma']:
    h, action = tuple(item['history']), item['action']
    actual = finish(h)
    for alternative in range(k):
        deviation = finish(h + (alternative,))
        independent = [share(action,actual,m) - share(alternative,deviation,m) for m in masks] + [Q(0)]
        assert independent == list(map(Q, x['gamma'][row]))
        slack = sum((independent[m-1] * value for m,value in weights.items()), Q(0))
        assert slack >= 0
        slacks.append(str(slack))
        if alternative != action:
            nonself.append(slack)
        row += 1
assert row == 1554 == len(x['gamma'])
coverage = [Q(any(m & (1<<a) for a in root)) for m in masks]
assert coverage == list(map(Q, x['coverage']))
W = sum((coverage[m-1] * value for m,value in weights.items()), Q(0))
queries = [{a:Q(1)} for a in range(k)] + [{a:Q(1,2),b:Q(1,2)} for a,b in combinations(range(k),2)] + [{a:Q(1,k) for a in range(k)}]
assert [{str(a):str(v) for a,v in p.items()} for p in queries] == x['queries']
assert len(x['LP_results']) == len(queries) == 22
deletion_values = []
for p, saved in zip(queries, x['LP_results']):
    assert saved['query'] == {str(a):str(v) for a,v in p.items()}
    expectations = []
    for i in range(n):
        other = root[:i] + root[i+1:]
        values = [sum((prob*share(a, other+(a,),m) for a,prob in p.items()),Q(0)) for m in masks]
        assert [-v for v in values] + [Q(1)] == list(map(Q,saved['deletion_rows'][i]))
        expectations.append(sum((values[m-1]*v for m,v in weights.items()),Q(0)))
    deletion_values.append(dict(query=saved['query'],seed_expected_by_deleted_position=list(map(str,expectations)),
                                seed_min=str(min(expectations)),seed_target_gap=str(W-Q(7,2)*min(expectations))))
report = dict(status='PASS_EXACT_SAVED_MATRIX_AND_SEED_FULL_HISTORY_SPE',
              input_sha256=hashlib.sha256(args.input.read_bytes()).hexdigest(),
              scope='One saved first iteration: full ordered-history IC coefficients, root coverage and all22x4 deletion rows match independent Fraction definitions; exact SPE on sampled seed weights only. No original imports, solver, LP or float optimality certificate.',
              n=n,k=k,customer_type_columns=63,history_count=259,gamma_rows=1554,
              gamma_customer_coefficients=1554*63,gamma_t_coefficients=1554,
              self_deviations=259,nonself_deviations=len(nonself),
              positive_nonself_slacks=sum(v>0 for v in nonself),zero_nonself_slacks=sum(v==0 for v in nonself),
              min_gamma=str(min(map(Q,slacks))),
              root=list(root),seed_positive_types=len(weights),seed_customer_count=str(sum(weights.values())),
              seed_welfare=str(W),seed_payoffs=[str(sum((v*share(a,root,m) for m,v in weights.items()),Q(0))) for a in root],
              coverage_coefficients=63,deletion_rows=22*4,deletion_customer_coefficients=22*4*63,
              deletion_t_coefficients=22*4,query_distributions=22,
              original_float_successful_LPs=sum(r['success'] for r in x['LP_results']),
              original_float_best_score=x['best_score'],
              original_float_objectives=[r['objective'] for r in x['LP_results']],
              seed_gamma_slacks=slacks,deletion_on_seed=deletion_values,
              new_original_function_calls=0,new_LP_calls=0)
args.out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('seed_gamma_slacks','deletion_on_seed','original_float_objectives')},indent=2))
