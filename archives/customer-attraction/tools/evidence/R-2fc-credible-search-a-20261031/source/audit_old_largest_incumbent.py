"""Independent unit-customer audit of an old relaxed, incorrectly scoped JSON.

No customer_attraction, LP, MILP, or SPE-solver imports are used. The source is
left unchanged. Its literal verified:true does not establish the full SPE
definition: the generating script excluded root incentive comparisons.
"""
from fractions import Fraction
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').is_file())
SOURCE = ROOT/'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_n3p6_best.json'
RAW = SOURCE.read_bytes()
data = json.loads(RAW)
inst = data['instance']
p, m = len(inst['topics']), inst['players']
units = tuple(frozenset(row['topics']) for row in inst['customers']
              for _ in range(row['multiplicity']))
policy = {tuple(row['history']):row['action'] for row in data['strategy']['actions']}
histories = tuple(h for d in range(m) for h in product(range(p), repeat=d))
assert len(policy) == len(data['strategy']['actions']) and set(policy) == set(histories)
assert all(a in range(p) for a in policy.values())


def terminal(h):
    while len(h) < m:
        h = h+(policy[h],)
    return h


def payoff(h, a):
    path = terminal(h)
    return sum((Fraction(1, sum(t in B for t in path)) for B in units if a in B), Fraction(0))


def welfare(path):
    return sum(any(a in B for a in path) for B in units)


rows = []
bad = []
for h in histories:
    a = policy[h]
    actual = payoff(h, a)
    for b in range(p):
        if b == a:
            continue
        deviation = payoff(h+(b,), b)
        row = {'history':h, 'chosen':a, 'deviation':b, 'actual':str(actual),
               'deviating':str(deviation), 'branch_terminal':terminal(h+(b,)),
               'slack':str(actual-deviation)}
        rows.append(row)
        if actual < deviation:
            bad.append(row)

path = terminal(())
opt = max(welfare(J) for J in combinations(range(p), min(m,p)))
assert tuple(path.count(a) for a in range(p)) == tuple(data['strategy']['terminal_counts'])
out = {
    'source':str(SOURCE.relative_to(ROOT)),
    'source_sha256':hashlib.sha256(RAW).hexdigest(),
    'implementation':'independent expanded unit customers; standard-library Fraction; complete ordered histories',
    'source_claimed_verified':data['verified'],
    'scope_correction':'The generating largest_incumbent_probe.py explicitly excluded every root incentive row. Its verified:true is not verification under the complete-history SPE definition.',
    'unit_customers':len(units), 'players':m, 'topics':p,
    'decision_histories':len(histories), 'proper_deviation_checks':len(rows),
    'full_history_SPE':not bad, 'bad_comparisons':bad,
    'nonroot_bad_comparisons':sum(bool(row['history']) for row in bad),
    'actual_path':path, 'actual_payoffs':[str(payoff((),a)) for a in path],
    'welfare':welfare(path), 'optimum':opt,
    'root_all_branches':[row for row in rows if not row['history']],
}
assert out['nonroot_bad_comparisons'] == 0 and len(bad) == 5
assert payoff((),0) == Fraction(375,2) and payoff((3,),3) == 357
(HERE/'old_largest_incumbent_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
