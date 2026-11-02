from pathlib import Path
import sys,random,itertools,json,time
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance,CustomerType,ExactSPESolver
from fractions import Fraction
from rank_two_probe import comps

def theta(I,k,prefix):
 vals=[]
 for c in comps(I.players-sum(prefix)-1,k):
  c=c+(0,)*(I.topic_count-k)
  bg=tuple(a+b for a,b in zip(prefix,c))
  vals.append(max(I.topic_payoff(a,bg[:a]+(bg[a]+1,)+bg[a+1:]) for a in range(k)))
 return min(vals)

def main():
 rng=random.Random(92513);best=Fraction(1);start=time.time()
 for k,r,s,num in [(4,3,0,400),(5,3,0,300),(6,4,0,100),(4,3,3,200),(5,3,5,150),(5,4,4,80),(7,5,0,50)]:
  for t in range(num):
   edges=[];base=[]
   for z in [(i,) for i in range(k)]+list(itertools.combinations(range(k),2)):
    w=rng.randrange(1 if len(z)==1 else 0,12)
    if w:
     for v in range(w):edges.append(set(z))
   for j in range(s):
    anchor=rng.randrange(k)
    for e in edges:
     if anchor in e and rng.random()<.5:e.add(k+j)
   d={}
   for e in edges:d[frozenset(e)]=d.get(frozenset(e),0)+1
   prefix=[0]*(k+s)
   for _ in range(rng.randrange(0,4)):prefix[rng.randrange(k+s)]+=1
   I=Instance(tuple(map(str,range(k+s))),tuple(CustomerType(e,w) for e,w in d.items()),r+sum(prefix));S=ExactSPESolver(I)
   root=S.threshold(prefix);th=theta(I,k,prefix);ratio=root/th if th else Fraction(1)
   if ratio<best:
    best=ratio;out={'k':k,'r':r,'s':s,'t':t,'prefix':prefix,'root':str(root),'theta':str(th),'ratio':str(ratio),'instance':I.to_dict()}
    print(json.dumps(out),flush=True)
    Path(__file__).with_name('rank_two_background_best.json').write_text(json.dumps(out,indent=2))
    if ratio<1:return
  print(json.dumps({'done':[k,r,s,num],'best':str(best),'seconds':time.time()-start}),flush=True)
if __name__=='__main__':main()
