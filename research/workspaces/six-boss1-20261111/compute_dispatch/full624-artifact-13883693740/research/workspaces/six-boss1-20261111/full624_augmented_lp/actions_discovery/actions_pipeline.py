"""Prepared full624 Actions job; one discovery followed by exact verification.

The default is a dry run. --execute requires an actual GitHub Actions runner.
No dispatch, git operation, token handling or external mutation occurs here.
All stage outputs are retained, including failed rational recoveries.
"""
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import argparse,json,os,platform,shutil,subprocess,sys,time

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
def sha(p):return sha256(p.read_bytes()).hexdigest()
parser=argparse.ArgumentParser()
parser.add_argument('--output',default='actions_run')
parser.add_argument('--method',choices=['highs-ds','highs-ipm'],default='highs-ds')
parser.add_argument('--time-limit',type=float,default=1800)
parser.add_argument('--execute',action='store_true')
args=parser.parse_args()
assert 170<args.time_limit<=7200
out=(HERE/args.output).resolve()
assert out.is_relative_to(HERE) and out!=HERE
manifest=json.loads((HERE/'inputs_manifest.json').read_text())
assembly=json.loads((HERE/'assembly_verification.json').read_text())
assert sha(HERE/'exact_matrix.json.gz')==manifest['exact_matrix_sha256']==assembly['matrix_sha256']
assert sha(HERE/'floating_problem.npz')==assembly['floating_problem_sha256']
assert assembly['rows']==20910 and assembly['columns']==20585
plan={'status':'PREPARED_NOT_EXECUTED' if not args.execute else 'EXECUTING',
    'command':[sys.executable,*sys.argv],'cwd':str(REPO),'output':str(out),
    'method':args.method,'time_limit':args.time_limit,'optimizer_calls_planned':1,
    'matrix_sha256':sha(HERE/'exact_matrix.json.gz'),'floating_problem_sha256':sha(HERE/'floating_problem.npz'),
    'scope':'All20910 symbolic rows and20585 nonnegative columns. Exact old dual zero-extension; exact new primal and, only if needed, dual.'}
print(json.dumps(plan,ensure_ascii=False,indent=2),flush=True)
if not args.execute:sys.exit(0)
assert os.environ.get('GITHUB_ACTIONS')=='true','No local optimization rerun is authorized by this prepared continuation.'
assert not out.exists(),str(out)
out.mkdir()
copy_names=('exact_matrix.json.gz','floating_problem.npz','epigraph_structure.json','zz_envelope_structure.json',
    'inherited_dual_lower_bound.json','inputs_manifest.json','assembly_verification.json',
    'assemble_solve.py','recover.py','verify_certificates.py','actions_stage.py','actions_pipeline.py')
for name in copy_names:shutil.copyfile(HERE/name,out/name)
(out/'actions_input_manifest.json').write_text(json.dumps({**plan,'input_sha256':{name:sha(out/name) for name in copy_names},
    'python':platform.python_version(),'started_utc':datetime.now(timezone.utc).isoformat()},ensure_ascii=False,indent=2)+'\n')
receipts=[]
def stage(name,argv,source):
    stdout=out/(name+'_stdout.txt');stderr=out/(name+'_stderr.txt')
    snapshots=out/'executed_sources';snapshots.mkdir(exist_ok=True)
    snapshot=snapshots/(source.stem+'_'+sha(source)+source.suffix)
    if not snapshot.exists():snapshot.write_bytes(source.read_bytes())
    record={'argv':argv,'cwd':str(REPO),'python':platform.python_version(),
        'source_sha256':sha(source),'source_snapshot':str(snapshot.relative_to(out)),
        'driver_sha256':sha(Path(__file__)),'started_utc':datetime.now(timezone.utc).isoformat()}
    started=time.monotonic()
    with stdout.open('w') as f,stderr.open('w') as g:
        result=subprocess.run(argv,cwd=REPO,stdout=f,stderr=g,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    record.update(exit_code=result.returncode,status='SUCCESS' if result.returncode==0 else 'FAILED',
        elapsed_seconds=time.monotonic()-started,ended_utc=datetime.now(timezone.utc).isoformat(),
        stdout_sha256=sha(stdout),stderr_sha256=sha(stderr))
    (out/('execution_'+name+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    receipts.append(record)
    print(json.dumps({'stage':name,**record},ensure_ascii=False),flush=True)
    return result.returncode
def run_recovery(attempt):
    return stage('recover_'+attempt,[sys.executable,'-B',str(HERE/'actions_stage.py'),attempt,str(out)],HERE/'actions_stage.py')

code=stage('solve',[sys.executable,'-B',str(HERE/'actions_stage.py'),'solve',str(out),args.method,str(args.time_limit)],HERE/'actions_stage.py')
if code:sys.exit(code)
numerical=json.loads((out/'numerical_result.json').read_text())
from fractions import Fraction
old=Fraction(json.loads((out/'inherited_dual_lower_bound.json').read_text())['normalization_multiplier'])
code=run_recovery('sameW') if abs(numerical['W_float']-float(old))<1e-8 else 1
if code:
    assert not (out/'augmented_lp_exact.json').exists(),'Partial result needs manual review before another recovery.'
    code=run_recovery('freeW')
if code:sys.exit(code)
if not (out/'exact_dual_certificate.json').exists():
    code=run_recovery('dual')
if code:sys.exit(code)
code=stage('verify',[sys.executable,'-B',str(HERE/'verify_certificates.py'),str(out)],HERE/'verify_certificates.py')
if code:sys.exit(code)
summary=json.loads((out/'certificate_verification.json').read_text())
(out/'actions_completed.json').write_text(json.dumps({'status':'EXACT_VERIFIED','verification':summary,
    'receipts':receipts,'finished_utc':datetime.now(timezone.utc).isoformat()},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'EXACT_VERIFIED','W':summary['W'],'same_optimum':summary['same_optimum'],
    'exact_increase':summary['exact_increase'],'output':str(out)},ensure_ascii=False),flush=True)
