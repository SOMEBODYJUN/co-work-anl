"""LCM-exact integer mutation attack of myopic-ceiling DP, then Fraction replay."""
from pathlib import Path
import sys,json,math,random,time,argparse
from fractions import Fraction as F
from itertools import combinations
import numpy as np
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(Path(__file__).parent.parent/'independent')]
from customer_attraction import Instance,CustomerType
from myopic_ceiling_dp import MyopicCeilingFloor


def compositions(n,k):
 if k==1:yield(n,)
 else:
  for x in range(n+1):
   for tail in compositions(n-x,k-1):yield(x,)+tail

class Engine:
 def __init__(self,p,m):
  self.p,self.m=p,m;self.L=math.lcm(*range(1,m+1));self.masks=np.arange(1,1<<p,dtype=np.int64);self.inc=((self.masks[:,None]>>np.arange(p))&1)
  self.states=[q for d in range(m+1)for q in compositions(d,p)];self.ids={q:i for i,q in enumerate(self.states)}
  self.nonterm=[i for i,q in enumerate(self.states)if sum(q)<m];self.terminal=[i for i,q in enumerate(self.states)if sum(q)==m]
  def coeff(q,a,missing=False):
   den=self.inc@np.array(q)
   if missing:den=den+self.inc[:,a]
   return np.array([self.L//int(v)if self.inc[j,a]and v else 0 for j,v in enumerate(den)],np.int64)
  self.paycoeff=np.array([[coeff(self.states[i],a)if self.states[i][a]else np.zeros(len(self.masks),np.int64)for a in range(p)]for i in self.terminal])
  self.myocoeff=np.array([[coeff(self.states[i],a,True)for a in range(p)]for i in self.nonterm])
  self.children={i:[self.ids[tuple(x+(a==j)for j,x in enumerate(self.states[i]))]for a in range(p)]for i in self.nonterm}
  self.portfolios=list(combinations(range(p),min(p,m)));self.cov=np.array([np.any(self.inc[:,q],axis=1)for q in self.portfolios],np.int64)
 def solve(self,r):
  r=np.array(r,np.int64);pay=self.paycoeff@r;myo=self.myocoeff@r
  H=[None]*len(self.states);G=[0]*len(H);floor=[None]*len(H);allowed=[None]*len(H)
  for t,i in enumerate(self.terminal):H[i]=np.array([t],np.int32)
  for i in reversed(self.nonterm):
   cs=self.children[i];f=max(int(pay[H[c],a].min())for a,c in enumerate(cs));aa=[a for a in range(self.p)if myo[i,a]>=f]
   H[i]=np.unique(np.concatenate([H[cs[a]]for a in aa]));floor[i]=f;allowed[i]=aa;G[i]=f+min(G[cs[a]]for a in aa)
  opt=int((self.cov@r).max());ratio=F(G[0],self.L*opt)if opt else F(1)
  self.last=(H,G,floor,allowed)
  return ratio
 def instance(self,r):return Instance(tuple(f'T{a}'for a in range(self.p)),tuple(CustomerType(frozenset(a for a in range(self.p)if mask>>a&1),int(v))for mask,v in enumerate(r,1)if v),self.m)


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--p',type=int,default=6);ap.add_argument('--m',type=int,default=4);ap.add_argument('--rounds',type=int,default=3000);args=ap.parse_args()
 eng=Engine(args.p,args.m);rng=random.Random(32122);n=(1<<args.p)-1
 source=Instance.from_dict(json.loads((ROOT/'examples/customer_attraction/root_tax_failure.json').read_text()))
 r=[0]*n
 for c in source.customers:r[sum(1<<a for a in c.topics)-1]=c.multiplicity
 best=r[:];bestval=eng.solve(r);value=bestval;records=[];started=time.time()
 for it in range(args.rounds):
  if it%300==0:r=best[:];value=eng.solve(r)
  prop=r[:]
  if rng.random()<.85:
   support=[j for j,v in enumerate(prop)if v];j=rng.choice(support)if support and rng.random()<.9 else rng.randrange(n)
   prop[j]=max(0,min(200,prop[j]+rng.choice((-3,-2,-1,1,2,3))))
  else:
   for j in rng.sample(range(n),rng.randint(1,3)):prop[j]=max(0,min(200,prop[j]+rng.choice((-2,-1,1,2))))
  if not any(prop):continue
  new=eng.solve(prop);temp=.01*(1-(it%300)/300)
  if new<=value or rng.random()<math.exp(-float(new-value)/max(temp,.0001)):r,value=prop,new
  if new<bestval:
   bestval,best=new,prop[:]
   ins=eng.instance(best);dp=MyopicCeilingFloor(ins);replay=dp.root()/ins.optimal_welfare();assert replay==new
   rec={'iteration':it,'ratio':str(new),'G':str(dp.root()),'OPT':ins.optimal_welfare(),'instance':ins.to_dict()};records.append(rec)
   print(json.dumps({k:v for k,v in rec.items()if k!='instance'}),flush=True)
   if new<F(1,2):break
 report={'scope':'finite exact search of a DP payment bridge, not a SPE counterexample','m':args.m,'p':args.p,'rounds_requested':args.rounds,'rounds_done':it+1,'seconds':time.time()-started,'best_ratio':str(bestval),'improvements':records,'best_instance':eng.instance(best).to_dict()}
 Path(__file__).with_name(f'myopic_directed_m{args.m}p{args.p}.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ('improvements','best_instance')}))

if __name__=='__main__':main()
