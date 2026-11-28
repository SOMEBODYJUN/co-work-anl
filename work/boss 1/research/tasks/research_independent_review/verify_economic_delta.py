"""Audit the portable experiment from a new relative directory, leaving the main ledger untouched."""
import csv
import hashlib
import json
import math
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[2]
ROOT = HERE.parents[4]
PYTHON = ROOT/'.venv-methods/bin/python'
OLD = WORK/'research/models/jst_audited_20261127'
NEW = WORK/'research/models/jst_portable_20261127'
RUNS = WORK/'compute/outputs'
OLD_OUT = RUNS/'historical-warning-audit-v2-de6d97643789.json'
NEW_OUT = RUNS/'historical-warning-portable-v3-933f425819ff.json'
OLD_REVIEW = 'f9387a47cfd3ad6151516e1daa60828ad6855edf09ff33f9c0f99d1e94fe94a3'
TIMES = ['/result/executed_at','/result/models/hist_gradient_boosting/elapsed_seconds','/result/models/logit/elapsed_seconds']


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(old, new, path=''):
    if type(old) != type(new):
        return [path]
    if isinstance(old, dict):
        assert old.keys() == new.keys(), path
        return [p for k in old for p in differences(old[k],new[k],path+'/'+k)]
    if isinstance(old, list):
        assert len(old) == len(new), path
        return [p for i,(a,b) in enumerate(zip(old,new)) for p in differences(a,b,path+'/'+str(i))]
    return [] if old == new else [path]


def scratch_replay():
    with tempfile.TemporaryDirectory(prefix='panel-portability-', dir=HERE) as tmp:
        rel = Path(tmp).relative_to(ROOT)
        prepared = rel/'panel'
        target = rel/'replay.json'
        cmd = [str(PYTHON),'tools/prepare_jst_example.py','--source',str((NEW/'JSTdatasetR6.dta').relative_to(ROOT)),'--output',str(prepared)]
        result = subprocess.run(cmd,cwd=ROOT,check=True,capture_output=True,text=True)
        actual_files = ROOT/prepared
        assert all(sha(actual_files/f)==sha(NEW/f) for f in ['JSTdatasetR6.dta','panel.csv','data_manifest.json'])
        spec = read(actual_files/'experiment.json')
        assert Path(spec['csv']) == prepared/'panel.csv' and (ROOT/spec['csv']).resolve().is_relative_to(HERE)
        assert differences(spec,read(NEW/'experiment.json')) == ['/csv']
        method = [str(PYTHON),'work.py','methods','run','--name','early-warning','--input',str(prepared/'experiment.json'),'--output',str(target)]
        p = subprocess.run(method,cwd=ROOT,check=True,capture_output=True,text=True,env={**os.environ,'OPENBLAS_NUM_THREADS':'2','OMP_NUM_THREADS':'2','MKL_NUM_THREADS':'2'})
        actual = read(ROOT/target)
        paths=sorted(differences(read(NEW_OUT),actual))
        assert paths == TIMES, paths
        return {'input_path_was_relative':True,'own_temporary_csv_resolved_in_reviewer_directory':True,
                'prepare_exit_code':result.returncode,'prepare_result':json.loads(result.stdout),
                'temporary_regenerated_dta_sha256':sha(actual_files/'JSTdatasetR6.dta'),'temporary_regenerated_panel_sha256':sha(actual_files/'panel.csv'),
                'temporary_regenerated_manifest_sha256':sha(actual_files/'data_manifest.json'),'method_exit_code':p.returncode,
                'execution_utc':actual['result']['executed_at'],'reviewer_method_raw_output_sha256':sha(ROOT/target),
                'output_delta_vs_portable':paths,'commands':['.venv-methods/bin/python tools/prepare_jst_example.py --source work/boss 1/research/models/jst_portable_20261127/JSTdatasetR6.dta --output <new repository-relative directory>/panel',
                    '.venv-methods/bin/python work.py methods run --name early-warning --input <new directory>/panel/experiment.json --output <new directory>/replay.json'],
                'main_compute_ledger_modified_by_reviewer':False}


