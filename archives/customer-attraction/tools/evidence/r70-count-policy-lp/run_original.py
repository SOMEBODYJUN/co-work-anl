"""One unmodified original main, six-trial prefix, read-only return observer."""
import contextlib, gzip, hashlib, io, json, platform, runpy, shutil, sys, time
from pathlib import Path
import numpy as np
import scipy

HERE=Path(__file__).resolve().parent
SOURCE=Path('/workspace/scratch/c0ab78c47566/round16-r70-count-policy-original.py')
HISTORICAL=Path('/workspace/scratch/c0ab78c47566/round16-r70-count-policy-result.json')
RUNTIME=HERE/'runtime'; RUNTIME.mkdir(exist_ok=True)
TARGET=RUNTIME/'count_policy_lp.py'
shutil.copyfile(SOURCE,TARGET)
expected='f79ac9370ec22954ba8ab081a8f1a2a2723d7d71159df8a45a50d592233c9ff4'
assert hashlib.sha256(TARGET.read_bytes()).hexdigest()==expected
argv=[str(TARGET),'--trials','6','--seed','28491','--output',str(RUNTIME/'result.json')]
capture={'counts':{},'solve_policy':[],'policy_lp':[],'linprog':[]}
last_matrix=None

def arr_digest(a):
    a=np.asarray(a,dtype=np.float64)
    return {'shape':list(a.shape),'float64_c_sha256':hashlib.sha256(a.tobytes(order='C')).hexdigest()}

def observe(frame,event,arg):
    global last_matrix
    name=frame.f_code.co_name
    path=Path(frame.f_code.co_filename)
    if event=='call' and path==TARGET:
        capture['counts'][name]=capture['counts'].get(name,0)+1
    if event!='return': return
    v=frame.f_locals
    if path==TARGET and name=='solve_policy':
        capture['solve_policy'].append({'weights':v['weights'].tolist(),'jitter':v['jitter'],
                                       'action':arg[0].tolist(),'outcome':arg[1].tolist()})
    elif path==TARGET and name=='policy_lp':
        capture['policy_lp'].append({'best_gap':float(arg[0]),'omit':int(arg[1]),'weights':arg[2].tolist(),
                                    'actual_terminal_index':int(arg[3]),'matrix':arr_digest(v['Aub'])})
        last_matrix=v['Aub'].tolist()
    elif name=='linprog' and path.name=='_linprog.py':
        capture['linprog'].append({'c':v['c'].tolist(),'A_ub':arr_digest(v['A_ub']),
                                  'b_ub':arr_digest(v['b_ub']),'A_eq':np.asarray(v['A_eq']).tolist(),
                                  'b_eq':np.asarray(v['b_eq']).tolist(),
                                  'success':bool(arg.success),'status':int(arg.status),'message':arg.message,
                                  'fun':None if arg.fun is None else float(arg.fun),
                                  'x':None if arg.x is None else arg.x.tolist()})

stdout,stderr=io.StringIO(),io.StringIO()
oldargv=sys.argv;begin=time.perf_counter();sys.argv=argv
try:
    with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
        sys.setprofile(observe)
        runpy.run_path(str(TARGET),run_name='__main__')
finally:
    sys.setprofile(None);sys.argv=oldargv
elapsed=time.perf_counter()-begin
assert capture['counts']['main']==1 and len(capture['policy_lp'])==6 and len(capture['linprog'])==42
assert all(x['success'] for x in capture['linprog'])
capture['last_policy_A_ub']=last_matrix
data=(json.dumps(capture,separators=(',',':'))+'\n').encode()
with (HERE/'capture.json.gz').open('wb') as out:
    with gzip.GzipFile(fileobj=out,mode='wb',mtime=0) as z:z.write(data)
(HERE/'stdout.txt').write_text(stdout.getvalue());(HERE/'stderr.txt').write_text(stderr.getvalue())
result=(RUNTIME/'result.json').read_bytes()
event={'kind':'one original unmodified main with --trials 6; read-only profiler; not default 50-trial replay',
       'argv':argv,'elapsed_seconds':elapsed,'exit_code':0,'python':platform.python_version(),
       'numpy':np.__version__,'scipy':scipy.__version__,'counts':capture['counts'],
       'LP_calls':len(capture['linprog']),'LP_successes':sum(x['success'] for x in capture['linprog']),
       'source_before_sha256':expected,'source_after_sha256':hashlib.sha256(TARGET.read_bytes()).hexdigest(),
       'historical_result_sha256':hashlib.sha256(HISTORICAL.read_bytes()).hexdigest(),
       'new_result_sha256':hashlib.sha256(result).hexdigest(),'byte_identical_to_historical':result==HISTORICAL.read_bytes(),
       'capture_uncompressed_bytes':len(data),'capture_uncompressed_sha256':hashlib.sha256(data).hexdigest(),
       'capture_gzip_sha256':hashlib.sha256((HERE/'capture.json.gz').read_bytes()).hexdigest(),
       'stdout':stdout.getvalue(),'stderr':stderr.getvalue()}
(HERE/'execution.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(event,ensure_ascii=False))
