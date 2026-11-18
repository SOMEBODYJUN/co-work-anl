"""Rational dual extraction and exact row reconstruction, one unpaid C mode."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
from scipy.optimize import linprog
from probe_C_four_light_TQ import build,PATTERN,TYPES

ROOT=Path(__file__).resolve().parent
c,A,b,E,d,names=build()
z=linprog(c,A_ub=A,b_ub=b,A_eq=E,b_eq=d,bounds=(0,None),method='highs')
assert z.success
mu=[F(float(v)).limit_denominator(1000000) for v in z.ineqlin.marginals]
nu=[F(float(v)).limit_denominator(1000000) for v in z.eqlin.marginals]
ce,Ae,be,Ee,de,_=build(exact=True)
assert all(v<=0 for v in mu)
rc=[F(ce[k])-sum((mu[i]*F(Ae[i,k]) for i in range(len(mu))),F())-sum((nu[i]*F(Ee[i,k]) for i in range(6)),F()) for k in range(len(ce))]
assert all(v>=0 for v in rc)
bound=sum((mu[i]*F(be[i]) for i in range(len(mu))),F())+sum((nu[i]*F(de[i]) for i in range(6)),F())
assert bound==F(77,144)
cert={'scope':'Only fixed C four-light pair mode and its relabelings. Exact dual of a necessary relaxation, not whole C or full six-person proof.',
      'pattern':[list(p) for p in PATTERN],'bound':str(bound),'client_types':len(TYPES),'columns':len(ce),
      'row_count':len(mu),'inequality_multipliers':[str(v) for v in mu],
      'equality_multipliers':[str(v) for v in nu],'minimum_exact_reduced_cost':str(min(rc)),
      'nonzero_inequality_multipliers':[{'row':i,'name':names[i],'multiplier':str(v)} for i,v in enumerate(mu) if v],
      'generator_sha256':hashlib.sha256((ROOT/'probe_C_four_light_TQ.py').read_bytes()).hexdigest()}
(ROOT/'C-four-light-pair-rational-dual.json').write_text(json.dumps(cert,indent=2)+'\n')
print(json.dumps({k:v for k,v in cert.items() if k not in ('inequality_multipliers',)},indent=2))
