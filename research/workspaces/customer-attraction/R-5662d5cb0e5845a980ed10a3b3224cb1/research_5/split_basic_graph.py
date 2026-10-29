"""Keep diagonal/offdiagonal basic rows separate in the exact shared reply graph."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,sys,time
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
sys.path.insert(0,str(OLD))
import attractive_nested as an
import new_reply_budget as nr
import actual_fifth_nested as nest
import full_new_reply_closure as cl
SPLIT=[(stage,diag,n) for stage,ns in (('R',nr.NAMES),('Z',nest.BASIC)) for diag in (0,1) for n in ns]
SI={x:i for i,x in enumerate(SPLIT)}

def build():
 old=json.loads((OLD/'attractive_nested_exact.json').read_text());histcols=[c for c in old['columns'] if c['kind']=='hist']
 cols,names,m,obj,norm=an.build(histcols);extra=[[F()]*len(cols) for _ in SPLIT]
 byhist={};hi=None
 for j,c in enumerate(cols):
  if c['kind']=='hist':hi=j;byhist[hi]={}
  elif c['kind']=='joint-reply':
   f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));byhist[hi].setdefault(g,{})[tuple(c['state'])]=j
 for hi,gs in byhist.items():
  c=cols[hi];a=tuple(map(int,c['actual_bits']));p=sum(a[:3]);pa=sum(a[:4]);ell=sum(a[:5]);whole=sum(a)
  words=[w for w,n in zip(nr.PAT,c['hist']) for _ in range(n)];nb=sum(w[1] for w in words);nc=sum(w[2] for w in words)
  for i,j in product(range(6),repeat=2):
   wi=words[i];wj=words[j];t,b,cc=wi;y=wj[2];diag=int(i==j);g=(1,diag,wi,wj);den=p+t+y+1
   def values(r,z):
    vals=[nr.share(b,p+t+b+cc)-nr.share(y,p+t+y+r)]
    vals += [nr.share(r,den)-F(q,den) for q in (b,cc,t,F(c['d'],6),*a,F(nb,6),F(nc,6))]
    vals += [nr.share(cc,p+t+b+cc)-F(r,p+t+b+1),nr.share(a[5],whole)-F(r,ell+1),-F(r)]
    ha=nr.share(a[4]+a[5],whole)+F(a[4],(pa+1)*(pa+2));vz=nr.share(z,pa+r+z)
    zs=[nr.share(a[4],whole)-nr.share(r,pa+r+z),ha-F(r+z,pa+1)+F(r*z,(pa+1)*(pa+2)),nr.share(a[5],whole)-F(z,ell+1),-F(z)]
    zs += [vz-F(q,pa+r+1) for q in a]
    zs += [vz-F(r,pa+r+1),F(r-z,den)]
    return {**{SI['R',diag,n]:v for n,v in zip(nr.NAMES,vals)},**{SI['Z',diag,n]:v for n,v in zip(nest.BASIC,zs)}}
   zero=values(0,0)
   for row,v in zero.items():extra[row][hi]+=v
   for st,col in gs[g].items():
    for row,v in values(*st).items():extra[row][col]+=v-zero[row]
 for stage,ns in (('R',nr.NAMES),('Z',nest.BASIC)):
  for diag,count in ((0,30),(1,6)):extra[SI[stage,diag,'capacity']][0]=F(count)
 # Exact consistency: two split rows reproduce every original f1 basic row.
 nbase=702+nr.NW+len(cl.EXTRA_NAMES)
 for n in nr.NAMES:
  oldrow=702+5+nr.NF+nr.NAMES.index(n)
  assert [x+y for x,y in zip(extra[SI['R',0,n]],extra[SI['R',1,n]])]==m[oldrow],('R',n)
 for n in nest.BASIC:
  oldrow=nbase+nest.NI['basic',1,n]
  assert [x+y for x,y in zip(extra[SI['Z',0,n]],extra[SI['Z',1,n]])]==m[oldrow],('Z',n)
 return cols,names+list(map(str,SPLIT)),m+extra,obj,norm

def main():
 start=time.time();cols,names,m,obj,norm=build();print('built',len(m),'rows',len(cols),'cols',time.time()-start,flush=True)
 if '--verify' in sys.argv:
  x=json.loads((HERE/'split_basic_exact.json').read_text());ys=[F(c['weight']) for c in x['columns']];slacks=[sum(v*y for v,y in zip(row,ys)) for row in m]
  assert min(ys)>=0 and min(slacks)>=0 and sum(v*y for v,y in zip(norm,ys))==1
  w=sum(v*y for v,y in zip(obj,ys));assert w==F(x['W']) and w<F(1,2)
  print({'rows':len(m),'min':str(min(slacks)),'W':str(w)});return
 a=np.array([[float(x) for x in row] for row in m]);scale=np.max(abs(a),axis=1);scale[scale==0]=1
 sol=linprog([float(x) for x in obj],A_ub=-a/scale[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(x) for x in norm]],b_eq=[1],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
 report={'scope':'16-histogram support necessary graph, not SPE or full-domain infeasibility','success':bool(sol.success),'status':sol.message,'W':sol.fun,'rows':len(m),'columns':len(cols),'seconds':time.time()-start}
 print(json.dumps(report,indent=2),flush=True)
 if sol.success and sol.fun<.5:
  exact=cl.exact_point(cols,names,m,obj,norm,sol.x);exact['scope']='exact feasible shared-reply necessary graph point after all f1 basic diagonal splits; not SPE or game';exact['additional_split_rows']=len(SPLIT)
  (HERE/'split_basic_exact.json').write_text(json.dumps(exact,indent=2)+'\n');report['exact_verified']=True
 (HERE/'split_basic_status.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
