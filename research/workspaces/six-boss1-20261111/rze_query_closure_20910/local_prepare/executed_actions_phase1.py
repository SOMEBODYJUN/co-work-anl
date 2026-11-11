"""One Actions-only phase-I discovery, with all inputs and failures retained.

Dependencies: Python standard library, numpy, scipy.  No local optimization
is authorized by this script's preparation mode.  A real run calls HiGHS-ds
exactly once; any unsuccessful state is saved and must not trigger a retry.
"""
from datetime import datetime,timezone
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json
import os
import platform
import signal
import sys
import time
import traceback

# Set before importing numerical libraries, without modifying system paths.
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ.setdefault('MKL_NUM_THREADS','1')
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,hstack,save_npz

HERE=Path(__file__).resolve().parent
POINT=HERE.parent/'full624_augmented_lp/recovery/augmented_lp_exact.json'
EXPECTED_POINT='cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'
EXPECTED_MATRIX='cf420cca78dd507239aa3baac1538093177d10c8b37af84fc5a945209816fdc8'

def sha(p):return sha256(p.read_bytes()).hexdigest()
def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def gzsave(path,data):
    raw=(json.dumps(data,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode()
    with path.open('wb') as out:
        with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0) as gz:gz.write(raw)
def array(result,group,field):
    obj=getattr(result,group,None)
    value=getattr(obj,field,None) if obj is not None else None
    return None if value is None else np.asarray(value,dtype=float).tolist()
def interrupted(signum,frame):raise RuntimeError('External interruption signal '+str(signum))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=HERE/'actions_output')
    ap.add_argument('--seconds',type=int,choices=(900,1800),default=1800)
    ap.add_argument('--prepare-only',action='store_true')
    args=ap.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    started=datetime.now(timezone.utc).isoformat();begin=time.perf_counter()
    report={'scope':'Numerical discovery only; exact recovery is a separate required step.',
            'started_utc':started,'linprog_calls':0,'method':'highs-ds','time_limit_seconds':args.seconds,
            'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
            'source_sha256':sha(Path(__file__)),'success':False,'status':'preparing',
            'prepare_only':args.prepare_only}
    if not args.prepare_only:
        with (out/'started.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
        assert not (out/'phase_I_discovery.json').exists(),'Previous discovery exists; refusing a second call.'
        signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    try:
        matrix_path=HERE/'symbolic_lift.json.gz';audit_path=HERE/'preflight_literal_audit.json'
        assert sha(POINT)==EXPECTED_POINT and sha(matrix_path)==EXPECTED_MATRIX
        audit=json.loads(audit_path.read_bytes());assert audit['passed']
        assert audit['point_sha256']==EXPECTED_POINT and audit['symbolic_lift_sha256']==EXPECTED_MATRIX
        lift=json.loads(gzip.decompress(matrix_path.read_bytes()));point=json.loads(POINT.read_bytes())
        assert lift['original_columns']==4849 and lift['nonnegative_new_columns'] and lift['row_constants']==0
        assert lift['old_descriptors']==[{k:v for k,v in c.items() if k!='weight'} for c in point['columns'][:4849]]
        w=[Fraction(c['weight']) for c in point['columns'][:4849]]
        ri=[];ci=[];av=[];rhs=[]
        for i,row in enumerate(lift['rows']):
            fixed=Fraction()
            for j,t in row['row']:
                v=Fraction(t)
                if j<4849:fixed+=v*w[j]
                else:ri.append(i);ci.append(j-4849);av.append(-float(v))
            rhs.append(fixed)
        n=len(lift['new_columns']);m=len(rhs);assert (m,n)==(21572,11034)
        A=coo_matrix((av,(ri,ci)),shape=(m,n)).tocsr()
        A=hstack([A,-np.ones((m,1))],format='csr')
        b=np.asarray([float(v) for v in rhs]);objective=np.zeros(n+1);objective[-1]=1.
        assert np.isfinite(A.data).all() and np.isfinite(b).all()
        save_npz(out/'phase_I_matrix.npz',A,compressed=True)
        np.savez_compressed(out/'phase_I_vectors.npz',b_ub=b,c=objective,
                            lower_bounds=np.zeros(n+1),upper_bounds=np.full(n+1,np.inf))
        gzsave(out/'phase_I_input_order.json.gz',{
            'row_order':[r['name'] for r in lift['rows']],
            'new_column_order':lift['new_columns']+[{'kind':'phase-I-uniform-delta'}],
            'original_old_column_order':lift['old_descriptors'],
            'fixed_old_values':[str(v) for v in w],
            'fixed_old_row_values':[str(v) for v in rhs],
            'inequality':'(-B) x - delta <= c dot old_point',
            'all_new_variables_nonnegative':True})
        (out/'executed_actions_phase1.py').write_bytes(Path(__file__).read_bytes())
        report.update(point_sha256=EXPECTED_POINT,symbolic_lift_sha256=EXPECTED_MATRIX,
                      preflight_sha256=sha(audit_path),shape=[m,n+1],matrix_nnz=int(A.nnz),
                      matrix_npz_sha256=sha(out/'phase_I_matrix.npz'),
                      vectors_npz_sha256=sha(out/'phase_I_vectors.npz'),
                      input_order_sha256=sha(out/'phase_I_input_order.json.gz'),
                      options={'time_limit':float(args.seconds),'dual_feasibility_tolerance':1e-9,
                               'primal_feasibility_tolerance':1e-9},status='prepared')
        save(out/'prepared_input.json',report)
        if args.prepare_only:
            print(json.dumps(report,ensure_ascii=False));return
        report['linprog_calls']=1;report['status']='optimizing'
        save(out/'started.json',report)
        print(json.dumps({'status':'starting single phase I','shape':report['shape'],
                          'matrix_nnz':report['matrix_nnz'],'method':'highs-ds','seconds':args.seconds}),flush=True)
        solver_begin=time.perf_counter()
        result=linprog(objective,A_ub=A,b_ub=b,bounds=(0,None),method='highs-ds',options=report['options'])
        report.update(solver_seconds=time.perf_counter()-solver_begin,
                      success=bool(result.success),status=int(result.status),message=str(result.message),
                      iterations=int(result.nit),crossover_iterations=int(getattr(result,'crossover_nit',0)),
                      phase_I=None if result.fun is None else float(result.fun),
                      x=None if result.x is None else np.asarray(result.x,dtype=float).tolist(),
                      row_slack=array(result,'ineqlin','residual'),row_marginals=array(result,'ineqlin','marginals'),
                      lower_residual=array(result,'lower','residual'),lower_marginals=array(result,'lower','marginals'),
                      upper_marginals=array(result,'upper','marginals'))
        report['lambda']=None if report['row_marginals'] is None else [-v for v in report['row_marginals']]
        report['fixed_old_row_values']=[str(v) for v in rhs]
        arrays={k:np.asarray(report[k]) for k in ('x','row_slack','row_marginals','lambda','lower_residual','lower_marginals','upper_marginals') if report[k] is not None}
        np.savez_compressed(out/'phase_I_solution.npz',**arrays)
        report['solution_npz_sha256']=sha(out/'phase_I_solution.npz')
        if result.x is not None:
            direct=b-A@result.x
            report['minimum_direct_slack']=float(direct.min())
            report['max_residual_displacement']=float(np.max(np.abs(direct-np.asarray(report['row_slack']))))
            report['maximum_original_violation']=float(max(0.,-np.min(b-A[:,:-1]@result.x[:-1])))
    except BaseException as exc:
        report.update(success=False,status='exception',exception_type=type(exc).__name__,
                      exception=str(exc),traceback=traceback.format_exc())
    finally:
        report['elapsed_seconds']=time.perf_counter()-begin
        report['finished_utc']=datetime.now(timezone.utc).isoformat()
        destination='prepare_failure.json' if args.prepare_only else 'phase_I_discovery.json'
        if not args.prepare_only or report['status']=='exception':save(out/destination,report)
    excluded={'x','row_slack','row_marginals','lambda','lower_residual','lower_marginals','upper_marginals','fixed_old_row_values'}
    print(json.dumps({k:v for k,v in report.items() if k not in excluded},ensure_ascii=False),flush=True)
    if not report['success']:raise SystemExit(1)

if __name__=='__main__':main()
