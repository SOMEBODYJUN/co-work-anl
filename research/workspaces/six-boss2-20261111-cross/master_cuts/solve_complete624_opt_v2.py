#!/usr/bin/env python3
"""Separate stricter IPM/crossover candidate after exact dual inconsistency.

The first exact feasible point and its failed dual diagnostics are immutable.
Only the approved matrix is reused; all outputs have a new opt_v2 prefix.
"""
from pathlib import Path
import argparse,datetime,platform,resource,sys,time
import solve_complete624_v1 as m


def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=('solve','reconstruct','dual','verify'));args=ap.parse_args()
    m.STEM='complete624_actual4_R00_opt_v2'
    started=time.time();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();success=False
    if args.mode=='solve':
        import scipy.optimize
        original=scipy.optimize.linprog
        def tighter(*a,**kw):
            kw['method']='highs-ipm'
            kw['options']={**kw.get('options',{}),'primal_feasibility_tolerance':1e-10,
                'dual_feasibility_tolerance':1e-10,'ipm_optimality_tolerance':1e-12,'time_limit':180}
            return original(*a,**kw)
        scipy.optimize.linprog=tighter
    try:getattr(m,args.mode)();success=True
    finally:m.write('execution_'+args.mode,{'command':[sys.executable,'-B',str(Path(__file__).resolve()),args.mode],
        'cwd':str(m.ROOT),'started_utc':stamp,'elapsed_seconds':time.time()-started,'success':success,
        'python':platform.python_version(),'wrapper_sha256':m.sha(__file__),
        'base_adapter_sha256':m.sha(m.HERE/'solve_complete624_v1.py'),
        'matrix_path':str(m.MATRIX.relative_to(m.ROOT)),'matrix_sha256':m.MATRIX_SHA,
        'numerical_method':'highs-ipm with crossover; primal/dual tolerances1e-10, IPM optimality1e-12',
        'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})


if __name__=='__main__':main()
