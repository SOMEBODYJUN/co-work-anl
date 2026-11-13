from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import cache
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
from sys import argv

ROOT = Path(argv[1] if len(argv) > 1 else '.').resolve()
ORIGINAL = ROOT / 'archives/customer-attraction/tools/evidence/local-potential-exclusion-complete-certificates-primary/original'
PACKETS = ORIGINAL / 'attack/potential_tax'
PINS = {
    'esm_exact_obstruction.json': '3c083466f35a2ccfbc0451b0536d47dcea16593767691987178b172865a82379',
    'six_esm_embedding.json': '7ac7c0ff8706e598a146b6c0c780990d10c806dd5147fb313a476db79e863185',
    'esm_units_audit.json': 'e722b4c5fa07d00df04c3b4216b8e8799870ea45d8862d361d1d90d3b3e1da1a',
    'six_esm_units_audit.json': '3e3c9c2e2fbb7544b31dbca2c72525d943faf6aee6103210ed741dd3f1ef23a3',
}

def read(path):
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == PINS[path.name], path
    def unique(pairs):
        result = dict(pairs)
        assert len(result) == len(pairs), path
        return result
    return json.loads(raw, object_pairs_hook=unique)

def types(rows, labels):
    result = {}
    for row in rows:
        assert set(row) == {'topics', 'multiplicity'}
        interest = tuple(row['topics'])
        multiplicity = row['multiplicity']
        assert interest == tuple(sorted(set(interest))) and set(interest) <= set(range(labels))
        assert type(multiplicity) is int and multiplicity > 0 and interest not in result
        result[interest] = multiplicity
    return result

def policy(rows, labels, players):
    result = {}
    depth = Counter()
    for row in rows:
        assert set(row) == {'history', 'action'}
        history, action = tuple(row['history']), row['action']
        assert history not in result and type(action) is int and action in range(labels)
        assert all(type(a) is int and a in range(labels) for a in history)
        result[history] = action
        depth[len(history)] += 1
    assert set(result) == {h for d in range(players) for h in product(range(labels), repeat=d)}
    assert depth == {d: labels ** d for d in range(players)}
    return result

def plays(strategy, labels, players):
    leaves = {h: h for h in product(range(labels), repeat=players)}
    for depth in reversed(range(players)):
        for h in product(range(labels), repeat=depth):
            leaves[h] = leaves[(*h, strategy[h])]
    return leaves

def payoff_function(customer_types, labels):
    @cache
    def from_counts(counts):
        reward = [Q(0) for _ in range(labels)]
        for interest, mass in customer_types.items():
            count = sum(counts[a] for a in interest)
            if count:
                for a in interest:
                    reward[a] += Q(mass, count)
        return tuple(reward)

    def payoff(h, a):
        assert a in h
        return from_counts(tuple(h.count(t) for t in range(labels)))[a]
    return payoff

def incentive(strategy, leaves, payoff, labels, redundant=None):
    rows = {}
    depths = Counter()
    for h, a in strategy.items():
        value = payoff(leaves[h], a)
        for deviation in range(labels):
            leaf = leaves[(*h, deviation)]
            slack = value - payoff(leaf, deviation)
            assert slack >= 0, (h, a, deviation, slack)
            rows[h, deviation] = (leaves[h], leaf, slack)
            depths[len(h)] += 1
    if redundant is not None:
        assert len(redundant) == len(rows)
        for item in redundant:
            key = tuple(item['history']), item['action']
            value = (tuple(item['actual_terminal']), tuple(item['deviation_terminal']), Q(item['slack']))
            assert rows.pop(key) == value, key
        assert not rows
    return depths

def static(customer_types, prefix, suffix):
    def background(interest):
        return sum(a in interest for a in prefix)
    def additions(interest):
        return sum(a in interest for a in suffix)
    return sum(mass * sum((Q(1, background(interest) + j) for j in range(1, additions(interest) + 1)), Q(0))
               for interest, mass in customer_types.items())

