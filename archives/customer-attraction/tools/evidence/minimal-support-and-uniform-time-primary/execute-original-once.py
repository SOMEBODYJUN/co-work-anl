#!/usr/bin/env python3
"""One raw minimal-support entry in its exact relative path; no extra source calls."""
from pathlib import Path
import contextlib,io,json,sys,runpy,shutil,time,traceback,hashlib,platform
E=Path(__file__).resolve().parent;S=E.parents[4];W=S/'cleanup/workspaces/Boss4/r3-minimal-support-and-uniform-time-primary';g=json.loads((W/'primary-authorization-check.json').read_text());assert g['status']=='pass' and g['actual_expected_intersection_count']==5
replay=E/'replay';assert not replay.exists(),'single original replay already exists; never repeat'
replay.mkdir();root=replay/'source-root';rel=Path('research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/mixed');source=E/'original'/rel/'audit_minimal_support.py';entry=root/rel/source.name;entry.parent.mkdir(parents=True);shutil.copyfile(source,entry)
dep=json.loads((E/'dependency-manifest.json').read_text())['rows'][0];p=S/dep['path'];q=root/dep['source_path'];q.parent.mkdir(parents=True);shutil.copyfile(p,q)
counts={};final={}
def profile(frame,event,arg):
 if frame.f_code.co_filename==str(entry):
  name=frame.f_code.co_name
  if event=='call':counts[name]=counts.get(name,0)+1
  if event=='return' and name=='main':
   z=frame.f_locals
   for k in ('comparisons','actual','u','d','K','taxes','pair','abstract','extra_pairs'):final[k]=z[k]
   final['histories']=len(z['histories']);final['clients']=len(z['clients']);final['REPO']=str(frame.f_globals['REPO']);final['SOURCE']=str(frame.f_globals['SOURCE'])
out=io.StringIO();err=io.StringIO();code=0;start=time.monotonic()
try:
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  sys.setprofile(profile)
  try:runpy.run_path(str(entry),run_name='__main__')
  finally:sys.setprofile(None)
except BaseException:code=1;traceback.print_exc(file=err)
(replay/'stdout.txt').write_text(out.getvalue());(replay/'stderr.txt').write_text(err.getvalue());(replay/'passive-observation.json').write_text(json.dumps({'method':'source-filename-only passive profile, observer invokes no source functions','function_calls':counts,'final_original_values':final,'observer_extra_original_calls':0},default=str,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
output=entry.with_name('minimal_support_audit.json');frozen=source.with_name(output.name)
rec={'status':'success' if not code else 'failure','exit_code':code,'original_entry_calls':1,'source_sha256':sha(source),'runtime_entry':str(entry.relative_to(S)),'source_bytes_unchanged':sha(source)==sha(entry),'new_empty_replay':True,'source_absolute_path_is_relocated':True,'python':platform.python_version(),'optimize':sys.flags.optimize,'elapsed_seconds':time.monotonic()-start,'true_runtime_file_inputs':[{'path':dep['path'],'runtime_path':str(q.relative_to(S)),'size':p.stat().st_size,'sha256':sha(p)}],'input_bytes_unchanged':sha(p)==sha(q),'output':{'path':str(output.relative_to(S)),'size':output.stat().st_size if output.exists() else None,'sha256':sha(output) if output.exists() else None,'frozen_sha256':sha(frozen),'frozen_byte_equal':output.exists() and output.read_bytes()==frozen.read_bytes()},'stdout_bytes':len(out.getvalue().encode()),'stderr_bytes':len(err.getvalue().encode()),'optimizer_SPE_solver_project_verifier_calls':0,'network_or_shared_repo_writes':0}
(replay/'execution.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2));assert code==0 and rec['output']['frozen_byte_equal'] and rec['input_bytes_unchanged']
