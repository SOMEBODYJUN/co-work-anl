from pathlib import Path
import sys,json,hashlib,subprocess,time,os,platform
c=Path(__file__).resolve().parent;label=sys.argv[1];base=c/'root-jk-replay';layout=base/'source-root'
entry=layout/'research/workspaces/customer-attraction/R-324fbf8f72b041578583b51189f13d1a'/('residual_deficit_padding_audit.py'if label=='audit'else'residual_deficit_padding_probe.py')
run=base/('run-'+label+'-001');assert not run.exists();run.mkdir(parents=True);cmd=[sys.executable,str(entry),'--output',str(run/'report.json')]
if label=='probe':cmd+=['--leaves','6']
env=os.environ.copy();env['PYTHONPATH']=str(layout);start=time.monotonic();p=subprocess.run(cmd,cwd=layout,env=env,capture_output=True);elapsed=time.monotonic()-start
(run/'stdout.txt').write_bytes(p.stdout);(run/'stderr.txt').write_bytes(p.stderr)
meta={'command':cmd,'cwd':str(layout),'PYTHONPATH':str(layout),'python_version':platform.python_version(),'assertions_enabled':__debug__,'exit_code':p.returncode,'elapsed_seconds':elapsed,'entry_sha256':hashlib.sha256(entry.read_bytes()).hexdigest(),'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr),'original_code_unmodified':True,'this_original_CLI_execution_count':1,'new_independent_implementation':False}
if p.returncode==0:
 fresh=json.loads((run/'report.json').read_text());old=json.loads((c/'root-jk-original-source'/('residual_deficit_padding_audit.json'if label=='audit'else'residual_deficit_padding_k6.json')).read_text());timing='runtime_seconds'if label=='audit'else'runtime';fresh.pop(timing);old.pop(timing);meta['all_nonruntime_JSON_fields_equal_frozen']=fresh==old;meta['nonruntime_differing_keys']=[k for k in set(fresh)|set(old)if fresh.get(k)!=old.get(k)];meta['report_sha256']=hashlib.sha256((run/'report.json').read_bytes()).hexdigest()
(run/'run-metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(json.dumps(meta),flush=True);sys.exit(p.returncode)
