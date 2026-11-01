"""Finite exact audits of the background interface; general proofs are in md."""
from fractions import Fraction as F
import json
from pathlib import Path

checks = dict(profit=0, drift=0, chord=0)
for r in range(2, 14):
    for B in range(10):
        C = max(F(d*(r-d), B+d) for d in range(1,r+1))
        c = C/(r-1)
        for b in range(B,B+4):
            for d in range(1,r+1):
                for j in range(11):
                    L = F(j*(r-1),10)
                    gap = (d+c*L)/(b+1+L)-F(d,b+d)
                    assert gap >= 0
                    assert gap == (d*(d-1)+L*(c*(b+d)-d))/((b+d)*(b+1+L))
                    raw = (d+L)/(b+1+L)-F(d,b+d)
                    assert raw == F(d*(d-1)+b*L,1)/((b+d)*(b+1+L))
                    checks['profit'] += 1
        assert C == max(F(d*(r-d), B+d) for d in range(1,r+1))

for r in range(2, 14):
    for b in range(10):
        for alpha in [F(j,10) for j in range(11)]:
            for rho in [F(j,7) for j in range(8)]:
                d = b+1+(r-1)*alpha
                for z in (0,1):
                    dn = b+z+1+(r-2)*alpha
                    drift = rho/d-rho/dn
                    assert drift == rho*(z-alpha)/(d*dn)
                    tax = F(z,(b+1)*(b+2))
                    assert drift <= tax
                    oldJ = rho*(r-1)**2*alpha*(1-alpha)/((b+1)*(b+r)*d)
                    newJ = rho*(r-2)**2*alpha*(1-alpha)/((b+z+1)*(b+z+r-1)*dn)
                    assert oldJ >= newJ
                    if z:
                        Jrelease = rho*(1-alpha)*(F(1,(b+1)*(b+2))-1/(d*dn))
                    else:
                        Jrelease = rho*alpha*(1/(d*dn)-F(1,(b+r-1)*(b+r)))
                    assert oldJ-newJ == Jrelease
                    checks['drift'] += 1
                K = (rho+alpha-rho*alpha)/(b+1)+rho*alpha/(b+r)
                J = rho*(r-1)**2*alpha*(1-alpha)/((b+1)*(b+r)*d)
                assert J >= 0
                assert K == rho/d + alpha/(b+1) + J
                checks['chord'] += 1

out = dict(status='FINITE_EXACT_AUDIT_PASSED', checks=checks,
           scope='The general claims rest on the algebraic proofs, not this finite grid.')
print(json.dumps(out,indent=2))
(Path(__file__).resolve().parent/'background_interface_audit.json').write_text(json.dumps(out,indent=2)+'\n')
