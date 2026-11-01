"""Six-player maximum-root path with two genuine terminal-theme copies.

All inequalities are ordinary SPE IC, safe floors, capacity, actual last IC,
and the established arbitrary-background two-remaining tax. A returned
float vector is discovery only; no theorem is claimed without exact replay.
"""
from itertools import product
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog

def qf(n,d):return F(n,d) if n else F(0)
def data(n=6,exact=False):
    # P0=M,A,...,last; P1=M,last,Q...; P2=M,A,last,R...
    count=n+(n-2)+(n-3)
    paths=[tuple(range(n)),(0,n-1)+tuple(range(n,n+n-2)),(0,1,n-1)+tuple(range(n+n-2,count))]
    starts=[1,2,3]
    names=[]
    for j in range(1,count):names.append(f'CAP:{j}')
    names+=['copy:second','copy:third']
    for pi,path in enumerate(paths):
        names += [f'P{pi}:pairO',f'P{pi}:lastO']
        for pos in range(starts[pi],n):
            for query in range(count):names.append(f'P{pi}:floor:{pos}:{query}')
    mat=[];root=[];maxcol=[]
    for bits in product(range(2),repeat=count):
        pays=[]
        for path in paths:
            den=sum(bits[j] for j in path)
            pays.append([qf(bits[j],den) for j in path])
        vals=[F(bits[0]-bits[j]) for j in range(1,count)]
        vals += [pays[0][1]-pays[1][1],pays[0][2]-pays[2][2]]
        for pi,path in enumerate(paths):
            prefix=sum(bits[j] for j in path[:-2]);lastpre=prefix+bits[path[-2]]
            h=pays[pi][-2]+pays[pi][-1]+F(bits[path[-2]],(prefix+1)*(prefix+2))
            vals += [F(n,2)*h+F(prefix,prefix+1),n*pays[pi][-1]+F(lastpre,lastpre+1)]
            for pos in range(starts[pi],n):
                denom=n-pos+sum(bits[j] for j in path[:pos])
                vals += [pays[pi][pos]-F(t,denom) for t in bits]
        mat.append(vals if exact else [float(v) for v in vals]);root.append(pays[0][0] if exact else float(pays[0][0]));maxcol.append(bits[0])
    if exact:return names,mat,root,maxcol
    return names,np.array(mat),np.array(root),np.array(maxcol)

def solve(n=6):
    names,mat,root,mc=data(n);nr=len(names)
    amat=np.column_stack((mat,-root,-mc));rhs=np.zeros(len(root))
    orow=np.array([-1 if name.endswith('O') else 0 for name in names]+[0,0])
    amat=np.vstack((amat,orow));rhs=np.append(rhs,-1.)
    out=[]
    for x in (1/n,0.18,0.2,0.25,0.3,0.4,0.5,1.):
        obj=np.zeros(nr+2);obj[-2:]=[x,1]
        lp=linprog(obj,A_ub=amat,b_ub=rhs,bounds=[(0,None)]*(nr+1)+[(None,None)],method='highs')
        row={'r_over_K':x,'status':lp.message}
        if lp.success:row.update(B=lp.x[-2],C=lp.x[-1],O_over_K=lp.fun,active={name:float(v) for name,v in zip(names,lp.x) if v>1e-8})
        out.append(row)
    return {'n':n,'states':len(root),'rows':nr,'bounds':out}
if __name__=='__main__':print(json.dumps(solve(),indent=2))
