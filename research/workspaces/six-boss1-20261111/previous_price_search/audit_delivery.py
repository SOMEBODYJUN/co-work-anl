#!/usr/bin/env python3
"""Check delivered Actions provenance and summarize the 90 replayed cones.

This script only reads frozen inputs, delivered artifacts and completed local
Fraction replays.  It neither imports the discovery code nor runs an optimizer.
"""
from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
ROOT = RUN.parents[2]
DISPATCH = RUN/'compute_dispatch'
RUN_ID = 43074273655
HEAD = '08d120b3337d3f3fcd608432bb288edcc81f8d33'
TAGS = {'14': F(1, 4), '12': F(1, 2), '34': F(3, 4)}
FIXED = {
    'peer_augmented_lp/augmented_lp_exact.json': 'd70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f',
    'peer_augmented_lp/exact_matrix.json.gz': '6ebf5f2f10843c5cee74391d057fe545449fb45a4e72f18d665e2a00258b6ea9',
    'previous_price_search/discover.py': '0fef4e8102e6336426821f437413bce338309528b2a56f2be9687b0eaac10bcd',
    'previous_price_search/verify.py': 'a84fb5666224665a8f95e944ceb6237e5b728126ea1eb839e3afcdcba2f8c9ba',
}


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).relative_to(ROOT).as_posix()


def file_record(path):
    path = Path(path)
    return {'path': relative(path), 'sha256': digest(path), 'bytes': path.stat().st_size}


def pin(value):
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def extremum(rows, field):
    row = min(rows, key=lambda r: F(r[field]))
    return {'case_id': row['case_id'], 'source': row['source'], 'seed': row['seed'], 'theta': row['theta'],
            'exact': row[field], 'approximate': float(F(row[field]))}


