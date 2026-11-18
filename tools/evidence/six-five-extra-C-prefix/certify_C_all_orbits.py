"""C-specific complete numerical scan, followed only on success by exact duals.
C has five new anchors, one old anchor5, a twice-chosen E and four selected light
branches. This imports no B program or multiplier and creates fresh C outputs.
"""
from pathlib import Path
import json,time
from fractions import Fraction as F
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
import verify_C_all_orbits as v
BASE=Path(__file__).parent
start=time.perf_counter()
modes=list(combinations_with_replacement(range(12),4))
can=[v.canonical(p) for p in modes];reps=sorted(set(x[0] for x in can))
mapping={'scope':'C four selected light branches only: all pair multisets modulo their simultaneous S4 anchor permutations and S4 extra renaming. Fifth new anchor4 and sole old anchor5 remain fixed.',
         'pairs':v.PAIRS,'representatives':[list(p) for p in reps],
         'mapping':[{'mode':list(p),'representative':reps.index(k),'extra_permutation':list(pi),'anchor_order':list(order)} for p,(k,pi,order) in zip(modes,can)]}
(BASE/'C-1365-to-69-orbit-map.json').write_text(json.dumps(mapping,separators=(',',':'))+'\n')
float_results=[];solver_results=[]
for pattern in reps:
    A,b,E,names=v.build(pattern)
    objective=np.zeros(v.COLS);objective[-1]=1
    z=linprog(objective,A_ub=np.array(A,dtype=float),b_ub=np.array(b,dtype=float),A_eq=np.array(E,dtype=float),b_eq=np.ones(6),bounds=[(0,None)]*v.COLS,method='highs')
    r={'mode':list(pattern),'status':int(z.status),'gamma':float(z.fun) if z.success else None}
    if z.success and z.fun<.5-1e-8:
        r['bad_point_atoms']=[{'block':block,'bits':list(bits),'mass':float(q)} for (block,bits),q in zip(v.TYPES,z.x[:-1]) if q>1e-9]
    float_results.append(r);solver_results.append(z)
float_failure=[r for r in float_results if r['status']!=0 or r['gamma'] is None or r['gamma']<.5-1e-8]
scan={'scope':'Full C-specific 69-orbit necessary-model float diagnosis only; not a proof. Fifth new anchor4 is fresh and queried.',
      'orbits':len(reps),'multisets':len(modes),'client_types':223,'rows':189,'float_results':float_results,'failures':float_failure,'elapsed_seconds':time.perf_counter()-start}
(BASE/'C-all-orbit-float-scan.json').write_text(json.dumps(scan,indent=2)+'\n')
print(json.dumps({'phase':'float scan','orbits':len(reps),'failures':len(float_failure),'minimum_gamma':min(r['gamma'] for r in float_results if r['gamma'] is not None)},indent=2),flush=True)
if float_failure:
    raise SystemExit(0)
certs=[];failures=[]
for pattern,z in zip(reps,solver_results):
    A,b,E,names=v.build(pattern)
    lam={i:F(float(q)).limit_denominator(10**8) for i,q in enumerate(z.ineqlin.marginals) if abs(q)>1e-10}
    y=[F(float(q)).limit_denominator(10**8) for q in z.eqlin.marginals]
    bound=sum((q*b[i] for i,q in lam.items()),F())+sum(y,F())
    residual=[F(int(c==v.COLS-1))-sum((q*A[i][c] for i,q in lam.items()),F())-sum((q*E[i][c] for i,q in enumerate(y)),F()) for c in range(v.COLS)]
    if bound<F(1,2) or min(residual)<0 or any(q>0 for q in lam.values()):
        failures.append({'mode':list(pattern),'reason':'exact dual not accepted','bound':str(bound),'minimum_reduced_cost':str(min(residual))});continue
    certs.append({'mode':list(pattern),'bound':str(bound),'inequality_dual':[[i,str(q)] for i,q in lam.items()],'equality_dual':[str(q) for q in y]})
result={'scope':'C-specific numerical discovery then exact rational acceptance; no B multiplier reuse; verifier independently rebuilds C background, light caps, all rows and coverage.',
        'certificates':certs,'failures':failures,'elapsed_seconds':time.perf_counter()-start}
(BASE/'C-all-orbit-rational-certificates.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'phase':'exact dual discovery','certificates':len(certs),'failures':failures},indent=2),flush=True)
if not failures:
    replay=v.verify();(BASE/'C-all-orbit-exact-replay.json').write_text(json.dumps(replay,indent=2)+'\n')
    print(json.dumps({k:q for k,q in replay.items() if k!='summaries'},indent=2))
