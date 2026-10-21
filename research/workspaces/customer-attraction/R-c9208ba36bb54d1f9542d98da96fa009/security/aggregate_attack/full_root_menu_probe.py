"""Discovery: freely mixed full root terminals as r-opponent extra-one dual."""
from pathlib import Path
exec(open(Path(__file__).with_name('extra_integer_probe.py')).read().split("out={'scope'")[0])
def run_menu(n,k,bg,w):
 M,sunk,R0,scale=base.representation(n,k,bg)
 actions,G,pair,actual=base.policy_cone(n,k,M,sunk,scale,w,rng)
 def term(h):
  while len(h)<n:h+=(actions[h],)
  return tuple(h.count(a) for a in range(k))
 h=np.array(term(()))@M
 root=M[actual[0]]/np.maximum(sunk+h,1)
 Bs=np.array([term((a,)) for a in range(k)])
 R=1/(1+sunk+Bs@M)
 starts=[base.security(w,M,R)[0],np.ones(k)/k]
 best=None
 for p in starts:
  old=0.
  for j in range(8):
   nw,v=base.cone_step(G,root,M,R,p)
   p,v=base.security(nw,M,R)
   if best is None or v>best['ratio']:
    best={'ratio':float(v),'n':n,'k':k,'background':bg,'actual':actual,'weights':nw.tolist(),'p':p.tolist(),'menu':Bs.tolist(),'actions':{','.join(map(str,h)):int(a) for h,a in actions.items()}}
   if v>1+1e-7 or v<old+1e-9:break
   old=v
 return best
out={'scope':'finite float discovery only','completed':0,'best':None}
for i in range(150):
 n,k=rng.choice([(3,6),(3,7),(4,5),(4,6)])
 bg=[0]*k
 if i%3:
  for _ in range(rng.choice([1,2,4,8])):bg[rng.randrange(k)]+=1
 w=np.array([rng.randrange(1,20) if rng.random()<rng.choice([.2,.5,1.]) else 0 for mask in range(1,1<<k)])
 z=run_menu(n,k,bg,w)
 if out['best'] is None or z['ratio']>out['best']['ratio']+1e-8:
  out['best']=z;print(i,z['ratio'],n,k,bg,flush=True)
 out['completed']=i+1
 if i%10==0 or z['ratio']>1+1e-7:Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
 if z['ratio']>1+1e-7:break
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
