"""Constructive anchor/gap attacks, exact integer all-SPE recursion and cone LP.

LCM-scaled payoffs are exact integers. Floating LP only proposes new games;
the resulting rational vector is checked against every complete-tree row.
This is finite falsification, not a universal theorem.
"""
from __future__ import annotations
import argparse, json, math, random, sys, time
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver, verify_certificate

def compositions(n,p):
    if p==1:
        yield (n,); return
    for a in range(n+1):
        for tail in compositions(n-a,p-1): yield (a,)+tail

class Engine:
    def __init__(self,p=7,m=5):
        self.p,self.m=p,m
        self.L=math.lcm(*range(1,m+1))
        self.masks=np.arange(1,1<<p,dtype=np.int64)
        self.inc=((self.masks[:,None]>>np.arange(p))&1).astype(np.int64)
        self.states=[list(compositions(d,p)) for d in range(m+1)]
        self.term=self.states[m]
        self.tid={q:i for i,q in enumerate(self.term)}
        self.coeff=[]
        for q in self.term:
            den=self.inc@np.array(q)
            self.coeff.append(np.array([[self.L//int(den[i]) if self.inc[i,a] and q[a] else 0 for i in range(len(den))] for a in range(p)],dtype=np.int16))
        self.coeff=np.array(self.coeff)
        self.cover=np.array([(self.inc@np.array(q)>0) for q in self.term],dtype=np.int64)
        self.portfolios=list(combinations(range(p),min(p,m)))
        self.ocover=np.array([np.any(self.inc[:,J],axis=1) for J in self.portfolios],dtype=np.int64)
        self.children={q:tuple(q[:a]+(q[a]+1,)+q[a+1:] for a in range(p)) for d in range(m) for q in self.states[d]}

    def solve(self,r):
        # LP vertices may have huge common denominators. Python integer
        # arithmetic is the exact fallback, never an overflowing int64 cast.
        self.r=np.array(r,dtype=np.int64 if sum(r)*self.L<=2**61 else object)
        self.pay=self.coeff@self.r
        self.welf=self.cover@self.r
        self.opts=self.ocover@self.r
        self.R={q:np.array([i],dtype=np.int32) for i,q in enumerate(self.term)}
        self.floor={}
        for d in range(self.m-1,-1,-1):
            for q in self.states[d]:
                children=self.children[q]
                floor=max(np.min(self.pay[self.R[c],a]) for a,c in enumerate(children))
                self.floor[q]=floor
                kept=[self.R[c][self.pay[self.R[c],a]>=floor] for a,c in enumerate(children)]
                self.R[q]=np.unique(np.concatenate(kept))
        outcomes=self.R[(0,)*self.p]
        mn=min(self.welf[outcomes])
        self.worst=outcomes[self.welf[outcomes]==mn]
        return Fraction(int(max(self.opts)),int(mn)) if mn else Fraction(1)

    def eligible_path(self,target,last_count_max):
        """One genuine realizable order with the desired final multiplicity."""
        def descend(h,q):
            if len(h)==self.m:
                return h if self.term[target][h[-1]]<=last_count_max else None
            for a,c in enumerate(self.children[q]):
                if target in self.R[c] and self.pay[target,a]>=self.floor[q]:
                    result=descend(h+(a,),c)
                    if result is not None:return result
            return None
        return descend((),(0,)*self.p)

    def cone(self,target,rng,variant=0,on_path=None):
        actions={}; terminals={}; rows=[]
        def expand(h,q,t):
            terminals[h]=t
            if len(h)==self.m:return
            children=self.children[q]
            candidates=[a for a,c in enumerate(children) if t in self.R[c] and self.pay[t,a]>=self.floor[q]]
            chosen=(on_path[len(h)] if on_path is not None and h==on_path[:len(h)] else rng.choice(candidates) if variant else candidates[0])
            if chosen not in candidates:raise AssertionError('ineligible forced path')
            actions[h]=chosen
            ts=[]
            for a,c in enumerate(children):
                if a==chosen:tt=t
                else:
                    v=self.pay[self.R[c],a]; candidates=self.R[c][v==min(v)]
                    tt=int(rng.choice(candidates)) if variant else int(candidates[0])
                ts.append(tt)
                expand(h+(a,),c,tt)
            rows.extend(self.coeff[t,chosen]-self.coeff[tt,a] for a,tt in enumerate(ts) if a!=chosen)
        expand((),(0,)*self.p,int(target))
        G=np.unique(np.array(rows),axis=0)
        G=G[np.any(G,axis=1)]
        return G,self.cover[target],actions

    def recover(self,G,w,x):
        r=[Fraction(float(t)).limit_denominator(10000000) for t in x]
        def valid(r):
            return sum(a*b for a,b in zip(w,r))==1 and min(r)>=0 and all(sum(int(a)*b for a,b in zip(row,r))>=0 for row in G)
        if valid(r):return r
        S=np.flatnonzero(x>1e-8)
        active=G[np.abs(G@x)<1e-7]
        basis={}
        for index,row in enumerate([w,*active]):
            v=[Fraction(int(row[j])) for j in S]+[Fraction(index==0)]
            for pivot in sorted(basis):
                c=v[pivot]
                if c:v=[a-c*b for a,b in zip(v,basis[pivot])]
            pivot=next((j for j,t in enumerate(v[:-1]) if t),None)
            if pivot is not None:
                c=v[pivot];basis[pivot]=[a/c for a in v]
            elif v[-1]:continue
            if len(basis)==len(S):break
        if len(basis)<len(S):return None
        y=[Fraction(0)]*len(S)
        for pivot in sorted(basis,reverse=True):y[pivot]=basis[pivot][-1]-sum(basis[pivot][j]*y[j] for j in range(pivot+1,len(S)))
        r=[Fraction(0)]*len(x)
        for j,v in zip(S,y):r[j]=v
        return r if valid(r) else None

    def optimize(self,G,w,portfolio):
        v=self.ocover[portfolio]
        res=linprog(-v.astype(float),A_ub=-G.astype(float),b_ub=np.zeros(len(G)),A_eq=w[None,:].astype(float),b_eq=[1.],bounds=(0,None),method='highs')
        if not res.success:return None
        r=self.recover(G,w,res.x)
        if r is None:return None
        L=math.lcm(*(t.denominator for t in r))
        ints=[int(t*L) for t in r]
        gcd=math.gcd(*ints);ints=tuple(t//gcd for t in ints)
        return ints,Fraction(sum(int(a)*b for a,b in zip(v,r)))

    def instance(self,r):
        return Instance(tuple(f'T{a}' for a in range(self.p)),tuple(CustomerType(frozenset(a for a in range(self.p) if mask&(1<<a)),int(n)) for mask,n in enumerate(r,1) if n),self.m)

def seeds(p,m,anchors=2):
    """Two anchors, gap options: cyclic affinity, disjoint private gaps.

    Mask customers belonging to an anchor and a contiguous cyclic set of gap
    themes make a deviation attract future anchor occupants nonuniformly.
    """
    k=p-anchors
    for width in (1,2,3):
        for anchor_ratio in ((1,1),(2,3),(1,3)):
            for ext in (1,2,3):
                r=[0]*((1<<p)-1)
                for i in range(k):
                    gaps=sum(1<<(anchors+(i+j)%k) for j in range(min(width,k)))
                    r[(1<<(i%anchors)|gaps)-1]+=m*anchor_ratio[i%2]
                    r[(1<<(anchors+i))-1]+=ext
                yield tuple(r)
    # Cycle customer blocks with one anchor and two crossing gap options.
    for jump in (1,2):
        r=[0]*((1<<p)-1)
        for i in range(k):
            r[((1<<(i%anchors))|(1<<(anchors+i))|(1<<(anchors+(i+jump)%k)))-1]+=m
            r[(1<<(anchors+i))-1]+=1
        yield tuple(r)

def distinct_maxima(r,p):
    S=[frozenset(mask for mask,n in enumerate(r,1) if n and mask&(1<<a)) for a in range(p)]
    return len({s for s in S if not any(s<t for t in S)})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rounds',type=int,default=40);ap.add_argument('--topics',type=int,default=7);ap.add_argument('--players',type=int,default=5);ap.add_argument('--anchors',type=int,default=2);ap.add_argument('--private-floor',type=int,default=0,help='if K>0, require each private type >=W/K to retain all distinct maximal themes');ap.add_argument('--last-count-max',type=int,default=0);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    eng=Engine(args.topics,args.players);rng=random.Random(64201);queue=list(seeds(args.topics,args.players,args.anchors));seen=set();history=[];best=Fraction(0);started=time.time()
    for iteration in range(args.rounds):
        while queue and queue[0] in seen:queue.pop(0)
        if not queue:break
        r=queue.pop(0);seen.add(r);ratio=eng.solve(r)
        target=int(rng.choice(eng.worst));path=None
        if args.last_count_max:
            candidates=[(int(t),eng.eligible_path(int(t),args.last_count_max)) for t in eng.worst]
            candidates=[pair for pair in candidates if pair[1] is not None]
            if not candidates:continue
            target,path=rng.choice(candidates)
        G,w,actions=eng.cone(target,rng,variant=iteration%2,on_path=path)
        if args.private_floor:
            private=np.array([-w.copy() for a in range(args.topics)])
            for a in range(args.topics):private[a,(1<<a)-1]+=args.private_floor
            G=np.concatenate((G,private))
        # Explicit all-history witness is checked independently at every best.
        row={'iteration':iteration,'source_ratio':str(ratio),'root':eng.term[target],'on_path':path,'rows':len(G),'seed_support':sum(n>0 for n in r),'source_maxima':distinct_maxima(r,args.topics)}
        endpoints=[]
        portfolios=[eng.portfolios.index(tuple(range(args.anchors,args.topics)))]+list(np.argsort(eng.opts)[-3:]) if args.topics-args.anchors==args.players else list(np.argsort(eng.opts)[-4:])
        for j in dict.fromkeys(portfolios):
            result=eng.optimize(G,w,j)
            if result:
                endpoint,value=result
                if args.private_floor and distinct_maxima(endpoint,args.topics)!=args.topics:raise AssertionError('private-floor maximality failure')
                if iteration%3==0:queue.insert(0,endpoint)
                else:queue.append(endpoint)
                endpoints.append((value,endpoint,j))
                if value>best:
                    best=value
                    inst=eng.instance(endpoint)
                    # Preserve the specified complete strategy, not just a count policy.
                    from customer_attraction import StrategyCertificate
                    cert=StrategyCertificate(actions,eng.term[target]);verify_certificate(inst,cert).assert_valid()
                    row['new_best']=str(best)
                    record={'best_ratio_lower_bound':str(best),'distinct_maximal_themes':distinct_maxima(endpoint,args.topics),'target':eng.term[target],'portfolio':eng.portfolios[j],'instance':inst.to_dict(),'certificate':cert.to_dict(),'row_scope':'all ordered histories','note':'not a universal bound'}
                    args.output.with_name(args.output.stem+'_best.json').write_text(json.dumps(record,indent=2)+'\n')
        if endpoints:
            # Deliberately cross facets of strong cones via small private and
            # cyclic overlap additions, then rebuild a genuine SPE next round.
            val,endpoint,j=max(endpoints)
            for _ in range(2):
                mut=[10*x for x in endpoint]
                mask=rng.choice([1<<a for a in range(args.topics)]+[rng.randrange(1,1<<args.topics)])
                mut[mask-1]+=1
                queue.append(tuple(mut))
        row['best']=str(best);row['elapsed']=round(time.time()-started,3);history.append(row);print(json.dumps(row),flush=True)
        args.output.write_text(json.dumps({'parameters':vars(args)|{'output':str(args.output)},'scope':'targeted anchor-gap cascade family with exact complete-tree cone checks','universal_bound_proved':False,'history':history},indent=2)+'\n')

if __name__=='__main__':main()
