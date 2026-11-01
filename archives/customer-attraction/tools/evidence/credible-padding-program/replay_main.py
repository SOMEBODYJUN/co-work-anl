#!/usr/bin/env python3
"""Observe one unchanged original finite main; no substituted functions or extra solver calls."""
import argparse
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


def plain(value):
    if isinstance(value, Fraction): return str(value)
    if isinstance(value, dict): return {str(k): plain(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)): return [plain(v) for v in value]
    if isinstance(value, (set,frozenset)): return [plain(v) for v in sorted(value)]
    return value


def fingerprint(path):
    b=path.read_bytes()
    return {'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}


def save(path,value):
    path.write_text(json.dumps(plain(value),ensure_ascii=False,indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--dependencies',type=Path,required=True)
    parser.add_argument('--run-dir',type=Path,required=True)
    parser.add_argument('--k',type=int,required=True)
    args=parser.parse_args()
    args.run_dir.mkdir(parents=True,exist_ok=False)
    run=args.run_dir.resolve(); source=run/'all_k_padding.py'
    shutil.copyfile(args.source,source)
    shutil.copytree(args.dependencies/'customer_attraction',run/'customer_attraction')
    inputs=[source]+sorted((run/'customer_attraction').glob('*.py'))
    before=[fingerprint(p) for p in inputs]
    filenames={str(p):p.name if p==source else 'customer_attraction/'+p.name for p in inputs}
    calls=Counter();capture={}
    def observe(frame,event,result):
        origin=filenames.get(frame.f_code.co_filename)
        if origin is None:return
        name=frame.f_code.co_name
        if event=='call':calls[origin+':'+name]+=1
        elif event=='return' and origin=='all_k_padding.py' and name=='main':
            loc=frame.f_locals
            for key in ['states','arcs','actions','ends','root','report','load','g','G','gap','solver']:
                if key in loc:capture[key]=loc[key]
    argv=sys.argv[:];oldpath=sys.path[:]
    sys.path.insert(0,str(run));sys.argv=[str(source),str(args.k),'--output',str(run/'report.json')]
    started=datetime.now(timezone.utc).isoformat();start=time.perf_counter()
    sys.setprofile(observe)
    try:runpy.run_path(str(source),run_name='__main__')
    finally:
        sys.setprofile(None);sys.argv=argv;sys.path[:]=oldpath
    original_seconds=time.perf_counter()-start
    # Serialize already-computed original locals without any Instance/Solver calls.
    nodes=[]
    for i,(counts,mode) in enumerate(capture['states']):
        nodes.append({'id':i,'counts':counts,'mode':mode,'action':capture['actions'].get(i),
                      'children':capture['arcs'].get(i,()),'end':capture['ends'][i]})
    dag={'k':args.k,'root':capture['root'],'nodes':nodes,'scope':'Original returned locals, no independent payoff/IC audit.'}
    raw=json.dumps(plain(dag),ensure_ascii=False,separators=(',',':')).encode()
    (run/'original-dag.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    solver=capture['solver']
    cache={'outcomes':[{'counts':c,'terminals':sorted(v)} for c,v in sorted(solver._outcomes.items())],
           'thresholds':[{'counts':c,'threshold':v} for c,v in sorted(solver._thresholds.items())],
           'payoffs':[{'counts':c,'payoffs':v} for c,v in sorted(solver._payoffs.items())]}
    save(run/'original-solver-cache.json',cache)
    save(run/'original-main-locals.json',{key:capture[key] for key in ['root','report','load','g','G','gap']})
    modes=Counter(node['mode'][0] for node in nodes)
    decision_modes=Counter(node['mode'][0] for node in nodes if node['action'] is not None)
    save(run/'capture-summary.json',{
        'nodes':len(nodes),'decision_nodes':len(capture['arcs']),'arcs':sum(len(x) for x in capture['arcs'].values()),
        'mode_counts':dict(modes),'decision_mode_counts':dict(decision_modes),
        'BI_cached_count_states':len(solver._outcomes),'BI_cached_thresholds':len(solver._thresholds),
        'BI_cached_terminal_payoff_vectors':len(solver._payoffs),
        'BI_retained_terminal_entries':sum(len(v) for v in solver._outcomes.values()),
        'dag_uncompressed_bytes':len(raw),'source_report':capture['report']})
    event={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
           'original_main_seconds_with_observer':original_seconds,'total_seconds_with_serialization':time.perf_counter()-start,
           'python':platform.python_version(),'assertions_enabled':__debug__,'k':args.k,
           'invocation':'One runpy original main, return-only profile; no replacements or extra original calls.',
           'inputs_before':before,'inputs_after':[fingerprint(p) for p in inputs],
           'call_events':dict(sorted(calls.items())),
           'helper_replacements':0,'additional_original_calls':0,'new_independent_DAG_or_IC_audits':0,
           'canonical_certificate_or_verifier_calls':0,'optimization_calls':0,
           'files':{p.name:fingerprint(p) for p in sorted(run.iterdir()) if p.is_file() and p!=source}}
    save(run/'execution.json',event)


if __name__=='__main__':main()
