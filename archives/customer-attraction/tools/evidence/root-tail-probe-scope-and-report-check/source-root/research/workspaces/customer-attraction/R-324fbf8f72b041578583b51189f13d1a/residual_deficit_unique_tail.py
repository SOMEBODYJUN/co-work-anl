"""Attack the minimum-welfare tail selector via strictly unique full SPE.

Only a positive exact, integerized complete-policy witness is a refutation.
"""
import argparse,itertools,json,math,random,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=4);ap.add_argument('--topics',type=int,default=5);ap.add_argument('--trials',type=int,default=300);ap.add_argument('--seed',type=int,default=324444);ap.add_argument('--output',required=True);a=ap.parse_args()
 m=a.players;k=a.topics;rng=random.Random(a.seed);mask=list(range(1,1<<k));n=len(mask);mem=np.array([[(b>>t)&1 for b in mask] for t in range(k)],dtype=int);L=math.lcm(*range(1,m+1));cache={};best=F(-100);records=[]
 def coeff(h,t):
  q=tuple(h.count(i) for i in range(k));key=(q,t)
  if key not in cache:
   den=np.array(q)@mem;cache[key]=np.array([L//int(d) if v else 0 for d,v in zip(den,mem[t])],dtype=int)
  return cache[key]
 for z in range(a.trials):
  mass=np.array([rng.choice([0,0,0,0,1,1,2,10])*rng.randint(10001,100003) for _ in mask],dtype=int)
  if not mass.sum():continue
  pol={};ends={h:h for h in itertools.product(range(k),repeat=m)};rows=[];strict=True
  for d in range(m-1,-1,-1):
   for h in itertools.product(range(k),repeat=d):
    branches=[ends[h+(t,)] for t in range(k)];values=[int(coeff(p,t)@mass) for t,p in enumerate(branches)];mx=max(values);chosen=values.index(mx);pol[h]=chosen;ends[h]=branches[chosen];base=coeff(ends[h],chosen)
    for t in range(k):
     if t!=chosen:
      row=base-coeff(branches[t],t);rows.append(row)
      if row@mass<=0:strict=False
  if not strict:continue
  rows=np.array(rows,dtype=int);path=ends[()];w=(mem[list(path)].sum(axis=0)>0).astype(int);target=(m-1)*coeff(path,path[-1])-L*w
  res=linprog(-target.astype(float),A_ub=-rows.astype(float),b_ub=np.zeros(len(rows)),A_eq=np.ones((1,n)),b_eq=[1],bounds=(0,None),method='highs')
  if not res.success:continue
  value=-res.fun/L
  if value>float(best)+1e-10:best=F(float(value)).limit_denominator(10**6);records.append({'trial':z,'best_float_gap_per_total_mass':value,'path':path,'unique_at_seed':True});print(records[-1],flush=True)
  if value>1e-7:
   cand=[F(float(v)).limit_denominator(10**7) for v in res.x];seed=[F(int(v),int(mass.sum())) for v in mass]
   # Mix rational candidate toward the strictly feasible seed to overcome rounding.
   for e in [F(1,10**j) for j in range(1,9)]:
    point=[(1-e)*x+e*y for x,y in zip(cand,seed)]
    slacks=[sum(F(int(v))*x for v,x in zip(r,point)) for r in rows]
    gap=sum(F(int(v))*x for v,x in zip(target,point))
    if min(slacks)>0 and gap>0:
     den=math.lcm(*(x.denominator for x in point));weights=[int(x*den) for x in point];g=math.gcd(*weights);weights=[x//g for x in weights]
     report={'status':'exact complete strictly unique SPE counterexample to last threshold selection','parameters':vars(a),'unit_clients':sum(weights),'path':path,'strict_min_scaled_comparison':str(min(slacks)),'gap_scaled':str(gap),'instance':{'topics':list(map(str,range(k))),'players':m,'customers':[{'topics':[t for t in range(k) if b>>t&1],'multiplicity':v} for b,v in zip(mask,weights) if v]},'certificate':{'terminal_counts':[path.count(t) for t in range(k)],'actions':[{'history':h,'action':t} for h,t in pol.items()]},'progress':records}
     Path(a.output).write_text(json.dumps(report,indent=2)+'\n');print('EXACT FAILURE',sum(weights),flush=True);return
 Path(a.output).write_text(json.dumps({'status':'no counterexample in sampled strict policies','parameters':vars(a),'progress':records},indent=2)+'\n')
if __name__=='__main__':main()
