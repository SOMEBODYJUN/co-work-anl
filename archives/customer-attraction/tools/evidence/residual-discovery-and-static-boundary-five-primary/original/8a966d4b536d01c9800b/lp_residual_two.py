"""LP search for residual-cover strengthening, two-player complete response maps."""
import sys,itertools,random,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
OUT=Path(__file__).resolve().parent

def search(trials=1000,k=6):
    masks=np.arange(1,1<<k);islike=np.array([[(b>>a)&1 for b in masks] for a in range(k)])
    p=np.zeros((k,k,k,len(masks)))
    for a in range(k):
      for b in range(k):
        c=islike[a]+islike[b]
        for who in {a,b}:p[a,b,who]=np.divide(islike[who],c,out=np.zeros(len(masks)),where=c>0)
    welfare=((islike[0]+islike[1])>0).astype(float)
    residual=((islike[0]+islike[1])==0)*((islike[2]+islike[3])>0)
    rng=random.Random(14591);start=time.time()
    for n in range(trials):
        response=[rng.randrange(k) for _ in range(k)];response[0]=1
        constraints=[]
        for a in range(k):
          for b in range(k):constraints.append(p[a,b,b]-p[a,response[a],response[a]])
        for a in range(k):constraints.append(p[a,response[a],a]-p[0,1,0])
        sol=linprog(-residual.astype(float),A_ub=np.array(constraints),b_ub=np.zeros(len(constraints)),A_eq=welfare.reshape(1,-1),b_eq=[1],bounds=(0,None),method='highs')
        if sol.success and -sol.fun>1+1e-7:
            data={'trial':n,'k':k,'response':response,'residual':-sol.fun,'types':[[int(b),float(x)] for b,x in zip(masks,sol.x) if x>1e-8]}
            (OUT/'residual_two_lp_witness.json').write_text(json.dumps(data,indent=2));print(json.dumps(data));return
        if n%200==0:print('lp',n,'elapsed',round(time.time()-start,1),flush=True)
    print('no witness',trials)
if __name__=='__main__':search(int(sys.argv[1]) if len(sys.argv)>1 else 1000)
