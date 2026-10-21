from pathlib import Path
import sys,random,json,time
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance,CustomerType,ExactSPESolver
from fractions import Fraction
from itertools import permutations
ROOT=Path(__file__).parent
MASKS=[sum((1<<(2+i)) for i in range(4) if mask>>i&1) for mask in range(1,16)]
def make(w,k=1,x=3,a=2):
 names=tuple(z+str(i) for i in range(k) for z in ['C','A','B1','B2'])+('D1','D2')
 c=[CustomerType(frozenset(range(4*i,4*i+4)),x) for i in range(k)]+[CustomerType(frozenset({4*i+1}),a) for i in range(k)]
 for mask,n in zip(MASKS,w):
  if not n:continue
  topics=set()
  for b in range(2):
   if mask>>(2+b)&1:topics.update(4*i+2+b for i in range(k))
  for d in range(2):
   if mask>>(4+d)&1:topics.add(4*k+d)
  c.append(CustomerType(frozenset(topics),n))
 return Instance(names,tuple(c),k+2)
def score(w):
 ins=make(w);s=ExactSPESolver(ins);target=ins.counts((0,4,5),terminal=True)
 deficits=[]
 for path in [(0,4,5),(0,5,4)]:
  c=(0,)*6;v=Fraction(0)
  for act in path:
   v+=max(Fraction(0),s.threshold(c)-ins.topic_payoff(act,target));c=c[:act]+(c[act]+1,)+c[act+1:]
  deficits.append(v)
 return min(deficits),ins,s
if __name__=='__main__':
 rng=random.Random(20261021);best=100;w=[0]*15;cur=100;started=time.time()
 for it in range(20000):
  if it%1000==0:
   w=[0]*15
   for j in range(rng.randrange(6,16)):w[rng.randrange(15)]+=1
   cur,_,_=score(w)
  v=w.copy();p=rng.randrange(15);v[p]=max(0,v[p]+rng.choice([-1,1]));z,ins,s=score(v)
  if z<cur or z==cur and rng.randrange(3)==0:w=v;cur=z
  if z<best:
   best=z;print(it,'deficit',best,'w',v,flush=True)
   data={'instance':ins.to_dict(),'deficit':str(z),'weights':v,'iteration':it}
   (ROOT/'anchor_best.json').write_text(json.dumps(data,indent=2))
  if z==0:
   print('CANDIDATE',json.dumps(ins.to_dict()),flush=True);break
 print('finished',it,'seconds',time.time()-started,flush=True)
