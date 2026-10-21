"""Independent Fraction audit of the monotone-support obstruction.

This verifier imports neither the LP nor an optimizer/model helper. The pseudo
payoff table is not a customer instance; the source strategy is separately
verified on its original 22 unit customers.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def main():
    obj=json.loads((HERE/'monotone_candidate.json').read_text())
    m,p=3,6
    assert (obj['m'],obj['p'])==(m,p)
    def prescribed(h):
        if not h:return 0
        if len(h)==1:return 3 if h[0]<3 else 0
        group=range(3) if h[1]<3 else range(3,6)
        return min(a for a in group if a not in h)
    policies={h:prescribed(h) for d in range(m) for h in product(range(p),repeat=d)}
    assert policies=={tuple(z['history']):z['action'] for z in obj['strategy_actions']}
    def outcome(h):
        while len(h)<m:h=h+(prescribed(h),)
        return tuple(h.count(a) for a in range(p))
    qs={tuple(h.count(a) for a in range(p)) for h in product(range(p),repeat=m)}
    vertices={(q,a)for q in qs for a in range(p)if q[a]}
    y={(tuple(z['q']),z['a']):Q(z['y'])for z in obj['vertices']}
    assert set(y)==vertices and min(y.values())>=0
    # This original 22-customer instance only certifies the graph's provenance.
    customers=[(frozenset([a]),c)for a,c in enumerate([1,3,1,1,3,1])]
    customers += [(frozenset([0,1,2,3,5]),6),(frozenset([0,2,3,4,5]),6)]
    def u(q,a):return sum(Q(c,sum(q[b]for b in B))for B,c in customers if a in B)
    graph_count=source_count=0
    for h,a in policies.items():
        for b in range(p):
            qa,qb=outcome(h),outcome(h+(b,))
            assert y[qb,b]<=y[qa,a]
            assert u(qb,b)<=u(qa,a)
            graph_count+=1;source_count+=1
    # Check every sharp pointwise same-label ratio independently, directly over
    # all nonempty interest types B containing that label.
    dilution_count=0
    for q,a in vertices:
        for r,b in vertices:
            if a!=b or q==r:continue
            k=max(Q(sum(r[c]for c in range(p)if mask>>c&1),
                    sum(q[c]for c in range(p)if mask>>c&1))
                  for mask in range(1,1<<p)if mask>>a&1)
            assert y[q,a]<=k*y[r,a]
            dilution_count+=1
    coverage={frozenset():Q(0)};efficiency_checks=0
    for q in qs:
        S=frozenset(a for a in range(p)if q[a])
        value=sum(q[a]*y[q,a]for a in S)
        if S in coverage:assert value==coverage[S]
        else:coverage[S]=value
        efficiency_checks+=1
    assert len(coverage)==42
    monotone_count=0
    for A in coverage:
        for B in coverage:
            if A<=B:
                assert coverage[A]<=coverage[B];monotone_count+=1
    root=outcome(());J=frozenset([1,2,4])
    W=sum(root[a]*y[root,a]for a in range(p)if root[a])
    O=coverage[J]
    assert root==(1,0,0,1,1,0) and W==1 and O==Q(9,4)>2*W
    # Failure of a single necessary coverage inequality proves there is no
    # common nonnegative customer measure producing this table.
    A,B=frozenset([4,5]),frozenset([3,5])
    assert (coverage[A],coverage[B],coverage[A|B],coverage[A&B])==(Q(3,4),Q(31,40),Q(23,20),Q(5,12))
    defect=coverage[A|B]+coverage[A&B]-coverage[A]-coverage[B]
    assert defect==Q(1,24)>0
    # Check an even more basic linear consistency identity: for three players,
    # utility of a doubled label is (2C(a)-C(b)+C(ab))/6.
    linear_failure=None
    for a in range(p):
        for b in range(p):
            if a==b:continue
            q=tuple(2*int(i==a)+int(i==b)for i in range(p))
            rhs=(2*coverage[frozenset([a])]-coverage[frozenset([b])]+coverage[frozenset([a,b])])/6
            if y[q,a]!=rhs:
                linear_failure={'a':a,'b':b,'y':str(y[q,a]),'required':str(rhs)};break
        if linear_failure:break
    assert linear_failure is not None
    return {'status':'exact_audit_passed','claim':'monotone support efficiency does not repair graph plus all sharp pairwise dilution',
            'players':m,'topics':p,'vertices':len(vertices),'source_customers':sum(c for _,c in customers),
            'source_SPE_comparisons':source_count,'pseudo_graph_comparisons':graph_count,
            'sharp_dilution_comparisons':dilution_count,'support_efficiency_checks':efficiency_checks,
            'visible_supports_including_empty':len(coverage),'monotonicity_checks_including_equality':monotone_count,
            'actual_surrogate':str(W),'comparison_surrogate':str(O),'submodular_defect':str(defect),
            'linear_shapley_inconsistency':linear_failure,
            'scope':'Template obstruction, not an SPE customer counterexample; general Q-CAG-HALF remains OPEN.'}

if __name__=='__main__':
    result=main();print(json.dumps(result,indent=2))
