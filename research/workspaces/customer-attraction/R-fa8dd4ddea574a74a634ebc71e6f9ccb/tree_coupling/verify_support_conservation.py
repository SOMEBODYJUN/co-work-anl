"""Definition-level exact checker. Does not import LP/probe implementations."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

BASE=Path(__file__).resolve().parent

def main():
    obj=json.loads((BASE/'support_conservation_obstruction.json').read_text())
    n,p=obj['n'],obj['p']
    actions={tuple(row['history']):row['action'] for row in obj['strategy_actions']}
    assert set(actions)=={h for d in range(n) for h in product(range(p),repeat=d)}
    y={(tuple(row['q']),row['a']):Fraction(row['value']) for row in obj['y']}
    counts={tuple(h.count(a) for a in range(p)) for h in product(range(p),repeat=n)}
    vertices={(q,a) for q in counts for a in range(p) if q[a]}
    assert set(y)==vertices and all(z>=0 for z in y.values())
    # Resolve from each ordered history without count-based tie assumptions.
    terminal={}
    for d in range(n,-1,-1):
        for h in product(range(p),repeat=d):
            terminal[h]=tuple(h.count(a) for a in range(p)) if d==n else terminal[h+(actions[h],)]
    graph_checks=0
    for h,a in actions.items():
        for b in range(p):
            assert y[terminal[h],a]>=y[terminal[h+(b,)],b]
            graph_checks+=1
    pair_checks=0
    for q,a in vertices:
        for r,b in vertices:
            if a!=b or q==r:continue
            sharp=max(Fraction(sum(r[c] for c in range(p) if B>>c&1),sum(q[c] for c in range(p) if B>>c&1)) for B in range(1,1<<p) if B>>a&1)
            assert y[q,a]<=sharp*y[r,a]
            pair_checks+=1
    covered={}
    support_checks=0
    for q in sorted(counts):
        support=tuple(a for a in range(p) if q[a])
        total=sum(q[a]*y[q,a] for a in support)
        if support in covered:
            assert covered[support]==total
            support_checks+=1
        else:covered[support]=total
    root=terminal[()]
    opt=tuple(obj['portfolio'].count(a) for a in range(p))
    W=sum(root[a]*y[root,a] for a in range(p) if root[a])
    O=sum(opt[a]*y[opt,a] for a in range(p) if opt[a])
    assert W==1 and O==Fraction(9,4)>2*W
    # Every common SIGNED customer representation satisfies this identity.
    q=(2,1,0,0,0,0)
    ca,cb,cab=covered[(0,)],covered[(1,)],covered[(0,1)]
    lhs=6*y[q,0]
    rhs=2*ca+cab-cb
    assert (y[q,0],ca,cb,cab,lhs,rhs)==(Fraction(3,8),Fraction(3,4),Fraction(3,4),Fraction(1),Fraction(9,4),Fraction(7,4))
    assert lhs!=rhs
    # Verify the universal identity directly for every interest type B.
    identity_checks=0
    for B in range(1,1<<p):
        F=Fraction(int(B&1!=0),sum(q[a] for a in range(p) if B>>a&1)) if B&1 else Fraction(0)
        ka=int(B&1!=0);kb=int(B&2!=0);kab=int(B&3!=0)
        assert 6*F==2*ka+kab-kb
        identity_checks+=1
    print(json.dumps({'exact':True,'ordered_histories':len(actions),'vertices':len(vertices),'graph_checks':graph_checks,'sharp_pair_checks':pair_checks,'support_classes':len(covered),'independent_support_conservation_checks':support_checks,'root_budget':str(W),'portfolio_budget':str(O),'universal_identity_checks':identity_checks,'violated_identity_lhs':str(lhs),'violated_identity_rhs':str(rhs)},indent=2))

if __name__=='__main__':main()
