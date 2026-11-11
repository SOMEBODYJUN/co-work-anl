"""A single reproducible stage for the prepared Actions continuation.

This file does not dispatch or authenticate to Actions.  Its solver stage
requires the runner's GITHUB_ACTIONS=true marker, preventing a local retry.
"""
from pathlib import Path
import json,os,platform,sys,time,traceback
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,csr_matrix
import assemble_solve as A

ROOT=A.HERE
stage=sys.argv[1]
out=Path(sys.argv[2]).resolve()
assert out.is_relative_to(ROOT) and out!=ROOT
A.HERE=out
os.environ.setdefault('FULL624_EXACT_TIME_LIMIT','1800')
import recover as R
R.HERE=out


def solve():
    assert os.environ.get('GITHUB_ACTIONS')=='true','Continuation is prepared for Actions, not another local solve.'
    method=sys.argv[3];limit=float(sys.argv[4])
    assert method in ('highs-ds','highs-ipm') and 170<limit<=7200
    assert not (out/'numerical_result.json').exists()
    p=np.load(out/'floating_problem.npz');shape=tuple(map(int,p['shape']))
    assert shape==(20910,20585)
    sparse=csr_matrix((p['data'],p['indices'],p['indptr']),shape=shape)
    options={'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10,
        'time_limit':limit,'presolve':True,'disp':True}
    if method=='highs-ipm':options['ipm_optimality_tolerance']=1e-12
    A.log('actions_one_full_solve_started',method=method,options=options)
    start=time.monotonic()
    solution=linprog(p['objective'],A_ub=sparse,b_ub=p['inequality_rhs'],
        A_eq=coo_matrix(p['normalization'].reshape(1,-1)).tocsr(),b_eq=p['normalization_rhs'],
        bounds=(0,None),method=method,options=options)
    report={'success':bool(solution.success),'status_code':int(solution.status),'message':solution.message,
        'solver_seconds':time.monotonic()-start,'nit':solution.nit,
        'crossover_nit':getattr(solution,'crossover_nit',None),
        'W_float':None if solution.fun is None else float(solution.fun),
        'method':method,'options':options,'optimizer_calls_this_actions_run':1,
        'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
        'exact_verified':False,'matrix_sha256':A.digest(out/'exact_matrix.json.gz'),
        'floating_problem_sha256':A.digest(out/'floating_problem.npz')}
    if solution.x is not None:
        arrays={'primal':solution.x,'scales':p['scales']}
        for name,source in [('inequality_marginals',solution.ineqlin),('equality_marginals',solution.eqlin),('lower_marginals',solution.lower)]:
            if source.marginals is not None:arrays[name]=source.marginals
        np.savez_compressed(out/'floating_solver_arrays.npz',**arrays)
        report.update(minimum_scaled_slack=float(np.min(-sparse@solution.x)),minimum_column=float(np.min(solution.x)),
            positive_original_columns=int(np.sum(solution.x[:4849]>1e-11)),
            positive_new_hidden_columns=int(np.sum(solution.x[15593:]>1e-11)))
    A.write('numerical_result.json',report)
    A.log('actions_full_solve_finished',**report)
    if not solution.success:raise RuntimeError('Actions discovery not optimal; all output retained; no automatic solver rerun.')


try:
    if stage=='solve':solve()
    elif stage in ('sameW','freeW'):R.primal(stage)
    elif stage=='dual':R.dual()
    else:raise AssertionError(stage)
except BaseException:
    if stage!='solve':
        A.write('recovery_'+stage+'_failure.json',{'attempt':stage,'traceback':traceback.format_exc(),
            'no_optimizer_rerun':True,'failure_is_not_an_infeasibility_certificate':True})
    raise
