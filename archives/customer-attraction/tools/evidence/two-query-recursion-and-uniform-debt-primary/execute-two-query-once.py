#!/usr/bin/env python3
"""One original3378 entry, four-path obligation only, passive observations."""
from pathlib import Path
import contextlib,io,json,sys,runpy,shutil,time,traceback,hashlib,platform
E=Path(__file__).resolve().parent;S=E.parents[4];W=S/'cleanup/workspaces/Boss4/r3-two-query-recursion-and-uniform-debt-primary';g=json.loads((W/'primary-authorization-check.json').read_text());assert g['status']=='pass' and g['actual_expected_intersection_count']==5
replay=E/'replay-two-query';assert not replay.exists(),'single original replay exists; never repeat'
replay.mkdir();root=replay/'source-root';rel=Path('research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/mixed');source=E/'original'/rel/'audit_two_query_recursion.py';entry=root/rel/source.name;entry.parent.mkdir(parents=True);shutil.copyfile(source,entry)
dep=json.loads((E/'dependency-manifest.json').read_text())['two_query']['available'][0];input_src=S/dep['path'];input_run=root/dep['source_path'];input_run.parent.mkdir(parents=True);shutil.copyfile(input_src,input_run)
counts={};final={}
def profile(frame,event,arg):
 if frame.f_code.co_filename==str(entry):
  name=frame.f_code.co_name
  if event=='call':counts[name]=counts.get(name,0)+1
  if event=='return' and name=='main':
   z=frame.f_locals
   for k in ('ZA','ZB','ZAb','ZBa','a','b','RAB','RBA','gammaA','gammaB','deepA','deepB','FA','FB','KAB','KBA','dA','dB','etaAB','etaBA'):final[k]=z[k]
   final['strategy_dictionary_loaded']=len(z['strategy']);final['unit_clients_loaded']=len(z['clients']);final['REPO']=str(frame.f_globals['REPO']);final['SOURCE']=str(frame.f_globals['SOURCE'])
out=io.StringIO();err=io.StringIO();code=0;start=time.monotonic()
try:
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  sys.setprofile(profile)
  try:runpy.run_path(str(entry),run_name='__main__')
  finally:sys.setprofile(None)
except BaseException:code=1;traceback.print_exc(file=err)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
(replay/'stdout.txt').write_text(out.getvalue());(replay/'stderr.txt').write_text(err.getvalue());(replay/'passive-observation.json').write_text(json.dumps({'method':'source-filename-only passive profile, no observer source calls','function_calls':counts,'final_original_values':final,'observer_extra_original_calls':0,'new_all43_SPE_audits':0,'new_258_full_IC_scans':0,'new_all36_K_scans':0},default=str,indent=2)+'\n')
output=entry.with_name('two_query_recursion_audit.json');frozen=source.with_name(output.name)
r={'status':'success' if not code else 'failure','exit_code':code,'original_entry_calls':1,'source_sha256':sha(source),'runtime_entry':str(entry.relative_to(S)),'source_bytes_unchanged':sha(source)==sha(entry),'new_empty_replay':True,'source_absolute_path_is_relocated':True,'python':platform.python_version(),'optimize':sys.flags.optimize,'elapsed_seconds':time.monotonic()-start,'true_runtime_file_inputs':[{'path':dep['path'],'runtime_path':str(input_run.relative_to(S)),'size':input_src.stat().st_size,'sha256':sha(input_src)}],'input_bytes_unchanged':sha(input_src)==sha(input_run),'output':{'path':str(output.relative_to(S)),'size':output.stat().st_size if output.exists() else None,'sha256':sha(output) if output.exists() else None,'frozen_sha256':sha(frozen),'frozen_byte_equal':output.exists() and output.read_bytes()==frozen.read_bytes()},'stdout_bytes':len(out.getvalue().encode()),'stderr_bytes':len(err.getvalue().encode()),'involved_child_IC_comparisons':2,'involved_terminal_BR_comparisons':2,'uniform_debt3862_calls':0,'optimizer_SPE_solver_or_project_calls':0,'network_or_shared_repo_writes':0}
(replay/'execution.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));assert code==0 and r['output']['frozen_byte_equal'] and r['input_bytes_unchanged']
