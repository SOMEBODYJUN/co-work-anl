"""Independently audit the exact frozen-policy omission proof without mutating the clone."""
import hashlib
import itertools
import json
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
task_id = 'boss3-wave8-new-3a-d5f9ded3c8d9a47c'
definition = json.loads((root / f'research/operations/map-v2/tasks/{task_id}.json').read_text())['definition']
registry = json.loads((root / 'research/registry.json').read_text())
ids = (definition['object_ids'][0], 'cag-whole-subtree-nine-exact-endpoints-and-reentry', 'M-b97a40a962c34f848cc8dcaf8b05a1f1')
refs = {item['path']: item['sha256'] for item in definition['context_plan']['reading_refs']}
for obj in registry['objects']:
    if obj['object_id'] in ids:
        for item in [obj['body'], *obj['evidence']]:
            assert item['path'] not in refs or item['sha256'] == refs[item['path']]
            refs[item['path']] = item['sha256']
for filename, expected in refs.items():
    assert hashlib.sha256((root / filename).read_bytes()).hexdigest() == expected

base = root / 'archives/customer-attraction/tools/evidence'
endpoints = base / 'whole-subtree-nine-endpoints-primary/original'
certificate = json.loads((base / 'fixed-five-player-omission-payments/fixed_omission_exact.json').read_text())
labels = tuple(range(7))
players = 5
masks = range(1, 128)
mask_labels = {mask: {a for a in labels if mask & (1 << a)} for mask in masks}
omitted = [mask for mask, member_labels in mask_labels.items() if member_labels.isdisjoint({0, 1})]
assert omitted == certificate['omitted_masks']
assert certificate['scale'] == 60
support_list = list(itertools.combinations(labels, players))
sharp = [3 if mask == 1 else 2 if mask == 2 else 1 if mask in (4, 8, 16, 32, 64) else 0 for mask in masks]


