"""Check preserved byte identities and saved report bindings only.

No original module is imported. This does not run a solver, reconstruct row
coefficients, rerun a strategy, or certify the mathematical recorded results.
"""
from pathlib import Path
import ast
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def inspect():
    primary = json.loads((HERE / 'source-manifest.json').read_text())
    related = json.loads((HERE / 'dependency-manifest.json').read_text())
    by_name = {}
    for record in primary + related:
        path = REPO / record['preserved_repo_path']
        raw = path.read_bytes()
        if record.get('encoding') == 'gzip':
            raw = gzip.decompress(raw)
        assert len(raw) == record['size']
        assert hashlib.sha256(raw).hexdigest() == record['sha256']
        name = Path(record['path']).name
        assert name not in by_name
        by_name[name] = (record, raw)
        if name.endswith('.py'):
            ast.parse(raw.decode(), filename=record['path'])
    assert len(primary) == 14 and len(related) == 16

    def document(name):
        return json.loads(by_name[name][1])

    bindings = []

    def bind(report, field, target, data=None):
        report_data = document(report) if data is None else data
        actual = by_name[target][0]['sha256']
        assert report_data[field] == actual, (report, field, target)
        bindings.append(dict(report=report, field=field, target=target,
                             sha256=actual, match=True))

    bind('actual13_two_state_certificate.json', 'code_sha256',
         'actual13_two_state_certificate.py')
    bind('actual13_two_state_certificate.json', 'source_certificate_sha256',
         'actual13_projection.json')
    bind('actual13_projection.json', 'code_sha256', 'actual13_projection.py')
    bind('actual13_projection.json', 'source_exact_point_sha256',
         'exact_current_source_own_index_v1.json')
    bind('audit_matched_indexed_hinges.json', 'target_code_sha256',
         'indexed_hinge_pricing.py')
    bind('audit_max_indexed.json', 'audited_code_sha256', 'max_indexed_coupling.py')
    bind('exact_indexed_separation.json', 'code_sha256', 'max_indexed_coupling.py')

    negative_lists = {}
    for source, result in document('exact_indexed_separation.json')['sources'].items():
        bind('exact_indexed_separation.json', 'source_sha256', source, result)
        assert result['rows'] == 1414
        assert result['negative_rows'] == len(result['negative_slacks'])
        negative_lists[source] = dict(reported_rows=result['rows'],
                                     saved_negative_values=len(result['negative_slacks']),
                                     other_row_values_saved=False)

    diagnostics = []
    for name, (record, _) in by_name.items():
        if name.startswith('joint_weighted_maxima_'):
            source = name.removeprefix('joint_weighted_maxima_')
            producer = 'joint_weighted_maxima.py'
        elif name.startswith('two_real_branches_'):
            source = name.removeprefix('two_real_branches_')
            producer = 'two_real_weighted_branches.py'
        else:
            continue
        result = document(name)
        bind(name, 'source_sha256', source)
        bind(name, 'code_sha256', producer)
        assert result['source_atoms'] == len(document(source)['atoms'])
        singles = result['single_history_diagnostics']
        diagnostics.append(dict(
            report=name, source_atoms=result['source_atoms'],
            actual_floating_status=singles['actual']['floating_lift_feasible'],
            max_floating_status=singles['max']['floating_lift_feasible'],
            saved_joint_field=('joint_history_diagnostic' in result
                               or 'floating_joint_lift_feasible' in result),
            saved_seconds=result.get('seconds'),
            status='saved diagnostics only; no LP or exact lift run here'))

    output = dict(
        status='PASS_SAVED_BYTES_AND_REPORT_BINDINGS_ONLY',
        primary_sources=len(primary), primary_bytes=sum(x['size'] for x in primary),
        related_dependencies=len(related), bindings=bindings,
        negative_lists=negative_lists, saved_lift_diagnostics=diagnostics,
        new_original_runs=0, new_math_coefficient_evaluations=0,
        scope='Byte identity, syntax and saved-field consistency; no new mathematical certification')
    (HERE / 'saved-identity-check.json').write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: output[k] for k in ['status', 'primary_sources',
                                           'primary_bytes', 'related_dependencies']}))


if __name__ == '__main__':
    inspect()
