"""Exact top-level program once via runpy; snapshot returned globals without extra original function calls."""
from pathlib import Path
import contextlib,hashlib,importlib.metadata,json,os,platform,runpy,shutil,sys,time,traceback
E=Path(__file__).resolve().parent;rows=json.loads((E/'source-manifest.json').read_text());src=next(x for x in rows if x['path'].endswith('diagnose_direct_floor.py'));old=next(x for x in rows if x['path'].endswith('diagnose_direct_floor.json'));replay=E/'replay-floor';replay.mkdir(exist_ok=False);root=replay/'source-root';root.mkdir();program=root/src['path'];program.parent.mkdir(parents=True);shutil.copyfile(E/'original'/src['path'],program);previous=Path.cwd();argv=sys.argv[:];start=time.time();exit_code=0;ns={}
try:
 os.chdir(root);sys.argv=[str(program)]
 with (replay/'original.stdout.txt').open('w')as out,(replay/'original.stderr.txt').open('w')as err:
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
   try:ns=runpy.run_path(str(program),run_name='__main__')
   except BaseException:exit_code=1;traceback.print_exc()
finally:os.chdir(previous);sys.argv=argv
if ns:
 res=ns['res'];proposal={'success':bool(res.success),'status':int(res.status),'message':str(res.message),'fun':float(res.fun),'nit':int(res.nit),'x_float':list(map(float,res.x)),'x_float_hex':[float(x).hex()for x in res.x]}
 for key in ['slack','con']:
  if key in res:proposal[key]=list(map(float,res[key]))
 for key in ['ineqlin','eqlin','lower','upper']:
  if key in res:proposal[key]={k:list(map(float,v))for k,v in res[key].items()}
 snapshot={'scope':'copy of returned original top-level namespace; no extra action/follow/utility/cov or LP calls','M':ns['M'],'K':ns['K'],'MASKS':list(ns['MASKS']),'HISTORIES':[list(h)for h in ns['HISTORIES']],'ROWS':[[str(v)for v in row]for row in ns['ROWS']],'OBJ':[str(v)for v in ns['OBJ']],'actual_path':list(ns['Z']),'comparison':list(ns['comparison']),'lp_proposal':proposal,'rational_point':list(map(str,ns['point'])),'common_denominator':ns['den'],'counts':ns['counts'],'exact_slacks':list(map(str,ns['slacks'])),'nonzero_customers':ns['customers'],'root':str(ns['root']),'payoffs':list(map(str,ns['payoffs'])),'opt':ns['opt'],'original_output_object':ns['out']}
 (replay/'complete-original-built-input-and-proposal.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report=program.with_suffix('.json');state={'original_program_calls':1,'execution_count':1,'method':'runpy.run_path exact original top-level bytes with __main__, capture returned namespace only; no extra original source function calls','argv':[str(program)],'cwd':str(root),'program':src['path'],'program_bytes':program.stat().st_size,'program_sha256':sha(program),'python':sys.version,'executable':sys.executable,'optimize':sys.flags.optimize,'platform':platform.platform(),'runtime_libraries':{n:importlib.metadata.version(n)for n in ['numpy','scipy']},'exit_code':exit_code,'duration_seconds':time.time()-start,'stdout_bytes':(replay/'original.stdout.txt').stat().st_size,'stderr_bytes':(replay/'original.stderr.txt').stat().st_size,'external_file_inputs':[],'local_program_imports':[],'source_side_effect':'No main guard; complete module top-level LP, exact IC/OPT postcheck and adjacent .json write_text overwrite. New empty mirror root preserves frozen originals.','path_difference':'same original repo-relative path inside independent source-root, different physical root','report_created':report.exists()}
if report.exists():state.update({'report_bytes':report.stat().st_size,'report_sha256':sha(report),'equals_frozen_bytes':report.read_bytes()==(E/'original'/old['path']).read_bytes(),'stdout_equals_report_bytes':(replay/'original.stdout.txt').read_bytes()==report.read_bytes()})
(replay/'execution-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');print(json.dumps(state,ensure_ascii=False));assert exit_code==0,'Failure preserved, no automatic retry'
