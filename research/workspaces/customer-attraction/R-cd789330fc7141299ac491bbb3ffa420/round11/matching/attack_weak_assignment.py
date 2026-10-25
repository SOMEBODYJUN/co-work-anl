"""One targeted attack on the all-input WEAK-Q conjecture.

The policy is the existing round10 m5 eight-theme full-history StrongA
witness, with every true IC retained.  One five-theme target is required to
be strictly uniquely optimal and every permutation must violate WEAK-Q.
This is a candidate attack only; a nonpositive floating optimum is no theorem.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations
import json, sys, time
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
sys.path[:0] = [str(ROOT), str(ROOT / 'tests/audits')]
from customer_attraction_strategy_lp import StrategyCone, coverage_row, payoff_row


def main():
    started = time.monotonic()
    source = HERE.parents[1] / 'round10/credible/strong_adjacent_gap_attack.json'
    data = json.loads(source.read_text())
    p, m = data['topics'], data['m']
    actions = {tuple(row['history']): row['action']
               for row in data['strategy']['actions']}
    cone = StrategyCone(p, m, actions)
    path = tuple(data['actual_path'])
    target = (0, 1, 2, 5, 6)
    O = coverage_row(p, target)
    n = (1 << p) - 1
    rows = [list(-row) + [0.0] for row in cone.matrix]
    for alternative in combinations_with_replacement(range(p), m):
        if alternative != target:
            rows.append([float(a-b) for a,b in zip(coverage_row(p, alternative), O)] + [1.0])
    for pi in permutations(target):
        price = [F(0)] * n
        for i, a in enumerate(pi):
            leaf = path[:i] + (a,) + path[i+1:]
            q = tuple(leaf.count(b) for b in range(p))
            price = [x+y for x,y in zip(price, payoff_row(p, q, a))]
        rows.append([float(F(m+1,m)*w-f) for w,f in zip(cone.welfare,price)] + [1.0])
    result = linprog([0.0]*n+[-1.0], A_ub=np.array(rows),
                     b_ub=np.zeros(len(rows)),
                     A_eq=np.array([[float(w) for w in cone.welfare]+[0.0]]),
                     b_eq=[1.0], bounds=[(0,None)]*n+[(None,None)],
                     method='highs', options={'time_limit': 40})
    report = dict(
        claim='WEAK-Q: some coverage-optimal m-tuple and permutation have frozen Q <= (1+1/m)W',
        scope='one existing complete policy cone; one strict unique-optimum target; finite floating attack only',
        source=str(source.relative_to(ROOT)), m=m, p=p, actual=list(path),
        target=list(target), exact_full_histories=len(actions),
        distinct_nonzero_true_IC_rows=len(cone.rows), total_lp_rows=len(rows),
        all_target_permutations=120, floating_status=result.status,
        message=result.message, half='OPEN', weak_assignment='OPEN',
        exact_primal=False, universal_bound_proved=False,
        seconds=time.monotonic()-started)
    if result.success:
        report['floating_common_strict_margin']=float(result.x[-1])
        if result.x[-1]>1e-7:
            report['floating_positive_candidate']=[
                dict(mask=j+1,weight=float(x)) for j,x in enumerate(result.x[:-1]) if x>1e-8]
    (HERE/'weak_assignment_attack.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
