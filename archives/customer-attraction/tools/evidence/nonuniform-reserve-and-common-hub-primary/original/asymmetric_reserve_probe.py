"""Exact finite attack of a stated all-k,t independent-reserve candidate.

The candidate says a>x/2 cannot admit C_1,...,C_k,D_1,...,D_t even
when independent reserves have arbitrary sizes. A rejected last-C subgame
cannot be repaired by earlier strategy choices. This probe does not prove
the candidate from finitely many failures.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement
from math import lcm
from pathlib import Path
import argparse,json,random


def build(k,t):
    names=[f'C{i}' for i in range(k)]+[f'A{i}' for i in range(k)]
    names += [f'B{i}_{r}' for i in range(k) for r in range(t)] +[f'D{r}' for r in range(t)]
    p=len(names); idx={a:i for i,a in enumerate(names)}
    typ=[]
    for i in range(k):
        typ.append(tuple([idx[f'C{i}'],idx[f'A{i}']]+[idx[f'B{i}_{r}'] for r in range(t)]))
        typ.append((idx[f'A{i}'],))
    for r in range(t):
        typ.append(tuple([idx[f'D{r}']]+[idx[f'B{i}_{r}'] for i in range(k)]))
        typ.append((idx[f'D{r}'],))
    return names,typ

class LastCGeometry:
    def __init__(self,k,t):
        self.k,self.t=k,t; self.m=k+t; self.names,self.typ=build(k,t); self.p=len(self.names)
        self.scale=lcm(*range(1,self.m+1))
        self.prefix=tuple(int(i<k-1) for i in range(self.p))
        self.target=tuple(int(i<k or i>=self.p-t) for i in range(self.p))
        self.states=[]; self.children={}; self.coeff={}
        def visit(q):
            if q in self.children or q in self.coeff:return
            if sum(q)==self.m:
                mat=[[0]*len(self.typ) for _ in range(self.p)]
                for z,signature in enumerate(self.typ):
                    d=sum(q[a] for a in signature)
                    if d:
                        for a in signature:
                            if q[a]:mat[a][z]=self.scale//d
                self.coeff[q]=mat
            else:
                cs=[]
                for a in range(self.p):
                    child=q[:a]+(q[a]+1,)+q[a+1:];cs.append(child);visit(child)
                self.children[q]=cs
            self.states.append(q)
        visit(self.prefix)
    def solve(self,x,a,reserves,details=False):
        weights=[v for _ in range(self.k) for v in (x,a)]+[v for bd in reserves for v in bd]
        pay={q:tuple(sum(c*w for c,w in zip(row,weights)) for row in mat) for q,mat in self.coeff.items()}
        R={}; floor={}; mini={}
        for q in self.states:
            if q in self.coeff:R[q]={q};continue
            cs=self.children[q]
            lows=[min(pay[z][aa] for z in R[c]) for aa,c in enumerate(cs)]
            F=max(lows);floor[q]=F;mini[q]=lows
            R[q]={z for aa,c in enumerate(cs) for z in R[c] if pay[z][aa]>=F}
        actual_ok=self.target in R[self.prefix]
        target_u=x*self.scale
        if not details:return actual_ok
        ia=self.k+(self.k-1)
        child=self.children[self.prefix][ia]
        minA=min(pay[z][ia] for z in R[child])
        witness=min((z for z in R[child] if pay[z][ia]==minA))
        return {'x':x,'a':a,'reserves':reserves,'last_C_actual_target_achievable':actual_ok,'last_C_threshold':str(Fraction(floor[self.prefix],self.scale)),'deviate_own_A_min':str(Fraction(minA,self.scale)),'own_A_min_terminal':witness,'names':self.names,'R_size':len(R[self.prefix]),'states':len(self.states)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--t',type=int,default=2);ap.add_argument('--k',type=int,default=3);ap.add_argument('--trials',type=int,default=1000);ap.add_argument('--seed',type=int,default=751103);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    geom=LastCGeometry(args.k,args.t);rng=random.Random(args.seed);tested=0;admissible=0;best=None;found=[]
    for _ in range(args.trials):
        x=rng.randint(2,12);a=rng.randint(x//2+1,x+2)
        reserves=[(rng.randint(1,3*x),rng.randint(0,2*x)) for r in range(args.t)]
        # The prescribed actual last D must beat every terminal legal alternative.
        H=reserves[-1][0]+reserves[-1][1]
        if reserves[-1][1]*2<x or H*2<x+2*a:continue
        if any(2*H<sum(bd) for bd in reserves[:-1]):continue
        if any(2*H<x+b for b,d in reserves[:-1]):continue
        admissible+=1
        r=geom.solve(x,a,reserves,True);tested+=1
        deficit=Fraction(r['deviate_own_A_min'])-x
        if best is None or deficit<Fraction(best['own_A_gap']):
            best=r|{'own_A_gap':str(deficit)}
        if r['last_C_actual_target_achievable']:
            found.append(r);break
    report={'scope':'finite exact counterexample search for arbitrary-reserve proposed theorem; not an all-parameter proof','seed':args.seed,'k':args.k,'t':args.t,'trials':args.trials,'tested':tested,'admissible':admissible,'scale':geom.scale,'best':best,'found':found}
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
