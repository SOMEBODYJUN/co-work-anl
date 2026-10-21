from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,sys,random
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('weakprobe',P/'root_stationary_weak_probe.py');wp=importlib.util.module_from_spec(spec);spec.loader.exec_module(wp)
from customer_attraction import CustomerType,Instance,ExactSPESolver

def run(n=4,p=6,rounds=40,seed=22345):
 rng=random.Random(seed);best=0;reports=[]
 for step in range(rounds):
  mas={mask:rng.choice([0,0,0,1,1,2,3,5,8]) for mask in range(1,1<<p)}
  if step%3==0:mas={mask:(rng.randint(1,12) if mask.bit_count()<=3 and rng.random()<.4 else 0) for mask in range(1,1<<p)}
  ins=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),v) for mask,v in mas.items() if v),n)
  sol=ExactSPESolver(ins);target=rng.choice(sorted(sol.worst_outcomes()));cert=sol.certificate(target,action_selector=lambda h,c:rng.choice(c),continuation_selector=lambda h,c:rng.choice(c))
  got=wp.analyze(cert.actions,n,p,f'random:{step}')
  if got.get('status')=='stationary_not_unique':continue
  v=max(r['float'] for r in got['reports'])
  if v>best+1e-8:
   best=v;got['step']=step;got['actions']=[dict(history=h,action=a) for h,a in sorted(cert.actions.items())];reports.append(got)
   print(json.dumps(dict(step=step,best=best,threshold=2/(2*n-1),pi=got['pi'])),flush=True)
   (P/'root_stationary_random.json').write_text(json.dumps(dict(players=n,topics=p,seed=seed,reports=reports),indent=2))
  if any(r.get('violates_weaker_cap') for r in got['reports']):return got
 return None
if __name__=='__main__':run(*map(int,sys.argv[1:]))
