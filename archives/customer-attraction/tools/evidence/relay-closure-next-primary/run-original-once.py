"""Run the unmodified independent kernel-review main exactly once in a new root."""
from pathlib import Path
import ast,hashlib,json,platform,shutil,subprocess,sys,time
E=Path(__file__).resolve().parent
items=json.loads((E/'source-manifest.json').read_text());src=next(r for r in items if r['path'].endswith('.py'));frozen=next(r for r in items if r['path'].endswith('optimal_exchange_review_audit.json'))
replay=E/'replay';replay.mkdir(exist_ok=False);root=replay/'source-root';root.mkdir();program=root/src['path'];program.parent.mkdir(parents=True);shutil.copyfile(E/'original'/src['path'],program)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
tree=ast.parse(program.read_text());imports=[n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)]+[a.name for n in ast.walk(tree)if isinstance(n,ast.Import)for a in n.names]
start=time.time();proc=subprocess.run([sys.executable,str(program)],cwd=root,capture_output=True)
(replay/'original.stdout.txt').write_bytes(proc.stdout);(replay/'original.stderr.txt').write_bytes(proc.stderr);report=program.with_name('optimal_exchange_review_audit.json')
state={'original_program_calls':1,'execution_count':1,'program':src['path'],'program_bytes':program.stat().st_size,'program_sha256':sha(program),'argv':[sys.executable,str(program)],'cwd':str(root),'python':sys.version,'executable':sys.executable,'optimize':sys.flags.optimize,'platform':platform.platform(),'imports':imports,'local_program_imports':[],'external_dependencies':[],'exit_code':proc.returncode,'duration_seconds':time.time()-start,'stdout_bytes':len(proc.stdout),'stdout_sha256':sha(replay/'original.stdout.txt'),'stderr_bytes':len(proc.stderr),'stderr_sha256':sha(replay/'original.stderr.txt'),'output_created':report.exists(),'exclusive_output':'original guarded main open x to source-adjacent filename','path_difference':'byte-identical source mirrored at original repo-relative path in independent external source-root, not original frozen filesystem root'}
if report.exists():state.update({'new_report_bytes':report.stat().st_size,'new_report_sha256':sha(report),'equals_frozen_report_bytes':report.read_bytes()==(E/'original'/frozen['path']).read_bytes(),'stdout_equals_report_bytes':proc.stdout==report.read_bytes()})
(replay/'execution-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');print(json.dumps(state,ensure_ascii=False));assert proc.returncode==0,'Original failure preserved; no automatic retry'
