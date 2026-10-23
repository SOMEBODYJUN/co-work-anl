"""Attack variable-r credible-incumbent Lipschitz candidate exactly."""
import json,sys,itertools
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver

def check(inst, actual_only=True):
 s=ExactSPESolver(inst); k=inst.topic_count;m=inst.players
 def inc(b,a):return tuple(x+(j==a) for j,x in enumerate(b))
 def f(b,t):
  return min(inst.topic_payoff(t,q) for q in s.outcomes(inc(b,t)))
 for depth in range(m-1):
  for h in itertools.combinations_with_replacement(range(k),depth):
   b=inst.counts(h);r=m-depth
   for t in range(k):
    left=f(b,t)
    for a in range(k):
     if actual_only and not any(inst.topic_payoff(a,q)>=s.threshold(b) for q in s.outcomes(inc(b,a))):continue
     right=F(r-1,r)*f(inc(b,a),t)
     if left<right:return dict(prefix=h,T=t,A=a,r=r,left=str(left),right=str(right),instance=inst.to_dict())
 return None
if __name__=='__main__':
 for p in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
  try:inst=Instance.from_dict(json.loads(p.read_text()))
  except (KeyError,ValueError,TypeError):continue
  if inst.players>5 or inst.topic_count>7 or inst.players<2:continue
  c=check(inst)
  if c:
   c['source']=p.name; print(json.dumps(c),flush=True)
   Path(__file__).with_name('incumbent_actual_lipschitz_failure.json').write_text(json.dumps(c,indent=2)+'\n');break
 else:print('no failure')
