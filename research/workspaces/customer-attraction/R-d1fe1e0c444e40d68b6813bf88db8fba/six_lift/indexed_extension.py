"""Try exact full-position indexed-family extensions of a saved fixed point.

Histogram candidates here have one follower word per T-membership (t=0/1).
Feasibility in this subset is a valid obstruction. Infeasibility of this subset
is not claimed to exclude arbitrary histograms or any SPE.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,sys
import numpy as np
from scipy.optimize import linprog
from fixed_graph import ROOT,LABELS,PATHS,TRUE,sh
from six_stress import exact_solve
FAMS={'AB':('AB','actual',2),'AF':('AF','second',2),'Sbranch':('A','actual',1),
 'Lactual':('ABCD','actual',4),'Lsecond':('AFGH','second',4),'Lthird':('ABFK','third',4)}
SCALE=60

def candidates(k,d):
 pats=list(product((0,1),repeat=k-1));out=[];words=[]
 for z in pats if d<6 else [pats[0]]:
  for o in pats if d else [pats[0]]:
   out.append([(0,)+z]*(6-d)+[(1,)+o]*d);words.append((z,o))
 return np.array(out,dtype=np.int8),words

def specs(k):
 out=[('source',)]+[('cap',q) for q in range(k)]
 for tag in PATHS:
  for j in TRUE[tag]:
   for q in range(k):out.append(('fixedfloor',tag,j,q))
  for q in range(k):
   for r in range(q,k):out.append(('fixedpair',tag,q,r))
 for j in range(1,k):
  for q in LABELS:out.append(('floorfixed',j,q))
  for q in range(k):
   for way in ('own','all','off'):out.append(('floorfamily',j,q,way))
 for qi,q in enumerate(LABELS):
  for r in LABELS[qi:]:out.append(('pairfixed',q,r))
 for q in range(k):
  for r in range(q,k):
   for way in ('all_equal','query_equal','first_branch','second_branch','all_distinct'):
    out.append(('pairfamily',q,r,way))
 return out

def coeffs(fam,a,d):
 prefix,source,j0=FAMS[fam];p=sum(a[LABELS.index(c)] for c in prefix);k=6-len(prefix)
 e,words=candidates(k,d);m=len(e);loads=p+e.sum(axis=2)
 share=np.zeros((m,6,k),dtype=np.int64)
 for den in range(1,7):share+=np.where(loads[:,:,None]==den,(60//den)*e,0)
 cnt=60*e.sum(axis=1);joint={(q,r):60*(e[:,:,q]*e[:,:,r]).sum(axis=1) for q in range(k) for r in range(q,k)}
 def bb(c):return a[LABELS.index(c)]
 pre=p+e[:,:,:k-2].sum(axis=2)
 av=np.zeros_like(pre,dtype=np.int64);gv=np.zeros_like(pre,dtype=np.int64)
 for pp in range(5):
  av=np.where(pre==pp,60//(pp+1),av);gv=np.where(pre==pp,60//((pp+1)*(pp+2)),gv)
 H=share[:,:,-2]+share[:,:,-1]+e[:,:,-2]*gv
 rows=[];kaps=[]
 for s in specs(k):
  kind=s[0];kap=0
  if kind=='source':v=int(360*sh(a,PATHS[source],j0))-share[:,:,0].sum(axis=1)
  elif kind=='cap':v=-cnt[:,s[1]];kap=360
  elif kind=='fixedfloor':
   _,tag,j,q=s;path=PATHS[tag];den=sum(bb(c) for c in path[:j])+6-j
   v=int(360*sh(a,path,j))-cnt[:,q]//den
  elif kind=='fixedpair':
   _,tag,q,r=s;path=PATHS[tag];pf=sum(bb(c) for c in path[:4]);de=(pf+1)*(pf+2)
   hf=sh(a,path,4)+sh(a,path,5)+F(bb(path[4]),de)
   v=int(360*hf)-(cnt[:,q]+cnt[:,r])//(pf+1)+joint[q,r]//de
  elif kind=='floorfixed':
   _,j,q=s;den=p+e[:,:,:j].sum(axis=2)+k-j
   target=np.zeros(m,dtype=np.int64)
   for dd in range(1,7):target+=(den==dd).sum(axis=1)*(60//dd)*bb(q)
   v=share[:,:,j].sum(axis=1)-target
  elif kind=='floorfamily':
   _,j,q,way=s;den=p+e[:,:,:j].sum(axis=2)+k-j
   floor=np.zeros_like(den,dtype=np.int64)
   for dd in range(1,7):floor=np.where(den==dd,60//dd,floor)
   v=np.zeros(m,dtype=np.int64)
   for i,l in product(range(6),repeat=2):
    if way=='own' and i!=l:continue
    if way=='off' and i==l:continue
    v+=share[:,i,j]-e[:,l,q]*floor[:,i]
  elif kind=='pairfixed':
   _,q,r=s;v=H.sum(axis=1)-(bb(q)+bb(r))*av.sum(axis=1)+bb(q)*bb(r)*gv.sum(axis=1)
  elif kind=='pairfamily':
   _,q,r,way=s;v=np.zeros(m,dtype=np.int64)
   for i,j,l in product(range(6),repeat=3):
    ok={'all_equal':i==j==l,'query_equal':j==l and i!=j,'first_branch':i==j and i!=l,
      'second_branch':i==l and i!=j,'all_distinct':len({i,j,l})==3}[way]
    if ok:v+=H[:,i]-(e[:,j,q]+e[:,l,r])*av[:,i]+e[:,j,q]*e[:,l,r]*gv[:,i]
  else:raise ValueError(s)
  rows.append(np.broadcast_to(v,(m,)));kaps.append(kap)
 return np.array(rows,dtype=np.int64),kaps,words

def run(path):
 data=json.loads(Path(path).read_text());pts=[(tuple(map(int,x['bits'])),x['d'],F(x['weight'])) for x in data['support']];K=F(data['K'])
 results={}
 for fam,(pref,src,j0) in FAMS.items():
  k=6-len(pref);blocks=[];meta=[];offsets=[0];kap=None
  for a,d,wt in pts:
   co,kap,words=coeffs(fam,a,d);blocks.append(co);meta.append(words);offsets.append(offsets[-1]+len(words))
  mat=np.hstack(blocks).astype(float);eq=np.zeros((len(pts),mat.shape[1]))
  for i in range(len(pts)):eq[i,offsets[i]:offsets[i+1]]=1
  bounds=np.array([float(v) for a,d,v in pts]);bub=np.array([float(F(c)*K) for c in kap])
  # Slack = mat*x + kap*K >=0. Normalization sums preserve fixed masses.
  sol=linprog(np.zeros(mat.shape[1]),A_ub=-mat,b_ub=bub,A_eq=eq,b_eq=bounds,bounds=(0,None),method='highs')
  print(fam,k,mat.shape,'success',sol.success,sol.message,flush=True)
  result={'k':k,'candidate_columns':mat.shape[1],'rows':mat.shape[0],'subset_feasible_float':bool(sol.success)}
  if sol.success:
   support=np.flatnonzero(sol.x>1e-8);active=np.flatnonzero(np.abs(mat@sol.x+bub)<1e-7)
   eqs=[[F(int(mat[i,j])) for j in support]+[-F(kap[i])*K] for i in active]
   eqs += [[F(int(eq[i,j])) for j in support]+[pts[i][2]] for i in range(len(pts))]
   try:
    exact=exact_solve(eqs,len(support));assert min(exact)>=0
    co=np.hstack(blocks);slacks=[sum(F(int(co[i,j]))*v for j,v in zip(support,exact))+F(kap[i])*K for i in range(len(kap))]
    assert min(slacks)>=0
    hist=[]
    for col,wt in zip(support,exact):
     group=max(i for i in range(len(pts)) if offsets[i]<=col);word=meta[group][col-offsets[group]]
     if wt:hist.append({'fixed_support_index':group,'zero_follower_word':word[0],'one_follower_word':word[1],'mass':str(wt)})
    for group in range(len(pts)):assert sum(F(h['mass']) for h in hist if h['fixed_support_index']==group)==pts[group][2]
    result.update(exact_verified=True,minimum_slack=str(min(slacks)),support=hist)
   except (AssertionError,ZeroDivisionError) as exc:result.update(exact_verified=False,error=str(exc))
  results[fam]=result
 out=Path(__file__).with_name('indexed_extension.json');out.write_text(json.dumps({'fixed_point':str(Path(path).name),'scope':__doc__,'families':results},indent=2)+'\n')
 print({fam:{k:v for k,v in r.items() if k!='support'} for fam,r in results.items()},flush=True)
if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).with_name('fixed_graph_priced.json')))
