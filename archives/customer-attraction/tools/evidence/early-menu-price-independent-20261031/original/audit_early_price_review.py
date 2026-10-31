"""Independent Fraction audit of B5-EARLY-MENU-LOAD-DEFECT-v1.

No imports from the author's audit or the game solver.  The finite checks
below audit identities and edge cases; the review gives the general proof.
Run from the repository root.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[5]
COUNTS = {"scalar_identities": 0, "range_bounds": 0,
          "remainder_bounds": 0, "scalings": 0,
          "spe_rows": 0, "real_menus": 0, "real_inequalities": 0,
          "relay_payment_bounds": 0, "root_envelope_points": 0,
          "zero_defect_menus": 0}


def inv(n):
    return F(1, n)


def share(numerator, denominator):
    return F(numerator, denominator) if numerator else F(0)


def gamma(xis, phis):
    aa, lo, pp = max(xis), min(xis), max(phis)
    assert aa >= 0 and lo <= 0 and 0 <= pp <= aa
    bb = pp - lo
    gg = aa if bb <= aa else (aa + bb) ** 2 / (4 * bb)
    assert 0 <= gg <= aa - lo / 4
    return gg


def scalar_audit():
    mus = [(F(1), F(0), F(0)), (F(0), F(1), F(0)),
           (F(1, 2), F(1, 3), F(1, 6)), (F(1, 3),) * 3]
    for d in range(4):
        ds = sorted(set((-d, 0, 1, 3)))
        for delta1, delta2 in product(ds, repeat=2):
            delta = (0, delta1, delta2)
            xis = tuple(inv(d + 1) - inv(d + dd + 1) for dd in delta)
            zs = tuple(inv((d + 1) * (d + 2))
                       - inv((d + dd + 1) * (d + dd + 2)) for dd in delta)
            phis = tuple(xx - zz for xx, zz in zip(xis, zs))
            gg = gamma(xis, phis)
            for a, b, s1, s2, r1, r2 in product((0, 1), repeat=6):
                ss, rr = (a, s1, s2), (b, r1, r2)
                av = share(a, d + a + b)
                bw = share(b, d + a + b)
                for mu in mus:
                    ee = sum(mm * r for mm, r in zip(mu, rr))
                    eps = sum(mm * ((s - r + ee) * xx - ee * s * zz)
                              for mm, s, r, xx, zz
                              in zip(mu, ss, rr, xis, zs))
                    assert eps <= gg
                    COUNTS["range_bounds"] += 1
                    for tau in (F(1, 3), F(1), F(7, 3)):
                        weights = tuple(tau * mm for mm in mu)
                        s_real = tau * av - sum(
                            z * s * inv(d + dd + 1 + r)
                            for z, s, r, dd in zip(weights, ss, rr, delta))
                        s_ref = tau * av - sum(
                            z * s * inv(d + 1 + r)
                            for z, s, r in zip(weights, ss, rr))
                        v_real = sum(
                            weights[j] * weights[k] * (rr[j] - rr[k])
                            * inv(d + delta[j] + 1 + ss[j])
                            for j, k in product(range(3), repeat=2))
                        v_ref = sum(
                            weights[j] * weights[k] * (rr[j] - rr[k])
                            * inv(d + 1 + ss[j])
                            for j, k in product(range(3), repeat=2))
                        assert s_ref - s_real + (v_ref - v_real) / tau == -tau * eps
                        defect_delta = sum(mu[j] * mu[k] * ss[j] * inv(d + 1 + rr[k])
                                           for j, k in product(range(3), repeat=2))
                        defect_delta -= sum(mu[j] * ss[j] * inv(d + delta[j] + 1 + rr[j])
                                            for j in range(3))
                        assert eps - defect_delta == v_real / tau ** 2
                        # Z cancels in G_ref-G_real for every eta.
                        COUNTS["scalar_identities"] += 1

    for d, a in product(range(6), (0, 1)):
        for tau, qq, eta in product(
                (F(1), F(5, 4), F(3), F(10)),
                (F(0), F(1, 7), F(1)),
                (F(0), F(1, 5), F(1), F(7))):
            t_eta = min(inv(d + 1), inv(d + 2) + eta * inv(d + a + 1))
            bound = max(F(0), qq - t_eta)
            us = sorted(set((F(0), F(1, 7), F(1), tau / 2, tau)))
            ls = (F(0), tau / 7, tau / 2, tau)
            for uu, ll in product(us, ls):
                if not 0 <= uu <= tau:
                    continue
                rem = qq * min(F(1), uu) - uu * inv(d + 1)
                rem -= eta * ll / (tau * (d + a + 1))
                rem += uu * ll / (tau * (d + 1) * (d + 2))
                assert rem <= bound
                COUNTS["remainder_bounds"] += 1
        for tau, qq, cc, uu_prime in product(
                (F(1, 9), F(1, 2), F(8, 9)),
                (F(0), F(1, 3), F(1)),
                (F(0), F(5, 2)),
                (F(0), F(2, 7), F(1))):
            assert qq * min(F(1), tau * uu_prime) - cc * tau == (
                tau * (qq * min(F(1), uu_prime) - cc))
            COUNTS["scalings"] += 1

    # New claims (6), (7), and (10), independently from their stated proofs.
    for p, ell, a, b in product(range(8), range(8), (0, 1), (0, 1)):
        loss = inv(p + 1) - inv(p + ell + 1)
        profit = share(ell, p + ell + a + b)
        assert loss / 4 <= F(3, 8) * profit
        if p >= 1:
            assert loss <= profit
        COUNTS["relay_payment_bounds"] += 1
    for d, a, b in product(range(15), (0, 1), (0, 1)):
        t_eta = min(inv(d + 1), inv(d + 2) + inv(2 * (d + a + 1)))
        lhs = 1 - t_eta + share(b, 2 * (d + a + b))
        rhs = int(d + a + b > 0) - share(a, 2 * (d + a + b))
        assert lhs <= rhs
        COUNTS["root_envelope_points"] += 1
    for ell in range(3):
        for loads in product(range(3), repeat=2):
            all_loads = (ell,) + loads
            for ss in product((0, 1), repeat=3):
                if any(s and load > ell for s, load in zip(ss, all_loads)):
                    continue
                for rr in product((0, 1), repeat=3):
                    if any(rr[j] and not rr[k] and all_loads[j] < all_loads[k]
                           for j, k in product(range(3), repeat=2)):
                        continue
                    xis = [inv(ell + 1) - inv(load + 1) for load in all_loads]
                    phis = [inv(ell + 2) - inv(load + 2) for load in all_loads]
                    for mu in mus:
                        ee = sum(mm * r for mm, r in zip(mu, rr))
                        covariance = sum(mm * r * xx for mm, r, xx in zip(mu, rr, xis))
                        covariance -= ee * sum(mm * xx for mm, xx in zip(mu, xis))
                        first = sum(mm * s * ((1 - ee) * xx + ee * pp)
                                    for mm, s, xx, pp in zip(mu, ss, xis, phis))
                        assert first <= 0 and covariance >= 0
                        assert first - covariance <= 0
                        COUNTS["zero_defect_menus"] += 1


def real_audit(instance_path, strategy_path):
    data = json.loads((ROOT / instance_path).read_text())
    certificate = json.loads((ROOT / strategy_path).read_text())
    if "strategy" in certificate:
        certificate = certificate["strategy"]
    acts = {tuple(row["history"]): row["action"] for row in certificate["actions"]}
    n, m = data["players"], len(data["topics"])
    customers = [(frozenset(c["topics"]), c["multiplicity"]) for c in data["customers"]]

    def terminal(h):
        while len(h) < n:
            h += (acts[h],)
        return h

    def utility(action, final):
        return sum(w * inv(sum(t in interest for t in final))
                   for interest, w in customers if action in interest)

    # Independently verify all complete-history one-step SPE comparisons.
    for h, action in acts.items():
        own = utility(action, terminal(h))
        for alternative in range(m):
            assert own >= utility(alternative, terminal(h + (alternative,)))
            COUNTS["spe_rows"] += 1

    portfolios = [(F(1),) * m,
                  (F(1, m),) * m,
                  (F(1, 2 * m),) * m]
    portfolios += [tuple(F(int(j == a)) for j in range(m)) for a in range(m)]
    for h in acts:
        if len(h) >= n - 1:
            continue
        outcome = terminal(h)
        aa, bb = outcome[len(h)], outcome[-1]
        v, w = utility(aa, outcome), utility(bb, outcome)
        continuations = [terminal(h + (a,)) for a in range(m)]
        replies = [z[-1] for z in continuations]
        ds = [sum(a in interest for a in h + outcome[len(h) + 1:-1])
              for interest, _ in customers]
        deltas = [[sum(a in interest for a in zz[len(h) + 1:-1])
                   - sum(a in interest for a in outcome[len(h) + 1:-1])
                   for zz in continuations] for interest, _ in customers]

        def menu_pay(topic, other, menu):
            return sum(mult * inv(d + dd[menu] + 1 + int(other in interest))
                       for (interest, mult), d, dd in zip(customers, ds, deltas)
                       if topic in interest)

        def ref_pay(topic, other):
            return sum(mult * inv(d + 1 + int(other in interest))
                       for (interest, mult), d in zip(customers, ds)
                       if topic in interest)

        for zz in portfolios:
            tau = sum(zz)
            mu = tuple(z / tau for z in zz)
            eps, upper = F(0), F(0)
            for (interest, mult), d, dd in zip(customers, ds, deltas):
                xis = [inv(d + 1) - inv(d + delta + 1) for delta in dd]
                zetas = [inv((d + 1) * (d + 2))
                         - inv((d + delta + 1) * (d + delta + 2)) for delta in dd]
                phis = [x - z for x, z in zip(xis, zetas)]
                ee = sum(mu[t] * int(replies[t] in interest) for t in range(m))
                eps += mult * sum(mu[t] * (
                    (int(t in interest) - int(replies[t] in interest) + ee) * xis[t]
                    - ee * int(t in interest) * zetas[t]) for t in range(m))
                upper += mult * gamma(xis, phis)
            assert eps <= upper
            ss = tau * v - sum(zz[t] * menu_pay(t, replies[t], t) for t in range(m))
            zslack = tau * w - sum(zz[t] * ref_pay(replies[t], aa) for t in range(m))
            vv = sum(zz[t] * zz[j] * (menu_pay(replies[t], t, t)
                     - menu_pay(replies[j], t, t)) for t, j in product(range(m), repeat=2))
            assert ss >= 0 and zslack >= 0 and vv >= 0
            defect_delta = sum(mu[t] * mu[j] * ref_pay(t, replies[j])
                               for t, j in product(range(m), repeat=2))
            defect_delta -= sum(mu[t] * menu_pay(t, replies[t], t) for t in range(m))
            assert eps - defect_delta == vv / tau ** 2
            assert defect_delta <= eps
            for eta in (F(0), F(1, 4), F(1), F(3)):
                for qmode in (0, 1, 2):
                    qs = [F(0) if qmode == 0 else F(1) if qmode == 1
                          else F(i % 4, 3) for i in range(len(customers))]
                    cover, envelope = F(0), eta * w
                    for (interest, mult), d, qq in zip(customers, ds, qs):
                        occupancy = sum(zz[t] for t in interest)
                        cover += mult * qq * min(F(1), occupancy)
                        threshold = min(inv(d + 1), inv(d + 2)
                                        + eta * inv(d + 1 + int(aa in interest)))
                        envelope += mult * max(F(0), qq - threshold)
                    if tau >= 1:
                        assert cover - tau * v <= envelope + tau * eps
                        assert cover - tau * v <= envelope + tau * defect_delta
                    # An independently computable upper price v+sum Gamma.
                    assert cover - tau * (v + upper) <= envelope
                    COUNTS["real_inequalities"] += 1
            COUNTS["real_menus"] += 1


if __name__ == "__main__":
    scalar_audit()
    real_audit("examples/customer_attraction/residual_counterexample.json",
               "evidence/certificates/customer_attraction/residual_counterexample.json")
    real_audit("examples/customer_attraction/individual_security_failure.json",
               "evidence/certificates/customer_attraction/individual_security_failure.json")
    print(json.dumps({"status": "passed", "counts": COUNTS,
                      "scope": "finite identity/boundary audit plus two fixed complete SPEs"},
                     indent=2))
