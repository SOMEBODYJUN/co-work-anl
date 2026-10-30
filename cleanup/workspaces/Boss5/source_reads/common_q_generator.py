"""Search for one static Q proving ui>=vn throughout an entire full SPE cone.

For EACH queried action a require ui - E_Q f_B(a)=G^T lambda_a+r_a,
lambda_a,r_a>=0. This is sufficient for all customer weights and ALL p.
"""
from attack import *
from scipy.sparse import lil_matrix

def common(cone,target):
    nr,nb= len(cone.rows),len(cone.Bs)
    A=lil_matrix((cone.m*cone.k,nb+cone.m*nr))
    rhs=[]
    for a in range(cone.m):
        for k in range(cone.k):
            i=a*cone.k+k
            for j,row in enumerate(cone.Frows):A[i,j]=float(row[a][k])
            for j,row in enumerate(cone.rows):A[i,nb+a*nr+j]=float(row[k])
            rhs.append(float(target[k]))
    eq=lil_matrix((1,nb+cone.m*nr));eq[0,:nb]=1
    obj=np.r_[np.zeros(nb),np.ones(cone.m*nr)]
    res=linprog(obj,A_ub=A.tocsr(),b_ub=rhs,A_eq=eq.tocsr(),b_eq=[1],bounds=(0,None),method='highs')
    if not res.success:return {'success':False,'status':res.message}
    vals=[F(float(x)).limit_denominator(10**8) for x in res.x]
    Q=vals[:nb]; lambdas=[vals[nb+a*nr:nb+(a+1)*nr] for a in range(cone.m)]
    residual=[[target[k]-sum(Q[j]*cone.Frows[j][a][k] for j in range(nb))-sum(lambdas[a][j]*cone.rows[j][k] for j in range(nr)) for k in range(cone.k)] for a in range(cone.m)]
    exact=sum(Q)==1 and min(vals)>=0 and min(x for r in residual for x in r)>=0
    return {'success':True,'exact':exact,'Q':[(B,q) for B,q in zip(cone.Bs,Q) if q],
            'lambda':[[{'row':cone.rows[j],'coefficient':x} for j,x in enumerate(lam) if x] for lam in lambdas],
            'residual':residual,'float_objective':res.fun,'sparse_duals':sum(bool(x) for x in vals[nb:])}

def run_common():
    for name in ['aggregate_theta_failure','root_tax_failure','global_decorrelation_failure']:
        cone=load(name)
        for i,targ in enumerate(cone.u):
            r=common(cone,targ)
            print(name,i,'success/exact',r.get('success'),r.get('exact'),'Q',r.get('Q'),'duals',r.get('sparse_duals'),flush=True)
            (OUT/f'common_Q_{name}_{i}.json').write_text(json.dumps(serial(r),indent=2))

if __name__=='__main__':run_common()
