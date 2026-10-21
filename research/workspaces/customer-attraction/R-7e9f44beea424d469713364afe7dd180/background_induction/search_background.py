"""Exact bitset SPE outcome search with a fixed legal prefix.
Integer scaled utilities; all terminal outcome sets, no canonical tie restriction.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import lcm
import random,json,time
from pathlib import Path

ROOT=Path(__file__).parent

def compositions(n,q):
    if q==1:
        yield(n,);return
    for i in range(n+1):
        for tail in compositions(n-i,q-1): yield(i,)+tail

class BackgroundSolver:
    def __init__(self,q,r,prefix,weights):
        self.q,self.r,self.prefix,self.weights=q,r,tuple(prefix),dict(weights)
        self.scale=lcm(*range(1,sum(prefix)+r+1))
        self.terminals=list(compositions(r,q));self.tidx={x:i for i,x in enumerate(self.terminals)}
        self.pays=[];self.profits=[]
        for c in self.terminals:
            pay=[0]*q;profit=Fraction(0)
            for mask,w in weights.items():
                load=sum((prefix[a]+c[a]) for a in range(q) if mask>>a&1)
                rem=sum(c[a] for a in range(q) if mask>>a&1)
                if load:
                    share=w*(self.scale//load)
                    for a in range(q):
                        if mask>>a&1: pay[a]+=share
                    profit+=Fraction(w*rem,load)
            self.pays.append(pay);self.profits.append(profit)
        self.cut=[]
        for a in range(q):
            vals=sorted(set(p[a] for p in self.pays)); masks=[];running=0
            groups={v:0 for v in vals}
            for i,p in enumerate(self.pays): groups[p[a]]|=1<<i
            for v in vals:
                running|=groups[v];masks.append(running)
            self.cut.append((vals,masks))
        self.thresholds={}
        self.out=self.solve((0,)*q)
    @lru_cache(None)
    def solve(self,c):
        if sum(c)==self.r: return 1<<self.tidx[c]
        children=[];floor=0
        for a in range(self.q):
            d=list(c);d[a]+=1;child=self.solve(tuple(d));children.append(child)
            vals,masks=self.cut[a]
            lo,hi=0,len(vals)-1
            while lo<hi:
                mid=(lo+hi)//2
                if masks[mid]&child: hi=mid
                else:lo=mid+1
            floor=max(floor,vals[lo])
        self.thresholds[c]=floor
        out=0
        for a,child in enumerate(children):
            vals,masks=self.cut[a]
            import bisect
            i=bisect.bisect_left(vals,floor)
            out|=child if not i else child&~masks[i-1]
        return out
    def minimum(self):
        out=self.out;minimum=None;arg=None
        while out:
            bit=out&-out;i=bit.bit_length()-1;out-=bit
            if minimum is None or self.profits[i]<minimum:minimum,arg=self.profits[i],self.terminals[i]
        return minimum,arg
    def optimum(self):
        v=max(self.profits);return v,self.terminals[self.profits.index(v)]

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--trials',type=int,default=1000);parser.add_argument('--q',type=int,default=7);parser.add_argument('--r',type=int,default=5);parser.add_argument('--seed',type=int,default=193773)
    args=parser.parse_args();rng=random.Random(args.seed);best=Fraction(0);start=time.time()
    for trial in range(args.trials):
        q,r=args.q,args.r
        p=[0]*q
        for _ in range(rng.randrange(0,6)):p[rng.randrange(q)]+=1
        weights={mask:rng.randrange(1,31) for mask in rng.sample(range(1,1<<q),rng.randrange(q,min(3*q,1<<q)))}
        sol=BackgroundSolver(q,r,p,weights);v,actual=sol.minimum();o,opt=sol.optimum();ratio=o/v if v else Fraction(1)
        if ratio>best:
            best=ratio;obj={'trial':trial,'q':q,'r':r,'prefix':p,'weights':weights,'actual':actual,'opt':opt,'ratio':str(ratio),'minimum':str(v),'optimum':str(o),'seed':args.seed}
            (ROOT/'background_best.json').write_text(json.dumps(obj,indent=2))
            print(trial,float(ratio),ratio,'p',p,'t',round(time.time()-start,2),flush=True)
    print('done',args.trials,'best',str(best),'seconds',time.time()-start)
