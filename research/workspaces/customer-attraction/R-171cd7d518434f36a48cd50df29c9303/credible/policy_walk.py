"""Credible full-history strategy-cone walk, exact acceptance.
No count Markov selector is asserted to cover all SPE strategies.
Float LP proposes a multiplicity point; canonical full-history Fraction verifier accepts it.
"""
from pathlib import Path
import sys,json,time,random,argparse,hashlib
from fractions import Fraction
from itertools import combinations
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction import ExactSPESolver,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import instance_from_clones,integer_clones,serializable,independently_verify,payoff_row
import numpy as np
from cone_attack_credible_variants import credible_cone,clones_of

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--steps',type=int,default=20);ap.add_argument('--p',type=int,default=7);ap.add_argument('--m',type=int,default=5);ap.add_argument('--seed',type=int,default=105);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--random-restarts',action='store_true');ap.add_argument('--lowfirst',type=str);ap.add_argument('--reply-seeds',action='store_true');args=ap.parse_args()
 rng=random.Random(args.seed);p=args.p;m=args.m;n=(1<<p)-1
 weights={1:m};weights.update({1<<j:1 for j in range(1,p)})
 clone=tuple(weights.get(x,0) for x in range(1,1<<p))
 pool=[clone];seen=set();best=Fraction(0);started=time.monotonic();log=[]
 for step in range(args.steps):
  source=pool[-1] if rng.random()<.7 else rng.choice(pool)
  if args.reply_seeds and step%3==0:
   if p!=7 or m!=5:raise ValueError('reply seed dimensions')
   x=12;b=4;alist=[4,5,6,7]
   weights={16|32:x,16|64:x}
   for j,a in enumerate(alist):weights[1<<j]=a;weights[(1<<j)|32|64]=b
   source=tuple(weights.get(mask,0) for mask in range(1,1<<p))
  if args.random_restarts and step%3==0:
   weights={}
   for a in range(p):weights[1<<a]=rng.randrange(1,9)
   for _ in range(2*p):
    mask=sum(1<<a for a in rng.sample(range(p),rng.choice((2,2,3,4))))
    weights[mask]=rng.choice((1,2,3,5,8,13,21))
   source=tuple(weights.get(mask,0) for mask in range(1,1<<p))
  ins=instance_from_clones(p,m,source);sol=ExactSPESolver(ins);outcomes=sorted(sol.worst_outcomes())
  if args.lowfirst:
   cap=Fraction(args.lowfirst);floor=sol.threshold((0,)*p)
   eligible=[]
   for q in sol.outcomes():
    if any(q in sol.outcomes(tuple(int(j==a) for j in range(p))) and floor<=sol._utility(q,a)<=cap*ins.welfare(q) for a in range(p)):
     eligible.append(q)
   if eligible:
    v=min(ins.welfare(q) for q in eligible);outcomes=[q for q in eligible if ins.welfare(q)==v]
  target=rng.choice(outcomes);mode=rng.choice(('uniform_credible','max_credible_payoff','min_credible_welfare','max_credible_welfare'))
  class InitialChoice:
   first=True
   def choice(self,options):
    if self.first:
     self.first=False;return min(options,key=lambda a:sol._utility(target,a))
    return rng.choice(options)
  cone,stats=credible_cone(sol,target,InitialChoice() if args.lowfirst else rng,mode)
  J=tuple(range(min(m,p))) if step%3 else rng.choice(tuple(combinations(range(p),min(m,p))))
  if args.lowfirst:
   cap=Fraction(args.lowfirst);first=cone.actions[()]
   added=tuple(cap*w-u for w,u in zip(cone.welfare,payoff_row(p,cone.root,first)))
   cone.rows=cone.rows+(added,);cone.matrix=np.array(cone.rows,dtype=float)
  result=cone.optimize(J)
  if not result['certified']:
   print(json.dumps({'step':step,'status':result['status']}),flush=True);continue
  point=integer_clones(result['values']);candidate=instance_from_clones(p,m,point)
  cert=StrategyCertificate(cone.actions,cone.root);verify_certificate(candidate,cert).assert_valid()
  W=candidate.welfare(cone.root);opt=candidate.optimal_welfare();ratio=Fraction(opt,W)
  q=tuple(point)
  if q not in seen:pool.append(q);seen.add(q)
  record={'step':step,'mode':mode,'ratio':ratio,'W':W,'OPT':opt,'LP_objective':result['value'],'source':source,'clones':point,'root_counts':cone.root,'stats':stats,'pool':len(pool),'rows':len(cone.rows),'seconds':time.monotonic()-started}
  if ratio>best or ratio>=2:
   best=max(best,ratio);record['strategy']=cert.to_dict()
   path=args.out/f'best_{step}.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(serializable(record),indent=2)+'\n')
   if not independently_verify(cone,point):raise AssertionError('independent exact full tree')
  log.append({k:v for k,v in record.items() if k!='strategy'});print(json.dumps(serializable({k:v for k,v in record.items() if k not in ('strategy','source','clones')})),flush=True)
  (args.out/'log.json').write_text(json.dumps(serializable(log),indent=2)+'\n')
  if ratio>2:break
if __name__=='__main__':main()
