#!/usr/bin/env python3
"""Exact dual recovery with separate per-row denominator scaling.

For selected multiplier row i let L_i A_i be integral. Let D*(c-W*n) be
integral. Substitute lambda_i=L_i*z_i/D, so the exact system is
sum_i (L_i*A_ij) z_i = D*(c_j-W*n_j). This avoids mixing the denominators of
all different rows in each column equation. Float QR only selects equations;
all recovered multipliers and every final column residual are exact.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,datetime,json,math,os,platform,sys,time
import numpy as np
from scipy.linalg import qr
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
import extend_master as engine
from merge_master import HERE,sha


def run(config,support_tolerance,float_file):
    start=time.time();data,rows,obj,norm=engine.load();floating=np.load(HERE/(float_file if float_file else engine.STEM+'_float.npz'));point=engine.read('exact');W=F(point['W'])
    support=[int(i) for i in np.flatnonzero(-floating['inequality_marginals']/floating['scales']>support_tolerance)]
    active=[j for j,c in enumerate(point['columns']) if F(c['weight'])>0 or abs(floating['lower_marginals'][j])<1e-12]
    equations=[];rhs=[];origins=[];seen=set()
    for j in active:
        row=tuple(rows[i].get(j,F()) for i in support);b=obj[j]-W*norm[j]
        if not any(row):assert b==0;continue
        if (row,b) in seen:continue
        seen.add((row,b));equations.append(row);rhs.append(b);origins.append(j)
    n=len(support)
    arr=np.array([[float(v) for v in row] for row in equations]);sc=np.max(abs(arr),axis=1);sc[sc==0]=1
    _,r,piv=qr((arr/sc[:,None]).T,mode='economic',pivoting=True);diag=np.abs(np.diag(r));rank=int(sum(diag>1e-10*max(diag[0],1)))
    assert rank==n,(rank,n)
    chosen=[int(i) for i in piv[:n]]
    L=[math.lcm(*(v.denominator for v in rows[i].values())) for i in support]
    D=math.lcm(*(b.denominator for b in rhs))
    entries={};bentries={}
    for k,q in enumerate(chosen):
        for i,v in enumerate(equations[q]):
            if v:
                scaled=v*L[i];assert scaled.denominator==1;entries[k,i]=ZZ(scaled.numerator)
        if rhs[q]:
            scaled=rhs[q]*D;assert scaled.denominator==1;bentries[k,0]=ZZ(scaled.numerator)
    engine.log('scaled-dual-reconstructing',multipliers=n,candidate_equations=len(equations),maximum_row_denominator_digits=max(len(str(v)) for v in L),rhs_denominator_digits=len(str(D)))
    a=DomainMatrix.from_dok(entries,(n,n),ZZ);b=DomainMatrix.from_dok(bentries,(n,1),ZZ)
    numer,denom=a.solve_den(b,method='rref')
    zs=[F(int(v[0]),int(denom)) for v in numer.to_list()]
    values=[z*F(l,D) for z,l in zip(zs,L)]
    if min(values)<0:
        engine.write('dual_support_diagnostic',{'support':support,'chosen_columns':[origins[i] for i in chosen],'negative_values':[{'row_index':i,'weight':str(v),'weight_float':float(v),'solver_weight':float(-floating['inequality_marginals'][i]/floating['scales'][i])} for i,v in zip(support,values) if v<0],'all_values':list(map(str,values)),'method':'exact integer column scaling','seconds':time.time()-start})
    assert min(values)>=0
    residual=[obj[j]-W*norm[j] for j in range(len(obj))]
    for i,v in zip(support,values):
        for j,c in rows[i].items():residual[j]-=v*c
    if min(residual)<0:
        engine.write('dual_residual_diagnostic',{'support_tolerance_float':support_tolerance,'negative_columns':[{'column':j,'residual':str(v),'display':float(v)} for j,v in enumerate(residual) if v<0],'weights':[{'row_index':i,'weight':str(v)} for i,v in zip(support,values)],'seconds':time.time()-start})
    assert min(residual)>=0,(residual.index(min(residual)),min(residual))
    x=[F(c['weight']) for c in point['columns']]
    assert sum(v*r for v,r in zip(x,residual))==0
    for i,v in zip(support,values):assert v*sum(c*x[j] for j,c in rows[i].items())==0
    out={'scope':data['scope'],'status':'passed','primal_value':str(W),'dual_value':str(W),'normalization_multiplier':str(W),'minimum_multiplier':str(min(values)),'minimum_dual_residual':str(min(residual)),'positive_multipliers':sum(v>0 for v in values),'matrix_sha256':sha(HERE/(engine.STEM+'_matrix.json.gz')),'point_sha256':sha(HERE/(engine.STEM+'_exact.json')),'row_multipliers':[{'row_index':i,'row_name':data['rows'][i]['name'],'weight':str(v)} for i,v in zip(support,values) if v],'residuals':list(map(str,residual)),'selected_column_equations':[origins[i] for i in chosen],'reconstruction':'Per-row integer column scaling lambda_i=L_i*z_i/D; final full rational residual and complementarity verification.','row_denominator_multipliers':[{'row_index':i,'L':str(l)} for i,l in zip(support,L)],'rhs_denominator_multiplier':str(D),'seconds':time.time()-start}
    engine.write('dual',out)
    engine.log('scaled-exact-dual-certified',**{k:v for k,v in out.items() if k not in ('row_multipliers','residuals','selected_column_equations','row_denominator_multipliers')})


def main():
    parser=argparse.ArgumentParser();parser.add_argument('config');parser.add_argument('--support-tolerance',type=float,default=1e-10);parser.add_argument('--float-file');args=parser.parse_args();cp=Path(args.config).resolve();assert cp.is_relative_to(HERE)
    config=json.loads(cp.read_text());engine.STEM=config['stem'];assert all(c.isalnum() or c=='_' for c in engine.STEM)
    started=time.time();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();success=False
    try:run(config,args.support_tolerance,args.float_file);success=True
    finally:
        engine.write('execution_scaled_dual',{'command':[sys.executable,'-B',str(Path(__file__).resolve()),str(cp),'--support-tolerance',str(args.support_tolerance)]+(['--float-file',args.float_file] if args.float_file else []),'cwd':os.getcwd(),'started_utc':stamp,'elapsed_seconds':time.time()-started,'success':success,'python':platform.python_version(),'script_sha256':sha(__file__),'engine_sha256':sha(HERE/'extend_master.py'),'config_sha256':sha(cp)})
if __name__=='__main__':main()
