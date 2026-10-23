"""Independent finite checks of the all-A policy and residual profit maximum.
No game model, discovery script or SPE solver is imported. All-n proof is separate.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import argparse


def vectors(s,k):
    if k==1:
        yield (s,)
    else:
        for z in range(s+1):
            for rest in vectors(s-z,k-1): yield (z,)+rest


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    runs=[]
    for n in range(2,9):
        nodes=comparisons=0
        for depth in range(n):
            for b in vectors(depth,n):
                obey=F(n,b[0]+n-depth)
                assert obey>=1
                for a in range(n):
                    deviation=obey if a==0 else F(1,b[a]+1)
                    assert obey>=deviation
                    comparisons+=1
                nodes+=1
        best=max(F(n*q[0],q[0]+1)+sum(k>0 for k in q[1:]) for q in vectors(n-1,n))
        hn=min(F(j)+F(n,j) for j in range(1,n+1))
        assert best==2*n-hn
        if n>=3: assert hn-1>2
        runs.append({'n':n,'count_decision_nodes':nodes,'comparisons_including_self':comparisons,
                     'Ftail':str(best),'h_n':str(hn),'local_loss':str(hn-1),
                     'u_current':1,'global_half_slack':1})
    result={'status':'PASS','scope':'finite exact regression; all-n proof in independent review','runs':runs}
    if args.output:
        with args.output.open('x') as f: json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result))

if __name__=='__main__': main()
