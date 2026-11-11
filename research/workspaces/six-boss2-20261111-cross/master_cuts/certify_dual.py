#!/usr/bin/env python3
"""Attempt an exact dual certificate for the finite 5716-row relaxation.

A successful output is a finite-system optimum, never a universal SPE bound.
Floating marginals only select a candidate support. Every final coefficient,
all 4849 dual residuals, and the primal/dual objective equality are exact.
"""
from fractions import Fraction as F
import json, sys, time, traceback
from pathlib import Path
import numpy as np
from merge_master import HERE, load_matrix, exact_linear_system, save, sha, announce


def main():
    began=time.time();data,rows,obj,norm=load_matrix();fl=np.load(HERE/'solution_float.npz')
    point=json.loads((HERE/'merged_5716_exact.json').read_text());W=F(point['W'])
    estimates=-fl['inequality_marginals']/fl['scales']
    support=[int(i) for i in np.flatnonzero(estimates>1e-10)]
    activecols=[int(j) for j in np.flatnonzero(abs(fl['lower_marginals'])<1e-8)]
    eq=[];rhs=[];origins=[];seen=set()
    for j in activecols:
        rr=tuple(rows[i].get(j,F()) for i in support);b=obj[j]-W*norm[j]
        if not any(rr):
            assert b==0,(j,b)
            continue
        key=(rr,b)
        if key in seen:continue
        seen.add(key);eq.append(list(rr));rhs.append(b);origins.append(j)
    announce('dual-reconstruction-start',positive_multiplier_support=len(support),candidate_column_equations=len(eq))
    vals,selected=exact_linear_system(eq,rhs)
    assert min(vals)>=0
    residual=[obj[j]-W*norm[j]-sum(v*rows[i].get(j,F()) for i,v in zip(support,vals)) for j in range(data['column_count'])]
    assert min(residual)>=0,(residual.index(min(residual)),min(residual))
    weights=[F(c['weight']) for c in point['columns']]
    assert sum(weights[j]*residual[j] for j in range(len(weights)))==0
    report={'scope':'Exact optimum of fixed sixteen-histogram 5716-row necessary relaxation only; not universal six-player SPE bound.','status':'passed','dual_value':str(W),'primal_value':point['W'],'minimum_dual_residual':str(min(residual)),'minimum_multiplier':str(min(vals)),'positive_multipliers':sum(v>0 for v in vals),'matrix_sha256':sha(HERE/'master_5716_exact.json.gz'),'point_sha256':sha(HERE/'merged_5716_exact.json'),'row_multipliers':[{'row_index':i,'row_name':data['rows'][i]['name'],'weight':str(v)} for i,v in zip(support,vals) if v],'normalization_multiplier':str(W),'residuals':list(map(str,residual)),'selected_column_equations':[origins[k] for k in selected],'seconds':time.time()-began}
    save('dual_exact.json',report)
    announce('exact-dual-certified',**{k:v for k,v in report.items() if k not in ('row_multipliers','residuals','selected_column_equations')})

if __name__=='__main__':
    start=time.time()
    try:main()
    except Exception as exc:
        save('dual_attempt_failure.json',{'error':repr(exc),'traceback':traceback.format_exc(),'seconds':time.time()-start,'scope':'No exact dual certificate claimed from this failed support attempt.'})
        raise
