from pathlib import Path
import sys,json,time
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance,CustomerType,ExactSPESolver

def instance(k,r,x,a,b,d):
    names=tuple(z+str(i) for i in range(k) for z in ['A','B','C'])+('D',)
    c=[]
    for i in range(k):
        if x:c.append(CustomerType(frozenset({3*i,3*i+1,3*i+2}),x))
        if a:c.append(CustomerType(frozenset({3*i}),a))
    if b:c.append(CustomerType(frozenset([3*i+1 for i in range(k)]+[3*k]),b))
    if d:c.append(CustomerType(frozenset({3*k}),d))
    return Instance(names,tuple(c),k+r)
if __name__=='__main__':
 k,r,x,a,b,d=map(int,sys.argv[1:]);ins=instance(k,r,x,a,b,d);s=ExactSPESolver(ins)
 target=tuple([v for _ in range(k) for v in [0,0,1]]+[r]);t=time.time()
 ok=target in s.outcomes();out={'parameters':[k,r,x,a,b,d],'target':target,'target_w':ins.welfare(target),'opt':ins.optimal_welfare(),'target_spe':ok,'minimum':s.minimum_welfare(),'stats':s.stats.__dict__,'seconds':time.time()-t}
 if not ok:
  c=(0,)*len(target)
  for action in [3*i+2 for i in range(k)]+[3*k]*r:
   floor=s.threshold(c);out.setdefault('path_thresholds',[]).append([list(c),str(floor),str(ins.topic_payoff(action,target))]);c=c[:action]+(c[action]+1,)+c[action+1:]
 print(json.dumps(out),flush=True)
