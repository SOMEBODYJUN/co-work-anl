"""Compare two saved reports as data; do not execute a mathematical audit.

The original prefix program and the mature independent definition checker are
both deliberately left unexecuted. No harmonic numbers or coefficients are
recomputed here. The expected old report is a projection of already saved EF
results, whose complete input/output hashes are recorded below.
"""
from pathlib import Path
import hashlib
import json

E = Path(__file__).resolve().parent
OLD = E / 'original/c0bad8199191aa2cfa27--prefix_absence_audit.json'
CODE = E / 'original/a645d421e80daabb96e8--prefix_absence_audit.py'
EF = E.parent / 'repeated-last-prefix-and-partition-primary/new-definition-check.json'
EF_RECORD = EF.parent / 'runtime-record.json'
OUTPUT = E / 'saved-report-comparison.json'


def fingerprint(path):
    raw = path.read_bytes()
    return {'path': str(path.relative_to(E.parents[4])),
            'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    if OUTPUT.exists():
        raise SystemExit('Saved report comparison already completed; preserve the event')
    old = json.loads(OLD.read_text())
    ef = json.loads(EF.read_text())
    record = json.loads(EF_RECORD.read_text())
    assert fingerprint(EF)['sha256'] == record['output_sha256']
    assert fingerprint(EF)['bytes'] == record['output_bytes']
    assert ef['status'] == 'pass'
    cases = ef['all_m_k_cases']
    improvements = [
        {key: case[key] for key in ['m', 'k', 'd', 'gamma']}
        for case in cases
        if case['m'] <= 20 and case['harmonic_certifies'] and not case['old_residual']
    ]
    expected = {
        'status': 'formula_audit_passed',
        'scope': 'analytic proof is in prefix_absence_repeated_last.md; finite audit only',
        'pattern_cases_m_le_12': ef['prefix_pattern_checks_m_le_12'],
        'coefficient_cases_m_le_100': ef['coefficient_checks_m_le_100'],
        'old_criterion_implications': ef['old_residual_to_harmonic_inclusions'],
        'polynomial_criterion_implications': ef['polynomial_certified_cases'],
        'strict_improvements_m_le_20': improvements,
    }
    compared = {key: old.get(key) == value for key, value in expected.items()}
    same = old == expected
    result = {
        'status': 'saved_reports_equal' if same else 'saved_report_difference',
        'comparison_only': True,
        'original_program_entry_runs_in_this_batch': 0,
        'mature_definition_checker_entry_runs_in_this_batch': 0,
        'new_harmonic_or_coefficient_evaluations': 0,
        'optimizer_calls': 0,
        'inputs': [fingerprint(p) for p in [OLD, CODE, EF, EF_RECORD]],
        'mature_record_hash_matches_saved_output': True,
        'saved_m_k_rows_read': len(cases),
        'compared_fields': compared,
        'unexpected_old_keys': sorted(set(old) - set(expected)),
        'strict_improvement_rows_equal_in_order': old.get('strict_improvements_m_le_20') == improvements,
        'strict_improvement_rows': len(improvements),
        'whole_parsed_json_equal': same,
        'limits': 'Data equality is not an original-program replay, independent new mathematical enumeration, historical argv recovery, SPE verification, or a universal proof.',
    }
    with OUTPUT.open('x') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    assert same, compared
    print('saved_reports_equal: 7 fields; 17 ordered improvement rows; no mathematical audit executed')


if __name__ == '__main__':
    main()
