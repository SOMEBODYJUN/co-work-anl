"""One unchanged top-level source invocation, passive return-only LP capture."""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import platform
import runpy
import shutil
import sys
import time
import numpy as np
import scipy

WORK=Path(__file__).resolve().parent
REPO=Path('/workspace/scratch/c0ab78c47566/boss7-cleaner')
RUNTIME=WORK/'runtime'
OUTPUT=WORK/'replay'
RUNTIME.mkdir(exist_ok=False)
OUTPUT.mkdir(exist_ok=False)
source=RUNTIME/'research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/global_proof/individual_floor_search.py'
source.parent.mkdir(parents=True)
shutil.copyfile(WORK/'individual_floor_search.py',source)
helper=RUNTIME/'tests/audits/customer_attraction_strategy_lp.py'
helper.parent.mkdir(parents=True)
shutil.copyfile(REPO/'archives/customer-attraction/tools/evidence/strategy-cones/original/tests/audits/customer_attraction_strategy_lp.py',helper)
dependency=REPO/'archives/customer-attraction/tools/evidence/credible-padding-program/dependencies/customer_attraction'
shutil.copytree(dependency,RUNTIME/'customer_attraction')


def digest(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())


def plain(x):
    if isinstance(x,Fraction):return str(x)
    if isinstance(x,np.ndarray):return plain(x.tolist())
    if isinstance(x,np.generic):return x.item()
    if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [plain(v) for v in x]
    return x


def save(name,value):
    (OUTPUT/name).write_text(json.dumps(plain(value),ensure_ascii=False,indent=2)+'\n')


inputs=[source,helper]+sorted((RUNTIME/'customer_attraction').glob('*.py'))
before=[digest(p) for p in inputs]
known={str(p):str(p.relative_to(RUNTIME)) for p in inputs}
calls=Counter();fits=[];captured={}


def observe(frame,event,value):
    file=frame.f_code.co_filename;name=frame.f_code.co_name
    if event=='call' and file in known:
        calls[known[file]+':'+name]+=1
    if event!='return':return
    if file==str(source) and name=='<module>':
        captured['cone']=frame.f_locals['cone']
    elif name=='linprog' and frame.f_back is not None and frame.f_back.f_code.co_filename==str(source):
        parent=frame.f_back.f_locals
        fits.append(dict(player=parent['player'],portfolio=list(parent['supp']),objective=plain(parent['obj']),
                         own=plain(parent['own']),result=plain(value)))


started=datetime.now(timezone.utc).isoformat();start=time.perf_counter();error=None
argv=sys.argv[:];sys.argv=[str(source)]
sys.setprofile(observe)
try:
    runpy.run_path(str(source),run_name='__main__')
except BaseException as exc:
    error=dict(type=type(exc).__name__,message=str(exc))
finally:
    sys.setprofile(None);sys.argv=argv
original_seconds=time.perf_counter()-start
model=None
if 'cone' in captured:
    c=captured['cone']
    model=dict(topics=c.topics,players=c.players,root=c.root,
        actions=[dict(history=h,action=a) for h,a in sorted(c.actions.items(),key=lambda z:(len(z[0]),z[0]))],
        terminals=[dict(history=h,counts=q) for h,q in sorted(c.terminals.items(),key=lambda z:(len(z[0]),z[0]))],
        rational_rows=c.rows,float_matrix=c.matrix,welfare=c.welfare)
    save('original-model.json',model)
raw=json.dumps(plain(fits),ensure_ascii=False,separators=(',',':')).encode()
(OUTPUT/'original-lp-results.json.gz').write_bytes(gzip.compress(raw,mtime=0))
summary=dict(LP_calls=len(fits),successful=sum(bool(x['result'].get('success')) for x in fits),
    statuses=dict(Counter(str(x['result'].get('status')) for x in fits)),players={})
for i in range(3):
    records=[x for x in fits if x['player']==i]
    okay=[x for x in records if x['result'].get('success')]
    best=min(okay,key=lambda x:x['result']['fun']) if okay else None
    summary['players'][str(i)]=dict(LPs=len(records),successful=len(okay),
        best_float_value=-best['result']['fun'] if best else None,
        best_portfolio=best['portfolio'] if best else None)
if model:
    summary.update(policy_nodes=len(model['actions']),terminal_lookup_nodes=len(model['terminals']),
        unique_nonzero_rows=len(model['rational_rows']),variables=63,root=model['root'])
save('capture-summary.json',summary)
save('execution.json',dict(started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),
    original_seconds_with_profile=original_seconds,total_seconds_with_serialization=time.perf_counter()-start,
    invocation='One unchanged runpy top-level source; passive profile observes original linprog returns and module globals',
    argv=[str(source)],python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
    assertions_enabled=__debug__,inputs_before=before,inputs_after=[digest(p) for p in inputs],
    original_call_counts=dict(sorted(calls.items())),original_LP_calls=len(fits),error=error,
    helper_replacements=0,additional_original_calls=0,BI_calls=0,canonical_certificate_calls=0,
    new_independent_mathematical_audits=0,raw_LP_bytes=len(raw),
    files={p.name:digest(p) for p in sorted(OUTPUT.iterdir()) if p.is_file()}))
if error:raise RuntimeError(error)
