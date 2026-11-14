from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
from math import comb
import json
from pathlib import Path
import sys


REPO = Path(sys.argv[1]).resolve()
PACKET = REPO / 'archives/customer-attraction/tools/evidence/R275-credible-search-20261031/original'
LABELS = tuple(range(7))
PLAYERS = 5
MASKS = [mask for mask in range(1 << len(LABELS)) if mask.bit_count() <= PLAYERS]
KEYS = sorted({(mask & 3, (mask >> 2).bit_count()) for mask in MASKS if mask})
ZERO = (F(0),) * len(KEYS)


def read(name, expected_sha):
    file = next(PACKET.glob(name))
    data = file.read_bytes()
    actual_sha = sha256(data).hexdigest()
    assert actual_sha == expected_sha
    return json.loads(data)


def mask_of(actions):
    mask = 0
    for a in actions:
        mask |= 1 << a
    return mask


def counts(actions):
    return tuple(actions.count(a) for a in LABELS)


@cache
def moment(mask):
    if mask == 0:
        return ZERO
    index = KEYS.index((mask & 3, (mask >> 2).bit_count()))
    return ZERO[:index] + (F(1),) + ZERO[index+1:]


def add(*terms):
    return tuple(sum(weight * row[j] for weight, row in terms) for j in range(len(KEYS)))


def dot(row, value):
    return sum(x * y for x, y in zip(row, value))


@cache
def payoff(final, a):
    assert len(final) == PLAYERS and a in final
    other = list(final)
    other.remove(a)
    terms = []
    for k in range(PLAYERS):
        weight = F(1, PLAYERS * comb(PLAYERS - 1, k))
        for predecessor in combinations(other, k):
            before = mask_of(predecessor)
            after = before | (1 << a)
            if before != after:
                terms.extend(((weight, moment(after)), (-weight, moment(before))))
    return add(*terms)


def axiom_rows():
    origins = defaultdict(list)
    for mask in MASKS:
        missing = [a for a in LABELS if not (1 << a) & mask]
        if mask.bit_count() < PLAYERS:
            for a in missing:
                row = add((1, moment(mask | 1 << a)), (-1, moment(mask)))
                origins[row].append(('mono', mask, a))
        if mask.bit_count() + 2 <= PLAYERS:
            for a, b in combinations(missing, 2):
                row = add((1, moment(mask | 1 << a)), (1, moment(mask | 1 << b)),
                          (-1, moment(mask)), (-1, moment(mask | 1 << a | 1 << b)))
                origins[row].append(('submod', mask, a, b))
    return origins


def path_rows(actual):
    origins = defaultdict(list)
    for i, a in enumerate(actual):
        final = tuple(sorted(actual))
        for b in LABELS:
            copied = tuple(sorted(actual[:i] + (b,) * (PLAYERS - i)))
            row = add((1, payoff(final, a)), (-1, payoff(copied, b)))
            if row != ZERO:
                origins[row].append(('path', actual[:i], a, b, final, copied))
    return origins


@cache
def literal_membership(final, a):
    row = []
    for mask in range(1, 1 << len(LABELS)):
        n = sum(bool(mask & (1 << b)) for b in final)
        row.append(F(1, n) if mask & (1 << a) else F(0))
    return tuple(row)


def joint_rows(strategy):
    original = strategy['actions']
    actions = {tuple(item['history']): item['action'] for item in original}
    histories = {h for d in range(PLAYERS) for h in product(LABELS, repeat=d)}
    assert set(actions) == histories and len(actions) == len(original)
    assert set(actions.values()) <= set(LABELS)

    @cache
    def terminal(h):
        return h if len(h) == PLAYERS else terminal(h + (actions[h],))

    origins = defaultdict(list)
    for h in sorted(histories):
        own = actions[h]
        final = tuple(sorted(terminal(h)))
        for b in LABELS:
            if b == own:
                continue
            other = tuple(sorted(terminal(h + (b,))))
            difference = add((1, payoff(final, own)), (-1, payoff(other, b)))
            if literal_membership(final, own) != literal_membership(other, b):
                origins[difference].append(('IC', h, own, b, final, other))
    assert counts(terminal(())) == tuple(strategy['terminal_counts'])
    return terminal(()), origins, actions, terminal


def dual_check(record, rows, w, objective):
    values = tuple(map(F, record['values']))
    assert record['certified'] and record['dual_optimal']
    assert min(values) >= 0 and dot(w, values) == 1
    assert all(dot(row, values) >= 0 for row in rows)
    bound = F(record['dual_bound'])
    assert dot(objective, values) == F(record['value']) == bound
    weights = [(i, F(mu)) for i, mu in record['dual_support']]
    assert all(0 <= i < len(rows) and mu > 0 for i, mu in weights)
    residual = add((bound, w), (-1, objective), *((-mu, rows[i]) for i, mu in weights))
    assert min(residual) >= 0 and dot(residual, values) == 0
    assert all(dot(rows[i], values) == 0 for i, _ in weights)
    return values, residual


