import sys,random,json,itertools,time
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[6]))
from customer_attraction.model import CustomerType,Instance
from customer_attraction.exact import ExactSPESolver
rng=random.Random(879162)
best=Fraction(0); tested=0
for t in range(5000):
    k=rng.choice([5,6,7]); m=rng.choice([2,3,4,5])
    # sparse interest patterns, actual noncoverage plausible
    types=[]
    for mask in range(1,1<<k):
        sz=mask.bit_count()
        if rng.random()< (0.65 if sz==1 else .19 if sz==2 else .05 if sz==3 else .012):
            types.append(CustomerType(frozenset(i for i in range(k) if mask>>i&1),rng.randint(1,25)))
    if not types:continue
    inst=Instance(tuple(map(str,range(k))),tuple(types),m)
    solver=ExactSPESolver(inst)
    opts=[];opt=inst.optimal_welfare()
    supports=[]
    for size in range(1,min(k,m)+1):
        for support in itertools.combinations(range(k),size):
            q=tuple(int(i in support) for i in range(k))
            if inst.welfare(q)==opt:opts.append(frozenset(support))
    for q in solver.outcomes():
        C=[a for a in types if any(q[i] for i in a.topics)]
        D=max(sum(a.multiplicity for a in types if not any(q[i] for i in a.topics) and a.topics&S) for S in opts)
        low=min(x for x,c in zip(inst.topic_payoffs(q),q) if c)
        tested+=1
        ratio=Fraction(D,m)/low if low else Fraction(0)
        if ratio>best:
            best=ratio
            if best>Fraction(4,5):print('best',str(best),'m',m,'t',t,'D',D,'low',str(low),flush=True)
        if D>m*low:
            out={'instance':inst.to_dict(),'terminal':q,'opt':opt,'D':D,'low':str(low),'ratio':str(ratio)}
            Path(__file__).with_name('min_floor_counterexample.json').write_text(json.dumps(out,indent=2))
            print(json.dumps(out),flush=True);sys.exit()
print('no violation',tested,'best',best)
