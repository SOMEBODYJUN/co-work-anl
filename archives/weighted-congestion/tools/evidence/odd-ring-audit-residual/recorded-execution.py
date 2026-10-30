#!/usr/bin/env python3
import concurrent.futures,hashlib,json,subprocess,sys,tempfile,time
from pathlib import Path
B=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache')
OUT=B/'odd-ring-audit-residual-replay';OUT.mkdir(exist_ok=True)
rows=[('literal','tests/audits/weighted_congestion/odd_ring/verify.py',[],'verification.json'),('ring','tests/audits/weighted_congestion/odd_ring_linear/verify_ring.py',['--enumerate','--output','new-ring.json'],'new-ring.json'),('attack','tests/audits/weighted_congestion/odd_ring_linear/attack.py',['--enumerate'],None),('asymptotic','tests/audits/weighted_congestion/odd_ring_linear_audit/audit_checks.py',[],'audit_checks.json')]
def run(row):
 name,path,args,output=row;folder=Path(tempfile.mkdtemp(prefix=name+'-',dir=OUT));code=folder/Path(path).name;code.write_bytes((B/path).read_bytes());cmd=[sys.executable,str(code),*args];start=time.monotonic();x=subprocess.run(cmd,cwd=folder,capture_output=True,text=True,timeout=240);(OUT/(name+'-stdout.txt')).write_text(x.stdout);(OUT/(name+'-stderr.txt')).write_text(x.stderr)
 result={'name':name,'command':cmd,'working_directory':str(folder),'exit_code':x.returncode,'elapsed_seconds':time.monotonic()-start,'source_path':path,'source_sha256':hashlib.sha256(code.read_bytes()).hexdigest(),'unchanged_source':code.read_bytes()==(B/path).read_bytes()}
 if x.returncode==0:
  raw=(folder/output).read_bytes() if output else x.stdout.encode();parsed=json.loads(raw);(OUT/(name+'.json')).write_bytes(raw);result['output_json']=name+'.json'
 print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(run,rows))
(OUT/'runs.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
if any(x['exit_code'] or not x['unchanged_source'] for x in results):raise SystemExit(1)
