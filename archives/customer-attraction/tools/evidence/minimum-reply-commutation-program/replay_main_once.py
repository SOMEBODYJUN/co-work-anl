"""Run the unchanged original main once and passively retain its final locals.

No second enumeration. The profile callback observes main return only, without
changing any frame local, source code, mathematical function or assertion.
"""
import argparse
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys
import time
import traceback

def fingerprint(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def encode(x):
    if isinstance(x,Fraction):return str(x)
    if isinstance(x,(tuple,list)):return [encode(v) for v in x]
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    return x

def main():
    p=argparse.ArgumentParser()
    for name in ('source','report','out'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();a.source=a.source.resolve();a.out.mkdir(parents=True,exist_ok=False)
    before=fingerprint(a.source);report_before=fingerprint(a.report)
    assert before=={'bytes':2779,'sha256':'631c4a897f21e52fffb50e7d76788a4acc36cbf955b86c0f3c42e9a9494c985d'}
    assert report_before=={'bytes':590,'sha256':'3834ff80162300c16bb14a17c65d3bc95ac07455ce6c58333410b411cf8bbc37'}
    captured={};main_calls=0
    def observe(frame,event,arg):
        nonlocal main_calls
        if frame.f_code.co_filename==str(a.source) and frame.f_code.co_name=='main':
            if event=='call':main_calls+=1
            if event=='return':
                loc=frame.f_locals
                captured.update({k:encode(loc[k]) for k in ('BR','feasible','ell','witness','swapped','source_floor','tie','delta','checked_last','checked_source')})
                captured['utility']=[{'c':c,'d':d,'payoffs':encode(u)} for (c,d),u in loc['utility'].items()]
        return observe
    output=io.StringIO();errors=io.StringIO();old_argv=sys.argv[:];old_profile=sys.getprofile()
    started=datetime.now(timezone.utc).isoformat();timer=time.monotonic();exit_code=0
    try:
        sys.argv=[str(a.source)];sys.setprofile(observe)
        with redirect_stdout(output),redirect_stderr(errors):runpy.run_path(str(a.source),run_name='__main__')
    except BaseException:
        exit_code=1;traceback.print_exc(file=errors)
    finally:
        sys.setprofile(old_profile);sys.argv=old_argv
    elapsed=time.monotonic()-timer
    (a.out/'stdout.txt').write_text(output.getvalue());(a.out/'stderr.txt').write_text(errors.getvalue())
    (a.out/'captured-main-locals.json').write_text(json.dumps(captured,indent=2)+'\n')
    event={'scope':'One unchanged original main via runpy __main__, with passive profile observation; not a second independent enumerator or quotient test',
           'wrapper_argv':[sys.executable,'-B',str(Path(__file__).resolve()),'--source',str(a.source),'--report',str(a.report),'--out',str(a.out)],
           'original_sys_argv':[str(a.source)],'entry_mode':'runpy.run_path(original_source,run_name=__main__)','cwd':str(Path.cwd()),
           'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':elapsed,'python':sys.version,
           'assertions_enabled':not sys.flags.optimize,'main_calls_observed':main_calls,'exit_code':exit_code,
           'source':before,'reference_report':report_before,'source_unchanged':fingerprint(a.source)==before,'reference_report_unchanged':fingerprint(a.report)==report_before,
           'stdout':fingerprint(a.out/'stdout.txt'),'stderr':fingerprint(a.out/'stderr.txt'),
           'stdout_byte_equal_reference_report':(a.out/'stdout.txt').read_bytes()==a.report.read_bytes(),
           'capture':fingerprint(a.out/'captured-main-locals.json'),'profile':'Read final locals on original main return only; no assignments to frame or source functions',
           'new_policy_enumerations':1,'additional_source_main_runs':0,'optimizer_runs':0,'quotient_test_runs':0}
    (a.out/'execution.json').write_text(json.dumps(event,indent=2)+'\n')
    print(output.getvalue(),end='');print(json.dumps(event,indent=2))
    assert exit_code==0 and main_calls==1 and event['source_unchanged'] and event['reference_report_unchanged'] and event['stdout_byte_equal_reference_report'] and not errors.getvalue()

if __name__=='__main__':main()
