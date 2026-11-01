"""Independent indexed reconstruction of the 2396-row positive obstruction.

The 1959 new rows are reconstructed by fixing whole theme indices and then
performing literal sums of customer shares, two-player profits, or three-player
profits. Their published histogram formulas are only used for comparison.
The original 437 rows are replayed from their exact published definitions.
No LP, SPE solver, or floating arithmetic is used.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import sys,json,hashlib,time

HERE=Path(__file__).resolve().parent;SIB=HERE.parent/'next_credible';ROOT=HERE.parents[4]
sys.path.insert(0,str(SIB))
from offdiagonal_probe import rows as off_rows
from crossmenu_probe import rows as cross_rows
from menutax_probe import rows as tax_rows
from alignedtax_probe import rows as aligned_rows
from tripleprofit_probe import rows as triple_rows
SOURCE=SIB/'enhanced_2396_exact_obstruction.json'
ns={};src=(ROOT/'tests/audits/customer_attraction_five_indexed.py').read_text()
exec(compile(src.split('from pathlib import Path')[0],'<old exact definitions>','exec'),ns)
TY=list(product((0,1),repeat=3));QU=list(product((0,1),repeat=4))
LABELS='ABCDEUVWXY';PATHS={'actual':'ABCDE','second':'AEUVW','third':'ABEXY'}

def share(path,pos):
 return F(1,sum(path)) if path[pos] else F()
def floor(prefix,bit):
 return F(1,sum(prefix)+5-len(prefix)) if bit else F()
def profit(prefix,choices):
 c=sum(choices)
 return F(c,sum(prefix)+c) if c else F()
def H(path):
 p=sum(path[:3]);return share(path,3)+share(path,4)+(F(1,(p+1)*(p+2)) if path[3] else F())

def expand(a):
 bits=list(map(int,a['bits']));assert len(bits)==10 and set(bits)<=set((0,1))
 b=dict(zip(LABELS,bits));hs=[a['AB_hist'],a['AE_hist'],a['second_hist']]
 assert all(len(h)==len(t) for h,t in zip(hs,(TY,TY,QU)))
 assert all(all(isinstance(v,int) and v>=0 for v in h) and sum(h)==5 for h in hs)
 rows=[]
 for h,tys in zip(hs,(TY,TY,QU)):
  rr=[ty for n,ty in zip(h,tys) for _ in range(n)]
  rr.sort(key=lambda ty:ty[0]);rows.append(rr)
 T=[r[0] for r in rows[0]];d=sum(T)
 assert all([r[0] for r in rr]==T for rr in rows)
 menus={l:[b[l]] for l in LABELS};menus['T']=T
 for f,(ell,h) in enumerate(a['menus_lh']):
  assert isinstance(ell,int) and isinstance(h,int) and 0<=h<=d and 0<=ell-h<=5-d
  menus['L'+str(f)]=[1]*(ell-h)+[0]*(5-d-ell+h)+[1]*h+[0]*(d-h)
  assert sum(menus['L'+str(f)])==ell and sum(t*l for t,l in zip(T,menus['L'+str(f)]))==h
 for tag,rr,names in [('AB',rows[0],'XY'),('AE',rows[1],'XY'),('Sbranch',rows[2],'UVW')]:
  for pos,name in enumerate(names,1):menus[tag+':'+name]=[r[pos] for r in rr]
 fixed={pn:tuple(b[k] for k in path) for pn,path in PATHS.items()}
 branches={'AB':[tuple((b['A'],b['B'])+tuple(r)) for r in rows[0]],
  'AE':[tuple((b['A'],b['E'])+tuple(r)) for r in rows[1]],
  'Sbranch':[tuple((b['A'],)+tuple(r)) for r in rows[2]]}
 return b,d,menus,fixed,branches

def direct_new(a):
 b,d,menus,fixed,branches=expand(a);out={}
 for f,pn in enumerate(PATHS):
  prefix=fixed[pn][:3];L=menus['L'+str(f)]
  out[pn+':old-last:off-T']=sum((share(prefix+(menus['T'][i],L[i]),4)-floor(prefix+(menus['T'][i],),menus['T'][j]) for i in range(5) for j in range(5) if i!=j),F())
 for tag,ps,first,names in [('AB',branches['AB'],3,'XY'),('AE',branches['AE'],3,'XY'),('Sbranch',branches['Sbranch'],2,'UVW')]:
  local={'T':menus['T']};local.update({name:menus[tag+':'+name] for name in names})
  for pos in range(len(names)):
   idx=first+pos
   for name,menu in local.items():out[f'{tag}:node-{pos+1}:off-{name}']=sum((share(path,idx)-floor(path[:idx],menu[j]) for i,path in enumerate(ps) for j in range(5) if i!=j),F())
   for name,menu in menus.items():
    if len(menu)==5 and name!='T':out[f'{tag}:node-{pos+1}:crossmenu-{name}']=sum((share(path,idx)-floor(path[:idx],bit) for path in ps for bit in menu),F())
 groups=[(pn,[p]) for pn,p in fixed.items()]+list(branches.items())
 pairs=[('T','L'+str(i)) for i in range(3)]
 for tag,names in [('AB','XY'),('AE','XY'),('Sbranch','UVW')]:
  keys=['T']+[tag+':'+name for name in names];pairs+=list(combinations_with_replacement(keys,2))
 for group,ps in groups:
  # Each inner query fixes actual comparison themes before summing this
  # customer's coefficient; there is no customer-dependent row selection.
  for ma,mb in combinations_with_replacement(menus,2):
   out[f'{group}:newtax:{ma}|{mb}']=sum((H(path)-profit(path[:3],(x,y)) for path in ps for x in menus[ma] for y in menus[mb]),F())
  for ma,mb in pairs:
   out[f'{group}:align-tax:{ma}|{mb}']=sum((H(path)-profit(path[:3],(menus[ma][i],menus[mb][i])) for path in ps for i in range(5)),F())
   out[f'{group}:off-tax:{ma}|{mb}']=sum((H(path)-profit(path[:3],(menus[ma][i],menus[mb][j])) for path in ps for i in range(5) for j in range(5) if i!=j),F())
 for source,names in [('AB','TXY'),('AE','TXY'),('Sbranch','TUVW')]:
  lm=[menus['T']]+[menus[source+':'+n] for n in names[1:]]
  for positions in combinations_with_replacement(range(len(names)),3):
   title=source+':'+''.join(names[i] for i in positions)
   triples=[tuple(lm[pos][i] for pos in positions) for i in range(5)]
   for tag,pn in [('AB','actual'),('AE','second')]:
    path=fixed[pn];R=sum((share(path,i) for i in (2,3,4)),F())
    out[f'{tag}:three-profit:{title}']=sum((F(5,3)*R-profit(path[:2],tri) for tri in triples),F())
   for mode in ('all','align','off'):
    out[f'Sbranch:three-profit-{mode}:{title}']=sum((F(5,3)*sum((share(path,k) for k in (2,3,4)),F())-profit(path[:2],tri) for i,path in enumerate(branches['Sbranch']) for j,tri in enumerate(triples) if mode=='all' or (mode=='align' and i==j) or (mode=='off' and i!=j)),F())
 return out

def run():
 t0=time.time();data=json.loads(SOURCE.read_text());terms=data['atom_masses'];assert len(terms)==38
 W=O=F();slacks={};families={};newchecks=0;newmass=F()
 for k,item in enumerate(terms):
  mass=F(item['mass']);assert mass>0
  a=item;b,d,_,_,_=expand(a)
  W+=mass*int(any(map(int,a['bits'][:5])));O+=mass*int(d>0)
  if a['bits']=='0000000000':newmass+=mass
  rr=ns['evaluate'](list(map(int,a['bits'])),[a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True)
  assert len(rr)==437
  published={}
  for f in (off_rows,cross_rows,tax_rows,aligned_rows,triple_rows):published.update(f(a))
  direct=direct_new(a);assert len(direct)==1959 and set(published)==set(direct)
  for n in direct:
   assert direct[n]==published[n],(k,n,direct[n],published[n]);newchecks+=1
  rr.update(direct);assert len(rr)==2396
  for n,v in rr.items():slacks[n]=slacks.get(n,F())+mass*v
  if k%8==0:print(json.dumps({'atoms_checked':k+1,'elapsed':time.time()-t0}),flush=True)
 assert W==1 and O==F(data['objective']) and O-2==F(data['gap_above_two'])>0
 assert len(slacks)==2396 and all(v>=0 for v in slacks.values())
 assert len([n for n,v in slacks.items() if v==0])==44
 report={'scope':'independent exact replay of positive necessary-condition obstruction; no SPE claimed',
  'positive_atoms':len(terms),'W':str(W),'O':str(O),'O_minus_2W':str(O-2*W),'rows':len(slacks),'minimum_slack':str(min(slacks.values())),
  'zero_slack_count':sum(v==0 for v in slacks.values()),'new_row_atom_equalities':newchecks,
  'new_zero_fixed_mask_mass':str(newmass),'all_masses_strictly_positive':True,
  'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'review_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  'elapsed_seconds':time.time()-t0,
  'method':'Original 437 rows replayed from canonical exact definitions. Every new 1959-row atom coefficient independently reconstructed from explicit common-index 0/1 menus and literal fixed-index comparison sums, then compared with published histogram formulas.'}
 return report

if __name__=='__main__':
 report=run();Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
