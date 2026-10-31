"""Independent checks of two explicit state interfaces, no game/LP imports.

The 69-customer input and closed policy are transcribed directly from the
mathematical statement. The n=16 two-family comparison only checks the exact
scalar consequence; its unbounded-scope content comes from the analytic proof.
"""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent


def main():
    types = [((0,), 30), ((1,), 7), ((2,), 5), ((3,), 7),
             ((2, 4), 2), ((2, 5), 2), ((1, 4, 5), 6),
             ((2, 4, 5), 4), ((3, 4, 5), 6)]
    customers = [frozenset(t) for t, number in types for _ in range(number)]
    assert len(customers) == 69

    def choose(h):
        if len(h) < 3:
            return 0
        acount = h.count(0)
        if acount <= 1:
            return 0
        if acount == 2 and 5 in h:
            return 4
        return 5

    def finish(h):
        while len(h) < 4:
            h += (choose(h),)
        return h

    def payoff(z, action):
        return sum((Q(1, sum(a in c for a in z)) for c in customers if action in c), Q(0))

    nodes = deviations = 0
    for depth in range(4):
        for h in product(range(6), repeat=depth):
            nodes += 1
            selected = choose(h)
            value = payoff(finish(h), selected)
            for a in range(6):
                if a == selected:
                    continue
                assert value >= payoff(finish(h+(a,)), a), (h, a)
                deviations += 1
    path = finish(())
    payoffs = [payoff(path, a) for a in path]
    welfare = sum(any(a in c for a in path) for c in customers)

    def profit(portfolio, background):
        result = Q(0)
        for c in customers:
            hits = sum(a in c for a in portfolio)
            if hits:
                old = sum(a in c for a in background)
                result += Q(hits, old+hits)
        return result

    def optimum(r, background):
        return max(profit(p, background) for p in combinations_with_replacement(range(6), r))

    def robust_floor(r, background):
        return max(sum((Q(1, r+sum(a in c for a in background))
                        for c in customers if action in c), Q(0)) for action in range(6))

    froot, fchild = optimum(4, ()), optimum(3, (0,))
    hroot, hchild = robust_floor(4, ()), robust_floor(3, (0,))
    child_profit = profit(path[1:], (path[0],))
    rhs = max(8*hroot, 2*payoffs[0]+max(fchild, 6*hchild))
    assert (nodes, deviations, path, welfare, froot, fchild, hroot, hchild, rhs) == (
        259, 1295, (0,0,0,5), 48, Q(69), Q(41), Q(15,2), Q(15,2), Q(65))

    n = 16
    hn = min(Q(j)+Q(n, j) for j in range(1, n+1))
    shared_lower = (2-hn)/n
    shared_upper = (Q(23-5*n, 6)-Q(2,n))/(n-1)
    assert (hn, shared_lower, shared_upper) == (Q(8), Q(-3,8), Q(-77,120))
    assert shared_lower > shared_upper
    report = {
        "status": "PASS",
        "closed_policy_ordered_nodes": nodes,
        "closed_policy_nonself_deviations": deviations,
        "actual_path": list(path),
        "actual_payoffs": list(map(str, payoffs)),
        "W": welfare,
        "F_root": str(froot), "F_child": str(fchild),
        "h_root": str(hroot), "h_child": str(hchild),
        "floor_max_step_RHS": str(rhs),
        "strict_floor_step_violation": str(froot-rhs),
        "child_actual_profit": str(child_profit),
        "child_actual_half_surplus": str(2*child_profit-fchild),
        "child_static_floor_surplus": str(6*hchild-fchild),
        "surplus_needed_at_parent": str(froot-fchild-2*payoffs[0]),
        "three_remaining_5_over_3_certified_surplus": str(2*Q(3,5)*fchild-fchild),
        "no_go_n": n, "h_n": str(hn),
        "same_f15_1_15_lower": str(shared_lower),
        "same_f15_1_15_upper": str(shared_upper),
        "necessary_relaxed_f15_1_0_upper": str(shared_upper-shared_lower),
        "scope": "Explicit finite SPE and scalar consequences only; general no-go and protected-reserve induction are reconstructed analytically in reserve_state_review.md."
    }
    (BASE / "reserve_states_independent_audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
