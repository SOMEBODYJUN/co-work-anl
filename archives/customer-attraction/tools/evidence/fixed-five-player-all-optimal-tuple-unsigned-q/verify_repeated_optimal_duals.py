"""Replay the exact rational certificates for all pointwise-failing repeated tuples.

Run from any directory as: python -B verify_repeated_optimal_duals.py REPO CERTIFICATE.
The certificate lists weights on lexicographically ordered nonzero distinct IC rows.
"""
import json
import sys
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path

LABELS = tuple(range(7))
MASKS = tuple(range(1, 128))
POSITIONS = tuple(range(5))
SCALE = 60
ORIGINALS = Path('archives/customer-attraction/tools/evidence/whole-subtree-nine-endpoints-primary/original')
POLICIES = {
    'sigma252': ('m5p7_residual.json', '2a154303b023acfdc7b09c8576f63b3acb50abb02bd8e3cca6a793152ad07233', (0, 0, 0, 1, 1)),
    'sigma48': ('m5p7_reentry_incumbent_half.json', 'e6269ea7551820d0d2c6192dd96d60b7bd2ce1f92b6ffd463fd8a13f89da0565', (0, 1, 0, 1, 0)),
}


def load(mask, path):
    return sum(bool(mask & (1 << a)) for a in path)


def digits(path):
    return ''.join(str(a) for a in path)


def payoff_row(a, leaf):
    return tuple(SCALE // load(mask, leaf) if mask & (1 << a) else 0 for mask in MASKS)


def read_strategy(root, spec):
    name, digest, expected_actual = spec
    raw = (root / ORIGINALS / name).read_bytes()
    assert sha256(raw).hexdigest() == digest
    entries = json.loads(raw)['exact']['strategy']['actions']
    actions = {tuple(entry['history']): entry['action'] for entry in entries}
    assert len(actions) == len(entries)
    layers = [list(product(LABELS, repeat=i)) for i in range(6)]
    assert set(actions) == {h for layer in layers[:-1] for h in layer}
    assert all(a in LABELS for a in actions.values())
    leaves = {h: h for h in layers[-1]}
    for layer in reversed(layers[:-1]):
        for history in layer:
            leaves[history] = leaves[history + (actions[history],)]
    assert leaves[()] == expected_actual
    return actions, leaves, expected_actual


def replay_policy(root, spec, certificates):
    actions, leaves, actual = read_strategy(root, spec)
    ic_rows = set()
    for h, a in actions.items():
        played = payoff_row(a, leaves[h])
        for b in LABELS:
            if b == a:
                continue
            deviation = payoff_row(b, leaves[h + (b,)])
            ic_rows.add(tuple(v - u for u, v in zip(played, deviation, strict=True)))
    ic_rows.discard((0,) * len(MASKS))
    ordered_ics = sorted(ic_rows)

    forced = {(i, a): payoff_row(a, leaves[actual[:i] + (a,)])
              for i in POSITIONS for a in LABELS}
    c = {mask: load(mask, actual) for mask in MASKS}
    used = set()
    pointwise = Counter()
    cone = Counter()
    ic_terms = order_terms = type_checks = 0
    nonempty_positive_cones = 0
    min_residual = None
    for slots in combinations_with_replacement(LABELS, len(POSITIONS)):
        support_size = len(set(slots))
        accepting_masks = [mask for mask in MASKS if load(mask, slots) > 0]
        q = {mask: SCALE * load(mask, slots) // (1 + c[mask]) for mask in accepting_masks}
        prices = {}
        for order in sorted(set(permutations(slots))):
            prices[order] = tuple(sum(forced[i, a][mask - 1] for i, a in enumerate(order)) - q[mask]
                                  for mask in accepting_masks)
        if any(min(row) >= 0 for row in prices.values()):
            pointwise[support_size] += 1
            continue

        assert support_size < len(POSITIONS)
        key = digits(slots)
        record = certificates[key]
        assert set(record) == {'IC', 'orders'}
        used.add(key)
        cone[support_size] += 1
        ics = {int(i): Fraction(weight) for i, weight in record['IC'].items()}
        orders = {tuple(map(int, order)): Fraction(weight) for order, weight in record['orders'].items()}
        assert all(0 <= i < len(ordered_ics) and weight > 0 for i, weight in ics.items())
        assert all(order in prices and weight > 0 for order, weight in orders.items())
        assert sum(orders.values()) == 1
        ic_terms += len(ics)
        order_terms += len(orders)
        for j, mask in enumerate(accepting_masks):
            remainder = sum(weight * ordered_ics[i][mask - 1] for i, weight in ics.items())
            remainder += sum(weight * prices[order][j] for order, weight in orders.items())
            assert remainder >= 0, (key, mask, remainder)
            min_residual = remainder if min_residual is None else min(min_residual, remainder)
            type_checks += 1
        # The all-label type is a positive-W SPE point: all labels pay equally.
        # Here every actual load is five and every order pays one, while Q is 5/6.
        # It certifies that the nonzero restricted cones are genuine, not empty.
        assert MASKS[-1] in accepting_masks
        assert all(row[-1] == 0 for row in ordered_ics)
        assert q[MASKS[-1]] == 50 and all(row[-1] == 10 for row in prices.values())
        nonempty_positive_cones += 1
    assert min_residual >= Fraction(SCALE, 27)
    assert used == set(certificates)
    assert sum(pointwise.values()) + sum(cone.values()) == 462
    return {'actual': digits(actual), 'nonzero_distinct_ic_rows': len(ordered_ics),
            'pointwise_counts': pointwise, 'cone_dual_counts': cone,
            'ic_terms': ic_terms, 'order_terms': order_terms, 'dual_type_checks': type_checks,
            'least_scaled_dual_residual': str(min_residual),
            'nonzero_cones_verified_with_all_label_type': nonempty_positive_cones}


def main():
    root = Path(sys.argv[1])
    certificates = json.loads(Path(sys.argv[2]).read_text())
    assert set(certificates) == set(POLICIES)
    result = {key: replay_policy(root, spec, certificates[key]) for key, spec in POLICIES.items()}
    assert {key: sum(row['cone_dual_counts'].values()) for key, row in result.items()} == {
        'sigma252': 110, 'sigma48': 103,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
