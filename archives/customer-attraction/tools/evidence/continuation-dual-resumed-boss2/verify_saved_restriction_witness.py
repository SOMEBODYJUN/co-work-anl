"""One independent exact check of the saved 13/4 restriction witness.

Reads saved reports and source actions; does not import any original program,
canonical solver, NumPy, or SciPy. No LP/search or old indexed-row recomputation.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
from collections import Counter
import hashlib
import json
import platform

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
EVIDENCE = HERE.parent
ORIGIN = EVIDENCE / 'strategy-cones/original/evidence/runs/2026-10-09/customer_attraction_strategy_lp_m4p5_certified.json'
STRATEGY_CODE = EVIDENCE / 'strategy-cones/original/tests/audits/customer_attraction_strategy_lp.py'
OLD = EVIDENCE / 'five-player-indexed/evidence/certificates/customer_attraction/five_player_indexed_bound.json'
TEN = EVIDENCE / 'continuation-closure-resumed-boss2/original/offdiagonal_closure.json'
EXCHANGE = EVIDENCE / 'continuation-closure-resumed-boss2/original/exchangeable_last_closure.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    for source in read(HERE / 'source-manifest.json'):
        path = HERE / 'original' / Path(source['path']).name
        assert path.stat().st_size == source['size'] and sha(path) == source['sha256']
    saved = read(HERE / 'original/restriction_probe.json')
    assert set(saved) == {'scope', 'best', 'failures'}
    assert set(saved['best']) == {'full', 'portfolio_actions', 'comparator_prefix', 'permutation_prefix', 'onpath'}
    assert set(saved['failures']) == {'permutation_prefix'}
    witness = saved['failures']['permutation_prefix']
    assert set(witness) == {'cone', 'portfolio', 'actions', 'value', 'dual_bound', 'point', 'negative_genuine_rows', 'dual'}
    assert witness['cone'] == 16 and witness['portfolio'] == [0, 1, 3, 4]
    origin = read(ORIGIN)
    assert witness['actions'] == origin['cone_proofs'][16]['actions']
    policy = {tuple(item['history']): item['action'] for item in witness['actions']}
    histories = [h for depth in range(4) for h in product(range(5), repeat=depth)]
    assert len(policy) == len(witness['actions']) == 156 and set(policy) == set(histories)
    assert all(policy[h] == (0 if all(a == 0 for a in h) else 2) for h in histories)
    values = list(map(F, witness['point']))
    assert len(values) == 31 and all(value >= 0 for value in values)
    expected = {1: F(1), 4: F(15, 16), 6: F(3, 4), 12: F(3, 4), 20: F(3, 4)}
    assert {mask: value for mask, value in enumerate(values, 1) if value} == expected
    unit_customers = [mask for mask, value in expected.items() for _ in range(int(16 * value))]
    assert len(unit_customers) == 67
    topic_sets = [{i for i, mask in enumerate(unit_customers) if mask & (1 << a)} for a in range(5)]
    assert all(topic_sets) and len({frozenset(topic) for topic in topic_sets}) == 5
    J = set(witness['portfolio'])

    def terminal(h):
        path = tuple(h)
        while len(path) < 4:
            path += (policy[path],)
        return path

    def utility(path, action):
        # Explicit 67 different unit customers, rather than a canonical row helper.
        return sum((F(1, sum(bool(mask & (1 << a)) for a in path))
                    for mask in unit_customers if mask & (1 << action)), F(0))

    def one_customer(path, action, mask):
        return (F(1, sum(bool(mask & (1 << a)) for a in path))
                if mask & (1 << action) else F(0))

    root_path = terminal(())
    actual_prefixes = {root_path[:depth] for depth in range(4)}
    welfare = len(set().union(*(topic_sets[a] for a in root_path)))
    objective = len(set().union(*(topic_sets[a] for a in J)))
    portfolios = {tuple(group): len(set().union(*(topic_sets[a] for a in group)))
                  for group in combinations(range(5), 4)}
    optimum = max(portfolios.values())
    assert root_path == (0, 0, 0, 0) and welfare == 16 and objective == 52 and optimum == 67
    assert F(objective, welfare) == F(witness['value']) == F(witness['dual_bound']) == F(13, 4)

    def included(h, alternative, mode):
        if mode != 'full' and alternative not in J:
            return False
        if mode == 'permutation_prefix':
            return len(set(h)) == len(h) and set(h) <= J and alternative not in h
        if mode == 'comparator_prefix':
            return set(h) <= J
        if mode == 'onpath':
            return h in actual_prefixes
        return True

    all_rows = []
    negatives = []
    modes = {mode: {'retained_nonzero_rows': 0, 'negative_rows': []}
             for mode in saved['best']}
    row_vectors = {mode: set() for mode in saved['best']}
    nonself = 0
    for h in histories:
        action = policy[h]
        chosen_path = terminal(h)
        actual = utility(chosen_path, action)
        values_here = []
        for alternative in range(5):
            alternative_path = terminal(h + (alternative,))
            slack = (actual - utility(alternative_path, alternative)) / 16
            values_here.append(str(slack))
            record = {'history': list(h), 'alternative': alternative, 'slack': str(slack)}
            if slack < 0:
                negatives.append(record)
            if alternative != action:
                nonself += 1
                row = tuple(one_customer(chosen_path, action, mask)
                            - one_customer(alternative_path, alternative, mask)
                            for mask in range(1, 32))
                assert any(row)
                for mode in modes:
                    if included(h, alternative, mode):
                        modes[mode]['retained_nonzero_rows'] += 1
                        row_vectors[mode].add(row)
                        if slack < 0:
                            modes[mode]['negative_rows'].append(record)
            else:
                assert slack == 0
        all_rows.append({'history': list(h), 'action': action, 'normalized_slacks_by_alternative_0_to_4': values_here})
    assert negatives == witness['negative_genuine_rows']
    assert len(negatives) == 13
    assert not modes['permutation_prefix']['negative_rows']
    assert {mode: len(data['negative_rows']) for mode, data in modes.items()} == {
        'full': 13, 'portfolio_actions': 9, 'comparator_prefix': 6, 'permutation_prefix': 0, 'onpath': 6}
    for mode in modes:
        modes[mode]['distinct_nonzero_coefficient_rows'] = len(row_vectors[mode])

    assert witness['dual'] == [
        {'history': [0], 'alternative': 1, 'weight': '3'},
        {'history': [0], 'alternative': 3, 'weight': '3'},
        {'history': [0], 'alternative': 4, 'weight': '3'}]
    residuals = []
    for mask in range(1, 32):
        a0 = int(bool(mask & 1))
        a2 = int(bool(mask & 4))
        q = sum(bool(mask & (1 << a)) for a in (1, 3, 4))
        comparison = int(bool(a0 or q))
        residual = F(13, 4) * a0 - comparison
        for entry in witness['dual']:
            h, alternative, multiplier = tuple(entry['history']), entry['alternative'], F(entry['weight'])
            assert multiplier >= 0 and included(h, alternative, 'permutation_prefix')
            coefficient = one_customer(terminal(h), policy[h], mask) - one_customer(terminal(h + (alternative,)), alternative, mask)
            residual -= multiplier * coefficient
        closed = F(a0) + F(3 * q, a0 + 1 + 2 * a2) - comparison
        assert residual == closed >= 0
        residuals.append({'mask': mask, 'a0': a0, 'a2': a2, 'petal_count': q, 'residual': str(residual)})
    assert all(F(residuals[mask - 1]['residual']) == 0 for mask in expected)

    # Saved scalar consumption/binding only for the already mature five-player row.
    off = read(HERE / 'original/offdiagonal_closure_audit.json')
    assert set(off) == {'scope', 'atoms', 'terminal_comparisons_in_new_row', 'offdiagonal_sum',
        'offdiagonal_mean', 'diagonal_sum', 'all_25_sum', 'decomposition_verified_every_atom'}
    assert off['atoms'] == 64 and off['terminal_comparisons_in_new_row'] == 20
    assert off['decomposition_verified_every_atom'] is True
    assert F(off['offdiagonal_sum']) == 20 * F(off['offdiagonal_mean']) < 0
    assert F(off['offdiagonal_sum']) + F(off['diagonal_sum']) == F(off['all_25_sum']) > 0
    assert F(off['diagonal_sum']) > 0
    assert F(off['offdiagonal_sum']) == F(read(TEN)['rows']['Sbranch:5:offdiag:2'])
    exchange = read(EXCHANGE)
    assert F(off['offdiagonal_mean']) == F(exchange['all_slacks']['branch_S -> S:2[j!=i]'])
    assert F(off['diagonal_sum']) == 5 * F(exchange['all_slacks']['branch_S -> S:2[i]'])

    report = {
        'scope': 'independent saved restriction-witness primal/dual and all ordered deviations; mature five-player scalar binding only',
        'python': platform.python_version(), 'assertions_enabled': __debug__,
        'primary_sha256_all_match': True,
        'dependencies': [{'path': str(path.relative_to(REPO)), 'bytes': path.stat().st_size, 'sha256': sha(path)}
                         for path in (ORIGIN, STRATEGY_CODE, OLD, TEN, EXCHANGE)],
        'selected_origin_cone': 16, 'origin_actions_exactly_match': True,
        'origin_cone_proofs': len(origin['cone_proofs']),
        'saved_best_five_modes': saved['best'],
        'histories': 156, 'comparisons_including_self': 780, 'nonself_comparisons': nonself,
        'policy_formula': '0 if every past action is 0, otherwise 2',
        'normalized_positive_masses': {str(mask): str(value) for mask, value in expected.items()},
        'unit_customer_counts': {str(mask): int(16 * value) for mask, value in expected.items()},
        'unit_customers': 67, 'five_distinct_nonempty_topic_subsets': True,
        'root_path': list(root_path), 'root_welfare': welfare,
        'fixed_comparison_portfolio': sorted(J), 'fixed_comparison_coverage': objective,
        'all_five_four_topic_portfolio_coverages': {','.join(map(str, group)): coverage for group, coverage in portfolios.items()},
        'actual_OPT4': optimum, 'comparison_over_W': str(F(objective, welfare)),
        'actual_OPT4_over_W_of_nonSPE_policy': str(F(optimum, welfare)),
        'all_history_slacks': all_rows, 'all_negative_genuine_rows': negatives,
        'mode_witness_checks': modes,
        'dual_weights': witness['dual'], 'all_31_dual_residuals': residuals,
        'fixed_permutation_cone_exact_optimum': '13/4',
        'is_full_SPE': False,
        'mature_offdiagonal_saved_scalar_binding': off,
        'five_player_matrix_recomputations': 0,
        'original_main_runs': 0, 'optimizer_calls': 0,
    }
    (HERE / 'saved-witness-exact-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'histories': 156, 'all_comparisons': 780, 'negative_genuine_rows': 13,
        'unit_customers': 67, 'comparison_cover': 52, 'actual_OPT4': 67,
        'permutation_exact_optimum': '13/4', 'dual_type_checks': 31,
        'five_player_matrix_recomputations': 0, 'original_main_runs': 0, 'optimizer_calls': 0}))


if __name__ == '__main__':
    main()