def audit_policy(policy_key, filename, expected_path, full_order):
    source = json.loads((endpoints / filename).read_text())
    data = source['exact']
    counts = data['integer_clones']
    entries = data['strategy']['actions']
    actions = {tuple(row['history']): row['action'] for row in entries}
    assert len(entries) == len(actions) == sum(len(labels)**depth for depth in range(players))
    assert set(actions) == {h for depth in range(players) for h in itertools.product(labels, repeat=depth)}
    assert set(actions.values()) <= set(labels)
    assert len(counts) == len(masks) and all(type(value) is int and value >= 0 for value in counts)

    @lru_cache(None)
    def finish(prefix):
        while len(prefix) < players:
            prefix += (actions[prefix],)
        return prefix

    @lru_cache(None)
    def share(a, z, mask):
        member_labels = mask_labels[mask]
        if a not in member_labels:
            return Fraction()
        return Fraction(1, sum(t in member_labels for t in z))

    actual = finish(())
    saved = certificate['policies'][policy_key]
    assert actual == expected_path == tuple(saved['actual'])
    assert data['strategy']['terminal_counts'] == [actual.count(a) for a in labels]
    forced = {(i, a): finish(actual[:i] + (a,)) for i in range(players) for a in labels}
    row = {(i, a): [share(a, forced[i, a], b) for b in masks] for i in range(players) for a in labels}

    def paid(order, mask):
        return sum(row[i, a][mask - 1] for i, a in enumerate(order))

    def audit_row(record, order, surplus):
        assert tuple(record['order']) == order
        assert record['true_leaves'] == [list(forced[i, a]) for i, a in enumerate(order)]
        assert record['slack_times_60'] == [60 * slack for slack in surplus]

    assert all(forced[i, a].count(t) <= 1 for i, a in enumerate(full_order) for t in range(2, 7))
    audit_row(saved['full_omission'], full_order, [paid(full_order, b) - 1 for b in omitted])
    assert min(saved['full_omission']['slack_times_60']) == 0
    assert [tuple(r['support']) for r in saved['all_supports']] == support_list
    total_paying = 0
    q_difference = None
    for record, support in zip(saved['all_supports'], support_list, strict=True):
        support_set = set(support)
        demand = {b: int(not mask_labels[b].isdisjoint(support_set)) for b in omitted}
        paying = []
        for order in itertools.permutations(support):
            slack = [paid(order, b) - demand[b] for b in omitted]
            if min(slack) >= 0:
                paying.append((order, slack))
        assert len(paying) == record['paying_order_count']
        total_paying += len(paying)
        order, slack = paying[0]
        audit_row(record, order, slack)
        for mask in masks:
            d = len(mask_labels[mask] & support_set)
            c = sum(a in mask_labels[mask] for a in actual)
            required = Fraction(d, 1+c) - int(c > 0 and d == 0)
            if q_difference is None and paid(order, mask) < required:
                q_difference = dict(support=support, order=order, mask=mask, paid=str(paid(order, mask)), required=str(required), actual_load=c, comparison_load=d)

    def point(masses):
        positive = [(b, n) for b, n in zip(masks, masses, strict=True) if n]

        @lru_cache(None)
        def payoff(z, a):
            return sum((n * share(a, z, b) for b, n in positive), Fraction())

        def coverage(support):
            return sum(n for b, n in positive if not mask_labels[b].isdisjoint(support))

        strict = ties = 0
        ic_rows = set()
        for h, a in actions.items():
            real_leaf = finish(h)
            for t in labels:
                if t == a:
                    continue
                alt_leaf = finish(h + (t,))
                delta = payoff(real_leaf, a) - payoff(alt_leaf, t)
                assert delta >= 0, (policy_key, h, a, t, delta)
                strict += delta > 0
                ties += delta == 0
                if masses is counts:
                    ic = tuple(share(a, real_leaf, b) - share(t, alt_leaf, b) for b in masks)
                    if any(ic):
                        ic_rows.add(ic)
        assert strict + ties == 16806
        w = coverage(actual)
        v = coverage(labels)
        assert sum(payoff(actual, a) for a in actual) == w
        values = {support: coverage(support) for support in support_list}
        optimum = max(values.values())
        payment = [sum(n * row[i, a][b - 1] for b, n in positive if b in omitted) for i, a in enumerate(full_order)]
        assert all(pay <= payoff(forced[i, a], a) <= payoff(actual, actual[i]) for i, (pay, a) in enumerate(zip(payment, full_order, strict=True)))
        assert v - w <= sum(payment) <= w
        if masses is counts:
            beta = Fraction(data['dual_bound'])
            weights = [(idx, Fraction(val)) for idx, val in data['dual_support']]
            rows = sorted(ic_rows)
            assert all(0 <= idx < len(rows) and val >= 0 for idx, val in weights)
            support = set(data['portfolio'])
            target = data['target']
            coverage_row = [int(not mask_labels[b].isdisjoint(actual)) for b in masks]
            objective = [int(not mask_labels[b].isdisjoint(support)) for b in masks]
            if source['parameters']['objective'] == 'residual':
                objective = [v_j - w_b - players * share(target, actual, b) for b, v_j, w_b in zip(masks, objective, coverage_row, strict=True)]
            slack = [beta*w_b - sum(val * rows[idx][b - 1] for idx, val in weights) - obj for b, w_b, obj in zip(masks, coverage_row, objective, strict=True)]
            assert min(slack) == 0
            assert sum(n*obj for n, obj in zip(masses, objective, strict=True)) == beta*w
            assert beta == Fraction(data['objective_value'])
        return dict(histories=len(actions), strict=strict, ties=ties, clients=sum(masses), W=w, V=v, OPT5=optimum,
                    optimal_five_label_supports=[list(support) for support, value in values.items() if value == optimum],
                    L_all=v-w, P_components=list(map(str, payment)), P=str(sum(payment)))

    original = point(counts)
    assert original == saved['original']
    sharp_point = point(sharp)
    assert sharp_point == saved['sharp']
    assert (sharp_point['W'], sharp_point['V'], sharp_point['OPT5'], sharp_point['P']) == (5, 10, 8, '5')
    zero_point = point([0] * len(masks))
    assert (zero_point['strict'], zero_point['ties'], zero_point['W'], zero_point['V'], zero_point['OPT5'], zero_point['P']) == (0, 16806, 0, 0, 0, '0')
    return dict(actual=actual, full_leaves=saved['full_omission']['true_leaves'], support_count=len(support_list),
                paying_permutations=total_paying, original=original, sharp=sharp_point,
                zero=zero_point, selected_dual=[data['dual_bound'], len(data['dual_support'])], q_difference=q_difference)

result = {
    'sigma252': audit_policy('sigma252', 'm5p7_residual.json', (0, 0, 0, 1, 1), (3, 2, 4, 5, 6)),
    'sigma48': audit_policy('sigma48', 'm5p7_reentry_incumbent_half.json', (0, 1, 0, 1, 0), (2, 3, 4, 6, 5)),
}
print(json.dumps({'verified_refs': refs, 'policies': result}, ensure_ascii=False, indent=2))
