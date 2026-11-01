"""One unchanged runpy main with passive return observation; no repeated helper/LP calls."""
from pathlib import Path
import contextlib,hashlib,io,json,math,platform,runpy,sys,time,traceback
from datetime import datetime,timezone
import numpy as np
import scipy

BASE=Path(__file__).resolve().parent
RUN=BASE/'runtime';OUT=BASE/'replay'
SOURCE=RUN/'cartesian_cone.py';LIMIT=RUN/'cartesian_limit.py'
RESULT=RUN/'cartesian_compiler_cone_k4.json'
assert not RESULT.exists() and not (OUT/'execution.json').exists()
def fp(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def plain(x):
    if isinstance(x,np.ndarray):return plain(x.tolist())
    if isinstance(x,np.generic):return plain(x.item())
    if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [plain(v) for v in x]
    if isinstance(x,float) and not math.isfinite(x):return str(x)
    return x
capture={};counts={'cone_main':0,'cone_function':0,'linprog':0,'limit_analyze':0,'limit_main':0}
def observer(frame,event,arg):
    if event!='return':return
    name=frame.f_code.co_name;filename=Path(frame.f_code.co_filename)
    if filename==SOURCE:
        if name=='<module>':counts['cone_main']+=1
        if name=='cone':
            counts['cone_function']+=1;q=frame.f_locals
            capture['model']={k:plain(q[k]) for k in ['k','d','inc','rows','obj','eq','bounds','first','second','W','p','rmix','actual']}
            capture['needed_iteration_order']=[list(z) for z in q['needed']]
            capture['last_replies']=[{'prefix':list(z),'reply':c} for z,c in q['last'].items()]
            capture['seed_payoffs']=[{'terminal':list(z),'action_payoffs':plain(v)} for z,v in q['V'].items()]
            capture['payoff_coefficients']=[{'terminal':list(z),'matrix':plain(v)} for z,v in q['P'].items()]
            capture['cone_return']=plain(arg)
    elif filename==LIMIT:
        if name=='analyze':counts['limit_analyze']+=1
        if name=='main':counts['limit_main']+=1
    if filename.name=='_linprog.py' and name=='linprog':
        counts['linprog']+=1
        capture['linprog_return']=plain(dict(arg))
        capture['linprog_inputs']={k:plain(frame.f_locals.get(k)) for k in ['c','A_ub','b_ub','A_eq','b_eq','bounds','method','options']}
inputs=[SOURCE,LIMIT,RUN/'cartesian_convexification_k4.json']
before=[fp(p) for p in inputs];stdout=io.StringIO();stderr=io.StringIO()
start=datetime.now(timezone.utc).isoformat();clock=time.monotonic();error=None
oldargv=sys.argv[:];sys.argv=[str(SOURCE)]
try:
    with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
        sys.setprofile(observer)
        try:runpy.run_path(str(SOURCE),run_name='__main__')
        finally:sys.setprofile(None)
except BaseException:
    error=traceback.format_exc()
finally:
    sys.argv=oldargv;sys.setprofile(None)
elapsed=time.monotonic()-clock
(OUT/'stdout.txt').write_text(stdout.getvalue());(OUT/'stderr.txt').write_text(stderr.getvalue())
(OUT/'capture.json').write_text(json.dumps(capture,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
if RESULT.exists():(OUT/'cartesian_compiler_cone_k4.json').write_bytes(RESULT.read_bytes())
event={'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'seconds_with_passive_profile':elapsed,
       'invocation':'One unchanged runpy main, passive sys.setprofile observes original cone/linprog returns; not an unwrapped CLI or an independent solver.',
       'argv':[str(SOURCE)],'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
       'assertions_enabled':__debug__,'original_call_counts':counts,'inputs_before':before,'inputs_after':[fp(p) for p in inputs],
       'observer':fp(Path(__file__)),'capture':fp(OUT/'capture.json'),'stdout':fp(OUT/'stdout.txt'),'stderr':fp(OUT/'stderr.txt'),
       'error':error,'finite_calls':0,'independent_mathematical_audits':0,'normalization_or_helper_replacements':0}
if RESULT.exists():event['new_report']=fp(OUT/'cartesian_compiler_cone_k4.json')
(OUT/'execution.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'error':error,'original_call_counts':counts,'seconds':elapsed,'output_exists':RESULT.exists()}))
if error:raise SystemExit(1)
