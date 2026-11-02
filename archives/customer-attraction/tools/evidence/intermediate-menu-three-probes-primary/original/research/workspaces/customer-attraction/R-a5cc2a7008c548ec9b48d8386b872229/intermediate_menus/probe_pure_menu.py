from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import random,json
ROOT=Path(__file__).resolve().parent

def solve(n,m,weights):
 @lru_cache(None)
 def pay(q,a,insert=False):
  return sum((F(w,sum(q[j] for j in range(n) if mask>>j&1)+int(insert)) for mask,w in weights if mask>>a&1),F(0))
 @lru_cache(None)
 def outcomes(q):
  if sum(q)==m:return frozenset([q])
  children=[];floor=F(0)
  for a in range(n):
   cc=list(q);cc[a]+=1;choices=outcomes(tuple(cc))
   children.append(choices);floor=max(floor,min(pay(z,a) for z in choices))
  return frozenset(z for a,choices in enumerate(children) for z in choices if pay(z,a)>=floor)
 zero=(0,)*n;menus=[]
 for a in range(n):
  q=list(zero);q[a]+=1
  menus.append(sorted((pay(z,a),max(pay(z,t,True) for t in range(n)),z) for z in outcomes(tuple(q))))
 values=sorted({d for cs in menus for d,cap,z in cs})
 for u in values:
  chosen=[]
  for a,cs in enumerate(menus):
   cs=[c for c in cs if c[0]<=u and c[1]>u]
   if not cs:break
   chosen.append(max(cs,key=lambda c:c[1]))
  if len(chosen)==n:return {'u':u,'menu':chosen,'pay':pay,'outcomes':outcomes}
 return None

def main():
 rng=random.Random(2026102303)
 for i in range(1400):
  n=rng.choice([3,4,5]);m=rng.choice([3,4,5,6])
  weights=[(mask,rng.randrange(0,10)) for mask in range(1,1<<n)]
  weights=[(a,b) for a,b in weights if b]
  ans=solve(n,m,weights)
  if ans:
   obj={'index':i,'n':n,'m':m,'weights':weights,'u':str(ans['u']),'menu':[[str(d),str(cap),list(z)] for d,cap,z in ans['menu']]}
   (ROOT/'pure_menu_separation.json').write_text(json.dumps(obj,indent=2))
   print(json.dumps(obj));return
 print('No pure full-outcome menu separation in 1400 samples')
if __name__=='__main__':main()
