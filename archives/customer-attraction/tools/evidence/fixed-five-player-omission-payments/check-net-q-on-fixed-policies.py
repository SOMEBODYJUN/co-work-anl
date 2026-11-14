"""Verify the stronger net-Q matching for both frozen policy cones."""
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

from verify_fixed_omission import LABELS, MASKS, PLAYERS, POLICIES, label_mask, read_policy


def pays(leaves, actual, support):
    support_mask = label_mask(support)
    targets = []
    for mask in MASKS:
        load = sum(bool(mask & (1 << a)) for a in actual)
        multiplicity = (mask & support_mask).bit_count()
        targets.append(Fraction(multiplicity, 1 + load) - int(load > 0 and multiplicity == 0))
    true = {(i, a): leaves[actual[:i] + (a,)] for i in range(PLAYERS) for a in support}
    price = {}
    for (i, a), leaf in true.items():
        for mask in MASKS:
            price[i, a, mask] = (Fraction(1, sum(bool(mask & (1 << b)) for b in leaf))
                                  if mask & (1 << a) else Fraction(0))
    result = []
    for order in permutations(support):
        slack = [sum(price[i, a, mask] for i, a in enumerate(order)) - target
                 for mask, target in zip(MASKS, targets, strict=True)]
        if min(slack) >= 0:
            result.append((order, slack))
    assert result, (actual, support)
    order, slack = result[0]
    return {'support': support, 'paying_count': len(result), 'order': order,
            'true_leaves': [true[i,a] for i,a in enumerate(order)], 'slacks': list(map(str,slack))}


def main(root):
    results = {}
    for name, spec in POLICIES.items():
        _, leaves, _, actual, _ = read_policy(root, spec)
        rows = [pays(leaves, actual, support) for support in combinations(LABELS, PLAYERS)]
        assert len(rows) == 21 and min(x['paying_count'] for x in rows) >= 4
        assert sum(x['paying_count'] for x in rows) == {'sigma252':432,'sigma48':402}[name]
        results[name] = rows
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main(Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd())