def cover(customer_types, suffix):
    return sum(mass for interest, mass in customer_types.items() if set(interest).intersection(suffix))

def budget(customer_types, leaves, labels, players):
    result = []
    actual = leaves[()]
    payoff = payoff_function(customer_types, labels)
    for i, a in enumerate(actual):
        h = actual[:i]
        r = players - i
        values = {q: static(customer_types, h, q) for q in combinations_with_replacement(range(labels), r)}
        maximum = max(values.values())
        fixed = max(v for q, v in values.items() if a in q)
        safe = sum(Q(mass, sum(t in interest for t in h) + r) for interest, mass in customer_types.items() if a in interest)
        u = payoff(actual, a)
        incremental = static(customer_types, h, (a,))
        result.append((r, maximum, fixed, u, safe, incremental - safe, u - safe - maximum + fixed))
    total_u = sum(row[3] for row in result)
    total_tax = sum(row[5] for row in result)
    assert total_u == cover(customer_types, actual)
    assert sum(row[-1] for row in result) == total_u + total_tax - result[0][1]
    assert sum(row[1]-row[2] for row in result) == result[0][1] - static(customer_types, (), actual)
    return result

def menu(customer_types, leaves, prefix, r, labels, *, report=True):
    payoff = payoff_function(customer_types, labels)
    actual = leaves[prefix]
    a = actual[len(prefix)]
    u = payoff(actual, a)
    optimum = max(static(customer_types, prefix, q) for q in product(range(labels), repeat=r))
    safe = sum(Q(mass, sum(t in interest for t in prefix) + r)
               for interest, mass in customer_types.items() if a in interest)
    results = []
    for t in range(labels):
        leaf = leaves[(*prefix, t)]
        tail = leaf[len(prefix)+1:]
        ell = optimum - static(customer_types, prefix, (t, *tail))
        gamma = u - payoff(leaf, t)
        g = sum(Q(mass, 1 + sum(x in interest for x in (*prefix, *tail)))
                for interest, mass in customer_types.items() if a in interest)
        margin = ell - gamma - (g - safe)
        results.append(margin)
        if report:
            print('menu', name(prefix), name((t,)), name(leaf), str(ell), str(gamma), str(g-safe), str(margin))
    return results

def name(h):
    return ''.join('ABCDEF'[a] for a in h) or '∅'

def print_table(rows):
    for row in rows:
        print(*(str(a) for a in row))

def parametric(strategy, leaves, old):
    old_payoff = payoff_function(old, 6)
    def affine(h, a):
        return (Q(0), Q(1, h.count(5))) if a == 5 else (old_payoff(h, a), Q(0))
    lower_all, upper_all = [], []
    for h, a in strategy.items():
        c0, c1 = affine(leaves[h], a)
        for t in range(6):
            dev = leaves[(*h, t)]
            d0, d1 = affine(dev, t)
            b, k = c0-d0, c1-d1
            witness = (name(h), name((a,)), name((t,)), name(leaves[h]), name(dev), str(b), str(k))
            if k > 0:
                bound = -b / k
                lower_all.append((bound, witness))
            elif k < 0:
                bound = -b / k
                upper_all.append((bound, witness))
            else:
                assert b >= 0, witness
    lower = max(b for b, _ in lower_all)
    upper = min(b for b, _ in upper_all)
    print('fixed_policy_parameter_interval', str(lower), str(upper))
    lower_tight = [w for b, w in lower_all if b == lower]
    upper_tight = [w for b, w in upper_all if b == upper]
    print('lower_tight', len(lower_tight), lower_tight[0])
    print('upper_tight', len(upper_tight), upper_tight[0])
    print('positive_slope_negative_slope_zero_slope_IC_rows', len(lower_all), len(upper_all),
          6 * len(strategy) - len(lower_all) - len(upper_all))
    return lower, upper

