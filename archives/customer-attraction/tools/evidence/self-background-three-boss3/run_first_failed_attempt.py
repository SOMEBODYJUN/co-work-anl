from pathlib import Path
import sys,subprocess,json,time,hashlib,platform,os
from datetime import datetime,timezone
import numpy,scipy
B=Path(__file__).resolve().parent.parent
S=Path(__file__).resolve().parent
R=B/'self_background_runtime'
p=R/'research/workspaces/customer-attraction/R-5dbadd913a00492e994a6cfca3ec53fc/continuation/self_background_probe.py'
assert not (p.parent/'signed_self_background_probe.json').exists()
start=datetime.now(timezone.utc).isoformat();tick=time.monotonic()
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
r=subprocess.run([sys.executable,str(p)],cwd=R,env=env,text=True,capture_output=True)
D=S/'replay';D.mkdir(exist_ok=True)
(D/'stdout.txt').write_text(r.stdout);(D/'stderr.txt').write_text(r.stderr)
output=p.parent/'signed_self_background_probe.json'
if output.exists():(D/'signed_self_background_probe.json').write_bytes(output.read_bytes())
record={'event':'one unmodified original entry subprocess on explicit21 canonical Instance inputs','command':[sys.executable,str(p)],'cwd':str(R),'start_utc':start,'elapsed_seconds':time.monotonic()-tick,'exit_code':r.returncode,'original_entry_calls':1,'unsigned_entry_calls':0,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'Python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,'assertions_enabled':__debug__,'output_file_exists':output.exists(),'stdout_bytes':len(r.stdout.encode()),'stderr_bytes':len(r.stderr.encode()),'runtime_Instances':21,'schema_exclusions':1,'scope':'new event; no historical identity claimed; exact negative primal or dual certification not added'}
(D/'execution-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2))
if output.exists():print(output.read_text())
assert r.returncode==0
