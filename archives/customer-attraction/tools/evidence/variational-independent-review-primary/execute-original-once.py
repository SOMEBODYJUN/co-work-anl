#!/usr/bin/env python3
"""One original blind-audit entry; passive source-only call observation."""
from pathlib import Path
import contextlib,io,json,sys,runpy,shutil,time,traceback,hashlib,platform
E=Path(__file__).resolve().parent;S=E.parents[4];W=S/'cleanup/workspaces/Boss4/r3-variational-independent-review-primary';g=json.loads((W/'primary-authorization-check.json').read_text());assert g['status']=='pass' and g['actual_expected_intersection_count']==5
replay=E/'replay';assert not replay.exists(),'single original replay already exists; never repeat'
replay.mkdir();rel=Path('research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/tail');source=E/'original'/rel/'audit_variational_blind.py';entry=replay/'source-root'/rel/source.name;entry.parent.mkdir(parents=True);shutil.copyfile(source,entry)
counts={};fixtures=[];case_returns=[];logargs=[];final={}
def profile(frame,event,arg):
 if frame.f_code.co_filename==str(entry):
  name=frame.f_code.co_name
  if event=='call':
   counts[name]=counts.get(name,0)+1
   if name=='audit_case':fixtures.append({k:frame.f_locals[k] for k in ('name','b','A','S','t','w')})
   if name=='log_bounds':logargs.append({'q':str(frame.f_locals['q']),'N':frame.f_locals['N']})
  if event=='return' and name=='audit_case':
   z=frame.f_locals;case_returns.append({k:str(z[k]) if k not in ('name','n','N') else z[k] for k in ('name','n','N','V','V1','R','R1','B','B1','seat','ratios')})
  if event=='return' and name=='<module>':
   z=frame.f_globals
   for k in ('lo','hi','t','wp','derivative','M','gradient','U'):final[k]=z[k]
out=io.StringIO();err=io.StringIO();code=0;start=time.monotonic()
try:
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  sys.setprofile(profile)
  try:runpy.run_path(str(entry),run_name='__main__')
  finally:sys.setprofile(None)
except BaseException:code=1;traceback.print_exc(file=err)
def encode(v):return sorted(v) if isinstance(v,(set,frozenset)) else str(v)
obs={'method':'passive source-filename-only call/return records; no source functions invoked by observer','function_calls':counts,'embedded_original_fixture_arguments':fixtures,'case_return_locals':case_returns,'log_bounds_arguments':logargs,'final_original_globals':final,'observer_extra_original_calls':0}
(replay/'passive-observation.json').write_text(json.dumps(obs,default=encode,ensure_ascii=False,indent=2)+'\n');(replay/'stdout.txt').write_text(out.getvalue());(replay/'stderr.txt').write_text(err.getvalue())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
output=entry.with_name('variational_blind_exact.json');frozen=E/'original'/rel/output.name
rec={'status':'success' if not code else 'failure','exit_code':code,'original_entry_calls':1,'source_sha256':sha(source),'runtime_entry':str(entry.relative_to(S)),'source_bytes_unchanged':sha(source)==sha(entry),'new_empty_replay':True,'source_absolute_path_is_relocated':True,'true_runtime_file_inputs':[],'python':platform.python_version(),'optimize':sys.flags.optimize,'elapsed_seconds':time.monotonic()-start,'output':{'path':str(output.relative_to(S)),'size':output.stat().st_size if output.exists() else None,'sha256':sha(output) if output.exists() else None,'frozen_sha256':sha(frozen),'frozen_byte_equal':output.exists() and output.read_bytes()==frozen.read_bytes()},'stdout_bytes':len(out.getvalue().encode()),'stderr_bytes':len(err.getvalue().encode()),'optimizer_SPE_project_calls':0,'network_or_shared_repo_writes':0}
(replay/'execution.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2));assert code==0 and rec['output']['frozen_byte_equal']
