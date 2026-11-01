"""Definition-level exact audit of the prefix-compiler bank policies.
This checks a finite list of parameters; general validity rests on the proof.
No imports from the repository SPE implementation.
"""
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import json


def audit(m,j):
 d=m-j
 size=(Q(2),)*j+(Q(d),)+(Q(1),)*(d-1)
 p=len(size); assert p==m
 checks=0; states=0
 def inc(c,a): return c[:a]+(c[a]+1,)+c[a+1:]
 def pay(c,a): return size[a]/c[a] if c[a] else Q(0)
 @lru_cache(None)
 def bi(c):
  if sum(c)==m: return c
  options=[bi(inc(c,a)) for a in range(p)]
  return options[max(range(p),key=lambda a:(pay(options[a],a),-a))]
 def leaf(c): return any(c[j+1:])
 @lru_cache(None)
 def run(mode,F,c):
  nonlocal checks,states
  states+=1
  if sum(c)==m: return c
  if mode=='BI': return bi(c)
  if mode=='H':
   a=j
  elif mode=='Y':
   assert all(x<=1 for x in c[:j]) and not leaf(c) and c[j]<=d
   empty=[a for a in range(j) if not c[a]]
   a=empty[0] if empty else j
  elif mode=='F':
   assert c[F]==1 and all(x<=1 for x in c[:j]) and not leaf(c) and c[j]<=d-1
   empty=[a for a in range(j) if not c[a]]
   a=empty[0] if empty else j if c[j]<d-1 else F
  else: raise AssertionError(mode)
  children=[]
  for b in range(p):
   cc=inc(c,b)
   nextmode=mode
   if sum(cc)<m and mode in ('Y','F'):
    cap=d if mode=='Y' else d-1
    if any(x>1 for x in cc[:j]) or leaf(cc) or cc[j]>cap: nextmode='BI'
   children.append(run(nextmode,F,cc))
  chosen=children[a]
  for b,outcome in enumerate(children):
   checks+=1
   assert pay(chosen,a)>=pay(outcome,b),(m,j,mode,F,c,a,b,chosen,outcome)
  return chosen
 records=[]
 for i in range(1,j+1):
  prefix=tuple(int(a<i-1) for a in range(j))+(0,)*d
  for T in range(p):
   c=inc(prefix,T)
   if T<i-1 or T>j: mode,F='BI',-1
   elif T==j: mode,F='Y',-1
   else: mode,F='F',T
   terminal=run(mode,F,c)
   assert pay(terminal,T)<=1,(m,j,i,T,terminal,pay(terminal,T))
   records.append({'i':i,'action':T,'terminal':terminal,'deviator_payoff':str(pay(terminal,T))})
 c=(1,)*j+(0,)*d
 terminal=run('H',-1,c)
 assert terminal==(1,)*j+(d,)+(0,)*(d-1)
 return {'m':m,'j':j,'d':d,'nodes_checked':states,'all_action_comparisons':checks,'punishments':records}

if __name__=='__main__':
 records=[audit(m,j) for m in range(2,8) for j in range(1,m)]
 result={'scope':'finite implementation audit only, m=2,...,7 and 1<=j<m; no theorem inferred from no failures','parameters':len(records),'nodes_checked':sum(x['nodes_checked'] for x in records),'all_action_comparisons':sum(x['all_action_comparisons'] for x in records),'records':records}
 out=Path(__file__).with_suffix('.json'); out.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='records'}))
