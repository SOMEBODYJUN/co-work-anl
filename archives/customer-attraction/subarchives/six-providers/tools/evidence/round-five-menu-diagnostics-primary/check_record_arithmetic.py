"""Check frozen proposal arithmetic only; no SPE enumeration or optimizer import.

The reported child attainability, pair minima, and floating optimization bounds
are deliberately outside this checker. Inputs are the exact original JSONLs and
the two frozen example instances kept beside them.
"""
from collections import Counter
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def compositions(total, width):
    if width == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, width - 1):
                yield (first,) + tail


def load(name):
    return json.loads((HERE / 'related' / name).read_text())


def customers(ins):
    return [(tuple(c['topics']), c.get('multiplicity', 1)) for c in ins['customers']]


def pay(ins, counts, action):
    return sum((F(mult, sum(counts[a] for a in liked))
                for liked, mult in customers(ins) if action in liked), F())


def query(ins, counts, p):
    return sum((mult * sum((p[a] for a in liked), F()) /
                (1 + sum(counts[a] for a in liked))
                for liked, mult in customers(ins)), F())


def welfare(ins, counts):
    return sum(mult for liked, mult in customers(ins)
               if any(counts[a] for a in liked))


def checked_menu_proposal(ins, record):
    path = record['path']
    n, m = len(ins['topics']), ins['players']
    counts = tuple(path.count(a) for a in range(n))
    p = tuple(map(F, record['p']))
    assert len(path) == m and len(p) == n
    assert all(v >= 0 for v in p) and sum(p) == 1
    assert record['W'] == welfare(ins, counts)
    assert tuple(map(F, record['payoffs'])) == tuple(pay(ins, counts, a) for a in path)
    choices = {tuple(map(int, key.split(','))): tuple(z)
               for key, z in record['choices'].items()}
    assert set(choices) == {(i, a) for i in range(m)
                            for a in range(n) if a != path[i]}
    psi = []
    for i in range(m):
        cols = [counts]
        for (ii, a), z in choices.items():
            if ii != i:
                continue
            assert len(z) == n and sum(z) == m and all(v >= 0 for v in z)
            forced_prefix = path[:i] + [a]
            assert all(z[t] >= forced_prefix.count(t) for t in range(n))
            assert pay(ins, z, a) <= F(record['payoffs'][i])
            cols.append(z)
        psi.append(min(query(ins, z, p) for z in cols))
    assert psi == list(map(F, record['psi']))
    gap = sum(psi, F()) - record['W']
    assert gap == F(record['gap'])
    assert abs(float(gap) - record['numeric_gap']) < 1e-12
    return {'path': path, 'welfare': record['W'], 'query': record['p'],
            'psi': list(map(str, psi)), 'gap': str(gap),
            'offpath_choices': len(choices),
            'prefix_count_and_current_payoff_caps_checked': True,
            'SPE_child_membership_recomputed': False}


aggregate = [json.loads(s) for s in
             (HERE / 'original' / 'aggregate_theta_diagnostic.jsonl').read_text().splitlines()]
assert len(aggregate) == 3 and aggregate[0]['done'] == 1 and aggregate[1]['done'] == 7
assert aggregate[-1]['paths_checked'] == 48
assert aggregate[1]['new_best'] == aggregate[-1]['best']
menu_checks = [checked_menu_proposal(load('aggregate_theta_failure.json'), r['new_best'])
               for r in aggregate[:-1]]

pair_log = [json.loads(s) for s in
            (HERE / 'original' / 'pair_five_individual_diagnostic.jsonl').read_text().splitlines()]
assert len(pair_log) == 2 and pair_log[0]['checked'] == 1
report = pair_log[-1]
ins = load('five_individual_security.json')
n, m = len(ins['topics']), ins['players']
rows = report['rows']
expected_bg = [bg for depth in range(m - 2) for bg in compositions(depth, n)]
assert len(rows) == report['backgrounds_checked'] == len(expected_bg) == 66
assert pair_log[0]['best'] == report['best'] == rows[0]
checked = []
static_evaluations = 0
for idx, (record, bg) in enumerate(zip(rows, expected_bg)):
    assert tuple(record['background']) == bg
    r = m - sum(bg)
    assert r == record['remaining'] >= 3
    z = tuple(record['terminal'])
    assert len(z) == n and sum(z) == m and all(v >= 0 for v in z)
    a, b = record['pair_actions']
    assert all(z[t] >= bg[t] + (a == t) + (b == t) for t in range(n))
    pair = pay(ins, z, a) + pay(ins, z, b)
    assert pair == F(record['pair_min'])
    p = tuple(map(F, record['query']))
    assert len(p) == n and all(v >= 0 for v in p) and sum(p) == 1
    prices = [query(ins, tuple(bg[t] + q[t] for t in range(n)), p)
              for q in compositions(r, n)]
    count = comb(r + n - 1, n - 1)
    assert len(prices) == record['static_count'] == count
    val = min(prices)
    assert val == F(record['security_lower'])
    margin = pair - 2 * val
    assert margin == F(record['margin_pair_minus_2lower'])
    assert margin > 0
    static_evaluations += count
    checked.append({'row_zero_based': idx, 'background': list(bg), 'remaining': r,
                    'pair_payoff_at_saved_terminal': str(pair),
                    'feasible_query_security_lower': str(val), 'margin': str(margin),
                    'static_count': count,
                    'pair_minimum_over_all_SPE_recomputed': False})
assert min(F(row['margin']) for row in checked) == F(report['best']['margin_pair_minus_2lower'])
out = {'scope': 'exact arithmetic of frozen proposals; no optimizer or SPE solver',
       'original_program_entries': 0, 'optimizer_calls': 0, 'SPE_solver_calls': 0,
       'menu_records': 3, 'menu_distinct_saved_proposals': menu_checks,
       'pair_records': 2, 'pair_rows_checked': len(checked),
       'pair_background_depth_counts': dict(Counter(sum(row['background']) for row in checked)),
       'pair_static_query_evaluations': static_evaluations,
       'minimum_saved_pair_minus_twice_feasible_lower': report['best']['margin_pair_minus_2lower'],
       'not_certified': ['MILP optimality or an upper bound for U',
                         'full-history membership of saved offpath terminal counts',
                         'minimum pair payoff over all SPE continuations',
                         'optimal security values or PB at the 66 backgrounds'],
       'pair_rows': checked}
(HERE / 'record-arithmetic-check.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: v for k, v in out.items()
                  if k not in ('pair_rows', 'menu_distinct_saved_proposals')}, indent=2))