def main():
    for name, expected in FIXED.items():
        assert digest(RUN/name) == expected
    specs = read(HERE/'computations.json')['experiments']
    bindings = {row['name']: row for row in read(HERE/'input_bindings.json')['experiments']}
    delivery = {row['theta']: row for row in read(DISPATCH/'delivery.json')}
    run = read(DISPATCH/f'run{RUN_ID}.json')
    artifacts = read(DISPATCH/f'run{RUN_ID}-artifacts.json')
    assert run['id'] == artifacts['run_id'] == RUN_ID
    assert run['head_sha'] == HEAD and run['status'] == 'completed' and run['conclusion'] == 'success'
    assert run['artifacts'] == artifacts['artifacts']
    expected_inputs = sorted((relative(RUN/name), expected) for name, expected in FIXED.items())
    provenance, cases, audits = [], [], []
    seen = set()
    for tag, theta in TAGS.items():
        name = f'six-boss1-previous-price-19621-theta{tag}'
        request = f'C-six-boss1-prev-price-19621-t{tag}-01'
        job = next(row for row in run['jobs'] if row['name'] == 'compute/'+request)
        assert job['status'] == 'completed' and job['conclusion'] == 'success'
        artifact = next(row for row in artifacts['artifacts'] if row['name'] == 'compute-'+request+'-1')
        archive = DISPATCH/f'price-theta{tag}.zip'
        assert artifact['digest'] == 'sha256:'+digest(archive)
        assert artifact['size_in_bytes'] == archive.stat().st_size
        unpacked = DISPATCH/f'price-theta{tag}'
        output = HERE/f'actions_theta{tag}'
        receipt_path = ROOT/delivery[tag]['result_path']
        receipt = read(receipt_path)
        assert digest(receipt_path) == delivery[tag]['result_sha256']
        assert receipt['request_id'] == request and receipt['experiment'] == name
        assert receipt['commit'] == delivery[tag]['commit'] == HEAD
        assert receipt['status'] == delivery[tag]['status'] == 'completed' and receipt['exit_code'] == 0
        assert receipt['spec'] == specs[name]
        assert receipt['experiment_pin'] == bindings[name]['experiment_pin'] == pin(specs[name])
        assert sorted((row['path'], row['sha256']) for row in receipt['input_files']) == expected_inputs
        assert receipt['input_files'] == bindings[name]['files']
        assert receipt['command'][1:] == specs[name]['command'][1:]
        assert specs[name]['python_packages'] == ['numpy==2.3.5', 'scipy==1.17.0']
        assert receipt['elapsed_seconds'] < specs[name]['timeout_seconds'] == 600
        stdout_path, stderr_path = unpacked/receipt['stdout_file'], unpacked/receipt['stderr_file']
        assert stderr_path.read_bytes() == b''
        stdout = [json.loads(line) for line in stdout_path.read_text().splitlines()]
        original_output = unpacked/relative(output)
        originals = {path.name: digest(path) for path in original_output.iterdir() if path.is_file()}
        copies = {path.name: digest(path) for path in output.iterdir() if path.is_file()}
        assert originals == copies and len(copies) == 33
        manifest = read(output/'manifest.json')
        summary = read(output/'summary.json')
        cloud_audit = read(output/'independent_audit.json')
        local_path = HERE/f'local_replay_theta{tag}.json'
        local = read(local_path)
        assert manifest['generator_sha256'] == FIXED['previous_price_search/discover.py']
        assert manifest['verifier_sha256'] == FIXED['previous_price_search/verify.py']
        assert manifest['point_sha256'] == FIXED['peer_augmented_lp/augmented_lp_exact.json']
        assert manifest['matrix_sha256'] == FIXED['peer_augmented_lp/exact_matrix.json.gz']
        assert manifest['runtime'] == {'python': receipt['python'], 'numpy': '2.3.5', 'scipy': '1.17.0'}
        assert len(manifest['result_files']) == len(manifest['cases_requested']) == summary['cases'] == 30
        expected = set(product(range(1, 6), range(1, 7), (theta,)))
        assert {(a, b, F(t)) for a, b, t in manifest['cases_requested']} == expected
        assert cloud_audit['all_checks_passed'] and local['all_checks_passed']
        assert cloud_audit['cases'] == local['cases']
        assert local['case_count'] == cloud_audit['case_count'] == 30
        assert local['manifest_sha256'] == digest(output/'manifest.json')
        assert local['verifier_sha256'] == FIXED['previous_price_search/verify.py']
        assert (HERE/f'local_replay_theta{tag}.stderr.txt').read_bytes() == b''
        assert [row for row in stdout if 'case_id' in row] == summary['results']
        audited = {row['case_id']: row for row in local['cases']}
        assert len(audited) == 30
        assert {row['verified'] for row in stdout if 'verified' in row} == set(audited)
        assert sum(row.get('completed_cases', 0) for row in stdout) == 30
        local_cases = set()
        for item in manifest['result_files']:
            path = output/item['file']
            assert path.parent == output and digest(path) == item['sha256']
            row = read(path)
            key = row['source'], row['seed'], F(row['theta'])
            assert key in expected and key not in local_cases and key not in seen
            local_cases.add(key); seen.add(key)
            proof = row['occupation_certificate']
            audit = audited[row['case_id']]
            assert row['success'] and audit['exact_slack'] == row['exact_slack']
            assert proof['exact_cone_lower_bound'] == audit['exact_cone_lower_bound']
            assert proof['active_parameter_lower_bound'] == audit['active_parameter_lower_bound']
            lower, active = F(proof['exact_cone_lower_bound']), F(proof['active_parameter_lower_bound'])
            assert lower >= 0 and active > F(1, 400)
            assert F(row['exact_slack']) >= active
            assert proof['nonseparation_certified'] and audit['nonseparation_certified']
            residuals = proof['all_parameter_residuals']
            if row['source'] == 5:
                assert lower == 0 and F(residuals['alpha_m']) == F(residuals['beta_m']) == 0
                assert all(F(value) > F(1, 400) for name_, value in residuals.items() if name_ not in ('alpha_m', 'beta_m'))
            else:
                assert lower == active > F(1, 400)
            assert audit['original_coefficients_checked'] == 4849
            assert audit['auxiliary_zero_coefficients_checked'] == 10744
            cases.append({'case_id': row['case_id'], 'source': row['source'], 'seed': row['seed'], 'theta': row['theta'],
                          'case_file': file_record(path), 'exact_slack': row['exact_slack'],
                          'complete_14_parameter_lower_bound': str(lower), 'active_parameter_lower_bound': str(active),
                          'mu_previous': row['parameters_full'][-1],
                          'parameters': row['parameters'], 'nonseparation_certified': True,
                          'original_coefficients_checked': 4849, 'auxiliary_zero_coefficients_checked': 10744,
                          'independent_bellman_types': audit['independent_bellman_types'],
                          'occupation_flow_equations_checked': audit['occupation_flow_equations_checked'],
                          'complete_boolean_domain_checked': audit['complete_boolean_domain_checked']})
        assert local_cases == expected
        audits.append(file_record(local_path))
        provenance.append({'theta': str(theta), 'request_id': request, 'job_id': job['id'],
                           'artifact_id': artifact['id'], 'artifact_digest': artifact['digest'],
                           'zip': file_record(archive), 'receipt': file_record(receipt_path),
                           'stdout': file_record(stdout_path), 'stderr': file_record(stderr_path),
                           'experiment_pin': receipt['experiment_pin'], 'runtime': manifest['runtime'],
                           'cloud_manifest': file_record(output/'manifest.json'),
                           'cloud_audit': file_record(output/'independent_audit.json'),
                           'local_audit': file_record(local_path), 'execution_seconds': receipt['elapsed_seconds'],
                           'copied_files_byte_identical': 33, 'case_count': 30})
    expected_all = set(product(range(1, 6), range(1, 7), TAGS.values()))
    assert seen == expected_all and len(cases) == 90
    cases.sort(key=lambda row: (F(row['theta']), row['source'], row['seed']))
    positive_nu = [row for row in cases if F(row['mu_previous']) > 0]
    assert len(positive_nu) == 7
    assert sum(F(row['complete_14_parameter_lower_bound']) > 0 for row in cases) == 72
    assert sum(F(row['complete_14_parameter_lower_bound']) == 0 for row in cases) == 18
    per_theta = []
    for theta in TAGS.values():
        subset = [row for row in cases if F(row['theta']) == theta]
        per_theta.append({'theta': str(theta), 'case_count': 30,
                          'minimum_returned_slack': extremum(subset, 'exact_slack'),
                          'minimum_active_cone_bound': extremum(subset, 'active_parameter_lower_bound'),
                          'minimum_complete_14_bound_sources_1_to_4': extremum([row for row in subset if row['source'] < 5], 'complete_14_parameter_lower_bound'),
                          'minimum_k2_active_12_bound': extremum([row for row in subset if row['source'] == 5], 'active_parameter_lower_bound'),
                          'positive_mu_previous_returned_weights': sum(F(row['mu_previous']) > 0 for row in subset)})
    summary = {'status': 'completed-and-independently-replayed', 'actions_run_id': RUN_ID, 'pushed_head': HEAD,
               'scope': 'Exactly 5 actual sources x 6 fixed actual seeds x 3 listed discounts, one fixed static menu and the fixed 19621x15593 necessary LP point. No unsampled-discount, larger-menu, nested-cone, SPE or half conclusion.',
               'case_count': 90, 'unique_case_count': 90, 'complete_cartesian_product_verified': True,
               'negative_rows': [], 'uncertified_cones': [], 'exact_nonseparation_certificates': 90,
               'strict_complete_14_parameter_cones': 72, 'zero_bound_complete_14_parameter_cones': 18,
               'zero_bound_reason': 'Only source actual5, k=2: alpha_m and beta_m are identically ineffective directions. Every one of the remaining 12 residuals is strictly positive.',
               'strict_active_parameter_cones': 90, 'simple_uniform_active_lower_bound': '1/400',
               'simple_bound_comparison': 'Every exact active-parameter cone lower bound is strictly greater than 1/400.',
               'minimum_returned_slack': extremum(cases, 'exact_slack'),
               'minimum_active_cone_bound': extremum(cases, 'active_parameter_lower_bound'),
               'minimum_complete_14_cone_bound': '0', 'by_theta': per_theta,
               'positive_mu_previous_count': len(positive_nu),
               'positive_mu_previous_cases': [{key: row[key] for key in ('case_id', 'source', 'seed', 'theta', 'mu_previous', 'exact_slack')} for row in positive_nu],
               'replayed_occupation_flow_equations': sum(row['occupation_flow_equations_checked'] for row in cases),
               'replayed_bellman_types': sum(row['independent_bellman_types'] for row in cases),
               'stationary_next_bit_policies_per_type': 16,
               'original_column_checks': 90*4849, 'auxiliary_zero_column_checks': 90*10744,
               'full_boolean_audit_scope': 'No batch row was negative, so these 90 audits use all original coordinate types, not a claimed 448-type full-domain expansion for every case. The two earlier smoke cases separately received full 448-type and literal-Boolean audits.',
               'local_optimizer_runs_in_this_delivery_audit': 0}
    write(HERE/'all_90_cases.json', {'summary': summary, 'cases': cases})
    write(HERE/'delivery_audit.json', {'all_checks_passed': True, 'run_metadata': file_record(DISPATCH/f'run{RUN_ID}.json'),
                                     'artifact_metadata': file_record(DISPATCH/f'run{RUN_ID}-artifacts.json'),
                                     'delivery_binding': file_record(DISPATCH/'delivery.json'), 'batches': provenance})
    tracked = [HERE/'computations.json', HERE/'input_bindings.json', HERE/'audit_delivery.py',
               HERE/'all_90_cases.json', HERE/'delivery_audit.json', RUN/'previous_price_search.md',
               HERE/'COMPUTE_HANDOFF.md', HERE/'next_cross_source_contract.md']
    tracked += [HERE/f'local_replay_theta{tag}{suffix}' for tag in TAGS for suffix in ('.json', '.stdout.txt', '.stderr.txt')]
    write(HERE/'manifest.json', {'schema': 1, 'status': 'complete-frozen-for-main-checkpoint',
                                'task': 'previous_price_search', 'run': 'six-boss1-20261111',
                                'actions_run_id': RUN_ID, 'pushed_head': HEAD, 'summary': summary,
                                'frozen_compute_dependencies': [file_record(RUN/name) for name in FIXED],
                                'audit_artifacts': [file_record(path) for path in tracked],
                                'cloud_batches': provenance, 'pending_obligations': []})
    print(json.dumps({'case_count': 90, 'negative_rows': 0, 'exact_nonseparation_certificates': 90,
                      'positive_mu_previous_count': len(positive_nu),
                      'minimum_active_bound': summary['minimum_active_cone_bound'],
                      'manifest_sha256': digest(HERE/'manifest.json')}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
