"""Independent exact audit of the star family's full policy, iid and security.

No import of the canonical model/solver or either candidate's audit.  The
mathematical all-n proof is in star_independent_review.md; finite checks here
test the implementation and arithmetic, rather than enlarging their scope.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
import json
from pathlib import Path


def intended(prefix, n, K):
    if not prefix:
        return 0
    if len(prefix) < n - 1:
        return 1
    nonb = [a for a in prefix if a != 1]
    if not nonb:
        return 2
    if len(nonb) == 1 and nonb[0] >= 2:
        return next(a for a in range(2, K+2) if a != nonb[0])
    return 1


def finish(prefix, n, K):
    z = list(prefix)
    while len(z) < n:
        z.append(intended(z, n, K))
    return tuple(z)


def own(a, z, n):
    if a == 1:
        return Q(2*(n-1), sum(b == 1 for b in z))
    shared = Q(2, sum(b != 1 for b in z))
    return shared if a == 0 else shared + Q(1, z.count(a))


def policy_audit(n, K):
    rows = 0
    for depth in range(n):
        for h in product(range(K+2), repeat=depth):
            chosen = intended(h, n, K)
            base = own(chosen, finish(h, n, K), n)
            for a in range(K+2):
                value = own(a, finish(h+(a,), n, K), n)
                assert base >= value, (n,K,h,a,base,value)
                rows += 1
    z = finish((), n, K)
    assert z == (0,)+(1,)*(n-1)
    assert all(own(a,z,n)==2 for a in z)
    return {"n": n, "K": K, "exact_ordered_comparisons": rows}


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total+1):
        for rest in compositions(total-first, parts-1):
            yield (first,)+rest


def security_audit(n, K):
    D = 2*K*n + 4*K+n
    s = Q(4*K,D)
    alpha = Q(n,D)
    value = 2-Q(2,D)
    minimum = None
    rows = 0
    # Enumerate all unordered static opponent combinations, including A.
    for counts in compositions(n-1,K+2):
        ncore = counts[0] + sum(counts[2:])
        pay_b = Q(2*(n-1),counts[1]+1)
        pay_c = Q(2,ncore+1) + sum(Q(1,1+c) for c in counts[2:])/K
        expected = (1-s)*pay_b + s*pay_c
        assert expected >= value
        minimum = expected if minimum is None else min(minimum,expected)
        rows += 1
    assert minimum == value
    # Direct dual evaluation for each pure query; Q does not observe the query.
    dual = [2*alpha + (1-alpha)]
    dual += [alpha*Q(2*(n-1),n)+(1-alpha)*2]
    for j in range(K):
        avg_against_one_c = sum(Q(2,2)+Q(1,1+int(j==k)) for k in range(K))/K
        dual.append(alpha*3 + (1-alpha)*avg_against_one_c)
    assert max(dual) == value
    assert all(x == value for x in dual[1:])
    return {"n":n,"K":K,"all_static_count_combinations":rows,
            "value":str(value),"primal_total_petals":str(s),
            "dual_probability_all_B":str(alpha),"dual_values":list(map(str,dual))}


def g(n,t):
    return sum((1-t)**j for j in range(n))/n


def iid_audit():
    n,K=30,100
    s=Q(1,20)
    ub=58*g(n,1-s)
    uc=g(n,s/K)+2*g(n,s)
    threshold=Q(120,59)
    assert ub > threshold
    assert uc > ub
    assert ub == Q(116,57)*(1-Q(1,20**30))
    assert g(n,s/K) >= Q(3971,4000)
    assert 2*g(n,s) > Q(392,375)
    assert Q(3971,4000)+Q(392,375)-Q(116,57)==Q(683,228000)
    lo,hi=Q(50342,10**6),Q(50343,10**6)
    assert 58*g(n,1-lo) < g(n,lo/K)+2*g(n,lo)
    assert 58*g(n,1-hi) > g(n,hi/K)+2*g(n,hi)
    lower_lambda=58*g(n,1-lo)
    upper_lambda=58*g(n,1-hi)
    assert Q(59,2)*lower_lambda > 60
    return {"n":n,"K":K,"B_at_s0":str(ub),"C_at_s0":str(uc),
            "threshold":str(threshold),"s_star_interval":[str(lo),str(hi)],
            "lambda_interval_decimal":[float(lower_lambda),float(upper_lambda)],
            "weak_bridge_gap_lower_decimal":float(Q(59,2)*lower_lambda-60)}


def all_n_symbolic_factor_check():
    # Formal polynomial identity, with sympy used only by this independent audit.
    import sympy as s
    n,K,r=s.symbols('n K r')
    D=2*K*n+4*K+n
    mixing=4*K/D
    value=2-2/D
    expression=(1-mixing)*2*(n-1)/(n-r)+mixing*(2/(r+1)+1-r/(2*K))-value
    claimed=2*r*(r-1)*(2*K*(n+1)+r+1)/(D*(n-r)*(r+1))
    assert s.cancel(expression-claimed)==0
    return str(s.factor(expression))


if __name__=='__main__':
    out={"identity_factor":all_n_symbolic_factor_check(),
         "full_policy_small":[policy_audit(n,K) for n,K in [(2,2),(3,2),(4,3),(5,3),(6,2)]],
         "security_small":[security_audit(n,K) for n in range(2,8) for K in (1,2,3)],
         "iid_n30_K100":iid_audit()}
    p=Path(__file__).with_name('star_independent_audit.json')
    p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({"output":str(p),"policy_comparisons":sum(x['exact_ordered_comparisons'] for x in out['full_policy_small']),
                      "security_count_combinations":sum(x['all_static_count_combinations'] for x in out['security_small']),
                      "n30_K100":out['iid_n30_K100']},indent=2))
