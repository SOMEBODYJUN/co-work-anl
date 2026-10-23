"""Exact identities and bounded diagnostics for a variable-r background invariant.

No finite diagnostic establishes a general theorem. Uses the complete set-valued
BI recurrence, preserving arbitrary choices separately at ordered histories.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations_with_replacement, product
from random import Random
import argparse,json

class Game:
    def __init__(self,topics,types,r):
        self.topics,self.types,self.r=topics,tuple(types),r
    @lru_cache(None)
    def utility(self,q):
        u=[Q(0)]*self.topics
        for mask,n,b in self.types:
            d=b+sum(q[a] for a in range(self.topics) if mask>>a&1)
            if d:
                for a in range(self.topics):
                    if q[a] and mask>>a&1:u[a]+=Q(n,d)
        return tuple(u)
    def profit(self,q,add=None):
        ans=Q(0)
        for mask,n,b in self.types:
            e=sum(q[a] for a in range(self.topics) if mask>>a&1)
            p=b+(int(bool(mask>>add&1)) if add is not None else 0)
            if e:ans+=Q(n*e,p+e)
        return ans
    @lru_cache(None)
    def optimum(self,k,add=None):
        return max((self.profit(tuple(c.count(a) for a in range(self.topics)),add) for c in combinations_with_replacement(range(self.topics),k)),default=Q(0))
    def floor(self,k,add=None):
        if not k:return Q(0)
        return max(sum((Q(n,b+(int(bool(mask>>add&1)) if add is not None else 0)+k) for mask,n,b in self.types if mask>>a&1),Q(0)) for a in range(self.topics))
    @lru_cache(None)
    def outcomes(self,q):
        if sum(q)==self.r:return frozenset([q])
        children=[]
        for a in range(self.topics):
            z=list(q);z[a]+=1
            children.append(self.outcomes(tuple(z)))
        floor=max(min(self.utility(z)[a] for z in child) for a,child in enumerate(children))
        return frozenset(z for a,child in enumerate(children) for z in child if self.utility(z)[a]>=floor)
    def threshold(self,q):
        return max(min(self.utility(z)[a] for z in self.outcomes(tuple(q[j]+(j==a) for j in range(self.topics)))) for a in range(self.topics))
    def admissible_roots(self):
        q0=(0,)*self.topics;theta=self.threshold(q0)
        for a in range(self.topics):
            for q in self.outcomes(tuple(int(j==a) for j in range(self.topics))):
                if self.utility(q)[a]>=theta:yield a,q

def family(r):
    # Known lower-bound family; no novelty claim for the instance.
    F=Q(2*r-1)
    choices=[(Q(t)+Q(r,t+1),t) for t in range(r)]
    delta,t=min(choices)
    child=F-delta
    Eroot=Q(1);Echild=Q(2*(r-1))-child
    assert Eroot==Echild+2-delta
    return {'r':r,'minimizing_t':t,'F_parent':str(F),'F_child':str(child),'delta':str(delta),'u_first':'1','E_root':str(Eroot),'E_child':str(Echild),'child_floor_reserve':str(Q(2*(r-1))-child)}

def audit():
    rows=[]
    for r in range(2,41):
        row=family(r)
        if int(r**.5)**2==r:
            q=int(r**.5)
            assert row['delta']==str(Q(2*q-1))
            assert row['E_child']==str(Q(2*q-2))
        rows.append(row)
    # For small r independently enumerate every ordered history under all-A.
    checks=0
    for r in range(2,6):
        for depth in range(r):
            for h in product(range(r),repeat=depth):
                actual=Q(r,h.count(0)+r-depth)
                assert actual>=1
                for a in range(1,r):
                    assert Q(1,1+h.count(a))<=actual
                    checks+=1
    return {'family_rows':rows,'ordered_history_comparisons':checks,'status':'identities and known-family SPE audit passed'}

def diagnostic():
    rng=Random(90471);cases=0;transitions=0;hard=0
    # A single bounded attack on the stated reserve transition, no optimization.
    for topics,r,reps in [(5,3,80),(6,3,80),(5,4,60),(6,4,40)]:
        for it in range(reps):
            prefix=tuple(rng.randrange(topics) for _ in range(rng.randrange(3)))
            masks=list(range(1,1<<topics))
            rng.shuffle(masks)
            support=masks[:rng.randrange(topics,min(len(masks),3*topics)+1)]
            types=[(mask,rng.randrange(1,9),sum(mask>>a&1 for a in prefix)) for mask in support]
            game=Game(topics,types,r);F=game.optimum(r);root_floor=2*r*game.floor(r)
            cases+=1
            for a,q in game.admissible_roots():
                transitions+=1
                u=game.utility(q)[a]
                d=tuple(q[j]-(j==a) for j in range(topics))
                childF=game.optimum(r-1,a);childR=game.profit(d,a)
                assert game.profit(q)==u+childR
                E=2*game.profit(q)-F;Ec=2*childR-childF
                assert E==Ec+2*u-(F-childF)
                h=game.floor(r-1,a)
                assert childR>=(r-1)*h
                sufficient=max(root_floor,2*u+max(childF,2*(r-1)*h))
                if F>root_floor:hard+=1
                if F>sufficient:
                    return {'status':'reserve transition counterexample','topics':topics,'r':r,'prefix':prefix,'types':types,'F':str(F),'root_floor_2rh':str(root_floor),'first_action':a,'terminal':q,'u':str(u),'F_child':str(childF),'h_child':str(h),'R_child':str(childR),'slack':str(E),'slack_child':str(Ec),'transition_deficit':str(F-sufficient),'cases':cases,'transitions':transitions,'hard_transitions':hard,'seed':90471}
    return {'status':'no counterexample in bounded diagnostic; no theorem','cases':cases,'transitions':transitions,'hard_transitions':hard,'seed':90471}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--diagnostic',action='store_true');args=ap.parse_args()
    print(json.dumps(diagnostic() if args.diagnostic else audit(),indent=2))
