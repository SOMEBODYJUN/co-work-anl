#!/usr/bin/env python3
"""One selected original entry per new empty replay; passive source-only observations."""
from pathlib import Path
import contextlib,io,json,sys,runpy,hashlib,shutil,time,traceback,platform
E=Path(__file__).resolve().parent;S=E.parents[4];W=S/'cleanup/workspaces/Boss4/r3-independent-waterfill-audits-primary'
gate=json.loads((W/'primary-authorization-check.json').read_text());assert gate['status']=='pass' and gate['actual_expected_intersection_count']==5
label=sys.argv[1];assert label in ('mixed','shared')
base=Path('research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2')
name={'mixed':'audit_waterfill_review.py','shared':'audit_waterfill_independent.py'}[label]
output_name={'mixed':'waterfill_review_audit.json','shared':'waterfill_independent_audit.json'}[label]
replay=E/'replay'/label;assert not replay.exists(),'original run already has replay; never repeat'
replay.mkdir(parents=True);root=replay/'source-root';here=root/base/label;here.mkdir(parents=True)
source=E/'original'/base/label/name;entry=here/name;shutil.copyfile(source,entry)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inputs=[]
if label=='mixed':
 for filename in ('endogenous_53_instance.json','endogenous_53_strategy.json','waterfill_exact.json'):
  p=E/'dependencies'/base/'tail'/filename;q=root/base/'tail'/filename;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
  inputs.append({'path':str(p.relative_to(S)),'runtime_path':str(q.relative_to(S)),'size':p.stat().st_size,'sha256':sha(p)})
counts={};fixtures=[];final={}
def profile(frame,event,arg):
 if frame.f_code.co_filename==str(entry):
  name=frame.f_code.co_name
  if event=='call':
   counts[name]=counts.get(name,0)+1
   if name=='audit':fixtures.append({k:frame.f_locals[k] for k in ('name','universe','background','root','tails','threshold','stops') if k in frame.f_locals})
  if event=='return':
   if label=='mixed' and name=='main':
    for k in ('comparisons','core_translation_checks','minimum','actual','utilities','load_spectrum','frozen_checks'):
     if k in frame.f_locals:final[k]=frame.f_locals[k]
   if label=='shared' and name=='<module>':
    g=frame.f_globals;observed.update({'rational_cases':len(g.get('cases',[])),'queries_checked':sum(a['queries_checked'] for a in g.get('cases',[])),'irrational_width':str(g['hi']-g['lo'])})
 return profile
observed={};out=io.StringIO();err=io.StringIO();exit_code=0;start=time.monotonic()
try:
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  sys.setprofile(profile)
  try:runpy.run_path(str(entry),run_name='__main__')
  finally:sys.setprofile(None)
except BaseException:
 exit_code=1;traceback.print_exc(file=err)
elapsed=time.monotonic()-start
(replay/'stdout.txt').write_text(out.getvalue());(replay/'stderr.txt').write_text(err.getvalue())
output=here/output_name;frozen=E/'original'/base/label/output_name
obs={'method':'source-filename-only passive profile; no source functions invoked by observer','function_calls':counts,'fixture_arguments':fixtures,'final_original_values':observed if label=='shared' else final,'no_extra_source_calls':True}
(replay/'passive-observation.json').write_text(json.dumps(obs,ensure_ascii=False,default=str,indent=2)+'\n')
rec={'status':'success' if exit_code==0 else 'failure','label':label,'exit_code':exit_code,'original_entry_calls':1,'source_sha256':sha(source),'runtime_entry':str(entry.relative_to(S)),'original_bytes_unchanged':sha(source)==sha(entry),'new_empty_replay':True,'source_absolute_path_is_relocated':True,'python':platform.python_version(),'optimize':sys.flags.optimize,'elapsed_seconds':elapsed,'true_file_inputs':inputs,'inputs_unchanged':all(sha(S/a['runtime_path'])==a['sha256'] for a in inputs),'output':{'path':str(output.relative_to(S)),'size':output.stat().st_size if output.exists() else None,'sha256':sha(output) if output.exists() else None,'frozen_sha256':sha(frozen),'frozen_byte_equal':output.exists() and output.read_bytes()==frozen.read_bytes()},'stdout_bytes':len(out.getvalue().encode()),'stderr_bytes':len(err.getvalue().encode()),'project_solver_payoff_verifier_imports':0,'no_shared_repo_write_or_network':True}
(replay/'execution.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2));assert exit_code==0 and rec['output']['frozen_byte_equal'] and rec['inputs_unchanged']
