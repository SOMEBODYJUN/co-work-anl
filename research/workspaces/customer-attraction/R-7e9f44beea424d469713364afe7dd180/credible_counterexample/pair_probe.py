from pathlib import Path
import sys, random, json
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).parent))
from last_share_probe import *

def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=5);ap.add_argument('--players',type=int,default=3);ap.add_argument('--trials',type=int,default=500);ap.add_argument('--compiler-seeds',action='store_true');ap.add_argument('--output',type=Path,default=Path(__file__).with_name('pair_failure.json'))
 args=ap.parse_args();p,m,trials=args.topics,args.players,args.trials;rng=random.Random(1236);best=F(0)
 for trial,x in zip(range(trials),seeds(p,m,rng,args.compiler_seeds)):
  inst=instance_from_clones(p,m,x);solver=ExactSPESolver(inst)
  choices=[]
  for q in solver.outcomes():
   if not inst.welfare(q):continue
   ps=paths_by_action(solver,q)
   for (pos,a),path in ps.items():
    pays=inst.player_payoffs(path)
    ratio=max(pays)/min(pays) if min(pays)>0 else F(10000)
    choices.append((ratio,q,path))
  _,q,path=max(choices)
  cone=credible_policy(solver,q,path,rng,('high','uniform','low')[trial%3])
  for a in set(path):
   for b in set(path):
    if a==b:continue
    objective=tuple(xx-2*yy for xx,yy in zip(payoff_row(p,q,a),payoff_row(p,q,b)))
    res=linprog(-np.asarray(objective,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.asarray([cone.welfare],float),b_eq=[1],bounds=(0,None),method='highs')
    if not res.success or -res.fun<1e-7:continue
    v=tuple(F(float(xx)).limit_denominator(10**7) for xx in res.x)
    if not(cone.verify(v) and dot(cone.welfare,v)==1):v=cone.recover_vertex(res.x)
    if v is None or not cone.verify(v) or dot(cone.welfare,v)!=1:continue
    value=dot(objective,v)
    if value<=0:continue
    clones=integer_clones(v);assert independently_verify(cone,clones)
    candidate=instance_from_clones(p,m,clones);checked=verify_certificate(candidate,StrategyCertificate(cone.actions,q));checked.assert_valid()
    record={'identity':'pairwise utility disparity >2 only, not aggregate cap or half-coverage counterexample','instance':candidate.to_dict(),'strategy':StrategyCertificate(cone.actions,q).to_dict(),'path':checked.terminal_history,'payoffs':candidate.player_payoffs(checked.terminal_history),'action_high':a,'action_low':b,'normalized_gap':value,'trial':trial}
    out=args.output;out.write_text(json.dumps(serializable(record),indent=2)+'\n');print(json.dumps(serializable({k:val for k,val in record.items() if k not in ('strategy','instance')})),flush=True);return
  if trial%50==0:print('progress',trial,flush=True)
 print('no counterexample in finite search',trials)
if __name__=='__main__':main()
