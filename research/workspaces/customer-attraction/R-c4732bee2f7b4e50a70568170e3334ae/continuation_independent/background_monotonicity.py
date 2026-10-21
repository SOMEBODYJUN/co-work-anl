"""Exact attacks on deletion/background monotonicity of worst SPE profit."""
import sys,random,json
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance, CustomerType, ExactSPESolver

def profit(inst,b,q):
    pay=inst.topic_payoffs(q)
    return sum((q[a]-b[a])*pay[a] for a in range(inst.topic_count))
def value(k,cs,r,b):
    inst=Instance(tuple(map(str,range(k))),tuple(cs),r+sum(b));solver=ExactSPESolver(inst)
    q=min(solver.outcomes(b),key=lambda q:profit(inst,b,q))
    return profit(inst,b,q),q
rng=random.Random(614)
for trial in range(10000):
    k=3;r=rng.choice([2,3,4]);cs=[]
    for mask in range(1,1<<k):
        val=rng.choice([0,0,1,2,3,5,10])
        if val:cs.append(CustomerType(frozenset(a for a in range(k) if mask>>a&1),val))
    b=tuple(rng.randrange(2) for _ in range(k));a=rng.randrange(k)
    bp=tuple(x+(j==a) for j,x in enumerate(b))
    v,q=value(k,cs,r,b);vp,qp=value(k,cs,r,bp)
    if vp>v:
        print(json.dumps({'trial':trial,'customers':[{'topics':sorted(c.topics),'multiplicity':c.multiplicity} for c in cs], 'r':r,'b':b,'added':a,'q':q,'vp_q':qp,'v':str(v),'vp':str(vp)}));break
else:print('none')
