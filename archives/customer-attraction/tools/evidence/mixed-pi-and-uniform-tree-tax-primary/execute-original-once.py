"""One original entry per fresh mode tree; passive original observations only."""
from pathlib import Path
import argparse,ast,contextlib,datetime,hashlib,json,os,platform,runpy,shutil,sys,time,traceback
p=argparse.ArgumentParser();p.add_argument('mode',choices=['pi-review','tree-tax']);mode=p.parse_args().mode
E=Path(__file__).resolve().parent;M=json.loads((E/'source-manifest.json').read_text());D=json.loads((E/'dependency-manifest.json').read_text());src=next(x for x in M if x['id']==('44d4846cdced71831d39'if mode=='pi-review'else'fb207f64371ab9ed8442'));out=E/'replay'/mode;out.mkdir(parents=True,exist_ok=False);root=out/'source-root';root.mkdir();program=root/src['path'];program.parent.mkdir(parents=True);shutil.copyfile(E/'original'/src['path'],program);inputs=[x for x in D if x['used_by']==mode]
for x in inputs:
 p=root/x['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(E/'dependencies'/x['path'],p);assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
assert hashlib.sha256(program.read_bytes()).hexdigest()==src['sha256']
tree=ast.parse(program.read_text());ob={'scope':'passive events of originally executed source plus returned namespace; zero extra original function calls','main_calls':0};node_records={};path_records={};root_leaves={};raw_events={'nodes':0,'paths':0,'root_leaves':0}
if mode=='tree-tax':
 nodeline=next(n.lineno for n in ast.walk(tree)if isinstance(n,ast.AugAssign)and isinstance(n.target,ast.Name)and n.target.id=='positive')
 pathline=next(n.lineno for n in ast.walk(tree)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='max_path_slack'for t in n.targets)and isinstance(n.value,ast.IfExp))
 taxline=next(n.lineno for n in ast.walk(tree)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='tax'for t in n.targets))
else:
 ob['source_packet_subscript_fields']=sorted({n.slice.value for n in ast.walk(tree)if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id=='packet'and isinstance(n.slice,ast.Constant)})
def add(target,key,value):
 if key in target:assert target[key]==value
 else:target[key]=value
def tr(frame,event,arg):
 if frame.f_code.co_filename!=str(program):return None
 name=frame.f_code.co_name;v=frame.f_locals
 if mode=='pi-review'and name=='main':
  if event=='call':ob['main_calls']+=1
  if event=='return'and'report'in v:
   ob.update({'unit_customers':len(v['clients']),'histories':[list(h)for h in sorted(v['histories'],key=lambda h:(len(h),h))],'exact_IC_gaps':list(map(str,v['gaps'])),'actual':list(v['actual']),'actual_u':list(map(str,v['utilities'])),'table_sizes':{k:len(t)for k,t in v['tables'].items()},'root_branches':v['root_branches'],'P3_maximizers':v['maximizers'][3],'P4_maximizers':v['maximizers'][4],'K':v['root_K'],'actual_column_caps':v['caps'],'main_original_report':v['report']})
  return tr
 if mode=='tree-tax'and name=='<module>':
  if event=='line'and frame.f_lineno in [nodeline,pathline,taxline]:
   key=(v['core'],str(v['lam']),tuple(v['h']))
   if frame.f_lineno==nodeline:
    raw_events['nodes']+=1;add(node_records,key,{'core':v['core'],'lambda':str(v['lam']),'history':list(v['h']),'leaf':list(v['z']),'current_tax':str(v['tax']),'regret':str(v['r']),'candidate_nonnegative_regrets':list(map(str,v['regrets']))})
   elif frame.f_lineno==pathline:
    raw_events['paths']+=1;add(path_records,key,{'core':v['core'],'lambda':str(v['lam']),'history':list(v['h']),'leaf':list(v['z']),'path_regret':str(v['path_regret']),'future_tax':str(v['future_tax']),'full_tax':str(v['full_tax']),'core_tax_per_role':str(v['core_tax']),'noncore_future_tax':str(v['future_tax']-(v['m']-len(v['h']))*v['core_tax']),'refund_minus_path_regret':str(v['slack']),'H':str(v['H']),'HJ':str(v['HJ'])})
   elif len(v['h'])==1:
    raw_events['root_leaves']+=1;key=(v['core'],str(v['lam']),v['root']);add(root_leaves,key,{'core':v['core'],'lambda':str(v['lam']),'root_action':v['root'],'leaf':list(v['z'])})
  return tr
 return None
oldcwd=Path.cwd();oldargv=sys.argv[:];oldtrace=sys.gettrace();sys.dont_write_bytecode=True;start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();rc=0;ns={}
try:
 os.chdir(root);sys.argv=[str(program)]
 with(out/'stdout.txt').open('w')as so,(out/'stderr.txt').open('w')as se,contextlib.redirect_stdout(so),contextlib.redirect_stderr(se):
  try:sys.settrace(tr);ns=runpy.run_path(str(program),run_name='__main__')
  except BaseException:rc=1;traceback.print_exc()
  finally:sys.settrace(oldtrace)
finally:os.chdir(oldcwd);sys.argv=oldargv
if mode=='tree-tax'and ns:
 ob.update({'raw_observed_line_events':raw_events,'unique_node_records':list(node_records.values()),'unique_prescribed_path_records':list(path_records.values()),'forced_root_leaves':list(root_leaves.values()),'source_original_report':ns['out'],'empty_root_IC_assertions_executed':0,'provided_empty_root_action':ns['actions'][()],'provided_terminal_counts':ns['cert']['terminal_counts'],'base_unit_count':len(ns['base'])})
(out/'passive-observation.json').write_text(json.dumps(ob,ensure_ascii=False,default=str,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
name='pi_review_audit.json'if mode=='pi-review'else'uniform_tree_tax_exact.json';report=program.parent/name;old=next(x for x in M if x['path'].endswith('/'+name));state={'mode':mode,'source_id':src['id'],'source_invocations':1,'source_sha256':sha(program),'source_bytes':program.stat().st_size,'start_utc':start,'duration_seconds':time.monotonic()-t,'source_argv':[str(program)],'cwd':str(root),'python':sys.version,'executable':sys.executable,'optimize':sys.flags.optimize,'platform':platform.platform(),'returncode':rc,'true_file_inputs':[{'id':x['id'],'path':x['path'],'sha256':x['sha256']}for x in inputs],'local_program_imports':[],'third_party_libraries':[],'entry':'runpy original __main__; source main guard invokes main once'if mode=='pi-review'else'runpy original top-level with no main guard or CLI','physical_path_difference':'fresh independent source-root with unchanged repo-relative paths, not author physical root','output_path':str(report.relative_to(E)),'output_bytes':report.stat().st_size if report.exists()else None,'output_sha256':sha(report)if report.exists()else None,'output_equals_frozen_bytes':report.exists()and report.read_bytes()==(E/'original'/old['path']).read_bytes(),'stdout_bytes':(out/'stdout.txt').stat().st_size,'stderr_bytes':(out/'stderr.txt').stat().st_size,'stdout_equals_output_bytes':report.exists()and report.read_bytes()==(out/'stdout.txt').read_bytes(),'extra_original_function_calls':0,'side_effect':'original fixed-name write_text output only in fresh HERE; frozen reports separate; bytecode disabled'}
(out/'execution.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');print(json.dumps(state,ensure_ascii=False));assert rc==0,'original failure retained, no retry'
