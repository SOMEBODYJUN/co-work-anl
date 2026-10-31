from pathlib import Path
import hashlib,json,os,platform,subprocess,sys,time

S=Path(__file__).resolve().parents[4]
E=S/'archives/customer-attraction/tools/evidence/count-markov-probes-primary'
SUB=Path('research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/strategy_duality')
name=sys.argv[1]
config={
 'count':{'file':'count_markov_probe.py','args':[],'seed':1001,'input':'128 exhaustive binary 7-type vectors; then 10000 RNG vectors of 7 integers in range(8); fixed players=3/topics=3','timeout':300},
 'fresh':{'file':'fresh_markov_probe.py','args':[],'seed':786,'input':'up to 1000 no-repeat auxiliary subset-potential games; players=3/topics=6; values range(10) on all size2/size3 subsets; cap=1000000; stops first mismatch','timeout':180},
 'generic':{'file':'markov_generic_probe.py','args':[],'seed':1001,'input':'default --players4 --topics3 --trials500; 7 nonnegative integer CAG types range(8); cap=1000000; stops first mismatch','timeout':180}
}[name]
out=E/f'replay-{name}'
out.mkdir(parents=True,exist_ok=True)
guard=out/'started.json'
if guard.exists():raise SystemExit('Already started: no repeat permitted')
data=(E/'original'/SUB/config['file']).read_bytes()
tree=E/f'replay-{name}-tree';src=tree/SUB/config['file'];src.parent.mkdir(parents=True,exist_ok=True);src.write_bytes(data)
command=[sys.executable,str(src),*config['args']]
meta={'command':command,'cwd':str(tree),'original_entry_runs_this_batch':1,'python':platform.python_version(),
      'source_sha256':hashlib.sha256(data).hexdigest(),'runtime_code_files':1,'external_input_files':0,
      'dependency_scope':'Python standard library only; built-in deterministic generator is the real input',
      'seed':config['seed'],'input_contract':config['input'],'timeout_seconds':config['timeout'],
      'solver_calls':0,'started_unix':time.time(),'PYTHONHASHSEED':'0'}
guard.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
t=time.monotonic()
try:
    q=subprocess.run(command,cwd=tree,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'},
                     capture_output=True,timeout=config['timeout'])
    stdout,stderr=q.stdout,q.stderr;meta.update(returncode=q.returncode,timed_out=False)
except subprocess.TimeoutExpired as exc:
    stdout,stderr=exc.stdout or b'',exc.stderr or b'';meta.update(returncode=None,timed_out=True)
meta.update(wall_seconds=time.monotonic()-t,stdout_bytes=len(stdout),stderr_bytes=len(stderr),
            source_unchanged=src.read_bytes()==data)
(out/'stdout.txt').write_bytes(stdout);(out/'stderr.txt').write_bytes(stderr)
(out/'execution.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(meta,ensure_ascii=False));print(stdout.decode())
