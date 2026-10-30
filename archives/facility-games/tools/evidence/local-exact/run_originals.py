from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,subprocess,sys,time
BASE=Path(__file__).resolve().parent; ROOT=BASE/'original'; OUT=BASE/'replay';OUT.mkdir(exist_ok=True)
JOBS=[('threshold-dp',[str(ROOT/'facility_spe/exact/threshold_dp.py')]),('mitm-selftest',[str(ROOT/'facility_spe/exact/mitm.py'),'--self-test']),('hardness-exploration',[str(ROOT/'tests/audits/hardness_enum.py')]),('bounded-author-example',[str(ROOT/'facility_spe/exact/bounded_overlap.py'),str(BASE/'author-example-input.json')])]
def run(job):
 name,args=job;start=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.monotonic();proc=subprocess.run([sys.executable,*args],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True)
 for kind,data in [('stdout',proc.stdout),('stderr',proc.stderr)]: (OUT/(name+'.'+kind+'.txt')).write_bytes(data)
 return {'job':name,'command':[sys.executable,*args],'cwd':str(ROOT),'started_utc':start,'elapsed_seconds':time.monotonic()-tick,'exit_code':proc.returncode,'stdout_bytes':len(proc.stdout),'stderr_bytes':len(proc.stderr),'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(proc.stderr).hexdigest()}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(run,JOBS))
 (OUT/'manifest.json').write_text(json.dumps({'python':sys.version,'PYTHONDONTWRITEBYTECODE':'1','jobs':rows},indent=2)+'\n');print(json.dumps(rows,indent=2));sys.exit(any(r['exit_code'] for r in rows))