def outcomes(values, actual):
    @cache
    def value_pay(final, a):
        return dot(payoff(final, a), values)

    floors = {}

    @cache
    def completions(h):
        if len(h) == PLAYERS:
            return frozenset((h,))
        children = {a: completions(tuple(sorted(h + (a,)))) for a in LABELS}
        threshold = max(min(value_pay(final, a) for final in children[a]) for a in LABELS)
        floors[h] = threshold
        return frozenset(final for a in LABELS for final in children[a]
                         if value_pay(final, a) >= threshold)

    result = completions(())
    actual_final = tuple(sorted(actual))
    failures = []
    for i, a in enumerate(actual):
        h = tuple(sorted(actual[:i]))
        present = actual_final in completions(tuple(sorted(h + (a,))))
        payment = value_pay(actual_final, a)
        if not present or payment < floors[h]:
            failures.append({'prefix_counts': counts(h), 'next_action': a,
                             'target_payoff': payment, 'credible_floor': floors[h],
                             'target_in_selected_child': present})
    return {'root_target_reachable': actual_final in result, 'root_outcomes': len(result),
            'count_states': completions.cache_info().currsize, 'root_threshold': floors[()],
            'onpath_obstructions': failures, 'root_supports': sorted(result)}


def exact():
    joint = read('633*', 'dbf83fe8561340f29505cb33e37c83cf79e521ab2c1bcb4f5dd959d2b0968d6d')
    path = read('19aa*', '977c497839350b22da1d9c043de23db34e77a6f04e9a10e544b80ce41213702c')
    assert [tuple(key) for key in joint['moment_orbits']] == KEYS == [tuple(key) for key in path['moment_orbits']]
    assert joint.get('root_marginal_floor') is None
    ax = axiom_rows()
    assert ZERO not in ax
    record = joint['exact_candidate']
    actual, ir, actions, terminal = joint_rows(record['complete_strategy'])
    assert actual == tuple(joint['milp']['path'])
    jr = path_rows(actual)
    rows = sorted(set(ax) | set(jr) | set(ir))
    w = moment(mask_of(actual))
    objective = moment(mask_of(joint['milp']['portfolio']))
    values, residual = dual_check(record, rows, w, objective)
    slack = Counter(dot(payoff(tuple(sorted(terminal(h))), a), values)
                    - dot(payoff(tuple(sorted(terminal(h + (b,)))), b), values)
                    for h, a in actions.items() for b in LABELS if a != b)
    archived = record['independent_uniform_order_audit']
    assert len(actions) == archived['histories'] and sum(slack.values()) == archived['nonself_deviations']
    assert min(slack) == 0 and slack[0] == archived['ties']
    assert max(dot(moment(mask), values) for mask in MASKS) == dot(objective, values)
    n_coeff = 0
    for final in combinations_with_replacement(LABELS, PLAYERS):
        for a in sorted(set(final)):
            raw = (F(0),) + literal_membership(final, a)
            transformed = [F(0)] * len(KEYS)
            full = (1 << len(LABELS)) - 1
            for mask in range(1, full + 1):
                missing = full ^ mask
                bits = tuple(1 << b for b in LABELS if mask & (1 << b))
                weight = -sum((-1)**k * raw[missing | sum(extra)]
                              for k in range(len(bits) + 1) for extra in combinations(bits, k))
                if mask.bit_count() > PLAYERS:
                    assert weight == 0
                else:
                    transformed = list(add((1, transformed), (weight, moment(mask))))
            assert tuple(transformed) == payoff(final, a)
            n_coeff += 1
    assert n_coeff == joint['coefficient_rows_checked']
    root = outcomes(values, actual)
    assert root['root_target_reachable']
    used = []
    for i, mu in record['dual_support']:
        row = rows[i]
        used.append({'index': i, 'weight': mu, 'row': row, 'axiom': ax.get(row, [None])[0],
                     'path': jr.get(row, [None])[0], 'IC': ir.get(row, [None])[0]})

    results = []
    for r in path['records']:
        rr = sorted(set(ax) | set(path_rows(tuple(r['path']))))
        assert len(rr) == r['rows']
        v, d = dual_check(r, rr, moment(mask_of(r['path'])), moment(mask_of(r['portfolio'])))
        results.append({'path': r['path'], 'portfolio': r['portfolio'], 'value': F(r['value']),
                        'row_count': len(rr), 'nonzero_residual': [(KEYS[i], x) for i, x in enumerate(d) if x]})
    assert len(results) == 30
    best = max(path['records'], key=lambda r: F(r['value']))
    assert F(best['value']) == F(path['best_value'])
    assert (best['path'], best['portfolio']) == (path['best_path'], path['best_portfolio'])
    best_root = outcomes(tuple(map(F, best['values'])), tuple(best['path']))
    actual_results = {k: v for k, v in best_root.items() if k != 'root_supports'}
    assert json.loads(json.dumps(actual_results, default=str)) == path['best_exact_point_credible_completion']
    results_json = {'joint': {'keys': KEYS, 'coefficients': n_coeff, 'unique_rows': len(rows),
                              'axioms': len(ax), 'path_rows': len(jr), 'IC_rows_including_zero': len(ir),
                              'histories': len(actions), 'slack_counts': sorted(slack.items()),
                              'dual_rows': used, 'residual': residual, 'root': root},
                    'path_projection': {'best_root': best_root, 'all_exact_records': results}}
    return results_json, (rows, w, objective, ax, jr, ir)


if __name__ == '__main__':
    data, _ = exact()
    print(json.dumps(data, default=str, indent=2))
