"""Discovery only: fixed complete count-policy cone versus last-seat availability.

All ordered histories are represented by their count state for this *chosen*
policy. This searches a subset of strategies, never asserts general compression.
The output is a cone point, not an exact certificate until audited separately.
"""
import argparse, itertools, json, math, random, time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for j in range(n + 1):
            for t in compositions(n-j, k-1):
                yield (j,) + t


class Cone:
    def __init__(self, k, n=5):
        self.k, self.n = k, n
        self.masks = np.arange(1, 1 << k)
        self.inc = ((self.masks[:, None] >> np.arange(k)) & 1).astype(float)
        self.states = [list(compositions(s, k)) for s in range(n+1)]
        self.utility = {}
        self.welfare = {}
        for q in self.states[n]:
            loads = self.inc @ q
            self.utility[q] = self.inc.T / np.maximum(loads, 1)
            self.welfare[q] = (loads > 0).astype(float)
        self.zero = (0,)*k

    def successor(self, q, a):
        r=list(q);r[a]+=1;return tuple(r)

    def policy(self, w, rng):
        ends = {q:q for q in self.states[self.n]}
        actions = {}
        for depth in range(self.n-1, -1, -1):
            for q in self.states[depth]:
                es=[ends[self.successor(q,a)] for a in range(self.k)]
                val=np.array([self.utility[e][a] @ w for a,e in enumerate(es)])
                best=np.flatnonzero(val >= val.max()-1e-9)
                # Either random tied continuation, or worst welfare among ties.
                if rng.random()<.7:
                    a=min(best, key=lambda a: self.welfare[es[a]] @ w)
                else:
                    a=rng.choice(best)
                actions[q]=int(a);ends[q]=es[a]
        return actions,ends

    def optimize(self, policy):
        actions,ends=policy
        rows=[];rhs=[]
        for depth in range(self.n):
            for q in self.states[depth]:
                a=actions[q];base=self.utility[ends[q]][a]
                for b in range(self.k):
                    other=self.utility[ends[self.successor(q,b)]][b]
                    rows.append(other-base);rhs.append(0)
        for q in self.states[self.n-1]:
            rows.append(-self.utility[ends[q]][actions[q]]);rhs.append(-1)
        return linprog(self.welfare[ends[self.zero]], A_ub=np.array(rows), b_ub=np.array(rhs), bounds=(0,None), method='highs')


def main():
    p=argparse.ArgumentParser();p.add_argument('--topics',type=int,default=6);p.add_argument('--iterations',type=int,default=100);p.add_argument('--seed',type=int,default=176);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    rng=random.Random(args.seed);np_rng=np.random.default_rng(args.seed);c=Cone(args.topics)
    best=math.inf;best_data=None;start=time.time()
    for i in range(args.iterations):
        if i and i%4 and best_data:
            w=np.array(best_data['weights']) + np_rng.exponential(.03, len(c.masks))
        else:
            w=np_rng.exponential(1,len(c.masks))*(np_rng.random(len(c.masks)) < rng.uniform(.1,.8))
        pol=c.policy(w,rng);r=c.optimize(pol)
        if r.success and r.fun < best-1e-9:
            best=r.fun
            best_data={'ratio':best,'weights':r.x.tolist(),'topics':args.topics,'providers':5,'policy':{','.join(map(str,q)):a for q,a in pol[0].items()},'iteration':i,'seed':args.seed,'note':'floating discovery; all count-state IC and final availability constraints'}
            args.out.write_text(json.dumps(best_data,indent=2))
            print(json.dumps({'iteration':i,'best':best,'support':int(sum(r.x>1e-7)),'elapsed':round(time.time()-start,2)}),flush=True)
    print(json.dumps({'iterations':args.iterations,'best':best,'seconds':time.time()-start}),flush=True)


if __name__=='__main__':main()
