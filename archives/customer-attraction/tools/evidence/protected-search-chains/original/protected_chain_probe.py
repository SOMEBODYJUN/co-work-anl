"""Partial reply chains for the protected two-comparator budget.

LP relaxations of genuine tail SPE. Strict separation is not a counterexample.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def scan(depth=1, bmax=4):
    p = 2 + 2*(depth+1)
    atoms = [(mask, b) for mask in range(1, 1<<p) for b in range(bmax+1)]
    masks=np.array([mask for mask,b in atoms],dtype=np.int64)
    bs=np.array([b for mask,b in atoms],dtype=np.int64)
    bit=[((masks>>a)&1).astype(float) for a in range(p)]
    def row(a, q):
        den=bs+sum(bit[j] for j in q)
        return np.divide(bit[a],den,out=np.zeros(len(atoms)),where=den>0)
    W=row(0,(0,1))+row(1,(0,1))
    D=((bs==0)&((masks&3)==0)&((masks&12)!=0)).astype(float)
    replies={0:1}
    for level in range(depth):
        for chain in range(2):
            a=2+2*level+chain; replies[a]=a+2
    constraints=[]; ids=[]
    for a,r in replies.items():
        for t in range(p):
            if t!=r:
                constraints.append(row(r,(a,r))-row(t,(a,t)))
                ids.append(['tail',a,r,t])
        if a:
            constraints.append(row(0,(0,1))-row(a,(a,r)))
            ids.append(['root',a,r])
    mat=np.array(constraints)
    result=linprog(-D,A_ub=-mat,b_ub=np.zeros(len(mat)),A_eq=[W],b_eq=[1],bounds=(0,None),method='highs')
    output={'depth':depth,'p':p,'bmax':bmax,'atoms':len(atoms),'rows':len(mat),'success':result.success}
    if result.success:
        output.update(value=-result.fun, support=[{'mask':mask,'b':b,'mass':str(F(float(w)).limit_denominator(10**7))}
            for (mask,b),w in zip(atoms,result.x) if w>1e-8], dual=[{'row':i,'multiplier':str(F(float(-w)).limit_denominator(10**7))}
            for i,w in zip(ids,result.ineqlin.marginals) if abs(w)>1e-8])
    return output


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--depth',type=int,default=1)
    ap.add_argument('--bmax',type=int,default=4);ap.add_argument('--output')
    args=ap.parse_args();result=scan(args.depth,args.bmax)
    blob=json.dumps(result,indent=2)
    if args.output:Path(args.output).write_text(blob+'\n')
    print(blob)
