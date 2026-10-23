from fractions import Fraction as F
from functools import lru_cache
import random,json,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def solve(n,m,weights,seed):
 rng=random.Random(seed)
 masks=[mask for mask,w in weights]
 @lru_cache(None)
 def pay(q,a,insert=False):
  return sum((F(w, sum(q[j] for j in range(n) if mask>>j&1)+int(insert)) for mask,w in weights if mask>>a&1),F(0))
 policy={}
 @lru_cache(None)
 def terminal(q):
  if sum(q)==m:return q
  children=[]
  for a in range(n):
   z=list(q);z[a]+=1;z=terminal(tuple(z))
   children.append((pay(z,a),a,z))
  best=max(x[0] for x in children)
  chosen=rng.choice([x for x in children if x[0]==best])
  policy[q]=chosen[1]
  return chosen[2]
 zero=(0,)*n;actual=terminal(zero)
 menu=[]
 for a in range(n):
  q=list(zero);q[a]+=1
  z=terminal(tuple(q))
  h=[a];c=tuple(q)
  while sum(c)<m:
   b=policy[c];h.append(b);cc=list(c);cc[b]+=1;c=tuple(cc)
  menu.append((h,z,pay(z,a),pay(z,h[-1]),[pay(z,t,True) for t in range(n)]))
 return max(x[2] for x in menu),menu,policy,pay

def main():
 rng=random.Random(2026102301)
 for index in range(1200):
  n=rng.choice([3,4,5,6]);m=rng.choice([3,4,5,6,7])
  weights=[(mask,rng.randrange(0,10)) for mask in range(1,1<<n)]
  weights=[(a,b) for a,b in weights if b]
  u,menu,policy,pay=solve(n,m,weights,index)
  last=min(x[3] for x in menu)
  if last>u:
   result={'index':index,'n':n,'m':m,'weights':weights,'u':str(u),'min_last':str(last),'menu':[{'history':h,'z':z,'root':str(d),'last':str(w),'insertion':[str(x) for x in k]} for h,z,d,w,k in menu],'policy':[[q,a] for q,a in sorted(policy.items())]}
   (ROOT/'last_dominance_counterexample.json').write_text(json.dumps(result,indent=2))
   print(json.dumps({k:result[k] for k in ['index','n','m','weights','u','min_last','menu']}))
   return
 print('No last-dominance separation in 1200 samples')
if __name__=='__main__':main()
