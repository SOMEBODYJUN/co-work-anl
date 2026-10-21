"""Find small-denominator Q for the group strategy. Numeric discovery only."""
from common_static_dual_probe import matrices
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import bmat,csr_matrix,vstack

n,k=3,6;policy={():0}
for a in range(k):
    policy[(a,)]=3 if a<3 else 0
    for b in range(k):policy[(a,b)]=next(c for c in (range(3) if b<3 else range(3,6)) if c not in (a,b))
g,st,c,bs,z=matrices(n,k,policy)
nr,nt=g.shape;nb=len(bs)
for denominator in range(1,21):
    blocks=[]
    for a in range(k):
        blocks.append([csr_matrix(st[a].T/denominator)]+[
            csr_matrix(g.T) if a==b else csr_matrix((nt,nr)) for b in range(k)])
    a=bmat(blocks,format='csr')
    a=vstack([a,csr_matrix(([1.]*nb,(np.zeros(nb,dtype=int),np.arange(nb))),shape=(1,nb+k*nr))])
    lb=np.r_[np.full(k*nt,-np.inf),denominator]
    ub=np.r_[np.tile(c/n,k),denominator]
    result=milp(np.r_[np.zeros(nb),np.ones(k*nr)],integrality=np.r_[np.ones(nb),np.zeros(k*nr)],
                bounds=Bounds(np.zeros(nb+k*nr),np.r_[np.full(nb,denominator),np.full(k*nr,np.inf)]),
                constraints=LinearConstraint(a,lb,ub),options={'time_limit':25.})
    print(denominator,result.message,flush=True)
    if result.success:
        report={'scope':'floating small-denominator discovery only','n':n,'k':k,'denominator':denominator,
                'Q':[{'background':b,'numerator':int(round(v))} for b,v in zip(bs,result.x[:nb]) if v>.5],
                'lambda':result.x[nb:].reshape(k,nr).tolist()}
        Path(__file__).with_name('simple_common_dual_groups.json').write_text(json.dumps(report,indent=2)+'\n')
        print(report['Q']);break
