"""Discovery only: alternating query/signed-potential LP in complete ordered SPE cones."""
import itertools,numpy as np,json,argparse,time
from scipy.optimize import linprog

def run(seed,n,k,steps):
 rng=np.random.default_rng(seed);profiles=list(itertools.combinations_with_replacement(range(k),n));backs=list(itertools.combinations_with_replacement(range(k),n-1));ix={s:i for i,s in enumerate(profiles)};ib={s:i+len(ix) for i,s in enumerate(backs)};K=len(ix)+len(ib)
 def ur(a,b):
  z=np.zeros(K);z[ix[tuple(sorted((*b,a)))]]=1;z[ib[tuple(sorted(b))]]=-1;return z
 phi=rng.uniform(-1,1,K);acts={}
 def end(h):
  while len(h)<n:h+=(acts[h],)
  return h
 for depth in reversed(range(n)):
  for h in itertools.product(range(k),repeat=depth):
   vals=[]
   for a in range(k):
    zz=end(h+(a,));vals.append(ur(a,zz[:depth]+zz[depth+1:])@phi)
   acts[h]=int(np.argmax(vals))
 z=end(());pay=np.array([ur(a,z[:i]+z[i+1:])for i,a in enumerate(z)]);W=pay.sum(0);G=[]
 for h,a0 in acts.items():
  zz=end(h);v=ur(a0,zz[:len(h)]+zz[len(h)+1:])
  for a in range(k):
   za=end(h+(a,));G.append(v-ur(a,za[:len(h)]+za[len(h)+1:]))
 G=np.array(G);menus=set()
 for i in range(n):
  for a in range(k):
   zz=end(z[:i]+(a,));menus.add(tuple(sorted(zz[:i]+zz[i+1:])))
 menus=sorted(menus);R=np.array([[ur(a,b)for a in range(k)]for b in menus])
 best=-100
 for step in range(steps):
  mat=R@phi
  pq=linprog(np.r_[np.zeros(k),-1],A_ub=np.c_[-mat,np.ones(len(menus))],b_ub=np.zeros(len(menus)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
  q=pq.x[:-1];M=np.einsum('i,bik->bk',q,R)
  lp=linprog(np.r_[W/n,-1],A_ub=np.vstack([np.c_[-G,np.zeros(len(G))],np.c_[-M,np.ones(len(M))]]),b_ub=np.zeros(len(G)+len(M)),bounds=[(-1,1)]*K+[(None,None)],method='highs')
  gap=-lp.fun;phi=lp.x[:-1];best=max(best,gap)
  if gap>1e-8:
   return {'seed':seed,'n':n,'topics':k,'step':step,'gap':gap,'path':z,'query':q.tolist(),'menus':menus,'phi':phi.tolist(),'profiles':profiles,'backs':backs,'payoffs':(pay@phi).tolist(),'actions':[(h,a)for h,a in acts.items()]}
 return None
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=3);ap.add_argument('--topics',type=int,default=3);ap.add_argument('--seeds',type=int,default=300);ap.add_argument('--steps',type=int,default=6);ap.add_argument('--output',required=True);a=ap.parse_args();start=time.time();candidate=None
 for seed in range(a.seeds):
  candidate=run(seed,a.n,a.topics,a.steps)
  if candidate:break
 result={'tested_seeds':seed+1,'seconds':time.time()-start,'candidate':candidate};json.dump(result,open(a.output,'w'),indent=2);print(json.dumps(result))
