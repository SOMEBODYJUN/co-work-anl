"""Formal integer-polynomial audit of the all-pair retained-tax obstruction.
No numerical interpolation and no SPE solver. z=m-3 is an indeterminate.
"""
from pathlib import Path
import argparse
import json


def add(*terms):
    out=[0]*max(map(len,terms))
    for term in terms:
        for k,v in enumerate(term):out[k]+=v
    while len(out)>1 and not out[-1]:out.pop()
    return out


def scale(a,n):return [n*x for x in a]
def sub(a,b):return add(a,scale(b,-1))
def mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    while len(out)>1 and not out[-1]:out.pop()
    return out


def audit():
    m=[3,1];r=[2,1];z=[0,1]
    X=scale(mul(mul(r,r),r),4)
    Y=scale(mul(mul(m,r),z),2)
    Z=mul(mul(m,z),add(mul(m,m),scale(m,-3),[4]))
    eps=scale(z,4)
    # Every expression is multiplied by positive D=2m(m-1).
    D=scale(mul(m,r),2)
    atoms=[(3,X),(12,X),(5,Y),(10,Y),(7,Z),(8,eps)]
    f=[]
    for a in range(4):
        f.append(add(*[mul(scale(m,2) if mask&1 else D,mass)
                       for mask,mass in atoms if mask>>a&1]))
    def g(a,b):
        return add(*[mul([2] if mask&1 else mul(m,r),mass)
                     for mask,mass in atoms if mask>>a&1 and mask>>b&1]) if any(mask>>a&1 and mask>>b&1 for mask,_ in atoms) else [0]
    p=add(mul(scale(m,2),X),mul(D,Y),mul(scale(r,2),Z))
    t=add(mul(D,X),mul(scale(m,2),Y),mul(scale(r,2),Z))
    budget=add(p,t,g(1,1))
    expected={
        (0,0):[320,904,984,522,136,14],
        (0,1):[320,808,808,402,100,10],
        (0,2):[64,264,344,202,56,6],
        (0,3):[64,168,204,124,36,4],
        (1,1):[320,808,772,360,84,8],
        (1,2):[64,168,168,82,20,2],
        (1,3):[64,168,168,82,20,2],
        (2,2):[64,168,168,82,20,2],
        (2,3):[64,72,28,4],
        (3,3):[64,120,74,20,2]}
    records=[]
    for (a,b),wanted in expected.items():
        got=add(budget,scale(f[a],-1),scale(f[b],-1),g(a,b))
        assert got==wanted,(a,b,got,wanted)
        assert got[0]>0 and all(x>=0 for x in got)
        records.append({'T':'CPLD'[a],'S':'CPLD'[b],'coefficients_ascending_in_m_minus_3':got})
    return {'scope':'Exact formal polynomial identities prove all retained two-remaining tax rows on the sharp six-group projection for every integer m>=3. Projection is NOT SPE.',
            'common_positive_multiplier':'2m(m-1)','checked_pair_rows':10,'rows':records}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
    report=audit()
    if args.output:
        with Path(args.output).open('x') as output:output.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
