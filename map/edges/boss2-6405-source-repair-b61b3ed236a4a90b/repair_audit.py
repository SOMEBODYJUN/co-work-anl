"""Exact finite checks for this repair, not a general certificate/scheduler finder."""
from fractions import Fraction as F
from itertools import combinations, product
from collections import defaultdict
from math import comb, isqrt
from pathlib import Path
import json


def subsets(k, upper):
    for r in range(upper + 1):
        yield from combinations(range(k), r)


def row_trade(d, k):
    s, L = d - 1, 2 * k * k
    Z = sum(comb(k, u) for u in range(s + 1))
    A = comb(k - 1, s)
    M = 1 + 120 * L * k**4 + 4 * k * Z * A
    a = F(1, M)
    all_y = (1 << k) - 1
    q = defaultdict(F)
    q[(-1, all_y)] += F(1) - F(3, 4 * L)
    for j in range(k):
        q[(j, 0)] += F(1, 8 * k * L)
    for ell in range(k):
        q[(-1, all_y ^ (1 << ell))] += F(1, 8 * k * L)
    coeff = {}
    for S in subsets(k, s):
        mask = sum(1 << i for i in S)
        coeff[mask] = (-1)**(s - len(S)) * comb(k - len(S) - 1, s - len(S))
        q[(-1, mask)] += F(1, 4 * L * Z)
        for j in range(k):
            q[(j, mask)] += F(1, 4 * L * k * Z)
    assert sum(q.values()) == 1
    target = defaultdict(F, {x: (1 - a) * w for x, w in q.items()})
    target[(-1, all_y)] += a * (1 - F(k, L))
    for j in range(k):
        target[(j, all_y)] += a / L
    cfg = defaultdict(F, {x: (1 - a) * w for x, w in q.items()})
    cfg[(-1, all_y)] += a
    for mask, b in coeff.items():
        for j in range(k):
            cfg[(j, mask)] += a * b / L
        cfg[(-1, mask)] -= a * k * b / L
    assert sum(cfg.values()) == 1 and min(cfg.values()) >= 0
    T = 1 + F(s, k)
    assert all(F(mask.bit_count(), k) + int(j >= 0) <= T for (j, mask), w in cfg.items() if w)
    tested = 0
    for S in subsets(k, d):
        mask = sum(1 << i for i in S)
        for incoming in [-1] + (list(range(k)) if len(S) < d else []):
            moment = lambda law: sum(w for (j, y), w in law.items() if y & mask == mask and (incoming == -1 or incoming == j))
            assert moment(target) == moment(cfg)
            tested += 1
    # Two or more different unit heads are pointwise zero in both measures.
    # The natural next mixed monomial differs, including d=k at the domain edge.
    mask = (1 << d) - 1
    moment = lambda law: sum(w for (j, y), w in law.items() if j == 0 and y & mask == mask)
    assert moment(target) == a / L and moment(cfg) == 0
    assert (1 - a) / (60 * L * k**4) - 2 * a >= 0
    return {"d": d, "k": k, "config_states": sum(w > 0 for w in cfg.values()), "representative_monomials": tested}


def raw_row(k):
    L = 2 * k * k
    M = 1 + 60 * L * k**4
    a, p, b = F(1, M), F(k, M * L), F(M - 1, 4 * M * L)
    masses = [k * p, b - (k - 1) * p, p, b - k * p, 1 - 2 * b + (k - 2) * p]
    assert sum(masses) == 1 and min(masses) >= 0
    # Each moment is computed once from legal CONFIG classes and once from the original law.
    assert (masses[0] + masses[1]) / k == (p + b) / k
    assert masses[0] / (k * k) == p / k
    assert masses[0] / k + masses[3] * F(k - 1, k) + masses[4] == 1 - b - b / k
    assert masses[3] * F(k - 2, k) + masses[4] == 1 - b - 2 * b / k
    assert (1 - a) / (30 * L * k**4) - 2 * a == 0


