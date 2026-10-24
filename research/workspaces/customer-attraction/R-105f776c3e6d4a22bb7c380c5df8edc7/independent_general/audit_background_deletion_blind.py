"""Definition-level independent audit of the background deletion regret bound.
No repository solver, previous proof, or harmonic-menu source is imported.
"""
from fractions import Fraction as F
from pathlib import Path
import json,random

def payoff(interests,background,leaf,topic):
    return sum((F(1,background[x]+sum(a in interests[x] for a in leaf))
                for x in range(len(interests)) if topic in interests[x]),F())

def audit(interests,b,d,n,k,rng,forced_root=None):
    original=[x+y for x,y in zip(b,d)]
    actions={}; leaves={}
    def solve(h):
        if len(h)==n:
            leaves[h]=h;return h
        children=[solve(h+(a,)) for a in range(k)]
        vals=[payoff(interests,original,children[a],a) for a in range(k)]
        best=max(vals);candidates=[a for a in range(k) if vals[a]==best]
        a=(forced_root if not h and forced_root is not None else rng.choice(candidates))
        assert a in candidates
        actions[h]=a;leaves[h]=children[a];return children[a]
    q=solve(())
    comparisons=0
    for h,a in actions.items():
        own=payoff(interests,original,leaves[h],a)
        for t in range(k):
            assert own>=payoff(interests,original,leaves[h+(t,)],t)
            comparisons+=1
    c=[sum(a in ix for a in q) for ix in interests]
    E=sum((F(d[x]*c[x],(b[x]+c[x])*(b[x]+d[x]+c[x]))
           for x in range(len(interests)) if c[x]),F())
    totalK=totalA=totalR=F();nodes=[]
    for j,a in enumerate(q):
        h=q[:j]
        p=[sum(t in ix for t in h) for ix in interests]
        K=max(sum((F(d[x],(b[x]+p[x]+1)*(b[x]+p[x]+d[x]+1))
                   for x in range(len(interests)) if t in interests[x]),F()) for t in range(k))
        A=sum((F(d[x],(b[x]+c[x])*(b[x]+d[x]+c[x]))
               for x in range(len(interests)) if a in interests[x]),F())
        own_b=payoff(interests,b,q,a)
        gains=[];slacks=[]
        for t in range(k):
            z=leaves[h+(t,)]
            orig=payoff(interests,original,z,t)
            deleted=payoff(interests,b,z,t)
            Delta=deleted-orig
            Gamma=payoff(interests,original,q,a)-orig
            gain=deleted-own_b
            assert Gamma>=0
            assert Delta<=K
            assert gain==Delta-A-Gamma
            assert gain<=K-A
            gains.append(gain);slacks.append(K-Delta+Gamma)
        R=max(F(),*gains)
        assert R<=K-A
        assert K-A-R==min(slacks)
        totalK+=K;totalA+=A;totalR+=R
        nodes.append({'position':j+1,'K':str(K),'A':str(A),'R':str(R)})
    assert totalA==E
    assert totalR<=totalK-E
    return {'n':n,'topics':k,'customers':len(interests),'nodes':len(actions),
            'original_comparisons':comparisons,'q':q,'R':str(totalR),
            'K':str(totalK),'E':str(E),'slack':str(totalK-E-totalR),
            'node_values':nodes}

def main():
    rng=random.Random(105776332)
    cases=[]
    # Sharp one-tail equality, positive R and E.
    sharp=audit([{0}]*3+[{1}]*2,[0]*5,[2]*3+[1]*2,1,2,rng,forced_root=1)
    assert sharp['R']=='1' and sharp['K']=='2' and sharp['E']=='1' and sharp['slack']=='0'
    cases.append(sharp)
    # Zero-tail, empty customer, all-zero-customer, and random full-history cases.
    cases.append(audit([],[],[],0,3,rng))
    for n in range(1,4):cases.append(audit([],[],[],n,3,rng))
    for case in range(60):
        k=3+(case%2);n=1+(case%3);N=case%9
        ix=[{t for t in range(k) if rng.randrange(2)} for _ in range(N)]
        b=[rng.randrange(4) for _ in range(N)]
        d=[rng.randrange(4) for _ in range(N)]
        cases.append(audit(ix,b,d,n,k,rng))
    result={'claim':'background-deletion actual-node regret bound',
            'status':'finite independent implementation audit; proof is algebraic',
            'cases':len(cases),'nodes':sum(c['nodes'] for c in cases),
            'original_comparisons':sum(c['original_comparisons'] for c in cases),
            'positive_regret_cases':sum(F(c['R'])>0 for c in cases),
            'sharp_case':sharp,'all_cases':cases}
    out=Path(__file__).with_name('background_deletion_blind_audit.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('all_cases','sharp_case')},indent=2))
    print('sharp_case',sharp)
if __name__=='__main__':main()
