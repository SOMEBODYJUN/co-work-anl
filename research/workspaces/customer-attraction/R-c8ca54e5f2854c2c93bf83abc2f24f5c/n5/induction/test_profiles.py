from itertools import product,combinations,combinations_with_replacement
from math import comb
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location("fourrem", "tests/audits/customer_attraction_four_remaining_profit.py")
fourrem=importlib.util.module_from_spec(spec); spec.loader.exec_module(fourrem)
spec3=importlib.util.spec_from_file_location("threerem", "tests/audits/customer_attraction_three_remaining_profit.py")
threerem=importlib.util.module_from_spec(spec3); spec3.loader.exec_module(threerem)
rebate3={(p,*a,d):float(min(sum(F(v)*F(p)**j for j,v in enumerate(threerem.coefficients(*a,q,r,d,l)))/(30*(p+1)*(p+2)*(p+3)) for q,r in product((0,1),repeat=2) for l in range(4))) for p in (0,1,2) for a in product((0,1),repeat=3) for d in range(4)}
rebate4={(p,*a):float(min(fourrem.direct_rho((*a,*b),p) for b in product((0,1),repeat=3))) for p in (0,1) for a in product((0,1),repeat=4)}
names=list('ABCDE')+list('QRST')
paths=[tuple(range(5)),(4,5,6,7,8)]
bits=np.array(list(product(range(2),repeat=len(names))),float)
# 512 base states; six copies e=0..5
x=np.repeat(bits,6,axis=0); e=np.tile(np.arange(6),len(bits)); o=(e>0).astype(float)
w=(x[:,:5].sum(axis=1)>0).astype(float)
rows=[]; rnames=[]
def row(n,v): rnames.append(n); rows.append(v)
def prof(p,k):
    return sum(comb(int(ee),j)*comb(5-int(ee),k-j)*(j/(pp+j) if j else 0) for j in range(k+1) if 0<=k-j<=5-int(ee) and j<=int(ee))
def pvec(p,k):
    return np.array([prof(pp,k) for pp in range(6) for ee in []])
def optprof(p,k):
    z=np.zeros(len(x))
    for j in range(1,k+1):
        nums=np.array([comb(int(ee),j)*comb(5-int(ee),k-j) if j<=ee and k-j<=5-ee else 0 for ee in e])
        z+=nums*j/(p+j)
    return z
us=[]
for h,path in enumerate(paths):
    counts=x[:,path].sum(axis=1); den=np.maximum(1,counts)
    u=[x[:,a]/den for a in path]; us.append(u)
    for i,a in enumerate(path):
        if h and i==0: continue
        p=x[:,path[:i]].sum(axis=1); rem=5-i
        for j,b in enumerate(names): row(f'{h}:{i}:K{b}',u[i]-x[:,j]/(p+rem))
        row(f'{h}:{i}:opt',5*u[i]-e/(p+rem))
    for k in (2,3,4):
        i=5-k; p=x[:,path[:i]].sum(axis=1)
        V=sum(u[i:])
        if k==2:
            beta=1; V=V+x[:,path[i]]/((p+1)*(p+2))
        elif k==3: beta=5/3
        else:
            beta=1499/750
            reb=np.array([rebate4[(int(pp),*map(int,aa))] for pp,aa in zip(p,x[:,path[i:]])])
            V=V-reb/beta
        opr=optprof(p,k)
        if k==3:
            for j in range(4):
                nums=np.array([comb(int(ee),j)*comb(5-int(ee),k-j) if j<=ee and k-j<=5-ee else 0 for ee in e])
                opr+=nums*np.array([rebate3[(int(pp),*map(int,aa),j)] for pp,aa in zip(p,x[:,path[i:]])])
        row(f'{h}:tail{k}:opt',comb(5,k)*beta*V-opr)
        for inds in combinations_with_replacement(range(len(names)),k):
            q=x[:,inds].sum(axis=1)
            qr=q/np.maximum(1,p+q)
            if k==3:
                qr+=np.array([rebate3[(int(pp),*map(int,aa),int(qq))] for pp,aa,qq in zip(p,x[:,path[i:]],q)])
            row(f'{h}:tail{k}:cmp'+''.join(names[j] for j in inds),beta*V-qr)
row('rootE',us[0][0]-us[1][0])
M=np.asarray(rows)
print('shape',M.shape,flush=True)
sol=linprog(-o,A_ub=csr_matrix(-M),b_ub=np.zeros(len(rows)),A_eq=csr_matrix(w[None,:]),b_eq=[1.],bounds=(0,None),method='highs')
print(sol.message,flush=True)
if sol.success:
 print('BETA',-sol.fun,flush=True)
 inds=np.flatnonzero(abs(sol.ineqlin.marginals)>1e-7)
 print('DUAL',[(rnames[i],-sol.ineqlin.marginals[i]) for i in inds],flush=True)
 atoms=np.flatnonzero(sol.x>1e-7)
 print('ATOMS',[(tuple(map(int,x[i])),int(e[i]),sol.x[i]) for i in atoms],flush=True)
 np.savez(Path(__file__).with_suffix('.npz'),x=x,e=e,w=w,M=M,names=rnames,primal=sol.x,dual=-sol.ineqlin.marginals,beta=-sol.fun)