def nc_case(k, r, d, q):
    t = min(d, q)
    p = F(1) if t == 1 else min(F(1), F(comb(k, t), r**(t - 1) * comb(q, t)))
    atoms = defaultdict(F)
    for h in range(r):
        for z, prob in [(q, p), (1, 1 - p)]:
            if not prob:
                continue
            others = [g for g in range(r) if g != h]
            for chosen in combinations(range(k), z):
                for groups in combinations(others, k - z):
                    for labels in product(range(k), repeat=k-z):
                        sent = [0] * r
                        sent[h] = sum(1 << j for j in chosen)
                        for g, j in zip(groups, labels):
                            sent[g] = 1 << j
                        weight = prob / (r * comb(k, z) * comb(r - 1, k - z) * k**(k-z))
                        atoms[(h, tuple(sent))] += weight
    assert sum(atoms.values()) == 1
    big = [F(0)] * r
    small = [[F(0)] * k for _ in range(r)]
    cylinder = {S: F(0) for S in subsets(k, d) if len(S) >= 2}
    success = F(0)
    for (h, sent), weight in atoms.items():
        assert sum(mask.bit_count() for mask in sent) == k
        big[h] += weight
        loads = [F(1) - F(mask.bit_count(), k) + int(g == h) for g, mask in enumerate(sent)]
        loads += [F(mask.bit_count(), k) for mask in sent]
        peak = max(loads)
        assert peak == 2 - F(sent[h].bit_count(), k)
        if peak <= 2 - F(q, k):
            success += weight
        for g, mask in enumerate(sent):
            for j in range(k):
                if mask & (1 << j):
                    small[g][j] += weight
        for S in cylinder:
            if sent[0] & sum(1 << j for j in S) == sum(1 << j for j in S):
                cylinder[S] += weight
    assert all(v == F(1, r) for v in big)
    assert all(v == F(1, r) for row in small for v in row)
    for S, value in cylinder.items():
        assert value <= F(1, r**len(S))
        expect = F(0) if len(S) > q else p * F(comb(q, len(S)), r * comb(k, len(S)))
        assert value == expect
    assert success == p
    return {"k": k, "r": r, "d": d, "q": q, "p": str(p), "atoms": len(atoms)}


def gated_case(states, resource_count):
    n = len(states)
    beta = F(0)
    for owners in product(range(-1, n), repeat=resource_count):
        values = [max(sum(w for u, w in state if owners[u] == g) for state in menu) for g, menu in enumerate(states)]
        ordered = sorted(values, reverse=True)
        for h, value in enumerate(ordered, 1):
            beta = max(beta, min(F(h, n), value))
    root = ("root",)
    jobs = [[(root, F(1))]]
    for g, menu in enumerate(states):
        gate = ("gate", g)
        jobs.append([(root, F(1, n)), (gate, F(1))])
        jobs.append([(gate, F(1))] + [(("private", g, s), F(1)) for s in range(len(menu))])
        for s, state in enumerate(menu):
            assert sum(w for _, w in state) == 1
            for u, w in state:
                jobs.append([(("private", g, s), w), (("resource", u), F(1))])
    opt, schedules = None, 0
    for assignment in product(*jobs):
        loads = defaultdict(F)
        for machine, time in assignment:
            loads[machine] += time
        peak = max(loads.values())
        opt = peak if opt is None else min(opt, peak)
        schedules += 1
    assert opt == 2 - beta
    return {"groups": n, "jobs": len(jobs), "resources": resource_count, "complete_assignments": schedules, "beta": str(beta), "opt": str(opt)}


def one_sided_search():
    cases = 0
    for U in range(1, 13):
        for qstar in range(1, U + 1):
            for prefix in product([False, True], repeat=qstar-1):
                accepted = [False] + list(prefix) + [True] * (U - qstar + 1)
                lo, hi = 0, U
                assert accepted[hi]
                while hi - lo > 1:
                    mid = (hi + lo) // 2
                    if accepted[mid]:
                        hi = mid
                    else:
                        lo = mid
                    assert lo < qstar and accepted[hi]
                assert hi <= qstar
                cases += 1
    return cases


