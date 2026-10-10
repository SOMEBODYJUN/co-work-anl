from symmetric_ne_bridge_attack import *
from itertools import product

def solve_exact(M,b):
    d=len(M[0]); a=[list(row)+[rhs] for row,rhs in zip(M,b)]
    pivots=[];r=0
    for c in range(d):
        k=next((k for k in range(r,len(a)) if a[k][c]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r]
        div=a[r][c];a[r]=[x/div for x in a[r]]
        for k in range(len(a)):
            if k!=r and a[k][c]:
                t=a[k][c];a[k]=[x-t*y for x,y in zip(a[k],a[r])]
        pivots.append(c);r+=1
    if any(not any(row[:-1]) and row[-1] for row in a):raise RuntimeError('Inconsistent system')
    if len(pivots)!=d:raise RuntimeError('Underdetermined support')
    x=[F(0)]*d
    for r,c in enumerate(pivots):x[c]=a[r][-1]
    return x


def extract(n,m,policy,q,label):
    masks,hist,finish,coeff,gamma,cov=setup(n,m,policy)
    probs=[sum(q[a] for a in range(m) if T>>a&1) for T in masks]
    psi=tuple(1-(1-t)**n for t in probs)
    g=tuple(F(1) if t==0 else (1-(1-t)**n)/(n*t) for t in probs)
    alpha=[tuple(g[t] if T>>a&1 else F(0) for t,T in enumerate(masks)) for a in range(m)]
    nerows=[tuple(w-n*u for w,u in zip(psi,alpha[a])) for a in range(m)]
    rows=list(gamma)+nerows
    obj=tuple(w-v for w,v in zip(cov,psi))
    res=linprog(np.array(obj,dtype=float),A_ub=-np.array(rows,dtype=float),
                b_ub=np.zeros(len(rows)),A_eq=np.array([cov],dtype=float),
                b_eq=[1],bounds=(0,None),method='highs')
    support=[j for j,x in enumerate(res.ineqlin.marginals) if -x>1e-8]
    f_res=np.array(obj,dtype=float)+np.array(rows,dtype=float).T@res.ineqlin.marginals
    active=[i for i,x in enumerate(f_res) if abs(x)<1e-8]
    M=[[rows[j][i] for j in support] for i in active]
    b=[obj[i] for i in active]
    sol=solve_exact(M,b)
    lam=[F(0)]*len(rows)
    for j,x in zip(support,sol):lam[j]=x
    residual=[a-sum(lam[j]*rows[j][i] for j in range(len(rows))) for i,a in enumerate(obj)]
    ans={'label':label,'scope':'One fixed full policy and fixed iid q, and all weights for which q is symmetric Nash.',
         'q':list(map(str,q)), 'n':n,'m':m,'fraction_valid':min(residual)>=0,
         'minimum_residual':str(min(residual)),'sparse_spe':[], 'sparse_ne':[],
         'residuals':{str(T):str(x) for T,x in zip(masks,residual) if x},
         'minimum_multiplier':str(min(lam))}
    for j,x in enumerate(lam):
        if not x:continue
        if j<len(gamma):
            ans['sparse_spe'].append({'history':list(hist[j//m]),'deviation':j%m,'lambda':str(x)})
        else:ans['sparse_ne'].append({'action':j-len(gamma),'lambda':str(x)})
    Path(__file__).with_name(label+'.json').write_text(json.dumps(ans,indent=2))
    print(json.dumps(ans,indent=2))


if __name__=='__main__':
    extract(3,6,policy36,[F(1,6)]*6,'36_uniform_iid_ne_dual')
