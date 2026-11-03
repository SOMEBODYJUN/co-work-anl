"""Local vectorization guard for structurally zero histogram cells.

Copied only the upstream aligned_rows function. For vector batches, t=0,d=5
and t=1,d=0 have zero cell count; clamp their unused lookup indices. Exact
scalar evaluation on all realizable positive cells is unchanged.
"""
from aligned_root_pricing import *

def aligned_rows_safe(hist,exact=True,bits=None):
 Q=base.EX['q'] if exact else base.VE['q']
 def sm(fn):return sum((n*fn(*map(int,ty)) for n,ty in zip(hist,TYPES) if (not exact or n)),F() if exact else 0)
 d=sm(lambda t,x,y,z,k:t)
 if exact:cov=int(d>0)
 else:cov=np.asarray(d>0,dtype=int)
 share={m:sm(lambda *tt:Q(tt[i],sum(tt))) for i,m in enumerate(RPOS)}
 count={m:sm(lambda *tt:tt[i]) for i,m in enumerate(RPOS)}
 out={}
 out['Root:aligned:r4']=1499*sum(share[m] for m in RPOS[1:])-3000*cov
 out['Root:aligned:r4-binary']=6*sum(share[m] for m in RPOS[1:])+share['T']-d-12*cov
 out['Root:aligned:r4-binary1999']=5997*sum(share[m] for m in RPOS[1:])+997*share['T']-997*d-12000*cov
 for v,table in enumerate(TABLES):
  def residual(t,x,y,z,k):
   vv=table[''.join(map(str,(t,x,y,z,k)))];e=d-t
   return vv[int(e)] if exact else np.take(np.asarray(vv,dtype=float),np.clip(np.asarray(e,dtype=int),0,len(vv)-1))
  aa=F(2) if v==0 else F(1999,1000)
  def value(t,x,y,z,k):
   beta=F(5,3) if t else aa
   return (beta if exact else float(beta))*Q(x+y+z+k,t+x+y+z+k)-residual(t,x,y,z,k)
  out[f'Root:aligned:r4-pareto{v}']=sm(value)-4*cov
 def g4(p,c):return Q(c*(c-1),p+c-1)+Q((5-c)*c,p+c)
 for m,cc in count.items():
  out[f'Root:aligned:r4-binary-menu:{m}']=29985*sum(share[z] for z in RPOS[1:])+4985*share['T']-4985*d-3000*sm(lambda t,x,y,z,k:g4(t,cc))
 b=list(map(int,bits)) if bits is not None else [0]*10
 ld=sum(b[:5]);u1=Q(b[0],ld);tail=Q(sum(b[1:5]),ld)
 out['Root:aligned:actual4-binary']=29985*tail-4985*(b[0]-u1)-3000*g4(b[0],d)
 r0=list(map(F,['0','0','1/750','1/1500','1/1500','39/500','1/1000','623/3000','2747/12000','691/6000','47/1500','1919/12000','0','77/750','1/4000','1169/6000']))
 r1=list(map(F,['0','133/750','2003/12000','61853/180000','251/3000','6331/22500','7363/36000','26047/60000','239/1200','14579/45000','22183/90000','5177/12000','15767/90000','63893/180000','43349/180000','41143/90000']))
 out['Root:aligned:r4-credit']=2998*sum(share[m] for m in RPOS[1:])-6000*cov-sm(lambda t,x,y,z,k:1500*(r1 if t else r0)[8*x+4*y+2*z+k])
 # At branch (T_i,X_i), compare all four triples chosen from T_{-i}.
 def g3(p,c):return Q(c*(4-c)*(3-c)/2,p+1)+Q(c*(c-1)*(4-c),p+2)+Q(c*(c-1)*(c-2)/2,p+3)
 # c=d-t is fixed conditional on a histogram. Closure handles d as vector.
 out['Root:aligned:r3']=20*sum(share[m] for m in RPOS[2:])-3*sm(lambda t,x,y,z,k:g3(t+x,d-t))
 H=share['Z']+share['K']+sm(lambda t,x,y,z,k:Q(z,(t+x+y+1)*(t+x+y+2)))
 out['Root:aligned:r2']=6*H-sm(lambda t,x,y,z,k:Q((d-t)*(4-d+t),t+x+y+1)+Q((d-t)*(d-t-1),t+x+y+2))
 for i in range(1,5):
  sh=share[RPOS[i]]
  out[f'Root:aligned:opt:{i}']=4*sh-sm(lambda *tt:Q(d-tt[0],sum(tt[:i])+5-i))
  for j,m in enumerate(RPOS[1:],1):
   de=sm(lambda *tt:Q(1,sum(tt[:i])+5-i))
   own=sm(lambda *tt:Q(tt[j],sum(tt[:i])+5-i))
   out[f'Root:aligned:menu:{i}:{m}']=4*sh-count[m]*de+own
 return out
