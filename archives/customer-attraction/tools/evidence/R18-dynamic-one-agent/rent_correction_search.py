from step_profit_search import *
from math import sqrt

def scan_corrected(I):
 S=ExactSPESolver(I);S.outcomes()
 @lru_cache(None)
 def FH(b):
  r=I.players-sum(b)
  out=Fraction(0)
  for d in compositions(r,I.topic_count):
   cur=Fraction(0)
   for C in I.customers:
    B=sum(b[a] for a in C.topics);D=sum(d[a] for a in C.topics)
    if D:cur+=C.multiplicity*Fraction(D,B+D)
   out=max(out,cur)
  h=0
  for C in I.customers:
   B=sum(b[a] for a in C.topics)
   if B+r:
    z=B/(B+r);h+=2*C.multiplicity*(sqrt(z)-z)
  return float(out)+h
 best=None
 for b,ends in S._outcomes.items():
  r=I.players-sum(b)
  if r<1:continue
  floor=S.threshold(b)
  for a in range(I.topic_count):
   child=b[:a]+(b[a]+1,)+b[a+1:]
   u=min((S._utility(z,a) for z in S.outcomes(child) if S._utility(z,a)>=floor),default=None)
   if u is None:continue
   gap=FH(b)-FH(child)-2*float(u)
   if best is None or gap>best[0]:best=(gap,b,a,u,FH(b),FH(child))
 return best

if __name__=='__main__':
 rng=Random(48723)
 for z in range(1000):
  k=rng.choice([3,4,5]);n=rng.choice([3,4,5])
  C=[]
  for mask in range(1,1<<k):
   w=rng.randrange(0,8)
   if w:C.append(CustomerType(frozenset(a for a in range(k) if mask>>a&1),w))
  I=Instance(tuple(map(str,range(k))),tuple(C),n)
  B=scan_corrected(I)
  if B[0]>1e-8:
   print(z,B,json.dumps(I.to_dict()),flush=True);break
 else:print('no failure in 1000')
