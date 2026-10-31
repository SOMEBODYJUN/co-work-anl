#!/usr/bin/env python3
"""Single unmodified original entry, passive call/branch observation only."""
from pathlib import Path
import ast,contextlib,io,json,sys,runpy,hashlib,shutil,time,traceback,platform
E=Path(__file__).resolve().parent;S=E.parents[4];W=S/'cleanup/workspaces/Boss4/r3-variational-waterfill-and-switch-debt-primary'
g=json.loads((W/'primary-authorization-check.json').read_text());assert g['status']=='pass' and g['actual_expected_intersection_count']==5
replay=E/'replay';assert not replay.exists(),'single original replay already exists; do not repeat'
replay.mkdir();rel=Path('research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/shared');source=E/'original'/rel/'audit_variational_common_credit.py';entry=replay/'source-root'/rel/source.name;entry.parent.mkdir(parents=True);shutil.copyfile(source,entry)
tr=ast.parse(source.read_text());node=next(a for a in ast.walk(tr) if isinstance(a,ast.If) and 'V(one)' in ast.unparse(a.test));branchline=node.body[0].lineno
counts={};fixtures=[];returns=[];joint_names=[];log_q=[];derivatives={}
def observe(frame,event,arg):
 if frame.f_code.co_filename==str(entry):
  name=frame.f_code.co_name
  if event=='call':
   counts[name]=counts.get(name,0)+1
   if name=='certificate':fixtures.append({k:frame.f_locals[k] for k in ('name','N','b','A','tails','t','w')})
   if name=='log_bounds':log_q.append(str(frame.f_locals['q']))
  if event=='return' and name=='certificate':
   z=frame.f_locals;queries=z['queries'];returns.append({'name':z['name'],'N':len(z['N']),'tail_count':len(z['w']),'query_entries':len(queries),'distinct_query_sets':len({frozenset(a) for a in queries}),'mass':str(z['M']),'loss':str(z['loss']),'H':str(z['H'])})
  if event=='return' and name=='<module>':
   for k in ('dx','dy','du','det','alpha_prime','beta_prime','root_prime','mass_prime'):derivatives[k]=str(frame.f_globals[k])
def trace(frame,event,arg):
 if event=='call':
  return trace if frame.f_code.co_filename==str(entry) and frame.f_code.co_name=='certificate' else None
 if event=='line' and frame.f_lineno==branchline:joint_names.append(frame.f_locals['name'])
 return trace
out=io.StringIO();err=io.StringIO();exit_code=0;start=time.monotonic()
try:
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  sys.setprofile(observe);sys.settrace(trace)
  try:runpy.run_path(str(entry),run_name='__main__')
  finally:sys.settrace(None);sys.setprofile(None)
except BaseException:exit_code=1;traceback.print_exc(file=err)
elapsed=time.monotonic()-start
(replay/'stdout.txt').write_text(out.getvalue());(replay/'stderr.txt').write_text(err.getvalue())
obs={'method':'source filename call/profile and selected original conditional assertion line events; no observer invokes original functions','function_calls':counts,'embedded_original_fixture_arguments':fixtures,'certificate_returns':returns,'conditional_V_initial_ge_tn_assertion_line':branchline,'conditional_V_initial_ge_tn_executed_names':joint_names,'log_bounds_actual_uncached_q':log_q,'nonmonotone_original_globals':derivatives,'observer_extra_original_calls':0}
(replay/'passive-observation.json').write_text(json.dumps(obs,ensure_ascii=False,default=str,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
output=entry.with_name('variational_common_credit_audit.json');frozen=E/'original'/rel/output.name
rec={'status':'success' if not exit_code else 'failure','exit_code':exit_code,'original_entry_calls':1,'source_sha256':sha(source),'runtime_entry':str(entry.relative_to(S)),'new_empty_replay':True,'source_absolute_path_is_relocated':True,'source_bytes_unchanged':sha(source)==sha(entry),'true_runtime_file_inputs':[],'python':platform.python_version(),'optimize':sys.flags.optimize,'elapsed_seconds':elapsed,'output':{'path':str(output.relative_to(S)),'size':output.stat().st_size if output.exists() else None,'sha256':sha(output) if output.exists() else None,'frozen_sha256':sha(frozen),'frozen_byte_equal':output.exists() and output.read_bytes()==frozen.read_bytes()},'stdout_bytes':len(out.getvalue().encode()),'stderr_bytes':len(err.getvalue().encode()),'optimizer_project_solver_payoff_verifier_calls':0,'shared_repo_writes_or_network':0}
(replay/'execution.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2));assert exit_code==0 and rec['output']['frozen_byte_equal']
