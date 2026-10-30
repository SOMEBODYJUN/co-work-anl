"""New exact reconstruction of the review's published boundary recipes, not a recovered old script."""
from fractions import Fraction as F
import importlib.util,json,sys
from pathlib import Path
base=Path(sys.argv[1]);source=base/'original/tests/audits/weighted_congestion/heterogeneous_endpoint/verify_endpoint_reduction.py'
s=importlib.util.spec_from_file_location('endpoint_original',source);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
alpha=F(12,5);w=F(23,1000);eps=F(1,10**12);rows=[]
for n in [10-eps,F(10),10+eps]:
 weights=[w]+[(n-1)*w/9]*9;W=sum(weights,F(0));p=[F(1,10000),F(0),F(1)];fs=[]
 for v in weights:
  coeff=F(99,100)*(m.poly(p,1+v)-alpha*m.poly(p,W)-(alpha-1)*F(1,100000))/(alpha*(1+v)**100-v**100)
  assert coeff>0;f=m.monomial(100,coeff);f[0]=F(1,100000);fs.append(f)
 m.endpoints(p,weights,fs,alpha);R=alpha*m.poly(p,1+W)-m.poly(p,F(1));assert (m.poly(fs[0],1+w)-alpha*m.poly(fs[0],F(1)))*W>R*w
 count=n.numerator//n.denominator;gamma=1+F(count)/n*(alpha-1);m.endpoints(p,[w]*count,[fs[0]]*count,gamma);assert n>(alpha-1)**2 and gamma>1 and gamma>alpha-1/(alpha-1)
 rows.append({'n':str(n),'m':count,'gamma':str(gamma),'input_endpoints':True,'selected_first':True,'output_endpoints':True})
weights=[w]*10+[F(1,10**6)];W=sum(weights,F(0));p=m.monomial(2);fs=[]
for v in weights[:10]:
 b=F(99,100)*(m.poly(p,1+v)-alpha*m.poly(p,W))/(alpha*(1+v)**100-v**100);assert b>0;fs.append(m.monomial(100,b))
fs.append([F(0)]);m.endpoints(p,weights,fs,alpha);R=alpha*m.poly(p,1+W)-m.poly(p,F(1));assert not (m.poly(fs[-1],1+weights[-1])-alpha*m.poly(fs[-1],F(1)))*W>R*weights[-1]
n=W/w;gamma=1+F(10)/n*(alpha-1);m.endpoints(p,[w]*10,[fs[0]]*10,gamma)
count=0
for k in [1,2,3,10,100]:
 for n in [k-eps,F(k),k+eps]:
  for a in [F(1000001,1000000),F(3,2),F(2),F(12,5),F(3),F(10)]:
   if n<1 or n<=(a-1)**2:continue
   mm=n.numerator//n.denominator;g=1+F(mm)/n*(a-1);assert mm>=1 and g>1 and g>a-1/(a-1);count+=1
assert count==62
print(json.dumps({'status':'passed','scope':'new reconstruction from complete review recipes; endpoint fixtures, not full-state enumeration','floor_fixtures':rows,'zero_satellite_fixture':{'lights':11,'all_endpoints':True,'zero_cannot_be_witness':True,'output_m':10,'gamma':str(gamma)},'rounding_formula_cases':count},indent=2))