def main():
    out = {}
    out["row_trade"] = [row_trade(d, k) for d, k in [(2, 2), (3, 3), (4, 4), (4, 7), (2, 8), (5, 8)]]
    for k in range(2, 101):
        raw_row(k)
        optimum = min(F(q, k) for q in range(k, 2*k+1) if (2*k-q)**2 <= k)
        assert optimum == 2 - F(isqrt(k), k)
        L = 2 * k * k
        assert 12*k*L + 12*L*k**3 + 6*k*L*(k-1)**2 <= 30*L*k**3
        for d in range(2, k+1):
            s = d - 1
            for r in range(s+1):
                total = sum((-1)**(s-u) * comb(k-u-1, s-u) * comb(k-r, u-r) for u in range(r, s+1))
                assert total == 1
    out["raw_and_optimum_k_range"] = [2, 100]
    out["nc_laws"] = [nc_case(*case) for case in [(2,2,1,2), (2,4,2,1), (2,4,2,2), (3,3,3,2), (3,4,3,3), (4,4,2,3), (4,6,4,4)]]
    one, half, zero = F(1), F(1,2), F(0)
    out["complete_gated_matrices"] = [
        gated_case([[[(0, one)]]], 1),
        gated_case([[[(0, one)]], [[(0, one)]]], 1),
        gated_case([[[(0, one)]], [[(1, one)]]], 2),
        gated_case([[[(0, one), (1, zero)], [(0, one), (1, zero)]], [[(0, half), (1, half)], [(0, half), (1, half)]]], 3),
    ]
    sorting_cases = 0
    for n in range(1, 6):
        for qualities in product([F(i,4) for i in range(5)], repeat=n):
            ordered = sorted(qualities, reverse=True)
            beta = max(min(F(k,n), value) for k, value in enumerate(ordered, 1))
            assert sum(qualities) <= n * (2*beta-beta*beta)
            sorting_cases += 1
    out["sorting_cases"] = sorting_cases
    for i in range(1001):
        beta = F(i,1000)
        D = (18 - 13*beta)/8
        margin = D*D-(1-F(5,8)*beta*beta)
        assert margin == (209*beta*beta - 468*beta + 260)/64 >= F(1,64)
    out["ratio_margin_endpoints"] = {str(b): str(((18-13*b)/8)**2 - (1-F(5,8)*b*b)) for b in [F(0),F(10,13),F(1)]}
    out["one_sided_nonmonotone_acceptance_tables"] = one_sided_search()
    for k in range(1, 31):
        x, y = F(1,3**k), F(2**k,3**k)
        delta = (2-x)*(2-2*y/3)-(2-x/3)*(2-y)
        assert delta == x*F(1,3)*(2*2**k-4+2**k*x) > 0
    out["palette_gap_at_one"] = str((2-F(1,3))/(2-F(2,3)))
    # Weakening strict external alternatives to >=T/2 would delete a used edge.
    # j at i has time 1; a,b each take 1/2 at i or the same external machine z.
    T, p_j, total_F, W = F(1), F(1), F(1), F(1,2)
    assert p_j + total_F - W > T
    assert max(p_j, F(1,2)+F(1,2)) == T
    out["weak_heavy_threshold_counterexample"] = {"T": "1", "false_lower_bound": "3/2", "actual_peak": "1"}
    # For every raw/fixed-d target, tiny<=T/2<unit<=T. The star injections
    # into other U / distinct B / distinct Z saturate all eligible tasks.
    for k in range(2, 101):
        for s in range(1,k):
            T = 1 + F(s,k)
            assert F(1,k) <= T/2 < 1 <= T
    for i in range(1,1001):
        delta = F(i,1000)
        D, C, e0 = 40/delta, 400/delta**2, delta**2/800
        assert 1/(D-1) <= delta/20
        assert e0*D == delta/20 and F(9,10)*C/D == 9/delta
        assert F(9,10)*e0 == 9*delta**2/8000
        assert (1-delta/20)**2 * F(9,2) >= F(9,4)
    out["all_assertions_passed"] = True
    target = Path(__file__).with_name("repair_audit.json")
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
