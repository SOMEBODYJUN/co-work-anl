"""2026-11-12 task-local exact checks; no historical code imported or run."""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).with_name('verification.md')
table=[list(map(F,(0,960,1220,1480,1740,2000))),list(map(F,(0,'1665/4','2745/4','3785/4','4825/4','5865/4'))),list(map(F,(0,320,524,728,932,1136)))]
checks={}
for p,d in product(range(3),range(6)):
 vals=[]
 for h,q,r in product((0,1),repeat=3):
  s=p+h+q+r;v=lambda a:F(a,s) if a else F(0);b=p+h
  G=-17040*v(h)+9000*F(h-q,p+3)+10080*F(h-r,p+3)+600*(5*v(r)-F(d,p+h+q+1))-1085*h+360*(5*(v(q)+v(r)+F(q,(b+1)*(b+2)))-F(5*r+d-2*r*d,b+1)-F(2*r*d,b+2))+2679*F(5*h,p+3)
  assert -table[p][d]-G>=0
  vals.append(G)
 assert -max(vals)==table[p][d]
checks['P7_hidden_states']=144
choose=lambda n,k:comb(n,k) if 0<=k<=n else 0
for p,d,q,r in product(range(3),range(6),range(2),range(6)):
 mix=sum((F(choose(d,s)*choose(5-d,r-s),choose(5,r))*table[p][s+(5-r)*q] for s in range(r+1)),F())
 assert mix>=F(r,5)*table[p][d]+F(5-r,5)*table[p][5*q]
checks['mixed_states']=216
certs=[('80','71/5',{'s1':'1/2','s2':'1/2','s3':'1/2','s4':'5','o4':'1'}),('65710/1073','56053/5365',{'s1':'1/2','s2':'7409/2146','s3':'7013/2146','s4':'2824/1073','i24':'3168/1073','i34':'2970/1073','o4':'1'}),('89090/1753','29147/3506',{'s1':'8089/3506','s2':'9673/3506','s3':'9475/3506','s4':'4475/1753','i24':'3960/1753','o4':'565/1753','r2opt':'297/1753'}),('6291370/137873','1983595/275746',{'s1':'559907/1102984','s2':'684353/275746','s3':'670295/275746','s4':'651245/275746','o4':'37685/137873','r2opt':'21087/137873','p7repeat':'33/275746'}),('3539900/137873','303930/137873',{'s1':'559907/1102984','s2':'684353/275746','s3':'670295/275746','s4':'651245/275746','o4':'37685/137873','r2opt':'21087/137873','p7repeat':'33/275746'}),('1951080/78349','3918479/1958725',{'s1':'3489701/1958725','s2':'948276/391745','s3':'185736/78349','s4':'188931/78349','o4':'18744/78349','r2opt':'58788/391745','p7repeat':'4473/69965657','p7opt':'18713/349828285'}),('463062/19157','1729493/957850',{'s1':'1633117/957850','s2':'225141/95785','s3':'44091/19157','s4':'47286/19157','o4':'3834/19157','r2O':'56232/95785','p7opt':'11/95785'})]
checks['envelopes']=[]
for Bs,Cs,ls in certs:
 B,C=F(Bs),F(Cs);lam={k:F(v) for k,v in ls.items()};res=[]
 for b,d in product(product((0,1),repeat=5),range(6)):
  s=sum(b);v=[F(x,s) if x else F() for x in b];p=sum(b[:3]);H=v[3]+v[4]+F(b[3],(p+1)*(p+2))
  rows={f's{j}':F(b[0]-b[j]) for j in range(1,5)}
  for i in range(1,5):
   for j in range(5):rows[f'i{i}{j}']=v[i]-F(b[j],sum(b[:i])+5-i)
   rows[f'o{i}']=5*v[i]-F(d,sum(b[:i])+5-i)
  rows['r2opt']=10*H-F(d*(5-d),p+1)-F(d*(d-1),p+2)
  rows['r2O']=F(5,2)*H+F(p,p+1)-int(d>0)
  pp=sum(b[:2]);rows['p7repeat']=17040*v[2]+1085*b[0]-2679*F(5*b[4],pp+3)-table[pp][d]
  rows['p7opt']=17040*v[2]+1085*b[0]-2679*F(d,pp+3)-table[pp][d]
  e=B*v[0]-C*b[0]-int(d>0)-sum(lam[k]*rows[k] for k in lam)
  assert e>=0,(Bs,b,d,e)
  res.append(e)
 checks['envelopes'].append({'B':Bs,'C':Cs,'types':len(res),'zero_residues':res.count(0),'minimum':str(min(res))})
