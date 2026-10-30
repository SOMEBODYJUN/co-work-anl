"""New cleaning-only arithmetic regression; the sources contain no executable audit.

Reconstructs a single customer's true menu cost and last-player rows directly.
Does not assume membership patterns are SPE and does not solve for a common Q.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def run():
    identities = clone_identities = 0
    weights = [(F(1, 4), F(1, 4)), (F(0), F(1)),
               (F(1, 2), F(3, 2)), (F(2), F(3))]
    for p, bits, z, eta in product(range(9), product((0, 1), repeat=6),
                                  weights, (F(0), F(1, 2), F(1))):
        a, b, t0, t1, r0, r1 = bits
        ts, rs = (t0, t1), (r0, r1)
        tau = sum(z)
        beta = F(b, p+a+b) if b else F(0)
        cost = sum(z[i] * F(ts[i], p+1+rs[i]) for i in range(2))
        zz = tau*beta-sum(z[i] * F(rs[i], p+1+a) for i in range(2))
        vv = sum(z[i]*z[j]*(F(rs[i], p+1+ts[i])-F(rs[j], p+1+ts[i]))
                 for i in range(2) for j in range(2))
        hh = eta*zz/tau+vv/tau
        d = sum(z[i]*ts[i] for i in range(2))
        ell = sum(z[i]*rs[i] for i in range(2))
        for q in (F(0), F(1), F(2)):
            residual = (q*min(F(1), d)-d/F(p+1)
                        -eta*ell/(tau*(p+a+1))+d*ell/(tau*(p+1)*(p+2)))
            assert q*min(F(1), d)-cost+hh == eta*beta+residual
            identities += 1
            if eta == F(1, 2) and q == 1:
                ll = beta-F(a, p+2)
                assert (min(F(1), d)-cost+hh+ll/2
                        == beta+residual-F(a, 2*(p+2)))
                clone_identities += 1
    common_defect = weak_payments = domination = 0
    for p, a, b in product(range(81), (0, 1), (0, 1)):
        den = (p+1)*(p+2)
        beta = F(b, p+a+b) if b else F(0)
        alpha = F(a, p+a+b) if a else F(0)
        w = F(int(p+a+b > 0))
        g_a = F(a, den)
        fresh_a = F(a if p == 0 else 0)
        base = F(p, p+1)
        assert base+g_a+beta/2+fresh_a/4 <= w
        common_defect += 1
        for truncated in (F(0), F(1)):
            assert w-truncated+truncated/F(p+1) >= beta+g_a
            weak_payments += 1
        e = F(p-1, 2*den) if a and b and p >= 2 else F(0)
        assert alpha-e >= g_a
        domination += 1
    reply_penalties = 0
    for p, a, reply in product(range(81), (0, 1), (0, 1)):
        assert F(reply, (p+1)*(p+2)) <= (
            F(reply, 2*(p+a+1))+F(a if p == 0 else 0, 4))
        reply_penalties += 1
    return {'status': 'passed', 'arithmetic': 'fractions.Fraction',
            'nonuniform_menu_identities': identities,
            'retained_clone_identities': clone_identities,
            'common_Q_defect_customer_cases': common_defect,
            'weak_payment_customer_corners': weak_payments,
            'strong_implies_weak_customer_cases': domination,
            'reply_penalty_customer_cases': reply_penalties,
            'scope': 'new cleaning-only finite algebra regression; not original-source audit, SPE search, Q optimization, or proof of universal parameters'}


if __name__ == '__main__':
    result = run()
    target = Path(__file__).with_name('replay')
    target.mkdir(exist_ok=True)
    (target/'retained-menu-slack-current.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
