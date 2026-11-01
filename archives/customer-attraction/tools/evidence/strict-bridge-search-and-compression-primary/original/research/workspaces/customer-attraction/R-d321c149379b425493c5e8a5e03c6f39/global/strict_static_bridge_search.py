"""Finite discovery: tie-free SPE versus all static PNE, exact integer arithmetic."""
from pathlib import Path
import itertools,json,random,argparse
import numpy as np

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--trials',type=int,default=100000);ap.add_argument('--p',type=int,default=5);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 p=a.p;m=3;r=random.Random(31415927)
 mem=np.array([[(b>>j)&1 for b in range(1,1<<p)] for j in range(p)],dtype=np.int64)
 qs=sorted(set(tuple(s.count(j) for j in range(p)) for s in itertools.product(range(p),repeat=m)))
 qi={q:i for i,q in enumerate(qs)}
 den=np.array(qs)@mem
 coeff=np.zeros((len(qs),p,len(mem[0])),dtype=np.int64)
 for i,q in enumerate(qs):
  for j in range(p):
   if q[j]:coeff[i,j]=mem[j]*np.where(den[i]>0,6//np.maximum(den[i],1),0)
 cov=(den>0).astype(np.int64)
 strict_count=0
 for trial in range(a.trials):
  w=np.array([r.randrange(1,10000) for _ in range(1,1<<p)],dtype=np.int64)
  us=coeff@w;ws=cov@w;actions={};strict=True
  def solve(h):
   nonlocal strict
   if len(h)==m:return qi[tuple(h.count(j) for j in range(p))]
   kid=[solve(h+(j,)) for j in range(p)];vals=[int(us[kid[j],j]) for j in range(p)];mx=max(vals)
   if vals.count(mx)>1:strict=False
   chosen=vals.index(mx);actions[h]=chosen
   return kid[chosen]
  actual=solve(())
  if not strict:continue
  strict_count+=1
  pne=[]
  for k,q in enumerate(qs):
   ok=True
   for j in range(p):
    if not q[j]:continue
    for t in range(p):
     qq=list(q);qq[j]-=1;qq[t]+=1
     if us[qi[tuple(qq)],t]>us[k,j]:ok=False;break
    if not ok:break
   if ok:pne.append(k)
  minp=min(ws[k] for k in pne)
  if minp>ws[actual]:
   out={'status':'exact finite discovery; full independent audit pending','seed':31415927,'trial':trial,'strict_count':strict_count,'p':p,'m':m,'weights':{str(i+1):int(x) for i,x in enumerate(w)},'actual':qs[actual],'W':int(ws[actual]),'minimum_pne_W':int(minp),'pne':[{'counts':qs[k],'W':int(ws[k])} for k in pne],'actions':[{'history':h,'action':v} for h,v in sorted(actions.items())]}
   a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True);return
  if trial%10000==0:print(trial,strict_count,flush=True)
 a.output.write_text(json.dumps({'status':'finite no discovery','trials':a.trials,'strict_count':strict_count,'p':p,'m':m},indent=2)+'\n')
 print('no discovery',a.trials,strict_count)
if __name__=='__main__':main()
