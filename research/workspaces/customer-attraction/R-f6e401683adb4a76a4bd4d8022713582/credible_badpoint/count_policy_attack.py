"""Exploratory SPE-cone policy iteration; all count policies are full-history SPEs.

Floating LP only generates candidate weights. Exact certification is separate.
Unlike a relaxation, every optimized row is an actual node deviation under one
common count policy. This covers a subset of pure full-history strategies.
"""
from __future__ import annotations
import argparse, importlib.util, json, random, sys, time
from fractions import Fraction
from itertools import combinations
from math import lcm, gcd
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT))
SPEC=importlib.util.spec_from_file_location('intset', ROOT/'research/workspaces/customer-attraction/R-d28e1c3c70cf4adfbb52398ac7cf4c7b/experiments/cex_exact_sweep.py')
MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)

class PolicySearch(MOD.IntegerSetSolver):
    def __init__(self,p,m,maxfreq=0):
        super().__init__(p,m)
        if maxfreq:
            keep=[j for j,b in enumerate(self.types) if b.bit_count()<=maxfreq]
            self.types=tuple(self.types[j] for j in keep)
            self.rows=self.rows[:,:,keep]; self.coverage=self.coverage[:,keep]
        self.supports=list(combinations(range(p),min(p,m)))
        self.comparisons=np.array([[bool(b&sum(1<<a for a in J)) for b in self.types] for J in self.supports],dtype=float)
    def policy(self,w,rng,tie_mode='random'):
        util=self.rows@w; welfare=self.coverage@w
        terms=np.empty(len(self.states),dtype=np.int32); actions={}
        for q,j in self.tindex.items(): terms[self.sindex[q]]=j
        for d in range(self.m-1,-1,-1):
            for q in self.layers[d]:
                ix=self.sindex[q]; child=self.children[ix]
                vals=[util[terms[c],a] for a,c in enumerate(child)]
                high=max(vals); admissible=[a for a,v in enumerate(vals) if abs(v-high)<1e-7]
                if tie_mode=='welfare':
                    low=min(welfare[terms[child[a]]] for a in admissible)
                    admissible=[a for a in admissible if abs(welfare[terms[child[a]]]-low)<1e-7]
                a=rng.choice(admissible); actions[ix]=a; terms[ix]=terms[child[a]]
        return actions,terms
    def cone(self,actions,terms):
        rows=[]
        for ix,a in actions.items():
            actual=self.rows[terms[ix],a]
            for b,c in enumerate(self.children[ix]):
                if b!=a: rows.append(actual-self.rows[terms[c],b])
        mat=np.unique(np.array(rows),axis=0)
        mat=mat[np.any(mat,axis=1)]
        return mat
    def optimize(self,actions,terms,Jindex):
        mat=self.cone(actions,terms); w=self.coverage[terms[0]]
        res=linprog(-self.comparisons[Jindex],A_ub=-mat,b_ub=np.zeros(len(mat)),A_eq=[w],b_eq=[1],bounds=(0,None),method='highs')
        if not res.success: return None
        return res.x,-res.fun,mat
    def exact_verify(self,actions,terms,weights):
        ws=[Fraction(x) for x in weights]
        def utility(t,a): return sum(Fraction(int(x),self.scale)*w for x,w in zip(self.rows[t,a],ws))
        slacks=[]
        for ix,a in actions.items():
            actual=utility(terms[ix],a)
            for b,c in enumerate(self.children[ix]):
                slacks.append(actual-utility(terms[c],b))
        return min(slacks),sum(Fraction(int(c))*w for c,w in zip(self.coverage[terms[0]],ws))

    def credible_cone(self,weights,rng,mode='uniform'):
        """All-history random choices in the complete credible continuation menus."""
        vals=[Fraction(float(x)).limit_denominator(1000000) for x in weights]
        scale=lcm(*(x.denominator for x in vals)); nums=[int(x*scale) for x in vals]
        common=gcd(*nums); nums=[x//common for x in nums] if common else nums
        if sum(nums)*self.scale>=2**62: return None
        # Reuse exact integer all-outcome recursion, with our potentially restricted types.
        utility=self.rows@np.array(nums,dtype=np.int64)
        welfare=self.coverage@np.array(nums,dtype=np.int64)
        outcomes=[None]*len(self.states)
        for q,j in self.tindex.items(): outcomes[self.sindex[q]]=np.array([j],dtype=np.int32)
        thresholds={}
        for d in range(self.m-1,-1,-1):
            for q in self.layers[d]:
                ix=self.sindex[q]; child=[outcomes[c] for c in self.children[ix]]
                floor=max(int(np.min(utility[C,a])) for a,C in enumerate(child)); thresholds[ix]=floor
                outcomes[ix]=np.unique(np.concatenate([C[utility[C,a]>=floor] for a,C in enumerate(child)]))
        roots=outcomes[0]; low=min(welfare[t] for t in roots)
        root=int(rng.choice(roots[welfare[roots]==low])); rows=[]; choices=[]
        def expand(hist,ix,target):
            if len(hist)==self.m: return
            child=self.children[ix]
            admissible=[a for a,c in enumerate(child) if target in outcomes[c] and utility[target,a]>=thresholds[ix]]
            selected=rng.choice(admissible); destinations=[]
            for b,c in enumerate(child):
                if b==selected: dest=target
                else:
                    menu=outcomes[c][utility[outcomes[c],b]<=utility[target,selected]]
                    assert len(menu)
                    if mode=='min': menu=menu[utility[menu,b]==min(utility[menu,b])]
                    elif mode=='max': menu=menu[utility[menu,b]==max(utility[menu,b])]
                    elif mode=='lowW': menu=menu[welfare[menu]==min(welfare[menu])]
                    dest=int(rng.choice(menu))
                destinations.append(dest)
                expand(hist+(b,),c,dest)
            choices.append([list(hist),selected,target,destinations])
            actual=self.rows[target,selected]
            for b,dest in enumerate(destinations):
                if b!=selected: rows.append(actual-self.rows[dest,b])
        expand((),0,root)
        mat=np.unique(np.array(rows),axis=0); mat=mat[np.any(mat,axis=1)]
        return root,mat,choices

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--topics',type=int,default=7); ap.add_argument('--players',type=int,default=5); ap.add_argument('--iterations',type=int,default=100); ap.add_argument('--seed',type=int,default=63); ap.add_argument('--maxfreq',type=int,default=0); ap.add_argument('--credible',action='store_true'); ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args(); s=PolicySearch(args.topics,args.players,args.maxfreq); rng=random.Random(args.seed)
    champion=None; best=0; records=[]; started=time.monotonic(); seen=set()
    for it in range(args.iterations):
        if champion is None or it%12==0:
            weights=np.array([rng.randrange(1,30) if rng.random()<.13 else 0 for _ in s.types],dtype=float)
            if it==0: weights=np.array([args.players if b==1 else 1 if b.bit_count()==1 else 0 for b in s.types],dtype=float)
        else:
            weights=champion.copy()
            if it%3==0:
                weights+=np.array([rng.random()*.02 if rng.random()<.05 else 0 for _ in s.types])
        cur=int(np.argmax(s.comparisons@weights)); ji=cur if it%4 else rng.randrange(len(s.supports))
        if args.credible:
            result=s.credible_cone(weights,rng,['uniform','min','max','lowW'][it%4])
            if result is None: continue
            root,mat,choices=result
            res=linprog(-s.comparisons[ji],A_ub=-mat,b_ub=np.zeros(len(mat)),A_eq=[s.coverage[root]],b_eq=[1],bounds=(0,None),method='highs')
            result=(res.x,-res.fun,mat) if res.success else None
        else:
            actions,terms=s.policy(weights,rng,'welfare' if it%2 else 'random')
            signature=tuple(actions.values())
            if signature in seen:
                for _ in range(5): weights[rng.randrange(len(weights))]+=rng.random()*.005
                actions,terms=s.policy(weights,rng)
            seen.add(tuple(actions.values()))
            root=int(terms[0]); result=s.optimize(actions,terms,ji)
        if result is None: continue
        candidate,value,mat=result
        champion=candidate
        if value>best+1e-8:
            best=value
            rat=[Fraction(float(x)).limit_denominator(10000000) for x in candidate]
            if args.credible:
                slack=min(sum(Fraction(int(x),s.scale)*w for x,w in zip(row,rat)) for row in mat)
                W=sum(Fraction(int(x))*w for x,w in zip(s.coverage[root],rat))
                actiondata=choices
            else:
                slack,W=s.exact_verify(actions,terms,rat); actiondata=[[list(s.states[ix]),a] for ix,a in actions.items()]
            row=dict(iteration=it,ratio=value,root=s.terminals[root],support=s.supports[ji],weights=[str(x) for x in rat],exact_slack=str(slack),exact_W=str(W),rows=len(mat),actions=actiondata)
            records.append(row)
            print(json.dumps({k:v for k,v in row.items() if k not in ['actions','weights']}),flush=True)
        if it%5==0:
            args.output.write_text(json.dumps(dict(scope='finite count-policy SPE cones; floating candidates until exact_slack>=0 and exact_W=1',args=vars(args)|{'output':str(args.output)},records=records,elapsed=time.monotonic()-started),indent=2)+'\n')
    args.output.write_text(json.dumps(dict(scope='finite count-policy SPE cones; floating candidates until exact_slack>=0 and exact_W=1',args=vars(args)|{'output':str(args.output)},records=records,elapsed=time.monotonic()-started),indent=2)+'\n')
if __name__=='__main__': main()
