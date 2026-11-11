"""Exact sparse recovery on one numerical candidate, with no optimizer calls.

Original positive masses and positive new624 masses are the unknowns.  All
10744 old canonical auxiliaries are eliminated symbolically and recomputed
after recovery.  Every result is accepted only by full rational row/column
checks.  A failed sameW recovery is not an infeasibility certificate.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json,os,sys,time,traceback
import numpy as np
from assemble_solve import HERE,BASE,ORIGINAL,M,N,NEWM,NEWN,frac,read,write,log,digest,dot


def sparse_affine_solve(equations, n, seed, label):
    basis={};started=time.monotonic();last=started;largest=0
    exact_limit=float(os.environ.get('FULL624_EXACT_TIME_LIMIT','170'))
    assert 0<exact_limit<=7200
    for processed,encoded in enumerate(equations,1):
        row={j:v for j,v in encoded.items() if v}
        while row:
            pivot=min(row)
            if pivot==n:
                raise AssertionError(('inconsistent_exact_equations',label,processed,str(row[n])))
            if pivot not in basis:
                scale=row[pivot]
                basis[pivot]={j:v/scale for j,v in row.items()}
                largest=max(largest,len(row));break
            scale=row[pivot]
            for j,v in basis[pivot].items():
                value=row.get(j,F())-scale*v
                if value:row[j]=value
                else:row.pop(j,None)
        now=time.monotonic()
        if now-last>15:
            log('exact_elimination_progress',label=label,equations=processed,rank=len(basis),variables=n,seconds=now-started)
            last=now
        if now-started>exact_limit:
            raise TimeoutError(('exact_elimination_local_limit',label,processed,len(basis),n))
    free=sorted(set(range(n))-set(basis))
    result=[F()]*n
    for j in free:result[j]=F(float(seed[j])).limit_denominator(10**12)
    for pivot in sorted(basis,reverse=True):
        row=basis[pivot]
        result[pivot]=row.get(n,F())-sum((v*result[j] for j,v in row.items() if pivot<j<n),F())
    return result,{'variables':n,'rank':len(basis),'processed_equations':len(equations),
        'largest_sparse_basis_row':largest,'free_variables':free,
        'free_values':[[j,str(result[j])] for j in free],'elimination_seconds':time.monotonic()-started,
        'elimination_time_limit':exact_limit}


def load():
    matrix=read(HERE/'exact_matrix.json.gz')
    epi=read(HERE/'epigraph_structure.json')
    zz=read(HERE/'zz_envelope_structure.json')
    floats=np.load(HERE/'floating_solver_arrays.npz')
    return matrix,epi,zz,floats


def primal(attempt):
    started=time.monotonic()
    matrix,epi,zz,floats=load()
    rows=matrix['rows'];obj=list(map(F,matrix['objective']));norm=list(map(F,matrix['normalization']))
    numerical=floats['primal'].copy()
    thresholds=dict(epi['thresholds'])
    for j,i in thresholds.items():
        numerical[j]=max(0.0,-sum(float(frac(v))*numerical[k] for k,v in rows[i] if k<ORIGINAL))
    for r in zz['auxiliaries']:
        numerical[r['column']]=min(sum(float(frac(v))*numerical[k] for k,v in rows[i] if k<ORIGINAL)
            for i in (r['q_upper_row'],r['v_upper_row']))
    # Marginal equations eliminate the simple new conditional masses first.
    support=[j for j in range(N,N+NEWN) if numerical[j]>1e-11]
    support += [j for j in range(ORIGINAL) if numerical[j]>1e-11]
    local={j:k for k,j in enumerate(support)}
    seed=numerical[support]
    equations=[];descriptions=[];seen=set();representation={}
    def restrict_original(encoded,sign=1):
        return {local[j]:sign*frac(v) for j,v in encoded if j in local and j<ORIGINAL}
    def add(eq,description,forced=False):
        eq={j:v for j,v in eq.items() if v}
        if not eq:return
        if not forced:
            scale=max(abs(float(v)) for v in eq.values())
            slack=sum(float(v)*seed[j] for j,v in eq.items())
            if abs(slack)>1e-10*scale:return
        pivot=min(eq);factor=eq[pivot]
        sig=tuple((j,v/factor) for j,v in sorted(eq.items()))
        if sig in seen:return
        seen.add(sig);equations.append(eq);descriptions.append(description)
    def project(encoded):
        out=defaultdict(F)
        for j,v in encoded:
            v=frac(v)
            if j in local:out[local[j]]+=v
            elif ORIGINAL<=j<N:
                for k,w in representation[j].items():out[k]+=v*w
        return {j:v for j,v in out.items() if v}
    for i in range(M,M+624,2):
        add({local[j]:frac(v) for j,v in rows[i] if j in local},
            {'kind':'full624_symbolic_marginal','row':i},True)
    for j,i in thresholds.items():
        hinge=restrict_original(rows[i],-1)
        representation[j]=hinge if numerical[j]>1e-12 else {}
        add(hinge,{'kind':'canonical_hinge_zero','auxiliary':j,'threshold_row':i})
    for record in zz['auxiliaries']:
        q=restrict_original(rows[record['q_upper_row']]);v=restrict_original(rows[record['v_upper_row']])
        qn=sum(float(w)*seed[k] for k,w in q.items());vn=sum(float(w)*seed[k] for k,w in v.items())
        representation[record['column']]=q if qn<=vn else v
        diff=defaultdict(F,q)
        for k,w in v.items():diff[k]-=w
        add(dict(diff),{'kind':'canonical_min_tie','auxiliary':record['column']})
    skipped=set(thresholds.values())|set(zz['upper_rows'])|set(range(M,M+624))
    multiplier=-floats['inequality_marginals']/floats['scales']
    roworder=sorted((i for i in range(len(rows)) if i not in skipped),key=lambda i:(multiplier[i]<1e-10,-multiplier[i],i))
    for i in roworder:
        add(project(rows[i]),{'kind':'projected_full_row','row':i,'numerical_dual_weight':float(multiplier[i])})
    norm_eq={local[j]:norm[j] for j in support if norm[j]};norm_eq[len(support)]=F(1)
    add(norm_eq,{'kind':'normalization'},True)
    oldW=F(read(BASE/'augmented_lp_exact.json')['W'])
    if attempt=='sameW':
        eq={local[j]:obj[j] for j in support if obj[j]};eq[len(support)]=oldW
        add(eq,{'kind':'fixed_old_exact_W','W':str(oldW)},True)
    write('primal_'+attempt+'_recovery_inputs.json',{
        'input_sha256':{name:digest(HERE/name) for name in ('exact_matrix.json.gz','floating_solver_arrays.npz','epigraph_structure.json','zz_envelope_structure.json','recover.py')},
        'attempt':attempt,'support':support,'unknowns':len(support),
        'positive_original_unknowns':sum(j<ORIGINAL for j in support),
        'positive_new_hidden_unknowns':sum(j>=N for j in support),
        'selected_equations':[[[j,str(v)] for j,v in sorted(eq.items())] for eq in equations],
        'descriptions':descriptions,'all_new_marginal_equalities_included':312,
        'optimizer_calls':0,'support_threshold':1e-11,'active_equation_threshold':1e-10})
    log('exact_primal_recovery_started',attempt=attempt,variables=len(support),equations=len(equations),
        original=sum(j<ORIGINAL for j in support),hidden=sum(j>=N for j in support))
    answer,recovery=sparse_affine_solve(equations,len(support),seed,'primal_'+attempt)
    full=[F()]*(N+NEWN)
    for j,v in zip(support,answer):full[j]=v
    assert min(full)>=0,('negative_core_mass',full.index(min(full)),str(min(full)))
    for j,i in thresholds.items():
        full[j]=max(F(),-dot([[k,v] for k,v in rows[i] if k<ORIGINAL],full))
    for r in zz['auxiliaries']:
        full[r['column']]=min(dot([[k,v] for k,v in rows[i] if k<ORIGINAL],full)
            for i in (r['q_upper_row'],r['v_upper_row']))
    assert min(full)>=0
    assert sum((a*b for a,b in zip(norm,full)),F())==1
    slacks=[dot(row,full) for row in rows]
    assert min(slacks)>=0,('negative_exact_row_slack',slacks.index(min(slacks)),str(min(slacks)),float(min(slacks)))
    W=sum((a*b for a,b in zip(obj,full)),F())
    if attempt=='sameW':assert W==oldW
    assert W>=oldW
    recovery.update(support=support,attempt=attempt,seconds=time.monotonic()-started,
        method='New conditional masses and original positive masses, sparse active-face elimination; all10744 old auxiliaries recomputed canonically.')
    point={'scope':'Exact feasible full624 fixed16-hist necessary LP only; no SPE completion.',
        'O':'1','W':str(W),'W_float':float(W),'strict_half_gap':str(1-2*W),
        'verified_rows':len(rows),'minimum_slack':str(min(slacks)),'exact_verified':True,
        'original_columns':ORIGINAL,'positive_columns':sum(v>0 for v in full),
        'columns':[{**c,'weight':str(v)} for c,v in zip(matrix['columns'],full)]}
    write('augmented_lp_exact.json',point)
    write('primal_exact_audit.json',{'W':str(W),'W_float':float(W),'old_W':str(oldW),
        'exact_increase':str(W-oldW),'increase_float':float(W-oldW),'row_slacks':list(map(str,slacks)),
        'minimum_slack':str(min(slacks)),'recovery':recovery})
    if W==oldW:
        inherited=read(HERE/'inherited_dual_lower_bound.json')
        certificate={**inherited,'equality_to_primal':True,
            'recovery':{'method':'Old exact dual zero-extended in all1248 new rows and4992 new columns.',
                'source_sha256':inherited['source_sha256']}}
        write('exact_dual_certificate.json',certificate)
    log('exact_primal_saved',W=str(W),W_float=float(W),same_old_W=W==oldW,
        exact_increase=str(W-oldW),variables=len(support),rank=recovery['rank'],free=len(recovery['free_variables']))


def dual():
    started=time.monotonic()
    matrix,epi,zz,floats=load();rows=matrix['rows']
    point=read(HERE/'augmented_lp_exact.json');full=[F(c['weight']) for c in point['columns']]
    W=F(point['W']);slacks=[dot(row,full) for row in rows]
    assert min(slacks)>=0 and min(full)>=0
    numerical=-floats['inequality_marginals']/floats['scales']
    simple=set(dict(epi['thresholds']).values())|set(zz['upper_rows'])
    keep=[i for i,v in enumerate(numerical) if v>1e-12 and slacks[i]==0]
    keep.sort(key=lambda i:(0 if M<=i<M+624 else 1 if i in simple else 2,i))
    local={i:k for k,i in enumerate(keep)};n=len(keep)+1;lower_index=n-1;rhs_index=n
    norm=list(map(F,matrix['normalization']));obj=list(map(F,matrix['objective']))
    columns=[j for j,v in enumerate(full) if v>0 or abs(floats['lower_marginals'][j])<1e-12]
    columns.sort(key=lambda j:(0 if j>=N else 1 if j>=ORIGINAL else 2,j))
    trans={j:{} for j in columns}
    for i in keep:
        for j,v in rows[i]:
            if j in trans:trans[j][local[i]]=frac(v)
    equations=[];descriptions=[];seen=set()
    for j in columns:
        eq=trans[j]
        if norm[j]:eq[lower_index]=norm[j]
        if obj[j]:eq[rhs_index]=obj[j]
        if not eq:continue
        sig=tuple(sorted(eq.items()))
        if sig in seen:continue
        seen.add(sig);equations.append(eq);descriptions.append(j)
    equations.append({lower_index:F(1),rhs_index:W})
    write('dual_recovery_inputs.json',{'sha256':{name:digest(HERE/name) for name in (
        'recover.py','exact_matrix.json.gz','floating_solver_arrays.npz','augmented_lp_exact.json','primal_exact_audit.json')},
        'support_rows':keep,'zero_residual_columns':columns,'equation_columns':descriptions,
        'candidate_row_threshold':1e-12,'zero_reduced_cost_threshold':1e-12,
        'exact_positive_slack_rows_removed':True,'optimizer_calls':0})
    log('exact_dual_recovery_started',variables=n,equations=len(equations),rows=len(keep),columns=len(columns))
    answer,recovery=sparse_affine_solve(equations,n,[numerical[i] for i in keep]+[float(W)],'dual')
    lam,lower=answer[:-1],answer[-1]
    assert min(lam)>=0,('negative_dual_weight',str(min(lam)))
    assert lower==W
    residuals=[c-lower*a for c,a in zip(obj,norm)]
    for i,weight in zip(keep,lam):
        assert weight*slacks[i]==0
        for j,v in rows[i]:residuals[j]-=weight*frac(v)
    assert min(residuals)>=0,('negative_dual_residual',residuals.index(min(residuals)),str(min(residuals)))
    assert sum((a*b for a,b in zip(residuals,full)),F())==0
    recovery.update(support_rows=keep,zero_residual_column_indices=columns,
        method='Sparse exact dual elimination; positive numerical multipliers pruned by exact primal complementarity; every residual checked.')
    write('exact_dual_certificate.json',{'verified':True,'normalization_multiplier':str(lower),
        'row_multipliers':[[i,str(w)] for i,w in zip(keep,lam) if w],
        'minimum_coefficient_residual':str(min(residuals)),'residuals':list(map(str,residuals)),
        'equality_to_primal':True,'identity':'objective = lower * normalization + sum_i lambda_i row_i + nonnegative residual',
        'recovery':recovery,'matrix_sha256':digest(HERE/'exact_matrix.json.gz'),'seconds':time.monotonic()-started})
    log('exact_dual_saved',W=str(W),W_float=float(W),positive_rows=sum(v>0 for v in lam),rank=recovery['rank'])


if __name__=='__main__':
    assert len(sys.argv)==2 and sys.argv[1] in ('sameW','freeW','dual')
    attempt=sys.argv[1]
    try:
        if attempt=='dual':dual()
        else:primal(attempt)
    except BaseException:
        write('recovery_'+attempt+'_failure.json',{'attempt':attempt,'traceback':traceback.format_exc(),
            'no_optimizer_rerun':True,'failure_is_not_an_infeasibility_certificate':True})
        raise
