"""Append the entire symbolic actual4/R/family0-off complete624 block.

Only a fixed16-hist necessary LP is handled.  All inherited rows/columns,
all16 hist and all4992 new nonnegative masses remain in the full problem.
Old coordinates are never replaced by the frozen point's numerical RHS.
One local HiGHS-IPM discovery has a hard170-second solver time limit.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip
import io
import json
import platform
import sys
import time

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
BASE = RUN / 'union_augmented_lp'
TRANSFER = RUN / 'complete624_transfer'
M, N, ORIGINAL, NEWM, NEWN = 19662,15593,4849,1248,4992
EXPECTED = {
    'union_augmented_lp/exact_matrix.json.gz': '99253e05bfe4c5705619777a5989ec9fab5c38dc7e56f934bbe8d9c071040ded',
    'union_augmented_lp/augmented_lp_exact.json': 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3',
    'union_augmented_lp/exact_dual_certificate.json': '78a7cb206f9e807d0228d20ca7eaeafaf088fc551c719ba44dad4ed10f70f5ef',
    'complete624_transfer/full_lift_bundle.json.gz': '3031a0710bd3b99fe421889ccb891e671d11f019f7d9cc9b3165818adc759d03',
    'complete624_transfer/full_lift_bundle_verification.json': 'feb9bcb853b1d9182d94189526fa39905a0f956324311f65f311b142111b7bf7',
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    if str(path).endswith('.gz'):
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            return json.load(f)
    return json.loads(path.read_text())


def write(name, value):
    target = HERE / name
    assert not target.exists(), ('refuse_overwrite', str(target))
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def log(event, **fields):
    record = {'event':event,'utc':datetime.now(timezone.utc).isoformat(),**fields}
    line=json.dumps(record,ensure_ascii=False)
    print(line,flush=True)
    with (HERE/'progress.jsonl').open('a') as f:
        f.write(line+'\n')


@lru_cache(maxsize=None)
def frac(value):
    return F(value)


def dot(encoded, values):
    return sum((frac(v)*values[j] for j,v in encoded if values[j]), F())


def assemble():
    start=time.monotonic()
    for relative,expected in EXPECTED.items():
        assert digest(RUN/relative)==expected,relative
    old=read(BASE/'exact_matrix.json.gz')
    bundle=read(TRANSFER/'full_lift_bundle.json.gz')
    frozen=read(TRANSFER/'freeze_manifest.json')
    for record in frozen['assets']:
        p=RUN.parent.parent.parent/record['path']
        assert p.exists(),str(p)
        assert digest(p)==record['sha256'],record['path']
    assert len(old['rows'])==len(old['row_names'])==M
    assert len(old['columns'])==len(old['objective'])==len(old['normalization'])==N
    assert bundle['base_matrix_sha256']==EXPECTED['union_augmented_lp/exact_matrix.json.gz']
    assert bundle['base_point_sha256']==EXPECTED['union_augmented_lp/augmented_lp_exact.json']
    assert (bundle['added_row_count'],bundle['added_column_count'])==(NEWM,NEWN)
    assert len(bundle['rows'])==len(bundle['row_names'])==len(bundle['row_metadata'])==NEWM
    assert len(bundle['new_columns'])==NEWN
    assert bundle['objective_extension']==bundle['normalization_extension']==['0']*NEWN
    assert all(j<ORIGINAL or N<=j<N+NEWN for row in bundle['rows'] for j,v in row)
    assert sum(map(len,bundle['rows']))==2254128
    assert sum(map(len,old['rows']))==954669
    assert len(bundle['mapping']['groups'])==78
    assert len({g['hist_column'] for g in bundle['mapping']['groups']})==16
    assert len(bundle['mapping']['budgets'])==624
    for gi,g in enumerate(bundle['mapping']['groups']):
        assert g['group_index']==gi
        assert len(g['states'])==4
        assert F(g['orbit_weight'])==F(g['multiplicity'],30)
        for si,state in enumerate(g['states']):
            assert state['state']==[si//2,si%2]
            expected=list(range(N+64*gi+16*si,N+64*gi+16*(si+1)))
            assert state['hidden_columns']==expected
            index=M+2*(4*gi+si)
            assert (state['equality_plus_row'],state['equality_minus_row'])==(index,index+1)
            plus={j:F(1) for j in expected}
            for j,v in state['old_marginal_affine']:
                assert j<ORIGINAL
                plus[j]=-F(v)
            assert [[j,str(v)] for j,v in sorted(plus.items())]==bundle['rows'][index-M]
            assert [[j,str(-v)] for j,v in sorted(plus.items())]==bundle['rows'][index-M+1]
    for i,record in enumerate(bundle['row_metadata']):
        assert record['index']==M+i and record['name']==bundle['row_names'][i]
        assert sha256(json.dumps(bundle['rows'][i],separators=(',',':')).encode()).hexdigest()==record['sparse_sha256']
    for i,budget in enumerate(bundle['mapping']['budgets']):
        assert budget['feature_index']==i and budget['row_index']==M+624+i
    matrix={**old,'columns':old['columns']+bundle['new_columns'],
        'rows':old['rows']+bundle['rows'],'row_names':old['row_names']+bundle['row_names'],
        'objective':old['objective']+bundle['objective_extension'],
        'normalization':old['normalization']+bundle['normalization_extension'],
        'baseline_rows':M,'baseline_columns':N,'this_round_added':NEWM,
        'this_round_added_columns':NEWN,'auxiliary_columns':N+NEWN-ORIGINAL,
        'appended_unique_rows':M+NEWM-old['original_rows'],
        'full624_auxiliaries':NEWN,'scope':bundle['scope'],
        'full624_bundle_sha256':EXPECTED['complete624_transfer/full_lift_bundle.json.gz']}
    target=HERE/'exact_matrix.json.gz'
    assert not target.exists()
    with target.open('wb') as raw:
        with gzip.GzipFile(fileobj=raw,filename='',mode='wb',mtime=0) as gz:
            with io.TextIOWrapper(gz,encoding='utf-8') as text:
                json.dump(matrix,text,ensure_ascii=False,separators=(',',':'))
    assert matrix['rows'][:M]==old['rows']
    assert matrix['columns'][:N]==old['columns']
    assert matrix['objective'][:N]==old['objective'] and matrix['normalization'][:N]==old['normalization']
    old_dual=read(BASE/'exact_dual_certificate.json')
    lower=F(old_dual['normalization_multiplier'])
    obj,norm=list(map(F,matrix['objective'])),list(map(F,matrix['normalization']))
    residuals=[c-lower*a for c,a in zip(obj,norm)]
    for i,lam in old_dual['row_multipliers']:
        lam=F(lam)
        assert 0<=i<M and lam>0
        for j,v in matrix['rows'][i]:
            residuals[j]-=lam*frac(v)
    assert residuals[:N]==list(map(F,old_dual['residuals']))
    assert min(residuals)>=0 and residuals[N:]==[F()]*NEWN
    assert lower==F(read(BASE/'augmented_lp_exact.json')['W'])
    write('inherited_dual_lower_bound.json',{
        'verified':True,'normalization_multiplier':str(lower),
        'source_sha256':EXPECTED['union_augmented_lp/exact_dual_certificate.json'],
        'row_multipliers':old_dual['row_multipliers'],'new_row_multipliers_all_zero':True,
        'residuals':list(map(str,residuals)),'columns_checked':N+NEWN,
        'minimum_coefficient_residual':str(min(residuals)),
        'matrix_sha256':digest(target),
        'identity':'objective = lower * normalization + sum_i lambda_i row_i + nonnegative residual',
        'scope':'Exact lower bound for the full augmented finite necessary LP only.'})
    for name in ('epigraph_structure.json','zz_envelope_structure.json'):
        destination=HERE/name
        assert not destination.exists()
        destination.write_bytes((BASE/name).read_bytes())
    paths=[RUN/p for p in EXPECTED]
    paths += [TRANSFER/'freeze_manifest.json',TRANSFER/'inputs_manifest.json',
        BASE/'epigraph_structure.json',BASE/'zz_envelope_structure.json',
        BASE/'recover_full.py',BASE/'recover_dual_repair2.py',BASE/'verify_certificates.py']
    write('inputs_manifest.json',{'sha256':{str(p.relative_to(RUN)):digest(p) for p in paths},
        'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
        'rows':M+NEWM,'columns':N+NEWN,'all_columns_nonnegative':True,
        'exact_matrix_sha256':digest(target),'all_zero_mass_hist_and_marginal_cells_retained':True,
        'new_rhs_fixed_point_substitutions':0,'solver_calls_before_this_task':0})
    nnz=sum(map(len,matrix['rows']))
    data=np.empty(nnz,dtype=np.float64)
    indices=np.empty(nnz,dtype=np.int32)
    indptr=np.empty(len(matrix['rows'])+1,dtype=np.int32)
    scales=np.empty(len(matrix['rows']),dtype=np.float64)
    k=0
    for i,row in enumerate(matrix['rows']):
        indptr[i]=k
        vals=[float(frac(v)) for j,v in row]
        scales[i]=max([abs(v) for v in vals]+[1.0e-50])
        for (j,_),v in zip(row,vals):
            indices[k]=j;data[k]=-v/scales[i];k+=1
    indptr[-1]=k
    assert k==nnz==3208797
    np.savez_compressed(HERE/'floating_problem.npz',data=data,indices=indices,indptr=indptr,
        shape=np.asarray([M+NEWM,N+NEWN]),objective=np.asarray(list(map(float,obj))),
        normalization=np.asarray(list(map(float,norm))),scales=scales,
        inequality_rhs=np.zeros(M+NEWM),normalization_rhs=np.asarray([1.0]))
    report={'status':'PASS','rows':M+NEWM,'columns':N+NEWN,'nonzeros':nnz,
        'old_rows_unchanged':M,'old_column_descriptors_unchanged':N,'old_auxiliaries_retained':10744,
        'new_rows':NEWM,'new_columns':NEWN,'new_nonzeros':2254128,
        'symbolic_marginal_equalities_rebuilt':312,'shared_hidden_blocks':312,
        'histogram_descriptors':16,'full624_budgets':624,
        'all_new_row_old_auxiliary_coefficients_zero':True,'new_objective_normalization_zero':True,
        'fixed_point_rhs_substitutions':0,'frozen_transfer_manifest_assets_verified':len(frozen['assets']),
        'inherited_exact_dual_reverified_columns':N+NEWN,'lower_bound':str(lower),
        'matrix_sha256':digest(target),'floating_problem_sha256':digest(HERE/'floating_problem.npz'),
        'seconds':time.monotonic()-start}
    write('assembly_verification.json',report)
    log('assembly_complete',**report)


def solve():
    assert not (HERE/'numerical_result.json').exists()
    p=np.load(HERE/'floating_problem.npz')
    shape=tuple(map(int,p['shape']))
    sparse=csr_matrix((p['data'],p['indices'],p['indptr']),shape=shape)
    options={'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10,
        'ipm_optimality_tolerance':1e-12,'time_limit':170.0,'presolve':True,'disp':True}
    log('one_full_augmented_numerical_solve_started',method='highs-ipm',shape=shape,options=options)
    start=time.monotonic()
    solution=linprog(p['objective'],A_ub=sparse,b_ub=p['inequality_rhs'],
        A_eq=coo_matrix(p['normalization'].reshape(1,-1)).tocsr(),b_eq=p['normalization_rhs'],
        bounds=(0,None),method='highs-ipm',options=options)
    numerical={'success':bool(solution.success),'status_code':int(solution.status),'message':solution.message,
        'solver_seconds':time.monotonic()-start,'nit':solution.nit,
        'crossover_nit':getattr(solution,'crossover_nit',None),
        'W_float':None if solution.fun is None else float(solution.fun),
        'method':'highs-ipm','options':options,'optimizer_calls':1,
        'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
        'exact_verified':False,'matrix_sha256':digest(HERE/'exact_matrix.json.gz'),
        'floating_problem_sha256':digest(HERE/'floating_problem.npz')}
    if solution.x is not None:
        numerical['minimum_scaled_slack']=float(np.min(-sparse@solution.x))
        numerical['minimum_column']=float(np.min(solution.x))
        numerical['positive_original_columns']=int(np.sum(solution.x[:ORIGINAL]>1e-10))
        numerical['positive_new_hidden_columns']=int(np.sum(solution.x[N:]>1e-10))
        arrays={'primal':solution.x,'scales':p['scales']}
        for name,source in [('inequality_marginals',solution.ineqlin),('equality_marginals',solution.eqlin),('lower_marginals',solution.lower)]:
            if source.marginals is not None:arrays[name]=source.marginals
        np.savez_compressed(HERE/'floating_solver_arrays.npz',**arrays)
    write('numerical_result.json',numerical)
    log('one_full_augmented_numerical_solve_finished',**numerical)
    if not solution.success:
        raise RuntimeError('One local discovery did not finish optimally; no local rerun. Prepare Actions continuation.')


if __name__=='__main__':
    assert len(sys.argv)==2 and sys.argv[1] in ('assemble','solve')
    globals()[sys.argv[1]]()
