from pathlib import Path
import hashlib,json,os,subprocess,sys,time

S=Path(__file__).resolve().parents[4];E=S/'archives/customer-attraction/tools/evidence/full-tree-milp-candidate-audits-primary'
tree=E/'replay-tree';sub=Path('research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_boss')
out=E/'replay-milp';out.mkdir(parents=True,exist_ok=True)
if (out/'started.json').exists():raise SystemExit('Original MILP main already started; no repeat')
target=tree/sub/'full_tree_milp.py';output=out/'new_m3p4i0.json'
cmd=[sys.executable,str(target),'--out',str(output)]
meta={'command':cmd,'cwd':str(tree),'original_main_runs_this_batch':1,
 'input_contract':'original defaults players3/topics4/player0/objectivegap/seconds30; root-in and root-out portfolios',
 'original_source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'expected_MILP_calls':2,
 'fixed_cone_LP_calls':0,'external_input_files':0,'started_unix':time.time()}
(out/'started.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
t=time.monotonic()
try:
 r=subprocess.run(cmd,cwd=tree,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'},capture_output=True,timeout=90)
 stdout,stderr=r.stdout,r.stderr;meta.update(returncode=r.returncode,timed_out=False)
except subprocess.TimeoutExpired as ex:
 stdout,stderr=ex.stdout or b'',ex.stderr or b'';meta.update(returncode=None,timed_out=True)
meta.update(wall_seconds=time.monotonic()-t,stdout_bytes=len(stdout),stderr_bytes=len(stderr))
(out/'stdout.txt').write_bytes(stdout);(out/'stderr.txt').write_bytes(stderr)
if output.exists():meta.update(output_bytes=output.stat().st_size,output_sha256=hashlib.sha256(output.read_bytes()).hexdigest())
(out/'execution.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(meta,ensure_ascii=False));print(stdout.decode())
