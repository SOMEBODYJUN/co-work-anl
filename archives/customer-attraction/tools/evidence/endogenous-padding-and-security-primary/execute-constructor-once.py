"""One unchanged constructor top-level execution, with true package closure; no verifier added."""
from pathlib import Path
import contextlib,datetime,hashlib,json,os,platform,runpy,shutil,sys,time,traceback
E=Path(__file__).resolve().parent;M=json.loads((E/'source-manifest.json').read_text());D=json.loads((E/'dependency-manifest.json').read_text());src=next(x for x in M if x['id']=='6b82d9246e87ddc266e8');out=E/'replay';out.mkdir(exist_ok=False);root=out/'source-root';root.mkdir();program=root/src['path'];program.parent.mkdir(parents=True);shutil.copyfile(E/'original'/src['path'],program)
for x in D:
 p=root/x['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(E/'dependencies'/x['path'],p);assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
assert program.parent.parents[5]==root;calls={'ExactSPESolver.certificate':0,'verify_certificate':0}
def tr(frame,event,arg):
 if event=='call'and str(root/'customer_attraction')in frame.f_code.co_filename:
  if frame.f_code.co_name=='certificate':calls['ExactSPESolver.certificate']+=1
  elif frame.f_code.co_name=='verify_certificate':calls['verify_certificate']+=1
 return None
oldcwd=Path.cwd();oldargv=sys.argv[:];oldpath=sys.path[:];oldtrace=sys.gettrace();sys.dont_write_bytecode=True;start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();rc=0;ns={}
try:
 os.chdir(root);sys.argv=[str(program)]
 with(out/'stdout.txt').open('w')as so,(out/'stderr.txt').open('w')as se,contextlib.redirect_stdout(so),contextlib.redirect_stderr(se):
  try:sys.settrace(tr);ns=runpy.run_path(str(program),run_name='__main__')
  except BaseException:rc=1;traceback.print_exc()
  finally:sys.settrace(oldtrace)
finally:os.chdir(oldcwd);sys.argv=oldargv;sys.path[:]=oldpath
if ns:
 sol=ns['sol'];cert=ns['cert'];ob={'scope':'originally observed package calls and final returned namespace only; no extra constructor/solver/verifier calls','actual_calls':calls,'generated_customer_count':sum(x.multiplicity for x in ns['ins'].customers),'generated_players':ns['ins'].players,'generated_topics':list(ns['ins'].topics),'strategy_keys':len(cert.actions),'terminal_counts':list(cert.terminal_counts),'solver_cache':{'count_states':len(sol._outcomes),'terminal_states':sum(sum(c)==ns['ins'].players for c in sol._outcomes),'retained_outcomes':sum(len(v)for v in sol._outcomes.values()),'threshold_states':len(sol._thresholds)}}
 (out/'passive-observation.json').write_text(json.dumps(ob,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
outputs=[program.parent/'endogenous_53_instance.json',program.parent/'endogenous_53_strategy.json'];state={'source_invocations':1,'source_id':src['id'],'source_bytes':program.stat().st_size,'source_sha256':sha(program),'entry':'original runpy top-level; no main guard; imports oracle to construct only','source_argv':[str(program)],'cwd':str(root),'resolved_ROOT':str(root),'start_utc':start,'duration_seconds':time.monotonic()-t,'python':sys.version,'executable':sys.executable,'optimize':sys.flags.optimize,'platform':platform.platform(),'returncode':rc,'true_file_dependencies':[{'id':x['id'],'path':x['path'],'sha256':x['sha256']}for x in D],'imported_local_modules':[{'module':k,'path':v.__file__,'sha256':sha(Path(v.__file__))}for k,v in sys.modules.items()if k.startswith('customer_attraction')and getattr(v,'__file__',None)],'third_party_libraries':[],'outputs':[{'path':str(p.relative_to(E)),'bytes':p.stat().st_size,'sha256':sha(p),'equals_primary_ids':[x['id']for x in M if p.read_bytes()==(E/'original'/x['path']).read_bytes()]}for p in outputs if p.exists()],'stdout_bytes':(out/'stdout.txt').stat().st_size,'stderr_bytes':(out/'stderr.txt').stat().st_size,'actual_calls':calls,'extra_original_function_calls':0,'path_difference':'fresh independent source-root preserving all repo-relative paths; not author physical root','side_effect':'constructor sys.path adds ROOT and writes two fixed names in fresh HERE; both frozen primary outputs separate, pycache disabled'}
(out/'execution.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');print(json.dumps(state,ensure_ascii=False));assert rc==0,'original failure retained, no retry'
