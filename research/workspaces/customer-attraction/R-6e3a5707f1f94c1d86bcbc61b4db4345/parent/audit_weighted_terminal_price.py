"""Deterministic Fraction audit of the parametric two-tail identity/corners.

This is finite arithmetic regression; the unbounded theorem is in the note.
No SPE solver or numerical optimization is used.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def share(bit, denominator):
    return F(bit, denominator) if bit else F(0)


def run():
    identity_count = 0
    corner_count = 0
    eta_values = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1), F(2)]
    q_values = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
    z_values = [(F(1, 2), F(1, 2)), (F(1), F(1)),
                (F(1, 2), F(3, 2)), (F(0), F(3))]
    for p, bits, z, eta in product(range(9), product((0, 1), repeat=6),
                                    z_values, eta_values):
        a, b, t0, t1, r0, r1 = bits
        ts, rs = (t0, t1), (r0, r1)
        tau = sum(z)
        d = sum(zi * ti for zi, ti in zip(z, ts))
        ell = sum(zi * ri for zi, ri in zip(z, rs))
        alpha, beta = share(a, p+a+b), share(b, p+a+b)
        s = tau*alpha - sum(zi*share(ti, p+1+ri)
                            for zi, ti, ri in zip(z, ts, rs))
        zz = tau*beta - sum(zi*share(ri, p+1+a)
                            for zi, ri in zip(z, rs))
        v = sum(z[i]*z[j]*(share(rs[i], p+1+ts[i])
                            - share(rs[j], p+1+ts[i]))
                for i in range(2) for j in range(2))
        raw = s+eta*zz/tau+v/tau
        expanded = (tau*alpha+eta*beta-d/F(p+1)
                    - eta*ell/(tau*(p+a+1))
                    + d*ell/(tau*(p+1)*(p+2)))
        assert raw == expanded, (p, bits, z, eta)
        for q in q_values:
            residual = (q*min(1,d)-d/F(p+1)
                        -eta*ell/(tau*(p+a+1))
                        +d*ell/(tau*(p+1)*(p+2)))
            assert q*min(1,d)-tau*alpha == eta*beta+residual-raw
        identity_count += 1
    for p, a, tau, eta, q in product(range(31), (0, 1),
            [F(1), F(3,2), F(2), F(4), F(10)], eta_values, q_values):
        threshold = min(F(1,p+1), F(1,p+2)+eta/F(p+a+1))
        expected = max(F(0),q-threshold)
        corners=[]
        for d,ell in product((F(0),F(1),tau),(F(0),tau)):
            value=(q*min(1,d)-d/F(p+1)-eta*ell/(tau*(p+a+1))
                   +d*ell/(tau*(p+1)*(p+2)))
            corners.append(value)
        assert max(corners)==expected,(p,a,tau,eta,q,corners,expected)
        corner_count+=1
    return {'status':'passed','arithmetic':'fractions.Fraction',
        'identity_cases':identity_count,'corner_cases':corner_count,
        'p_identity_range':[0,8],'p_corner_range':[0,30],
        'eta_values':list(map(str,eta_values)),
        'q_values':list(map(str,q_values)),
        'scope':'finite regression of exact identities and analytical corner reduction; not a general SPE search or proof'}


if __name__=='__main__':
    report=run()
    path=Path(__file__).with_name('weighted_terminal_price_audit.json')
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
