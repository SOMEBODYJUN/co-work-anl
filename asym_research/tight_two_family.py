#!/usr/bin/env python3
"""Generate the exact six-vertex heterogeneous 2-lower-bound family."""
import argparse,json
from fractions import Fraction as Q
from bounded_overlap import solve,serial


def instance(M):
    if M <= 4:
        raise ValueError('M must be an integer greater than 4')
    return {'weights':[M,1,M+8,M+2,10,6],
            'locations':[[0,1,2],[0,1,3,4],[0,2,3,5],[1,2,3],[1,4],[2,5]],
            'U1':[0,1],'U2':[2,3]}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--M',type=int,default=1000)
    parser.add_argument('--output')
    args=parser.parse_args()
    ins=instance(args.M)
    ans=solve(ins)
    expected=Q(2*args.M+10,args.M+14)
    assert ans['alpha']==expected and ans['kappa']==2
    text=json.dumps(ins,ensure_ascii=False,indent=2)
    if args.output:
        with open(args.output,'w') as f:f.write(text+'\n')
        print(json.dumps({'output':args.output,'exact_optimal_factor':str(expected),'decimal':float(expected)}))
    else:
        print(text)