three = read(PACKETS / 'esm_exact_obstruction.json')
six = read(PACKETS / 'six_esm_embedding.json')
audit3 = read(ORIGINAL / 'review/esm_units_audit.json')
audit6 = read(ORIGINAL / 'review/six_esm_units_audit.json')
assert audit3['source_sha256'] == PINS['esm_exact_obstruction.json']
assert audit6['packet_sha256'] == PINS['six_esm_embedding.json']
old = types(three['customers'], 5)
assert sum(old.values()) == 621 and len(old) == 11
new = types(six['instance']['customers'], 6)
assert new == {**old, (5,): 510}
strateg3 = policy(three['strategy'], 5, 3)
strateg6 = policy(six['strategy'], 6, 6)
assert strateg3 == {(): three['root_action'], **{(i,): a for i,a in enumerate(three['second_actions'])},
                   **{(i,j): a for i,row in enumerate(three['last_actions']) for j,a in enumerate(row)}}
leaves3 = plays(strateg3, 5, 3)
leaves6 = plays(strateg6, 6, 6)
assert leaves3[()] == tuple(three['actual_path']) == (0,1,2)
assert leaves6[()] == tuple(six['actual_path']) == (5,5,5,0,1,2)
assert tuple(six['examined_prefix']) == (5,5,5) and six['examined_action'] == 0 and six['remaining'] == 3
print('frozen_IC_counts', incentive(strateg3, leaves3, payoff_function(old, 5), 5, three['IC_rows']),
      incentive(strateg6, leaves6, payoff_function(new, 6), 6))
for customer_types, labels in ((old,5), (new,6)):
    covers = {tuple(interest for interest in customer_types if a in interest) for a in range(labels)}
    assert len(covers) == labels
counts_to_actions = defaultdict(set)
for h, a in strateg6.items():
    counts_to_actions[tuple(h.count(i) for i in range(6))].add(a)
assert sum(len(v) > 1 for v in counts_to_actions.values()) == 22
print('three_budget r P P_A u safe tax margin')
bud3 = budget(old, leaves3, 5, 3)
print_table(bud3)
print('six_budget r P P_A u safe tax margin')
bud6 = budget(new, leaves6, 6, 6)
print_table(bud6)
assert tuple(row[-1] for row in bud3) == (Q(-1), Q(139,2), Q(0))
assert bud6[-3:] == bud3
for j in range(6):
    if j+1 < 6:
        print('adjacent_margin', j+1, str(bud6[j][-1] + bud6[j+1][-1]))
for i in range(6):
    print('tail_margin', i+1, str(sum(row[-1] for row in bud6[i:])))
for c, label, pl in ((old,5,3), (new,6,6)):
    print('OPT',pl,max(cover(c,q) for q in combinations_with_replacement(range(label),pl)))
for c, p, n in ((old, (), 5), (new, (5,5,5), 6)):
    val = {q: static(c,p,q) for q in product(range(n), repeat=3)}
    assert max(val.values()) == 801 and max(v for q,v in val.items() if 0 in q) == 754
    print('static_ordered_comparisons', name(p), len(val))
    print('ordered_maximizers', name(p), sorted({name(tuple(sorted(q))) for q,v in val.items() if v == 801}),
          sorted({name(tuple(sorted(q))) for q,v in val.items() if v == 754 and 0 in q}))
assert menu(old, leaves3, (), 3, 5) == [1, 5, 5, 5, 1]
assert menu(new, leaves6, (5,5,5), 3, 6) == [1, 5, 5, 5, 1, 5]
old_payoff = payoff_function(old, 5)
old_floor = min(old_payoff(leaves3[h], a) for h, a in strateg3.items())
assert old_floor == 166
print('old_history_payoff_floor', old_floor)
lower0, upper0 = parametric(strateg6, leaves6, old)
restored = dict(strateg6)
for h,a in strateg3.items():
    g = (5,5,5,*h)
    if restored[g] != a:
        print('literal_change', name(g), name((restored[g],)), name((a,)))
    restored[g] = a
