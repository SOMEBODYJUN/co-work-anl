"""Check the saved ROW duals from the full ordered policy, without a solver.

The source report does not store its per-case primal vectors.  This checker
verifies all dual upper bounds and supplies a separate one-customer maximizer
for the maximum over all cases.  It does not certify every reported primal.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def main():
    data = json.loads((HERE / 'row_attack.json').read_text())
    root_bytes = (HERE / 'root_tax_failure.json').read_bytes()
    root = json.loads(root_bytes)
    assert hashlib.sha256(root_bytes).hexdigest() == data['source_sha256']
    actions = {tuple(x['history']): x['action'] for x in data['strategy']['actions']}
    original = {tuple(x['history']): x['action'] for x in root['strategy']['actions']}
    assert actions == original
    p, m = data['topics'], data['players']
    assert (p, m) == (6, 4)
    required = {h for d in range(m) for h in product(range(p), repeat=d)}
    assert set(actions) == required
    assert all(a in range(p) for a in actions.values())
    terminals = {}
    for d in range(m, -1, -1):
        for h in product(range(p), repeat=d):
            terminals[h] = (tuple(h.count(a) for a in range(p)) if d == m
                            else terminals[h + (actions[h],)])

    def coverage(support):
        mask = sum(1 << a for a in set(support))
        return tuple(F(bool(mask & customer)) for customer in range(1, 1 << p))

    def payoff(counts, action):
        return tuple(F(1, sum(counts[a] for a in range(p) if mask & (1 << a)))
                     if mask & (1 << action) else F(0)
                     for mask in range(1, 1 << p))

    constraints = set()
    comparisons = 0
    for h, action in actions.items():
        actual = payoff(terminals[h], action)
        for alternative in range(p):
            if alternative == action:
                continue
            comparisons += 1
            other = payoff(terminals[h + (alternative,)], alternative)
            row = tuple(a-b for a, b in zip(actual, other))
            if any(row):
                constraints.add(row)
    gamma = tuple(sorted(constraints))
    path = []
    while len(path) < m:
        path.append(actions[tuple(path)])
    assert path == data['actual_path'] == [0, 0, 0, 5]
    assert tuple(path.count(a) for a in range(p)) == tuple(data['strategy']['terminal_counts'])
    welfare = coverage(path)
    tuples = list(combinations_with_replacement(range(p), m))
    tuples.remove((0, 1, 2, 3))
    tuples.insert(0, (0, 1, 2, 3))
    expected = {(j, i) for j in tuples for i in (1, 4)}
    seen = set()
    minimum_residual = None
    bounds = []
    multipliers = 0
    for case in data['cases']:
        j, position = tuple(case['J']), case['actual_position']
        key = (j, position)
        assert key in expected and key not in seen
        seen.add(key)
        cover = coverage(j)
        rows = gamma + tuple(tuple(a-b for a, b in zip(cover, coverage(k))) for k in tuples)
        objectives = []
        for i in range(m):
            prefix = tuple(path[:i])
            query = [payoff(terminals[prefix + (t,)], t) for t in j]
            objectives.append(tuple(o-w-sum(v[k] for v in query)
                                    for k, (o, w) in enumerate(zip(cover, welfare))))
        assert objectives[0] == objectives[1] == objectives[2]
        objective = objectives[position - 1]
        beta = F(case['exact_dual_upper_bound'])
        assert beta == F(case['normalized_gap'])
        assert case['exact_primal'] is True  # Historical assertion, no vector stored.
        residual = [beta*w-o for w, o in zip(welfare, objective)]
        used = set()
        for row_index, text in case['dual_nonzero_multipliers']:
            mu = F(text)
            assert 0 <= row_index < len(rows) and row_index not in used and mu > 0
            used.add(row_index)
            multipliers += 1
            residual = [v - mu*r for v, r in zip(residual, rows[row_index])]
        assert all(v >= 0 for v in residual)
        current = min(residual)
        minimum_residual = current if minimum_residual is None else min(minimum_residual, current)
        assert beta <= F(-1, 4)
        bounds.append(beta)
    assert seen == expected
    assert len(data['cases']) == data['lp_cases'] == data['checked_exact_duals'] == 252
    assert data['failed_exact_duals'] == 0 and data['universal_ROW_proved'] is False
    assert max(bounds) == F(data['maximum_exact_primal_gap']) == F(-1, 4)

    # A single unit customer interested in A,E,F. All prescribed choices cover
    # it; a switch among A,E,F preserves its total number of covering players.
    # This exact point is in the same full-policy cone and has W=OPT=1.
    witness_mask = (1 << 0) | (1 << 4) | (1 << 5)
    coordinate = witness_mask - 1
    assert all(row[coordinate] >= 0 for row in gamma)
    assert welfare[coordinate] == 1
    j = (0, 1, 2, 3)
    query_values = [payoff(terminals[(t,)], t)[coordinate] for t in j]
    witness_gap = coverage(j)[coordinate] - welfare[coordinate] - sum(query_values)
    assert witness_gap == F(-1, 4)
    result = {
        'status': 'passed', 'histories': len(actions),
        'ordered_nonself_deviations_reconstructed': comparisons,
        'unique_nonzero_Gamma_rows': len(gamma), 'client_type_columns': 63,
        'optimal_tuple_comparisons_per_case': len(tuples),
        'saved_duals_verified': len(seen), 'saved_nonzero_multipliers_verified': multipliers,
        'coordinate_residuals_verified': len(seen)*63,
        'minimum_dual_residual': str(minimum_residual),
        'maximum_dual_bound': str(max(bounds)),
        'same_cone_maximum_witness': {'unit_clients': 1, 'interest_mask': witness_mask,
            'J': list(j), 'actual_position': 1, 'W': '1', 'OPT': '1',
            'query_values': list(map(str, query_values)), 'ROW_gap': str(witness_gap)},
        'saved_case_primal_vectors_present': False,
        'saved_case_primal_optimality_independently_checked': False,
        'float_solver_calls': 0, 'original_main_calls': 0, 'strategy_sampling_calls': 0,
        'source_sha256': hashlib.sha256((HERE/'row_attack.json').read_bytes()).hexdigest(),
        'root_source_sha256': hashlib.sha256(root_bytes).hexdigest(),
    }
    (HERE/'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
