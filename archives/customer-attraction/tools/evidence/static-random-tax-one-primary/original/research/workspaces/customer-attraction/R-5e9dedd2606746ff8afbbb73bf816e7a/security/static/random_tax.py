exec(open(__file__.replace('random_tax.py','tax_probe.py')).read().split("if __name__")[0])
import random,time
rng=random.Random(19211)
def policy(w):
  sig={}
  @lru_cache(None)
  def end(h):
    if len(h)==n:return h
    ez=[end(h+(a,)) for a in range(k)]
    uv=[sum(w.get(M,0)*coef(a,z,M) for M in masks) for a,z in enumerate(ez)]
    # preference high root coverage (sometimes ties random)
    best=max(range(k),key=lambda a:(uv[a],rng.random()))
    sig[h]=best;return ez[best]
  end(())
  return sig
start=time.time()
for it in range(100):
  if it%2==0:
    ww={M:rng.randrange(1,10) for M in rng.sample(masks,rng.randrange(8,25))}
  else:
    ww={1:4,2:1,4:1,8:1}
    for M in rng.sample(masks,rng.randrange(2,15)):ww[M]=rng.randrange(1,10)
  sig=policy(ww)
  (f,cc,w),z,g=optimize(sig)
  print(it,round(-f,9),cc,z,round(time.time()-start,2),flush=True)
  if f < -1e-8:
    ws={M:F(float(x)).limit_denominator(1000000) for M,x in zip(masks,w) if x>1e-8}
    den=math.lcm(*(x.denominator for x in ws.values()));wi={M:int(x*den) for M,x in ws.items()}
    vals=[sum(row[masks.index(M)]*v for M,v in wi.items()) for row in g]
    print('FOUND',wi,min(vals),flush=True)
    json.dump({'n':n,'k':k,'weights':wi,'sigma':{','.join(map(str,h)):a for h,a in sig.items()},'comparator':cc,'root':z},open(__file__.replace('random_tax.py','tax_candidate.json'),'w'))
    break
