"""Run the untouched primary stdlib main exactly once in its copied tree."""
from pathlib import Path
import hashlib,json,os,platform,subprocess,sys,time
S=Path(__file__).resolve().parents[4]
E=S/'archives/customer-attraction/tools/evidence/terminal-clone-primary-and-review'
sub=Path('research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3')
tree=E/'replay-tree';target=tree/sub/'next_counterexample/terminal_clone_refutation_review.py'
source=tree/sub/'next_boss/terminal_exact_audit.json'
report=target.with_suffix('.json');out=E/'replay-original-review';out.mkdir(parents=True,exist_ok=True)
assert not (out/'started.json').exists() and not report.exists(),'Original main already started/output exists; no rerun'
meta={'command':[sys.executable,'-B',str(target)],'cwd':str(tree),'python':platform.python_version(),
 'original_main_runs_this_batch':1,'original_main_runs_in_CF_batch':0,'solver_calls':0,
 'source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
 'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'input_report_record_used':'/0/records/0',
 'started_unix':time.time()}
(out/'started.json').write_text(json.dumps(meta,indent=2)+'\n');t=time.monotonic()
r=subprocess.run(meta['command'],cwd=tree,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
meta.update(returncode=r.returncode,wall_seconds=time.monotonic()-t,stdout_bytes=len(r.stdout),stderr_bytes=len(r.stderr))
(out/'stdout.txt').write_bytes(r.stdout);(out/'stderr.txt').write_bytes(r.stderr)
if report.exists():
 b=report.read_bytes();(out/'terminal_clone_refutation_review.json').write_bytes(b)
 old=(E/'original'/sub/'next_counterexample/terminal_clone_refutation_review.json').read_bytes()
 a=json.loads(old);n=json.loads(b);keys=sorted(k for k in set(a)|set(n) if a.get(k)!=n.get(k))
 meta.update(output_bytes=len(b),output_sha256=hashlib.sha256(b).hexdigest(),
     frozen_sha256=hashlib.sha256(old).hexdigest(),byte_identical=b==old,
     differing_top_level_keys=keys,all_math_fields_equal=keys==['source'])
(out/'execution.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(meta,ensure_ascii=False));raise SystemExit(r.returncode)
