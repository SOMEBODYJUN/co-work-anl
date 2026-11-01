"""Reconstruct these four finite proposals; validate every ordered-history IC.

Rational recovery is only a candidate generator. Exact checks, rather than
rounding tolerances or HiGHS status, certify the reconstructed finite games.
Run from any directory; output goes beside this script in exact_reports.json.
"""
from fractions import Fraction as F
from itertools import product, combinations
from functools import lru_cache
from pathlib import Path
from math import lcm
import hashlib
import json

HERE = Path(__file__).resolve().parent


def audit(path):
    data = json.loads(path.read_text())
    actual = tuple(map(int, data['parameters']['path'].split(',')))
    portfolio = tuple(map(int, data['parameters']['portfolio'].split(',')))
    m, k = len(actual), data['parameters']['topics']
    weights = {mask: F(str(v)).limit_denominator(1_000_000)
               for mask, v in enumerate(data['types'], 1)}
    assert len(weights) == 2**k - 1 and all(v >= 0 for v in weights.values())
    actions = {tuple(v['history']): v['action'] for v in data['actions']}
    histories = {h for d in range(m) for h in product(range(k), repeat=d)}
    assert len(actions) == len(data['actions']) and set(actions) == histories
    assert all(type(a) is int and 0 <= a < k for a in actions.values())

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == m else terminal(h + (actions[h],))

    def payoff(h, i):
        t = terminal(h)
        a = t[i]
        return sum((w / sum(bool(mask & (1 << b)) for b in t)
                    for mask, w in weights.items() if mask & (1 << a)), F())

    slacks = []
    for h in sorted(histories, key=lambda x: (len(x), x)):
        i, chosen = len(h), actions[h]
        for a in range(k):
            slacks.append(payoff(h + (chosen,), i) - payoff(h + (a,), i))
    assert min(slacks) >= 0, (path.name, min(slacks))
    assert terminal(()) == actual
    coverage = lambda s: sum(w for mask, w in weights.items()
                             if any(mask & (1 << a) for a in s))
    welfare = coverage(actual)
    optimum = max(coverage(s) for d in range(min(m, k)+1)
                  for s in combinations(range(k), d))
    query = sum((payoff(actual[:i] + (a,), i)
                 for i in range(m) for a in portfolio), F())
    compare = coverage(portfolio)
    objective = (m-1)*welfare + query - m*compare
    scale = lcm(*(w.denominator for w in weights.values()))
    return dict(file=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                normalized_types={str(b): str(w) for b, w in weights.items() if w},
                integer_scale=scale, integer_customers={str(b): int(w*scale)
                                                       for b, w in weights.items() if w},
                maximum_recovery_distance=max(abs(float(weights[b])-float(v))
                    for b, v in enumerate(data['types'], 1)),
                nodes=len(histories), comparisons_including_chosen=len(slacks),
                deviations=len(histories)*(k-1), minimum_IC_slack=str(min(slacks)),
                actual=actual, portfolio=portfolio,
                root_payoffs=[str(payoff((), i)) for i in range(m)],
                W=str(welfare), OPT=str(optimum), comparison_coverage=str(compare),
                query=str(query), objective=str(objective),
                integer_W=str(welfare*scale), integer_OPT=str(optimum*scale),
                integer_objective=str(objective*scale),
                solver_status=data['status'], original_fun=data['fun'],
                original_dual_bound=data['mip_dual_bound'],
                conclusion='finite reconstructed SPE only; no MILP optimality certificate')


if __name__ == '__main__':
    names = ['full_tree_aabb_bcde.json', 'full_tree_abb_bcd.json',
             'full_tree_abc_bcd.json', 'full_tree_abc_cde.json']
    report = [audit(HERE / 'original' / name) for name in names]
    (HERE / 'exact_reports.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
