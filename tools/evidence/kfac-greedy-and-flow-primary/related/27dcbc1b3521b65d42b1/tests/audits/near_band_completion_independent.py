"""Independent exact preliminary audit; not a production EPTAS or its universal proof.
Original algebraic core preserved; command-line output replaces temporary paths.
"""
from fractions import Fraction as F
from itertools import product
from random import Random
import json
from pathlib import Path
import argparse
C={'instances':0,'full_support_cells':0,'heavy_patterns':0,'near_cells':0,'selector_outputs':0,'comparisons':0,'monotone_light_moves':0}

def exact_cells(a,b,ww,H):
    heavy=[i for i,w in enumerate(ww) if w>H]
    possible=set()
    for st in product((-1,0,1),repeat=len(ww)):
        C['full_support_cells']+=1
        m=st.count(0); B=a-b+sum(w*x for w,x in zip(ww,st))
        lo=-H;hi=H
        for w,x in zip(ww,st):
            if x!=1:lo=max(lo,-w)
            if x!=-1:hi=min(hi,w)
        if m==1:
            if B:continue
        else:
            d=B/(1-m);lo=max(lo,d);hi=min(hi,d)
        if lo<=hi:
            C['near_cells']+=1
            possible.add(tuple(st[i] for i in heavy))
    return heavy,possible

def check_ne(a,b,ww,pp,H):
    X=a+sum(w*p for w,p in zip(ww,pp));Y=b+sum(w*(1-p) for w,p in zip(ww,pp))
    assert abs(X-Y)<=H
    for i,(w,p) in enumerate(zip(ww,pp)):
        assert 0<=p<=1
        c1=a+w+sum(v*pp[j] for j,v in enumerate(ww) if j!=i)
        c2=b+w+sum(v*(1-pp[j]) for j,v in enumerate(ww) if j!=i)
        assert (p==0 or c1<=c2) and (p==1 or c2<=c1), (a,b,ww,pp,i,c1,c2)
        C['comparisons']+=2
    return X-Y

def near_select(a,b,ww,H,heavy,st):
    pp=[None]*len(ww);kh=0;D=a-b
    for i,x in zip(heavy,st):
        if x:pp[i]=F(1 if x==1 else 0);D+=x*ww[i]
        else:kh+=1
    light=[i for i in range(len(ww)) if i not in heavy]
    S=sum(ww[i] for i in light)
    if kh==0 or abs(D)<=S:
        r=D
        for i in sorted(light,key=lambda i:(-ww[i],i)):
            p=F(0 if r>0 else 1)
            pp[i]=p;r+=(2*p-1)*ww[i]
        if kh==0:
            if abs(r)>H:return None
            delta=r
        elif r==0:delta=F(0)
        else:
            sig=1 if r>0 else -1
            j=min((i for i in light if (pp[i]==1)==(sig==1)),key=lambda i:(ww[i],i))
            assert ww[j]>=abs(r)
            delta=sig*(ww[j]-abs(r))/kh
            pp[j]=(1+delta/ww[j])/2
    else:
        if kh<2:return None
        sig=1 if D>0 else -1
        t=(abs(D)-S)/(kh-1)
        moved=set()
        for i in light:pp[i]=F(0 if sig>0 else 1)
        while True:
            eligible=[i for i in light if i not in moved and ww[i]<t]
            if not eligible:break
            i=min(eligible);moved.add(i);pp[i]=F(1 if sig>0 else 0)
            C['monotone_light_moves']+=1
            t=(abs(D)-S+2*sum(ww[j] for j in moved))/(kh-1)
        if t>H:return None
        delta=-sig*t
    for i,x in zip(heavy,st):
        if x==0:pp[i]=(1+delta/ww[i])/2
    assert check_ne(a,b,ww,pp,H)==delta
    return pp

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    cases=[]
    vals=[F(0),F(1,10),F(1,2),F(1),F(2),F(7)]
    weights=[F(1,10),F(1,2),F(1),F(3)]
    for a,b in product(vals[:5],repeat=2):
        for ww in product(weights,repeat=2):
            for eta in (F(1,8),F(1,4),F(1,2)):
                cases.append((a,b,list(ww),eta))
    rng=Random(670982)
    for _ in range(800):
        k=rng.randrange(0,7)
        ww=[F(rng.randrange(1,41),rng.choice([1,2,5,10,100,2**30])) for _ in range(k)]
        a=F(rng.randrange(0,41),rng.choice([1,2,10,100]));b=F(rng.randrange(0,41),rng.choice([1,2,10,100]))
        eta=rng.choice([F(1,10),F(1,6),F(1,4),F(1,2)])
        cases.append((a,b,ww,eta))
    # Explicit S=0, D=0, boundary w=H, k_h=1, and near-existence-but-pure-completion-fails.
    cases += [(F(0),F(0),[],F(1,4)),(F(0),F(0),[F(10),F(1),F(1)],F(1,8)),(F(3),F(0),[F(10),F(10),F(1),F(1,10)],F(1,4)),(F(7),F(0),[F(10),F(10)],F(1,4))]
    for a,b,ww,eta in cases:
        W=a+b+sum(ww);H=eta*W
        heavy,possible=exact_cells(a,b,ww,H)
        for st in product((-1,0,1),repeat=len(heavy)):
            C['heavy_patterns']+=1
            out=near_select(a,b,ww,H,heavy,st)
            assert (out is not None)==(st in possible),(a,b,ww,eta,H,heavy,st,possible,out)
            if out is not None:
                C['selector_outputs']+=1
                assert all((x==0 and 0<out[i]<1) or (x==1 and out[i]==1) or (x==-1 and out[i]==0) for i,x in zip(heavy,st))
        C['instances']+=1
    report={'counts':C,'seed':670982,'status':'all assertions passed; finite audit only','parameters':'400 background/2-weight instances x 3 eta plus 800 random <=6-common and explicit boundaries'}
    if args.output:
        if args.output.exists():
            raise FileExistsError("frozen evidence must not be overwritten")
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    main()
