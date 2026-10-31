from pathlib import Path
import sys,subprocess,json,hashlib,time,platform
c=Path(__file__).resolve().parent;label=sys.argv[1];base=c/'root-jd-replay';layout=base/'source-root'
entry=layout/'research/workspaces/customer-attraction/R-324fbf8f72b041578583b51189f13d1a'/('seat_spectrum_audit.py'if label=='seats'else'terminal_menu_audit.py')
run=base/('run-'+label+'-001');assert not run.exists();run.mkdir(parents=True)
args=[sys.executable,str(entry)]
if label=='seats':args+=['--output',str(run/'report.json')]
t=time.monotonic();p=subprocess.run(args,cwd=layout,capture_output=True);elapsed=time.monotonic()-t
(run/'stdout.txt').write_bytes(p.stdout);(run/'stderr.txt').write_bytes(p.stderr)
meta={'command':args,'cwd':str(layout),'python_version':platform.python_version(),'assertions_enabled':__debug__,'exit_code':p.returncode,'elapsed_seconds':elapsed,'entry_sha256':hashlib.sha256(entry.read_bytes()).hexdigest(),'stdout_bytes':len(p.stdout),'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_bytes':len(p.stderr),'original_entry_unmodified':True,'new_independent_implementation':False,'execution_count_for_this_source_this_JD_batch':1}
if label=='seats'and p.returncode==0:
 original=next(x for x in json.loads((c/'root-ix-next-local-inputs/local-export-manifest.json').read_text())['rows']if x['id']=='146b0601a95316cd06a1')
 meta['report_matches_frozen_1466_bytes']=(run/'report.json').read_bytes()==Path(original['local_path']).read_bytes()
(run/'run-metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(json.dumps(meta),flush=True)
sys.exit(p.returncode)
