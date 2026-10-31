from pathlib import Path
import sys,json,random,time,math
from itertools import product,combinations
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as F
D=Path(__file__).resolve().parent;ROOT=D.parents[4]
sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone,payoff_row,coverage_row,dot,serializable,integer_clones

def gen(p,n,w,rng,prefer0=False):
 L=math.lcm(*range(1,n+1));masks=np.arange(1,1<<p);inc=np.array([[int(mask>>a&1) for mask in masks] for a in range(p)],dtype=int)
 @lru_cache(None)
 def u(q):
  loads=np.array(q)@inc
  shares=np.array([L//d if d else 0 for d in loads])*w
  return tuple(int(v) for v in inc@shares)
 term={};actions={}
 for depth in range(n,-1,-1):
  for h in product(range(p),repeat=depth):
   if depth==n:term[h]=tuple(h.count(a) for a in range(p));continue
   vals=[u(term[h+(a,)])[a] for a in range(p)];best=max(vals);cands=[a for a in range(p) if vals[a]==best]
   a=0 if prefer0 and 0 in cands else rng.choice(cands);actions[h]=a;term[h]=term[h+(a,)]
 return StrategyCone(p,n,actions)

def optimize(c,a,J):
 norm=payoff_row(c.topics,c.root,a);o=coverage_row(c.topics,J)
 res=linprog(-np.array(o,dtype=float),A_ub=-c.matrix,b_ub=np.zeros(len(c.rows)),A_eq=np.array([norm],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
 if not res.success:return None
 return res,norm,o

if __name__=='__main__':
 p=int(sys.argv[1]) if len(sys.argv)>1 else 5;n=int(sys.argv[2]) if len(sys.argv)>2 else 4;iters=int(sys.argv[3]) if len(sys.argv)>3 else 100
 rng=random.Random(437);
 w=np.zeros((1<<p)-1,dtype=int);w[0]=n
 for a in range(1,p):w[(1<<a)-1]=1
 best=0;start=time.time()
 for t in range(iters):
  c=gen(p,n,w,rng,prefer0=(t==0));support=tuple(a for a,x in enumerate(c.root) if x)
  # Normalize an occupied theme and check every maximal portfolio if modest.
  Js=list(combinations(range(p),min(p,n)))
  rng.shuffle(Js)
  for a in support:
   for J in Js:
    r=optimize(c,a,J)
    if r is None:continue
    res,norm,o=r;val=-res.fun
    if val>best+1e-7:
     best=val;ww=tuple(F(float(x)).limit_denominator(10**8) for x in res.x);ok=c.verify(ww) and dot(norm,ww)==1
     record={'n':n,'p':p,'iteration':t,'root_counts':c.root,'a':a,'J':J,'float_ratio':val,'exact':ok,'ratio':str(dot(o,ww)),'seconds':time.time()-start}
     print(json.dumps(record),flush=True)
     record.update({'weights':list(map(str,ww)),'actions':[{'h':h,'a':b} for h,b in c.actions.items()]})
     (D/f'individual_search_p{p}_n{n}_best.json').write_text(json.dumps(record))
     if ok and dot(o,ww)>2*n-1:
      print('COUNTEREXAMPLE',flush=True);sys.exit()
  if t%10==0:print('done',t,'elapsed',time.time()-start,flush=True)
