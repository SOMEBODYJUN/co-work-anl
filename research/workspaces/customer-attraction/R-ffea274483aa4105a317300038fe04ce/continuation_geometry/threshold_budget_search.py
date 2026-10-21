"""Finite attacks on the unproved gate-max budget bridge."""
from fractions import Fraction as F
from pathlib import Path
from customer_attraction import Instance,CustomerType,ExactSPESolver
import json,random,argparse

def budget_min(I):
 S=ExactSPESolver(I);best=None;bestpath=None;number=0
 for path in S.ordered_outcomes():
  k=[0]*I.topic_count;t=[F(0)]*I.topic_count
  for a in path:
   t[a]=max(t[a],S.threshold(tuple(k)));k[a]+=1
  b=sum(x*y for x,y in zip(k,t));number+=1
  assert b<=I.welfare(tuple(k))
  if best is None or b<best:best=b;bestpath=path
 return best,bestpath,number

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--trials',type=int,default=100);ap.add_argument('--topics',type=int,default=7);ap.add_argument('--players',type=int,default=5);ap.add_argument('--seed',type=int,default=188019)
 args=ap.parse_args();rng=random.Random(args.seed);worst=None
 for z in range(args.trials):
  C=[]
  for mask in range(1,1<<args.topics):
   if mask.bit_count()>3:continue
   v=rng.randrange(5) if rng.random()<0.35 else 0
   if v:C.append(CustomerType(frozenset(a for a in range(args.topics) if mask>>a&1),v))
  I=Instance(tuple(map(str,range(args.topics))),tuple(C),args.players)
  b,path,n=budget_min(I);O=I.optimal_welfare();ratio=F(O,1)/b if b else F(1)
  if worst is None or ratio>worst[0]:worst=(ratio,z,b,O,path,n,I.to_dict())
  if 2*b<O:
   print(json.dumps({'status':'candidate bridge false','seed':args.seed,'trial':z,'budget':str(b),'OPT':O,'path':path,'instance':I.to_dict()},indent=2),flush=True);return
 print(json.dumps({'status':'finite no counterexample; not proof','seed':args.seed,'trials':args.trials,'topics':args.topics,'players':args.players,'largest_OPT_over_budget':str(worst[0]),'witness_trial':worst[1],'witness_budget':str(worst[2]),'witness_OPT':worst[3],'witness_path':worst[4],'paths_at_witness':worst[5],'witness_instance':worst[6]},indent=2),flush=True)
if __name__=='__main__':main()
