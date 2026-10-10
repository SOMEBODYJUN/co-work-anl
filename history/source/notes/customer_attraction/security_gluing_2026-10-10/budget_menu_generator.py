"""Exact SPE-menu optimization of GB over every pure SPE of a fixed game,p.

The menu recursion keeps every attainable terminal count vector. Counts
compress only symmetric utility states; the reconstructed policy specifies
all ordered histories. Off-path continuations for different FIRST deviations
are independent, so on-path query budgets can be optimized branch by branch.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

BASE=Path('/workspace/scratch/4fa21fc3d3cc');OUT=BASE/'security_cone_attack';ROOT=BASE/'co-work-anl'

class Menu:
    def __init__(self,game,p):
        self.game=game;self.n=game['players'];self.m=len(game['topics']);self.p=list(map(F,p));assert sum(self.p)==1 and min(self.p)>=0
        self.types=[(frozenset(r['topics']),r['multiplicity']) for r in game['customers']]
        self.zero=(0,)*self.m
    @lru_cache(None)
    def utility(self,a,q):
        return sum((F(w,sum(q[b] for b in likes)) for likes,w in self.types if a in likes),F(0))
    def step(self,q,a):return q[:a]+(q[a]+1,)+q[a+1:]
    @lru_cache(None)
    def menus(self,c):
        if sum(c)==self.n:return (c,)
        branches=[self.menus(self.step(c,a)) for a in range(self.m)]
        floor=max(min(self.utility(a,q) for q in branches[a]) for a in range(self.m))
        return tuple(sorted({q for a,branch in enumerate(branches) for q in branch if self.utility(a,q)>=floor}))
    @lru_cache(None)
    def query_mean(self,own,q):
        B=q[:own]+(q[own]-1,)+q[own+1:];assert min(B)>=0
        return sum((self.p[a]*F(w,1+sum(B[b] for b in likes)) for a in range(self.m) for likes,w in self.types if a in likes),F(0))
    def coverage(self,q):return sum(w for likes,w in self.types if sum(q[a] for a in likes))
    def generic_policy(self,history,desired,policy):
        if len(history)==self.n:
            assert tuple(history.count(a) for a in range(self.m))==desired;return
        c=tuple(history.count(a) for a in range(self.m));assert desired in self.menus(c)
        minima=[min(self.menus(self.step(c,a)),key=lambda q:(self.utility(a,q),q)) for a in range(self.m)]
        floor=max(self.utility(a,q) for a,q in enumerate(minima))
        selected=next(a for a in range(self.m) if desired in self.menus(self.step(c,a)) and self.utility(a,desired)>=floor)
        policy[history]=selected
        for a in range(self.m):self.generic_policy(history+(a,),desired if a==selected else minima[a],policy)
    def optimize(self):
        rootmenus=self.menus(self.zero);best=None;possible=0
        for z in product(range(self.m),repeat=self.n):
            q=tuple(z.count(a) for a in range(self.m))
            if q not in rootmenus:continue
            prefix=self.zero;choices={};C=F(0);valid=True
            for i,own in enumerate(z):
                u=self.utility(own,q)
                for b in range(self.m):
                    branch=self.menus(self.step(prefix,b))
                    if b==own:
                        if q not in branch:valid=False;break
                        chosen=q
                    else:
                        eligible=[r for r in branch if self.utility(b,r)<=u]
                        if not eligible:valid=False;break
                        chosen=max(eligible,key=lambda r:(self.query_mean(b,r),r))
                    choices[(i,b)]=chosen;C+=self.p[b]*self.query_mean(b,chosen)
                if not valid:break
                prefix=self.step(prefix,own)
            if not valid:continue
            possible+=1;gb=C-self.coverage(q)
            if best is None or gb>best[0]:best=(gb,z,q,choices,C)
        assert best is not None
        gb,z,q,choices,C=best;policy={}
        for i,own in enumerate(z):
            h=z[:i];policy[h]=own
            for b in range(self.m):
                if b!=own:self.generic_policy(h+(b,),choices[(i,b)],policy)
        assert len(policy)==sum(self.m**i for i in range(self.n))
        result={'players':self.n,'topics':self.m,'root_SPE_count_menus':len(rootmenus),'possible_ordered_SPE_paths':possible,
                'GB_violation_sumC_minus_W':str(gb),'outcome':list(z),'W':self.coverage(q),'sum_C':str(C),
                'utilities':[str(self.utility(a,q)) for a in z],
                'strategy':{'actions':[{'history':list(h),'action':a} for h,a in sorted(policy.items(),key=lambda r:(len(r[0]),r[0]))]}}
        return result

def run():
    sources=[]
    original=json.load(open(ROOT/'evidence/certificates/customer_attraction/onpath_budget_failure.json'))
    sources.append(('original36',json.load(open(ROOT/'examples/customer_attraction/aggregate_theta_failure.json')),original['security']))
    c=json.load(open(OUT/'individual_security_failure_360.json'));sources.append(('individual360',c['game'],c['security']))
    for name in ['root_tax_failure','global_decorrelation_failure']:
        game=json.load(open(ROOT/'examples/customer_attraction'/f'{name}.json'));c=json.load(open(ROOT/'evidence/certificates/customer_attraction'/f'{name}.json'));sources.append((name,game,c['security']))
    for name,game,sec in sources:
        result=Menu(game,sec['primary']).optimize();print(name,{k:v for k,v in result.items() if k!='strategy'},flush=True)
        payload={'game':game,'security':sec,**result};(OUT/f'all_SPE_GB_{name}.json').write_text(json.dumps(payload,indent=2)+'\n')

if __name__=='__main__':run()
