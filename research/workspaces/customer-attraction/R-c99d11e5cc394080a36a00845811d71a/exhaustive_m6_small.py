from customer_attraction import CustomerType, ExactSPESolver, Instance
from fractions import Fraction
from itertools import combinations, product
import json,time

def run(p,players=6,max_mult=2):
 sig=[frozenset(c) for sz in range(1,p+1) for c in combinations(range(p),sz)]
 best=None; count=0; t=time.time()
 for w in product(range(max_mult+1),repeat=len(sig)):
  if not any(w):continue
  ins=Instance(tuple(f'T{i}' for i in range(p)),tuple(CustomerType(s,n) for s,n in zip(sig,w) if n),players)
  sol=ExactSPESolver(ins); rr=sol.inefficiency_ratio(); W=sol.minimum_welfare(); O=ins.optimal_welfare(); count+=1
  row={'weights':list(w),'W':W,'OPT':O,'ratio':str(rr),'outcomes':len(sol.outcomes())}
  if best is None or rr>Fraction(best['ratio']): best=row
 return {'players':players,'topics':p,'max_multiplicity':max_mult,'instances':count,'best':best,'elapsed_seconds':time.time()-t,'status':'finite_exact_screen_only'}
if __name__=='__main__':
 out=[run(2),run(3)]; open('exhaustive_m6_small_report.json','w').write(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
