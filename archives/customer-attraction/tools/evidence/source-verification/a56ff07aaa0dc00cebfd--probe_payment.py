from __future__ import annotations
import sys,json,random,time,argparse
from pathlib import Path
from fractions import Fraction
from itertools import combinations,permutations,product
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver
import importlib.util
sp=importlib.util.spec_from_file_location('slp',ROOT/'tests/audits/customer_attraction_strategy_lp.py')
slp=importlib.util.module_from_spec(sp);sys.modules['slp']=slp;sp.loader.exec_module(slp)
OUT=Path(__file__).resolve().parent

def payment_rows(cone,support):
 h=();result=[]
 for i in range(cone.players):
  result.append(tuple(slp.payoff_row(cone.topics,cone.terminals[h+(a,)],a) for a in support))
  h=h+(cone.actions[h],)
 return result

def probe(cone,support,matching=True):
 n=(1<<cone.topics)-1
 objective=slp.coverage_row(cone.topics,support)
 rows=payment_rows(cone,support)
 if matching:
  pm=[tuple(sum((rows[i][perm[i]][j] for i in range(cone.players)),Fraction(0)) for j in range(n)) for perm in permutations(range(cone.players))]
  c=np.r_[np.array(cone.welfare,dtype=float)-np.array(objective,dtype=float),1.]
  aub=np.c_[-cone.matrix,np.zeros(len(cone.rows))]
  aub=np.r_[aub,np.c_[np.array(pm,dtype=float),-np.ones(len(pm))]]
  rhs=np.zeros(len(aub))
  res=linprog(c,A_ub=aub,b_ub=rhs,A_eq=np.array([tuple(cone.welfare)+(Fraction(0),)],float),b_eq=[1],bounds=[(0,None)]*n+[(None,None)],method='highs')
 else:
  avg=tuple(sum((rows[i][k][j] for i in range(cone.players) for k in range(len(support))),Fraction(0))/len(support) for j in range(n))
  c=np.array(tuple(w+p-o for w,p,o in zip(cone.welfare,avg,objective)),float)
  res=linprog(c,A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],float),b_eq=[1],bounds=(0,None),method='highs')
 if not res.success:return None
 if res.fun>=-1e-7:return None
 vals=tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x[:n])
 if not cone.verify(vals) or slp.dot(cone.welfare,vals)!=1:
  vals=cone.recover_vertex(res.x[:n])
 if vals is None or not cone.verify(vals):return None
 matrix=[[slp.dot(r,vals) for r in rs] for rs in rows]
 best=max(sum(matrix[i][perm[i]] for i in range(cone.players)) for perm in permutations(range(cone.players)))
 avg=sum(sum(rs) for rs in matrix)/len(support)
 opt=slp.dot(objective,vals)
 val=opt-1-(best if matching else avg)
 if val<=0:return None
 clones=slp.integer_clones(vals)
 inst=slp.instance_from_clones(cone.topics,cone.players,clones)
 return {'instance':inst.to_dict(),'actions':[{ 'h':list(h),'a':a} for h,a in cone.actions.items()],'portfolio':list(support),'root':list(cone.root),'W':inst.welfare(cone.root),'ratio':str(opt),'matching':str(best),'uniform':str(avg),'gap':str(val),'kind':'matching' if matching else 'uniform'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=6);ap.add_argument('--players',type=int,default=5);ap.add_argument('--cones',type=int,default=20);ap.add_argument('--seed',type=int,default=619);ap.add_argument('--matching',action='store_true');ns=ap.parse_args()
 rng=random.Random(ns.seed);p=ns.topics;m=ns.players;start=time.time();seen=set();ci=0
 seeds=list(slp.structural_seeds(p,m))
 while ci<ns.cones:
  if seeds:r=seeds.pop(0)
  else:r=tuple(rng.randrange(0,7) if rng.random()<.25 else 0 for mask in range(1,1<<p))
  inst=slp.instance_from_clones(p,m,r);solver=ExactSPESolver(inst)
  for target in sorted(solver.worst_outcomes()):
   for rep in range(2):
    cone=slp.cone_from_solver(solver,target,rng,rep==1)
    key=tuple(sorted(cone.actions.items()))
    if key in seen:continue
    seen.add(key);ci+=1
    for support in combinations(range(p),m):
     ans=probe(cone,support,ns.matching)
     if ans:
      path=OUT/('payment_failure_'+ans['kind']+'.json');path.write_text(json.dumps(ans,indent=2));print('FOUND',path,ans['gap'],ans['ratio'],flush=True);return
    print(ci,'elapsed',round(time.time()-start,2),flush=True)
    if ci>=ns.cones:break
   if ci>=ns.cones:break
if __name__=='__main__':main()
