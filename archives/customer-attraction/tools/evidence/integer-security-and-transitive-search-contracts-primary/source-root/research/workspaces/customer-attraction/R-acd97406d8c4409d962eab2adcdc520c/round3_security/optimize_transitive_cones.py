"""Numerical separation in symmetry-restricted real SPE cones; exploratory."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from cone_optimize import cone
from search_security import Search

def main():
    ap=argparse.ArgumentParser();ap.add_argument('seed',type=Path);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();data=json.loads(a.seed.read_text());classes=[tuple(x) for x in data['classes']]
    seeds=data.get('bank',[data['best']]);results=[]
    for j,x in enumerate(seeds[:10]):
        s=Search(x['n'],x['k']);g=s.k//2;P=np.zeros((len(s.masks),len(classes)),dtype=np.int64)
        for i,mask in enumerate(s.masks):
            cl=tuple(sorted((int(mask[:g].sum()),int(mask[g:].sum()))))
            if cl in classes:P[i,classes.index(cl)]=1
        info,root,G,states=cone(s,np.array(x['weights'],dtype=np.int64))
        fixed=np.mean(s.security_coeff/s.scale,axis=1)@P
        GG=G@P;c=s.coverage_coeff[root]@P
        lp=linprog(np.r_[np.zeros(len(classes)),-1],
             A_ub=np.r_[np.c_[-GG,np.zeros(len(GG))],np.c_[-fixed,np.ones(len(fixed))]],
             b_ub=np.zeros(len(GG)+len(fixed)),A_eq=[np.r_[c,0]],b_eq=[1],
             bounds=[(0,None)]*len(classes)+[(None,None)],method='highs')
        r=dict(seed=j,n=s.n,k=s.k,status=lp.message,states=states,rows=len(G),root=s.final[root],initial=x)
        if lp.success:r.update(orbit_weights=lp.x[:-1].tolist(),value=float(lp.x[-1]),gap=float(1-s.n*lp.x[-1]),min_margin=float(np.min(GG@lp.x[:-1])))
        results.append(r);print(json.dumps({k:v for k,v in r.items() if k!='initial'}),flush=True)
        a.output.write_text(json.dumps(dict(status='UNCERTIFIED_LP_SEARCH',classes=classes,results=results),indent=2)+'\n')
        if lp.success and r['gap'] < -1e-7:break

if __name__=='__main__':main()
