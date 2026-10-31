from pathlib import Path
import hashlib,json,os,platform,subprocess,sys,time
import numpy,scipy

S=Path(__file__).resolve().parents[4]
E=S/'archives/customer-attraction/tools/evidence/markov-welfare-policy-cones-primary'
SUB=Path('research/workspaces/customer-attraction/R-e6796fb9db2a4ae9994cee93ac9bd152/independent')
name=sys.argv[1]
cfg={'welfare':('markov_welfare_gap.py',['--output','new_markov_gap.json'],180,
 'default players3/topics4/samples20000/seed71/max-policies100000; numpy default_rng, integer weights0..4 masked by per-sample uniform(.2,1)'),
 'cone':('policy_cone_search.py',['--output','new_policy_cone.json'],180,
 'default players5/topics7/seed133/restarts30/steps10; source-generated lognormal/sparsity/noise and support choices; 300 planned LP steps unless failure breaks each restart')}
file,args,timeout,input_note=cfg[name]
out=E/f'replay-{name}';out.mkdir(parents=True,exist_ok=True)
if (out/'started.json').exists():raise SystemExit('Already started; no duplicate original run')
tree=E/f'replay-{name}-tree';src=tree/SUB/file;src.parent.mkdir(parents=True,exist_ok=True)
data=(E/'original'/SUB/file).read_bytes();src.write_bytes(data)
cmd=[sys.executable,str(src),*args]
meta={'command':cmd,'cwd':str(tree),'original_entry_runs_this_batch':1,
 'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,
 'source_sha256':hashlib.sha256(data).hexdigest(),'external_code_dependencies':0,'external_input_files':0,
 'runtime_dependencies':'numpy for welfare; numpy and scipy.optimize.linprog for cone; standard library otherwise',
 'input_contract':input_note,'timeout_seconds':timeout,'started_unix':time.time(),
 'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}}
(out/'started.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
t=time.monotonic()
try:
 q=subprocess.run(cmd,cwd=tree,env={**os.environ,**meta['environment_overrides']},capture_output=True,timeout=timeout)
 stdout,stderr=q.stdout,q.stderr;meta.update(returncode=q.returncode,timed_out=False)
except subprocess.TimeoutExpired as ex:
 stdout,stderr=ex.stdout or b'',ex.stderr or b'';meta.update(returncode=None,timed_out=True)
meta.update(wall_seconds=time.monotonic()-t,stdout_bytes=len(stdout),stderr_bytes=len(stderr),source_unchanged=src.read_bytes()==data)
(out/'stdout.txt').write_bytes(stdout);(out/'stderr.txt').write_bytes(stderr)
output=tree/args[-1]
if output.exists():
 b=output.read_bytes();(out/output.name).write_bytes(b)
 meta.update(output_file=output.name,output_bytes=len(b),output_sha256=hashlib.sha256(b).hexdigest())
else:meta.update(output_file=None,output_note='original creates a report only on improvement/counterexample; absence is not a frozen-output mismatch')
(out/'execution.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(meta,ensure_ascii=False));print(stdout.decode())
