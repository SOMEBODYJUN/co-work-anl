"""Exact rational feasible refinement for the averaged root-menu necessary rows."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json
HERE=Path(__file__).parent
old=json.loads((HERE/'enhanced_2396_exact_obstruction.json').read_text())['atom_masses']
run=json.loads((HERE/'root_menu_completion.json').read_text());variables=run['variables_spec'];specs=run['row_specs'];names=run['row_names'];groups=run['groups']
from offdiagonal_probe import types,quads,paths,labels
mass=[F(a['mass']) for a in old];bits=[list(map(int,a['bits'])) for a in old];menus=[]
for i,n in enumerate(labels):menus.append((n,1,[b[i] for b in bits]))
d=[sum(n*t[0] for n,t in zip(a['AB_hist'],types)) for a in old];menus.append(('T',5,d))
for j in range(3):menus.append(('L'+str(j),5,[a['menus_lh'][j][0] for a in old]))
for tag,key,ts,ns in [('AB','AB_hist',types,'XY'),('AE','AE_hist',types,'XY'),('S','second_hist',quads,'UVW')]:
 for po,nm in enumerate(ns,1):menus.append((tag+':'+nm,5,[sum(n*t[po] for n,t in zip(a[key],ts)) for a in old]))
md={n:(size,count) for n,size,count in menus}
def q(n,d):return F(n,d) if n else F()
pathidx={n:[labels.index(c) for c in p] for n,p in paths.items()}
def coefficient(sp,variable):
 a,t,v=variable;b=bits[a];total=t+sum(v);pay=[q(x,total) for x in v];kind=sp[0]
 if kind=='root':return q(b[0],sum(b[:5]))-q(t,total)
 if kind=='menu':
  j,n=sp[1:];s,c=md[n];return pay[j]-q(c[a],s*(t+sum(v[:j])+4-j))
 if kind=='own':
  j,po=sp[1:];x=t if po==0 else v[po-1];return pay[j]-q(x,t+sum(v[:j])+4-j)
 if kind=='reverse':
  pn,j,k=sp[1:];idx=pathidx[pn];return q(b[idx[j]],sum(b[i] for i in idx))-q(v[k],sum(b[i] for i in idx[:j])+5-j)
 if kind=='profit':
  r,ids=sp[1:];start=4-r;beta=F(1499,750) if r==4 else F(5,3);bg=t+sum(v[:start]);load=sum(b[i] for i in ids);return beta*sum(pay[start:])-q(load,bg+load)
 if kind=='tax':
  ia,ib=sp[1:];na,sa,ca=menus[ia];nb,sb,cb=menus[ib];x=F(ca[a],sa);y=F(cb[a],sb);bg=t+sum(v[:2]);H=sum(pay[2:])+q(v[2],(bg+1)*(bg+2));return H-(x+y)/(bg+1)+2*x*y/((bg+1)*(bg+2))
 raise ValueError(sp)
x=[F(float(t)).limit_denominator(10**9) for t in run['point']]
for a,t in groups:
 inds=[i for i,(aa,bt,v) in enumerate(variables) if aa==a and bt==t];target=mass[a]*(d[a] if t else 5-d[a])/5;gap=target-sum(x[i] for i in inds);imax=max(inds,key=lambda i:x[i]);x[imax]+=gap;assert x[imax]>=0
assert min(x)>=0
S=[i for i,t in enumerate(x) if t]
slacks={n:sum((coefficient(sp,variables[i])*x[i] for i in S),F()) for n,sp in zip(names,specs)}
assert min(slacks.values())>0
record={'scope':'exact feasible refinement for 1310 necessary averaged root-menu inequalities only; no complete SPE asserted','variables':len(x),'positive_variables':len(S),'inequalities':len(names),'equalities':len(groups),'all_constraints_verified_exactly':True,'minimum_slack':str(min(slacks.values())),'minimum_slack_float':float(min(slacks.values())),'positive_refinements':[{'atom':variables[i][0],'t':variables[i][1],'replies':variables[i][2],'mass':str(x[i])} for i in S]}
(HERE/'root_menu_completion_exact.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:v for k,v in record.items() if k!='positive_refinements'},indent=2))
