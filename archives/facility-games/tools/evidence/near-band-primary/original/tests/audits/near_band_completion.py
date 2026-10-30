"""Independent fixed-heavy-support near-band audit; no global EPTAS verification.
Reproducible exact-support oracle; prototype select only, not production solver.
"""
from fractions import Fraction as F
from itertools import product
import random, json, argparse
from pathlib import Path

def near_exists(D, ws, k, H):
    for actions in product((0,1,2),repeat=len(ws)):
        mixed=actions.count(2)
        z=D+sum((w if a==1 else -w if a==0 else F(0) for w,a in zip(ws,actions)),F(0))
        lo,hi=-H,H
        for w,a in zip(ws,actions):
            if a!=1: lo=max(lo,-w)
            if a!=0: hi=min(hi,w)
        if lo>hi: continue
        factor=1-k-mixed
        if factor==0:
            if z==0: return True
        elif lo<=z/factor<=hi:
            return True
    return False

def select(D, ws, k, H):
    S=sum(ws,F(0))
    if D < -S:
        ans=select(-D,ws,k,H)
        return None if ans is None else (-ans[0], [1-p for p in ans[1]])
    if k==0 or abs(D)<=S:
        L,R=max(D,F(0)),max(-D,F(0))
        p=[F(0)]*len(ws)
        for i in sorted(range(len(ws)),key=lambda j:(-ws[j],j)):
            if L<=R: p[i]=F(1);L+=ws[i]
            else: R+=ws[i]
        r=L-R
        if k==0:
            return (r,p) if abs(r)<=H else None
        if r==0: return F(0),p
        high=F(1) if r>0 else F(0)
        candidates=[i for i in range(len(ws)) if p[i]==high]
        assert candidates
        j=min(candidates,key=lambda i:(ws[i],i))
        assert abs(r)<=ws[j]
        delta=(1 if r>0 else -1)*(ws[j]-abs(r))/k
        p[j]=(1+delta/ws[j])/2
        return delta,p
    # Now D>S>=(possibly 0).
    if k==1: return None
    moved=set()
    while True:
        t=(D-S+2*sum((ws[i] for i in moved),F(0)))/(k-1)
        if t>H: return None
        additions={i for i,w in enumerate(ws) if i not in moved and w<t}
        if not additions:
            return -t,[F(int(i in moved)) for i in range(len(ws))]
        moved |= additions

def check(D,ws,k,H,ans):
    delta,p=ans
    assert abs(delta)<=H
    # k genuinely mixed heavy clients of weight 2H; background encodes D.
    hw=2*H
    hp=(1+delta/hw)/2
    heavy=k*hw*(2*hp-1)
    assert delta==D+sum((w*(2*x-1) for w,x in zip(ws,p)),F(0))+heavy
    for w,x in zip(ws+[hw]*k,p+[hp]*k):
        assert 0<=x<=1
        diff=delta+w*(1-2*x)
        assert (x==0 and diff>=0) or (x==1 and diff<=0) or (0<x<1 and diff==0), (D,ws,k,H,ans,w,x,diff)

def main():
    rng=random.Random(20261009)
    cases=[]
    for k in range(5):
        for ws in ([],[F(1)],[F(1),F(1)], [F(1,2),F(1,4),F(1,8)]):
            S=sum(ws,F(0))
            for D in {F(0),S,-S,S+F(1,8),-S-F(1,8),S+F(k),-S-F(k)}:
                cases.append((D,ws,k,F(1)))
    for _ in range(1200):
        H=F(rng.randint(1,5),rng.randint(1,5))
        ws=[H*F(rng.randint(1,12),12) for _ in range(rng.randrange(7))]
        D=H*F(rng.randint(-120,120),12)
        cases.append((D,ws,rng.randrange(5),H))
    yes=0
    records=[]
    for case_id,(D,ws,k,H) in enumerate(cases):
        exists=near_exists(D,ws,k,H)
        ans=select(D,ws,k,H)
        assert exists==(ans is not None),(D,ws,k,H,exists,ans)
        if ans is not None: check(D,ws,k,H,ans);yes+=1
        records.append({'case_id':case_id,'D':str(D),'light_weights':list(map(str,ws)),
                        'heavy_mixer_count':k,'H':str(H),'near_feasible':exists,
                        'answer':None if ans is None else {'delta':str(ans[0]),'light_probabilities':list(map(str,ans[1]))}})
    result={'cases':len(cases),'near_feasible':yes,'seed':20261009,'status':'passed',
            'meaning':'finite exact attack only; not a theorem proof',
            'scope':'fixed heavy support central representative only, not full EPTAS or global approximation',
            'generator':'boundary cases plus 1200 random cases; H=U{1..5}/U{1..5}, light length=U{0..6}, light weights=H*U{1..12}/12, D=H*U{-120..120}/12, k=U{0..4}',
            'checks':['exact 3^light support closure enumeration band feasibility',
                      'direct rational conditional-cost NE inequalities including heavy mixers of weight 2H',
                      'exact total difference identity','exact probability domain'],
            'records':records}
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    if args.output:
        if args.output.exists():
            raise FileExistsError("frozen evidence must not be overwritten")
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({key:value for key,value in result.items() if key!='records'}))

if __name__=='__main__':main()
