"""Structured full-history policy cones, compressed by group symmetry.

Two groups of n topics each; second player chooses the group opposite player 1,
and every later player chooses a fresh topic in player 2's group.  Rows include
all repeated-history partitions, not only the distinct histories.  Floating LP
is only a discovery tool. Variables are total normalized orbit populations.
"""
import argparse, json, math, time
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


@lru_cache(None)
def partitions(s, cap=None):
    if s == 0: return ((),)
    if cap is None: cap = s
    return tuple((a,) + p for a in range(min(cap,s),0,-1)
                 for p in partitions(s-a,a))


@lru_cache(None)
def selection_loads(q, count):
    """Number of subsets of exactly count labels with a given load."""
    dp = {(0,0):1}
    for c in q:
        nd = defaultdict(int)
        for (k,v),r in dp.items():
            nd[k,v] += r
            if k < count: nd[k+1,v+c] += r
        dp = nd
    return tuple((v,r) for (k,v),r in dp.items() if k == count)


class Cone:
    def __init__(self,n,group_topics=None):
        self.n=n
        self.k=group_topics or n
        self.types=tuple((a,b) for a in range(self.k+1) for b in range(a,self.k+1) if a+b)

    @lru_cache(None)
    def raw_pay(self,x,y,g,c,a,b):
        q=[list(x)+[0]*(self.k-len(x)),list(y)+[0]*(self.k-len(y))]
        counts=[a,b]
        if counts[g] == 0: return F(0)
        q[g].remove(c)
        counts[g] -= 1
        ds=[selection_loads(tuple(q[j]),counts[j]) for j in range(2)]
        value=sum((F(r*s,c+h+k) for h,r in ds[0] for k,s in ds[1]),F(0))
        return value / (math.comb(self.k,a)*math.comb(self.k,b))

    @lru_cache(None)
    def pay(self,x,y,g,c):
        return tuple((self.raw_pay(x,y,g,c,a,b)+self.raw_pay(x,y,g,c,b,a))/2
                     for a,b in self.types)

    @lru_cache(None)
    def coverage(self,x,y):
        def raw(a,b):
            empty=F(math.comb(self.k-len(x),a) if a<=self.k-len(x) else 0,
                    math.comb(self.k,a))
            empty*=F(math.comb(self.k-len(y),b) if b<=self.k-len(y) else 0,
                     math.comb(self.k,b))
            return 1-empty
        return tuple((raw(a,b)+raw(b,a))/2 for a,b in self.types)

    def terminal(self,x,y,g,current_group,current_count,r):
        """Current choice followed by r fresh choices in designated group g."""
        q=[list(x),list(y)]
        if current_count:
            q[current_group].remove(current_count)
            q[current_group].append(current_count+1)
        else: q[current_group].append(1)
        q[g].extend([1]*r)
        return tuple(sorted(q[0],reverse=True)),tuple(sorted(q[1],reverse=True))

    def rows(self):
        rows=[];meta=[]
        # All depths >=2. By exchange of groups we can designate group X.
        for d in range(2,self.n):
            r=self.n-d-1
            for sx in range(1,d+1):
                for x in partitions(sx):
                    for y in partitions(d-sx):
                        tx,ty=self.terminal(x,y,0,0,0,r)
                        actual=self.pay(tx,ty,0,1)
                        for h,q in enumerate((x,y)):
                            for c in (0,)+tuple(set(q)):
                                if h==0 and c==0: continue
                                ax,ay=self.terminal(x,y,0,h,c,r)
                                alternative=self.pay(ax,ay,h,c+1)
                                rows.append(tuple(a-b for a,b in zip(alternative,actual)))
                                meta.append((d,x,y,h,c))
        # Second player: fresh opposite versus fresh same or repeating first.
        actual=self.pay((1,),(1,)*(self.n-1),1,1)
        for repeat in (False,True):
            q=(2,)+(1,)*(self.n-2) if repeat else (1,)*self.n
            alternative=self.pay(q,(),0,2 if repeat else 1)
            rows.append(tuple(a-b for a,b in zip(alternative,actual)))
            meta.append(('second',repeat))
        return rows,meta

    def run(self):
        rows,meta=self.rows()
        A=np.array(rows,dtype=float)
        rootx=(1,);rooty=(1,)*(self.n-1)
        u=self.pay(rootx,rooty,0,1);w=self.coverage(rootx,rooty)
        tests=[]
        for x in range(self.n+1):
            cmp=self.coverage((1,)*x,(1,)*(self.n-x))
            tests.append(('weak',x,tuple(o-v-self.n*t for o,v,t in zip(cmp,w,u))))
        for k in range(1,2*self.k+1):
            tau=F(2*self.k,k)
            cover=tuple(min(F(1),F(a+b,k)) for a,b in self.types)
            tests.append(('uniform_price',k,tuple(o-v-tau*t for o,v,t in zip(cover,w,u))))
        records=[]
        for name,param,target in tests:
            result=linprog(-np.array(target,dtype=float),A_ub=A,b_ub=np.zeros(len(A)),
                           A_eq=np.ones((1,len(self.types))),b_eq=[1],bounds=(0,None),method='highs')
            if result.success:
                rec={'test':name,'parameter':param,'value':float(-result.fun),
                     'support':{str(ab):float(v) for ab,v in zip(self.types,result.x) if v>1e-8}}
                records.append(rec)
        return {'players':self.n,'group_topics':self.k,'variables':len(self.types),'rows':len(rows),
                'best':max(records,key=lambda z:z['value']),'records':records}


def main():
    p=argparse.ArgumentParser();p.add_argument('--players',type=int,nargs='+',required=True)
    p.add_argument('--group-multiplier',type=int,default=1)
    p.add_argument('--output',required=True);args=p.parse_args();out=[]
    for n in args.players:
        start=time.time();rec=Cone(n,n*args.group_multiplier).run();rec['seconds']=time.time()-start;out.append(rec)
        print(json.dumps({k:v for k,v in rec.items() if k!='records'}),flush=True)
        Path(args.output).write_text(json.dumps({'scope':'Floating structured complete-policy cones; not a general theorem',
                                               'results':out},indent=2)+'\n')

if __name__=='__main__': main()
