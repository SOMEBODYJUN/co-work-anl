"""Execute exactly one requested unchanged original in a fresh isolated tree; passive trace only."""
from pathlib import Path
import argparse,ast,contextlib,datetime,hashlib,json,os,platform,runpy,shutil,sys,time,traceback
p=argparse.ArgumentParser();p.add_argument('mode',choices=['fixed-cone','known-cases']);mode=p.parse_args().mode
E=Path(__file__).resolve().parent;M=json.loads((E/'source-manifest.json').read_text());D=json.loads((E/'dependency-manifest.json').read_text());row=next(x for x in M if x['id']==('1bd769d92e6bcbdc563a'if mode=='fixed-cone'else'f690378df805d692ebb2'));out=E/'replay'/mode;out.mkdir(parents=True,exist_ok=False);root=out/'source-root';root.mkdir();program=root/row['path'];program.parent.mkdir(parents=True);shutil.copyfile(E/'original'/row['path'],program)
chosen=[x for x in D if (x['path'].startswith('evidence/')if mode=='fixed-cone'else not x['path'].startswith('evidence/'))]
for x in chosen:
 q=root/x['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(E/'dependencies'/x['path'],q);assert hashlib.sha256(q.read_bytes()).hexdigest()==x['sha256']
assert program.parent.parents[5]==root and hashlib.sha256(program.read_bytes()).hexdigest()==row['sha256']
source=program.read_text();tree=ast.parse(source);lp_line=next((n.lineno for n in ast.walk(tree)if isinstance(n,ast.Assert)and ast.unparse(n.test)=='res.success'),None)
observations={'scope':'passive events and returned namespace only; zero extra original source/solver/verifier function invocations','LP_calls':[],'threshold_returns':[],'verify_certificate_calls':0,'solver_certificate_calls':0}
def tr(frame,event,arg):
 fn=frame.f_code.co_filename;name=frame.f_code.co_name
 if fn==str(program)and name=='<module>':
  if event=='line'and frame.f_lineno==lp_line:
   v=frame.f_locals;res=v['res'];observations['LP_calls'].append({'q':list(v['q']),'success':bool(res.success),'status':int(res.status),'fun':float(res.fun),'nit':int(res.nit),'message':str(res.message)})
  return tr
 if str(root/'customer_attraction')in fn:
  if event=='call'and name=='verify_certificate':observations['verify_certificate_calls']+=1
  if event=='call'and name=='certificate':observations['solver_certificate_calls']+=1
  if name=='threshold':
   if event=='return':
    v=frame.f_locals;s=v['self'];observations['threshold_returns'].append({'prefix':list(v['counts']),'floor':str(arg),'customer_count':sum(c.multiplicity for c in s.instance.customers),'topic_count':s.instance.topic_count,'players':s.instance.players,'retained_at_prefix':len(s._outcomes[v['counts']]),'cache_count_states':len(s._outcomes),'cache_terminal_states':sum(sum(c)==s.instance.players for c in s._outcomes),'cache_retained_outcomes':sum(len(a)for a in s._outcomes.values())})
   return tr
 return None
oldcwd=Path.cwd();oldargv=sys.argv[:];oldpath=sys.path[:];oldtrace=sys.gettrace();sys.dont_write_bytecode=True
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();exit_code=0;ns={}
try:
 os.chdir(root);sys.path.insert(0,str(root));sys.argv=[str(program)]
 with (out/'stdout.txt').open('w')as so,(out/'stderr.txt').open('w')as se,contextlib.redirect_stdout(so),contextlib.redirect_stderr(se):
  try:sys.settrace(tr);ns=runpy.run_path(str(program),run_name='__main__')
  except BaseException as ex:exit_code=ex.code if isinstance(ex,SystemExit)and isinstance(ex.code,int)else 1;traceback.print_exc()
  finally:sys.settrace(oldtrace)
finally:os.chdir(oldcwd);sys.argv=oldargv;sys.path[:]=oldpath
if ns and mode=='fixed-cone':
 observations.update({'r':ns['r'],'k':ns['k'],'types':[list(z)for z in ns['types']],'histories':[list(h)for h in ns['histories']],'all_r':[list(q)for q in ns['all_r']],'all_r1':[list(q)for q in ns['all_r1']],'exact_constraint_rows':[[str(x)for x in z]for z in ns['constraints']],'exact_root_equality':[str(x)for x in ns['eq']],'ic_count':ns['ic_count'],'candidate_if_generated':ns.get('candidate'),'last_reconstructed_weights':[str(x)for x in ns.get('w',[])],'last_exact_gap_normalized':str(ns.get('exact_gap')),'last_exact_min_IC_slack':str(min(ns['ic_slacks']))if 'ic_slacks'in ns else None,'last_exact_min_dual_variable_residual':str(min(ns['residual'])),'last_numeric_result':{'x':list(map(float,ns['res'].x)),'fun':float(ns['res'].fun),'inequality_marginals':list(map(float,ns['res'].ineqlin.marginals)),'equality_marginal':float(ns['res'].eqlin.marginals[0])}})
if ns and mode=='known-cases':observations['actual_source_cases']=ns['cases']
(out/'passive-observation.json').write_text(json.dumps(observations,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
outputs=[q for q in program.parent.glob('*.json')];state={'mode':mode,'source_invocations':1,'start_utc':start,'duration_seconds':time.monotonic()-t,'source_id':row['id'],'source_sha256':sha(program),'source_bytes':program.stat().st_size,'entry':'one runpy original top-level; no CLI; no main guard','source_argv':[str(program)],'cwd':str(root),'original_ROOT':str(root),'physical_path_difference':'new independent source-root with unchanged repo-relative paths, not author physical root','python':sys.version,'executable':sys.executable,'optimize':sys.flags.optimize,'platform':platform.platform(),'returncode':exit_code,'true_file_dependencies':[{'path':x['path'],'id':x['id'],'sha256':x['sha256']}for x in chosen],'imported_local_modules':[{'module':k,'path':v.__file__,'sha256':sha(Path(v.__file__))}for k,v in sys.modules.items()if k.startswith('customer_attraction')and getattr(v,'__file__',None)],'third_party_versions':{k:getattr(sys.modules[k],'__version__',None)for k in ['numpy','scipy']if k in sys.modules},'outputs':[{'path':str(q.relative_to(E)),'bytes':q.stat().st_size,'sha256':sha(q),'equals_primary_report_ids':[x['id']for x in M if x['path'].endswith('.json')and q.read_bytes()==(E/'original'/x['path']).read_bytes()]}for q in sorted(outputs)],'stdout_bytes':(out/'stdout.txt').stat().st_size,'stderr_bytes':(out/'stderr.txt').stat().st_size,'trace_extra_original_calls':0,'side_effect':'only fresh original HERE outputs; original source uses write_text overwrite, old frozen reports stored separately; pycache disabled'}
(out/'execution.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');print(json.dumps(state,ensure_ascii=False));assert exit_code==0,'original failure retained; no retry'
