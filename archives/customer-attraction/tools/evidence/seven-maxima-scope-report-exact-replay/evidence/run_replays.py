"""Save one author-entry replay and one independently implemented report check.

This runner does not run LP or construct or audit a complete SPE. The author
script is unmodified. It reports 3872 columns for its modified target.
"""
from pathlib import Path
import ast
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    events = []
    for name, script in [('author', ROOT/'original/audit_dense_shared_seven_n6.py'),
                         ('independent', HERE/'verify_scope_report.py')]:
        r = subprocess.run([sys.executable, '-I', str(script)], cwd=HERE, capture_output=True)
        (HERE/f'{name}-stdout.txt').write_bytes(r.stdout)
        (HERE/f'{name}-stderr.txt').write_bytes(r.stderr)
        events.append(dict(name=name, command=[sys.executable,'-I',str(script)], cwd=str(HERE),
                           entry_executions_in_this_runner=1, exit_code=r.returncode,
                           source_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),
                           stdout_sha256=hashlib.sha256(r.stdout).hexdigest(), stderr_size=len(r.stderr),
                           assertions_enabled=True))
        assert r.returncode == 0 and not r.stderr
    author = ast.literal_eval((HERE/'author-stdout.txt').read_text())
    independent = json.loads((HERE/'independent-stdout.txt').read_text())
    assert author['columns'] == independent['author_modified_target']['columns'] == 3872
    assert author['minimum'] == independent['author_modified_target']['minimum']
    assert list(author['arg']) == [3, 8, 40]
    assert independent['all_original_fields_equal']
    output = dict(events=events, original_JSON_writer_not_found=True,
                  author_stdout_is_not_the_original_scope_JSON=True,
                  author_entry_modified_target='W - (U - private_at_index6)/2',
                  persisted_independent_verifier_executions=1,
                  other_internal_reconstruction='Internal reading subagent reported one separate unsaved in-memory Fraction reconstruction before duplicate-run avoidance message; no original checker entry run there.',
                  LP_runs=0, complete_SPE_audits=0, scope='literal coefficients and static coverage only')
    (HERE/'execution-record.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(author_exit=0, independent_exit=0, original_report_all_eight_fields_equal=True,
                          dense_columns=independent['dense']['columns'], author_modified_target_columns=author['columns']),ensure_ascii=False))


if __name__ == '__main__':
    main()
