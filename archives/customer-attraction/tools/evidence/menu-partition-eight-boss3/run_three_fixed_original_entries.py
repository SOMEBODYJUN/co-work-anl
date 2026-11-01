from pathlib import Path
import subprocess,sys,time,json,hashlib,platform
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
S=Path(__file__).resolve().parent;R=S.parent/'menu_partition_runtime';BASE=R/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_boss'
cases=[('menu-exclusion',BASE/'audit_menu_exclusion.py',[],S/'original/menu_exclusion_audit.json'),('partition-127',BASE/'partition_attack/exact_audit.py',[],S/'original/exact_witness.json'),('partition-14',BASE/'partition_attack/exact_audit.py',['--source','integer_simplification.json'],S/'original/small_exact_witness.json')]
def run(case):
 name,script,args,frozen=case;D=S/'replay'/name;D.mkdir(parents=True,exist_ok=True);tick=time.monotonic();start=datetime.now(timezone.utc).isoformat()
 cmd=[sys.executable,'-I','-B',str(script),*args];r=subprocess.run(cmd,cwd=R,text=True,capture_output=True)
 (D/'stdout.txt').write_text(r.stdout);(D/'stderr.txt').write_text(r.stderr)
 event={'event':'new unmodified original fixed-input entry; not historical process identity','command':cmd,'source_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'cwd':str(R),'start_utc':start,'elapsed_seconds':time.monotonic()-tick,'exit_code':r.returncode,'Python':platform.python_version(),'assertions_enabled':True,'original_entry_calls':1,'canonical_imports':0,'LP_calls':0,'discovery_probe_calls':0,'stdout_bytes':len(r.stdout.encode()),'stderr_bytes':len(r.stderr.encode()),'frozen_report_bytes_equal':r.stdout.encode()==frozen.read_bytes(),'frozen_report_all_fields_equal':json.loads(r.stdout)==json.loads(frozen.read_text())if r.returncode==0 else False,'frozen_report_sha256':hashlib.sha256(frozen.read_bytes()).hexdigest()}
 (D/'execution-record.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n');assert r.returncode==0,(name,r.stderr)
 (D/'parsed-output.json').write_text(json.dumps(json.loads(r.stdout),ensure_ascii=False,indent=2)+'\n');assert event['frozen_report_all_fields_equal']
 return {'case':name,'event':event}
with ThreadPoolExecutor(max_workers=3)as pool:
 for x in pool.map(run,cases):print(json.dumps(x,ensure_ascii=False,indent=2))
