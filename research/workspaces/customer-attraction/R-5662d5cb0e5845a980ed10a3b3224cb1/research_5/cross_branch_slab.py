"""Full actual-B Q/R states crossed with visible R/Z terminal graph.

Fixed old histogram/R-threshold support only. Each R slab is split into eight
actual-B states alpha; conditional Z masses beta <= alpha preserve the full
joint distribution. All Z-Z overlap coefficients are nonnegative and lifted
to min(beta_e,beta_f) within each sector, jointly realized by nested Z.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
import sys,json,time,hashlib
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from scipy.linalg import qr
HERE=Path(__file__).resolve().parent
import coupled_latest_master as current
import full_new_reply_closure as cl
import new_reply_budget as nr
STATES=tuple(product(range(2),range(2),(0,6)))
PN=[(kind,f,g,p) for kind,f,g,p in product(('ZZ-IC','PAIR-RZ','PAIR-ZZ'),range(2),range(2),cl.P4)]
PI={x:i for i,x in enumerate(PN)}
ORBS=((0,0),(1,0),(1,1))
CN=[(kind,f,d) for kind,(f,d) in product(('Q-R','Q-Z','R-R','R-Z','oldR-Q','oldR-R','oldZ-Q','oldZ-R'),ORBS)]
CI={x:i for i,x in enumerate(CN)}
BN=[(member,f,d,q) for member,(f,d),q in product(range(2),ORBS,range(12))]
BI={x:i for i,x in enumerate(BN)}

def add(row,j,v):
 if v:row[j]=row.get(j,F())+v

def build():
 source=HERE/'coupled_latest_exact.json';point=json.loads(source.read_text());cols,names,m,obj,norm=current.build();vals=[F(c['weight']) for c in point['columns']]
 assert json.dumps(cols)==json.dumps([{k:v for k,v in c.items() if k!='weight'} for c in point['columns']])
 byhist={};hi=None;bc={}
 for j,c in enumerate(cols):
  if c['kind']=='hist':hi=j;byhist[hi]={}
  elif c['kind']=='joint-reply':
   f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));byhist[hi].setdefault(g,{})[tuple(c['state'])]=j
  elif c['kind']=='actual-B-branch-state':bc[c['hist_column'],c['Q'],c['R'],c['ell']]=j
 base=[F()]*len(cols);base[0]=vals[0];mapping=[[] for _ in cols];variables=[];sectors=[];slabs=[];betabounds=[]
 for hi,gs in byhist.items():
  hmass=vals[hi];base[hi]=hmass
  if not hmass:continue
  rm={g:vals[st[1,0]]+vals[st[1,1]] for g,st in gs.items()};cuts=sorted({F(),hmass,*rm.values()})
  for lo,up in zip(cuts,cuts[1:]):
   mass=up-lo;rs={g:int(up<=r) for g,r in rm.items()};alphas=[]
   for g,st in gs.items():
    if rs[g]:base[st[1,0]]+=mass
   for state in STATES:
    aid=len(variables);variables.append({'kind':'alpha','hist_column':hi,'left':str(lo),'right':str(up),'state':list(state)});alphas.append(aid);mapping[bc[hi,*state]].append((aid,F(1)));betas={}
    for g,st in gs.items():
     bid=len(variables);variables.append({'kind':'beta','hist_column':hi,'left':str(lo),'right':str(up),'state':list(state),'group':[g[0],g[1],list(g[2]),list(g[3])]});betas[g]=bid;betabounds.append((aid,bid))
     if rs[g]:mapping[st[1,0]].append((bid,F(-1)));mapping[st[1,1]].append((bid,F(1)))
     else:mapping[st[0,1]].append((bid,F(1)))
    sectors.append((hi,lo,up,state,rs,aid,betas))
   slabs.append((mass,alphas))
  for j,c in enumerate(cols):
   if c['kind']=='overlap' and c['hist_column']==hi:
    cv=lambda g:(g[0],g[1],tuple(g[2]),tuple(g[3]));g,h=map(cv,c['groups']);base[j]=min(rm[g],rm[h])
 ncore=len(variables);overlaps={}
 for si,(_,lo,up,state,rs,aid,beta) in enumerate(sectors):
  for j,k in combinations(sorted(beta.values()),2):overlaps[si,j,k]=len(variables);variables.append({'kind':'overlap','sector':si,'beta_pair':[j,k]})
 rows=[];constants=[]
 for row in m:
  out={};const=F()
  for j,v in enumerate(row):
   if not v:continue
   const+=v*base[j]
   for k,c in mapping[j]:add(out,k,v*c)
  rows.append({j:v for j,v in out.items() if v});constants.append(const)
 extra=[{} for _ in PN+CN+BN];cnst=[F() for _ in extra];nn=len(PN);bb=nn+len(CN)
 for si,(hi,lo,up,state,rs,aid,beta) in enumerate(sectors):
  c=cols[hi];a=tuple(map(int,c['actual_bits']));p=sum(a[:3]);pa=sum(a[:4]);s=sum(a);pb=p+a[5];Db=(pb+1)*(pb+2);D=(pa+1)*(pa+2);qB,rB,L=state
  HA=nr.share(a[4]+a[5],s)+F(a[4],D);HB=nr.share(qB+rB,pb+qB+rB)+F(qB,Db)
  vq=nr.share(qB,pb+qB+rB);vr=nr.share(rB,pb+qB+rB)
  words=[w for w,n in zip(nr.PAT,c['hist']) for _ in range(n)];edges=[(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
  group=lambda e:(e[0],int(e[1]==e[2]),words[e[1]],words[e[2]])
  for e in edges:
   f,i,j=e;ge=group(e);ve=beta[ge];re=rs[ge];diag=int(i==j);de=p+words[i][0]+words[j][1+f]+1;dea=pa+re+1
   for ee in edges:
    g,k,l=ee;gf=group(ee);vf=beta[gf];pat=cl.partition((i,j,k,l))
    row=extra[PI['ZZ-IC',f,g,pat]];add(row,ve,F(1,dea));add(row,vf,-F(1,dea))
    row=extra[PI['PAIR-RZ',f,g,pat]];add(row,aid,HA-F(re,pa+1));add(row,vf,-F(1,pa+1)+F(re,D))
    row=extra[PI['PAIR-ZZ',f,g,pat]];add(row,aid,HA);add(row,ve,-F(1,pa+1));add(row,vf,-F(1,pa+1));ov=ve if ve==vf else overlaps[si,*sorted((ve,vf))];add(row,ov,F(1,D))
   # Both directions of genuine/safe terminal queries across the B branch.
   terms={'Q-R':(vq-F(re,pb+2),F()),'Q-Z':(vq,-F(1,pb+2)),'R-R':(vr-F(re,pb+qB+1),F()),'R-Z':(vr,-F(1,pb+qB+1)),
    'oldR-Q':(F(re-qB,de),F()),'oldR-R':(F(re-rB,de),F()),'oldZ-Q':(-F(qB,dea),F(1,dea)),'oldZ-R':(-F(rB,dea),F(1,dea))}
   for kind,(v,w) in terms.items():row=extra[nn+CI[kind,f,diag]];add(row,aid,v);add(row,ve,w)
   # True B-branch strong PAIR with every old legal fixed/indexed query.
   for qi in range(12):
    oldq=a[qi] if qi<6 else (words[i]+words[j])[qi-6]
    row=extra[bb+BI[0,f,diag,qi]];add(row,aid,HB-F(re+oldq,pb+1)+F(re*oldq,Db))
    row=extra[bb+BI[1,f,diag,qi]];add(row,aid,HB-F(oldq,pb+1));add(row,ve,-F(1,pb+1)+F(oldq,Db))
 rows += [{j:v for j,v in row.items() if v} for row in extra];constants+=cnst;names += list(map(str,PN+CN+BN))
 for aid,bid in betabounds:rows.append({aid:F(1),bid:F(-1)});constants.append(F());names.append('beta-upper:'+str(bid))
 for mass,alphas in slabs:
  rows.append({j:F(1) for j in alphas});constants.append(-mass);names.append('slab-sum-lower')
  rows.append({j:F(-1) for j in alphas});constants.append(mass);names.append('slab-sum-upper')
 for (si,j,k),v in overlaps.items():
  for source in (j,k):rows.append({source:F(1),v:F(-1)});constants.append(F());names.append('overlap-upper:'+str(v))
 return point,variables,ncore,sectors,slabs,overlaps,names,rows,constants

def solve(rows,bs,n,c=None):
 rr=[];cc=[];vv=[]
 for i,row in enumerate(rows):
  for j,v in row.items():rr.append(i);cc.append(j);vv.append(float(v))
 a=coo_matrix((vv,(rr,cc)),shape=(len(rows),n)).tocsr();b=np.array([float(v) for v in bs]);scale=np.maximum(np.asarray(abs(a).max(axis=1).toarray()).ravel(),abs(b));scale[scale==0]=1
 sol=linprog(np.zeros(n) if c is None else c,A_ub=-a.multiply(1/scale[:,None]),b_ub=b/scale,bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
 return sol,a,b,scale

def main():
 start=time.time();point,vs,ncore,sectors,slabs,ovs,names,rows,bs=build();print('built',len(rows),'rows',len(vs),'variables',time.time()-start,flush=True)
 if '--ablate' in sys.argv:
  nb=len(rows)-len(PN)-len(CN)-len(BN)-sum(1 for n in names if n.startswith('beta-upper:') or n.startswith('slab-sum-') or n.startswith('overlap-upper:'))
  # The raw new families immediately follow original rows; find their names exactly.
  cross_ids={i for i,n in enumerate(names) if n in set(map(str,CN))};pair_ids={i for i,n in enumerate(names) if n in set(map(str,BN))}
  reports=[]
  for label,omit in [('no-new-cross',cross_ids|pair_ids),('quotes-only',pair_ids),('branch-pairs-only',cross_ids)]:
   ids=[i for i in range(len(rows)) if i not in omit];ss,_,_,_=solve([rows[i] for i in ids],[bs[i] for i in ids],len(vs))
   rr={'ablation':label,'rows':len(ids),'success':bool(ss.success),'status':ss.message};reports.append(rr);print(json.dumps(rr),flush=True)
  (HERE/'cross_branch_slab_ablation.json').write_text(json.dumps({'scope':'fixed-R-threshold support floating feasibility only','results':reports},indent=2)+'\n');return
 if '--verify' in sys.argv:
  er=json.loads((HERE/'cross_branch_slab_exact.json').read_text());ys=[F(v['weight']) for v in er['variables']];assert len(ys)==ncore
  full=ys+[F()]*(len(vs)-ncore)
  for (_,j,k),v in ovs.items():full[v]=min(ys[j],ys[k])
  slacks=[b+sum(v*full[j] for j,v in row.items()) for row,b in zip(rows,bs)];assert min(full)>=0 and min(slacks)>=0
  print({'rows':len(rows),'minimum_slack':str(min(slacks)),'W':point['W']});return
 sol,a,b,scale=solve(rows,bs,len(vs));status={'scope':'fixed hist/R-threshold sub-support, complete conditional B-state/Z cube; not SPE or universal proof','success':bool(sol.success),'status':sol.message,'rows':len(rows),'variables':len(vs),'core_variables':ncore,'W':point['W'],'seconds':time.time()-start};print(json.dumps(status,indent=2),flush=True)
 (HERE/'cross_branch_slab_status.json').write_text(json.dumps(status,indent=2)+'\n')
 if not sol.success:return
 np.savez(HERE/'cross_branch_slab_float.npz',x=sol.x)
 # Eliminate zero and saturated beta variables plus one alpha per slab.
 expr=[None]*len(vs);nfree=0
 for mass,alphas in slabs:
  pos=[j for j in alphas if sol.x[j]>1e-9];assert pos;pivot=max(pos,key=lambda j:sol.x[j]);others=[]
  for j in alphas:
   if j not in pos:expr[j]=(F(),{})
   elif j!=pivot:expr[j]=(F(),{nfree:F(1)});others.append(nfree);nfree+=1
  expr[pivot]=(mass,{j:F(-1) for j in others})
 for hi,lo,up,state,rs,aid,beta in sectors:
  for g,j in beta.items():
   if sol.x[j]<1e-9:expr[j]=(F(),{})
   elif sol.x[aid]-sol.x[j]<1e-9:expr[j]=expr[aid]
   else:expr[j]=(F(),{nfree:F(1)});nfree+=1
 for (_,j,k),v in ovs.items():expr[v]=expr[j if sol.x[j]<=sol.x[k] else k]
 r2=[];b2=[]
 for row,const in zip(rows,bs):
  rr={};co=const
  for j,v in row.items():
   e0,ee=expr[j];co+=v*e0
   for k,w in ee.items():add(rr,k,v*w)
  rr={k:v for k,v in rr.items() if v}
  if rr or co<0:r2.append(rr);b2.append(co)
 # Explicit nonnegativity for dependent alpha expressions and beta ordering.
 for mass,alphas in slabs:
  for j in alphas:r2.append(dict(expr[j][1]));b2.append(expr[j][0])
 for hi,lo,up,state,rs,aid,beta in sectors:
  order=sorted(beta.values(),key=lambda j:sol.x[j])
  for j,k in zip(order,order[1:]):
   rr=dict(expr[k][1]);co=expr[k][0]-expr[j][0]
   for v,w in expr[j][1].items():add(rr,v,-w)
   r2.append({v:w for v,w in rr.items() if w});b2.append(co)
 print('reduced exact recovery',nfree,'variables',len(r2),'rows',flush=True)
 sol2,a2,bf2,sc2=solve(r2,b2,nfree,np.random.default_rng(932).normal(size=nfree));assert sol2.success,sol2.message
 res=(a2@sol2.x+bf2)/sc2;active=[i for i,v in enumerate(res) if abs(v)<1e-9]
 # Select a numeric independent subset, then solve and verify every row exactly.
 eq=[]
 for j,y in enumerate(sol2.x):
  if y<1e-9:eq.append(({j:F(1)},F()))
 eq += [(r2[i],-b2[i]) for i in active if r2[i]]
 mat=np.array([[float(rr.get(j,F())) for j in range(nfree)] for rr,bb in eq]);rs=np.max(abs(mat),axis=1);rs[rs==0]=1
 _,rr,piv=qr((mat/rs[:,None]).T,pivoting=True,mode='economic');rank=np.sum(abs(np.diag(rr[:,:nfree]))>1e-9);assert rank==nfree,(rank,nfree)
 chosen=[eq[int(i)] for i in piv[:nfree]];x=cl.exact_solve([[row.get(j,F()) for j in range(nfree)]+[bb] for row,bb in chosen],nfree)
 full=[e0+sum(v*x[j] for j,v in ee.items()) for e0,ee in expr]
 for (_,j,k),v in ovs.items():full[v]=min(full[j],full[k])
 slacks=[co+sum(v*full[j] for j,v in row.items()) for row,co in zip(rows,bs)];assert min(full)>=0 and min(slacks)>=0,(min(full),min(slacks))
 er={'scope':'exact complete-cube conditional cross-branch necessary point, not SPE or half counterexample','source_sha256':hashlib.sha256((HERE/'coupled_latest_exact.json').read_bytes()).hexdigest(),'W':point['W'],'O':'1','rows':len(rows),'variables_count':len(vs),'core_variables':ncore,'free_vertex_variables':nfree,'minimum_slack':str(min(slacks)),'variables':[{**v,'weight':str(y)} for v,y in zip(vs[:ncore],full[:ncore])]}
 (HERE/'cross_branch_slab_exact.json').write_text(json.dumps(er,indent=2)+'\n');status['exact_verified']=True;status['free_vertex_variables']=nfree;(HERE/'cross_branch_slab_status.json').write_text(json.dumps(status,indent=2)+'\n');print('EXACT',json.dumps({k:v for k,v in er.items() if k!='variables'},indent=2),flush=True)
if __name__=='__main__':main()
