#!/usr/bin/env python3
"""Independent exhaustive optimization of suffix profit for the known n-family.
No SPE claims are inferred from this finite audit; complete SPE proof is canonical.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import argparse,json

def family(n):
    # A=0,B=1, ordinary/special leaves 2,...,n+1.
    x=n-2;types=[]
    for j in range(n):
        leaf=j+2
        types.extend([(frozenset([leaf]),x),(frozenset([1,leaf]),x)])
        types.append((frozenset([0,leaf]) if j<n-1 else frozenset([0,1,leaf]),1 if j<n-1 else n-1))
    return types

def profit(types,counts):
    return sum((F(w*sum(counts[t] for t in tags),int(0 in tags)+sum(counts[t] for t in tags)) for tags,w in types if sum(counts[t] for t in tags)),F())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--max-n',type=int,default=8);ap.add_argument('--output');args=ap.parse_args();rows=[]
    for n in range(4,args.max_n+1):
        types=family(n);k=n+2;best=None;witness=None;num=0
        for seq in combinations_with_replacement(range(k),n-1):
            counts=[0]*k
            for a in seq:counts[a]+=1
            p=profit(types,counts);num+=1
            if best is None or p>best:best=p;witness=counts
        expected=F(2*(n-1)*(n-2))+F(7*n-13,6);u=F(n)-F(1,n);opt=2*n*n-2*n-2
        assert best==expected
        q=[0]*k;q[1]=1;q[n+1]=1
        for a in range(2,n-1):q[a]=1
        assert sum(q)==n-1 and profit(types,q)==best
        rows.append({'n':n,'customers':sum(w for _,w in types),'candidate_profiles':num,'F_tail':str(best),'expected':str(expected),'argmax':witness,'specified_argmax':q,'root_utility':str(u),'OPT':opt,'bellman_slack':str(2*u+best-opt),'required_coefficient':str(F(opt-best,u))})
    out={'scope':'finite exhaustive exact suffix-profit optimization; not a general SPE proof','rows':rows}
    data=json.dumps(out,indent=2)
    if args.output:
        path=Path(args.output)
        if path.exists():raise FileExistsError(path)
        path.write_text(data+'\n')
    print(data)
if __name__=='__main__':main()
