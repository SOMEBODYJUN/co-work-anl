"""Fraction audit of deletion identities and a real two-edge square flow.

The proof in notes.md is universal.  The bounded exhaustive checks here audit
the formulas and include zero loads, repeated prefix actions, and absent reply
labels.  The formal square-flow strategy is not a claimed bad SPE.
"""
from fractions import Fraction as F
from itertools import product
import json


def R(q, a, b, mask):
    x = lambda s: int(bool(mask & (1 << s)))
    return F(x(a)-x(b), 1+sum(q[s]*x(s) for s in range(len(q))))


def delta(q, s, a, b, mask):
    x = lambda z: int(bool(mask & (1 << z)))
    load = sum(q[z]*x(z) for z in range(len(q)))
    return F(x(s)*(x(a)-x(b)), load*(load+1)) if x(s) else F(0)


def compositions(total, p):
    if p == 1:
        yield (total,)
    else:
        for a in range(total+1):
            for rest in compositions(total-a, p-1):
                yield (a,)+rest


def universal_formula_audit():
    deletion_checks = recurrence_checks = square_checks = 0
    for p in range(1, 6):
        for total in range(1, 6):
            for q in compositions(total, p):
                for a, b in product(range(p), repeat=2):
                    for mask in range(1, 1 << p):
                        load = sum(q[s]*bool(mask & (1 << s)) for s in range(p))
                        diff = int(bool(mask & (1 << a)))-int(bool(mask & (1 << b)))
                        rhs = F(diff if not load else 0)
                        for s in range(p):
                            if not q[s]:
                                continue
                            smaller = tuple(z-int(j == s) for j, z in enumerate(q))
                            assert delta(q,s,a,b,mask) == R(smaller,a,b,mask)-R(q,a,b,mask)
                            deletion_checks += 1
                            rhs += q[s]*R(smaller,a,b,mask)
                        assert (total+1)*R(q,a,b,mask) == rhs
                        recurrence_checks += 1
                        if q[a] and q[b]:
                            sq = F(diff*diff, load*(load+1)) if load else F(0)
                            assert delta(q,a,a,b,mask)-delta(q,b,a,b,mask) == sq
                            assert sq >= 0
                            square_checks += 1
    return dict(deletion_checks=deletion_checks,
                leave_one_out_recurrence_checks=recurrence_checks,
                square_checks=square_checks)


def reachable_square_audit():
    # n=4, labels A=0,B=1,C=2.  Unlisted early actions are C.
    # All terminal replies are C except ACA -> A.  AAC is its count representative.
    p,n = 3,4
    actions={h:2 for d in range(n) for h in product(range(p),repeat=d)}
    actions[(0,)]=0
    actions[(0,0)]=1
    actions[(0,2)]=0
    actions[(0,2,0)]=0
    changed=(0,2,0)
    normalized=actions.copy();normalized[changed]=2

    def terminals(policy):
        result={h:h for h in product(range(p),repeat=n)}
        for d in range(n-1,-1,-1):
            for h in product(range(p),repeat=d):
                result[h]=result[h+(policy[h],)]
        return result

    old,new=terminals(actions),terminals(normalized)
    assert old[()]==new[()]

    def row(policy, ends, h, a, mask):
        def payoff(end, selected):
            return F(1,sum(bool(mask&(1<<z)) for z in end)) if mask&(1<<selected) else F(0)
        return payoff(ends[h],policy[h])-payoff(ends[h+(a,)],a)

    # Edge 1: source (ACA,C), target (AAB,A); edge 2: source (ACC,C), target (ACA,A).
    edges=[((0,),2),((0,2),2)]
    q=(2,0,1)
    checks=0
    for mask in range(1,1<<p):
        error=sum((row(normalized,new,h,a,mask)-row(actions,old,h,a,mask)
                   for h,a in edges),F(0))
        expected=delta(q,0,0,2,mask)-delta(q,2,0,2,mask)
        assert error==expected and error>=0
        checks+=1
    return dict(real_early_rows=[[list(h),a] for h,a in edges],
                changed_leaf=list(changed),row_identity_checks=checks,
                scope="formal full strategy; square identity, no nontrivial SPE assertion")


if __name__ == "__main__":
    print(json.dumps(dict(status="all_exact_checks_passed",
        formulas=universal_formula_audit(),reachable_square=reachable_square_audit()),indent=2))
