#!/usr/bin/env python3
"""Find an alternate dual support on the exact primal point's active face.

This is discovery only. A separate scaled_dual run must recover rational
weights and verify all columns; this script never certifies an optimum.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,os,platform,sys,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
import extend_master as engine
from merge_master import HERE,sha

def main():
    parser=argparse.ArgumentParser();parser.add_argument('config');args=parser.parse_args();cp=Path(args.config).resolve();cfg=json.loads(cp.read_text());engine.STEM=cfg['stem'];start=time.time()
    data,rows,obj,norm=engine.load();point=engine.read('exact');W=F(point['W']);x=[F(c['weight']) for c in point['columns']]
    active=[i for i,row in enumerate(rows) if sum(v*x[j] for j,v in row.items() if x[j])==0]
    scales=[float(max((abs(v) for v in row.values()),default=F(1))) for row in rows]
    rr=[];cc=[];vv=[]
    for local,i in enumerate(active):
        for j,v in rows[i].items():rr.append(j);cc.append(local);vv.append(float(v)/scales[i])
    mat=csr_matrix((vv,(rr,cc)),shape=(len(obj),len(active)));rhs=np.array([float(c-W*n) for c,n in zip(obj,norm)])
    positive=[j for j,v in enumerate(x) if v>0]
    sol=linprog(np.ones(len(active)),A_ub=mat,b_ub=rhs,A_eq=mat[positive,:],b_eq=rhs[positive],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-10,'primal_feasibility_tolerance':1e-10,'time_limit':60})
    result={'scope':'Float support discovery on exact primal-active rows; no exact optimum assertion.','success':bool(sol.success),'message':sol.message,'active_rows':len(active),'positive_primal_columns':len(positive),'seconds':time.time()-start,'point_sha256':sha(HERE/(engine.STEM+'_exact.json'))}
    if sol.success:
        terms=np.zeros(len(rows))
        for i,t in zip(active,sol.x):terms[i]=t
        residual=rhs-mat@sol.x
        np.savez(HERE/(engine.STEM+'_dual_l1_float.npz'),inequality_marginals=-terms,scales=np.array(scales),lower_marginals=residual,x=np.array(list(map(float,x))))
        result.update({'positive_multipliers_1e_10':int(sum(terms/np.array(scales)>1e-10)),'minimum_residual_float':float(min(residual)),'objective_float':float(sol.fun),'iterations':int(sol.nit)})
    result['execution']={'command':[sys.executable,'-B',str(Path(__file__).resolve()),str(cp)],'cwd':os.getcwd(),'python':platform.python_version(),'script_sha256':sha(__file__),'config_sha256':sha(cp)}
    engine.write('dual_repair_float',result);print(json.dumps(result,ensure_ascii=False),flush=True)
    assert sol.success
if __name__=='__main__':main()
