"""Independent fixed-index replay of the exact 53-histogram root refinement.

No primitive coefficient generator or vectorized source row is imported.
Every inequality is evaluated as its literal whole-theme comparison sum.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time,hashlib
from review_2396 import expand,share,floor,profit,H,LABELS

HERE=Path(__file__).resolve().parent;SIB=HERE.parent/'next_credible'
SOURCE=SIB/'root_full_hist_completion_exact.json';SPEC=SIB/'root_full_hist_completion.json'

def coefficient(spec,a,hist):
 b,d,menus,fixed,_=expand(a)
 ps=[tuple((t,)+tuple(v)) for t,v,n in hist for _ in range(n)]
 assert len(ps)==5 and sum(p[0] for p in ps)==d
 kind=spec[0]
 if kind=='root':return share(fixed['actual'],0)-sum((share(p,0) for p in ps),F())/5
 if kind=='menu':
  _,j,name=spec;name=name.replace('S:','Sbranch:');menu=menus[name]
  return sum((share(p,j+1)-floor(p[:j+1],q) for p in ps for q in menu),F())/(5*len(menu))
 if kind=='own':
  _,j,pos=spec
  return sum((share(p,j+1)-floor(p[:j+1],p[pos]) for p in ps),F())/5
 if kind=='reverse':
  _,pn,j,k=spec;oldp=fixed[pn]
  return sum((share(oldp,j)-floor(oldp[:j],p[k+1]) for p in ps),F())/5
 if kind=='profit':
  _,r,ids=spec;beta={4:F(1499,750),3:F(5,3)}[r];start=5-r;choices=tuple(b[LABELS[i]] for i in ids)
  return sum((beta*sum((share(p,k) for k in range(start,5)),F())-profit(p[:start],choices) for p in ps),F())/5
 if kind=='tax':
  _,i,j=spec;names=list(LABELS)+['T','L0','L1','L2','AB:X','AB:Y','AE:X','AE:Y','Sbranch:U','Sbranch:V','Sbranch:W'];left,right=menus[names[i]],menus[names[j]]
  return sum((H(p)-profit(p[:3],(q,r)) for p in ps for q in left for r in right),F())/(5*len(left)*len(right))
 if kind=='off':
  _,j,k=spec
  return sum((share(p,j+1)-floor(p[:j+1],q[k+1]) for i,p in enumerate(ps) for l,q in enumerate(ps) if i!=l),F())/5
 raise ValueError(spec)

def run():
 start=time.time();data=json.loads(SOURCE.read_text());spec=json.loads(SPEC.read_text());old=json.loads((SIB/'enhanced_2396_exact_obstruction.json').read_text())['atom_masses']
 terms=data['positive_histograms'];assert len(terms)==53 and len(spec['row_specs'])==len(spec['row_names'])==1326
 groups=[F() for _ in old];slack={n:F() for n in spec['row_names']};checks=0
 for k,item in enumerate(terms):
  mass=F(item['mass']);assert mass>0;ai=item['atom'];hist=item['histogram'];groups[ai]+=mass
  assert all(t in (0,1) and len(v)==4 and all(x in (0,1) for x in v) and isinstance(n,int) and n>0 for t,v,n in hist)
  for n,sp in zip(spec['row_names'],spec['row_specs']):slack[n]+=mass*coefficient(sp,old[ai],hist);checks+=1
  if k%10==0:print(json.dumps({'histograms_checked':k+1,'elapsed':time.time()-start}),flush=True)
 assert all(z==F(a['mass']) for z,a in zip(groups,old))
 assert all(v>0 for v in slack.values());minimum=min(slack.values());assert minimum==F(data['minimum_slack'])
 return {'scope':'independent exact audit of necessary root-histogram refinement only; not SPE',
  'positive_histograms':len(terms),'old_atoms':len(old),'mass_equalities':len(groups),'rows':len(slack),'exact_row_histogram_evaluations':checks,
  'minimum_slack':str(minimum),'minimum_slack_float':float(minimum),'all_constraints_strictly_positive':True,
  'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'elapsed_seconds':time.time()-start}

if __name__=='__main__':
 report=run();Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
