from pathlib import Path
import sys,json,time
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

def instance(m):
 k=m-1;p=3*k+2;B=3*k;T=B+1
 types=[]
 for i in range(k):
  types.extend([CustomerType(frozenset([i,k+2*i]),2),CustomerType(frozenset([i,k+2*i+1]),2)])
 types.extend([CustomerType(frozenset([B]),3),CustomerType(frozenset([T]),3),CustomerType(frozenset([B]+list(range(k,3*k))),2),CustomerType(frozenset([T]+list(range(k,3*k))),2)])
 return Instance(tuple(map(str,range(p))),tuple(types),m)
if __name__=='__main__':
 for m in map(int,sys.argv[1:] or ['3','4']):
  inst=instance(m);s=ExactSPESolver(inst);c=inst.counts(list(range(m-1))+[3*(m-1)]);t=time.time()
  outcomes=s.outcomes();print(m,'target',c in outcomes,'n_out',len(outcomes),'time',time.time()-t,flush=True)
  if c in outcomes:
   cert=s.certificate(c,on_path=list(range(m-1))+[3*(m-1)])
   Path(__file__).with_name(f'multigadget_m{m}.json').write_text(json.dumps(dict(instance=inst.to_dict(),certificate=cert.to_dict())))
