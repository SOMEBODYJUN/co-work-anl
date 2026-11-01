"""Run the unchanged frozen root-menu recovery once in a new source layout.

The floating discovery LP and prior root primitive prefix are never executed.
Full original globals already calculated by that single recovery are retained.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse
import collections
import hashlib
import json
import math
import platform
import runpy
import shutil
import sys
import time

HERE = Path(__file__).resolve().parent


def read_json(path):
    return json.loads(path.read_text())


def checked(path, row):
    raw = path.read_bytes()
    assert len(raw) == row['size']
    assert hashlib.sha256(raw).hexdigest() == row['sha256']
    return raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runtime', required=True, type=Path)
    ap.add_argument('--repository', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    if args.runtime.exists() and any(args.runtime.iterdir()):
        raise SystemExit('runtime must be new or empty')
    args.runtime.mkdir(parents=True, exist_ok=True)
    args.output.mkdir(parents=True, exist_ok=True)
    source_rows = read_json(HERE / 'source-manifest.json')
    related = read_json(HERE / 'related-dependencies.json')
    routes = []
    for row in source_rows:
        source = HERE / 'original' / row['id'] / Path(row['path']).name
        routes.append((source, args.runtime / row['path'], row))
    for row in related:
        routes.append((HERE / 'related' / row['path'], args.runtime / row['path'], row))
    for source, target, row in routes:
        raw = checked(source, row)
        assert target.resolve().is_relative_to(args.runtime.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    root = args.runtime / Path(source_rows[0]['path']).parent
    floating = read_json(root / 'root_menu_completion.json')
    exact_before = (root / 'root_menu_completion_exact.json').read_bytes()
    old = read_json(root / 'enhanced_2396_exact_obstruction.json')['atom_masses']
    prior = {}
    for row in read_json(HERE / 'prior-order-evidence.json'):
        prior[Path(row['path']).name] = json.loads(checked(args.repository / row['path'], row))
    order_event = prior['root-primitive-interface-execution.json']
    previous_full = prior['root_full_hist_completion.json']
    primitive_source = next(x for x in source_rows if Path(x['path']).name == 'root_menu_completion.py')
    assert order_event['source_sha256'] == primitive_source['sha256']
    assert order_event['primitive_prefix_exec_calls'] == 1 and order_event['LP_calls'] == 0
    assert floating['row_names'] == previous_full['row_names'][:1310]
    assert floating['row_specs'] == previous_full['row_specs'][:1310]
    assert len(set(floating['row_names'])) == 1310
    types = list(product((0, 1), repeat=3))
    counts = [sum(n * t[0] for n, t in zip(a['AB_hist'], types)) for a in old]
    assert len(old) == 38 and counts == [1] * 38
    variables = [[a, t, list(v)] for a in range(38) for t in (0, 1)
                 if (counts[a] if t else 5 - counts[a]) for v in product((0, 1), repeat=4)]
    groups = [[a, t] for a in range(38) for t in (0, 1)]
    assert variables == floating['variables_spec'] and groups == floating['groups']
    assert floating['variables'] == len(variables) == len(floating['point']) == 1216
    assert floating['inequalities'] == len(floating['row_names']) == len(floating['row_specs']) == len(floating['dual_rows']) == 1310
    assert floating['equalities'] == len(groups) == len(floating['dual_equalities']) == 76
    for key in ('point', 'dual_rows', 'dual_equalities'):
        assert all(isinstance(x, (int, float)) and math.isfinite(x) for x in floating[key])
    assert min(floating['point']) >= 0 and min(floating['dual_rows']) >= 0
    assert sum(x > 0 for x in floating['point']) == 92
    families = collections.Counter(x[0] for x in floating['row_specs'])
    assert dict(families) == {'root': 1, 'menu': 84, 'own': 19, 'reverse': 40, 'profit': 935, 'tax': 231}
    input_review = {
        'all_14_top_level_float_fields_read': list(floating),
        'current_float_row_names_and_specs_equal_previously_bound_1310_primitive_order': True,
        'prior_primitive_prefix_reexecutions': 0,
        'complete_deterministic_variable_and_group_domains_match': True,
        'row_families': dict(families), 'old_atoms': len(old), 'all_old_T_counts': 1,
        'variables': len(variables), 'groups': len(groups),
        'float_positive_variables': sum(x > 0 for x in floating['point']),
        'float_dual_rows_nonzero': sum(x != 0 for x in floating['dual_rows']),
        'float_equality_duals_nonzero': sum(x != 0 for x in floating['dual_equalities']),
        'float_dual_rows_sum_as_exact_stored_binary_numbers': str(sum(map(F, floating['dual_rows']), F())),
        'float_dual_rows_sum_float': sum(floating['dual_rows']),
        'float_margin': floating['margin'],
        'float_dual_optimality_certification': False,
        'positive_float_columns': [{'index': i, 'variable': variables[i], 'value': x}
                                   for i, x in enumerate(floating['point']) if x > 0],
        'all_nonzero_float_inequality_multipliers': [{'index': i, 'name': floating['row_names'][i], 'value': x}
                                                   for i, x in enumerate(floating['dual_rows']) if x != 0],
        'all_equality_multipliers': [{'group': group, 'value': x}
                                     for group, x in zip(groups, floating['dual_equalities'])]}
    (args.output / 'input-contract-review.json').write_text(json.dumps(input_review, ensure_ascii=False, indent=2) + '\n')

    script = root / 'recover_root_completion.py'
    old_path = list(sys.path)
    old_dontwrite = sys.dont_write_bytecode
    sys.path.insert(0, str(root))
    sys.dont_write_bytecode = True
    started = time.time()
    clock = time.perf_counter()
    try:
        g = runpy.run_path(str(script), run_name='__main__')
    finally:
        sys.path[:] = old_path
        sys.dont_write_bytecode = old_dontwrite
    elapsed = time.perf_counter() - clock
    generated = (root / 'root_menu_completion_exact.json').read_bytes()
    assert generated == exact_before
    (args.output / 'root_menu_completion_exact.json').write_bytes(generated)
    # Read existing globals. No additional calls to coefficient or recovery.
    slacks = g['slacks']
    x, S = g['x'], g['S']
    minimum_original_slack = min(slacks.values())
    assert len(slacks) == 1310 and len(S) == 92 and minimum_original_slack > 0
    group_rows = []
    correction_count = 0
    for a, t in groups:
        indexes = [i for i, (aa, tt, v) in enumerate(variables) if aa == a and tt == t]
        target = F(old[a]['mass']) * (counts[a] if t else 5 - counts[a]) / 5
        actual = sum((x[i] for i in indexes), F())
        assert actual == target
        pre = [F(float(floating['point'][i])).limit_denominator(10**9) for i in indexes]
        changes = [{'index': i, 'correction': str(x[i] - initial)} for i, initial in zip(indexes, pre) if x[i] != initial]
        assert len(changes) <= 1
        if changes:
            correction_count += 1
            assert changes[0]['index'] == indexes[max(range(len(indexes)), key=lambda j: pre[j])]
        group_rows.append({'atom': a, 't': t, 'target_mass': str(target), 'actual_mass': str(actual),
                           'positive_cells': sum(x[i] > 0 for i in indexes), 'rounding_mass_correction': changes})
    observed = {'original_recovery_runs': 1, 'original_coefficient_evaluations': len(S) * len(slacks),
                'additional_coefficient_calls_after_original_return': 0,
                'full_recovered_vector': list(map(str, x)), 'positive_indices': S,
                'all_1310_original_slacks': {n: str(v) for n, v in slacks.items()},
                'all_76_exact_mass_groups': group_rows,
                'groups_with_nonzero_mass_repair': correction_count,
                'minimum_slack_names': [n for n, v in slacks.items() if v == minimum_original_slack],
                'positive_cell_distribution_per_group': dict(collections.Counter(row['positive_cells'] for row in group_rows)),
                'original_float_LP_runs': 0, 'prior_prefix_or_root53_replays': 0,
                'output_bytes_equal_frozen_19288B': True}
    observed_path = args.output / 'original-return-observation.json'
    observed_path.write_text(json.dumps(observed, ensure_ascii=False, indent=2) + '\n')
    event = {'started_unix': started, 'original_recovery_elapsed_seconds': elapsed,
             'python': platform.python_version(), 'assertions_enabled': __debug__,
             'original_recovery_top_level_invocations': 1,
             'original_recovery_sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
             'original_float_LP_runs': 0, 'previous_prefix_reexecutions': 0, 'previous_root53_audit_runs': 0,
             'output_bytes': len(generated), 'output_sha256': hashlib.sha256(generated).hexdigest(),
             'output_equal_frozen': True,
             'observation_sha256': hashlib.sha256(observed_path.read_bytes()).hexdigest(),
             'wrapper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (args.output / 'event.json').write_text(json.dumps(event, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'event': 'wrapper completed after original stdout', 'output_byte_equal': True,
                      'original_recovery_seconds': elapsed, 'original_slacks': len(slacks),
                      'exact_mass_groups': len(group_rows), 'mass_repaired_groups': correction_count}, ensure_ascii=False))


if __name__ == '__main__':
    main()
