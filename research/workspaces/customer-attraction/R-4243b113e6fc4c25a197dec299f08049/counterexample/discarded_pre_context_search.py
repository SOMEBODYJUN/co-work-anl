import itertools, numpy as np, random, functools, time

def comps(t,r):
 if r==1: yield (t,); return
 for k in range(t+1):
  for x in comps(t-k,r-1): yield (k,)+x

class Game:
 def __init__(self,r,m):
  self.r=r;self.m=m
  self.C=[list(comps(t,r)) for t in range(m+1)]
  self.ID=[{c:i for i,c in enumerate(cs)} for cs in self.C]
  self.patterns=np.array([[int(p>>i&1) for i in range(r)] for p in range(1,2**r)],dtype=float)
  final=np.array(self.C[m]);cover=final@self.patterns.T
  self.coeff=np.array([np.divide(self.patterns[:,i],cover,out=np.zeros_like(cover),where=cover>0) for i in range(r)])
  self.welfare=(cover>0).astype(float)
  self.next=[]
  for t in range(m):
   self.next.append(np.array([[self.ID[t+1][c[:a]+(c[a]+1,)+c[a+1:]] for a in range(r)] for c in self.C[t]]))
  # Optimizer at most m topics = final multisets
 def solve(self,w, witness=False):
  u=self.coeff@w; wf=self.welfare@w
  O=[{i} for i in range(len(self.C[self.m]))]
  if witness: allO=[None]*(self.m+1); allO[self.m]=O
  for t in reversed(range(self.m)):
   P=[]
   for cc,nxt in zip(self.C[t],self.next[t]):
    Q=[O[j] for j in nxt]
    threshold=max(min(u[a,list(q)]) for a,q in enumerate(Q))
    outs=set()
    for a,q in enumerate(Q):
     outs.update(z for z in q if u[a,z]>=threshold-1e-8)
    P.append(outs)
   O=P
   if witness: allO[t]=O
  worst=min(O[0],key=lambda z:wf[z]); opt=max(wf)
  if witness:return opt/wf[worst],self.C[self.m][worst],wf[worst],opt,allO,u
  return opt/wf[worst]

if __name__=='__main__':
 r=int(__import__('sys').argv[1]);m=int(__import__('sys').argv[2]);g=Game(r,m)
 best=1;start=time.time()
 for k in range(100000):
  # sparse large varying weights
  w=np.random.randint(0,25,size=2**r-1)*np.random.binomial(1,0.3,size=2**r-1)
  if not w.any():continue
  ratio=g.solve(w)
  if ratio>best+1e-8:
   best=ratio;print(k,'best',best,'w',w.tolist(), 'result',g.solve(w,True)[:4],flush=True)
  if ratio>2+1e-8:break
  if k%100==0 and time.time()-start>50: break
 print('DONE',k,best,flush=True)
