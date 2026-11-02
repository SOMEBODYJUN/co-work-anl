"""Independent definition-level regression; imports no author/solver code.

The symbolic argument is in virtual_replay_independent_review.md. This probe
checks ordered history lifting and local/path inequalities on explicit SPEs.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def run_case(name, customers, m, sigma):
    # customers is an explicit list of interest-label sets, one per unit person.
    topics = (0, 1)
    def old_end(h):
        z = tuple(h)
        while len(z) < m:
            z += (sigma(z),)
        return z
    def pay(z, i):
        return sum((F(1, sum(a in customer for a in z))
                    for customer in customers if z[i] in customer), F(0))
    old_checks = 0
    for d in range(m):
        for h in product(topics, repeat=d):
            z = old_end(h)
            for t in topics:
                assert pay(z, d) >= pay(old_end(h + (t,)), d)
                old_checks += 1
    all_rows = []
    local_checks = 0
    suffix_checks = 0
    for deleted_mask in range((1 << m) - 1):
        L = tuple(i for i in range(m) if deleted_mask >> i & 1)
        J = tuple(i for i in range(m) if not (deleted_mask >> i & 1))
        q, n = len(L), len(J)
        Lset = set(L)
        def lift_prefix(h):
            j = J[len(h)]
            old = ()
            s = 0
            for i in range(j):
                if i in Lset:
                    old += (sigma(old),)
                else:
                    old += (h[s],)
                    s += 1
            assert s == len(h)
            return old
        def tau(h):
            return sigma(lift_prefix(h))
        def new_end(h):
            z = tuple(h)
            while len(z) < n:
                z += (tau(z),)
            return z
        def replay(new_z):
            old = ()
            s = 0
            for i in range(m):
                if i in Lset:
                    old += (sigma(old),)
                else:
                    old += (new_z[s],)
                    s += 1
            assert s == n
            return old
        def local(h):
            d, old_i = len(h), J[len(h)]
            zn = new_end(h)
            zo = replay(zn)
            lifted = lift_prefix(h)
            assert zo == old_end(lifted)
            u, U = pay(zo, old_i), pay(zn, d)
            R = U - u
            assert 0 <= R <= q * u
            gains, branch_refunds = [], []
            K = max(sum(t in c for c in customers) for t in topics)
            for t in topics:
                znt = new_end(h + (t,))
                zot = replay(znt)
                assert zot == old_end(lifted + (t,))
                ut, Ut = pay(zot, old_i), pay(znt, d)
                Rt, gamma = Ut - ut, u - ut
                assert gamma >= 0
                assert Ut - U == Rt - R - gamma
                assert Ut <= (q + 1) * U
                assert Rt <= q * ut
                assert Rt <= F(q, q + 1) * K
                gains.append(Ut - U)
                branch_refunds.append(Rt)
            rho = max(F(0), *gains)
            assert rho <= q * u - R
            assert rho <= max(F(0), max(branch_refunds) - R)
            return rho, q * u - R, u, R, zo
        for d in range(n):
            for h in product(topics, repeat=d):
                rho, cap, _, _, zo = local(h)
                local_checks += len(topics)
                walk, rr, bb = h, F(0), F(0)
                while len(walk) < n:
                    ri, bi, _, _, zi = local(walk)
                    assert zi == zo
                    rr += ri
                    bb += bi
                    walk += (tau(walk),)
                assert rr <= bb
                suffix_checks += 1
        zn = new_end(())
        zo = replay(zn)
        PJ = sum((pay(zo, i) for i in J), F(0))
        PL = sum((pay(zo, i) for i in L), F(0))
        W = sum(any(a in c for a in zo) for c in customers)
        e = sum(not any(zo[i] in c for i in J) and any(zo[i] in c for i in L)
                for c in customers)
        refund = sum((pay(zn, d) - pay(zo, i) for d, i in enumerate(J)), F(0))
        assert refund == PL - e
        total_rho = sum((local(zn[:d])[0] for d in range(n)), F(0))
        assert total_rho <= q * PJ - PL + e == q * W - (q + 1) * PL + e
        K = max(sum(t in c for c in customers) for t in topics)
        if q:
            assert PL >= F(q * K, m)
            spectrum = F(0)
            for d, old_i in enumerate(J):
                rho, _, u, R, _ = local(zn[:d])
                three_cap = min(q * u, F(q * K, q + 1), F(m, q + 1) * PL) - R
                assert three_cap >= 0
                assert rho <= three_cap
                spectrum += three_cap + R
            assert total_rho <= spectrum - PL + e
        all_rows.append({"L": L, "path": zn, "regret_sum": str(total_rho),
                         "bound8": str(q * W - (q + 1) * PL + e)})
    return {"name": name, "m": m, "unit_customers": len(customers),
            "old_ic_checks": old_checks, "new_ic_checks": local_checks,
            "prescribed_suffix_checks": suffix_checks, "deletions": all_rows}


def main():
    # Genuine order dependence: AB and BA have equal counts but different replies.
    def history_ties(h):
        if not h:
            return 0
        if len(h) == 1:
            return 1 - h[0]
        return {(0, 0): 1, (0, 1): 0, (1, 0): 1, (1, 1): 0}[h]
    results = [run_case("ordered_history_ties", [{0}, {1}], 3, history_ties)]
    for q in range(1, 6):
        m = q + 1
        def sharp_sigma(h):
            return 0 if not h else 1
        result = run_case(f"sharp_q_{q}", [{0}] + [{1} for _ in range(m)], m, sharp_sigma)
        tail_deleted = next(row for row in result["deletions"] if row["L"] == tuple(range(1, m)))
        assert tail_deleted["regret_sum"] == str(q)
        result["sharp_ratio"] = str(q + 1)
        results.append(result)
    target = Path(__file__).with_name("virtual_replay_independent_exact.json")
    target.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"cases": len(results), "old_ic_checks": sum(r["old_ic_checks"] for r in results),
                      "new_ic_checks": sum(r["new_ic_checks"] for r in results),
                      "prescribed_suffix_checks": sum(r["prescribed_suffix_checks"] for r in results),
                      "deletion_sets": sum(len(r["deletions"]) for r in results),
                      "output": str(target)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