base=ROOT/'archives/customer-attraction/tools/evidence/weighted-source-contracts-resumed-boss3/original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate'
checks['source_evaluations']=[]
for name,scale,which in [('exact_weighted_source.json',40844,'mW'),('exact_current_source_payment_v1.json',51560,'z4')]:
 raw=(base/name).read_bytes();x=json.loads(raw);val=F();W=F();O=F();keys=set()
 for a in x['atoms']:
  mass=F(a['exact_mass']);assert mass>0
  assert sum(a['AB_hist'])==sum(a['AE_hist'])==sum(a['second_hist'])==5
  d=sum(a['AB_hist'][4:]);assert d==sum(a['AE_hist'][4:])==sum(a['second_hist'][8:])
  z=list(map(int,a['max_bits']));p=sum(z[:2]);u=F(z[2],sum(z)) if z[2] else F()
  j=sum(a['second_hist'][i] for i in range(16) if i&1) if which=='mW' else 5*z[4]
  val+=mass*(17040*u+1085*z[0]-2679*F(j,p+3)-table[p][d])/scale
  W+=mass*int(any(map(int,a['bits'][:5])));O+=mass*int(d>0)
  keys.add(json.dumps({k:v for k,v in a.items() if k not in ('H_bit','exact_mass')},sort_keys=True))
 assert W==1 and val<0
 checks['source_evaluations'].append({'input':name,'sha256':hashlib.sha256(raw).hexdigest(),'atoms':len(x['atoms']),'merged_types':len(keys),'W':str(W),'O':str(O),'scale':scale,'query':which,'exact_cut':str(val)})
assert checks['source_evaluations'][0]['exact_cut']=='-169500194513991512083150016856795303715058552168132987135/24368697863582404164257358829723456062199106455303425183072'
assert checks['source_evaluations'][1]['exact_cut']=='-873030838468862296964238756691087720236458052575800500150227171047/392978057633533432339819921780551383171650379400924880646307953737104'
# Signed/H4 coverage dictionary, all feasible per-client actual/comparison counts.
for c,k in product(range(9),range(9)):
 V=F(1,c+1) if c else F();J=F(c,c+1);e=F(k,c+1);O=int(k>0)
 E=J+e-O;Jout=J if c and not k else F();REP=F(k-1,c+1) if k else F()
 assert E==Jout+REP>=0
checks['coverage_dictionary_types']=81
# Three singleton occupancy columns: all 10 counts, exact dual and attaining mixture.
vals=[]
for a in range(4):
 for b in range(4-a):
  q=(a,b,3-a-b);W=sum(c>0 for c in q);H=F(sum(F(3) if c==0 else F(4,c+1) for c in q),3)
  D=W-F(9,10)*(W-H);assert D>=F(21,10);vals.append((q,W,H))
assert F(9,10)*(F(2)-F(19,9))+F(1,10)*(3-2)==0
assert F(9,10)*2+F(1,10)*3==F(21,10)
checks['three_singleton_occupancies']=len(vals)
OUT.write_text('# 本任务2026-11-12新有理校验\n\n仅运行此独立转写checker一次。没有import或运行原审计、LP、BI或发现器。检查覆盖系数域与两个固定必要点；未重查5484/6565原行、未重查四点中的后两点，也未认证必要点为SPE。\n\n```json\n'+json.dumps(checks,ensure_ascii=False,indent=2)+'\n```\n')
print(json.dumps({'status':'PASS','P7':144,'mixed':216,'envelope_type_checks':7*192,'source_atoms':111,'coverage_types':81,'occupancy_columns':10,'report':str(OUT.relative_to(ROOT))},ensure_ascii=False))
