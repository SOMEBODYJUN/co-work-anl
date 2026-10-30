"""Run six byte-preserved original entry points once; capture real stdout/stderr."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,subprocess,sys,time
BASE=Path(__file__).resolve().parent
ROOT=BASE/'original'
NAMES=('double_lpt','uniform_light_flow','two_light_potential','greedy_heaviest','nested_anchor','descent_trap')
def run(name):
    script=ROOT/'tests/audits'/('kfac_'+name+'.py')
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic()
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    result=subprocess.run([sys.executable,str(script)],cwd=ROOT,env=env,capture_output=True)
    for kind,data in (('stdout',result.stdout),('stderr',result.stderr)):
        (BASE/'replay'/(name+'.'+kind+'.txt')).write_bytes(data)
    return {'name':name,'script':str(script.relative_to(ROOT)),'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'command':[sys.executable,str(script)],'cwd':str(ROOT),'started_utc':start,'elapsed_seconds':time.monotonic()-clock,'exit_code':result.returncode,'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(result.stderr).hexdigest(),'stdout_bytes':len(result.stdout),'stderr_bytes':len(result.stderr)}
if __name__=='__main__':
    (BASE/'replay').mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        rows=list(pool.map(run,NAMES))
    (BASE/'replay/manifest.json').write_text(json.dumps({'python':sys.version,'python_executable':sys.executable,'PYTHONDONTWRITEBYTECODE':'1','jobs':rows},indent=2)+'\n')
    print(json.dumps(rows,indent=2))
    if any(r['exit_code'] for r in rows):sys.exit(1)
