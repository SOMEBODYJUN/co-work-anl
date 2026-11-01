from pathlib import Path
import subprocess,sys,time,json,hashlib,platform
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
S=Path(__file__).resolve().parent;R=S.parent/'independent_ranks_runtime'
folder=R/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/independent_attack'
def run(name):
 p=folder/name;dest=S/'replay'/p.stem;dest.mkdir(parents=True,exist_ok=True)
 t=time.monotonic();start=datetime.now(timezone.utc).isoformat()
 result=subprocess.run([sys.executable,'-I','-B',str(p)],cwd=R,text=True,capture_output=True)
 (dest/'stdout.txt').write_text(result.stdout);(dest/'stderr.txt').write_text(result.stderr)
 event={'event':'one new unmodified standard-library original entry; not historical event identity','source':name,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'command':[sys.executable,'-I','-B',str(p)],'cwd':str(R),'start_utc':start,'elapsed_seconds':time.monotonic()-t,'exit_code':result.returncode,'Python':platform.python_version(),'assertions_enabled':True,'original_entry_calls':1,'LP_calls':0,'canonical_imports':0,'stdout_bytes':len(result.stdout.encode()),'stderr_bytes':len(result.stderr.encode())}
 (dest/'execution-record.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
 assert result.returncode==0,(name,result.stderr)
 parsed=json.loads(result.stdout);(dest/'parsed-output.json').write_text(json.dumps(parsed,ensure_ascii=False,indent=2)+'\n')
 return {'source':name,'event':event,'output':parsed}
with ThreadPoolExecutor(max_workers=3)as pool:
 for result in pool.map(run,['check_fixed_rank.py','check_rank_one.py','check_repeated_last.py']):print(json.dumps(result,ensure_ascii=False,indent=2))
