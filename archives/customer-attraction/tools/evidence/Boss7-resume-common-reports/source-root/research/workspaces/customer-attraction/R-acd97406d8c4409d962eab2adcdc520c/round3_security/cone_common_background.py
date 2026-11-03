"""Search a universal static rival distribution for a fixed real policy cone.

All results remain numeric candidate certificates.  The cone describes every
type-weight vector satisfying the same fully expanded SPE policy comparisons.
"""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import bmat,coo_matrix,csr_matrix,block_diag,hstack,vstack
from cone_optimize import cone
from search_security import Search


def common_background(s,w):
    info,root,G,states=cone(s,w)
    B=s.security_coeff/s.scale
    types=len(w);rivals=len(B);nr=len(G)
    # For each query and each customer type, retain the coefficient identity.
    qcoeff=csr_matrix(np.vstack([B[:,a,:].T for a in range(s.k)]))
    multipliers=block_diag([csr_matrix(G.T/s.scale)]*s.k,format='csr')
    A=hstack([qcoeff,multipliers],format='csr')
    c=np.tile(s.coverage_coeff[root]/s.n,s.k)
    lp=linprog(np.zeros(A.shape[1]),A_ub=A,b_ub=c,
               A_eq=csr_matrix(np.r_[np.ones(rivals),np.zeros(nr*s.k)][None,:]),
               b_eq=[1],bounds=(0,None),method='highs')
    result=dict(status='UNCERTIFIED_NUMERIC_CANDIDATE' if lp.success else lp.message,
                n=s.n,k=s.k,root_counts=s.final[root],policy_subproblems=states,
                Gamma_rows=nr,initial=info)
    if lp.success:
        Q=lp.x[:rivals];lam=lp.x[rivals:].reshape((s.k,nr))
        result.update(Q=[dict(counts=s.cts[s.n-1][j],probability=float(q))
                         for j,q in enumerate(Q) if q>1e-10],
                      Gamma_multiplier_support=int(np.count_nonzero(lam>1e-9)),
                      min_residual=float(np.min(c-A@lp.x)),
                      multiplier_rows=[[(G[j].tolist(),float(v)) for j,v in enumerate(row) if v>1e-10]
                                       for row in lam])
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('seed',type=Path);ap.add_argument('--count',type=int,default=5)
    ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    seed=json.loads(a.seed.read_text());seeds=seed.get('bank',[seed.get('best',seed)])
    results=[]
    for j,x in enumerate(seeds[:a.count]):
        if not x:continue
        s=Search(x['n'],x['k']);r=common_background(s,np.array(x['weights'],dtype=np.int64));results.append(r)
        print(json.dumps({k:v for k,v in r.items() if k not in ('initial','multiplier_rows')}),flush=True)
        a.output.write_text(json.dumps(dict(status='EXPLORATORY',results=results),indent=2)+'\n')

if __name__=='__main__':main()
