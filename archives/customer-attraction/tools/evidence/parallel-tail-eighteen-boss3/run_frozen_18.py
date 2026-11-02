"""Replay only the 18 frozen parameter records; retain three full certificates.

The frozen original main is NOT run: it only specifies the first six cases.
This driver calls original trial once per supplied record with cert=True, checks
all old fields exactly, and stores complete strategies only on successful paths.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, platform, runpy, subprocess, sys, time

def fingerprint(p):
    return {'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def worker(repo, base):
    package=repo/'archives/customer-attraction/tools/evidence/exact-spe'
    sys.path.insert(0,str(package))
    import customer_attraction
    assert Path(customer_attraction.__file__).resolve()==(package/'customer_attraction/__init__.py').resolve()
    source=base/'original/parallel_attack.py'
    ns=runpy.run_path(str(source),run_name='frozen_parallel_attack_functions')
    tags=('parallel_attack_results','parallel_attack_support_results','parallel_attack_repaired_r2','support_targeted_diagnostic')
    reports={tag:json.loads((base/'original'/(tag+'.json')).read_text())for tag in tags}
    assert [len(reports[t])for t in tags]==[6,4,3,5]
    outdir=base/'replay';outdir.mkdir(exist_ok=True)
    records=[];successes=[]
    for tag in tags:
        for index,old in enumerate(reports[tag]):
            started=time.monotonic()
            fresh=ns['trial'](**old['params'],cert=True)
            cert=fresh.pop('certificate',None)
            assert fresh==old,(tag,index,{k:(old.get(k),fresh.get(k))for k in set(old)|set(fresh)if old.get(k)!=fresh.get(k)})
            case={'source_report':tag+'.json','source_index':index,'params':old['params'],
                  'all_frozen_fields_identical':True,'all_frozen_fields':list(old),
                  'fresh_record':fresh,'elapsed_seconds':time.monotonic()-started}
            if cert is not None:
                cfile='certificate-'+tag+'-'+str(index)+'.json'
                (outdir/cfile).write_text(json.dumps({'instance':fresh['instance'],'certificate':cert},indent=2)+'\n')
                case['new_full_certificate']=cfile
                case['certificate_fingerprint']=fingerprint(outdir/cfile)
                successes.append({'report':tag+'.json','index':index,'params':old['params'],'certificate':cfile,'verification':fresh['verification']})
            records.append(case)
            print(json.dumps({'case':len(records),'report':tag,'index':index,'params':old['params'],
                              'matched':True,'path_reachable':fresh['path_reachable'],
                              'elapsed_seconds':case['elapsed_seconds']},ensure_ascii=False),flush=True)
    assert len(records)==18 and len(successes)==3
    result={'scope':'18 supplied finite records only, original trial definition replayed once per record; no parameter search',
            'records':records,'successes':successes,'all18_fields_match':True,
            'target_count_reachable':3,'target_count_unreachable':15,
            'new_full_ordered_history_certificates':3,
            'source_main_runs':0,'original_trial_calls':18,
            'original_module_loads':1,'new_independent_solver_claimed':False,
            'python':platform.python_version(),
            'dependencies':{str(p.relative_to(repo)):fingerprint(p)for p in sorted((package/'customer_attraction').glob('*.py'))if p.name!='__main__.py'},
            'input_fingerprints':{str(p.relative_to(base)):fingerprint(p)for p in sorted((base/'original').glob('*'))}}
    (outdir/'all-eighteen-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'completed':18,'successful_full_certificates':3,'all_fields_match':True}),flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True,type=Path);ap.add_argument('--worker',action='store_true');a=ap.parse_args()
    base=Path(__file__).resolve().parent
    if a.worker:
        worker(a.repo.resolve(),base);return
    out=base/'replay';out.mkdir(exist_ok=True)
    cmd=[sys.executable,'-I',str(Path(__file__).resolve()),'--repo',str(a.repo.resolve()),'--worker']
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
    proc=subprocess.run(cmd,capture_output=True,text=True)
    (out/'stdout.txt').write_text(proc.stdout);(out/'stderr.txt').write_text(proc.stderr)
    event={'argv':cmd,'start_utc':utc,'elapsed_seconds':time.monotonic()-t,'returncode':proc.returncode,
           'worker_driver':fingerprint(Path(__file__)),
           'stdout':fingerprint(out/'stdout.txt'),'stderr':fingerprint(out/'stderr.txt'),
           'scope':'original main zero calls; original trial18; only18 supplied records; certificates generated only when true'}
    (out/'execution-record.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
    print(proc.stdout,end='');print(proc.stderr,end='',file=sys.stderr)
    if proc.returncode:raise SystemExit(proc.returncode)
    print(json.dumps(event,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
