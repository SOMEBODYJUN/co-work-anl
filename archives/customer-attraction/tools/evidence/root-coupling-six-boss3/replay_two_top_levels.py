#!/usr/bin/env python3
"""Exactly two unmodified original top levels in fresh mirrored layout; 0 LP."""
from pathlib import Path
import hashlib,json,os,platform,subprocess,sys,time
P=Path(__file__).resolve().parent;R=Path('/workspace/scratch/9559bf893d22/boss3_root_coupling_runtime')
assert not R.exists();R.mkdir()
N=R/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_credible';N.mkdir(parents=True)
for f in (P/'original').iterdir():(N/f.name).write_bytes(f.read_bytes())
for name in ('root_menu_completion_exact.json','enhanced_2396_exact_obstruction.json','offdiagonal_probe.py'):(N/name).write_bytes((P/'related'/name).read_bytes())
p=R/'evidence/certificates/customer_attraction/five_player_indexed_bound.json';p.parent.mkdir(parents=True);p.write_bytes((P/'related'/p.name).read_bytes())
inputs=[f for f in R.rglob('*') if f.is_file() and f.name not in ('independent_root_lift.json','root_coupling_obstruction_exact.json')]
before={str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs}
results=[]
for stem,out in [('check_independent_root_menus','independent_root_lift.json'),('audit_root_coupling_obstruction','root_coupling_obstruction_exact.json')]:
 start=time.perf_counter();r=subprocess.run([sys.executable,str(N/(stem+'.py'))],cwd=R,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True);elapsed=time.perf_counter()-start
 (P/(stem+'.stdout')).write_bytes(r.stdout);(P/(stem+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0,(stem,r.returncode,r.stderr)
 data=(N/out).read_bytes();(P/('current-'+out)).write_bytes(data)
 assert data==(P/'original'/out).read_bytes(),out
 results.append({'original_script':stem+'.py','command':[sys.executable,str(N/(stem+'.py'))],'cwd':str(R),'returncode':r.returncode,'wall_seconds_including_imports':elapsed,'stdout_file':stem+'.stdout','stderr_file':stem+'.stderr','output':'current-'+out,'output_bytes':len(data),'output_sha256':hashlib.sha256(data).hexdigest(),'byte_equal_frozen':True})
after={str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs};assert before==after
j={'kind':'two original top-level replays only; no float coupling solver or prior recovery','python':platform.python_version(),'assertions_enabled':__debug__,'wrapper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'original_top_level_runs':2,'original_LP_calls':0,'root92_recovery_runs':0,'full53_recovery_runs':0,'full1326_matrix_audits':0,'random_samples':0,'input_files':before,'inputs_unchanged':True,'runs':results}
(P/'two-original-top-level-events.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');print(json.dumps(j,ensure_ascii=False))
