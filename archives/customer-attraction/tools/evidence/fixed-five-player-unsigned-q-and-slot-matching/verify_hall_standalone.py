"""Compare exact matching orders for the two given full action tables."""
import json
from collections import Counter
from itertools import combinations_with_replacement, permutations
from hashlib import sha256
from itertools import product
from json import loads
from math import lcm
from pathlib import Path
from sys import argv

ROOT = Path(argv[1])
ORIGINALS = ROOT / 'archives/customer-attraction/tools/evidence/whole-subtree-nine-endpoints-primary/original'
LABELS = range(7)
TYPES = range(1, 128)
POSITIONS = range(5)
SCALE = lcm(*range(1, 7))
SPECS = {
    'sigma252': ('m5p7_residual.json', '2a154303b023acfdc7b09c8576f63b3acb50abb02bd8e3cca6a793152ad07233', (0, 0, 0, 1, 1)),
    'sigma48': ('m5p7_reentry_incumbent_half.json', 'e6269ea7551820d0d2c6192dd96d60b7bd2ce1f92b6ffd463fd8a13f89da0565', (0, 1, 0, 1, 0)),
}


def load_table(spec):
    filename, digest, intended_actual = spec
    raw = (ORIGINALS / filename).read_bytes()
    assert sha256(raw).hexdigest() == digest
    exact = loads(raw)['exact']
    entries = exact['strategy']['actions']
    actions = {tuple(entry['history']): entry['action'] for entry in entries}
    assert len(entries) == len(actions)
    assert set(actions) == {h for i in POSITIONS for h in product(LABELS, repeat=i)}
    assert all(a in LABELS for a in actions.values())

    def complete(h):
        while len(h) < 5:
            h += (actions[h],)
        return h

    actual = complete(())
    assert actual == intended_actual
    leaves = {(i, a): complete(actual[:i] + (a,)) for i in POSITIONS for a in LABELS}
    return actual, leaves, exact['integer_clones']


def hit(mask, a):
    return bool(mask & (1 << a))


def load(mask, h):
    return sum(hit(mask, a) for a in h)


def rows(actual, leaves, support):
    for mask in TYPES:
        c = load(mask, actual)
        d = load(mask, support)
        threshold = SCALE * d // (1 + c) - SCALE * (c > 0 and d == 0)
        payoff = {(i, a): SCALE // load(mask, leaf) if hit(mask, a) else 0
                  for (i, a), leaf in leaves.items() if a in support}
        yield mask, threshold, payoff



def digits(support):
    return ''.join(map(str, support))


EXTERNAL = {2, 3, 4, 5, 6}
EXPECTED_POSITIONS = {
    'sigma252': {2: [4, 5], 3: [2, 3, 4, 5], 4: [2, 4, 5], 5: [2, 4, 5], 6: [1, 2, 3, 4, 5]},
    'sigma48': {2: [2, 4, 5], 3: [1, 3, 5], 4: [4, 5], 5: [1, 2, 3, 5], 6: [2, 4, 5]},
}
EXPECTED_COUNTS = {
    'sigma252': {1: 3, 2: 48, 3: 153, 4: 127, 5: 21},
    'sigma48': {1: 2, 2: 46, 3: 162, 4: 128, 5: 21},
    'both': {1: 2, 2: 26, 3: 86, 4: 88, 5: 18},
}


def check_rows(actual, leaves):
    eligible = {a: [] for a in LABELS}
    deltas = []
    for (i, a), leaf in leaves.items():
        external = [b for b in leaf if b in EXTERNAL]
        admissible = a in (0, 1) or external == [a]
        delta = [leaf.count(b) - actual.count(b) for b in LABELS]
        bound = delta[a] + sum(max(0, delta[b]) for b in LABELS if b != a)
        if admissible:
            eligible[a].append(i + 1)
            assert bound <= 1
        else:
            b = next(b for b in EXTERNAL if b != a and b in leaf) if leaf.count(a) == 1 else a
            mask = (1 << a) | (1 << b)
            assert load(mask, actual) == 0 and load(mask, leaf) >= 2
        deltas.append({'position': i + 1, 'query': a, 'leaf': digits(leaf),
                       'max_load_increase_for_type_accepting_query': bound,
                       'eligible': admissible})
    return eligible, deltas


def verified_orders(table, support):
    actual, leaves, _ = table
    # In this calculation support is a tuple of five slots, so duplicates are counted.
    checks = list(rows(actual, leaves, support))
    for order in sorted(set(permutations(support))):
        pay = [sum(payoff[i, a] for i, a in enumerate(order)) for _, _, payoff in checks]
        net = all(value >= threshold for value, (_, threshold, _) in zip(pay, checks, strict=True))
        unsigned = all(value >= SCALE * load(mask, support) // (1 + load(mask, actual))
                       for value, mask in zip(pay, TYPES, strict=True))
        assert net == unsigned
        if unsigned:
            yield order


def main():
    tables = {key: load_table(spec) for key, spec in SPECS.items()}
    eligible, row_details = {}, {}
    for key, (actual, leaves, _) in tables.items():
        eligible[key], row_details[key] = check_rows(actual, leaves)
        assert {a: eligible[key][a] for a in EXTERNAL} == EXPECTED_POSITIONS[key]
        assert all(eligible[key][a] == [1, 2, 3, 4, 5] for a in (0, 1))
    eligible['both'] = {a: sorted(set(eligible['sigma252'][a]) & set(eligible['sigma48'][a]))
                        for a in LABELS}

    counts = {key: Counter() for key in eligible}
    distinct_supports = {}
    orders_checked_per_policy = 0
    multisets_checked_per_policy = 0
    for slots in combinations_with_replacement(LABELS, 5):
        multisets_checked_per_policy += 1
        all_orders = sorted(set(permutations(slots)))
        orders_checked_per_policy += len(all_orders)
        admissible_orders = {}
        for key, positions in eligible.items():
            admissible_orders[key] = [p for p in all_orders
                                      if all(i in positions[a] for i, a in enumerate(p, start=1))]
            if admissible_orders[key]:
                counts[key][len(set(slots))] += 1
            if key in tables:
                assert list(verified_orders(tables[key], slots)) == admissible_orders[key]
        if len(set(slots)) == 5:
            distinct_supports[digits(slots)] = {
                key: {'count': len(orders), 'first': digits(orders[0]) if orders else None}
                for key, orders in admissible_orders.items()
            }

    assert counts == EXPECTED_COUNTS
    assert orders_checked_per_policy == 7**5
    assert multisets_checked_per_policy == 462
    assert [J for J, records in distinct_supports.items() if not records['both']['count']] == [
        '02456', '12456', '23456']
    output = {'actual_paths': {k: digits(v[0]) for k, v in tables.items()},
              'eligible_positions': eligible,
              'exact_forced_rows': row_details,
              'distinct_supports': distinct_supports,
              'multiset_counts_by_distinct_support_size': counts,
              'orders_checked_per_policy': orders_checked_per_policy,
              'multisets_checked_per_policy': multisets_checked_per_policy,
              'types_checked_per_order': len(TYPES)}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
