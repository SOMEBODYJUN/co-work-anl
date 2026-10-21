"""Exact repair certificate using 3 true comparison rows and 2 pair circuits."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

BASE=Path(__file__).resolve().parent

def main():
    obj=json.loads((BASE/'support_conservation_obstruction.json').read_text())
    n,p=obj['n'],obj['p'];assert n==3 and p==6
    actions={tuple(x['history']):x['action'] for x in obj['strategy_actions']}
    counts=sorted({tuple(h.count(a) for a in range(p)) for h in product(range(p),repeat=n)})
    vs=[(q,a) for q in counts for a in range(p) if q[a]]
    vid={v:i for i,v in enumerate(vs)}
    def v(labels,a):
        q=tuple(labels.count(b) for b in range(p))
        row=[Fraction(0)]*len(vs);row[vid[q,a]]=1;return row
    def add(*terms):return [sum(t[i] for t in terms) for i in range(len(vs))]
    def scale(c,row):return [c*x for x in row]
    def terminal(h):
        while len(h)<n:h=h+(actions[h],)
        return h
    # Nonnegative y rows (target minus source) from actual terminal deviations.
    gs=[]
    for h,b in [((2,4),1),((4,2),3),((4,4),2)]:
        a=actions[h]
        gs.append(add(v(terminal(h),a),scale(-1,v(terminal(h+(b,)),b))))
    assert gs[0]==add(v((2,3,4),3),scale(-1,v((1,2,4),1)))
    assert gs[1]==add(v((0,2,4),0),scale(-1,v((2,3,4),3)))
    assert gs[2]==add(v((3,4,4),3),scale(-1,v((2,4,4),2)))
    # Each row kappa*target - source is universally nonnegative per type.
    specs=[(2,(0,3,4),4,(3,4,4),4,1),
           (2,(0,3,4),3,(3,3,4),3,1),
           (1,(2,2,4),2,(1,2,4),2,2),
           (1,(2,4,4),4,(1,2,4),4,2),
           (1,(0,3,4),0,(0,2,4),0,2)]
    ds=[]
    for mult,target,a,source,b,kappa in specs:
        assert a==b
        row=add(scale(kappa,v(target,a)),scale(-1,v(source,b)))
        qt=tuple(target.count(c) for c in range(p));qs=tuple(source.count(c) for c in range(p))
        sharp=max(Fraction(sum(qt[c] for c in range(p) if B>>c&1),sum(qs[c] for c in range(p) if B>>c&1)) for B in range(1,1<<p) if B>>a&1)
        assert sharp==kappa
        ds.append(scale(mult,row))
    def circuit(a,b):
        # I_ab = 2Ua(2a+b)+2Ub(a+2b)-Ua(a+2b)-3Ub(3b).
        return add(scale(2,v((a,a,b),a)),scale(2,v((a,b,b),b)),scale(-1,v((a,b,b),a)),scale(-3,v((b,b,b),b)))
    I24,I34=circuit(2,4),circuit(3,4)
    # Check universal signed identities directly at every customer type.
    for B in range(1,1<<p):
        values=[]
        for q,a in vs:
            values.append(Fraction(int(B>>a&1),sum(q[c] for c in range(p) if B>>c&1)) if B>>a&1 else Fraction(0))
        assert sum(x*y for x,y in zip(I24,values))==0
        assert sum(x*y for x,y in zip(I34,values))==0
    budget=add(*[scale(2,v((0,3,4),a)) for a in (0,3,4)],*[scale(-1,v((1,2,4),a)) for a in (1,2,4)])
    # Full Farkas vector equality; no samples or LP state are trusted.
    rhs=add(*gs,*ds,scale(-1,I24),I34)
    assert budget==rhs
    print(json.dumps({'exact':True,'target_factor':'2','vertices':len(vs),'true_comparison_rows':3,'universal_sharp_dilution_rows':5,'cross_topic_circuits':2,'pointwise_identity_checks':2*((1<<p)-1),'coefficient_checks':len(vs),'uses_support_conservation':False,'uses_nonnegative_customer_weights_for_circuits':False},indent=2))

if __name__=='__main__':main()
