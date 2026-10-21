"""Finite fixed legal-background count-policy cones; numerical discovery only.

Alternates exact incidence LPs to attack B(u_first) <= W - gamma*u_first.
Count policies are a legal subclass and represent every ordered history, but
these trials are not exhaustive over strategies or price vertices.
"""
import argparse,itertools,json,random,runpy
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

D=runpy.run_path('research/workspaces/customer-attraction/R-c9208ba36bb54d1f9542d98da96fa009/early_opportunity/background_attack.py')
prep=D['prep']

def price(member,mass,v):
    k,n=member.shape
    ans=linprog(np.r_[np.full(k,v),-mass],A_ub=np.c_[-member.T,np.eye(n)],b_ub=np.zeros(n),bounds=[(0,1)]*k+[(0,1)]*n,method='highs')
    assert ans.success
    return ans.x[:k],-ans.fun

def main():
    ps=argparse.ArgumentParser();ps.add_argument('--topics',type=int,default=6);ps.add_argument('--old',type=int,default=2);ps.add_argument('--future',type=int,default=2);ps.add_argument('--trials',type=int,default=100);ps.add_argument('--gamma',type=float,default=1);ps.add_argument('--seed',type=int,default=2026102122);ps.add_argument('--output',required=True);args=ps.parse_args()
    k=args.topics;n=2**k-1;rng=random.Random(args.seed);records=[]
    seeds=[np.array(z,float) for z in itertools.product([0,1],repeat=k) if any(z)]
    seeds += [np.full(k,1/t) for t in range(2,k+1)]
    for tr in range(args.trials):
        mass=np.array([rng.choice([0,0,0,1,2,5,10,30]) for _ in range(n)],float)
        masks,member,rows,root,a,u,w,bg,actions=prep(k,args.old,args.future,mass,rng)
        best={'value':-1e99}
        for z0 in seeds:
            z=z0
            for it in range(5):
                target=np.minimum(1,z@member)-w-(sum(z)-args.gamma)*u
                ans=linprog(-target,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=np.ones((1,n)),b_eq=[1],bounds=(0,None),method='highs')
                if not ans.success:break
                value=-ans.fun
                if value>best['value']+1e-10:
                    best={'value':float(value),'trial':tr,'iteration':it,'queries':list(map(float,z)),'root':root,'target_action':a,'background':bg,'weights':{str(mask):float(v) for mask,v in zip(masks,ans.x) if v>1e-9},'actions':[{'counts':q,'action':a} for q,a in actions.items()]}
                newz,_=price(member,ans.x,u@ans.x)
                if np.linalg.norm(z-newz)<1e-8:break
                z=newz
        records.append(best)
        Path(args.output).write_text(json.dumps({'scope':__doc__,'parameters':vars(args),'records':records},indent=2)+'\n')
        if tr%10==0 or best['value']>1e-8: print(json.dumps({a:b for a,b in best.items() if a not in ['weights','actions']}),flush=True)
        if best['value']>1e-8:break
if __name__=='__main__':main()
