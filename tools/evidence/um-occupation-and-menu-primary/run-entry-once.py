"""Four standalone original main entries; one original library API probe, once each."""
from pathlib import Path
import json,hashlib,subprocess,sys,os,time,datetime
E=Path(__file__).resolve().parent;sid=sys.argv[1]
sources={s['id']:s for s in json.loads((E/'inventory-primary.json').read_text())};s=sources[sid]
folder=E/'runs'/sid;folder.mkdir(parents=True,exist_ok=False);root=folder/'input-tree';root.mkdir();cwd=folder/'cwd';cwd.mkdir()
inputs=[]
def cp(src,rel,source_id,role):
 p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(src.read_bytes());inputs.append({'source_id':source_id,'relative_path':rel,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':role});return p
original=cp(E/'original'/f'{sid}.py',s['path'],sid,'byte-exact primary original')
assert inputs[0]['sha256']==s['sha256']
library=sid=='46554c947efcae1aa3e7'
if library:
 probe=cp(E/'check-core-apis.py','probe/check-core-apis.py','new-api-probe','hand-solvable API checks, no original main')
 argv=[sys.executable,str(probe),str(original)]
else:argv=[sys.executable,str(original)]
meta={'status':'running','source_id':sid,'original_main_entries':0 if library else 1,'api_probe_runs':1 if library else 0,'definition_only_library_imports':1 if library else 0,'argv':argv,'cwd':str(cwd),'cwd_initially_empty':True,'input_aliases':inputs,'python':sys.version,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytecode_writes_disabled':True,'network_calls':0,'source_files_modified':False}
(folder/'execution.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');start=time.monotonic()
r=subprocess.run(argv,cwd=cwd,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True)
(folder/'stdout.txt').write_bytes(r.stdout);(folder/'stderr.txt').write_bytes(r.stderr)
if r.returncode==0:(folder/'report.json').write_text(json.dumps(json.loads(r.stdout),ensure_ascii=False,indent=2)+'\n')
meta.update(status='completed',returncode=r.returncode,elapsed_seconds=time.monotonic()-start,stdout_sha256=hashlib.sha256(r.stdout).hexdigest(),stderr_sha256=hashlib.sha256(r.stderr).hexdigest(),inputs_unchanged_after_run=all(hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256'] for a in inputs))
(folder/'execution.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_id':sid,'original_main_entries':meta['original_main_entries'],'api_probe_runs':meta['api_probe_runs'],'returncode':r.returncode,'elapsed_seconds':meta['elapsed_seconds'],'stderr_bytes':len(r.stderr),'inputs_unchanged_after_run':meta['inputs_unchanged_after_run']}))
