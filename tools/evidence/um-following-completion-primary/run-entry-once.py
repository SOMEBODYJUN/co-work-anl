"""One fresh original-entry run per source; preserve real project path dependencies."""
from pathlib import Path
import json,hashlib,subprocess,os,sys,datetime,time
E=Path(__file__).resolve().parent
sid=sys.argv[1]
sources={s['id']:s for s in json.loads((E/'inventory-primary.json').read_text())}
s=sources[sid];folder=E/'runs'/sid;folder.mkdir(parents=True,exist_ok=False)
root=folder/'input-tree';root.mkdir();cwd=folder/'cwd';cwd.mkdir()
inputs=[]
def cp(src,relative,source_id,role):
    dst=root/relative;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(src.read_bytes())
    h=hashlib.sha256(dst.read_bytes()).hexdigest();inputs.append({'source_id':source_id,'path':str(dst),'relative_path':relative,'sha256':h,'role':role});return dst
entry=cp(E/'original'/f'{sid}.py',s['path'],sid,'primary original entry')
assert inputs[-1]['sha256']==s['sha256']
if sid=='7e9a28847d18f65c3e1a':
    cp(E/'support/1d119c87988eadadc643.py','tests/audits/unrelated_machines/rooted_dag_token_bridge.py','1d119c87988eadadc643','actual dynamic sibling dependency; only definitions/functions invoked, old main zero')
    cp(E/'support/a71bb7269384ec6a5cfe.md','research/current/unrelated_machines/large_bundle_collision_square_root_floor.md','a71bb7269384ec6a5cfe','actual runtime proof byte-read for SHA; not imported or executed')
argv=[sys.executable,str(entry)]
report=folder/'report.json'
if sid=='7e9a28847d18f65c3e1a':argv+=['--output',str(report)]
meta={'status':'running','source_id':sid,'entry_runs':1,'argv':argv,'cwd':str(cwd),'cwd_initially_empty':True,'input_aliases':inputs,'python':sys.version,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'network_calls':0,'bytecode_writes_disabled':True,'source_files_modified':False}
(folder/'execution.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
start=time.monotonic();r=subprocess.run(argv,cwd=cwd,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True)
(folder/'stdout.txt').write_bytes(r.stdout);(folder/'stderr.txt').write_bytes(r.stderr)
if r.returncode==0 and not report.exists():report.write_text(json.dumps(json.loads(r.stdout),ensure_ascii=False,indent=2)+'\n')
meta.update(status='completed',returncode=r.returncode,elapsed_seconds=time.monotonic()-start,stdout_sha256=hashlib.sha256(r.stdout).hexdigest(),stderr_sha256=hashlib.sha256(r.stderr).hexdigest(),inputs_unchanged_after_run=all(hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256'] for x in inputs))
(folder/'execution.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_id':sid,'returncode':r.returncode,'elapsed_seconds':meta['elapsed_seconds'],'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'report':str(report),'inputs_unchanged_after_run':meta['inputs_unchanged_after_run']}))
