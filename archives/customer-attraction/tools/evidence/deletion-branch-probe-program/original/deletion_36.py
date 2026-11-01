exec(open(__file__.replace('deletion_36.py','tax_probe.py')).read().split("if __name__")[0])
import random,time
sys.path.insert(0,'.')
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
rng=random.Random(31289)
def makepolicy(w):
  ins=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if (M>>a)&1),v) for M,v in w.items()),n)
  sol=ExactSPESolver(ins)
  target=min(sol.outcomes(),key=ins.welfare)
  return sol.certificate(target,action_selector=lambda h,aa:rng.choice(aa),continuation_selector=lambda h,cc:rng.choice(cc)).actions
start=time.time()
for it in range(1):
  ww={M:rng.randrange(1,8) for M in rng.sample(masks,rng.randrange(6,24))}
  n=3
  def aa(h):
    if not h:return 0
    if len(h)==1:return 3 if h[0]<3 else 0
    group=range(3) if h[1]<3 else range(3,6)
    return next(a for a in group if a not in h)
  sig={h:aa(h) for d in range(n) for h in product(range(k),repeat=d)}
  @lru_cache(None)
  def end(h):return h if len(h)==n else end(h+(sig[h],))
  z0=end(())
  gam=[]
  for h,a0 in sig.items():
    z=end(h)
    for a in range(k):gam.append([coef(a0,z,M)-coef(a,end(h+(a,)),M) for M in masks]+[F(0)])
  c=[F(int(any((M>>a)&1 for a in z0))) for M in masks]
  # fixed query distributions (pure, uniform pairs, uniform all)
  pp=[{a:F(1)} for a in range(k)]+[{a:F(1,2),b:F(1,2)} for a,b in combinations(range(k),2)]+[{a:F(1,k) for a in range(k)}]
  best=(-1e9,None)
  for p in pp:
    ub=[[-x for x in row] for row in gam]
    for i in range(n):
      zz=z0[:i]+z0[i+1:]
      ub.append([-sum(v*coef(a,zz+(a,),M) for a,v in p.items()) for M in masks]+[F(1)])
    res=linprog(np.array(c+[-(n-F(1,2))],float),A_ub=np.array(ub,float),b_ub=np.zeros(len(ub)),A_eq=np.array([[F(1)]*len(masks)+[F(0)]],float),b_eq=[1],bounds=[(0,None)]*(len(masks)+1),method='highs')
    if res.success and -res.fun>best[0]:best=(-res.fun,(p,res.x))
  print(it,best[0],z0,round(time.time()-start,1),flush=True)
  if best[0]>1e-8:
    p,w=best[1]
    ws={M:F(float(x)).limit_denominator(1000000) for M,x in zip(masks,w) if x>1e-8}
    den=math.lcm(*(x.denominator for x in ws.values()));wi={M:int(x*den) for M,x in ws.items()}
    vals=[sum(row[masks.index(M)]*v for M,v in wi.items()) for row in gam]
    print('FOUND',p,wi,'mingamma',min(vals),flush=True)
    json.dump({'n':n,'k':k,'weights':wi,'sigma':{','.join(map(str,h)):a for h,a in sig.items()},'p':{a:str(v) for a,v in p.items()},'root':z0},open(__file__.replace('deletion_probe.py','deletion_candidate.json'),'w'))
    break
