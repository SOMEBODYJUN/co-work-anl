"""Finite signed-potential experiment: all ordered binary policies n<=4, fixed p.
Anonymous two-action payoffs (a_1..a_n,b_0..b_{n-1}) are unrestricted.
LP feasibility is only discovery; infeasibility counts are not a general theorem.
"""
import argparse,itertools,json,time
import numpy as np
from scipy.optimize import linprog

def check(n,p,limit):
 hs=[h for d in range(n) for h in itertools.product((0,1),repeat=d)];idx={h:i for i,h in enumerate(hs)}
 payoff=np.eye(2*n); zero=np.zeros(2*n)
 def u(act,k):return payoff[k-1] if act==0 else payoff[n+k]
 count=0;start=time.time();out={'players':n,'pA':p,'full_policies':2**len(hs),'tested':0,'found':None}
 for code in range(min(2**len(hs),limit)):
  acts=[(code>>i)&1 for i in range(len(hs))]
  terminals={}
  for d in range(n-1,-1,-1):
   for h in itertools.product((0,1),repeat=d):
    a=acts[idx[h]];hh=h+(a,)
    terminals[h]=hh if d==n-1 else terminals[hh]
  z=terminals[()];k=z.count(0);W=k*u(0,k)+(n-k)*u(1,k) if 0<k<n else n*u(z[0],k)
  rows=[]
  for h in hs:
   a=acts[idx[h]];zz=terminals[h];actual=u(a,zz.count(0));alt=1-a;hh=h+(alt,);other=hh if len(hh)==n else terminals[hh]
   rows.append(u(alt,other.count(0))-actual)
  menu=set()
  for i in range(n):
   for a in (0,1):
    hh=z[:i]+(a,);zz=hh if len(hh)==n else terminals[hh]
    menu.add(zz.count(0)-(a==0))
  # max t subject to W/n-pmean(H)+t<=0, bounded payoff box for scale.
  for j in menu:rows.append(W/n-p*u(0,j+1)-(1-p)*u(1,j))
  lp=linprog(np.r_[np.zeros(2*n),-1.],A_ub=np.c_[np.array(rows),np.r_[np.zeros(len(hs)),np.ones(len(menu))]],b_ub=np.zeros(len(rows)),bounds=[(-1,1)]*(2*n)+[(None,None)],method='highs')
  count+=1
  if lp.success and lp.x[-1]>1e-8:
   out['found']={'code':code,'path':z,'menu_countsA':sorted(menu),'gap':lp.x[-1],'payoffs':lp.x[:-1].tolist()};break
 out['tested']=count;out['seconds']=time.time()-start
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=4);ap.add_argument('--p',type=float,default=.5);ap.add_argument('--limit',type=int,default=32768);ap.add_argument('--output',required=True);a=ap.parse_args();o=check(a.n,a.p,a.limit);json.dump(o,open(a.output,'w'),indent=2);print(json.dumps(o))
