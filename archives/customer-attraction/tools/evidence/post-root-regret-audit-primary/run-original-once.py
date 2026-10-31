"""Two unmodified original entries, each once in its own new source root."""
from pathlib import Path
import ast,hashlib,json,platform,shutil,subprocess,sys,time
E=Path(__file__).resolve().parent
primary=json.loads((E/'source-manifest.json').read_text());deps=json.loads((E/'dependency-manifest.json').read_text())
by={Path(r['path']).name:r for r in primary}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
runs=[]
for case,name,output in [('exchange','audit_exchange_potential_credit.py','exchange_potential_credit_audit.json'),('insertion','audit_owner_insertion_identity.py','owner_insertion_identity_audit.json')]:
 root=E/'replay'/case/'source-root';root.mkdir(parents=True,exist_ok=False)
 program=root/by[name]['path'];program.parent.mkdir(parents=True);shutil.copyfile(E/'original'/by[name]['path'],program)
 dependencies=[]
 if case=='exchange':
  for r in deps:
   target=root/r['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(E/'dependencies'/r['path'],target)
   dependencies.append({'path':r['path'],'sha256':sha(target),'bytes':target.stat().st_size})
 tree=ast.parse(program.read_text());imports=[n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)]+[a.name for n in ast.walk(tree)if isinstance(n,ast.Import)for a in n.names]
 start=time.time();proc=subprocess.run([sys.executable,str(program)],cwd=root,capture_output=True)
 directory=root.parent;(directory/'original.stdout.txt').write_bytes(proc.stdout);(directory/'original.stderr.txt').write_bytes(proc.stderr)
 report=program.with_name(output)
 state={'case':case,'original_program_execution_count':1,'argv':[sys.executable,str(program)],'cwd':str(root),'program':by[name]['path'],'program_sha256':sha(program),'program_bytes':program.stat().st_size,'imports':imports,'local_program_imports':[],'dependencies':dependencies,'exit_code':proc.returncode,'duration_seconds':time.time()-start,'stdout_bytes':len(proc.stdout),'stdout_sha256':sha(directory/'original.stdout.txt'),'stderr_bytes':len(proc.stderr),'stderr_sha256':sha(directory/'original.stderr.txt'),'report_created':report.exists(),'exclusive_output':'unmodified guarded main writes adjacent JSON with open x','path_difference':'source bytes and relative layout mirrored below a new external source-root, not original frozen filesystem path'}
 if report.exists():
  state.update({'new_report_bytes':report.stat().st_size,'new_report_sha256':sha(report),'equals_frozen_report_bytes':report.read_bytes()==(E/'original'/by[output]['path']).read_bytes(),'stdout_equals_report_bytes':proc.stdout==report.read_bytes()})
 (directory/'execution-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');runs.append(state)
 if proc.returncode:
  raise RuntimeError(f'Original {case} failed {proc.returncode}; all failure data preserved; no retry')
summary={'python':sys.version,'python_executable':sys.executable,'optimize':sys.flags.optimize,'platform':platform.platform(),'original_program_calls':len(runs),'runs':runs,'original_program_calls_per_entry':1,'note':'No importing original code to reuse definitions; no mutual imports. This recorder does not add any game/IC/search calculation.'}
(E/'replay/execution-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
