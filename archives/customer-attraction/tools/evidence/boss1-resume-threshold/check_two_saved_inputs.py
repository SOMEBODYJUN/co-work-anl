#!/usr/bin/env python3
"""New exact max-min audit of two already-published customer tables.

No original module, solver, certificate, random generator, or optimizer is run.
This calculates all child SPE outcome sets; it does not validate the supplied
historical complete strategy maps. Their exact action tables have separate
proofs/evidence in the linked formal objects. Counts cache outcome sets only.
"""
from fractions import Fraction as F
from functools import cache
from itertools import product
from pathlib import Path
import hashlib
import json


def audit(spec):
    p, m = spec['topics'], spec['players']
    types = [(frozenset(t), n) for t, n in spec['customer_types']]

    def inc(k, a):
        return k[:a] + (k[a] + 1,) + k[a + 1:]

    @cache
    def utility(k, a):
        return sum((F(n, sum(k[t] for t in ts))
                    for ts, n in types if a in ts), F(0))

    def welfare(k):
        return sum(n for ts, n in types if any(k[t] for t in ts))

    @cache
    def outcomes(k):
        if sum(k) == m:
            return frozenset([k])
        children = [outcomes(inc(k, a)) for a in range(p)]
        threshold = max(min(utility(z, a) for z in children[a]) for a in range(p))
        return frozenset(z for a in range(p) for z in children[a]
                         if utility(z, a) >= threshold)

    root = (0,) * p
    outcomes(root)
    path = tuple(spec['actual'])
    target = tuple(path.count(a) for a in range(p))
    k, rows, theta, realizable = root, [], [], True
    for action in path:
        row = [min(utility(z, a) for z in outcomes(inc(k, a))) for a in range(p)]
        rows.append(row)
        theta.append(max(row))
        realizable &= target in outcomes(inc(k, action)) and utility(target, action) >= max(row)
        k = inc(k, action)
    optimal, optimum = [], -1
    for t in product(range(p), repeat=m):
        counts = tuple(t.count(a) for a in range(p))
        w = welfare(counts)
        if w > optimum:
            optimum, optimal = w, [t]
        elif w == optimum:
            optimal.append(t)
    sums = [(sum((rows[i][a] for i, a in enumerate(t)), F(0)), t) for t in optimal]
    lo, hi = min(sums), max(sums)
    w = welfare(target)
    result = {
        'name': spec['name'], 'customers': sum(n for _, n in types),
        'actual': path, 'actual_payoffs': [str(utility(target, a)) for a in path],
        'actual_realizable_by_some_complete_SPE': bool(realizable),
        'historical_complete_strategy_revalidated': False,
        'welfare': w, 'optimum': optimum, 'optimal_ordered_tuple_count': len(optimal),
        'L_rows': [[str(v) for v in row] for row in rows],
        'Theta': list(map(str, theta)), 'Theta_sum': str(sum(theta)),
        'minimum_optimal_L_sum': str(lo[0]), 'minimum_tuple': lo[1],
        'maximum_optimal_L_sum': str(hi[0]), 'maximum_tuple': hi[1],
        'SM_opt_all_slack': str(lo[0] - (optimum - w)),
        'SM_opt_exists_slack': str(hi[0] - (optimum - w)),
        'TB_slack': str(w + sum(theta) - optimum),
        'count_states': outcomes.cache_info().currsize,
    }
    assert realizable
    expected = spec['expected']
    for key, value in expected.items():
        assert result[key] == value, (spec['name'], key, result[key], value)
    return result


def main():
    base = Path(__file__).resolve().parent
    data = json.loads((base / 'two_saved_inputs.json').read_text())
    result = {
        'scope': 'two existing customer tables; exact child-SPE sets and all optimal ordered tuples',
        'original_main_import_or_random_runs': 0,
        'new_exact_inputs': len(data),
        'results': [audit(s) for s in data],
    }
    (base / 'two_saved_inputs_result.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    hashes = {name: hashlib.sha256((base / name).read_bytes()).hexdigest()
              for name in ['check_two_saved_inputs.py', 'two_saved_inputs.json', 'two_saved_inputs_result.json']}
    (base / 'execution.json').write_text(json.dumps({
        'command': 'python3 archives/customer-attraction/tools/evidence/boss1-resume-threshold/check_two_saved_inputs.py',
        'exit_code': 0, 'hashes': hashes, 'no_original_main_or_module_executed': True,
        'no_original_full_strategy_SPE_scan': True,
    }, indent=2) + '\n')
    print(json.dumps({'new_exact_inputs': len(data), 'checks': 'all passed', 'results': result['results']}, indent=2))


if __name__ == '__main__':
    main()
