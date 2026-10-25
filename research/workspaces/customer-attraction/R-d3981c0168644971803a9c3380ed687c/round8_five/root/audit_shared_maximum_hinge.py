"""Independent exact scalar elimination audit; no author imports."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

knots = sorted({F(d, p+1) for p in range(3) for d in range(6)})
parameters = knots + [F(35, 2)]
checks = 0
zero = 0
for t in parameters:
    lam = (35-2*t)/5
    assert lam >= 0
    for p, d, j, h in product(range(3), range(6), range(6), range(2)):
        den = (p+1)*(p+3)
        cap = F(5*h-j, p+3)
        # Coefficient of v is 40 on both sides, so set it to zero here.
        bns5 = -F(35*h, p+3)-F(d, p+1)+F(2*h*d, den)
        combined = bns5 + lam*cap
        projected = -lam*F(j,p+3)-F(d,p+1)+2*max(F(0),d-t*(p+1))/den
        ell = 2*(d-t*(p+1))/den
        residue = projected-combined
        assert residue == max(F(0),ell)-h*ell >= 0
        checks += 1
        zero += residue == 0
assert max(knots) == 5
report = {"status": "PASS", "scope": "all p,d,j,H coefficient states at all exact knots and t=35/2",
          "knots": list(map(str,knots)), "checks": checks, "zero_residues": zero,
          "tail_slope": "(2/5)*sum_j_weight >= 0",
          "limitation": "Algebra plus legitimate old BNS and one shared maximum; not HALF(5)."}
Path(__file__).with_suffix(".json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report))
