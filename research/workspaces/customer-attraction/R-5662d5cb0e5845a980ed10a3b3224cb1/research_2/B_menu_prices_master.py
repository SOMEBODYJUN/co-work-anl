"""Required actual-source prices for the B branch's new Yi reply menu.

research_1 identified that ell was present but these seven ordinary common
catalog rows were omitted. Default replays the minimal actual4->B coupled
master; --all-families also prices every explicit actual-B and max-M menu.
Fixed16 old histogram support only: no universal half inference.
"""
from fractions import Fraction as F
from pathlib import Path
import sys,json,time
import numpy as np
from scipy.optimize import linprog
import coupled_B_branch_master as minimal
HERE=Path(__file__).resolve().parent

def build(all_families=False):
    if all_families:
        from maxroot_identity_master import build as full_build
        cols,names,m,obj,norm=full_build()
    else:cols,names,m,obj,norm=minimal.build()
    groups={}
    for j,c in enumerate(cols):
        kind=c['kind']
        if kind=='actual-B-branch-state':key='actual-B-4'
        elif kind=='actual-B-family-state':key='actual-B-'+str(c['source'])
        elif kind=='maximum-root-family-state':key='maximum-M-root'
        else:continue
        groups.setdefault(key,[]).append(j)
    for key,indices in groups.items():
        block=[[F()]*len(cols) for _ in range(7)];block[6][0]=F(1)
        for j in indices:
            c=cols[j];a=tuple(map(int,cols[c['hist_column']]['actual_bits']));ell=c['ell'];whole=sum(a)
            for pos in range(6):
                actualpay=F(a[pos],whole) if a[pos] else F()
                block[pos][j]=actualpay-F(ell,6*(6-pos+sum(a[:pos])))
            block[6][j]=-F(ell,6)
        names += [key+':actual-menu-price:'+str(pos+1) for pos in range(6)]+[key+':menu-CAP']
        m.extend(block)
    return cols,names,m,obj,norm

def main():
    all_families='--all-families' in sys.argv;stem='all_menu_prices' if all_families else 'B_menu_prices'
    start=time.time();cols,names,m,obj,norm=build(all_families);print('built',len(m),'rows',len(cols),'columns',time.time()-start,flush=True)
    if '--verify' in sys.argv:
        report=json.loads((HERE/(stem+'_exact.json')).read_text());ys=[F(c['weight']) for c in report['columns']]
        assert min(ys)>=0 and sum(x*y for x,y in zip(norm,ys))==1
        slacks=[sum(x*y for x,y in zip(row,ys)) for row in m];assert min(slacks)>=0
        W=sum(x*y for x,y in zip(obj,ys));assert W==F(report['W']);print({'rows':len(m),'W':str(W),'minimum_slack':str(min(slacks))});return
    mat=np.array([[float(v) for v in row] for row in m]);scale=np.max(abs(mat),axis=1);scale[scale==0]=1
    sol=linprog([float(v) for v in obj],A_ub=-mat/scale[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(v) for v in norm]],b_eq=[1],bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    out={'scope':'explicit B-menu Yi common actual-source prices; fixed16hist support only, not SPE or universal bound','all_families':all_families,'success':bool(sol.success),'status':sol.message,'W':sol.fun,'rows':len(m),'columns':len(cols),'seconds':time.time()-start};print(json.dumps(out,indent=2),flush=True)
    if sol.success and sol.fun<.5:
        er=minimal.base.cl.exact_point(cols,names,m,obj,norm,sol.x);er['scope']=out['scope'];target=HERE/(stem+'_exact.json')
        if target.exists():raise FileExistsError(target)
        target.write_text(json.dumps(er,indent=2)+'\n');out['exact_verified']=True
    target=HERE/(stem+'_status.json')
    if target.exists():raise FileExistsError(target)
    target.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
