"""One original __main__ run; passive profile captures built-in input and existing action returns."""
from pathlib import Path
import ast,contextlib,hashlib,json,os,platform,runpy,shutil,sys,time,traceback
E=Path(__file__).resolve().parent;items=json.loads((E/'source-manifest.json').read_text());src=next(r for r in items if r['path'].endswith('.py'));frozen=next(r for r in items if r['path'].endswith('conditional_transport_audit.json'))
replay=E/'replay';replay.mkdir(exist_ok=False);root=replay/'source-root';root.mkdir();program=root/src['path'];program.parent.mkdir(parents=True);shutil.copyfile(E/'original'/src['path'],program)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
observed_actions={};run_observation={}
def profile(frame,event,arg):
 if event!='return' or frame.f_code.co_filename!=str(program):return
 if frame.f_code.co_name=='action':
  h=tuple(frame.f_locals['h'])
  if h in observed_actions:assert observed_actions[h]==arg
  observed_actions[h]=arg
 elif frame.f_code.co_name=='run':
  v=frame.f_locals
  run_observation.update({'scope':'passive original return locals, no extra action/terminal/pay/IC invocation','groups':[list(g)for g in v['groups']],'unit_customer_likes':[sorted(c)for c in v['units']],'p':[str(x)for x in v['p']],'all_conditional_tail_loads':[str(x)for x in v['ell']],'original_gap_values_in_original_order':[str(x)for x in v['gaps']],'actual_path':list(v['path']),'original_return':arg})
old_cwd=Path.cwd();old_argv=sys.argv[:];exit_code=0;start=time.time()
try:
 os.chdir(root);sys.argv=[str(program)]
 with (replay/'original.stdout.txt').open('w')as out,(replay/'original.stderr.txt').open('w')as err:
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
   try:
    sys.setprofile(profile);runpy.run_path(str(program),run_name='__main__')
   except BaseException:
    exit_code=1;traceback.print_exc()
   finally:sys.setprofile(None)
finally:os.chdir(old_cwd);sys.argv=old_argv
run_observation['observed_original_action_returns']=[{'history':list(h),'action':a}for h,a in sorted(observed_actions.items(),key=lambda x:(len(x[0]),x[0]))]
(replay/'program-built-input-and-runtime.json').write_text(json.dumps(run_observation,ensure_ascii=False,indent=2)+'\n')
report=program.with_name('conditional_transport_audit.json');tree=ast.parse(program.read_text());imports=[n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)]+[a.name for n in ast.walk(tree)if isinstance(n,ast.Import)for a in n.names]
state={'original_program_calls':1,'execution_count':1,'method':'runpy.run_path original bytes with __main__; passive sys.setprofile observes action/run returns only, no extra source-function calls','argv':[str(program)],'cwd':str(root),'program':src['path'],'program_bytes':program.stat().st_size,'program_sha256':sha(program),'python':sys.version,'executable':sys.executable,'optimize':sys.flags.optimize,'platform':platform.platform(),'imports':imports,'local_program_imports':[],'external_dependencies':[],'exit_code':exit_code,'duration_seconds':time.time()-start,'stdout_bytes':(replay/'original.stdout.txt').stat().st_size,'stdout_sha256':sha(replay/'original.stdout.txt'),'stderr_bytes':(replay/'original.stderr.txt').stat().st_size,'stderr_sha256':sha(replay/'original.stderr.txt'),'report_created':report.exists(),'source_output_behavior':'original write_text overwrites adjacent filename; new empty isolated source root and once-only wrapper keep frozen originals untouched','path_difference':'byte-identical source at original repo-relative path below independent external source-root, not original frozen filesystem path','observed_policy_keys':len(observed_actions),'observed_gap_values':len(run_observation.get('original_gap_values_in_original_order',[]))}
if report.exists():state.update({'new_report_bytes':report.stat().st_size,'new_report_sha256':sha(report),'equals_frozen_report_bytes':report.read_bytes()==(E/'original'/frozen['path']).read_bytes(),'stdout_equals_report_bytes':(replay/'original.stdout.txt').read_bytes()==report.read_bytes()})
(replay/'execution-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');print(json.dumps(state,ensure_ascii=False));assert exit_code==0,'Original failure preserved; no automatic retry'
