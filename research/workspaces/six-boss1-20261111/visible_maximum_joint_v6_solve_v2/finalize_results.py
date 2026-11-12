#!/usr/bin/env python3
"""Freeze the completed v2 evidence without importing or invoking any solver."""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
WS=HERE.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((HERE/name).read_text())


def durable_json(name,data):
    payload=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
    fd=os.open(HERE/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
    with os.fdopen(fd,'wb') as stream:
        stream.write(payload);stream.flush();os.fsync(stream.fileno())


def main():
    for name in ['result_summary.json','freeze_manifest.json','SHA256SUMS']:
        assert not (HERE/name).exists(), 'Already frozen or partially frozen: '+name
    scaffold=read('scaffold_manifest.json')
    assert digest(HERE/'scaffold_manifest.json')=='3f16193e13ac0cb04c4f3272fc068e4922adf661a3b41d627ad64b87db244ec8'
    for name,expected in scaffold['artifact_sha256'].items():
        assert digest(HERE/name)==expected,name
    assert len(scaffold['code_artifact_sha256'])==9
    immutable={
        'exact_certificate.json':'bbacce728e8172049b52e8468e4e6921d316854a2113528e5c74d64d7372f028',
        'optimal_face.json':'7258aacace9180c43e8bc8a30a103bc3bd090eb6c19dd77f9a771c01d2c8be77',
        'independent_check_result.json':'daed49eecbec08d58884cff6c2b290e080e0bfcab81fd9ebb99921a2482dc18d',
        'optimal_face_check_result.json':'5e6e8d460f3ab98f09ec25f45f2f174a4302c21c9a591a2c2743a6943541b33b',
        'single_lp_consumed.json':'115a3c3ebbec578d682dd0355e8dbe21e78cddee700c2a2f24fb7dd6aa72a209',
        'main_release.json':'9aed677521b19c1c4c4a41a0ef644cf1f540c037c6509210107297479dc4d741',
    }
    for name,expected in immutable.items():assert digest(HERE/name)==expected,name
    at_solve=read('source_pins_at_solve.json')
    for path,expected in at_solve.items():assert digest(REPO/path)==expected,path
    fresh_pins=read('fresh_diagnostic_source_pins.json')
    for path,record in fresh_pins['files'].items():
        p=REPO/path
        assert digest(p)==record['sha256'] and p.stat().st_size==record['bytes'],path
    predecessor=read('predecessor_obstacle_pins.json')
    for path,expected in predecessor['files'].items():assert digest(REPO/path)==expected,path
    old=WS/'visible_maximum_joint_v6_solve'
    for name,expected in predecessor['original_core_sha256'].items():assert digest(old/name)==expected,name
    assert not (old/'single_lp_consumed.json').exists()
    revoke=WS/'registration/v6_first_release_revoked.json'
    assert digest(revoke)=='5ec0322aaeccc5c102a38f53368ebff7d45468c86174159dcb17029c033d0c61'
    for entry in read('expected_outputs.json')['post_release_order']:
        for name in entry['outputs']:assert (HERE/name).is_file(),name
    for name in ['fresh_payment_branches.py','verify_fresh_payment_branches.py','finalize_results.py']:
        text=(HERE/name).read_text();tree=ast.parse(text);compile(text,str(HERE/name),'exec')
        modules=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):modules.extend(z.name for z in node.names)
            elif isinstance(node,ast.ImportFrom):modules.append(node.module)
        assert all(x and x.split('.')[0] in ['ast','datetime','fractions','hashlib','itertools','json','os','pathlib'] for x in modules)
    c=read('exact_certificate.json');f=read('optimal_face.json');n=read('numerical_summary.json')
    cc=read('independent_check_result.json');fc=read('optimal_face_check_result.json')
    d=read('fresh_payment_branches.json');dc=read('fresh_payment_branches_check.json');mark=read('single_lp_consumed.json')
    assert n['success'] is True and n['status']==0 and n['iterations']==72
    assert mark['optimizer_calls_consumed']==1 and mark['raw_inequalities']==4177 and mark['nonnegative_columns']==513 and mark['equalities']==2
    assert cc['status']=='PASS_FULL_RAW_FRACTION_VERIFICATION_V6'
    assert fc['status']=='PASS_COMPLETE_OPTIMAL_FACE_FRACTION_VERIFICATION_V6'
    assert dc['status']=='PASS_INDEPENDENT_FRESH_TRUE_PAYMENT_AND_WHOLE_FACE_OBSTRUCTION'
    assert dc['diagnostic_sha256']==digest(HERE/'fresh_payment_branches.json')
    summary={
        'schema':'visible_maximum_joint_v6_solve_v2_completed_summary_v1',
        'status':'COMPLETE_EXACT_SINGLE_LP_FULL_FACE_AND_FRESH_DIAGNOSTICS',
        'agent':'/root/visible_joint_v6_solve','owner':'Boss1','RUN':'six-boss1-20261111',
        'input_sha256':c['input_sha256'],'release_sha256':immutable['main_release.json'],
        'source_and_release_checkpoint_reported_by_main':'511725e6d2e7bc37fde7983e613c1b4f84c470c7',
        'run_artifacts_checkpoint_state_at_freeze':'LOCAL_COMPLETE_WAITING_MAIN_SERIAL_CHECKPOINT; no Git, sync, or publication by this agent',
        'optimizer_calls_v1':0,'optimizer_calls_v2':1,'optimizer_calls_total':1,
        'consumption_marker_exists':True,'consumption_marker_sha256':immutable['single_lp_consumed.json'],
        'solver':mark['solver'],'options':mark['options'],'numeric_objective':n['objective'],'iterations':n['iterations'],
        'dimensions':{'all_raw_rows':4177,'all_nonnegative_columns':513,'signed_free_equalities':2,'affine_rhs_minus_one_rows':30},
        'objective':c['objective'],'objective_decimal':c['objective_decimal'],'half_gap':c['half_gap'],'K':c['K'],
        'primal_support':c['primal_support'],'positive_raw_indices':c['dual']['positive_raw_indices'],
        'positive_raw_rows_with_exact_raw_weights_and_metadata':c['dual']['positive_raw_rows'],
        'whole_face_zero_residual_columns':f['zero_residual_columns'],
        'whole_face_forced_zero_column_count':len(f['forced_zero_columns']),
        'whole_face_restricted_equation_rank':f['restricted_equation_rank'],
        'whole_face_unconstrained_affine_parameter_count':f['unconstrained_affine_parameter_count'],
        'whole_face_free_parameter_columns':[v['column'] for v in f['parameters']],
        'whole_face_all4177_and_all513_constraints_preserved':True,
        'relative_feasible_dimension_asserted':False,
        'fresh_same_history_groups':[{'ordered_history':g['ordered_history'],'raw_indices':g['raw_indices']} for g in d['same_history_weak_intersections']],
        'whole_face_SPE_obstruction':d['whole_face_SPE_obstruction'],
        'corrected_X_model':d['corrected_X_model'],
        'new_positive_wallet_parameters':[{'raw_index':r['raw_index'],'source':r['source'],'target':r['target'],
                                          'source_IC_weight':r['source_IC_weight'],'tau':r['tau'],'lambda':r['lambda'],
                                          's':r['s_25_minus_lambda'],'signed_C_equality_multiplier':r['signed_C_equality_multiplier'],
                                          'metadata':r['source_metadata_verbatim']} for r in d['seven_minimal_CAP_rows']],
        'independent_checks':{'certificate':cc['status'],'complete_face':fc['status'],'fresh_real_histories':dc['status']},
        'primary_sha256':{name:digest(HERE/name) for name in ['exact_certificate.json','independent_check_result.json','optimal_face.json','optimal_face_check_result.json','fresh_payment_branches.json','fresh_payment_branches_check.json','proof.md']},
        'scaffold_nine_core_files_unchanged':True,
        'prior_failure':'v1 source-pins interface preflight obstacle before any consumption, retained and bound by predecessor_obstacle_pins.json; Main revoked v1 release.',
        'v2_solver_recovery_or_verification_failure':None,
        'scope':'Exact optimum of this frozen necessary LP and a fresh obstruction to every SPE realization of its optimal face. No new rows, second optimization, uniform epsilon, or half claim.'
    }
    durable_json('result_summary.json',summary)
    artifacts={p.name:digest(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name not in ['freeze_manifest.json','SHA256SUMS']}
    manifest={
        'schema':'visible_maximum_joint_v6_solve_v2_final_freeze_v1',
        'status':'FROZEN_COMPLETE_EXACT_SINGLE_LP_V2_WITH_WHOLE_FACE_SPE_OBSTRUCTION',
        'agent':'/root/visible_joint_v6_solve','owner':'Boss1','RUN':'six-boss1-20261111',
        'freeze_utc':datetime.now(timezone.utc).isoformat(),
        'optimizer_calls_v1':0,'optimizer_calls_v2':1,'optimizer_calls_total':1,
        'input_sha256':c['input_sha256'],'release_sha256':immutable['main_release.json'],
        'source_and_release_checkpoint_reported_by_main':'511725e6d2e7bc37fde7983e613c1b4f84c470c7',
        'current_runtime_artifacts_remote_checkpoint_claimed':False,
        'consumption_marker_permanent':True,'no_optimizer_replay_authorized_or_performed':True,
        'raw_rows':4177,'nonnegative_columns':513,'equalities':2,
        'immutable_core_scaffold_artifacts_verified':len(scaffold['artifact_sha256']),
        'immutable_nine_core_verified':9,'source_pins_at_solve_verified':len(at_solve),
        'fresh_diagnostic_source_pins_verified':len(fresh_pins['files']),
        'prior_failure_pins_verified':predecessor['files'],
        'prior_release_revocation':{'path':str(revoke.relative_to(REPO)),'sha256':digest(revoke)},
        'prior_v1_marker_absent':True,'prior_v1_nine_core_verified':9,
        'exact_objective':c['objective'],'K':c['K'],
        'positive_raw_indices':c['dual']['positive_raw_indices'],
        'whole_face_free_parameter_columns':[v['column'] for v in f['parameters']],
        'SPE_nonrealization_gap':dc['whole_face_SPE_obstruction_gap'],
        'independent_check_statuses':summary['independent_checks'],
        'artifacts':artifacts,
        'artifact_bytes':{name:(HERE/name).stat().st_size for name in artifacts},
        'artifact_count_excluding_manifest_and_checksums':len(artifacts),
        'historical_scaffold_or_queue_status_fields_preserved':True,
        'excluded_runtime_directories':['__pycache__'],
        'scope':summary['scope']
    }
    durable_json('freeze_manifest.json',manifest)
    checksums={**artifacts,'freeze_manifest.json':digest(HERE/'freeze_manifest.json')}
    checksum_data=''.join(h+'  '+name+'\n' for name,h in sorted(checksums.items()))
    fd=os.open(HERE/'SHA256SUMS',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
    with os.fdopen(fd,'w') as stream:
        stream.write(checksum_data);stream.flush();os.fsync(stream.fileno())
    for name,expected in checksums.items():assert digest(HERE/name)==expected
    dirfd=os.open(HERE,os.O_RDONLY)
    try:os.fsync(dirfd)
    finally:os.close(dirfd)
    print(json.dumps({'status':manifest['status'],'artifact_count':len(artifacts),
                      'checksum_lines':len(checksums),'freeze_manifest_sha256':digest(HERE/'freeze_manifest.json'),
                      'SHA256SUMS_sha256':digest(HERE/'SHA256SUMS'),
                      'result_summary_sha256':digest(HERE/'result_summary.json'),
                      'proof_sha256':digest(HERE/'proof.md'),'optimizer_calls_total':1},indent=2))


if __name__=='__main__':main()
