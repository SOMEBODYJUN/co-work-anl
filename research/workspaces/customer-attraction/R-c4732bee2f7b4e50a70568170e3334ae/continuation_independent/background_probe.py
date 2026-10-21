"""Exploratory exact background-profit ratios; finite evidence, never a theorem."""
import sys,random,json
from fractions import Fraction
from itertools import product
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance, CustomerType, ExactSPESolver

def compositions(n,k):
    if k==1: yield (n,);return
    for a in range(n+1):
        for z in compositions(n-a,k-1):yield (a,)+z

def run(seed=613,count=300):
    rng=random.Random(seed);best=Fraction(0); record=None
    for trial in range(count):
        k=rng.choice([3,4]);r=rng.choice([3,4,5]);bgsize=rng.choice([1,2,3]);m=r+bgsize
        cs=[]
        for mask in range(1,1<<k):
            val=rng.choice([0,0,0,1,2,3,5,10,20])
            if val:cs.append(CustomerType(frozenset(a for a in range(k) if mask>>a&1),val))
        inst=Instance(tuple(map(str,range(k))),tuple(cs),m);solver=ExactSPESolver(inst)
        b=rng.choice(tuple(compositions(bgsize,k)))
        def profit(q):
            pay=inst.topic_payoffs(q)
            return sum((q[a]-b[a])*pay[a] for a in range(k))
        outcomes=solver.outcomes(b);worst=min(outcomes,key=profit);val=profit(worst)
        opt=max(profit(tuple(x+y for x,y in zip(b,t))) for t in compositions(r,k))
        ratio=opt/val if val else Fraction(1)
        if ratio>best:
            best=ratio;record={'trial':trial,'instance':inst.to_dict(),'background':b,'worst':worst,'profit':str(val),'optimal_profit':str(opt),'ratio':str(ratio)}
            print(json.dumps(record),flush=True)
    return record
if __name__=='__main__':
    rec=run(count=int(sys.argv[1]) if len(sys.argv)>1 else 300)
    print('FINAL '+json.dumps(rec))
