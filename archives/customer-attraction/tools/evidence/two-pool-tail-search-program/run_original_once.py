"""Run the unmodified original main once, passively observing batch returns.

No program parameters, NumPy arrays, or branches are changed. Profiling only
reads completed test_parameters returns and the corresponding parameter batch.
"""
from collections import Counter
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import runpy
import sys
import time
import traceback
import numpy as np


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    source=Path(sys.argv[1]).resolve()
    expected=Path(sys.argv[2]).resolve()
    out=Path(sys.argv[3]).resolve()
    out.mkdir(parents=True,exist_ok=True)
    if sys.flags.optimize:
        raise RuntimeError('Keep assertions enabled for execution recording')
    if (out/'execution.json').exists() or source.with_suffix('.json').exists():
        raise RuntimeError('Refuse to overwrite an existing original execution')
    source_sha=sha(source);expected_sha=sha(expected)
    assert source_sha=='f268d9322c947d4bf805397b2c489f7f310b81966c9f4d8b8378bfb93376746e'
    calls=Counter();batches=[];floor_hist=Counter();eligible_floor_hist=Counter()
    all_min=None;eligible_min=None;eligible_max=None;argmin=None
    total=eligible=survivors=0

    def observe(frame,event,arg):
        nonlocal all_min,eligible_min,eligible_max,argmin,total,eligible,survivors
        if frame.f_code.co_filename!=str(source):
            return
        name=frame.f_code.co_name
        if event=='call' and name in ('main','coefficient_tables','test_parameters'):
            calls[name]+=1
        if event!='return' or name!='test_parameters' or arg is None:
            return
        ok,floor,tail=arg
        pars=frame.f_locals['parameters']
        batch_start=total
        total+=len(pars);eligible+=int(tail.sum());survivors+=int(ok.sum())
        low=int(floor.min());all_min=low if all_min is None else min(all_min,low)
        for value in floor:floor_hist[int(value)]+=1
        candidates=[]
        for i in np.flatnonzero(tail):
            value=int(floor[i]);eligible_floor_hist[value]+=1
            candidates.append((value,i))
            if eligible_min is None or value<eligible_min:
                eligible_min=value;argmin=list(map(int,pars[i]))
            eligible_max=value if eligible_max is None else max(eligible_max,value)
        first=min(candidates,default=None)
        batches.append({'batch':len(batches),'start':batch_start,'rows':len(pars),
                        'tail_supported':int(tail.sum()),'survivors':int(ok.sum()),
                        'minimum_root_floor_times_12':low,
                        'minimum_supported_root_floor_times_12':None if first is None else first[0],
                        'first_supported_argmin':None if first is None else list(map(int,pars[first[1]]))})

    started=datetime.now(timezone.utc).isoformat();tick=time.monotonic();error=None
    with (out/'stdout.txt').open('w') as stdout,(out/'stderr.txt').open('w') as stderr:
        try:
            with redirect_stdout(stdout),redirect_stderr(stderr):
                sys.setprofile(observe)
                runpy.run_path(str(source),run_name='__main__')
        except BaseException:
            error=traceback.format_exc();stderr.write(error)
        finally:
            sys.setprofile(None)
    elapsed=time.monotonic()-tick
    produced=source.with_suffix('.json')
    capture={'scope':'Passive observation of one unmodified original main; no second parameter scan.',
             'function_calls':dict(calls),'batches':len(batches),'checked':total,'tail_supported':eligible,
             'tail_unsupported':total-eligible,'survivors':survivors,
             'minimum_root_floor_times_12':all_min,
             'minimum_supported_root_floor_times_12':eligible_min,
             'maximum_supported_root_floor_times_12':eligible_max,
             'first_supported_minimizer_parameters':argmin,
             'root_floor_histogram':{str(k):v for k,v in sorted(floor_hist.items())},
             'supported_root_floor_histogram':{str(k):v for k,v in sorted(eligible_floor_hist.items())},
             'all_batches':batches}
    (out/'captured-batches.json').write_text(json.dumps(capture,indent=2)+'\n')
    result={'kind':'one-original-main-with-read-only-profile','source_id':'9178a319461f5fdf746b',
            'started_utc':started,'elapsed_seconds':elapsed,'python':sys.version,'numpy':np.__version__,
            'invocation':['runpy.run_path',str(source),'run_name=__main__'],'argv':sys.argv,
            'source_sha256_before':source_sha,'source_sha256_after':sha(source),
            'expected_report_sha256_before':expected_sha,'expected_report_sha256_after':sha(expected),
            'error':error,'original_main_calls':calls['main'],'original_coefficient_table_calls':calls['coefficient_tables'],
            'original_test_parameters_calls':calls['test_parameters'],
            'produced_report_path':str(produced),'produced_report_bytes':produced.stat().st_size if produced.exists() else None,
            'produced_report_sha256':sha(produced) if produced.exists() else None,
            'byte_equal_to_frozen_report':produced.exists() and produced.read_bytes()==expected.read_bytes(),
            'stdout_bytes':(out/'stdout.txt').stat().st_size,'stdout_sha256':sha(out/'stdout.txt'),
            'stderr_bytes':(out/'stderr.txt').stat().st_size,'stderr_sha256':sha(out/'stderr.txt'),
            'captured_batches_sha256':sha(out/'captured-batches.json'),
            'profile_changes_to_arrays_or_parameters':False}
    (out/'execution.json').write_text(json.dumps(result,indent=2)+'\n')
    assert error is None and sha(source)==source_sha and sha(expected)==expected_sha
    assert calls==Counter(main=1,coefficient_tables=1,test_parameters=809)
    assert total==103474 and eligible==38130 and survivors==0
    assert result['byte_equal_to_frozen_report'] and result['stderr_bytes']==0
    print(json.dumps({'status':'PASS','seconds':elapsed,'checked':total,'tail_supported':eligible,
                      'minimum_supported_root_floor_times_12':eligible_min,'argmin':argmin,
                      'source_main_calls':calls['main'],'byte_equal_to_frozen_report':True}))


if __name__=='__main__':main()