restored_leaves = plays(restored, 6, 6)
print('changed_completion_histories', [(name(h), name(leaves6[h]), name(z)) for h,z in restored_leaves.items() if leaves6[h] != z])
assert restored_leaves[()] == leaves6[()]
print('literal_restored_IC_counts', incentive(restored, restored_leaves, payoff_function(new, 6), 6))
lower1, upper1 = parametric(restored, restored_leaves, old)
assert (lower0, upper0) == (lower1, upper1) == (Q(1017, 2), Q(516))
assert upper1 / 4 < old_floor
print('changed_IC_terminal_counts', sum(
    (leaves6[h], leaves6[(*h, t)]) != (restored_leaves[h], restored_leaves[(*h, t)])
    for h in strateg6 for t in range(6)))
for h in strateg3:
    g = (5, 5, 5, *h)
    dev = restored_leaves[(*g, 5)]
    assert dev == leaves6[(*g, 5)] and dev.count(5) >= 4
print('new_F_deviation_final_F_loads', dict(sorted(Counter(
    restored_leaves[(5, 5, 5, *h, 5)].count(5) for h in strateg3).items())))

def expected_budget(J):
    return [(6, 801 + Q(11, 6) * J, 801 + Q(11, 6) * J, J / 3, J / 6, Q(5, 6) * J, J / 6),
            (5, 801 + Q(5, 6) * J, 801 + Q(5, 6) * J, J / 3, J / 6, J / 3, J / 6),
            (4, 801 + J / 3, 801 + J / 3, J / 3, J / 6, J / 6, J / 6), *bud3]

# Each static candidate's difference from the proposed optimum is affine in J.
# The same feasible candidates attain each proposed maximum throughout the interval.
for J in (lower1, Q(509), Q(510), upper1):
    customer_types = {**old, (5,): J}
    assert budget(customer_types, restored_leaves, 6, 6) == expected_budget(J)
    assert max(static(customer_types, (5,5,5), q) for q in product(range(6), repeat=2)) == 597
    for completed in (leaves6, restored_leaves):
        assert menu(customer_types, completed, (5,5,5), 3, 6, report=False) == [1, 5, 5, 5, 1, 5]
    unconstrained_winners = [(5,5,5,1,2,3), (5,5,1,2,3), (5,1,2,3), (1,2,3), (1,2), (2,)]
    forced_winners = [*unconstrained_winners[:3], (0,1,2), *unconstrained_winners[4:]]
    for i, (unconstrained, forced) in enumerate(zip(unconstrained_winners, forced_winners)):
        h = leaves6[()][:i]
        suffixes = list(combinations_with_replacement(range(6), 6 - i))
        row = expected_budget(J)[i]
        actual = leaves6[()][i]
        assert actual in forced
        assert static(customer_types, h, unconstrained) == row[1] == max(
            static(customer_types, h, q) for q in suffixes)
        assert static(customer_types, h, forced) == row[2] == max(
            static(customer_types, h, q) for q in suffixes if actual in q)
    print('parameter_endpoint_budget', J, 'P6', expected_budget(J)[0][1],
          'W', 546+J, 'C', Q(647,2)+Q(4,3)*J, 'balance', Q(137,2)+J/2)
for J in (Q(508), Q(517)):
    h = (0,3,3) if J < lower1 else (0,0,3,5,5)
    a = strateg6[h]
    t = 1 if J < lower1 else 5
    old_new_payoff = payoff_function({**old, (5,): J}, 6)
    slack = old_new_payoff(leaves6[h], a) - old_new_payoff(leaves6[(*h,t)], t)
    assert slack < 0
    print('outside_integer_boundary', J, name(h), str(slack))
old_potentials = [max(static(old, (), q) for q in combinations_with_replacement(range(5), i))
                  for i in range(7)]
assert old_potentials == [0, 360, 597, 801, Q(1861,2), Q(2079,2), Q(2283,2)]
print('old_empty_background_potentials', [str(x) for x in old_potentials])
assert old_potentials[3] - old_potentials[2] - bud3[0][3] == 38
