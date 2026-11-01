"""Count semantics, not a second complete quotient-test implementation.

Two-player SPE totals are counted from terminal payoff formulas; random signal
diagnostics deliberately reuse the author's seeded backward_policy routine.
"""
from itertools import product
from pathlib import Path
import importlib.util
import json
import random
import sys

BASE = Path(__file__).resolve().parent


def main():
    frozen = json.loads((BASE / 'original/action_quotient_replay.json').read_text())
    table = []
    q1_policies = q2_policies = 0
    for a, b in product(range(4), repeat=2):
        count = 0
        # Shared customers contribute c/2 to every player in every two-player
        # terminal, so c in 0..3 never changes a best-response comparison.
        class_private = (a, a, b)
        def private_pay(current, other):
            same = (current < 2) == (other < 2)
            return class_private[current] * (1 if same else 2)
        for replies in product(range(3), repeat=3):
            if any(private_pay(replies[root], root) < max(private_pay(d, root) for d in range(3)) for root in range(3)):
                continue
            root_values = [private_pay(root, replies[root]) for root in range(3)]
            count += sum(value == max(root_values) for value in root_values)
        table.append({'private_a': a, 'private_b': b, 'spe_per_shared_c': count, 'shared_c_values': 4})
        if a == b == 0:
            q1_policies += 4 * count
        else:
            q2_policies += 4 * count
    assert q1_policies == 324 and q2_policies == 532
    assert q1_policies + q2_policies == frozen['exhaustive_full_SPE']
    compiled_two = q1_policies * 2 + q2_policies * 6
    assert compiled_two == 3840

    # This intentionally shares the author's sampler, BI implementation and
    # random consumption order. It only distinguishes label and coverage tests.
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(BASE / 'related'))
    spec = importlib.util.spec_from_file_location('author_quotient_tests', BASE / 'related/test_duplicate_action_quotient.py')
    author = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author)
    rng = random.Random(566240)
    diagnostics = []
    for game in range(200):
        weights = {}
        for b in range(1, 8):
            mask = (3 if b & 1 else 0) | (4 if b & 2 else 0) | (8 if b & 4 else 0)
            weights[mask] = rng.randrange(6)
        policy = author.backward_policy(weights, 4, 3, rng)
        projection, groups = author.cover_classes(weights, 4)
        label_changes = [a for a in range(4) if policy[(0, a)] != policy[(1, a)]]
        class_changes = [a for a in range(4) if projection[policy[(0, a)]] != projection[policy[(1, a)]]]
        diagnostics.append({'game': game, 'quotient_topics': len(groups), 'label_signal_actions': label_changes, 'coverage_signal_actions': class_changes})
    label_cases = sum(bool(x['label_signal_actions']) for x in diagnostics)
    coverage_cases = sum(bool(x['coverage_signal_actions']) for x in diagnostics)
    assert label_cases == frozen['duplicate_signal_dependent_cases'] == 43
    qk_counts = {str(q): sum(x['quotient_topics'] == q for x in diagnostics) for q in (1, 2, 3)}
    compiled_three = sum(sum(x['quotient_topics'] ** i for i in (1, 2, 3)) for x in diagnostics)
    assert compiled_three == 7800 and qk_counts == {'1': 0, '2': 0, '3': 200}
    original_six = sum(7 ** i for i in range(1, 7))
    quotient_six = sum(6 ** i for i in range(1, 7))
    assert original_six == frozen['six_player_original_IC_comparisons'] == 137256
    assert quotient_six == frozen['six_player_quotient_IC_comparisons'] == 55986
    assert compiled_two + compiled_three + quotient_six == frozen['compiled_exact_IC_comparisons'] == 67626
    result = {
        'status': 'PASS-count-semantics',
        'exhaustive_game_formula': '4^3=64',
        'exhaustive_policy_formula': '64*3^(1+3)=5184',
        'two_player_count_method': 'Independent private-payoff comparison; shared-c contribution cancels. No quotient compiler or author is_spe invoked for this count.',
        'two_player_SPE_by_private_masses': table,
        'two_player_q1_policies': q1_policies,
        'two_player_q2_policies': q2_policies,
        'two_player_compiled_IC': compiled_two,
        'random_diagnostic_method': 'Reuses author backward_policy and exact seeded RNG consumption; not independent BI or complete test implementation.',
        'random_seed': 566240,
        'random_quotient_size_counts': qk_counts,
        'label_signal_cases': label_cases,
        'coverage_signal_cases': coverage_cases,
        'label_only_signal_cases': label_cases - coverage_cases,
        'random_compiled_IC': compiled_three,
        'six_original_history_count': sum(7 ** i for i in range(6)),
        'six_original_IC': original_six,
        'six_quotient_history_count': sum(6 ** i for i in range(6)),
        'six_quotient_lifts_including_terminals': sum(6 ** i for i in range(7)),
        'six_quotient_IC': quotient_six,
        'compiled_IC_sum': compiled_two + compiled_three + quotient_six,
        'all_IC_counts_include_self_actions': True,
        'random_signal_details': diagnostics
    }
    output = BASE / 'replay'
    output.mkdir(exist_ok=True)
    (output / 'count-semantics.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'two_player_compiled_IC', 'random_compiled_IC', 'label_signal_cases', 'coverage_signal_cases', 'label_only_signal_cases', 'compiled_IC_sum']}, indent=2))


if __name__ == '__main__':
    main()
