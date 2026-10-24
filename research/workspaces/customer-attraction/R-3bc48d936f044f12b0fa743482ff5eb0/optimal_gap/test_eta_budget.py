"""Attack one exact all-input candidate: retain full xi but omit eta in global gap budget.
Finite output never establishes the candidate or Q-CAG-HALF.
"""
import argparse, itertools, json, math, random
from functools import lru_cache
from fractions import Fraction
from pathlib import Path

def evaluate(m,p,weights,rng):
    L=math.lcm(*range(1,m+1))
    masks=[j for j,w in enumerate(weights) if w]
    sets=[sum(1<<j for j in masks if j>>a&1) for a in range(p)]
    def size(U):return sum(weights[j] for j in masks if U>>j&1)
    @lru_cache(None)
    def welfare(c):return size(union(c))
    def union(c):
        U=0
        for a,k in enumerate(c):
            if k: U|=sets[a]
        return U
    @lru_cache(None)
    def utility(a,c):
        return sum(weights[j]*(L//sum(c[b] for b in range(p) if j>>b&1)) for j in masks if j>>a&1)
    policy={}
    @lru_cache(None)
    def solve(c):
        if sum(c)==m:return c
        children=[]
        for a in range(p):
            cc=list(c);cc[a]+=1
            z=solve(tuple(cc));children.append((utility(a,z),rng.random(),a,z))
        _,_,a,z=max(children); policy[c]=a
        return z
    @lru_cache(None)
    def F(k,P):
        if k==0:return size(P)
        return max(F(k-1,P|A) for A in sets)
    c=(0,)*p; terminal=solve(c); W=welfare(terminal); O=F(m,0)
    rows=[]; eta_sum=Fraction(0)
    for i in range(m):
        r=m-i; P=union(c); S=sets[policy[c]]
        choices=[]
        G=F(r,P)
        for a,A in enumerate(sets):
            if F(r-1,P|A)!=G:continue
            cc=list(c);cc[a]+=1
            z=solve(tuple(cc));tail=tuple(z[j]-c[j]-int(j==a) for j in range(p));Y=union(tail)
            M=size(A&~(P|S)); t=size(A&~(P|S|Y));d=Fraction(utility(a,z),L)
            eta=r*d-M-(r-1)*t
            assert eta>=0
            choices.append((eta/Fraction(r),a,eta))
        v,a,eta=min(choices); eta_sum+=v
        rows.append({'r':r,'chosen':policy[c],'min_eta_over_r':str(v),'menu_argmin':a})
        cc=list(c);cc[policy[c]]+=1;c=tuple(cc)
    excess=eta_sum-(2*W-O)
    return excess,{'players':m,'topics':p,'weights':weights,'W':W,'OPT':O,'eta_sum':str(eta_sum),'excess':str(excess),'rows':rows,'policy':[{'counts':list(k),'action':a} for k,a in sorted(policy.items(),key=lambda z:(sum(z[0]),z[0]))]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--trials',type=int,default=1000);ap.add_argument('--seed',type=int,default=723);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    rng=random.Random(args.seed);best=None
    for trial in range(args.trials):
        m=rng.choice([2,3,4,5]);p=rng.choice([3,4,5,6]);weights=[0]*(1<<p)
        for j in range(1,1<<p):
            if rng.random()<.35:weights[j]=rng.randint(1,30)
        excess,record=evaluate(m,p,weights,rng)
        if best is None or excess>Fraction(best['excess']):
            best=record;best['trial']=trial
        if excess>0:
            args.output.write_text(json.dumps({'candidate':'sum_i min_menu eta_i/r_i <= 2W-OPT','seed':args.seed,'counterexample':record},indent=2));print('COUNTEREXAMPLE',trial,m,p,W if False else record['excess']);return
    args.output.write_text(json.dumps({'candidate':'sum_i min_menu eta_i/r_i <= 2W-OPT','status':'finite tests only','seed':args.seed,'trials':args.trials,'best':best},indent=2));print('NO_COUNTEREXAMPLE',args.trials,'max_excess',best['excess'])
if __name__=='__main__':main()
