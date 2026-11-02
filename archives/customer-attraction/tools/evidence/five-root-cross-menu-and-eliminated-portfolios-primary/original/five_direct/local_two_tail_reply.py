"""Local necessary-condition discovery, never a full SPE claim.

One genuine maximum-theme root branch C,A,B,D,E and the genuine last
response R after its penultimate player forces a comparison topic T.
All 127 nonzero client memberships are retained. Output is floating only.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json
import numpy as np
from scipy.optimize import linprog


def main():
    # C,T,A,B,D,E,R
    types=list(product((0,1),repeat=7))[1:]
    ar=np.array(types,dtype=float)
    act=[0,2,3,4,5]
    csize=ar[:,0]
    k=ar[:,act].sum(axis=1)
    root=np.divide(ar[:,0],k,out=np.zeros(len(types)),where=k>0)
    target=ar[:,1]*(1-.8*ar[:,0])
    rows=[];names=[]
    def row(name, vals):
        names.append(name);rows.append(np.array(vals,dtype=float))
    def shr(num,den):
        return np.divide(num,den,out=np.zeros(len(types)),where=den>0)
    for t in range(1,7):row(f'size{t}',ar[:,t]-csize)
    last=shr(ar[:,5],k)
    for t in range(7):row(f'last_{t}',shr(ar[:,t],ar[:,[0,2,3,4]].sum(axis=1)+1)-last)
    for j in range(1,4):
        prefix=ar[:,act[:j]].sum(axis=1)
        cur=act[j];r=5-j
        payoff=shr(ar[:,cur],k)
        for t in range(7):row(f'node{j}_{t}',shr(ar[:,t],prefix+r)-payoff)
    for rem,beta in ((3,F(5,3)),(4,F(1499,750))):
        prefix=ar[:,act[:5-rem]].sum(axis=1)
        actual=shr(ar[:,act[5-rem:]].sum(axis=1),k)
        for qs in combinations_with_replacement(range(7),rem):
            h=ar[:,qs].sum(axis=1)
            row(f'tail{rem}_{qs}',shr(h,prefix+h)-float(beta)*actual)
    base_count=ar[:,[0,2,3]].sum(axis=1)
    devk=base_count+ar[:,1]+ar[:,6]
    dp=shr(ar[:,4],k)
    row('penult_T_true_R',shr(ar[:,1],devk)-dp)
    rp=shr(ar[:,6],devk)
    for t in range(7):
        row(f'reply_R_BR{t}',shr(ar[:,t],base_count+ar[:,1]+1)-rp)
    out={'scope':'floating necessary local branch inequalities; not SPE or a welfare theorem','types':len(types),'rows':len(rows),'points':[]}
    for ratio in (F(1,5),F(21,100),F(11,50),F(6,25),F(1,4),F(3,10),F(1,3)):
        z=linprog(-target,A_ub=np.array(rows+[root]),b_ub=[0.]*len(rows)+[float(ratio)],A_eq=[csize],b_eq=[1.],bounds=(0,None),method='highs')
        q={'root_cap':str(ratio),'success':bool(z.success)}
        if z.success:
            q.update(F=float(-z.fun),slope=float(-z.ineqlin.marginals[-1]),intercept=float(-z.eqlin.marginals[0]),active={n:float(-v) for n,v in zip(names,z.ineqlin.marginals[:-1]) if abs(v)>1e-8},support=[{'bits':''.join(map(str,types[i])),'mass':float(v)} for i,v in enumerate(z.x) if v>1e-8])
        out['points'].append(q)
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
