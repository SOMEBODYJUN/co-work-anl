"""One unchanged tax_probe main with passive capture of its fifteen LPs."""
from pathlib import Path
from contextlib import redirect_stdout,redirect_stderr
from collections import Counter
import hashlib,json,platform,runpy,sys,time,traceback,gzip
import numpy,scipy

BASE=Path(__file__).resolve().parent
SOURCE=Path('/workspace/scratch/c0ab78c47566/round15-tax-probe.py')
RUNTIME=BASE/'runtime';OUT=BASE/'replay'
assert not RUNTIME.exists() and not OUT.exists()
RUNTIME.mkdir();OUT.mkdir()
SCRIPT=RUNTIME/'tax_probe.py';SCRIPT.write_bytes(SOURCE.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SCRIPT)=='8f72ad4dc8464ef17883bce8f273faefe55152dd31b35aeee136c8bcf3579e21'
calls=Counter();records=[];pending={};shared=None

def observe(frame,event,arg):
    global shared
    if frame.f_code.co_filename==str(SCRIPT) and event=='call':
        if frame.f_code.co_name in ('<module>','optimize','terminal'):calls[frame.f_code.co_name]+=1
    if frame.f_code.co_name!='linprog' or not frame.f_code.co_filename.endswith('/scipy/optimize/_linprog.py'):return
    if event=='call':
        parent=frame.f_back;assert parent.f_code.co_filename==str(SCRIPT)
        p=parent.f_locals;a=frame.f_locals
        matrix={'A_ub':a['A_ub'].tolist(),'b_ub':a['b_ub'].tolist(),'A_eq':a['A_eq'].tolist(),'b_eq':a['b_eq'],'bounds':a['bounds'],'method':a['method']}
        if shared is None:shared=matrix
        else:assert shared==matrix
        pending[id(frame)]={'portfolio':list(p['cc']),'c':a['c'].tolist()}
    elif event=='return':
        rec=pending.pop(id(frame))
        def arr(value):return None if value is None else value.tolist()
        rec['result']={'success':bool(arg.success),'status':int(arg.status),'message':str(arg.message),'fun':None if arg.fun is None else float(arg.fun),'x':arr(arg.x),'nit':int(arg.nit),'inequality_marginals':arr(arg.ineqlin.marginals),'equality_marginals':arr(arg.eqlin.marginals),'lower_marginals':arr(arg.lower.marginals)}
        records.append(rec)

before=sha(SCRIPT);tick=time.perf_counter();error=None;exit_code=0;namespace=None
sys.argv=[str(SCRIPT)]
with (OUT/'stdout.txt').open('w') as stdout,(OUT/'stderr.txt').open('w') as stderr:
    try:
        with redirect_stdout(stdout),redirect_stderr(stderr):
            sys.setprofile(observe)
            namespace=runpy.run_path(str(SCRIPT),run_name='__main__')
    except BaseException:
        error=traceback.format_exc();exit_code=1;stderr.write(error)
    finally:sys.setprofile(None)
elapsed=time.perf_counter()-tick
assert not pending
capture={'scope':'Passive capture of one unchanged original main, no second optimize or LP call.','function_calls':dict(calls),'lp_calls':len(records),'shared_LP_constraints':shared,'LP_records':records}
if namespace is not None:
    ns=namespace
    capture['source_globals']={'n':ns['n'],'k':ns['k'],'masks':ns['masks'],'seed':ns['seed'],'sigma':[{'history':list(h),'action':a} for h,a in ns['sigma'].items()]}
    capture['optimize_return']={'best_fun':float(ns['f']),'best_portfolio':list(ns['cc']),'root':list(ns['z']),'gamma':[[str(x) for x in row] for row in ns['g']]}
    capture['main_reconstruction']={'weights':ns['wi'],'common_denominator':ns['den'],'normalized_rational_weights':{str(m):str(x) for m,x in ns['ws'].items()},'all_gamma_values':[str(x) for x in ns['vals']]}
raw=(json.dumps(capture,indent=2)+'\n').encode()
(OUT/'capture.json.gz').write_bytes(gzip.compress(raw,mtime=0))
event={'source_id':'17182ac367b77ce669e6','event':'one unchanged original main via runpy and read-only sys.setprofile','argv':[str(SCRIPT)],'source_sha256_before':before,'source_sha256_after':sha(SCRIPT),'exit_code':exit_code,'exception':error,'elapsed_seconds':elapsed,'python':sys.version,'numpy':numpy.__version__,'scipy':scipy.__version__,'platform':platform.platform(),'source_module_calls':calls['<module>'],'source_optimize_calls':calls['optimize'],'source_terminal_calls':calls['terminal'],'LP_calls':len(records),'capture_uncompressed_bytes':len(raw),'capture_uncompressed_sha256':hashlib.sha256(raw).hexdigest(),'capture_gzip_sha256':sha(OUT/'capture.json.gz'),'stdout_bytes':(OUT/'stdout.txt').stat().st_size,'stdout_sha256':sha(OUT/'stdout.txt'),'stderr_bytes':(OUT/'stderr.txt').stat().st_size,'stderr_sha256':sha(OUT/'stderr.txt'),'old_seed_SPE_oracle_reruns':0,'worst_tax_calls':0}
(OUT/'execution.json').write_text(json.dumps(event,indent=2)+'\n')
assert exit_code==0 and sha(SCRIPT)==before
assert calls==Counter({'<module>':1,'optimize':1,'terminal':216}) and len(records)==15
print(json.dumps({'status':'PASS','elapsed_seconds':elapsed,'LP_calls':len(records),'best_fun':capture['optimize_return']['best_fun'],'root':capture['optimize_return']['root'],'integer_weights':capture['main_reconstruction']['weights'],'stdout':(OUT/'stdout.txt').read_text()}))
