"""Independent, self-contained Fraction audit of the core/satellite family.

No canonical solver, original packet, LP, or floating-point optimization is
imported. Complete histories are enumerated only for small regressions. The
large n=30,K=100 case uses the universal classification proved in README.md;
we do not pretend to enumerate its exponentially many histories.
"""
from fractions import Fraction as F
from itertools import product
from decimal import Decimal, localcontext
from pathlib import Path
import json


def policy(h, n, K):
    # labels A=0, B=1, C_j=j+2 (0 <= j < K).
    if not h:
        return 0
    if len(h) < n - 1:
        return 1
    nonB = [a for a in h if a != 1]
    if not nonB:
        return 2
    if len(nonB) == 1 and nonB[0] >= 2:
        return 3 if nonB[0] == 2 else 2
    return 1


def terminal(h, n, K):
    while len(h) < n:
        h += (policy(h, n, K),)
    return h


def utility(a, z, n, K):
    if a == 1:
        return F(2 * (n - 1), z.count(1))
    core = F(2, sum(b != 1 for b in z))
    return core + (F(1, z.count(a)) if a >= 2 else 0)


def exhaustive_small(n, K):
    checks = 0
    minimum = None
    for depth in range(n):
        for h in product(range(K + 2), repeat=depth):
            a = policy(h, n, K)
            value = utility(a, terminal(h, n, K), n, K)
            for b in range(K + 2):
                gap = value - utility(b, terminal(h + (b,), n, K), n, K)
                assert gap >= 0, (n, K, h, b, gap)
                minimum = gap if minimum is None else min(minimum, gap)
                checks += 1
    return dict(n=n, K=K, comparisons=checks, minimum_gap=str(minimum))


def h_balanced(r, K):
    q, t = divmod(r, K)
    return F(K - t, K * (q + 1)) + F(t, K * (q + 2))


def exact_security(n, K):
    assert n >= 2 and K >= 1
    D = 2 * K * n + 4 * K + n
    s = F(4 * K, D)
    v = 2 - F(2, D)
    alpha = F(n, D)
    primal_margins = []
    for r in range(n):
        # Any A competitor can be changed to C without increasing query value.
        actual = (1-s) * F(2*(n-1), n-r) + s * (F(2, r+1) + h_balanced(r,K))
        elementary = (1-s) * F(2*(n-1), n-r) + s * (F(2,r+1) + 1-F(r,2*K))
        margin = F(2*r*(r-1)*(2*K*(n+1)+r+1), D*(n-r)*(r+1))
        assert h_balanced(r,K) >= 1 - F(r,2*K)
        assert elementary - v == margin >= 0
        assert actual >= elementary
        primal_margins.append(str(actual-v))
    # Dual Q: all B with mass alpha; B^(n-2)+uniform C otherwise.
    payoff_A = 1 + alpha
    payoff_B = alpha * F(2*(n-1),n) + (1-alpha)*2
    payoff_C = alpha * 3 + (1-alpha)*(2-F(1,2*K))
    assert payoff_B == payoff_C == v
    assert payoff_A <= v
    return dict(D=D, query_total_C=str(s), query_B=str(1-s),
                query_each_C=str(s/K), value=str(v),
                dual_mass_all_B=str(alpha), dual_payoff_A=str(payoff_A),
                dual_payoff_B=str(payoff_B), dual_payoff_C=str(payoff_C),
                exact_primal_margins_by_nonB_competitors=primal_margins,
                W_minus_n_v=str(2*n-n*v))


def g(n, t):
    if not t:
        return F(1)
    return (1-(1-t)**n)/(n*t)


def weak_iid_witness():
    n,K=30,100
    s0=F(1,20)
    B=2*(n-1)*g(n,1-s0)
    C=g(n,s0/K)+2*g(n,s0)
    private_bound=1-F(n-1,2)*s0/K
    core_bound=F(392,375)
    assert F(19,20)**10 < F(3,5)
    assert g(n,s0/K) >= private_bound == F(3971,4000)
    assert 2*g(n,s0) > core_bound
    assert C > private_bound+core_bound == F(24457,12000)
    assert private_bound+core_bound > F(116,57) > B
    assert B == F(116,57)*(1-F(1,20**30))
    assert B > F(120,59)
    guaranteed_gap=F(59,2)*B-60
    assert guaranteed_gap == F(2,57)-F(3422,57*20**30) > 0
    # Numerical display is not used in any exact sign or optimality proof.
    with localcontext() as ctx:
        ctx.prec=70
        lo,hi=Decimal(0),Decimal(1)
        def gd(t):
            return Decimal(1) if not t else (1-(1-t)**n)/(n*t)
        for _ in range(240):
            s=(lo+hi)/2
            Bn=2*(n-1)*gd(1-s)
            Cn=gd(s/K)+2*gd(s)
            if Bn<Cn:
                lo=s
            else:
                hi=s
        root=(lo+hi)/2
        lam=2*(n-1)*gd(1-root)
        numeric=dict(s=str(root),lambda_value=str(lam),
                     iid_total_Z=str(n*lam),weak_iid_payment=str((Decimal(n)-Decimal('.5'))*lam),
                     weak_iid_failure_gap=str((Decimal(n)-Decimal('.5'))*lam-2*n))
    return dict(n=n,K=K,unit_customers=2+2*(n-1)+K,W=2*n,
                exact_B_at_s0=str(B),exact_C_at_s0=str(C),
                threshold=str(F(120,59)),
                proved_strict_weak_iid_gap_lower_bound=str(guaranteed_gap),
                numeric_display=numeric)


def main():
    small=[exhaustive_small(n,K) for n,K in [(2,2),(3,2),(4,3),(5,4)]]
    # Exact finite regressions of the universal symbolic formula.
    for n in range(2,51):
        for K in (1,2,3,10,100):
            exact_security(n,K)
    report=dict(status='Independent exact audit; general classification proof in README.md',
                small_full_history_regressions=small,
                security_formula_regressions=245,
                n30_K100_security=exact_security(30,100),
                weak_iid_counterexample=weak_iid_witness())
    target=Path(__file__).with_name('star_family_exact_audit.json')
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
