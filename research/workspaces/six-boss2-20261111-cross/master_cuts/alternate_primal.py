#!/usr/bin/env python3
"""Find a separately named exact primal candidate with altered floating scaling.

All original points and matrices remain untouched. Float solver output only
selects a basis; the imported exact reconstruction verifies the entire matrix.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,datetime,json,os,platform,sys,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
import extend_master as engine
from merge_master import HERE,sha

def main():
    ap=argparse.ArgumentParser();ap.add_argument('config');ap.add_argument('output_stem');ap.add_argument('--method',default='highs-ds',choices=('highs-ds','highs-ipm'));args=ap.parse_args();cp=Path(args.config).resolve();cfg=json.loads(cp.read_text());stem=args.output_stem
    assert stem and all(c.isalnum() or c=='_' for c in stem)
    assert not list(HERE.glob(stem+'_*')),'Require a fresh output stem'
    engine.STEM=cfg['stem'];data,rows,obj,norm=engine.load();oldpoint=engine.read('exact');base_matrix=HERE/(engine.STEM+'_matrix.json.gz');base_point=HERE/(engine.STEM+'_exact.json');start=time.time()
    rr=[];cc=[];vv=[]
    for i,row in enumerate(rows):
        for j,v in row.items():rr.append(i);cc.append(j);vv.append(-float(v))
    mat=csr_matrix((vv,(rr,cc)),shape=(len(rows),len(obj)))
    options={'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10,'time_limit':120}
    if args.method=='highs-ipm':options['ipm_optimality_tolerance']=1e-12
    sol=linprog(list(map(float,obj)),A_ub=mat,b_ub=np.zeros(len(rows)),A_eq=csr_matrix([list(map(float,norm))]),b_eq=[1],bounds=(0,None),method=args.method,options=options)
    engine.STEM=stem
    engine.write('float_status',{'success':bool(sol.success),'message':sol.message,'W_float':None if sol.fun is None else float(sol.fun),'method':args.method,'external_row_scaling':False,'seconds':time.time()-start,'source_matrix_sha256':sha(base_matrix),'old_point_sha256':sha(base_point),'float_only':True})
    engine.log('alternate-float',success=bool(sol.success),W_float=sol.fun,seconds=time.time()-start);assert sol.success
    np.savez(HERE/(stem+'_float.npz'),x=sol.x,scaled_slacks=sol.ineqlin.residual,inequality_marginals=sol.ineqlin.marginals,lower_marginals=sol.lower.marginals,scales=np.ones(len(rows)))
    engine.load=lambda:(data,rows,obj,norm)
    engine.reconstruct()
    point=engine.read('exact');W=F(point['W']);oldW=F(oldpoint['W'])
    report={'scope':'Alternate exact feasible point on identical 5752 matrix; no optimality claim until separately verified dual.','matrix_file':base_matrix.name,'matrix_sha256':sha(base_matrix),'old_point_file':base_point.name,'old_point_sha256':sha(base_point),'new_point_file':stem+'_exact.json','new_point_sha256':sha(HERE/(stem+'_exact.json')),'old_W':str(oldW),'new_W':str(W),'exact_W_difference':str(W-oldW),'difference_display':float(W-oldW),'seconds':time.time()-start,'execution':{'command':[sys.executable,'-B',str(Path(__file__).resolve()),str(cp),stem,'--method',args.method],'cwd':os.getcwd(),'python':platform.python_version(),'script_sha256':sha(__file__),'engine_sha256':sha(HERE/'extend_master.py'),'helper_sha256':sha(HERE/'merge_master.py')}}
    engine.write('comparison',report);engine.log('alternate-exact-comparison',**report)
if __name__=='__main__':main()
