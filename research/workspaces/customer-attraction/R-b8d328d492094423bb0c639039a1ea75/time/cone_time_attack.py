"""Targeted cone/query coordinate attack on universal uniform-time menu inequality.
Not a certificate unless rational reconstruction and all exact checks pass.
"""
import numpy as np, json, itertools, time, argparse
from functools import lru_cache
from scipy.optimize import linprog
from pathlib import Path


def model(m,k):
 masks=np.arange(1,1<<k)
 inc=((masks[:,None]>>np.arange(k))&1).astype(float)
 @lru_cache(None)
 def compositions(t,j):
  if j==1:return [(t,)]
  return [(a,)+b for a in range(t+1) for b in compositions(t-a,j-1)]
 states=[q for t in range(m+1) for q in compositions(t,k)]
 layers=[[q for q in states if sum(q)==t] for t in range(m+1)]
 def add(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
 terminal=layers[-1]
 payoff={q:np.divide(inc, inc@q[:,None] if False else (inc@np.array(q))[:,None],out=np.zeros_like(inc),where=(inc@np.array(q))[:,None]>0).T for q in terminal}
 extra={q:(inc/(1+inc@np.array(q))[:,None]).T for q in terminal}
 return inc,layers,add,payoff,extra


def policy_from_weights(m,k,w,data,rng):
 inc,layers,add,payoff,extra=data
 out={q:q for q in layers[m]}; policy={}
 for t in range(m-1,-1,-1):
  for q in layers[t]:
   us=np.array([payoff[out[add(q,a)]][a]@w for a in range(k)])
   best=np.flatnonzero(us>=max(us)-1e-9)
   a=int(rng.choice(best));policy[q]=a;out[q]=out[add(q,a)]
 return policy,out


def matrix_policy(m,k,policy,out,data):
 inc,layers,add,payoff,extra=data
 constraints=[]
 for t in range(m):
  for q in layers[t]:
   a=policy[q];own=payoff[out[q]][a]
   for b in range(k):
    row=payoff[out[add(q,b)]][b]-own
    if np.max(np.abs(row))>1e-12:constraints.append(row)
 actual=[];q=(0,)*k;columns=[]
 for i in range(m):
  columns.append(np.stack([extra[out[add(q,a)]] for a in range(k)]))
  a=policy[q];actual.append(a);q=add(q,a)
 W=(inc@np.array(q)>0).astype(float)
 return np.stack(constraints),np.stack(columns),W,actual


def query_oracle(columns,w,lam):
 m,k,_,d=columns.shape
 C=columns@w
 rows=[]
 for i in range(m):
  for a in range(k):
   row=np.zeros(k+m);row[:k]=-C[i,a];row[k+i]=1;rows.append(row)
 z=linprog(np.r_[np.zeros(k),-np.array(lam)],A_ub=rows,b_ub=np.zeros(m*k),A_eq=[np.r_[np.ones(k),np.zeros(m)]],b_eq=[1],bounds=[(0,None)]*(k+m),method='highs')
 if not z.success:raise Exception(z.message)
 return z.x[:k],z.x[k:],-z.fun


def cone_oracle(constraints,columns,W,p,lam):
 m,k,_,d=columns.shape
 rows=np.c_[constraints,np.zeros((len(constraints),m))].tolist()
 for i in range(m):
  for a in range(k):
   row=np.r_[-p@columns[i,a],np.zeros(m)];row[d+i]=1;rows.append(row)
 z=linprog(np.r_[W/m,-np.array(lam)],A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=[np.r_[np.ones(d),np.zeros(m)]],b_eq=[1],bounds=[(0,None)]*(d+m),method='highs')
 if not z.success:raise Exception(z.message)
 return z.x[:d],z.x[d:],-z.fun


def run(args):
 rng=np.random.default_rng(args.seed);records=[];best=-999;start=time.time()
 for m,k in [(3,4),(4,4),(5,4),(6,4),(4,5),(5,5),(6,5)]:
  data=model(m,k);inc=data[0];d=len(inc)
  for seed in range(args.trials):
   w=rng.integers(0,12,size=d).astype(float)
   if seed%3==0:w=(rng.random(d)<.3)*rng.integers(0,8,size=d)
   if not w.sum():w[0]=1
   w=w/w.sum();policy,out=policy_from_weights(m,k,w,data,rng)
   constraints,columns,W,actual=matrix_policy(m,k,policy,out,data)
   for choice in ['uniform','early','late']:
    lam=np.ones(m)/m if choice=='uniform' else np.eye(m)[0 if choice=='early' else m-1]
    w0=w.copy()
    for it in range(args.iterations):
     p,psi,val=query_oracle(columns,w0,lam)
     w1,psi,gap=cone_oracle(constraints,columns,W,p,lam)
     if gap>best:
      best=gap
      print('BEST',m,k,seed,choice,it,gap,'W',W@w1,'p',p.round(6).tolist(),'psi',psi.round(6).tolist(),flush=True)
     if gap>1e-8:
      rec=dict(m=m,k=k,seed=seed,choice=choice,iteration=it,gap=gap,weights=w1.tolist(),p=p.tolist(),psi=psi.tolist(),W=float(W@w1),actual=actual,policy={','.join(map(str,q)):a for q,a in policy.items()})
      records.append(rec)
      Path(args.output).write_text(json.dumps({'records':records,'elapsed':time.time()-start},indent=2))
      if choice=='uniform':return
     if np.max(np.abs(w0-w1))<1e-8:break
     w0=w1
   if seed%10==0:print('progress',m,k,seed,'best',best,'elapsed',time.time()-start,flush=True)
 Path(args.output).write_text(json.dumps({'records':records,'elapsed':time.time()-start,'best':best,'scope':'Finite coordinate-cone attack; negative results prove no universal claim.'},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--trials',type=int,default=25);p.add_argument('--iterations',type=int,default=4);p.add_argument('--seed',type=int,default=331902);p.add_argument('--output',default=str(Path(__file__).with_suffix('.json')));run(p.parse_args())
