"""Exact local algebra audit; no SPE or universal welfare search is performed."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random


def U(bg, x, y):
    return F(x, bg + 1 + y)


def check_identity(p, loads, ss, rr, z, eta):
    tau = sum(z, F())
    base = p + loads[0]
    a, b = ss[0], rr[0]
    v, w = U(base, a, b), U(base, b, a)
    S = tau*v - sum((zt*U(p+lt, s, r)
                     for zt, lt, s, r in zip(z, loads, ss, rr)), F())
    S0 = tau*v - sum((zt*U(base, s, r)
                      for zt, s, r in zip(z, ss, rr)), F())
    Z = tau*w - sum((zt*U(base, r, a) for zt, r in zip(z, rr)), F())
    V = sum((zt*zq*(U(p+lt, rt, st)-U(p+lt, rq, st))
             for zt, lt, st, rt in zip(z, loads, ss, rr)
             for zq, rq in zip(z, rr)), F())
    V0 = sum((zt*zq*(U(base, rt, st)-U(base, rq, st))
              for zt, st, rt in zip(z, ss, rr)
              for zq, rq in zip(z, rr)), F())
    G, G0 = S+eta*Z/tau+V/tau, S0+eta*Z/tau+V0/tau
    xi = [F(1, base+1)-F(1, p+lt+1) for lt in loads]
    ze = [F(1, (base+1)*(base+2))-F(1, (p+lt+1)*(p+lt+2))
          for lt in loads]
    mu = [t/tau for t in z]
    ell = sum((t*r for t, r in zip(mu, rr)), F())
    eps = sum((t*s*x-t*r*x+ell*t*x-ell*t*s*y
               for t, s, r, x, y in zip(mu, ss, rr, xi, ze)), F())
    assert G0 == G-tau*eps
    reference_decoupled = sum((mt*mq*U(base, st, rq)
                               for mt, st in zip(mu, ss)
                               for mq, rq in zip(mu, rr)), F())
    true_diagonal = sum((mt*U(p+lt, st, rt)
                         for mt, lt, st, rt in zip(mu, loads, ss, rr)), F())
    delta = reference_decoupled-true_diagonal
    assert delta == eps-V/tau**2
    assert G0 == S+eta*Z/tau-tau*delta
    d = sum((t*s for t, s in zip(z, ss)), F())
    L = sum((t*r for t, r in zip(z, rr)), F())
    H = sum((t*s*r for t, s, r in zip(z, ss, rr)), F())
    den = (base+1)*(base+2)
    assert S0 == tau*v-d/F(base+1)+H/F(den)
    assert V0 == (d*L-tau*H)/den
    for q in (F(), F(1, 3), F(1)):
        rem = q*min(F(1), d)-d/F(base+1)-eta*L/(tau*(base+a+1))+d*L/(tau*den)
        assert q*min(F(1), d)-tau*v == eta*w+rem-G0
    # This is only a range envelope, independent of whether these rows are SPE.
    pos, neg = max(xi), min(xi)
    phi = max(x-y for x, y in zip(xi, ze))
    assert pos >= 0 >= neg and 0 <= phi <= pos
    aa, bb = pos, phi-neg
    gamma = aa if bb <= aa else (aa+bb)**2/(4*bb)
    assert eps <= gamma <= pos-neg/4
    no_selected_crowding = all(not s or lt <= loads[0] for s, lt in zip(ss, loads))
    reply_load_order = all(not (rt and not rq) or lt >= lq
                           for rt, lt in zip(rr, loads) for rq, lq in zip(rr, loads))
    if no_selected_crowding and reply_load_order:
        assert eps <= 0


def check_corners(bg, a, eta, tau, q):
    den = (bg+1)*(bg+2)
    def rem(u, ell):
        return q*min(F(1), u)-u/F(bg+1)-eta*ell/(tau*(bg+a+1))+u*ell/(tau*den)
    target = max(F(), q-F(1, bg+1), q-F(1, bg+2)-eta/F(bg+a+1))
    assert max(rem(u, ell) for u, ell in product((F(), F(1), tau), (F(), tau))) == target
    for i, j in product(range(9), repeat=2):
        assert rem(tau*i/8, tau*j/8) <= target


def check_range_sharp(bg, lo, hi):
    # Relaxed local patterns, explicitly not asserted to form an equilibrium.
    xplus = F(1, bg+1)-F(1, hi+1)
    xminus = F(1, bg+1)-F(1, lo+1)
    phiplus = F(1, bg+2)-F(1, hi+2)
    aa, bb = xplus, phiplus-xminus
    gamma = aa if bb <= aa else (aa+bb)**2/(4*bb)
    ee = F() if bb <= aa else (bb-aa)/(2*bb)
    # r=0,s=1 at high load; r=1,s=0 at low load.
    value = (1-ee)*(aa+ee*phiplus)+ee*(1-ee)*(-xminus)
    assert value == gamma


def main():
    rng = random.Random(202610215)
    identity_count = 0
    for p, l0, l1 in product(range(4), repeat=3):
        for ss, rr in product(product((0, 1), repeat=2), repeat=2):
            for z in ((F(1), F(1)), (F(2, 3), F(1, 3)), (F(1, 5), F(2, 5))):
                for eta in (F(), F(1, 2), F(1), F(7, 3)):
                    check_identity(p, [l0, l1], ss, rr, z, eta)
                    identity_count += 1
    for _ in range(2000):
        n = rng.randrange(3, 8)
        check_identity(rng.randrange(10), [rng.randrange(9) for _ in range(n)],
                       [rng.randrange(2) for _ in range(n)],
                       [rng.randrange(2) for _ in range(n)],
                       [F(rng.randrange(1, 20), rng.randrange(1, 20)) for _ in range(n)],
                       F(rng.randrange(10), rng.randrange(1, 10)))
        identity_count += 1
    corner_count = 0
    for bg, a, eta, tau, q in product((0, 1, 2, 7, 101, 10**6), (0, 1),
                                      (F(), F(1, 5), F(1, 2), F(1), F(17, 3)),
                                      (F(1), F(7, 3), F(10)),
                                      (F(), F(1, 3), F(1))):
        check_corners(bg, a, eta, tau, q)
        corner_count += 1
    range_count = 0
    for bg in range(9):
        for lo in range(bg+1):
            for hi in range(bg, 12):
                check_range_sharp(bg, lo, hi)
                range_count += 1
    rent_count = 0
    for p, ll, a, b in product(range(8), range(1, 12), range(2), range(2)):
        assert F(ll, (p+1)*(p+ll+1)) <= F(3, 2)*F(ll, p+ll+a+b)
        rent_count += 1
    residue_count = 0
    for dd, a, b in product(range(20), range(2), range(2)):
        denom = dd+a+b
        vv = F(a, denom) if a else F()
        ww = F(b, denom) if b else F()
        threshold = min(F(1, dd+1), F(1, dd+2)+F(1, 2*(dd+a+1)))
        assert ww/2+1-threshold <= F(denom > 0)-vv/2
        residue_count += 1
    report = {
        "status": "all exact local algebra checks passed",
        "scope": "finite implementation audit, no SPE claim and no general welfare proof",
        "identity_and_envelope_cases": identity_count,
        "parametric_corner_cases": corner_count,
        "relaxed_range_sharpness_cases": range_count,
        "unloading_actual_rent_cases": rent_count,
        "global_actual_residue_cases": residue_count,
        "seed": 202610215,
    }
    out = Path(__file__).with_name('early_menu_load_defect_audit.json')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
