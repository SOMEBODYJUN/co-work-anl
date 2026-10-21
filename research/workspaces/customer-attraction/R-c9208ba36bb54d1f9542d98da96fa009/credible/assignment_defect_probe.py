"""Finite exact-payoff attack on an unproved assignment-defect sufficient bridge.

Policies are count-dependent complete SPE (a subset, never a full-history reduction).
Every payoff and twice every defect is integral under lcm(1,...,m) scaling.
"""
import argparse,json,math,time
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import numpy as np
from scipy.optimize import linear_sum_assignment


def comps(n,p):
    if p==1:
        yield (n,);return
    for v in range(n+1):
        for t in comps(n-v,p-1):yield (v,)+t


def kernel(h,t,r,d):
    return (F(r-t,h+t+r) if r!=t else F(0))-F(d,h+t+1)


def run(p,m,n,trials,seed,output):
    rng=np.random.default_rng(seed)
    levels=[np.array(list(comps(z,p)),dtype=np.int16) for z in range(m+1)]
    indices=[{tuple(q):i for i,q in enumerate(level)} for level in levels]
    kids=[]
    for z in range(m):
        kk=[]
        for q in levels[z]:
            row=[]
            for a in range(p):
                qq=q.copy();qq[a]+=1;row.append(indices[z+1][tuple(qq)])
            kk.append(row)
        kids.append(np.array(kk))
    scale=math.lcm(*range(1,m+1))
    inv=np.array([0]+[scale//z for z in range(1,m+1)],dtype=np.int64)
    portfolios=list(combinations(range(p),m))
    best=F(-10**9);nocollision=0;start=time.time();bestdata=None
    for trial in range(trials):
        # Sparse catalogs make actual collision-free paths reasonably frequent.
        density=float(rng.choice([.08,.12,.16,.20]))
        member=(rng.random((n,p))<density).astype(np.int64)
        # Each topic nonempty; retain unit customers and a common finite catalog.
        for a in range(p):
            if not member[:,a].any():member[int(rng.integers(n)),a]=1
        loads=levels[m]@member.T
        pay=inv[loads]@member
        outcomes=[None]*(m+1);policies=[None]*m
        outcomes[m]=np.arange(len(levels[m]))
        for z in reversed(range(m)):
            cout=outcomes[z+1][kids[z]]
            vals=pay[cout,np.arange(p)[None,:]]
            # random deterministic ordering only selects among exact ties.
            order=rng.permutation(p)
            selected=order[np.argmax(vals[:,order],axis=1)]
            policies[z]=selected
            outcomes[z]=cout[np.arange(len(cout)),selected]
        actual=[];q=np.zeros(p,dtype=np.int16)
        for z in range(m):
            a=int(policies[z][indices[z][tuple(q)]])
            actual.append(a);q[a]+=1
        actual_load=member@q
        if actual_load.max()>1:continue
        nocollision+=1
        pval=[int(member[:,a].sum()) for a in actual[:-1]]
        L=int(member[:,actual[-1]].sum())
        coverages=np.array([np.any(member[:,ss],axis=1).sum() for ss in portfolios])
        optimum=int(coverages.max())
        optports=[portfolios[j] for j in np.flatnonzero(coverages==optimum)]
        defects={};intersections={}
        prefix=np.zeros(p,dtype=np.int16)
        for i in range(m-1):
            for T in range(p):
                qq=prefix.copy();qq[T]+=1
                for z in range(i+1,m):
                    R=int(policies[z][indices[z][tuple(qq)]])
                    qq[R]+=1
                hp=member@qq-member[:,T]-member[:,R]
                baseline=actual_load-member[:,actual[i]]-member[:,actual[-1]]
                delta=sum((kernel(int(hh),int(t),int(r),int(d))-kernel(int(pp),int(t),int(r),int(d)) for hh,pp,t,r,d in zip(hp,baseline,member[:,T],member[:,R],member[:,actual[-1]])),F(0))
                defects[i,T]=delta
                intersections[i,T]=int((member[:,T]*member[:,actual[i]]).sum())
            prefix[actual[i]]+=1
        # The strongest variant can choose the optimal portfolio as well as assignment.
        best_assignment=None
        for portfolio in optports:
            cost=[]
            for i in range(m-1):cost.append([defects[i,T]-F(intersections[i,T],2) for T in portfolio])
            cost.append([-F(int((member[:,T]*member[:,actual[-1]]).sum()),2) for T in portfolio])
            rr,cc=linear_sum_assignment(np.array(cost,dtype=float))
            value=sum((cost[i][j] for i,j in zip(rr,cc)),F(0))-F(L,2)
            if best_assignment is None or value<best_assignment[0]:
                best_assignment=(value,portfolio,list(map(int,cc)),cost)
        excess,portfolio,assignment,cost=best_assignment
        if excess>best:
            best=excess
            bestdata={'scope':'finite exact-payoff search; count-dependent complete SPE subset; not a general theorem','p':p,'m':m,'n':n,'trial':trial,'seed':seed,'actual':actual,'W':int(actual_load.sum()),'OPT':optimum,'portfolio':portfolio,'assignment':assignment,'excess':str(excess),'member':member.tolist(),'count_policy':[[q.tolist(),int(policies[z][j])] for z in range(m) for j,q in enumerate(levels[z])],'cost':[[str(x) for x in row] for row in cost]}
            Path(output).write_text(json.dumps(bestdata,indent=2)+'\n')
            print(json.dumps({'trial':trial,'nocollision':nocollision,'new_best_excess':str(best),'seconds':round(time.time()-start,2)}),flush=True)
        if excess>0:break
    summary={'trials_requested':trials,'trials_executed':trial+1,'actual_collision_free_cases':nocollision,'best_excess':str(best),'counterexample_found':best>0,'seconds':time.time()-start}
    Path(str(output)+'.summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=9);ap.add_argument('--players',type=int,default=5);ap.add_argument('--customers',type=int,default=30);ap.add_argument('--trials',type=int,default=1000);ap.add_argument('--seed',type=int,default=721028);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    run(a.topics,a.players,a.customers,a.trials,a.seed,a.output)
