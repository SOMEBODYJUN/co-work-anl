exec(open(__file__.replace('worst_tax.py','tax_probe.py')).read().split("if __name__")[0])
import random,time
sys.path.insert(0,'.')
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
rng=random.Random(72892)
start=time.time()
for it in range(80):
  if it%3==0:
    ww={M:rng.randrange(1,5) for M in rng.sample(masks,rng.randrange(5,18))}
  elif it%3==1:
    ww={1:4,2:1,4:1,8:1}
    for M in rng.sample(masks,rng.randrange(2,10)):ww[M]=rng.randrange(1,4)
  else:
    ww={1:12,2:8,4:4,8:8,17:6,33:6,20:3,36:3,49:6,50:2,52:1,56:2}
    for M in rng.sample(masks,rng.randrange(2,8)):ww[M]=rng.randrange(1,4)
  ins=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if (M>>a)&1),v) for M,v in ww.items()),n)
  sol=ExactSPESolver(ins)
  def score(q):
    return sum(v*(int((d:=sum(q[a] for a in range(k) if (M>>a)&1))>0)+F(d,d+1)) for M,v in ww.items())
  target=min(sol.outcomes(),key=score)
  sig=sol.certificate(target,action_selector=lambda h,aa:rng.choice(aa),continuation_selector=lambda h,cc:rng.choice(cc)).actions
  (f,cc,w),z,g=optimize(sig)
  print(it,round(-f,9),cc,z,len(sol.outcomes()),round(time.time()-start,2),flush=True)
  if f < -1e-8:
    ws={M:F(float(x)).limit_denominator(1000000) for M,x in zip(masks,w) if x>1e-8}
    den=math.lcm(*(x.denominator for x in ws.values()));wi={M:int(x*den) for M,x in ws.items()}
    vals=[sum(row[masks.index(M)]*v for M,v in wi.items()) for row in g]
    print('FOUND',wi,min(vals),flush=True)
    json.dump({'n':n,'k':k,'weights':wi,'sigma':{','.join(map(str,h)):a for h,a in sig.items()},'comparator':cc,'root':z},open(__file__.replace('worst_tax.py','tax_candidate.json'),'w'))
    break
