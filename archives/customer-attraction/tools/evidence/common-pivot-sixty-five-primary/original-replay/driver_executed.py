from pathlib import Path
import subprocess,time,json,hashlib,sys,platform,os
BASE=Path(__file__).parent
EV=BASE/'staging/archives/customer-attraction/tools/evidence/common-pivot-sixty-five-primary'
RUNTIME=BASE/'runtime'
ENTRY=RUNTIME/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/round3_indexed/reopt_common_pivot.py'
OUT=EV/'original-replay';OUT.mkdir()
argv=[sys.executable,str(ENTRY)]
t0=time.perf_counter();run=subprocess.run(argv,cwd=RUNTIME,capture_output=True)
(OUT/'stdout.txt').write_bytes(run.stdout);(OUT/'stderr.txt').write_bytes(run.stderr)
generated=ENTRY.with_suffix('.json');frozen=EV/'original/reopt_common_pivot.json'
import scipy,numpy
report={'event':'new-isolated-original-entry-execution','argv':argv,'cwd':str(RUNTIME),'elapsed_seconds':time.perf_counter()-t0,'exit_code':run.returncode,'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,'assertions_enabled':__debug__,'entry_sha256':hashlib.sha256(ENTRY.read_bytes()).hexdigest(),'stdout_sha256':hashlib.sha256(run.stdout).hexdigest(),'stderr_bytes':len(run.stderr),'entry_calls':1,'frozen_unchanged':hashlib.sha256(frozen.read_bytes()).hexdigest()=='d79cc6c3d6d52191c583b5aabebdb96ffbeed4653c65064c7a00a77026e7539d'}
if generated.exists():
 data=generated.read_bytes();(OUT/'reopt_common_pivot.json').write_bytes(data)
 a=json.loads(data);b=json.loads(frozen.read_bytes())
 report.update({'output_sha256':hashlib.sha256(data).hexdigest(),'byte_equal_frozen':data==frozen.read_bytes(),'full_fields_equal':a==b,'objective':a['objective'],'dual_beta':a['dual_beta'],'changed_fields':[k for k in b if a.get(k)!=b[k]],'max_point_difference':max(abs(x-y) for x,y in zip(a['point'],b['point'])),'max_lambda_difference':max(abs(x-y) for x,y in zip(a['dual_lambda'],b['dual_lambda']))})
(OUT/'event.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert run.returncode==0 and report['frozen_unchanged']
