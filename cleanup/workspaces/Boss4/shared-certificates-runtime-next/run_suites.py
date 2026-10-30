import pathlib,subprocess,json,time,os,concurrent.futures,sys
root=pathlib.Path('tools/evidence/shared-certificates-runtime').resolve();cwd=root/'replay';out=root/'execution';out.mkdir(exist_ok=True)
suites={
'four-seed':['python3','-B','tests/test_four_seed.py','--report',str(out/'four-seed-report.json')],
'shared-phi':['python3','-B','tests/test_shared_phi.py','--report',str(out/'shared-phi-report.json')],
'shared-offdiag':['python3','-B','tests/test_shared_offdiag.py','-v'],
'verify-phi':['python3','-B','tests/test_verify_phi.py','-v']}
def run(item):
    name,cmd=item;start=time.time();env=dict(os.environ);env['PYTHONPATH']=str(cwd);env['PYTHONDONTWRITEBYTECODE']='1'
    r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True)
    (out/(name+'.stdout.txt')).write_text(r.stdout);(out/(name+'.stderr.txt')).write_text(r.stderr)
    rec={'name':name,'command':cmd,'cwd':str(cwd),'exit_code':r.returncode,'elapsed_seconds':time.time()-start,'stdout_path':str(out/(name+'.stdout.txt')),'stderr_path':str(out/(name+'.stderr.txt')),'source_unmodified':True}
    (out/(name+'.execution.json')).write_text(json.dumps(rec,indent=2)+'\n');print(name,r.returncode,r.stdout,r.stderr[-1200:],flush=True);return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records=list(pool.map(run,suites.items()))
(out/'suite-executions.json').write_text(json.dumps(records,indent=2)+'\n')
sys.exit(any(r['exit_code'] for r in records))
