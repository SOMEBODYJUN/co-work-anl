"""Joint cones for independent node-minimum SPEs along an arbitrary path.

A feasible point with summed node payoffs < OPT/2 refutes only the threshold
path bridge, since these independent SPEs need not form one actual path.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance,ExactSPESolver
from fractions import Fraction
from scipy.optimize import linprog
from functools import lru_cache
import numpy as np, json,argparse,itertools,random,math

def run(inst,path,rng):
 sol=ExactSPESolver(inst);p=inst.topic_count;m=inst.players;L=math.lcm(*range(1,m+1));masks=range(1,1<<p)
 @lru_cache(None)
 def vec(c,a):
  return np.array([L//sum(c[b] for b in range(p) if mask>>b&1) if mask>>a&1 else 0 for mask in masks],dtype=np.int64)
 # a is occupied in each vector request, so denominator nonzero whenever needed.
 rows=[]; objective=np.zeros((1<<p)-1,dtype=np.int64);chosen=[]
 for t in range(m):
  k=inst.counts(path[:t]);floor=sol.threshold(k)
  choices=[(a,c) for a in range(p) for c in sol.outcomes(k[:a]+(k[a]+1,)+k[a+1:]) if inst.topic_payoff(a,c)==floor]
  # equality alone ensures the branch is a valid min-payoff SPE at this node.
  a,target=rng.choice(choices);objective+=vec(target,a);chosen.append((a,target))
  def expand(k,target,forced=None):
   if sum(k)==m:return target
   floor=sol.threshold(k)
   admissible=[a for a in range(p) if target in sol.outcomes(k[:a]+(k[a]+1,)+k[a+1:]) and inst.topic_payoff(a,target)>=floor]
   chosen_a=forced if forced is not None else rng.choice(admissible)
   terminals=[]
   for b in range(p):
    child=k[:b]+(k[b]+1,)+k[b+1:]
    if b==chosen_a:want=target
    else:
     ell=min(inst.topic_payoff(b,c) for c in sol.outcomes(child))
     want=rng.choice([c for c in sol.outcomes(child) if inst.topic_payoff(b,c)==ell])
    terminals.append(expand(child,want))
   actual=terminals[chosen_a]
   for b in range(p):
    if b!=chosen_a:rows.append(vec(actual,chosen_a)-vec(terminals[b],b))
   return actual
  expand(k,target,a)
 # maximizing witness coverage can use each support <=m. Pick the original best.
 supports=list(itertools.combinations(range(p),min(m,p)))
 support=max(supports,key=lambda z:inst.welfare(tuple(int(a in z) for a in range(p))))
 cover=np.array([int(any(mask>>a&1 for a in support)) for mask in masks],dtype=float)
 result=linprog(objective.astype(float),A_ub=-np.array(rows,dtype=float),b_ub=np.zeros(len(rows)),A_eq=[cover],b_eq=[1],bounds=(0,None),method='highs')
 if not result.success:return None
 return float(result.fun/L),result.x,{'path':path,'node_choices':[(a,list(c)) for a,c in chosen],'comparison_support':support,'rows':len(rows),'objective_scaled':objective.tolist()}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--trials',type=int,default=20);ap.add_argument('--seed',type=int,default=20261021);ap.add_argument('--output',required=True);args=ap.parse_args()
 raw=json.loads(Path(args.input).read_text());inst=Instance.from_dict(raw.get('instance',raw));rng=random.Random(args.seed)
 # source min-Q path; random trials alternate unrestricted and exact shortest path
 import importlib.util
 s=importlib.util.spec_from_file_location('probe',Path(__file__).with_name('threshold_probe.py'));mod=importlib.util.module_from_spec(s);s.loader.exec_module(mod)
 q,minpath,sol=mod.run(inst);best=1
 for t in range(args.trials):
  path=minpath if t%2==0 else tuple(rng.randrange(inst.topic_count) for _ in range(inst.players))
  out=run(inst,path,rng)
  if out is None:continue
  ratio,w,meta=out
  if ratio<best:
   best=ratio;record={'status':'floating LP proposal requiring rational reconstruction','source':args.input,'trial':t,'ratio':ratio,'weights':w.tolist(),**meta}
   Path(args.output).write_text(json.dumps(record,indent=2)+'\n');print(t,ratio,meta['path'],flush=True)
  if ratio<.5-1e-9:break
if __name__=='__main__':main()
