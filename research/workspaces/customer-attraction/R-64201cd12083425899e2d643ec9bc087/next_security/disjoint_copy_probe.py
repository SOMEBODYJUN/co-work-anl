"""Try delaying security compensation across independent 36-customer gadgets.

Exact integer backward induction for a deterministic count-dependent SPE;
floating LP is used only for intermediate static-security values.
"""
from pathlib import Path
import argparse,json,sys,time
sys.dont_write_bytecode=True
from functools import lru_cache
from itertools import combinations,combinations_with_replacement
from fractions import Fraction as F
from math import lcm
import numpy as np
from scipy.optimize import linprog

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--copies',type=int,default=2);ap.add_argument('--scale2',type=int,default=1);ap.add_argument('--mode',default='open');ap.add_argument('--oldpreferred',action='store_true');ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    k=6*a.copies;n=3*a.copies;types=[];w=[]
    for j in range(a.copies):
        X=list(range(6*j,6*j+3));Y=list(range(6*j+3,6*j+6));scale=a.scale2 if j==1 else 1
        for x in X:
            for y in Y:types.append((1<<x)|(1<<y));w.append(scale)
        for xx in combinations(X,2):
            for yy in combinations(Y,2):types.append(sum(1<<x for x in xx+yy));w.append(3*scale)
    inc=np.array([[(mask>>x)&1 for x in range(k)] for mask in types],dtype=np.int64);w=np.array(w,np.int64);L=lcm(*range(1,n+1));nodes=0;start=time.time()
    @lru_cache(None)
    def pay(q):
        d=inc@np.array(q);inv=np.array([L//int(x) if x else 0 for x in d]);return tuple((w*inv)@inc)
    @lru_cache(None)
    def flag_next(q,flags,x):
        g=x//6;count=sum(q[6*g:6*g+6]);ff=list(flags)
        ff[g]=(x%6)//3 if count<2 else 0
        return tuple(ff)
    def oldpriority(q,flags,x):
        g=x//6;local=q[6*g:6*g+6];d=sum(local)
        if not d:preferred=6*g
        elif d==1:preferred=6*g+3*(1-flags[g])
        elif d==2:
            G=range(6*g+3*flags[g],6*g+3*flags[g]+3);preferred=min(G,key=lambda z:(q[z],z))
        else:preferred=min(range(6*g,6*g+6),key=lambda z:(q[z],z))
        return x!=preferred
    @lru_cache(None)
    def solve(q,flags):
        nonlocal nodes;nodes+=1
        if sum(q)==n:return q
        options=[];floor=-1
        for x in range(k):
            child=q[:x]+(q[x]+1,)+q[x+1:];term=solve(child,flag_next(q,flags,x));value=pay(term)[x]
            if value>floor:floor=value;options=[(x,term)]
            elif value==floor:options.append((x,term))
        pref=lambda x:oldpriority(q,flags,x) if a.oldpreferred else q[x]
        if a.mode=='open':key=lambda z:(sum(q[6*(z[0]//6):6*(z[0]//6)+6]),pref(z[0]),z[0])
        elif a.mode=='finish':key=lambda z:(-sum(q[6*(z[0]//6):6*(z[0]//6)+6]),pref(z[0]),z[0])
        elif a.mode=='repeat':key=lambda z:(-q[z[0]],z[0])
        else:key=lambda z:(z[0],)
        x,term=min(options,key=key);policy[q,flags]=x;return term
    policy={};root=(0,)*k;flags=(0,)*a.copies;term=solve(root,flags);q=root;path=[]
    while sum(q)<n:
        x=policy[q,flags];path.append(x);flags=flag_next(q,flags,x);q=q[:x]+(q[x]+1,)+q[x+1:]
    ups=[F(pay(term)[x],L) for x in path];sec=[];exact_root=None
    for j in range(n):
        bg=inc@np.bincount(path[:j],minlength=k);r=n-j;B=list(combinations_with_replacement(range(k),r-1));M=np.array([(w/(1+bg+inc[:,b].sum(axis=1)))@inc for b in B])
        z=linprog(np.r_[np.zeros(k),-1.],A_ub=np.c_[-M,np.ones(len(M))],b_ub=np.zeros(len(M)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs');assert z.success;sec.append(z.x[-1])
        if j==0 and a.scale2==1:
            exact_root=min(sum(F(int(w[t])*sum(inc[t]),k*(1+int(sum(inc[t,x] for x in b)))) for t in range(len(w))) for b in B)
            assert abs(float(exact_root)-sec[-1])<1e-7
    pairs=[float(ups[j]+ups[j+1])+(n-j-2)*sec[j+2]-(n-j)*sec[j] for j in range(n-2)]
    ans=dict(status='exact deterministic SPE construction; intermediate security numerical',copies=a.copies,scale2=a.scale2,mode=a.mode,oldpreferred=a.oldpreferred,states=nodes,seconds=time.time()-start,path=path,payoffs=list(map(str,ups)),W=str(sum(ups)),security=sec,root_security_exact=str(exact_root) if exact_root is not None else None,pair_budgets=pairs)
    a.output.write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps(ans),flush=True)

if __name__=='__main__':main()
