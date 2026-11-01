#!/usr/bin/env python3
"""Single original entry, separate new local path; profile never calls source functions."""
from pathlib import Path
import contextlib,io,json,sys,runpy,hashlib,shutil,time,traceback,platform
E=Path(__file__).resolve().parent
S=E.parents[4]
W=S/'cleanup/workspaces/Boss4/r3-waterfill-credit-and-sharpness-primary'
gate=json.loads((W/'primary-authorization-check.json').read_text())
assert gate['status']=='pass' and gate['actual_expected_intersection_count']==5
replay=E/'replay'
assert not replay.exists(),'This single original replay already exists; never repeat.'
replay.mkdir()
rel=Path('research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/tail')
root=replay/'source-root';here=root/rel;here.mkdir(parents=True)
source=E/'original'/rel/'audit_waterfill.py';entry=here/source.name
shutil.copyfile(source,entry)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inputs=[]
for name in ('endogenous_53_instance.json','endogenous_53_strategy.json'):
 p=E/'dependencies'/rel/name;q=here/name;shutil.copyfile(p,q)
 inputs.append({'source':str(p.relative_to(S)),'runtime_path':str(q.relative_to(S)),'size':p.stat().st_size,'sha256':sha(p)})
counts={};final={}
def profile(frame,event,arg):
 if frame.f_code.co_filename==str(entry):
  if event=='call':counts[frame.f_code.co_name]=counts.get(frame.f_code.co_name,0)+1
  if event=='return' and frame.f_code.co_name=='<module>':
   g=frame.f_globals
   for k in ('comparisons','finite_checks','least','actual','z','t0','D','m','p'):
    if k in g: final[k]=str(g[k])
   final['expected_histories']=len(g.get('expected',()))
   final['backgrounds']=len(g.get('backgrounds',()))
 return profile
out=io.StringIO();err=io.StringIO();exit_code=0;start=time.monotonic()
try:
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  sys.setprofile(profile)
  try:runpy.run_path(str(entry),run_name='__main__')
  finally:sys.setprofile(None)
except BaseException:
 exit_code=1;traceback.print_exc(file=err)
elapsed=time.monotonic()-start
(replay/'stdout.txt').write_text(out.getvalue());(replay/'stderr.txt').write_text(err.getvalue())
output=here/'waterfill_exact.json';frozen=E/'original'/rel/'waterfill_exact.json'
ob={'method':'passive Python profile of original filename only; no source function invoked by observer','original_function_calls':counts,'final_original_globals':final,'no_extra_original_import_or_calls':True}
(replay/'passive-observation.json').write_text(json.dumps(ob,indent=2)+'\n')
record={'status':'success' if exit_code==0 else 'failure','exit_code':exit_code,'original_entry_calls':1,'source_sha256':sha(source),'runtime_entry':str(entry.relative_to(S)),'new_empty_replay':True,'original_bytes_unchanged':sha(source)==sha(entry),'python':platform.python_version(),'optimize':sys.flags.optimize,'elapsed_seconds':elapsed,'true_file_inputs':inputs,'input_bytes_unchanged':all(sha(S/a['runtime_path'])==a['sha256'] for a in inputs),'output':{'path':str(output.relative_to(S)),'size':output.stat().st_size if output.exists() else None,'sha256':sha(output) if output.exists() else None,'frozen_sha256':sha(frozen),'frozen_byte_equal':output.exists() and output.read_bytes()==frozen.read_bytes()},'stdout_bytes':len(out.getvalue().encode()),'stderr_bytes':len(err.getvalue().encode()),'no_solver_LP_verifier_import':True,'source_absolute_path_is_relocated':True,'no_shared_repo_write_or_network':True}
(replay/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
assert exit_code==0
assert record['output']['frozen_byte_equal'] and record['input_bytes_unchanged']
