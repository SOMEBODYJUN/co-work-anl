"""Find rational duals, then call the separate solver-free exact verifier."""
from pathlib import Path
import json,time
from fractions import Fraction as F
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
import verify_B_all_orbits as v
BASE=Path(__file__).parent
start=time.perf_counter()
modes=list(combinations_with_replacement(range(12),4))
can=[v.canonical(p) for p in modes];reps=sorted(set(x[0] for x in can))
mapping={'scope':'All four-branch pair multisets, modulo simultaneous S4 extra renaming and new-anchor branch permutation.',
         'pairs':v.PAIRS,'representatives':[list(p) for p in reps],
         'mapping':[{'mode':list(p),'representative':reps.index(k),'extra_permutation':list(pi),'anchor_order':list(order)} for p,(k,pi,order) in zip(modes,can)]}
(BASE/'B-1365-to-69-orbit-map.json').write_text(json.dumps(mapping,separators=(',',':'))+'\n')
certs=[];failures=[];float_results=[]
for pattern in reps:
    A,b,E,names=v.build(pattern)
    objective=np.zeros(v.COLS);objective[-1]=1
    z=linprog(objective,A_ub=np.array(A,dtype=float),b_ub=np.array(b,dtype=float),A_eq=np.array(E,dtype=float),b_eq=np.ones(6),bounds=[(0,None)]*v.COLS,method='highs')
    float_results.append({'mode':list(pattern),'status':int(z.status),'gamma':float(z.fun) if z.success else None})
    if not z.success:
        failures.append({'mode':list(pattern),'reason':'solver status '+str(z.status)});continue
    lam={i:F(float(q)).limit_denominator(10**8) for i,q in enumerate(z.ineqlin.marginals) if abs(q)>1e-10}
    y=[F(float(q)).limit_denominator(10**8) for q in z.eqlin.marginals]
    bound=sum((q*b[i] for i,q in lam.items()),F())+sum(y,F())
    residual=[F(int(c==v.COLS-1))-sum((q*A[i][c] for i,q in lam.items()),F())-sum((q*E[i][c] for i,q in enumerate(y)),F()) for c in range(v.COLS)]
    if bound<F(1,2) or min(residual)<0 or any(q>0 for q in lam.values()):
        failures.append({'mode':list(pattern),'reason':'exact dual not accepted','bound':str(bound),'minimum_reduced_cost':str(min(residual))});continue
    certs.append({'mode':list(pattern),'bound':str(bound),'inequality_dual':[[i,str(q)] for i,q in lam.items()],'equality_dual':[str(q) for q in y]})
result={'scope':'Numerical discovery followed by exact rational acceptance; verifier independently rebuilds all rows and full orbit coverage.','certificates':certs,'failures':failures,'float_results':float_results,'elapsed_seconds':time.perf_counter()-start}
(BASE/'B-all-orbit-rational-certificates.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'orbits':len(reps),'certificates':len(certs),'failures':failures,'elapsed_seconds':result['elapsed_seconds']},indent=2),flush=True)
if not failures:
    replay=v.verify();(BASE/'B-all-orbit-exact-replay.json').write_text(json.dumps(replay,indent=2)+'\n')
    print(json.dumps({k:q for k,q in replay.items() if k!='summaries'},indent=2))
