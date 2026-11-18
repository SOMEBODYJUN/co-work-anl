from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from runpy import run_path
import sys

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

source = Path(__file__).with_name("probe_glued_branches.py")
namespace = run_path(str(source))
shares, rows, anchors = (namespace[k] for k in ('returns','rows','anchors'))
BRANCHES = ((0,6),(1,6),(2,6),(2,4),(3,5))


def solve(tau, joint):
    linked = tuple(BRANCHES[i] for i in joint)
    groups = ((linked,) + tuple((b,) for b in BRANCHES if b not in linked)) if linked else tuple((b,) for b in BRANCHES)
    objective, ai, aj, av, ei, ej, ev = ([] for _ in range(7))
    keys = {}
    eq_len = 1 + len(groups)*len(anchors)
    size = len(anchors)

    def eq(row, col, coeff):
        if coeff:
            ei.append(row); ej.append(col); ev.append(coeff)

    def inequalities(mapping, col, group):
        for name, value in mapping.items():
            if value:
                row = keys.setdefault((group,name),len(keys))
                ai.append(row); aj.append(col); av.append(-float(value))

    def table(shared, target, branch, tail):
        i,label = branch
        actual = shared[:6]
        leaf = actual[:i]+(shared[label],)+tail
        v = rows(tau, leaf, shared+tail, target, i+1)
        v['IC-own'] = shares(actual)[i]-shares(leaf)[i]
        for j,b in enumerate(tail):
            v[f'CAP{j}'] = shared[6]-b
        return leaf,v

    for idx,(shared,target) in enumerate(anchors):
        actual = shared[:6]
        r = rows(tau,actual,shared,target,0)
        r.update({f'CAP{j}':shared[6]-v for j,v in enumerate(shared)})
        for j,v in enumerate(shared):
            r[f'OPT{j}']=target*(1-v)-6*(1-target)*v
        r['W-opt']=target-int(any(actual))
        r['CAP-C']=tau*shared[6]-target
        col=len(objective); objective.append(int(any(actual)))
        inequalities(r,col,None); eq(0,col,target)
        for group_index in range(len(groups)):
            eq(1+group_index*size+idx,col,-1)
    for group_index,group in enumerate(groups):
        tails = [tuple(product((0,1),repeat=5-branch[0])) for branch in group]
        for idx,(shared,target) in enumerate(anchors):
            by_branch = [{t:table(shared,target,b,t) for t in ts} for b,ts in zip(group,tails)]
            for suffixes in product(*tails):
                col=len(objective); objective.append(0)
                for k,(branch,tail) in enumerate(zip(group,suffixes)):
                    leaf,r=by_branch[k][tail]
                    if len(group)==2:
                        alternative=suffixes[1-k]
                        r=r.copy()
                        pay=shares(leaf)
                        for i in range(branch[0]+1,6):
                            den=sum(leaf[:i])+6-i
                            for j,b in enumerate(alternative):
                                r[f'cross-{i}-{j}']=pay[i]-Q(b,den)
                        # Two true final positions also compare this other leaf's legal actions.
                        p=sum(leaf[:4]);a=leaf[4];D=(p+1)*(p+2)
                        for j,b in enumerate(alternative):
                            r[f'pair-cross-{j}']=(pay[4]+pay[5]+Q(a,D)-Q(b,p+1)
                                                   -Q(target)/tau*(Q(1,p+1)-Q(b,D)))
                    inequalities(r,col,branch)
                eq(1+group_index*size+idx,col,1)
    shape=(len(keys),len(objective))
    print('assembled',tau, joint,shape,len(av),flush=True)
    matrix=coo_matrix((av,(ai,aj)),shape=shape).tocsc()
    eq_matrix=coo_matrix((ev,(ei,ej)),shape=(eq_len,len(objective))).tocsc()
    res=linprog(objective,A_ub=matrix,b_ub=np.zeros(len(keys)),A_eq=eq_matrix,
                b_eq=np.r_[1,np.zeros(eq_len-1)],bounds=(0,None),method='highs')
    print('joint',tau,joint,res.status,res.fun,flush=True)
    if res.success:
        print('active-cross',[(key,-res.ineqlin.marginals[k]) for key,k in keys.items() if key[1].startswith(('cross','pair-cross')) and -res.ineqlin.marginals[k]>1e-8],flush=True)

if __name__ == '__main__':
    solve(Q(sys.argv[1]),tuple(map(int,sys.argv[2:])))