def audit_splits(spec,result):
    with (NEW/'panel.csv').open() as f:
        panel = list(csv.DictReader(f))
    assert len(panel) == 1703
    s = spec['split']
    parts = {
        'train':[d for d in panel if d['as_of']<=s['train_end'] and d['horizon_end']<s['calibration_start']],
        'calibration':[d for d in panel if s['calibration_start']<=d['as_of']<=s['calibration_end'] and d['horizon_end']<s['test_start']],
        'test':[d for d in panel if s['test_start']<=d['as_of']<=s['test_end'] and d['horizon_end']<=spec['label_observed_through']]}
    out = {}
    for key,rows in parts.items():
        row=dict(rows=len(rows),as_of_min=min(r['as_of'] for r in rows),as_of_max=max(r['as_of'] for r in rows),
                 last_label_maturity=max(r['horizon_end'] for r in rows),distinct_country_episodes=len({r['event_id'] for r in rows if r['event']=='1'}))
        assert all(result['splits'][key][k]==v for k,v in row.items())
        assert all(int(r['horizon_end'][:4])-int(r['as_of'][:4])==3 for r in rows)
        out[key]=row
    assert [r['as_of_max'][:4] for r in out.values()] == ['1981','1999','2016']
    assert [r['last_label_maturity'][:4] for r in out.values()] == ['1984','2002','2019']
    return out


def audit_inputs(plans,runs):
    answer=[]
    for job in plans:
        path=Path(job['input'])
        assert not path.is_absolute() and (ROOT/path).resolve().is_relative_to(ROOT)
        meta=read(ROOT/path)
        entry={'id':job['id'],'spec':str(path),'spec_sha256':sha(ROOT/path)}
        run=runs[job['id']]
        assert run['input_sha256']==entry['spec_sha256'] and run['status']=='complete'
        fields=[run['code_sha256'],run['environment_sha256'],job['method'],entry['spec_sha256']]
        if 'csv' in meta:
            csv_path=Path(meta['csv'])
            assert not csv_path.is_absolute() and (ROOT/csv_path).resolve().is_relative_to(ROOT)
            entry.update(csv=str(csv_path),csv_sha256=sha(ROOT/csv_path))
            fields.append(entry['csv_sha256'])
        assert hashlib.sha256('|'.join(fields).encode()).hexdigest()==run['fingerprint']
        result_file=WORK/'compute'/run['output']
        assert sha(result_file)==run['output_sha256']
        entry['input_kind']=read(result_file)['result']['input_kind']
        entry['output_sha256']=sha(result_file)
        answer.append(entry)
    return answer


