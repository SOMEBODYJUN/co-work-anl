"""Definition-level Fraction verification; no scipy or probe imports."""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]


def main():
    obj=json.loads((BASE/'pair_dilution_obstruction.json').read_text())
    n,p=obj['n'],obj['p']
    actions={tuple(x['history']):x['action'] for x in obj['strategy_actions']}
    assert set(actions)=={h for d in range(n) for h in product(range(p),repeat=d)}
    y={(tuple(x['q']),x['a']):Fraction(x['value']) for x in obj['y']}
    terminals={}
    for d in range(n,-1,-1):
        for h in product(range(p),repeat=d):
            terminals[h]=tuple(h.count(a) for a in range(p)) if d==n else terminals[h+(actions[h],)]
    vs={(q,a) for h in product(range(p),repeat=n) for q in [tuple(h.count(a) for a in range(p))]
        for a in range(p) if q[a]}
    assert set(y)==vs and all(v>=0 for v in y.values())
    graph_count=0
    for h,a in actions.items():
        for b in range(p):
            assert y[(terminals[h+(b,)],b)]<=y[(terminals[h],a)]
            graph_count+=1
    dilution_count=0
    for q,a in vs:
        for r,b in vs:
            if a!=b or q==r:continue
            kapp=max(Fraction(sum(r[c] for c in range(p) if mask>>c&1),
                              sum(q[c] for c in range(p) if mask>>c&1))
                     for mask in range(1,1<<p) if mask>>a&1)
            assert y[(q,a)]<=kapp*y[(r,a)]
            dilution_count+=1
    root=terminals[()]
    portfolio=obj['portfolio']
    opt=tuple(portfolio.count(a) for a in range(p))
    W=sum(root[a]*y[(root,a)] for a in range(p) if root[a])
    O=sum(opt[a]*y[(opt,a)] for a in range(p) if opt[a])
    assert W==1 and O==Fraction(9,4) and O>2*W
    # Independently verify source strategy against its original unit customers.
    source=json.loads((ROOT/obj['unit_customer_source']).read_text())
    customers=[(frozenset(x['topics']),x['multiplicity']) for x in source['customers']]
    def utility(q,a):
        return sum(Fraction(mult,sum(q[b] for b in B)) for B,mult in customers if a in B)
    actual_comparisons=0
    for h,a in actions.items():
        for b in range(p):
            assert utility(terminals[h],a)>=utility(terminals[h+(b,)],b)
            actual_comparisons+=1
    # Demonstrate why y cannot come from ANY common customer weights: full-
    # repetition utility fixes C({a})=n*y_(n e_a,a), then Shapley marginal rows
    # have universal identities. It suffices here to test equal-coverage sums.
    same_support_violation=None
    coverage={}
    for q in sorted({q for q,a in vs}):
        supp=tuple(a for a in range(p) if q[a])
        value=sum(q[a]*y[(q,a)] for a in supp)
        if supp in coverage and coverage[supp][1]!=value:
            same_support_violation=(supp,coverage[supp],(q,value));break
        coverage[supp]=(q,value)
    assert same_support_violation is not None
    print(json.dumps({'exact':True,'vertices':len(vs),'graph_checks_including_self':graph_count,
                      'sharp_dilution_checks':dilution_count,'source_SPE_checks':actual_comparisons,
                      'root_payoff_sum':str(W),'comparison_payoff_sum':str(O),
                      'same_support_coverage_violation':str(same_support_violation)},indent=2))


if __name__=='__main__':main()
