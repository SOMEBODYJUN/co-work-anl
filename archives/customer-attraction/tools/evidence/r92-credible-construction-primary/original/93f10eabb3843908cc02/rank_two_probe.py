from pathlib import Path
import sys,random,itertools,json,time
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance,CustomerType,ExactSPESolver
from fractions import Fraction

def comps(n,k):
 if k==1:yield(n,);return
 for a in range(n+1):
  for z in comps(n-a,k-1):yield(a,)+z

def theta(I):
 vals=[]
 for p in comps(I.players-1,I.topic_count):
  vals.append(max(I.topic_payoff(a,p[:a]+(p[a]+1,)+p[a+1:]) for a in range(I.topic_count)))
 return min(vals)

def main():
 rng=random.Random(9251);best=Fraction(1);start=time.time()
 for k,m,num in [(4,3,400),(5,3,300),(6,3,150),(5,4,100),(6,4,50),(7,5,10)]:
  for t in range(num):
   ty=[]
   for s in [(i,) for i in range(k)]+list(itertools.combinations(range(k),2)):
    w=rng.randrange(0,12)
    if w:ty.append(CustomerType(frozenset(s),w))
   I=Instance(tuple(map(str,range(k))),tuple(ty),m);S=ExactSPESolver(I)
   root=S.threshold((0,)*k);th=theta(I);ratio=root/th if th else Fraction(1)
   if ratio<best:
    best=ratio;out={'k':k,'m':m,'t':t,'root':str(root),'theta':str(th),'ratio':str(ratio),'instance':I.to_dict()}
    print(json.dumps(out),flush=True)
    Path(__file__).with_name('rank_two_best.json').write_text(json.dumps(out,indent=2))
    if ratio<1:return
  print(json.dumps({'done':[k,m,num],'best':str(best),'seconds':time.time()-start}),flush=True)
if __name__=='__main__':main()
