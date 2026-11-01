from fractions import Fraction as F
from itertools import product
import random,json
random.seed(492)

def check(k,types):
 def u(a,counts):
  return sum((F(w,sum(counts[j] for j in range(k) if mask>>j&1)) for mask,w in types.items() if mask>>a&1),F(0))
 for A in range(k):
  payoff={}
  for B,C in product(range(k),repeat=2):
   cnt=[0]*k
   for x in A,B,C:cnt[x]+=1
   payoff[B,C]=[u(x,cnt) for x in (A,B,C)]
  br={B:[C for C in range(k) if payoff[B,C][2]==max(payoff[B,D][2] for D in range(k))] for B in range(k)}
  pnes=[(B,C) for B,C in product(range(k),repeat=2) if C in br[B] and payoff[B,C][1]==max(payoff[D,C][1] for D in range(k))]
  if not pnes:raise RuntimeError('no PNE')
  minpn=min(payoff[B,C][0] for B,C in pnes)
  threshold=max(min(payoff[B,C][1] for C in br[B]) for B in range(k))
  spes=[(B,C) for B in range(k) for C in br[B] if payoff[B,C][1]>=threshold]
  for B,C in spes:
   if payoff[B,C][0]<minpn:
    return {'k':k,'types':types,'root':A,'tail_spe':[B,C], 'spe_root_payoff':str(payoff[B,C][0]),'min_pne_root_payoff':str(minpn),'tail_pnes':pnes,'last_br':br,'first_tail_threshold':str(threshold)}
for it in range(20000):
 k=random.randrange(3,7)
 types={mask:random.randrange(1,8) for mask in range(1,1<<k) if random.random()<.22}
 if not types:continue
 ans=check(k,types)
 if ans:
  print(json.dumps({'iteration':it,**ans},ensure_ascii=False,indent=2));break
else:print('No counterexample found; not a proof')
