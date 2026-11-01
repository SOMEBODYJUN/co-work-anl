from functools import lru_cache
from fractions import Fraction
from itertools import product

def possible(vals,m=6):
 k=len(vals)
 @lru_cache(None)
 def rec(h):
  i=len(h)
  if i==m:return {h}
  child={a:rec(h+(a,)) for a in range(k)}
  mins=[min(Fraction(vals[a],seq.count(a)) if seq.count(a) else 0 for seq in child[a]) for a in range(k)]
  threshold=max(mins)
  out=set()
  for a in range(k):
   for seq in child[a]:
    pay=Fraction(vals[a],seq.count(a))
    if pay>=threshold:out.add(seq)
  return out
 return rec(())

if __name__=='__main__':
 import sys
 best=(Fraction(999),None)
 for k in [3,4,5,6,7]:
  for vals in product(range(1,9), repeat=k):
   if vals!=tuple(sorted(vals)):continue
   s=possible(vals)
   opt=sum(sorted(vals,reverse=True)[:min(6,k)])
   rat=min(Fraction(sum(vals[a] for a in set(seq)),opt) for seq in s)
   if rat<best[0]:
    seq=min(s,key=lambda q: Fraction(sum(vals[a] for a in set(q)),opt));best=(rat,(vals,seq,len(s),opt));print('BEST',rat,best[1],flush=True)
   if rat<Fraction(1,2):
    print('COUNTER',vals,rat,seq,'opt',opt,'S',len(s));sys.exit()
  print('done k',k,'best',best,flush=True)
