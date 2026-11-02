"""Recover two original fixed-input audit entries without touching their sources.

Run once with a new --stage directory. This is an execution recorder, not a new
mathematical verifier, discovery search, or reconstruction of an old process.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    stage = args.stage.resolve()
    stage.mkdir(parents=True, exist_ok=False)
    terminal = stage/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_terminal'
    parent = terminal.parent/'next_boss/partition_attack'
    terminal.mkdir(parents=True)
    parent.mkdir(parents=True)
    original = here/'original'
    source = original/'950d924781d6bf698c1e--independent_partition_audit.py'
    audit = terminal/'independent_partition_audit.py'
    shutil.copyfile(source, audit)
    inputs = here.parent/'menu-partition-eight-boss3/original'
    dependencies = [inputs/name for name in ('small_exact_witness.json', 'exact_witness.json')]
    for dependency in dependencies:
        shutil.copyfile(dependency, parent/dependency.name)
    before = {str(p): sha(p) for p in [source, *dependencies]}
    checks = []
    for large, frozen_name, output_name in (
        (False, '9b64a5d486b1e177f5e9--independent_partition_small_audit.json', 'independent_partition_small_audit.json'),
        (True, 'a86a6d1d35753216ea80--independent_partition_audit.json', 'independent_partition_large_audit.json'),
    ):
        label = '127' if large else '14'
        destination = here/'replay'/label
        destination.mkdir(parents=True, exist_ok=False)
        argv = [sys.executable, '-I', '-B', str(audit)] + (['--large'] if large else [])
        start = datetime.now(timezone.utc).isoformat()
        clock = time.monotonic()
        result = subprocess.run(argv, cwd=stage, capture_output=True, check=False)
        elapsed = time.monotonic()-clock
        (destination/'stdout.txt').write_bytes(result.stdout)
        (destination/'stderr.txt').write_bytes(result.stderr)
        record = {
            'event': 'new fixed-input execution of the recovered frozen independent source; not historical execution identity',
            'argv': argv, 'cwd': str(stage), 'start_utc': start,
            'elapsed_seconds': elapsed, 'exit_code': result.returncode,
            'Python': sys.version, 'assertions_enabled': '-O' not in argv,
            'source_sha256': sha(source),
            'input_name': 'exact_witness.json' if large else 'small_exact_witness.json',
            'input_sha256': sha(parent/('exact_witness.json' if large else 'small_exact_witness.json')),
            'actual_output_basename': output_name,
            'stdout_bytes': len(result.stdout), 'stderr_bytes': len(result.stderr),
            'original_independent_audit_calls': 1, 'author_exact_audit_calls': 0,
            'LP_calls': 0, 'canonical_imports': 0, 'discovery_calls': 0,
        }
        dump(destination/'execution-record.json', record)
        assert result.returncode == 0 and not result.stderr
        generated = terminal/output_name
        generated_bytes = generated.read_bytes()
        assert generated_bytes == result.stdout
        (destination/'generated-report.json').write_bytes(generated_bytes)
        current = json.loads(generated_bytes)
        historical = json.loads((original/frozen_name).read_bytes())
        differences = [key for key in historical if historical[key] != current.get(key)]
        assert current.keys() == historical.keys()
        expected = ['minimum_partition_excess_over_W'] if large else []
        assert differences == expected, differences
        if large:
            assert historical[differences[0]] == 9 and current[differences[0]] == '9'
        author = json.loads((parent/('exact_witness.json' if large else 'small_exact_witness.json')).read_bytes())
        assert current['actual_path'] == [author['root_action'], author['complete_replies'][author['root_action']]]
        assert current['payoff_rows'][0]['payoffs'] == author['root_deviation_payoffs']
        assert [row['payoffs'] for row in current['payoff_rows'][1:]] == author['last_payoff_matrix']
        assert [row['chosen'] for row in current['payoff_rows'][1:]] == author['complete_replies']
        assert current['actual_payoffs'] == author['actual_payoffs']
        assert current['actual_W'] == author['W'] and current['OPT'] == author['OPT']
        assert current['all_optimal_ordered_portfolios'] == [author['unique_optimal_support'], author['unique_optimal_support'][::-1]]
        assert sorted(set(row['minimum_over_all_partitions'] for row in current['partition_minima'])) == sorted(set(author['partition_minima_for_two_matchings']))
        assert str(current['minimum_partition_excess_over_W']) == author['minimum_excess_over_W']
        assert current['unit_clients_expanded'] == author['unit_customers']
        assert current['half_coverage_holds'] == author['half_coverage_holds']
        checks.append({
            'clients': int(label), 'frozen_report': frozen_name,
            'frozen_sha256': sha(original/frozen_name),
            'current_generated_sha256': sha(generated),
            'frozen_and_current_bytes_equal': (original/frozen_name).read_bytes() == generated_bytes,
            'all_top_level_keys_equal': True,
            'different_fields': [
                {'field': key, 'historical': historical[key], 'historical_type': type(historical[key]).__name__,
                 'current': current[key], 'current_type': type(current[key]).__name__}
                for key in differences
            ],
            'all_other_fields_equal': True,
            'all_numeric_mathematical_values_agree_with_author_input': True,
            'original_input_stored_payoffs_read_by_audit': False,
            'author_input_and_primary_report_comparison_is_packaging_check': True,
        })
    after = {str(p): sha(p) for p in [source, *dependencies]}
    assert before == after
    dump(here/'replay-comparison.json', {
        'scope': 'two recovered original independent fixed-input entries; no author audit or discovery rerun',
        'records': checks, 'source_and_dependencies_unchanged': before == after,
        'independent_entries': 2, 'author_exact_audit_entries': 0,
        'discovery_entries': 0, 'LP_calls': 0, 'canonical_imports': 0,
    })
    print(json.dumps({'independent_entries': 2, 'checks': checks}, ensure_ascii=False))


if __name__ == '__main__':
    main()
