#!/usr/bin/env python3
"""Numerical policy/cone iteration for m*u_last/W; exact candidate recovery."""
from pathlib import Path
import sys,random,json,time
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
import numpy as np
from scipy.optimize import linprog
from customer_attraction import ExactSPESolver,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import StrategyCone,payoff_row,instance_from_clones,integer_clones,dot,serializable,independently_verify


def increment(k,a):return tuple(x+(i==a) for i,x in enumerate(k))

def policy(solver,path,rng):
 p,m=solver.instance.topic_count,solver.instance.players
 target=solver.instance.counts(path,terminal=True);actions={}
 def expand(h,k,q):
  if len(h)==m:return
  floor=solver.threshold(k)
  options=[a for a in range(p) if q in solver.outcomes(increment(k,a)) and solver._utility(q,a)>=floor]
  chosen=path[len(h)] if h==path[:len(h)] else rng.choice(options)
  assert chosen in options
  actions[h]=chosen;actual=solver._utility(q,chosen)
  for a in range(p):
   child=increment(k,a)
   if a==chosen:desired=q
   else:
    menu=[d for d in solver.outcomes(child) if solver._utility(d,a)<=actual]
    desired=rng.choice(sorted(menu))
   expand(h+(a,),child,desired)
 expand((),(0,)*p,target)
 return StrategyCone(p,m,actions)


def optimize(cone,last):
 objective=tuple(cone.players*v for v in payoff_row(cone.topics,cone.root,last))
 res=linprog(-np.array(objective,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
 if not res.success:return None
 vals=tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
 if not cone.verify(vals) or dot(cone.welfare,vals)!=1:vals=cone.recover_vertex(res.x)
 if vals is None or not cone.verify(vals) or dot(cone.welfare,vals)!=1:return None
 return dot(objective,vals),integer_clones(vals)


def best_path(solver,rng):
 paths=list(solver.ordered_outcomes())
 values=[Fraction(solver.instance.players)*solver.instance.player_payoffs(path)[-1]/max(1,solver.instance.welfare(solver.instance.counts(path))) for path in paths]
 mx=max(values)
 return rng.choice([path for path,val in zip(paths,values) if val==mx]),mx


def main():
 rng=random.Random(431904);start=time.time();best=Fraction(0);records=[];trials=0
 for players,topics in [(5,5),(6,5),(7,5)]:
  for restart in range(30):
   weights=[0]*((1<<topics)-1)
   if restart==0:
    weights[0]=players-1;weights[1]=2
   else:
    for mask in rng.sample(range(1,1<<topics),rng.randrange(5,16)):weights[mask-1]=rng.randrange(1,15)
   for iteration in range(6):
    instance=instance_from_clones(topics,players,weights);solver=ExactSPESolver(instance)
    path,_=best_path(solver,rng);cone=policy(solver,path,rng)
    result=optimize(cone,path[-1]);trials+=1
    if result is None:break
    value,clones=result
    if value>best:
     assert independently_verify(cone,clones)
     newinstance=instance_from_clones(topics,players,clones)
     verify_certificate(newinstance,StrategyCertificate(cone.actions,cone.root)).assert_valid()
     best=value;record={'players':players,'topics':topics,'restart':restart,'iteration':iteration,'trials':trials,'value':str(value),'path':path,'clones':clones,'actions':[{'history':h,'action':a} for h,a in sorted(cone.actions.items())]}
     records.append(record)
     print(json.dumps({k:record[k] for k in ['players','restart','iteration','trials','value']}),flush=True)
     Path(__file__).with_name('terminal_cap_iteration.json').write_text(json.dumps(serializable({'seed':431904,'trials':trials,'records':records}),indent=2)+'\n')
     if best>2:raise SystemExit('Exact candidate refutes cap')
    if clones==tuple(weights):break
    weights=clones
  print(json.dumps({'completed_players':players,'best':str(best),'seconds':time.time()-start}),flush=True)
 print('FINAL',trials,best,time.time()-start)

if __name__=='__main__':main()
