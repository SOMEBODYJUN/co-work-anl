"""Exact unit-client-family and algebra boundary audit. Not an SPE certificate."""
from fractions import Fraction as F
from pathlib import Path
import json
import argparse


def audit(m):
    H=3*m*m-7*m+2
    X=4*(m-1)**3;Y=2*m*(m-1)*(m-3)
    Z=m*(m-3)*(m*m-3*m+4);eps=4*(m-3)
    # C=bit0,P=bit1,L=bit2,D=bit3.
    atoms=[(3,X),(12,X),(5,Y),(10,Y),(7,Z),(8,eps)]
    size=lambda a:sum(n for mask,n in atoms if mask>>a&1)
    K=size(0)
    assert all(size(a)<=K for a in range(4))
    def utility(a,counts):
        return sum((F(n,sum(counts[z] for z in range(4) if mask>>z&1))
                    for mask,n in atoms if n and mask>>a&1),F(0))
    counts=[m-2,1,1,0]
    v=utility(0,counts);p=utility(1,counts);t=utility(2,counts)
    E=m*v-K
    c=F((m-1)**2)-F(m*m*(m-3)**2,2*H)
    q=m*size(3)
    assert q-K==c*E
    floors=[];br=[]
    for a in range(4):
        fl=sum((F(n,(m-2)*(mask&1)+2) for mask,n in atoms if mask>>a&1),F(0))
        assert p>=fl
        floors.append(str(p-fl))
        dev=[m-2,1,0,0];dev[a]+=1
        gain=utility(a,dev)
        assert t>=gain
        br.append(str(t-gain))
    if m==4:
        afterD=[2,0,0,1]
        gains=[]
        for a in range(4):
            terminal=afterD.copy();terminal[a]+=1
            gains.append(utility(a,terminal))
        assert gains[2]>max(gains[:2]+gains[3:])
        terminal=afterD.copy();terminal[2]+=1
        deviator=utility(3,terminal)
        assert deviator==82>p==68
    return {'m':m,'coefficient':str(c),'E':str(E),'floor_slacks':floors,'terminal_BR_slacks':br}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output')
    args=parser.parse_args()
    rows=[audit(m) for m in range(3,101)]
    report={'scope':'Exact audit of six-group projection and formulas, NOT a full SPE certificate.',
            'checked_m':list(range(3,101)),'sample':rows[:8]}
    if args.output:
        with Path(args.output).open('x') as output:
            output.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