if __name__ == '__main__':
    assert sha(HERE/'economic_checks.json')==OLD_REVIEW
    old=read(OLD/'experiment.json');new=read(NEW/'experiment.json')
    assert differences(old,new)==['/csv'] and Path(old['csv']).is_absolute() and not Path(new['csv']).is_absolute()
    assert (ROOT/new['csv']).resolve()==(NEW/'panel.csv').resolve()
    assert all(sha(OLD/f)==sha(NEW/f) for f in ['panel.csv','JSTdatasetR6.dta','NOTICE.md'])
    assert differences(read(OLD/'data_manifest.json'),read(NEW/'data_manifest.json'))==['/preparation_script_sha256']
    oldout=read(OLD_OUT);newout=read(NEW_OUT)
    assert sorted(differences(oldout,newout))==TIMES
    assert newout['result']['data_sha256']==sha(NEW/'panel.csv')
    assert sha(ROOT/'tools/prepare_jst_example.py')==read(NEW/'data_manifest.json')['preparation_script_sha256']
    pinned=read(HERE/'economic_checks.json');ledger=read(WORK/'compute/ledger.json')
    runs={r['id']:r for r in ledger['runs']};plan=read(WORK/'research/models/compute-current.json')['jobs']
    assert len(runs)==len(ledger['runs'])==12 and len(plan)==len({j['id'] for j in plan})==11
    assert set(runs)-{j['id'] for j in plan}=={'historical-warning-audit-v2'}
    assert runs['historical-warning-audit-v2']['output_sha256']==sha(OLD_OUT)
    assert runs['historical-warning-portable-v3']['output_sha256']==sha(NEW_OUT)
    compat=read(HERE/'independent_models.json')['corrected_sensitivity']
    scores={}
    for name,model in newout['result']['models'].items():
        for stage,sec in [('raw','raw_test'),('calibrated','calibrated_test')]:
            actual,own=model[sec],compat[name]['metrics'][stage]
            assert math.isclose(actual['brier'],own['brier'],abs_tol=5e-15) and math.isclose(actual['roc_auc'],own['auc'],abs_tol=5e-15)
            assert actual['detected_episodes']==len(own['detected']) and actual['missed_episodes']==len(own['missed'])
            score_field='raw_score' if stage=='raw' else 'score'
            threshold=model['raw_alarm_threshold' if stage=='raw' else 'alarm_threshold']
            pred=[p for p in newout['result']['test_predictions'] if p['model']==name]
            eventset={p['event_id'] for p in pred if p['event']==1}
            hit={p['event_id'] for p in pred if p['event']==1 and p[score_field]>threshold}
            assert hit==set(own['detected']) and eventset-hit==set(own['missed'])
            assert sum(p['event']==0 and p[score_field]>threshold for p in pred)==own['false_alarms']
            scores[name+'_'+stage]={'brier':actual['brier'],'auc':actual['roc_auc'],'detected_episodes':len(own['detected']),
                                    'missed_episodes':len(own['missed']),'false_alarms':own['false_alarms'],'negative_periods':own['negatives']}
    lineage=read(WORK/'research/source_lineage.json');state=read(WORK/'research_state.json')
    groups=[r for r in lineage['events'] if 'PF029' in r['evidence_ids'] or 'QA001' in r['evidence_ids']]
    assert len(groups)==2 and state['sources']['QA001']['corroborates']=='PF029' and not state['sources']['QA001']['targets']
    assert len(state['sources'])==lineage['evidence_record_count']==157 and len(lineage['events'])==105 and len(lineage['publications'])==113
    support= ['formal/report.md','formal/judgments.json','formal/scenarios.json','compute/ledger.json','research/graph_current.json','research/model_results.md',
              'research/method_runs.md','research/challenges.md','research/tasks/release_audit/pre_repair_cases.json','research/tasks/release_audit/pre_repair_results.json','research/tasks/fresh_restore/receipt.json','research/historical_model_correction.md','research/models/model_decisions.md','research/source_lineage.json','research/models/compute-current.json',
              'research/models/compute-portable-history.json','research/models/compute-audited-history.json','research/receipts/portable_input_repair.json',
              'research/receipts/portable_experiment_replay.json','research/receipts/current_plan_portability.json','research/RESUME.md','research/data/audit_crosscheck_record.json']
    for f in ['formal/judgments.json','formal/scenarios.json','research/graph_current.json','research/model_results.md','research/models/model_decisions.md','research/source_lineage.json']:
        assert sha(WORK/f)==pinned['file_sha256'][f], f
    for p in (OLD,NEW):
        support.extend(str((p/f).relative_to(WORK)) for f in ['experiment.json','data_manifest.json','JSTdatasetR6.dta','panel.csv'])
    support.extend(str(p.relative_to(WORK)) for p in [OLD_OUT,NEW_OUT,HERE/'economic_checks.json',HERE/'economics_review.md',HERE/'economic_delta.md',Path(__file__)])
    out={'schema':'independent-economic-delta.v1','author':'boss 1','reviewer':'/root/research_independent_review','cycle':1,'as_of':'2026-11-27 America/Los_Angeles',
         'scope':'经济五项的路径、时间字段、来源分组及报告增量；不签家庭HTML、数值实现、离线浏览器、最终恢复和正式发布。',
         'supersedes_in_part':{'previous_economic_receipt_sha256':OLD_REVIEW,'corrected_statement':'此前独立正文“最后信息年分别1984、2002、2019”表述错误；这三年是最后标签成熟年。信息年应为1981、1999、2016。原签名原文保留。'},
         'split_recomputed_from_1703_csv_rows':audit_splits(new,newout['result']),'numerical_uses':scores,
         'current_plan_11_specs':audit_inputs(plan,runs),'principal_ledger_actual_runs':len(runs),'principal_ledger_sessions':len(ledger['sessions']),
         'runner_reported_core_hours':sum(r['estimated_core_hours'] for r in ledger['sessions']),'two_outputs_differ_only_in':TIMES,
         'portable_input_changed_fields':differences(old,new),'portable_manifest_changed_fields':differences(read(OLD/'data_manifest.json'),read(NEW/'data_manifest.json')),
         'origin_source_groups':{'source_records':157,'publication_locator_groups':113,'event_or_publication_groups':105,'case':'PF029和QA001两稿同一众邦接管事实，只按一案。105是混合索引组数，不是独立危机或宏观观察数。','publication_index_rows':groups},
         'actual_separate_reviewer_replay':scratch_replay(),'reviewed_at_utc':datetime.now(timezone.utc).isoformat(),
         'reviewed_worktree_head_at_read':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
         'current_file_sha256':{f:sha(WORK/f) for f in support},'repository_prepare_sha256':sha(ROOT/'tools/prepare_jst_example.py'),
         'economic_verdicts':{k:'pass' for k in ['sources','frameworks','models','hyperedges','judgments']},'final_release_verdict':'outside_delta_scope'}
    (HERE/'economic_delta.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(sha(HERE/'economic_delta.json'),sha(HERE/'economic_delta.md'),out['split_recomputed_from_1703_csv_rows'])
