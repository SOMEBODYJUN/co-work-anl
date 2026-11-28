"""Verify current inputs, unchanged prior results, fresh outputs and identities; retain raw evidence."""
import argparse
import csv
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED

from run_replay import SHA, WORK, OUT, OLD, LOCAL, LOGS, MODELS, JST, HOUSE, FORMAL, LEDGER, digest, read, write, frozen

PRIOR = '1580e869769a9410b88d040acf08bab394c6f9d2'
OLD_RECEIPT = 'ad736d10d0e1e8661de6ea47cfce18027d01b2de4d9ea84e641c777067335c06'
FORMAL_HASHES = {'report.md':'65afc995b3031ffbdff967633fd0aa37274629cad40b7880bae663cbb20f7b4c',
                 'judgments.json':'af04fefc8348bf50902501082b6cce62d386d91d7336699461cf71d35986049a',
                 'scenarios.json':'0133496a1354d514372e6bd9ed35efd83eb3ea6e914b5a2074a0e8bedaa7ae9b',
                 'calculator.html':'f0c72e3baa689bdbb6e7c4e75e12186e0fc1e2f6d2d59308ecdd39013a3ca049'}
ENGINE = 'e89e241afd96b9ce24b5df343ea9d1e8b14880f17ab265a31690d34b379dbeaa'
TIMINGS = {'/result/executed_at','/result/models/logit/elapsed_seconds','/result/models/hist_gradient_boosting/elapsed_seconds'}


def old_bytes(path):
    return subprocess.check_output(['git','show',PRIOR+':'+str(path)])


