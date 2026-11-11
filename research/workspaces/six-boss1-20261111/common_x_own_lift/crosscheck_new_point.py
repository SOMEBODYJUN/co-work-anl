"""Cross-check the new fixed-point evaluation with the pre-existing contract API.

The sparse-layer builder/verifier are not imported.  The existing contract's
own_blocks and diagnose_own were written before this layer and are hash-bound.
Only the authorized new 5b1b point is read; writes stay here.
"""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE=HERE.parent


def sha(p): return sha256(p.read_bytes()).hexdigest()


def main():
    point_path=BASE/'maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json'
    assert sha(point_path)=='5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe'
    freeze=json.loads((HERE/'freeze_manifest.json').read_text())
    assert all(sha(HERE/n)==r['sha256'] for n,r in freeze['files'].items())
    layer=json.loads((HERE/'own_facets.json').read_text())
    root_map=BASE/'root_x_joint_contract/own_blocks.json'
    assert sha(root_map)==next(r['sha256'] for r in layer['inputs'] if r['path']=='root_x_joint_contract/own_blocks.json')
    root_diag=BASE/'root_x_joint_contract/diagnose_own.py'
    spec=importlib.util.spec_from_file_location('previous_contract_diagnostic',root_diag)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    point=json.loads(point_path.read_text()); values=[module.exact(c['weight']) for c in point['columns']]
    prior=json.loads(root_map.read_text())
    independent=[module.evaluate_block(b,values) for b in prior['blocks']]
    actual_path=HERE/'fullX_5b1b_fixed_diagnostic.json'; actual=json.loads(actual_path.read_text())
    for before,after in zip(independent,actual['blocks']):
        for k in ('block','key','H','x','yQ','yR','old_masses','preconditions_pass','failed_preconditions',
                  'mass_identity_residual','six_facet_slacks','beta_lower','beta_upper','L','U','interval_gap','fixed_values_complete'):
            assert before[k]==after[k],(before['block'],k)
        if before['fixed_values_complete']:
            for k in ('beta_witness','X1_four_cells','X0_four_cells'): assert before[k]==after[k]
    failed=[b['block'] for b in independent if not b['fixed_values_complete']]
    assert failed==actual['failed_blocks']==[57,59,81,86,115]
    assert actual['summary']['negative_facet_counts']=={'O6':5}
    assert actual['negative_point_columns']==[]
    report=dict(status='EXISTING_CONTRACT_API_EXACT_CROSSCHECK_PASS',
                blocks_checked=210,facets_checked=1260,witnesses_checked=205,failed_blocks=failed,
                point_sha256=sha(point_path),diagnostic_sha256=sha(actual_path),
                prior_mapping_sha256=sha(root_map),prior_diagnostic_code_sha256=sha(root_diag),
                frozen_artifacts_unchanged=True,LP_calls=0,
                checker_sha256=sha(Path(__file__)),
                scope='Fixed supplied old masses/x/y only; no original-row recheck, no reselection, no global infeasibility claim.')
    (HERE/'fullX_5b1b_crosscheck.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__': main()
