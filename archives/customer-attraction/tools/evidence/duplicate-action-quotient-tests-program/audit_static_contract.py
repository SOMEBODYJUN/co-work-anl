"""Read-only source/receipt audit; never imports or runs either original program.

The count diagnostic is read as stored evidence. No original main, backward
induction, policy enumeration, or explain_counts.py is executed here.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    base = args.repo / 'archives/customer-attraction/tools/evidence/action-quotient-parent-replay'
    tests = base / 'related/test_duplicate_action_quotient.py'
    core = base / 'related/duplicate_action_quotient.py'
    expected_test = '0bca5b6f8f04c1ac0e5e8c26a04c03c80a99239c1a3af09d44ff033aabe36ad6'
    expected_core = '7e43a0270ea0b6d89abf99be3fa066b45145b0dbe5cd72dd813c036c6ebfad0f'
    assert len(tests.read_bytes()) == 4370 and sha(tests) == expected_test
    assert len(core.read_bytes()) == 2506 and sha(core) == expected_core
    tree = ast.parse(tests.read_text())
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    assert [node.name for node in functions] == [
        'histories', 'continuation', 'pay', 'is_spe', 'opt', 'audit', 'backward_policy', 'main']
    imports = [ast.unparse(node) for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    assert imports == [
        'import json, random', 'from fractions import Fraction as F',
        'from itertools import product, combinations',
        'from duplicate_action_quotient import cover_classes, quotient_policy, quotient_weights, project_history']
    assertions = sorted([
        {'line': node.lineno, 'test': ast.unparse(node.test)}
        for node in ast.walk(tree) if isinstance(node, ast.Assert)], key=lambda item: item['line'])
    assert len(assertions) == 8
    assert ast.unparse(tree.body[-1]) == "if __name__ == '__main__':\n    main()"
    calls = sorted({ast.unparse(node.func) for node in ast.walk(tree) if isinstance(node, ast.Call)})
    assert not set(calls) & {'open', 'exec', 'eval', 'input', 'parse_args'}

    event_path = base / 'replay/execution-event.json'
    event = json.loads(event_path.read_text())
    author_path = base / 'related/duplicate_action_quotient_test_report.json'
    stdout_path = base / 'replay/author-stdout.json'
    stderr_path = base / 'replay/author-stderr.txt'
    author = json.loads(author_path.read_text())
    assert stdout_path.read_bytes() == author_path.read_bytes()
    assert sha(stdout_path) == event['stdout_sha256']
    assert len(stdout_path.read_bytes()) == event['stdout_bytes'] == 339
    assert stderr_path.read_bytes() == b'' and event['stderr_bytes'] == 0
    assert event['compiler_sha256'] == expected_core and event['test_sha256'] == expected_test
    assert event['status'] == 'PASS' and event['exit_code'] == 0
    assert event['assertions_enabled'] and event['pythonoptimize_environment_removed']
    assert not event['wrapper_is_original_parent_runner']
    assert not event['new_independent_full_test_implementation']
    assert len(author) == 9
    parent_path = base / 'original/action_quotient_replay.json'
    parent = json.loads(parent_path.read_text())
    assert all(parent[key] == value for key, value in author.items())
    assert set(parent) - set(author) == {'review', 'compiler_sha256', 'test_sha256'}

    counts_path = base / 'replay/count-semantics.json'
    counts = json.loads(counts_path.read_text())
    table = counts['two_player_SPE_by_private_masses']
    assert len(table) == 16
    assert {(r['private_a'], r['private_b']) for r in table} == {(a,b) for a in range(4) for b in range(4)}
    assert all(row['shared_c_values'] == 4 for row in table)
    q1 = sum(4 * row['spe_per_shared_c'] for row in table if row['private_a'] == row['private_b'] == 0)
    q2 = sum(4 * row['spe_per_shared_c'] for row in table if row['private_a'] or row['private_b'])
    assert (q1,q2) == (324,532) and q1+q2 == author['exhaustive_full_SPE']
    details = counts['random_signal_details']
    assert len(details) == 200 and [item['game'] for item in details] == list(range(200))
    for item in details:
        assert item['quotient_topics'] in (1,2,3)
        assert set(item['coverage_signal_actions']) <= set(item['label_signal_actions']) <= set(range(4))
    label_count = sum(bool(item['label_signal_actions']) for item in details)
    class_count = sum(bool(item['coverage_signal_actions']) for item in details)
    assert (label_count,class_count,label_count-class_count) == (43,16,27)
    assert all(item['quotient_topics'] == 3 for item in details)
    components = {
        'two_player_compiled_IC': q1 * (1+1) + q2 * (2+4),
        'three_player_compiled_IC': sum(sum(item['quotient_topics']**i for i in (1,2,3)) for item in details),
        'six_player_compiled_IC': sum(6**i for i in range(1,7)),
    }
    assert list(components.values()) == [3840,7800,55986]
    assert sum(components.values()) == author['compiled_exact_IC_comparisons'] == 67626
    assert sum(7**i for i in range(1,7)) == author['six_player_original_IC_comparisons'] == 137256
    assert 4**3 == author['exhaustive_games'] == 64
    assert 4**3 * 3**(1+3) == author['exhaustive_full_policies'] == 5184
    assert author['random_three_player_games'] == 200
    assert author['duplicate_signal_dependent_cases'] == label_count
    assert author['six_player_quotient_IC_comparisons'] == components['six_player_compiled_IC']
    assert author['all_checks_passed'] is True

    shared = [tests, core, author_path, parent_path, event_path, stdout_path, stderr_path, counts_path,
              base/'replay_author_tests.py', base/'explain_counts.py', base/'manifest.json']
    result = {
        'status': 'PASS-static-source-and-stored-evidence-reconciliation',
        'source_id': '27c3f7501ae211076aa5',
        'scope': 'AST and immutable-byte binding; algebraic totals from existing diagnostic records; no original implementation execution',
        'new_original_main_invocations': 0,
        'new_original_function_invocations': 0,
        'new_explain_counts_invocations': 0,
        'new_independent_full_test_implementation': False,
        'shared_inputs': [{'path': str(path.relative_to(args.repo)), 'bytes': path.stat().st_size, 'sha256': sha(path)} for path in shared],
        'imports': imports,
        'functions': [{'name': node.name, 'line': node.lineno, 'end_line': node.end_lineno,
                       'arguments': [arg.arg for arg in node.args.args]} for node in functions],
        'assertions': assertions,
        'main_guard': ast.unparse(tree.body[-1]),
        'fixed_input_contract': {
            'exhaustive': {'topics': 3, 'players': 2, 'weights': '3:a,4:b,7:c; a,b,c in range(4)',
                           'original_history_lengths': [0,1], 'all_full_policies_per_game': 81},
            'seeded': {'topics': 4, 'players': 3, 'seed': 566240, 'games': 200,
                       'membership_masks_in_order': [3,4,7,8,11,12,15], 'multiplicities': 'rng.randrange(6)',
                       'random_consumption': 'weights and all-node BI tie choices share the same RNG'},
            'six': {'topics': 7, 'players': 6, 'weights': {'1':6,'2':1,'4':1,'8':1,'16':1,'96':1},
                    'prescribed_action_every_history': 0, 'unit_customers': 11},
        },
        'existing_execution_receipt_validated': True,
        'stored_diagnostic_records_parsed': {'two_private_mass_pairs': len(table), 'seeded_cases': len(details)},
        'label_signal_cases': label_count, 'coverage_signal_cases': class_count, 'label_only_signal_cases': label_count-class_count,
        'compiled_IC_components': components,
        'compiled_IC_sum': sum(components.values()),
        'author_report_fields': author,
        'coverage_limits': [
            'audit does not itself check source SPE; main supplies screening/assertions',
            'only dictionary policies; callable route and reverse construction are not tested',
            'assertions check every returned lift entry, but not an independent exact lift key-set assertion',
            'all original fixtures have duplicate labels; no identity-projection case',
            'only positive player counts 2,3,6; no malformed-input or negative-weight suite',
            '200 seeded BI outputs are not all possible three-player SPE or all tie choices',
            'existing full replay is the same author test, not a new independent implementation',
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status':result['status'], 'source_id':result['source_id'],
                      'functions':len(functions), 'source_assertion_sites':len(assertions),
                      'shared_input_files':len(shared), 'new_original_main_invocations':0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
