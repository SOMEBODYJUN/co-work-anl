"""All actual strong PAIR(R,Z), PAIR(Z,Z) on fixed threshold R support.
Z-Z overlaps have only nonnegative coefficients; nested Z within each R slab
realizes their pairwise maxima simultaneously, preserving all earlier rows.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
import sys,json,time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
TARGET='pair_master' if '--master' in sys.argv else ('pair_cross' if '--cross' in sys.argv else 'pair_closure')
# Freeze the strengthened diagonal-split point.
if '--split' not in sys.argv:sys.argv.append('--split')
import zz_threshold_closure as zz
import full_new_reply_closure as cl
import new_reply_budget as nr
PAIR=[(kind,f,g,pat) for kind,f,g,pat in product(('RZ','ZZ'),range(2),range(2),cl.P4)]
PI={x:i for i,x in enumerate(PAIR)}

def build():
 old,vs,bounds,names,rows,bs,cols,base,mapping=zz.build();nz=len(vs)
 slabs={}
 for j,v in enumerate(vs):
  key=(v['hist_column'],v['left'],v['right']);f,d,wi,wj=v['group'];g=(f,d,tuple(wi),tuple(wj));slabs.setdefault(key,{})[g]=j
 overlaps={}
 for key,gs in slabs.items():
  for j,k in combinations(sorted(gs.values()),2):overlaps[key,j,k]=nz+len(overlaps)
 new=[{} for _ in PAIR];nb=[F() for _ in PAIR]
 for key,gs in slabs.items():
  hi,left,right=key;mass=F(right)-F(left);c=cols[hi];a=tuple(map(int,c['actual_bits']));pa=sum(a[:4]);whole=sum(a);D=(pa+1)*(pa+2)
  ha=nr.share(a[4]+a[5],whole)+F(a[4],D)
  words=[w for w,n in zip(nr.PAT,c['hist']) for _ in range(n)]
  edges=[(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
  def group(e):return e[0],int(e[1]==e[2]),words[e[1]],words[e[2]]
  def add(row,j,v):row[j]=row.get(j,F())+v
  for e in edges:
   f,i,j=e;ve=gs[group(e)];re=vs[ve]['r']
   for ee in edges:
    g,k,l=ee;vf=gs[group(ee)];pat=cl.partition((i,j,k,l))
    q=PI['RZ',f,g,pat];nb[q]+=mass*(ha-F(re,pa+1));add(new[q],vf,-F(1,pa+1)+F(re,D))
    q=PI['ZZ',f,g,pat];nb[q]+=mass*ha;add(new[q],ve,-F(1,pa+1));add(new[q],vf,-F(1,pa+1))
    ov=ve if ve==vf else overlaps[key,*sorted((ve,vf))]
    add(new[q],ov,F(1,D))
 rows=rows+[{j:v for j,v in row.items() if v} for row in new];bs=bs+nb;names=names+list(map(str,PAIR))
 for (key,j,k),v in overlaps.items():
  for source in (j,k):rows.append({source:F(1),v:F(-1)});bs.append(F());names.append('ZZ-overlap-upper:'+str(v)+':'+str(source))
 return old,vs,bounds,names,rows,bs,slabs,overlaps

def solve_float(rows,bs,bounds,c=None):
 n=len(bounds);ri=[];ci=[];vals=[]
 for i,row in enumerate(rows):
  for j,v in row.items():ri.append(i);ci.append(j);vals.append(float(v))
 a=coo_matrix((vals,(ri,ci)),shape=(len(rows),n)).tocsr();bf=np.array([float(x) for x in bs]);scale=np.maximum(np.asarray(abs(a).max(axis=1).toarray()).ravel(),abs(bf));scale[scale==0]=1
 sol=linprog(np.zeros(n) if c is None else c,A_ub=-a.multiply(1/scale[:,None]),b_ub=bf/scale,bounds=[(0,None if b is None else float(b)) for b in bounds],method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
 return sol,a,bf,scale

def main():
 start=time.time();old,vs,bounds,names,rows,bs,slabs,overlaps=build();nz=len(vs)
 print('built',len(rows),'rows',nz+len(overlaps),'vars',time.time()-start,flush=True)
 if '--verify' in sys.argv:
  er=json.loads((HERE/(TARGET+'_exact.json')).read_text());ys=[F(v['weight']) for v in er['variables']]
  assert len(ys)==nz and all(F()<=y<=b for y,b in zip(ys,bounds))
  full=ys+[F()]*len(overlaps)
  for (key,j,k),v in overlaps.items():full[v]=min(ys[j],ys[k])
  slacks=[b+sum(v*full[j] for j,v in row.items()) for row,b in zip(rows,bs)]
  assert min(slacks)>=0
  print(json.dumps({'rows':len(rows),'minimum_slack':str(min(slacks)),'W':old['W']},indent=2));return
 sol,a,bf,scale=solve_float(rows,bs,bounds+[None]*len(overlaps))
 report={'scope':'fixed exact split-graph hist/R threshold support; all Z->Z and PAIR(R,Z),PAIR(Z,Z); not SPE','success':bool(sol.success),'status':sol.message,'rows':len(rows),'variables':nz+len(overlaps),'W':old['W'],'seconds':time.time()-start}
 print(json.dumps(report,indent=2),flush=True)
 if not sol.success:
  (HERE/(TARGET+'_status.json')).write_text(json.dumps(report,indent=2)+'\n');return
 # Replace overlaps with jointly attainable minima; restrict to discovered
 # Z order within each slab to recover an exact point with only nz variables.
 ovmap={v:min((j,k),key=lambda j:sol.x[j]) for (key,j,k),v in overlaps.items()}
 r2=[]
 for row in rows:
  out={}
  for j,v in row.items():jj=ovmap.get(j,j);out[jj]=out.get(jj,F())+v
  r2.append({j:v for j,v in out.items() if v})
 b2=list(bs)
 for key,gs in slabs.items():
  order=sorted(gs.values(),key=lambda j:sol.x[j])
  for j,k in zip(order,order[1:]):r2.append({k:F(1),j:F(-1)});b2.append(F())
 sol2,a2,bf2,scale2=solve_float(r2,b2,bounds,np.random.default_rng(91).normal(size=nz))
 assert sol2.success,sol2.message
 ys=[None]*nz;free=[]
 for j,(y,b) in enumerate(zip(sol2.x,bounds)):
  if y<1e-9:ys[j]=F()
  elif float(b)-y<1e-9:ys[j]=b
  else:free.append(j)
 residual=(a2@sol2.x+bf2)/scale2;eqs=[]
 for i,(row,b) in enumerate(zip(r2,b2)):
  if abs(residual[i])>1e-9:continue
  const=b+sum(v*ys[j] for j,v in row.items() if ys[j] is not None)
  eq=[row.get(j,F()) for j in free]+[-const]
  if any(eq):eqs.append(eq)
 yy=cl.exact_solve(eqs,len(free))
 for j,y in zip(free,yy):ys[j]=y
 assert all(F()<=y<=b for y,b in zip(ys,bounds))
 slacks=[b+sum(v*ys[j] for j,v in row.items()) for row,b in zip(r2,b2)];assert min(slacks)>=0
 # Verify all original overlap rows with actual minima, independently of order.
 full=ys+[F()]*len(overlaps)
 for (key,j,k),v in overlaps.items():full[v]=min(ys[j],ys[k])
 original=[b+sum(v*full[j] for j,v in row.items()) for row,b in zip(rows,bs)];assert min(original)>=0
 er={'scope':'complete cube feasible point after all chosen terminal and strong pair classes; not SPE','W':old['W'],'O':'1','rows':len(rows),'original_Z_variables':nz,'overlap_variables':len(overlaps),'minimum_slack':str(min(original)),'free_vertex_variables':len(free),'variables':[{**v,'weight':str(y)} for v,y in zip(vs,ys)]}
 (HERE/(TARGET+'_exact.json')).write_text(json.dumps(er,indent=2)+'\n');report['exact_verified']=True;report['minimum_exact_slack']=str(min(original));report['free_vertex_variables']=len(free)
 (HERE/(TARGET+'_status.json')).write_text(json.dumps(report,indent=2)+'\n');print('EXACT',json.dumps({k:v for k,v in er.items() if k!='variables'},indent=2),flush=True)
if __name__=='__main__':main()
