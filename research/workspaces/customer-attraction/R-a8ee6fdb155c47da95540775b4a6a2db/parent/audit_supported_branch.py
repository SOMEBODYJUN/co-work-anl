"""Independent parent reconstruction from the saved complete action table.

No import from the author's attack implementation. Fractions throughout.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from functools import lru_cache
import hashlib
import json

HERE = Path(__file__).resolve().parent


def main():
    source = HERE.parent / 'attack/supported_branch_six_full_policy.json'
    data = json.loads(source.read_text())
    m, p = data['m'], data['p']
    interests = [set(c) for c in data['clients']]
    policy = {tuple(row['history']): row['action'] for row in data['policy']}

    @lru_cache(None)
    def leaf(h):
        return h if len(h) == m else leaf(h + (policy[h],))

    def profit(z, i):
        return sum((F(1, sum(a in c for a in z)) for c in interests if z[i] in c), F())

    histories = comparisons = 0
    minslack = None
    for depth in range(m):
        for h in product(range(p), repeat=depth):
            histories += 1
            actual = leaf(h)
            assert actual[depth] == policy[h]
            for a in range(p):
                slack = profit(actual, depth) - profit(leaf(h + (a,)), depth)
                assert slack >= 0, (h, a, slack)
                minslack = slack if minslack is None else min(minslack, slack)
                comparisons += 1
    assert histories == len(policy) == 1365 and comparisons == 5460

    def budget(h):
        z = leaf(h)
        out = sum((profit(z, i) for i in range(len(h), m)), F())
        for i in range(len(h), m):
            for c in interests:
                if z[i] in c:
                    prior = sum(a in c for a in z[:i])
                    out += F(1, prior+1) - F(1, prior+m-i)
        return out

    h = (3, 3, 3)
    harmonic = [sum((F(1, j) for j in range(1, k+1)), F()) for k in range(m+1)]
    vals = {}
    for comparison in combinations_with_replacement(range(p), 3):
        vals[comparison] = sum((harmonic[sum(a in c for a in h+comparison)]
                                  - harmonic[sum(a in c for a in h)]
                                  for c in interests), F())
    maximum = max(vals.values())
    opt = [q for q, v in vals.items() if v == maximum]
    support = sorted(set(a for q in opt for a in q))
    actualbudget = budget(h)
    branches = []
    for a in support:
        arrival = sum((F(1, sum(b in c for b in h)+1) for c in interests if a in c), F())
        branchbudget = arrival+budget(h+(a,))
        assert branchbudget > actualbudget
        branches.append({'forced': a, 'leaf': leaf(h+(a,)),
                         'root_payoff': str(profit(leaf(h+(a,)), len(h))),
                         'arrival_plus_child_budget': str(branchbudget),
                         'excess_over_actual_budget': str(branchbudget-actualbudget)})
    assert leaf(()) == (3,3,3,2,0,0)
    assert maximum == F(13,3) and actualbudget == F(14,3) and support == [0,1]
    report = {'status': 'INDEPENDENT_EXACT_FULL_SPE_AUDIT_PASS',
              'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'decision_histories': histories, 'action_comparisons': comparisons,
              'minimum_IC_slack': str(minslack), 'actual': leaf(()),
              'local_actual_profit': str(profit(leaf(h), len(h))),
              'local_budget': str(actualbudget), 'local_maximum_potential': str(maximum),
              'all_potential_maximizers': opt, 'their_union_support': support,
              'supported_branches': branches,
              'scope': 'The support-restricted or support-averaged branch monotonicity is false. Neither the copy-tax potential candidate nor half is refuted.'}
    (HERE/'supported_branch_independent_exact.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
