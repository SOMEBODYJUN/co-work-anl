"""Finite full-strategy-cone attack on the prefix-penalty payment interface.

A positive point must satisfy every exact t breakpoint and every tested prefix,
and must make the fixed m-topic comparison support uniquely coverage-optimal.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse,json,math,random,sys
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver,verify_certificate
from entrant_cone_probe import cone

def penalty_rows(m,p,masks,actual,opt,klist):
    d=[sum(bool(s&(1<<a)) for a in opt) for s in masks]
    c=[sum(bool(s&(1<<a)) for a in actual) for s in masks]
    rows=[];meta=[]
    for k in klist:
        b=[sum(bool(s&(1<<a)) for a in actual[:m-k]) for s in masks]
        ts={F(0),F(4)}|{F(4*m*(bb+1),dd*(k-1)+m*(bb+1)) for bb,dd in zip(b,d) if dd}
        for t in sorted(ts):
            row=[]
            for bb,cc,dd in zip(b,c,d):
                J=(1-F(2*(k-2)*dd,m*(bb+k))-min(F(t*dd,m*(bb+1)),F(t*dd/m+4-t,bb+k))) if dd else F(0)
                row.append(J-(F(2*bb,cc) if cc else F(0)))
            rows.append(tuple(row));meta.append((k,str(t)))
    return rows,meta

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=5);ap.add_argument('--topics',type=int,default=6);ap.add_argument('--rounds',type=int,default=20);ap.add_argument('--seed',type=int,default=739124);ap.add_argument('--all-prefixes',action='store_true');ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 if args.output.exists():raise ValueError('refuse overwrite')
 rng=random.Random(args.seed);m=args.players;p=args.topics;best=0.;checks=0
 supports=list(combinations(range(p),min(m,p)))
 for it in range(args.rounds):
  weights={1<<a:rng.randint(1,10) for a in range(p)}
  weights.update({s:rng.randint(1,15) for s in rng.sample(range(1,1<<p),min(10,(1<<p)-1))})
  inst=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if s>>a&1),w) for s,w in weights.items()),m)
  sol=ExactSPESolver(inst);target=rng.choice(sorted(sol.outcomes()));cert=sol.certificate(target,action_selector=lambda h,c:rng.choice(c),continuation_selector=lambda h,c:rng.choice(c))
  masks,game,_,actual=cone(cert,m,p)
  opt=max(supports,key=lambda z:sum(w for s,w in weights.items() if any(s>>a&1 for a in z)))
  pay,meta=penalty_rows(m,p,masks,actual,opt,range(2,m+1) if args.all_prefixes else [2])
  o=tuple(int(any(s>>a&1 for a in opt)) for s in masks)
  optimality=[]
  for other in supports:
   if other==opt:continue
   oo=[int(any(s>>a&1 for a in other)) for s in masks]
   optimality.append(tuple(x-y for x,y in zip(o,oo)))
  constraints=game+pay+optimality
  A=np.zeros((len(constraints),len(masks)+1));A[:,:-1]=-np.array(constraints,dtype=float)
  A[len(game):,-1]=1.
  objective=np.zeros(len(masks)+1);objective[-1]=-1
  eq=np.zeros((1,len(masks)+1));eq[0,:-1]=1
  res=linprog(objective,A_ub=A,b_ub=np.zeros(len(A)),A_eq=eq,b_eq=[1],bounds=[(0,None)]*len(masks)+[(None,None)],method='highs');checks+=1
  if not res.success:raise RuntimeError(res.message)
  gap=res.x[-1]
  if gap>best+1e-8:best=gap;print(json.dumps({'iteration':it,'gap':gap,'actual':actual,'opt':opt}),flush=True)
  if gap>1e-7:
   fr=[F(float(x)).limit_denominator(10**7) for x in res.x[:-1]];den=math.lcm(*(x.denominator for x in fr));ints=[int(x*den) for x in fr];g=math.gcd(*ints);ints=[w//g for w in ints]
   dot=lambda row:sum(x*w for x,w in zip(row,ints))
   if min(map(dot,game),default=F(0))<0 or min(map(dot,pay+optimality))<=0:print('rejected rationalization',flush=True);continue
   cand=Instance(inst.topics,tuple(CustomerType(frozenset(a for a in range(p) if s>>a&1),w) for s,w in zip(masks,ints) if w),m);verify_certificate(cand,cert).assert_valid()
   record={'status':'exact_auxiliary_counterexample_candidate','parameters':vars(args)|{'output':str(args.output)},'iteration':it,'actual':actual,'optimal_support':opt,'minimum_penalty_slack':str(min(map(dot,pay))),'minimum_optimality_slack':str(min(map(dot,optimality))),'instance':cand.to_dict(),'certificate':cert.to_dict(),'penalty_slacks':[dict(k=k,t=t,slack=str(dot(row))) for row,(k,t) in zip(pay,meta)]}
   args.output.write_text(json.dumps(record,indent=2)+'\n');print('FOUND',args.output,flush=True);return
 args.output.write_text(json.dumps({'status':'finite_probe_only','parameters':vars(args)|{'output':str(args.output)},'LP_checks':checks,'maximum_positive_gap':best},indent=2)+'\n');print('DONE',checks,best,flush=True)
if __name__=='__main__':main()
