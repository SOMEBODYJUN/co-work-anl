from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import sys

repo = Path(sys.argv[1]).resolve()
original = repo / 'archives/customer-attraction/tools/evidence/R275-credible-search-20261031/original'
source_paths = {
    'positive': original / 'eb29376c023b5cd9726a__submodular_joint_m5p7_q32_genuine.json',
    'zero_floor': original / '633b64cbcf0233d0f667__submodular_joint_m5p7_q32.json',
}
expected_hashes = {
    'positive': '48dd63e02d6623f34967db6bf8e22a55f303f6fe72b1f06a7847e36e139110a0',
    'zero_floor': 'dbf83fe8561340f29505cb33e37c83cf79e521ab2c1bcb4f5dd959d2b0968d6d',
}


def check_point(source, positive):
    point = source['exact_candidate']
    meta = source['milp']
    labels = tuple(range(meta['topics']))
    player_count = meta['players']
    path = tuple(meta['path'])
    portfolio = tuple(meta['portfolio'])
    distinguished = (1 << meta['distinguished_topics']) - 1
    rows_keys = tuple(map(tuple, source['moment_orbits']))
    values = tuple(map(F, point['values']))
    zero_row = (F(0),) * len(rows_keys)
    all_masks = tuple(mask for mask in range(1 << len(labels)) if mask.bit_count() <= player_count)

    def combine(*terms):
        return tuple(sum(scale * row[j] for scale, row in terms) for j in range(len(rows_keys)))

    def dot(row):
        return sum(x * y for x, y in zip(row, values))

    def mask_of(labels_in_support):
        mask = 0
        for a in labels_in_support:
            mask |= 1 << a
        return mask

    @lru_cache(None)
    def value_row(mask):
        if not mask:
            return zero_row
        key = mask & distinguished, (mask & ~distinguished).bit_count()
        return tuple(F(key == x) for x in rows_keys)

    def count(history):
        return tuple(history.count(a) for a in labels)

    def inc(counts, a):
        return counts[:a] + (counts[a] + 1,) + counts[a+1:]

    @lru_cache(None)
    def payoff_row(counts, a):
        other_copies = tuple(b for b in labels for _ in range(counts[b] - (a == b)))
        assert len(other_copies) == player_count - 1 and counts[a] > 0
        row = [F(0)] * len(rows_keys)
        for size in range(player_count):
            weight = F(1, player_count * comb(player_count - 1, size))
            for predecessors in combinations(other_copies, size):
                mask = mask_of(predecessors)
                before, after = value_row(mask), value_row(mask | (1 << a))
                for j in range(len(row)):
                    row[j] += weight * (after[j] - before[j])
        return tuple(row)

    @lru_cache(None)
    def payoff(counts, a):
        return dot(payoff_row(counts, a))

    def difference(plus, minus):
        return combine((1, plus), (-1, minus))

    actions = {tuple(row['history']): row['action'] for row in point['complete_strategy']['actions']}
    all_histories = {h for i in range(player_count) for h in product(labels, repeat=i)}
    assert set(actions) == all_histories and len(actions) == len(point['complete_strategy']['actions'])
    assert all(a in labels for a in actions.values())

    @lru_cache(None)
    def terminal_counts(h):
        if len(h) == player_count:
            return count(h)
        return terminal_counts(h + (actions[h],))

    @lru_cache(None)
    def terminal_path(h):
        if len(h) == player_count:
            return h
        return terminal_path(h + (actions[h],))

    root_counts = terminal_counts(())
    assert terminal_path(()) == path
    assert root_counts == tuple(point['complete_strategy']['terminal_counts']) == count(path)
    welfare_row = value_row(mask_of(path))
    target = value_row(mask_of(portfolio))
    assert dot(welfare_row) == 1
    optimum = max(dot(value_row(mask)) for mask in all_masks)
    assert optimum == dot(target) == F(point['value'])

    axioms = set()
    for mask in all_masks:
        missing = [a for a in labels if not (mask & (1 << a))]
        if mask.bit_count() < player_count:
            for a in missing:
                axioms.add(difference(value_row(mask | (1 << a)), value_row(mask)))
        if mask.bit_count() + 2 <= player_count:
            for a, b in combinations(missing, 2):
                axioms.add(combine((1, value_row(mask | (1 << a))), (1, value_row(mask | (1 << b))),
                                   (-1, value_row(mask)), (-1, value_row(mask | (1 << a) | (1 << b)))))
    axioms.discard(zero_row)

    ic, original_query, path_rows, floor_rows = set(), [], set(), set()
    slacks = []
    for h in all_histories:
        chosen = actions[h]
        own = payoff_row(terminal_counts(h), chosen)
        for a in labels:
            if a != chosen:
                deviation = payoff_row(terminal_counts(h + (a,)), a)
                row = difference(own, deviation)
                ic.add(row)
                slacks.append(dot(row))
    ic.discard(zero_row)
    assert min(slacks) == 0
    assert len(slacks) == point['independent_uniform_order_audit']['nonself_deviations']
    assert sum(s == 0 for s in slacks) == point['independent_uniform_order_audit']['ties']
    root_mask = mask_of(path)
    for a in sorted(set(path)):
        without = root_mask & ~(1 << a)
        if positive:
            floor_rows.add(combine((1 - F(str(source['root_marginal_floor'])), welfare_row), (-1, value_row(without))))
    root_marginals = {a: dot(difference(welfare_row, value_row(root_mask & ~(1 << a)))) for a in sorted(set(path))}
    for i, chosen in enumerate(path):
        h = path[:i]
        original_query.append([payoff(terminal_counts(h + (a,)), a) for a in labels])
        prefix = count(h)
        for a in labels:
            copies = prefix[:a] + (prefix[a] + player_count - i,) + prefix[a+1:]
            path_rows.add(difference(payoff_row(root_counts, chosen), payoff_row(copies, a)))
    path_rows.discard(zero_row)

    # Original code deduplicates in signed-customer coordinates before mapping.
    # A reduced IC row may become exactly zero even if its original row was nonzero.
    @lru_cache(None)
    def raw_payoff(counts, a):
        return tuple(F(1, sum(counts[b] for b in labels if mask & (1 << b)))
                     if mask & (1 << a) else F(0) for mask in range(1, 1 << len(labels)))

    independent_coefficient_rows = 0
    for history in product(labels, repeat=player_count):
        q = count(history)
        if history != tuple(sorted(history)):
            continue
        assert sum(q[a] * payoff(q, a) for a in labels if q[a]) == dot(value_row(mask_of(history)))
        for a in labels:
            if not q[a]:
                continue
            raw = raw_payoff(q, a)
            # Compare every coefficient after the raw-player form is expanded by Möbius inversion.
            transformed = [F(0)] + list(raw)
            for bit in labels:
                for mask in range(1 << len(labels)):
                    if not mask & (1 << bit):
                        transformed[mask] -= transformed[mask | (1 << bit)]
            full = (1 << len(labels)) - 1
            coefficients = [F(0)] * len(rows_keys)
            for mask in range(1, full + 1):
                v = -transformed[full ^ mask]
                if mask.bit_count() > player_count:
                    assert v == 0
                else:
                    key = mask & distinguished, (mask & ~distinguished).bit_count()
                    coefficients[rows_keys.index(key)] += v
            assert tuple(coefficients) == payoff_row(q, a)
            independent_coefficient_rows += 1
    assert independent_coefficient_rows == source['coefficient_rows_checked']
    zero_survives = any(
        payoff_row(terminal_counts(h), actions[h]) == payoff_row(terminal_counts(h + (a,)), a)
        and raw_payoff(terminal_counts(h), actions[h]) != raw_payoff(terminal_counts(h + (a,)), a)
        for h in all_histories for a in labels if a != actions[h]
    )
    combined = tuple(sorted(axioms | path_rows | floor_rows | ic | ({zero_row} if zero_survives else set())))
    assert all(dot(row) >= 0 for row in combined)
    beta = F(point['dual_bound'])
    coefficients = [(i, F(value)) for i, value in point['dual_support']]
    assert all(0 <= i < len(combined) and mu > 0 for i, mu in coefficients)
    residual = combine((beta, welfare_row), (-1, target), *((-mu, combined[i]) for i, mu in coefficients))
    assert all(r >= 0 for r in residual)
    assert beta == optimum and dot(residual) == 0 and all(dot(combined[i]) == 0 for i, _ in coefficients)

    @lru_cache(None)
    def outcome_set(prefix):
        if sum(prefix) == player_count:
            return frozenset({prefix})
        children = [outcome_set(inc(prefix, a)) for a in labels]
        floor = max(min(payoff(q, a) for q in children[a]) for a in labels)
        return frozenset(q for a in labels for q in children[a] if payoff(q, a) >= floor)

    root_outcomes = outcome_set((0,) * len(labels))
    assert root_counts in root_outcomes
    minima, patched_roots, lower_actions = [], {}, {}

    def realize(h, target_counts):
        prefix = count(h)
        if len(h) == player_count:
            assert prefix == target_counts
            return
        children = [outcome_set(inc(prefix, a)) for a in labels]
        branch_mins = [min(children[a], key=lambda q: (payoff(q, a), q)) for a in labels]
        floor = max(payoff(q, a) for a, q in enumerate(branch_mins))
        chosen = next(a for a in labels if target_counts in children[a] and payoff(target_counts, a) >= floor)
        lower_actions[h] = chosen
        for a in labels:
            realize(h + (a,), target_counts if a == chosen else branch_mins[a])

    for i, chosen in enumerate(path):
        h = path[:i]
        lower_actions[h] = chosen
        prefix = count(h)
        row = []
        for a in labels:
            if a == chosen:
                row.append(payoff(root_counts, chosen))
            else:
                branch = h + (a,)
                lower_q = min(outcome_set(inc(prefix, a)), key=lambda q: (payoff(q, a), q))
                row.append(payoff(lower_q, a))
                patched_roots[branch] = lower_q
                realize(branch, lower_q)
        minima.append(row)
    assert len(patched_roots) == player_count * (len(labels) - 1)
    assert all(a != b[:len(a)] for a in patched_roots for b in patched_roots if a != b)
    assert set(lower_actions) == all_histories
    assert all(minima[i][a] <= original_query[i][a] <= original_query[i][path[i]]
               for i in range(player_count) for a in labels)

    @lru_cache(None)
    def patched_terminal(h):
        return count(h) if len(h) == player_count else patched_terminal(h + (lower_actions[h],))

    assert patched_terminal(()) == root_counts
    assert all(patched_terminal(branch) == q for branch, q in patched_roots.items())
    for h in all_histories:
        chosen = lower_actions[h]
        assert payoff(patched_terminal(h), chosen) >= max(payoff(patched_terminal(h + (a,)), a) for a in labels)
    assert all(minima[i][a] == payoff(patched_terminal(path[:i] + (a,)), a)
               for i in range(player_count) for a in labels)

    def up_record(matrix):
        sums = [sum(row[a] for row in matrix) for a in labels]
        best_all, best_opt = None, None
        for mask in all_masks[1:]:
            support = tuple(a for a in labels if mask & (1 << a))
            fill = min(support, key=lambda a: (sums[a], a))
            tup = support + (fill,) * (player_count - len(support))
            query_sum = sum(sums[a] for a in tup)
            gap = (player_count - 1) + query_sum - player_count * dot(value_row(mask))
            cand = gap, tup, query_sum
            best_all = min(best_all, cand) if best_all is not None else cand
            if dot(value_row(mask)) == optimum:
                best_opt = min(best_opt, cand) if best_opt is not None else cand
        return {'matrix': matrix, 'query_sums': sums, 'best_all': best_all, 'best_opt': best_opt,
                'specified_portfolio_query': sum(sums[a] for a in portfolio),
                'specified_portfolio_gap': player_count - 1 + sum(sums[a] for a in portfolio) - player_count * optimum}

    intersections = []
    for a, b, c in combinations(labels, 3):
        t = sum((-1) ** (size + 1) * dot(value_row(mask_of(subset)))
                for size in (1, 2, 3) for subset in combinations((a, b, c), size))
        if t < 0:
            intersections.append(((a, b, c), t))
    outside = tuple(a for a in labels if not (distinguished & (1 << a)))
    outside_value = dot(value_row(mask_of(outside)))
    full_submodular_bounds = {}
    for a in sorted(set(path)):
        left = mask_of((a, *outside[1:]))
        right = mask_of((a, outside[0], *outside[2:]))
        full_submodular_bounds[a] = dot(combine((1, value_row(left)), (1, value_row(right)),
                                               (-1, value_row(left & right))))
        assert full_submodular_bounds[a] < outside_value
    if positive:
        assert ((1, 2, 3), F(-10, 57)) in intersections
        assert root_marginals == {0: F(6, 19), 1: F(3, 19)}
        h, k = (0, 0, 1), (0, 1, 0)
        assert (actions[h], actions[k]) == (6, 0)
    else:
        h, k = (2, 1, 3), (2, 3, 1)
        assert (actions[h], actions[k]) == (0, 1)
    assert h != k and count(h) == count(k)

    def pair_intersection(a, b):
        return dot(combine((1, value_row(1 << a)), (1, value_row(1 << b)),
                           (-1, value_row(mask_of((a, b))))))

    boolean_quadratic = (dot(value_row(1)) - sum(pair_intersection(0, b) for b in outside)
                         + sum(pair_intersection(b, c) for b, c in combinations(outside, 2)))
    assert all(z - z * r + comb(r, 2) >= 0 for z in (0, 1) for r in range(len(outside) + 1))
    if not positive:
        assert boolean_quadratic == -F(1, 4)

    return {'support': portfolio, 'actual_path': path, 'root_marginals': root_marginals,
            'W': F(1), 'OPT': optimum, 'histories': len(all_histories), 'nonself_deviations': len(slacks),
            'positive_slack_min': min(s for s in slacks if s), 'ties': sum(s == 0 for s in slacks),
            'coefficient_rows': independent_coefficient_rows, 'combined_rows': len(combined),
            'row_counts': {'axioms': len(axioms), 'path': len(path_rows), 'root_floors': len(floor_rows), 'IC_without_zero': len(ic)},
            'dual_terms': len(coefficients), 'dual_bound': beta, 'dual_residual': residual,
            'distinct_spe_root_counts': len(root_outcomes), 'fixed_input_min_spe_welfare': min(dot(value_row(mask_of(a for a in labels if q[a]))) for q in root_outcomes),
            'first_deviation_subtrees': len(patched_roots),
            'changed_actions': sum(actions[h] != lower_actions[h] for h in actions),
            'strictly_decreased_queries': [(i + 1, a, original_query[i][a], minima[i][a]) for i in range(player_count) for a in labels if original_query[i][a] > minima[i][a]],
            'original_strategy': up_record(original_query), 'pasted_minimum_strategy': up_record(minima),
            'negative_triple_intersections': intersections, 'boolean_quadratic_separator_value': boolean_quadratic,
            'full_submodular_extension_upper_bounds': full_submodular_bounds,
            'same_count_distinct_history_choices': [(h, actions[h]), (k, actions[k])]}


if __name__ == '__main__':
    results = {}
    for name, file in source_paths.items():
        raw = file.read_bytes()
        digest = sha256(raw).hexdigest()
        assert digest == expected_hashes[name], (name, digest)
        results[name] = {'sha256': digest, **check_point(json.loads(raw), name == 'positive')}
    print(json.dumps(results, default=str, indent=2))
