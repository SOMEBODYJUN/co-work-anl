"""Materialize an isolated frozen split runtime and run one original verify CLI."""
from pathlib import Path
import hashlib,json,os,platform,subprocess,sys,time
import numpy,scipy

repo=Path('/workspace/scratch/c0ab78c47566/boss7-cleaner')
scratch=Path(__file__).resolve().parent
e=repo/'archives/customer-attraction/tools/evidence'
closure=e/'zz-threshold-closure-program'
dest=scratch/'runtime'
assert not dest.exists()
manifest=json.loads((closure/'source-manifest.json').read_text())
sources=[]
for s in manifest['default_runtime_sources']:
    sources.append({**s,'stored_path':str((closure/s['preserved_as']).resolve().relative_to(repo))})
prefix='research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/'
for stored,name in [('split-basic-graph-program/original/split_basic_graph.py','split_basic_graph.py'),('split-basic-graph-program/related/split_basic_exact.json','split_basic_exact.json'),('zz-threshold-closure-program/related/zz_split_exact.json','zz_split_exact.json')]:
    p=e/stored;raw=p.read_bytes()
    sources.append({'original_path':prefix+name,'stored_path':str(p.relative_to(repo)),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
assert len({s['original_path'] for s in sources})==len(sources)
dest.mkdir();(dest/'work.py').write_text('# Inert root marker, never executed.\n')
for s in sources:
    data=(repo/s['stored_path']).read_bytes()
    assert len(data)==s['bytes'] and hashlib.sha256(data).hexdigest()==s['sha256']
    p=dest/s['original_path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
out=scratch/'rerun';out.mkdir()
(out/'runtime-manifest.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
argv=[sys.executable,'-B',str(dest/(prefix+'zz_threshold_closure.py')),'--split','--verify']
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
start=time.perf_counter();run=subprocess.run(argv,cwd=dest,env=env,capture_output=True);elapsed=time.perf_counter()-start
(out/'stdout.txt').write_bytes(run.stdout);(out/'stderr.txt').write_bytes(run.stderr)
unchanged=all(hashlib.sha256((dest/s['original_path']).read_bytes()).hexdigest()==s['sha256'] for s in sources)
report={'argv':argv,'cwd':str(dest),'python':sys.version,'numpy':numpy.__version__,'scipy':scipy.__version__,'assertions_enabled':True,'PYTHONOPTIMIZE_removed':True,'elapsed_seconds':elapsed,'exit_code':run.returncode,'original_main_runs':1,'LP_calls':0,'runpy_or_trace_or_profile':False,'original_functions_modified':False,'available_frozen_files':len(sources),'available_manifest_not_dynamic_load_trace':True,'all_frozen_files_unchanged':unchanged,'stdout_sha256':hashlib.sha256(run.stdout).hexdigest(),'stderr_bytes':len(run.stderr)}
(out/'execution.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2));print(run.stdout.decode());print(run.stderr.decode())
assert run.returncode==0 and unchanged
