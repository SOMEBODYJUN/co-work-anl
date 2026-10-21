"""Common transport feasibility for all retained pair orbit rows, fixed marginals.

Numerical discovery only. All output is a necessary-condition relaxation,
not an SPE construction or a welfare theorem.
"""
from pathlib import Path
import sys,json,hashlib
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix,csr_matrix
HERE=Path(__file__).resolve().parent;ACTOR=HERE.parent
sys.path.insert(0,str(ACTOR/'round4_coupling'))
from pair_transport import LM,source_data,ORBITS
from joint_transport import family


def solve(target='AB',source='second',terminal=False):
    path=ACTOR/'round5_pricing/exact_optimum_primal_cross_pair.json'
    atoms=json.loads(path.read_text())['atoms'];masses=[F(a['exact_mass']) for a in atoms]
    pair_specs=[(u,v,o) for u,v in combinations_with_replacement(range(3),2) for o in range(5)]
    names=[f'pair{u}{v}:{ORBITS[o]}' for u,v,o in pair_specs]
    allvars=[];marg=[];rc=[];blocks=[]
    for ai,(atom,mass) in enumerate(zip(atoms,masses)):
        src=family(atom,source);tar=family(atom,target);q=len(src)
        fixed=list(map(int,atom['bits']));prefix=fixed[0] if source=='second' else fixed[0]+fixed[1 if source=='AB' else 4]
        groups=[]
        for t in (0,1):
            su=sorted(set(z for z in src if z[0]==t));tu=sorted(set(z for z in tar if z[0]==t))
            index={}
            for si,s in enumerate(su):
                p=prefix+sum(s[:-2]);f,l=s[-2:]
                H=F(f+l,p+f+l) if f+l else F(0);H+=F(f,(p+1)*(p+2))
                for ti,z in enumerate(tu):
                    idx=len(allvars);allvars.append((ai,s,z));index[si,ti]=idx
                    coeff=[]
                    for u,v,o in pair_specs:
                        B=sum(w[u] for w in tar);C=sum(w[v] for w in tar);K=sum(w[u]*w[v] for w in tar)
                        n,L,M=LM(q,z[u],z[v],B,C,K)[o]
                        coeff.append(n*H-F(L,p+1)+F(M,(p+1)*(p+2)))
                    rc.append(coeff)
            for si,s in enumerate(su):marg.append(([(index[si,ti],1) for ti in range(len(tu))],mass*src.count(s)))
            for ti,z in enumerate(tu):marg.append(([(index[si,ti],1) for si in range(len(su))],mass*tar.count(z)))
            groups.append((su,tu))
        blocks.append(groups)
    Aeq=lil_matrix((len(marg),len(allvars)));b=[]
    for i,(ent,rhs) in enumerate(marg):
        for j,c in ent:Aeq[i,j]=c
        b.append(float(rhs))
    R=np.asarray([[float(c) for c in col] for col in rc]).T
    # max common epsilon after normalizing rows by multiplicity (orbit size).
    norms=np.asarray([1 if o==0 else 4 if o<4 else 12 for _,_,o in pair_specs],dtype=float)
    Au=np.column_stack((-R,norms));Ae=csr_matrix(np.column_stack((Aeq.toarray(),np.zeros(len(marg)))))
    c=np.zeros(len(allvars)+1);c[-1]=-1
    res=linprog(c,A_ub=csr_matrix(Au),b_ub=np.zeros(len(names)),A_eq=Ae,b_eq=np.asarray(b),bounds=[(0,None)]*len(allvars)+[(None,None)],method='highs')
    out={'scope':'Floating common-transport necessary-condition feasibility only', 'source':source,'target':target,'source_path':str(path),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'variables':len(allvars),'marginal_equalities':len(marg),'row_count':len(names),'success':res.success,'message':res.message}
    if res.success:
        lam=-res.ineqlin.marginals
        out.update({'max_common_normalized_margin':float(res.x[-1]),'joint_weights':{n:float(v) for n,v in zip(names,lam) if v>1e-9},'minimum_marginal_residual':float(np.min(res.eqlin.residual))})
    return out

if __name__=='__main__':
    reports=[solve(t) for t in ('AB','AE')]
    (HERE/'joint_pair_feasibility.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(json.dumps(reports,indent=2))
