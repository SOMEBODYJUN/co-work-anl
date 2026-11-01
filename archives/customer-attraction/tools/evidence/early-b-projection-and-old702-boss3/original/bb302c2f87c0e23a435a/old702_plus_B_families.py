"""Full coefficient-domain primal lift: 702 rows plus all actual i->B graphs.

For each actual type, a separate conditional distribution supplies each
branch family's hidden topic bits and endpoint reply count. All families
share the complete actual-type marginal and the same scalar K. This is a
larger domain than true games; a feasible bad point is never an SPE.
"""
from itertools import product
from pathlib import Path
import sys,json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
from max_branch_lp import branch_rows

ROOT=Path(__file__).resolve().parents[5]
OLD=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
sys.path.insert(0,str(OLD))
import new_reply_budget as nr

def solve(sources=(0,1,2,3)):
    n=6;types,old=nr.old_system();nt=len(types);Kcol=nt;nv=nt+1
    families=[];nrw=len(old)
    for source in sources:
        states=list(product(tuple(product(range(2),repeat=n-source-1)),(0,n)))
        names,_=branch_rows((0,)*7,(source,n-1),states[0][0],0,0)
        families.append((source,states,names,nv,nrw));nv+=nt*len(states);nrw+=len(names)
    ur=[];uc=[];uv=[];er=[];ec=[];ev=[]
    def add_u(row,col,val):
        if val:ur.append(row);uc.append(col);uv.append(float(-val))
    def add_e(row,col,val):er.append(row);ec.append(col);ev.append(float(val))
    for i,(_,row) in enumerate(old):
        for j,val in enumerate(row):add_u(i,j,val)
    for j,(bits,d) in enumerate(types):
        if d:add_e(0,j,1)
    for fi,(source,states,names,startcol,startrow) in enumerate(families):
        for i,name in enumerate(names):
            if name.startswith('CAP:'):add_u(startrow+i,Kcol,1)
        for ti,(bits,d) in enumerate(types):
            eqrow=1+fi*nt+ti;add_e(eqrow,ti,-1)
            for si,(hidden,ell) in enumerate(states):
                col=startcol+ti*len(states)+si;add_e(eqrow,col,1)
                nn,vals=branch_rows(bits+(0,),(source,n-1),hidden,d,ell)
                assert nn==names
                for i,val in enumerate(vals):add_u(startrow+i,col,val)
    amat=coo_matrix((uv,(ur,uc)),shape=(nrw,nv)).tocsc();eqmat=coo_matrix((ev,(er,ec)),shape=(1+nt*len(families),nv)).tocsc()
    obj=np.zeros(nv)
    for i,(bits,d) in enumerate(types):obj[i]=int(any(bits))
    rhs=np.zeros(eqmat.shape[0]);rhs[0]=1
    lp=linprog(obj,A_ub=amat,b_ub=np.zeros(nrw),A_eq=eqmat,b_eq=rhs,bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    out={'scope':'full 448 types, old 702 plus separately lifted actual-i-to-B branch families; float only','sources':[s+1 for s in sources],'rows':nrw,'equality_rows':eqmat.shape[0],'variables':nv,'nonzero_coefficients':amat.nnz+eqmat.nnz,'status':lp.message}
    if lp.success:
        out.update(W=lp.fun,ratio=1/lp.fun,K=float(lp.x[Kcol]),active_types=[{'actual_bits':''.join(map(str,types[j][0])),'d':types[j][1],'mass':float(v)} for j,v in enumerate(lp.x[:nt]) if v>1e-8],active_family_rows={str(source+1):{name:float(-lp.ineqlin.marginals[startrow+i]) for i,name in enumerate(names) if -lp.ineqlin.marginals[startrow+i]>1e-8} for source,states,names,startcol,startrow in families})
    return out
if __name__=='__main__':print(json.dumps(solve(),indent=2))