def normalized(value):
    def every(v,path):
        if isinstance(v,dict):
            return {k:every(x,path+'/'+k) for k,x in v.items() if path+'/'+k not in TIMINGS}
        if isinstance(v,list):
            return [every(x,path+'/'+str(i)) for i,x in enumerate(v)]
        return v
    return digest(json.dumps(every(value,''),ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())


def differences(before, after, path=''):
    if isinstance(before,dict) and isinstance(after,dict) and before.keys()==after.keys():
        return [item for k in before for item in differences(before[k],after[k],path+'/'+k)]
    if isinstance(before,list) and isinstance(after,list) and len(before)==len(after):
        return [item for i,(a,b) in enumerate(zip(before,after)) for item in differences(a,b,path+'/'+str(i))]
    return [] if type(before) is type(after) and before==after else [{'path':path,'frozen':before,'fresh':after}]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--formal-peer',type=Path, help='Matching source checkout, read-only; use when available')
    args=parser.parse_args()
    git_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    assert git_head == SHA
    status=read(LOGS/'status-before.stdout'); initial=read(LOGS/'session-start.stdout'); final=read(LOGS/'session-check.stdout')
    assert status==read(LOGS/'status-after.stdout') and len(status['completed_stages'])==17
    assert not status['graph']['unresolved'] and not status['graph']['unresolved_edges']
    assert initial['actor']==final['actor']=='boss 1' and initial['run_id']==final['run_id']=='35440ff34fc845dbaa2b3d94cf6d2c00'
    assert final['cycle']==1 and not final['complete'] and final['completed_stages']==status['completed_stages']
    state=read(WORK/'research_state.json')
    assert (WORK/'research_state.json').read_bytes()==frozen(WORK/'research_state.json') and LEDGER.read_bytes()==frozen(LEDGER)
    stages=[]
    for k in status['completed_stages']:
        for name,sha in state['stages'][k]['files'].items():
            path=WORK/name
            row={'stage':k,'file':name,'registered':sha,'git_object':digest(frozen(path)),'observed':digest(path.read_bytes())}
            assert row['registered']==row['git_object']==row['observed']
            stages.append(row)
    formal={}
    for p,expected in [(FORMAL/k,v) for k,v in FORMAL_HASHES.items()]+[(HOUSE/'engine.js',ENGINE)]:
        hashes={'expected':expected,'frozen_git':digest(frozen(p)),'new_clone':digest(p.read_bytes())}
        if args.formal_peer:
            hashes['source_checkout']=digest((args.formal_peer/p).read_bytes())
        assert len(set(hashes.values()))==1
        formal[str(p.relative_to(WORK))]=hashes

    code=sorted(Path('cncrisis').glob('*.py'))+[Path('work.py'),Path('crisis.py')]+sorted(Path('.').glob('requirements*.txt'))
    code_hash=digest(b''.join(str(p).encode()+b'\0'+p.read_bytes() for p in code))
    assert all(old_bytes(p)==frozen(p)==p.read_bytes() for p in code)
    baseline=read(LEDGER); expanded=read(LOCAL/'ledger-13.json')
    assert expanded['runs'][:-1]==baseline['runs'] and expanded['sessions'][:-1]==baseline['sessions']
    assert len(expanded['runs'])==13 and len(baseline['runs'])==12
    runs={r['id']:r for r in baseline['runs']}
    old_comparison=read(OLD/'comparisons.json'); prior={r['original_id']:r for r in old_comparison['runner']['jobs']}
    old_receipt=read(OLD/'receipt.json')
    assert digest((OLD/'receipt.json').read_bytes())==OLD_RECEIPT and old_receipt['verdict']=='fail'
    previous_files={'research/tasks/fresh_restore/receipt.json':OLD_RECEIPT,**old_receipt['artifact_sha256']}
    assert len(previous_files)==13 and all(digest((WORK/p).read_bytes())==sha==digest(frozen(WORK/p)) for p,sha in previous_files.items())
    current=read(MODELS/'compute-current.json')
    assert 'historical-warning-audit-v2' not in {j['id'] for j in current['jobs']}
    root=Path.cwd().resolve(); inherited=[]; local_inputs=[]
    with ZipFile(OLD/'raw_evidence.zip') as z:
        for job in current['jobs']:
            source=Path(job['input']); pathset=[source]
            spec=read(source)
            if spec.get('csv'):
                pathset.append(Path(spec['csv']))
            record={}
            for p in pathset:
                assert not p.is_absolute() and p.is_file() and p.resolve().is_relative_to(root)
                sha=digest(p.read_bytes()); assert sha==digest(frozen(p))
                record[str(p)]=sha
            local_inputs.append({'job':job['id'],'paths_and_sha256':record})
            if job['id']=='historical-warning-portable-v3':
                continue
            prev=prior[job['id']]; row=runs[job['id']]
            job_from_old=next(j for j in json.loads(old_bytes(WORK/prev['original_plan']))['jobs'] if j['id']==job['id'])
            assert job==job_from_old and not prev['source_spec_external_csv']
            assert all(record[str(p)]==digest(old_bytes(p))==prev['clone_input_hashes'][str(p)] for p in pathset)
            out=WORK/'compute'/row['output']; raw=z.read(prev['archived_as'])
            assert out.read_bytes()==old_bytes(out)==frozen(out)
            fresh_old_sha=digest(raw)
            original_sha=digest(out.read_bytes())
            old_replay=normalized(json.loads(raw)); current_result=normalized(read(out))
            assert row['status']=='complete' and row['input_sha256']==prev['clone_input_hashes'][str(source)]
            assert row['code_sha256']==code_hash==prev['code_sha256'] and row['environment_sha256']==prev['environment_sha256']
            assert row['fingerprint']==prev['fingerprint'] and original_sha==row['output_sha256']==prev['frozen_file_sha256']
            assert fresh_old_sha==prev['replay_file_sha256'] and old_replay==current_result==prev['replay_normalized_sha256']
            inherited.append({'id':job['id'],'spec_unchanged':True,'input_sha256':record,
                              'output_frozen_now_and_then':original_sha,'old_actual_output_in_archive':prev['archived_as'],
                              'old_real_execution_output_sha256':fresh_old_sha,'normalized_now_and_previous_actual':current_result,
                              'runner_code_sha256':code_hash,'environment_sha256':row['environment_sha256'],
                              'fingerprint':row['fingerprint'],'prior_actual_wall_seconds':prev['runner_wall_seconds']})
    assert len(inherited)==10 and len(local_inputs)==11
    old_model=runs['historical-warning-portable-v3']; actual=expanded['runs'][-1]
    assert actual['id']=='fresh-v2-'+old_model['id'] and actual['status']=='complete' and actual['wall_seconds']>0
    for key in ('method','input_sha256','code_sha256','environment_sha256','fingerprint','versions'):
        assert old_model[key]==actual[key]
    assert actual['code_sha256']==code_hash
    model_dir=WORK/'compute'
    a,b=read(model_dir/old_model['output']),read(model_dir/actual['output'])
    assert digest((model_dir/actual['output']).read_bytes())==actual['output_sha256']
    delta=differences(a,b); assert {x['path'] for x in delta}==TIMINGS
    assert normalized(a)==normalized(b)==old_comparison['runner']['portable_corrected_jst']['replay_normalized_sha256']
    assert b['result']['data_sha256']==digest((JST/'panel.csv').read_bytes())
    assert len(b['result']['test_predictions'])==374
    stages_mid=read(LOGS/'status-during-replay-ledger.stdout')
    assert len(stages_mid['completed_stages'])==4
    tests=read(HOUSE/'checks.json'); contracts=read(HOUSE/'python_reference_checks.json'); migration=read(HOUSE/'contract_migration_replay.json')
    with (HOUSE/'synthetic_strategy_results.csv').open() as f:
        rows=list(csv.DictReader(f))
    groups=defaultdict(list)
    for row in rows:
        groups[row['strategy']].append(row)
    three={'continuity','severe','recovery'}
    assert all(len(rs)==3 and {r['scenario'] for r in rs}==three for rs in groups.values())
    common={k for k, rs in groups.items() if all(r['feasible']=='true' for r in rs)}
    assert all((r['commonFeasible']=='true')==(r['strategy'] in common) for r in rows)
    counts={'rules':len(groups),'scenario_outcomes':len(rows),'common':len(common),
            'distinct_common_trajectories':len({r['trajectory'] for r in rows if r['strategy'] in common}),
            'distinct_all_trajectories':len({r['trajectory'] for r in rows}),
            'pareto':len({r['strategy'] for r in rows if r['pareto']=='true'})}
    assert list(counts.values())==[500,1500,134,105,416,6]
    assert tests['checks']==32 and tests['failures']==0
    periods=[r['compared_periods'] for r in contracts['comparisons']]; assert sum(periods)==146
    full=read(LOGS/'full-months.stdout'); pack=read(LOGS/'pack-months.stdout')
    assert full['newMonths']==full['oldMonths']==migration['observedMonthsCompared']==168216
    assert full['fields']==len(migration['comparedMonthlyFields'])==43 and full['unequalUnroundedPairs']==0
    assert full['unroundedNewJointSHA256']==full['unroundedOldJointSHA256']
    assert digest((LOCAL/'monthly_ledgers.npz').read_bytes())==pack['sha256'] and pack['round_trip_all_values_and_types']
    doctor=read(LOGS/'doctor.stdout')
    assert doctor['vendor_integrity']=='pass' and not doctor['vendor_failures']
    assert (LOGS/'pip-check.stdout').read_text().strip()=='No broken requirements found.'
    frozen_env=sorted((OLD/'resolved-environment.txt').read_bytes().splitlines())
    assert sorted((LOGS/'pip-freeze.stdout').read_bytes().splitlines())==frozen_env and len(frozen_env)==40
    restored=read(LOCAL/'regenerated.json')
    assert all(o['byte_equal'] and o['rewritten_or_created'] for r in restored for o in r['output'].values())
    result={
        'schema':'cncrisis-fresh-restore-verification.v2','commit':SHA,'old_commit':PRIOR,'binding':state['runtime'],'cycle':state['cycle'],
        'formal_and_engine':formal,'state_sha256':digest(frozen(WORK/'research_state.json')),
        'registered_stage_files':stages,'completed_stages':status['completed_stages'],'remaining':status['remaining_stages'],
        'graph':{'nodes':len(status['graph']['nodes']),'edges':len(status['graph']['edges']),'unresolved':status['graph']['unresolved'],
                 'unresolved_edges':status['graph']['unresolved_edges']},
        'active_plan':{'path':str(MODELS/'compute-current.json'),'sha256':digest((MODELS/'compute-current.json').read_bytes()),
                       'all_input_paths_clone_local':True,'inputs':local_inputs},
        'original_fresh_restore_evidence_unchanged':previous_files,'previous_strict_verdict':'fail','carried_from_prior_real_replay':inherited,
        'runner_code_sha256':code_hash,'model_source_hashes':{str(p):digest(p.read_bytes()) for p in code},
        'new_actual_model':{'base':old_model,'replayed':actual,'changed_fields':delta,'canonical_output_sha256':normalized(b),
                            'held_out_prediction_rows':len(b['result']['test_predictions']),'split_rows':{k:v['rows'] for k,v in b['result']['splits'].items()},
                            'baseline_brier':b['result']['baseline']['brier'],
                            'calibrated':{k:{x:v['calibrated_test'][x] for x in ['brier','detected_episodes','missed_episodes']} for k,v in b['result']['models'].items()}},
        'budget':{'before':read(LOGS/'compute-plan-before.stdout'),'fresh_session':expanded['sessions'][-1],
                  'after':read(LOGS/'compute-plan-after.stdout')},
        'ledger':{'frozen_sha256':digest(frozen(LEDGER)),'post_append_sha256':digest((LOCAL/'ledger-13.json').read_bytes()),
                  'frozen_rows':12,'expanded_rows':13,'stages_during':stages_mid['completed_stages'],
                  'stale_reasons':stages_mid['remaining_stages'],'restored_stages':final['completed_stages'],
                  'final_session_check_exit':3,'globally_complete':False},
        'environment':{'reuse':'Existing isolated venv from 1580 fresh-restore experiment, used solely as interpreter/dependencies. This round performs no network install.',
                       'python':(LOGS/'python-version.stdout').read_text().strip(),'node':(LOGS/'node-version.stdout').read_text().strip(),
                       'visible_cores':int((LOGS/'visible-cores.stdout').read_text()),'site_packages_inheritance':False,
                       'all_observed_distributions':len(frozen_env),'exact_project_requirements':38,'additional':{'cloudpickle':'3.1.3','pip':'25.0.1'},
                       'pip_freeze_sha256':digest((LOGS/'pip-freeze.stdout').read_bytes()),'doctor':doctor},
        'family':{'input_kind':'synthetic_example','recomputed_from_csv':counts,'node_checks':tests['checks'],'failures':tests['failures'],
                  'contract_periods':periods,'max_abs_error_yuan':max(n for r in contracts['comparisons'] for n in r['max_abs_error_cny'].values()),
                  'engine_migration':{'pairs':migration['matchedPolicyScenarioPairs'],'months':migration['observedMonthsCompared'],
                                      'compared_fields':migration['comparedMonthlyFields'],'differing_pairs':migration['differingPolicyScenarioPairs'],
                                      'winning_rules':migration['newWinners']},'unrounded_capture':full,'lossless_archive':pack},
        'registered_output_file_checks':restored}
    write(OUT/'verification.json',result)
    files=set()
    for rec in restored:
        files.update(Path(f) for f in rec['input_code_sha256'])
        files.update(Path(f) for f in rec['output'])
    files.update([JST/'NOTICE.md',JST/'data_manifest.json',JST/'experiment.json',JST/'panel.csv',JST/'JSTdatasetR6.dta',
                  MODELS/'compute-current.json',MODELS/'compute-portable-history.json',OUT/'replay_plan.json',model_dir/old_model['output'],
                  model_dir/actual['output'],FORMAL/'report.md',FORMAL/'scenarios.json',FORMAL/'judgments.json',FORMAL/'calculator.html'])
    files.update(code)
    files.update([Path("vendor/numpy-financial/LICENSE.txt"), Path("research/models/jst_example/NOTICE.md")])
    files.update(Path(p) for j in local_inputs for p in j['paths_and_sha256'])
    if (LOCAL/'initial-formal.json').exists():
        files.add(LOCAL/'initial-formal.json')
    files.update(LOCAL/n for n in ['commands.json','regenerated.json','runner.stdout','runner.stderr','ledger-12.json','ledger-13.json'])
    files.update(LOGS.glob('*'))
    index={}
    with ZipFile(OUT/'raw_evidence.zip','w',compression=ZIP_DEFLATED) as z:
        for p in sorted(files):
            archive=('audit/'+str(p.relative_to(LOCAL))) if p.is_relative_to(LOCAL) else ('repo/'+str(p))
            index[archive]=digest(p.read_bytes());z.write(p,archive)
        for n in ['engine.js','synthetic_household.json','scenarios.json']:
            contents=old_bytes(HOUSE/n); name='migration-source-1580/'+n
            z.writestr(name,contents);index[name]=digest(contents)
        z.writestr('sha256.json',json.dumps(index,indent=2)+'\n')
    with ZipFile(OUT/'raw_evidence.zip') as z:
        assert z.testzip() is None and all(digest(z.read(n))==v for n,v in index.items())
    print(json.dumps({'stage_file_checks':len(stages),'carried_verified':len(inherited),'new_method_runs':1,
                      'raw_archive_members_hashed':len(index),'regenerated':sum(len(r['output']) for r in restored),
                      'monthly_archive_sha256':pack['sha256'],'strict_portability':'pass'},indent=2))


if __name__=='__main__':
    main()
