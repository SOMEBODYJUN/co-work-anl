from step_profit_search import *
from math import sqrt

def scan_sqrt(I):
 S=ExactSPESolver(I);S.outcomes()
 @lru_cache(None)
 def F(b):
  r=I.players-sum(b);out=Fraction(0)
  for d in compositions(r,I.topic_count):
   cur=Fraction(0)
   for C in I.customers:
    B=sum(b[a] for a in C.topics);D=sum(d[a] for a in C.topics)
    if D:cur+=C.multiplicity*Fraction(D,B+D)
   out=max(out,cur)
  return out
 best=None
 for b,ends in S._outcomes.items():
  r=I.players-sum(b)
  if r<1:continue
  floor=S.threshold(b)
  for a in range(I.topic_count):
   child=b[:a]+(b[a]+1,)+b[a+1:]
   gap=F(b)-F(child)
   for z in S.outcomes(child):
    u=S._utility(z,a)
    if u<floor:continue
    charge=0
    for C in I.customers:
     if a in C.topics:
      B=sum(b[j] for j in C.topics);Z=sum(z[j] for j in C.topics)
      charge+=2*C.multiplicity*(sqrt(B+1)-sqrt(B))/sqrt(Z)
    deficit=float(gap)-charge
    if best is None or deficit>best[0]:best=(deficit,b,a,z,str(u),str(gap),charge)
 return best

if __name__=='__main__':
 rng=Random(912343)
 for z in range(1000):
  k=rng.choice([3,4,5]);n=rng.choice([3,4,5])
  C=[]
  for mask in range(1,1<<k):
   w=rng.randrange(0,8)
   if w:C.append(CustomerType(frozenset(a for a in range(k) if mask>>a&1),w))
  I=Instance(tuple(map(str,range(k))),tuple(C),n)
  B=scan_sqrt(I)
  if B[0]>1e-8:
   print(z,B,json.dumps(I.to_dict()),flush=True);break
 else:print('no failure in 1000')
