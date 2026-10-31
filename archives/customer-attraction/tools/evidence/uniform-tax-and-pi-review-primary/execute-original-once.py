"""One unchanged original top-level execution with passive per-lambda observation."""
from pathlib import Path
import ast,contextlib,datetime,hashlib,json,os,platform,runpy,shutil,sys,time,traceback
E=Path(__file__).resolve().parent;M=json.loads((E/'source-manifest.json').read_text());src=next(x for x in M if x['path'].endswith('.py'));D=json.loads((E/'dependency-manifest.json').read_text());out=E/'replay';out.mkdir(exist_ok=False);root=out/'source-root';root.mkdir();program=root/src['path'];program.parent.mkdir(parents=True);shutil.copyfile(E/'original'/src['path'],program)
for x in D:
 p=root/x['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(E/'dependencies'/x['path'],p);assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
assert program.parent.parents[5]==root;tree=ast.parse(program.read_text());rowline=next(n.lineno for n in ast.walk(tree)if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and isinstance(n.value.func.value,ast.Name)and n.value.func.value.id=='rows'and n.value.func.attr=='append');snap=[]
def tr(frame,event,arg):
 if frame.f_code.co_filename==str(program)and frame.f_code.co_name=='<module>':
  if event=='line'and frame.f_lineno==rowline:
   v=frame.f_locals;snap.append({'lambda':str(v['lam']),'scaled_comparisons':v['scaled_comparisons'],'nodes':[{'history':list(h),'regret':str(v['regret'][h]),'current_tax':str(v['tax'][h]),'remaining_credit':str(v['credits'][h])}for h in v['regret']],'prescribed_suffix_regret_sums':list(map(str,v['path_sums']))})
  return tr
 return None
prev=Path.cwd();oldargv=sys.argv[:];oldtrace=sys.gettrace();sys.dont_write_bytecode=True;start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();exitcode=0;ns={}
try:
 os.chdir(root);sys.argv=[str(program)]
 with (out/'stdout.txt').open('w')as so,(out/'stderr.txt').open('w')as se,contextlib.redirect_stdout(so),contextlib.redirect_stderr(se):
  try:sys.settrace(tr);ns=runpy.run_path(str(program),run_name='__main__')
  except BaseException:exitcode=1;traceback.print_exc()
  finally:sys.settrace(oldtrace)
finally:os.chdir(prev);sys.argv=oldargv
if ns:
 observation={'scope':'passive originally executed per-lambda row lines and final namespace; no extra original function calls','per_lambda':snap,'original_IC_slacks':list(map(str,ns['old_slacks'])),'original_actions':[{'history':list(h),'action':a}for h,a in ns['actions'].items()],'expanded_unit_likes':[sorted(t)for t in ns['customers']],'original_output':ns['answer'],'common_core_units':sum(len(t)==ns['k']for t in ns['customers'])}
 (out/'passive-observation.json').write_text(json.dumps(observation,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report=program.parent/'uniform_tax_independent_audit.json';frozen=E/'original'/next(x['path']for x in M if x['id']=='90dc474ead88b2d29be2');state={'source_id':src['id'],'source_invocations':1,'start_utc':start,'duration_seconds':time.monotonic()-t,'source_sha256':sha(program),'source_bytes':program.stat().st_size,'source_argv':[str(program)],'cwd':str(root),'original_ROOT':str(root),'entry':'original top-level runpy; no main guard/CLI','path_difference':'independent source-root preserving original repo-relative code/input paths, not frozen physical root','python':sys.version,'executable':sys.executable,'optimize':sys.flags.optimize,'platform':platform.platform(),'returncode':exitcode,'local_program_imports':[],'third_party_libraries':[],'true_file_inputs':[{'path':x['path'],'id':x['id'],'sha256':x['sha256']}for x in D],'output_path':str(report.relative_to(E)),'output_created':report.exists(),'output_bytes':report.stat().st_size if report.exists()else None,'output_sha256':sha(report)if report.exists()else None,'output_equals_frozen_bytes':report.exists()and report.read_bytes()==frozen.read_bytes(),'stdout_equals_output_bytes':report.exists()and report.read_bytes()==(out/'stdout.txt').read_bytes(),'stdout_bytes':(out/'stdout.txt').stat().st_size,'stderr_bytes':(out/'stderr.txt').stat().st_size,'passive_lambda_snapshots':len(snap),'extra_original_function_calls':0,'side_effect':'original write_text fixed report filename only in fresh HERE; original frozen report separate; bytecode disabled'}
(out/'execution.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');print(json.dumps(state,ensure_ascii=False));assert exitcode==0,'original failure retained; no retry'
