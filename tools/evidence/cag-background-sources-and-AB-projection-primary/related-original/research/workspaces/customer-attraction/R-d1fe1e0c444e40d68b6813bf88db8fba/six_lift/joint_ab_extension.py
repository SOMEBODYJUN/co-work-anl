"""Complete AB/AF histogram feasibility at one exact six-player fixed point.
All d-compatible histograms are enumerated. A rational Farkas obstruction is
checked with integer column evaluations, not by accepting LP infeasibility.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,sys
import numpy as np
from scipy.optimize import linprog
import indexed_extension as ie

def compositions(n,k):
 if k==1:yield (n,);return
 for j in range(n+1):
  for rest in compositions(n-j,k-1):yield (j,)+rest

def complete(k,d):
 pats=list(product((0,1),repeat=k-1));h0=list(compositions(6-d,len(pats)));h1=list(compositions(d,len(pats)))
 out=[];words=[]
 for z,o in product(h0,h1):
  out.append([(0,)+p for p,n in zip(pats,z) for _ in range(n)]+[(1,)+p for p,n in zip(pats,o) for _ in range(n)])
  words.append((z,o))
 return np.array(out,dtype=np.int8),words
ie.candidates=complete
original_specs=ie.specs
def filtered_specs(k):
 out=[]
 for spec in original_specs(k):
  kind=spec[0]
  if kind in ('fixedfloor','fixedpair') and spec[1]!='actual':continue
  if kind=='floorfixed' and spec[2] not in 'ABCDEF':continue
  if kind=='pairfixed' and any(c not in 'ABCDEF' for c in spec[1:]):continue
  out.append(spec)
 return out
ie.specs=filtered_specs

def run(fam='AB'):
 here=Path(__file__).resolve().parent;data=json.loads((here/'joint_AB_input.json').read_text())
 pts=[(tuple(map(int,x['actual_bits']+'0000000')),x['d'],F(x['weight'])) for x in data['support']];K=F(data['K'])
 k=6-len(ie.FAMS[fam][0]);offsets=[0];mat=None;kap=None
 for group,(a,d,wt) in enumerate(pts):
  co,kap,words=ie.coeffs(fam,a,d)
  assert np.max(np.abs(co))<32768
  if mat is None:mat=np.empty((co.shape[0],len(pts)*co.shape[1]),dtype=np.int16)
  mat[:,offsets[-1]:offsets[-1]+co.shape[1]]=co
  offsets.append(offsets[-1]+co.shape[1]);print('built group',group,'histograms',co.shape[1],flush=True)
 counts=np.diff(offsets);assert len(set(counts))==1
 n=mat.shape[1];rng=np.random.default_rng(42);selected=set()
 for start,end in zip(offsets[:-1],offsets[1:]):selected.update(map(int,rng.choice(np.arange(start,end),size=min(32,end-start),replace=False)))
 kapp=np.array(kap);bub=np.array([float(F(c)*K) for c in kap]);mass=np.array([float(p[2]) for p in pts])
 for it in range(100):
  ids=np.array(sorted(selected));groupids=np.searchsorted(offsets,ids,side='right')-1
  eq=np.zeros((len(pts),len(ids)+1));eq[groupids,np.arange(len(ids))]=1
  sub=np.c_[-mat[:,ids].astype(float),-np.ones(mat.shape[0])]
  sol=linprog(np.r_[np.zeros(len(ids)),1.],A_ub=sub,b_ub=bub,A_eq=eq,b_eq=mass,bounds=(0,None),method='highs')
  assert sol.success,sol.message
  lam=-sol.ineqlin.marginals
  rc=-lam@mat-sol.eqlin.marginals[np.repeat(np.arange(len(pts)),counts)]
  neg=np.flatnonzero(rc<-1e-7)
  print('phase',it,'artificial',sol.fun,'columns',len(ids),'minrc',float(rc.min()),'negative',len(neg),flush=True)
  if sol.fun<1e-9 or not len(neg):break
  selected.update(map(int,neg[np.argsort(rc[neg])[:500]]))
  for g in range(len(pts)):
   j=offsets[g]+int(np.argmin(rc[offsets[g]:offsets[g+1]]))
   if rc[j]<-1e-7:selected.add(j)
 else:raise RuntimeError('phase I convergence')
 report={'family':fam,'k':k,'n_fixed_types':len(pts),'histograms_per_fixed_type':int(counts[0]),'complete_columns':n,'necessary_rows':mat.shape[0],
 'fixed_W':data['W'],'fixed_O':data['O'],'phase_I_float':float(sol.fun),
 'scope':'Full d-compatible histogram domain for this one indexed family at the saved fixed point; not six-player SPE or half counterexample'}
 if sol.fun>1e-8:
  # Nonnegative rational row weights. Every coefficient is already scaled by60.
  L=np.rint(np.maximum(lam,0)*10**7).astype(np.int64)
  weighted=L@mat.astype(np.int64)
  maxima=[int(weighted[start:end].max()) for start,end in zip(offsets[:-1],offsets[1:])]
  cap=int(L@kapp)
  contradiction=sum(pt[2]*v for pt,v in zip(pts,maxima))+K*cap
  assert contradiction<0,contradiction
  report.update(exact_farkas_verified=True,integer_row_weights={':'.join(map(str,ie.specs(k)[i])):int(v) for i,v in enumerate(L) if v},
   per_fixed_type_integer_maxima=maxima,K_integer_coefficient=cap,exact_upper_bound=str(contradiction),
   interpretation='Every histogram extension has weighted nonnegative-row sum at most this strictly negative value; therefore no extension exists')
 else:
  support=np.flatnonzero(sol.x[:-1]>1e-8)
  cols=ids[support]
  active=np.flatnonzero(np.abs(mat[:,cols].astype(float)@sol.x[support]+bub)<1e-7)
  equations=[[F(int(mat[i,c])) for c in cols]+[-F(kap[i])*K] for i in active]
  equations += [[F(int(groupids[j]==g)) for j in support]+[pts[g][2]] for g in range(len(pts))]
  from six_stress import exact_solve
  exact=exact_solve(equations,len(cols));assert min(exact)>=0
  slacks=[sum(F(int(mat[i,c]))*v for c,v in zip(cols,exact))+F(kap[i])*K for i in range(mat.shape[0])]
  assert min(slacks)>=0
  records=[]
  for c,v in zip(cols,exact):
   g=int(np.searchsorted(offsets,c,side='right')-1)
   assert pts[g][1]==1
   _,words=complete(k,pts[g][1]);h0,h1=words[c-offsets[g]]
   if v:records.append({'fixed_support_index':g,'histogram_t0':list(h0),'histogram_t1':list(h1),'mass':str(v)})
  for g in range(len(pts)):assert sum(F(r['mass']) for r in records if r['fixed_support_index']==g)==pts[g][2]
  report.update(exact_feasible_verified=True,minimum_slack=str(min(slacks)),extension_support=records,
   scope='Complete four-bit six-index AB necessary graph extends the saved joint-system point; not a strategy or SPE realization')
 (here/('joint_full_'+fam+'_extension.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('integer_row_weights','per_fixed_type_integer_maxima','extension_support')},indent=2),flush=True)
if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else 'AB')
