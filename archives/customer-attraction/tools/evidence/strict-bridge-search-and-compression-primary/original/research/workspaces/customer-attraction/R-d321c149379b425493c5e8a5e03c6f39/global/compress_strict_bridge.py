"""MILP discovery only; chosen strict SPE and static profitable witnesses frozen."""
from pathlib import Path
import json,itertools,argparse
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--positive',action='store_true');a=ap.parse_args();src=json.loads(a.input.read_text());p=src['p'];m=src['m']
 masks=list(range(1,1<<p));mem=np.array([[(b>>j)&1 for b in masks] for j in range(p)],dtype=np.int64);w=np.array([src['weights'].get(str(b),0) for b in masks]);actions={tuple(x['history']):x['action'] for x in src['actions']}
 qs=sorted(set(tuple(s.count(j) for j in range(p)) for s in itertools.product(range(p),repeat=m)));qi={q:i for i,q in enumerate(qs)};den=np.array(qs)@mem;coeff=np.zeros((len(qs),p,len(masks)),dtype=np.int64)
 for i,q in enumerate(qs):
  for j in range(p):
   if q[j]:coeff[i,j]=mem[j]*np.where(den[i]>0,6//np.maximum(den[i],1),0)
 cov=(den>0).astype(np.int64);terminal={}
 def walk(h):
  if len(h)==m:out=qi[tuple(h.count(j) for j in range(p))]
  else:
   for j in range(p):walk(h+(j,))
   out=terminal[h+(actions[h],)]
  terminal[h]=out;return out
 actual=walk(());rows=[];labels=[];lower=[]
 for h,c in sorted(actions.items()):
  for j in range(p):
   if j!=c:rows.append(coeff[terminal[h],c]-coeff[terminal[h+(j,)],j]);lower.append(1);labels.append(['spe',h,j])
 pne=tuple(src['pne'][0]['counts']);pk=qi[pne]
 for k,q in enumerate(qs):
  static=[]
  for j in range(p):
   if not q[j]:continue
   for b in range(p):
    if b==j:continue
    qq=list(q);qq[j]-=1;qq[b]+=1
    static.append((coeff[k,j]-coeff[qi[tuple(qq)],b],j,b))
  if k==pk:
   for row,j,b in static:rows.append(row);lower.append(0);labels.append(['pne',q,j,b])
  else:
   row,j,b=min(static,key=lambda t:int(t[0]@w));assert row@w<0
   rows.append(-row);lower.append(1);labels.append(['notpne',q,j,b])
 rows.append(cov[pk]-cov[actual]);lower.append(1);labels.append(['welfaregap'])
 ans=milp(np.ones(len(masks)),integrality=np.ones(len(masks)),bounds=Bounds(np.ones(len(masks)) if a.positive else np.zeros(len(masks)),np.full(len(masks),np.inf)),constraints=LinearConstraint(np.array(rows),np.array(lower),np.full(len(rows),np.inf)),options={'time_limit':60,'mip_rel_gap':0.0})
 out={'status':'MILP discovery; exact audit pending','solver_message':ans.message,'success':bool(ans.success),'objective':float(ans.fun) if ans.fun is not None else None,'input':str(a.input),'p':p,'m':m,'actions':src['actions'],'chosen_pne':pne,'positive_types_required':a.positive,'witnesses':labels}
 if ans.x is not None:out['weights']={str(b):int(round(v)) for b,v in zip(masks,ans.x) if round(v)>0};out['minimum_integer_margin']=int(min(np.array(rows)@np.rint(ans.x).astype(np.int64)-np.array(lower)))
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
