"""Independent exact integer audit of the nine-provider tail-selector obstruction.

Imports no canonical model, SPE solver, certificate verifier, NumPy or LP code.
All nonself comparisons use one common exact utility scale. The set-valued
recursion retains every full-history pure SPE continuation, including arbitrary
ties. Count caching stores sets and does not select a Markov strategy.
"""
from functools import lru_cache
from itertools import combinations
from math import lcm
from pathlib import Path
from collections import defaultdict
import argparse,json,time


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
 m=9;k=12;scale=lcm(*range(1,m+1));start=time.monotonic()
 # Each listed mass represents that many separate unit customers.
 types=[]
 for x in range(3):
  for y in range(3,6):types.append(((x,y),10))
 for X in combinations(range(3),2):
  for Y in combinations(range(3,6),2):types.append((X+Y,30))
 for x in range(6,12):types.append(((x,),101))
 assert sum(v for _,v in types)==966
 finals=[];utilities=[];coverages=[];threshold={};visited=0

 def inc(p,a):return p[:a]+(p[a]+1,)+p[a+1:]
 @lru_cache(None)
 def solve(p):
  nonlocal visited
  visited+=1
  if sum(p)==m:
   u=[0]*k;w=0
   for B,mass in types:
    d=sum(p[b]for b in B)
    if d:
     assert scale%d==0
     w+=mass;share=mass*(scale//d)
     for b in B:
      if p[b]:u[b]+=share
   tag=len(finals);finals.append(p);utilities.append(tuple(u));coverages.append(w)
   return frozenset((tag,))
  children=[solve(inc(p,a))for a in range(k)]
  floors=[min(utilities[tag][a]for tag in child)for a,child in enumerate(children)]
  floor=max(floors);threshold[p]=floor
  # A selected action can retain any child SPE giving it at least the best
  # guaranteed value. Other child SPEs can be selected independently per history.
  answer=set()
  for a,child in enumerate(children):
   answer.update(tag for tag in child if utilities[tag][a]>=floor)
  assert answer
  return frozenset(answer)
 zero=(0,)*k;root=solve(zero);minw=min(coverages[tag]for tag in root)
 worst=sorted((tag for tag in root if coverages[tag]==minw),key=lambda tag:finals[tag])
 assert len(root)==20 and len(worst)==18 and minw==946
 assert all(finals[tag][6:]==(1,)*6 for tag in root)
 assert set(coverages[tag]for tag in root)=={946,966}
 # All unit customers are covered by X0,X1,X2 and the six outside leaves.
 chosen={0,1,2,*range(6,12)}
 assert len(chosen)==m and all(chosen.intersection(B)for B,_ in types)
 path_count=0;tails=set();violations=[];spectra=[]
 for tag in worst:
  target=finals[tag];u=utilities[tag]
  layers={zero:1};tail_pairs=set();all_leaves_first=True
  for depth in range(m):
   nxt=defaultdict(int)
   for p,ways in layers.items():
    for a in range(k):
     if p[a]>=target[a]:continue
     child=inc(p,a)
     if tag not in solve(child) or u[a]<threshold[p]:continue
     nxt[child]+=ways
     if a<6 and any(p[x]==0 for x in range(6,12)):all_leaves_first=False
     if depth==m-2:
      for b in range(k):
       if child[b]>=target[b]:continue
       end=inc(child,b)
       if end==target and tag in solve(end) and u[b]>=threshold[child]:tail_pairs.add((a,b))
   layers=nxt
  count=layers[target];path_count+=count
  assert count==1440 and all_leaves_first
  for a,b in tail_pairs:
   assert u[a]==u[b]==120*scale
   tails.add((a,b))
   assert (m-1)*u[b]>minw*scale
   # kappa_9=5/8, hence m-kappa_9=67/8.
   assert 67*u[a]>8*minw*scale
  spectra.append({'terminal_counts':target,'ordered_paths':count,'tails':sorted(tail_pairs)})
 assert path_count==25920
 report={'status':'passed exact independent finite recursion','providers':m,'topics':k,'distinct_unit_customers':966,'payoff_integer_scale':scale,'all_count_states':visited,'terminal_count_states':len(finals),'root_spe_terminal_count_vectors':len(root),'root_welfare_spectrum':[946,966],'worst_spe_terminal_count_vectors':len(worst),'worst_spe_ordered_paths':path_count,'all_worst_paths_outside_leaves_first':True,'all_worst_path_payoffs':[101]*6+[100,120,120],'min_welfare':946,'opt':966,'last_selector_cost':960,'penultimate_selector_cost':1005,'half_margin':926,'root_counts':[finals[tag]for tag in sorted(root,key=lambda tag:finals[tag])],'worst_outcome_path_spectra':spectra,'runtime_seconds':time.monotonic()-start}
 Path(args.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({key:val for key,val in report.items()if key not in ['root_counts','worst_outcome_path_spectra']},indent=2))
if __name__=='__main__':main()
