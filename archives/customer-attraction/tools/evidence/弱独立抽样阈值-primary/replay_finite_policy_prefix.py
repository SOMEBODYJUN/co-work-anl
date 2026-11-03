"""Execute only the frozen review's six-case finite prefix, once.

The original main is not called. Its rows initialization and first for-loop
are reused as AST nodes, followed by return rows. The already certified iid
100 cut and m53 constants later in main are never entered. Frozen sources and
reports stay intact. No solver or LP method is invoked.
"""
import ast
import hashlib
import json
from pathlib import Path
import sys
import time

E = Path(__file__).resolve().parent
OUT = E / 'finite-policy-prefix-replay.json'
if OUT.exists():
    raise SystemExit('Successful finite-prefix replay exists; do not rerun')
assert sys.flags.optimize == 0, 'assertions must remain enabled'
source = E / 'original/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_search/weak_iid_policy_review.py'
frozen_report = source.with_suffix('.json')
raw = source.read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'b00ab9598462ea0836b3bf8720d5d5054d58ddb663a81fab5847f543357f04b1'
tree = ast.parse(raw, filename=str(source))
original_main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
assert isinstance(original_main.body[0], ast.Assign)
assert ast.unparse(original_main.body[0]) == 'rows = []'
assert isinstance(original_main.body[1], ast.For)
assert ast.literal_eval(original_main.body[1].iter) == [(2, 2), (3, 2), (3, 3), (4, 4), (5, 5), (6, 4)]
assert isinstance(original_main.body[2], ast.Assign)
assert ast.unparse(original_main.body[2]).startswith('m = K = 100')

# Load the exact imports and definitions, but omit the module's main guard.
definitions = ast.Module(body=[n for n in tree.body if not isinstance(n, ast.If)], type_ignores=[])
namespace = {'__name__': 'frozen_finite_policy_prefix', '__file__': str(source)}
exec(compile(definitions, str(source), 'exec'), namespace)
canonical = namespace['verify_certificate']
verifier_rows = []

def observed_verify(instance, certificate):
    result = canonical(instance, certificate)
    verifier_rows.append({'m': instance.players, 'K': instance.topic_count - 2,
                          'valid': result.valid, 'checked_histories': result.checked_histories,
                          'checked_deviations': result.checked_deviations,
                          'violations': len(result.violations), 'errors': list(result.errors)})
    return result

namespace['verify_certificate'] = observed_verify
prefix = ast.FunctionDef(name='finite_prefix_only', args=original_main.args,
                         body=original_main.body[:2] + [ast.Return(value=ast.Name(id='rows', ctx=ast.Load()))],
                         decorator_list=[])
prefix_tree = ast.fix_missing_locations(ast.Module(body=[prefix], type_ignores=[]))
prefix_ast_sha = hashlib.sha256(ast.dump(prefix_tree, include_attributes=False).encode()).hexdigest()
exec(compile(prefix_tree, str(source) + '#main-finite-prefix-only', 'exec'), namespace)
started = time.monotonic()
rows = namespace['finite_prefix_only']()
elapsed = time.monotonic() - started
expected = json.loads(frozen_report.read_text())['finite_full_history_checks']
assert rows == expected
for row, checked in zip(rows, verifier_rows):
    assert checked['valid'] and not checked['violations'] and not checked['errors']
    assert checked['checked_histories'] == row['ordered_decision_histories']
    assert checked['checked_deviations'] == row['direct_comparisons']
    p = row['K'] + 2
    assert row['ordered_decision_histories'] == sum(p ** d for d in range(row['m']))
    assert row['direct_comparisons'] == (p - 1) * row['ordered_decision_histories']
    assert row['W'] == 2 * row['m']
    assert row['OPT'] == 2 * row['m'] + min(row['K'], row['m'] - 1)
result = {'status': 'passed', 'entry_attempts': 1, 'entry_successes': 1,
          'full_original_main_calls': 0, 'original_finite_prefix_calls': 1,
          'threshold_original_main_calls': 0, 'iid_cut_and_threshold_scalar_reruns': 0,
          'equilibrium_solver_calls': 0, 'LP_solver_calls': 0,
          'assertions_enabled': sys.flags.optimize == 0,
          'source_sha256': hashlib.sha256(raw).hexdigest(),
          'frozen_report_sha256': hashlib.sha256(frozen_report.read_bytes()).hexdigest(),
          'finite_prefix_ast_sha256': prefix_ast_sha,
          'extraction_contract': 'Exact original main.body[0:2], plus return rows; exact original imports and helper definitions; original main and main guard not called.',
          'finite_full_history_checks': rows, 'canonical_verifier_checks': verifier_rows,
          'all_six_frozen_rows_equal': True,
          'total_ordered_decision_histories': sum(r['ordered_decision_histories'] for r in rows),
          'total_direct_nonself_comparisons': sum(r['direct_comparisons'] for r in rows),
          'elapsed_seconds': elapsed}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'finite_cases': len(rows),
                  'histories': result['total_ordered_decision_histories'],
                  'nonself_comparisons_per_method': result['total_direct_nonself_comparisons'],
                  'frozen_rows_equal': True, 'scalar_reruns': 0}, ensure_ascii=False))
