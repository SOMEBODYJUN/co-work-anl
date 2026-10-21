"""Floating discovery only: test a specific extra-mass background construction.

For p random root queries, take the expected full r-player terminal count as
the fractional competitor load. If its p-query payoff exceeds the root u,
this only refutes that construction, not freely optimized extra-mass safety.
"""
from extra_mass_probe import game_policy,OUT
import numpy as np
from scipy.optimize import linprog
import argparse,random,json,time

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=30);ap.add_argument('--topics',type=int,default=7);ap.add_argument('--remaining',type=int,default=5);ap.add_argument('--queries',type=int,default=30);ap.add_argument('--seed',type=int,default=71071);a=ap.parse_args()
    rng=random.Random(a.seed);nr=np.random.default_rng(a.seed);k=a.topics;r=a.remaining
    member=np.array([[(B>>i)&1 for B in range(1,1<<k)]for i in range(k)],dtype=float)
    best=-1e99;record=None;start=time.time();rows=[]
    for game in range(a.games):
        past=[0]*k
        for _ in range(rng.randrange(10)):past[rng.randrange(k)]+=1
        w=np.array([rng.randrange(1,8)if rng.random()<.35 else 0 for _ in range((1<<k)-1)],dtype=int)
        G,c,acts,target=game_policy(w,member,r,past,rng)
        def terminal(h):
            while len(h)<r:h=h+(acts[h],)
            return np.bincount(h,minlength=k)
        T=np.array([terminal((i,))for i in range(k)]);b=np.array(past)@member
        for query in range(a.queries):
            p=nr.dirichlet(np.ones(k)*nr.choice([.1,.3,1.,3.]))
            loads=p@T@member;obj=(p@member)/(1+b+loads)-c
            ans=linprog(-obj,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=c[None,:],b_eq=[1.],bounds=(0,None),method='highs')
            if not ans.success:print(json.dumps({'game':game,'query':query,'error':ans.message}),flush=True);continue
            gap=-ans.fun
            if gap>best+1e-9:
                best=gap;record={'status':'FLOATING ONLY','gap':best,'game':game,'query':query,'past':past,'root_query':p.tolist(),'weights':ans.x.tolist(),'remaining':r,'topics':k,'actions':[{'history':list(h),'action':aa}for h,aa in acts.items()]};print(json.dumps({key:record[key]for key in ['game','query','gap','past']}),flush=True)
            if gap>1e-7:
                (OUT/'full_terminal_push_candidate.json').write_text(json.dumps(record,indent=2)+'\n');return
        rows.append({'game':game,'best_gap_so_far':best})
    (OUT/f'full_terminal_push_scan_{k}_{r}_{a.seed}.json').write_text(json.dumps({'status':'finite floating discovery only','seed':a.seed,'best':best,'runs':rows,'elapsed':time.time()-start},indent=2)+'\n')
    print(json.dumps({'status':'finite floating discovery only','best':best,'elapsed':time.time()-start}),flush=True)

if __name__=='__main__':main()
