"""Integer-scaled exact continuation thresholds, with exploratory mutations.

This independent implementation caches SETS of outcomes, never one Markov policy.
Final candidates are checked by the normative Fraction solver separately.
"""
import itertools,math,random,json,argparse,time
from pathlib import Path
import numpy as np

class Geometry:
 def __init__(self,m,p):
  self.m=m;self.p=p;self.L=math.lcm(*range(1,m+1));self.masks=range(1,1<<p)
  self.states=[]
  for t in range(m,-1,-1):
   for actions in itertools.combinations_with_replacement(range(p),t):
    k=tuple(actions.count(a) for a in range(p));self.states.append(k)
  self.index={k:i for i,k in enumerate(self.states)}
  self.term=[k for k in self.states if sum(k)==m];self.T=len(self.term)
  self.children=[tuple(self.index[k[:a]+(k[a]+1,)+k[a+1:]] for a in range(p)) if sum(k)<m else () for k in self.states]
  self.coeff=np.zeros((p,self.T,(1<<p)-1),dtype=np.int64)
  self.cover=np.zeros((self.T,(1<<p)-1),dtype=np.int64)
  for j,c in enumerate(self.term):
   for mask in self.masks:
    load=sum(c[a] for a in range(p) if mask>>a&1)
    if load:
     self.cover[j,mask-1]=1
     for a in range(p):
      if c[a] and mask>>a&1:self.coeff[a,j,mask-1]=self.L//load
 def run(self,w,details=False):
  U=np.dot(self.coeff,w); welfare=np.dot(self.cover,w);R=[];M=[];Q=[];paths=[]
  for j,ch in enumerate(self.children):
   if not ch:
    R.append((j,));M.append(0);Q.append(0);paths.append(())
   else:
    floor=max(min(U[a,t] for t in R[ch[a]]) for a in range(self.p))
    outcomes=set(t for a in range(self.p) for t in R[ch[a]] if U[a,t]>=floor)
    R.append(tuple(outcomes));M.append(int(floor));a=min(range(self.p),key=lambda a:Q[ch[a]])
    Q.append(int(floor)+Q[ch[a]]);paths.append((a,)+paths[ch[a]])
  opt=int(max(welfare));total=Q[-1]
  if details:return {'scaled_threshold_total':total,'scale':self.L,'optimum':opt,'ratio':f'{total}/{self.L*opt}','path':paths[-1], 'thresholds':[M[self.index[tuple(paths[-1][:t].count(a) for a in range(self.p))]] for t in range(self.m)],'minimum_spe_welfare':int(min(welfare[t] for t in R[-1]))}
  return total/(self.L*opt) if opt else 1

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=5);ap.add_argument('--topics',type=int,default=7);ap.add_argument('--steps',type=int,default=3000);ap.add_argument('--seed',type=int,default=20261021);ap.add_argument('--output',required=True);ap.add_argument('--input');args=ap.parse_args()
 rng=random.Random(args.seed);g=Geometry(args.players,args.topics);w=np.zeros((1<<g.p)-1,dtype=np.int64)
 if args.input:
  raw=json.loads(Path(args.input).read_text());raw=raw.get('instance',raw)
  assert raw['players']==g.m and len(raw['topics'])==g.p
  for c in raw['customers']:w[sum(1<<a for a in c['topics'])-1]+=c.get('multiplicity',1)
 else:
  w[0]=10*g.m
  for a in range(1,min(g.p,g.m)):w[(1<<a)-1]=10
 best=g.run(w);current=best;bestw=w.copy();print('initial',best,flush=True)
 for step in range(args.steps):
  nw=w.copy();mask=rng.randrange(1,1<<g.p);delta=rng.choice([-3,-2,-1,1,2,3]);nw[mask-1]=max(0,nw[mask-1]+delta)
  ratio=g.run(nw);temp=.001*(1-step/args.steps)
  if ratio<=current or rng.random()<math.exp(min(0,(current-ratio)/max(temp,1e-9))):w=nw;current=ratio
  if ratio<best:
   best=ratio;bestw=nw.copy();record={'status':'exploratory exact integer-scale, not an SPE counterexample','parameters':vars(args),'step':step,'instance':{'topics':list(map(str,range(g.p))),'players':g.m,'customers':[{'topics':[a for a in range(g.p) if mask>>a&1],'multiplicity':int(nw[mask-1])} for mask in g.masks if nw[mask-1]]},**g.run(nw,True)}
   Path(args.output).write_text(json.dumps(record,indent=2)+'\n');print(step,best,record['thresholds'],record['minimum_spe_welfare'],flush=True)
   if best<.5:break
 print('done',best,flush=True)
if __name__=='__main__':main()
