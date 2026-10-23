"""Attack D<=W using fully specified two-player reply policies, not samples of paths."""
import sys,json,random,time,itertools
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import CustomerType,Instance,ExactSPESolver,verify_certificate
q=6;groups=[{0,1},{2,3}];banks={4,5}
types=[frozenset(g) for g in groups]+[frozenset(t for t in range(q) if mask>>t&1) for mask in range(1,1<<q) if mask&48]
N=len(types)
def gain(x,y):
 return np.array([float(Fraction(int(x in B),1+int(y in B))) for B in types])
gains=[[gain(x,y) for y in range(q)] for x in range(q)]
objective=np.array([-1.,-1.]+[0.]*(N-2));normal=np.array([0.,0.]+[1.]*(N-2))
rng=random.Random(983220);best=0;witness=None;t0=time.time();done=0
# Both variants and banks may have arbitrary, separately specified offpath ties.
for reply0 in itertools.product(range(q),repeat=q-1):
 reply=reply0[:4]+(5,reply0[4])
 rows=[]
 for x in range(q):
  for y in range(q):rows.append(gains[y][x]-gains[reply[x]][x])
 for x in range(q):rows.append(gains[x][reply[x]]-gains[4][5])
 result=linprog(objective,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),A_eq=normal[None,:],b_eq=[1],bounds=(0,None),method='highs')
 done+=1
 if not result.success:continue
 val=-result.fun
 if val>best+1e-8:
  best=val;print('BEST',best,'REPLY',reply,flush=True)
 if val>1+1e-8:
  xs=[Fraction(float(x)).limit_denominator(1000000) for x in result.x]
  from math import lcm
  den=lcm(*(x.denominator for x in xs));weights=[int(x*den) for x in xs]
  customers=[CustomerType(B,w) for B,w in zip(types,weights) if w]
  inst=Instance(tuple(map(str,range(q))),tuple(customers),2)
  cert=ExactSPESolver(inst).certificate(on_path=(4,5));verify_certificate(inst,cert).assert_valid()
  witness={'reply':reply,'D':sum(weights[:2]),'W':sum(weights[2:]),'types':[{'topics':sorted(B),'multiplicity':w} for B,w in zip(types,weights) if w],'certificate':cert.to_dict()}
  break
out={'candidate':'D<=W for pair-disjoint nonempty maximal D projections','q':q,'m':2,'all_reply_policies_tested':done,'total_reply_policies':q**(q-1),'best_lp_D_over_W':best,'witness':witness,'elapsed_seconds':time.time()-t0}
Path(__file__).with_name('separable_cones_audit.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='witness'},indent=2))
