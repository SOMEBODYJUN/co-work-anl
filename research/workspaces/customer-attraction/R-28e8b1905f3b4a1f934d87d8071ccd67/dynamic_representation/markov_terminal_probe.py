"""Compare full-history SPE terminal counts with count-Markov pure SPEs.
Exploratory exact small-state diagnostic; no universal theorem asserted.
"""
from itertools import product
from pathlib import Path
import sys, json, random
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver

def states(p,t):
    if p==1:
        yield (t,); return
    for a in range(t+1):
        for q in states(p-1,t-a): yield (a,)+q

def markov(ins):
    p,m=ins.topic_count,ins.players
    outcomes={}
    pay={q:ins.topic_payoffs(q) for q in states(p,m)}
    levels=[tuple(states(p,t)) for t in range(m)]
    def inc(c,a):return c[:a]+(c[a]+1,)+c[a+1:]
    # Recursively instantiate every Markov continuation, deepest level first.
    found={}
    count=0
    def visit(t, mapping):
        nonlocal count
        if t<0:
            q=mapping[(0,)*p]
            found.setdefault(q,dict(mapping));count+=1
            return
        level=levels[t]
        choices=[]
        for c in level:
            targets=[inc(c,a) if t==m-1 else mapping[inc(c,a)] for a in range(p)]
            vals=[pay[q][a] for a,q in enumerate(targets)]
            best=max(vals)
            choices.append(tuple(q for a,q in enumerate(targets) if vals[a]==best))
        for qs in product(*choices):
            changed=dict(mapping);changed.update(zip(level,qs));visit(t-1,changed)
    visit(m-1,{})
    return set(found), count

def main():
    rng=random.Random(16671)
    p,m=3,3
    for j in range(400):
        weights=tuple(rng.randrange(5) for _ in range((1<<p)-1))
        ins=Instance(tuple(map(str,range(p))),tuple(CustomerType(tuple(a for a in range(p) if mask>>a&1),weights[mask-1]) for mask in range(1,1<<p) if weights[mask-1]),m)
        full=ExactSPESolver(ins).outcomes();mp,n=markov(ins)
        if full!=mp:
            print(json.dumps({'weights':weights,'full':sorted(full),'markov':sorted(mp),'count':n,'instance':ins.to_dict()},default=str));return
    print('No difference on 400 fixed-seed p3,m3 inputs')
if __name__=='__main__':main()
