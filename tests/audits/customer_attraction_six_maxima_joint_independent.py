"""Second implementation. Imports no author/repository audit or discovery code."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse,json,hashlib
F=Fraction
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path)
args=parser.parse_args()
repo=Path(__file__).resolve().parents[2]
certificate=repo/'evidence/certificates/customer_attraction/six_maxima_joint_bound.json'
raw=json.loads(certificate.read_text())
assert raw['n5_common_denominator']==10000
expected_order=['mixed:'+str(t) for t in range(5)]+['lastBR:'+str(j) for j in range(6)]
expected_order+=['twoTax:'+str(j)+str(k) for j in range(6) for k in range(j,6)]
assert raw['row_order_n5']==expected_order

def masks(n):
 for bits in product((0,1), repeat=n):
  yield sum(bit<<i for i,bit in enumerate(bits)),bits

def coarse(n,I,J):
 ib=[int(I>>j&1) for j in range(6)]
 jb=[int(J>>j&1) for j in range(n)]
 load=sum(jb)
 utility=[F(x,load) if x else F(0) for x in jb]
 coeff=[]
 for t in range(n):
  if sum(ib)==6: floor=F(1,n)
  elif sum(ib)==1: floor=F(1,2*n)
  elif t==n-1: floor=F(n+1,n*(n+5))
  else: floor=F(1,3*n-2*t)
  coeff.append(utility[t]-floor)
 # Actual earlier membership remains fixed under the final deviation.
 old_load=sum(jb[:-1])
 for j in range(6): coeff.append(utility[-1]-F(ib[j],old_load+1))
 before_last_two=sum(jb[:-2])
 actual_last_two=sum(utility[-2:])
 for j in range(6):
  for k in range(j,6):
   simulated=ib[j]+ib[k]
   hypothetical_two=F(simulated,before_last_two+simulated) if simulated else F(0)
   actual_penultimate_tax=F(jb[-2],(before_last_two+1)*(before_last_two+2))
   coeff.append(actual_last_two+actual_penultimate_tax-hypothetical_two)
 return coeff

# Completeness independently from all6^5 labeled routes rather than RGS recursion.
canonical=set()
for route in product(range(6),repeat=5):
 mapping={};labels=[]
 for j in route:
  if j not in mapping: mapping[j]=len(mapping)
  labels.append(mapping[j])
 canonical.add(tuple(labels))
assert len(canonical)==52
assert len(raw['n5_certificates'])==52
assert {tuple(x['route']) for x in raw['n5_certificates']}==canonical
count5=0;min5=None
for c in raw['n5_certificates']:
 a=c['route'];assert all(isinstance(v,int) and v>=0 for v in c['multipliers_numerator'])
 lam=[F(v,raw['n5_common_denominator']) for v in c['multipliers_numerator']]
 assert len(lam)==32 and min(lam)>=0
 m=None;cnt=0
 for I in range(1,64):
  for J,js in masks(5):
   if js[-1]!=int(I>>a[-1]&1):continue
   if any(js[t] and not(I>>a[t]&1) for t in range(5)):continue
   residual=F(J!=0)-F(1,2)-sum(x*y for x,y in zip(lam,coarse(5,I,J)))
   assert residual>=0,(a,I,J,residual)
   cnt+=1;m=residual if m is None else min(m,residual)
 assert cnt==c['column_count'] and m==F(c['minimum_residual'])
 count5+=cnt;min5=m if min5 is None else min(m,min5)
assert count5==20080 and min5==0
universal={}
for n,expected in [(6,F(1,72)),(7,F(1,32)),(8,F(23393,532224))]:
 lam=[F(35,48)]*(n-2)+[F(0)]*2+[F(0)]+[F(1,8)]*5
 for j in range(6):
  for k in range(j,6):
   lam.append(F(5,48) if j==0 and k>0 else F(1,96) if j>0 and k>j else F(0))
 m=None;cnt=0;coremin=None
 for I in range(1,64):
  for J,js in masks(n):
   if js[-1]!=I%2:continue
   r=F(J!=0)-F(1,2)-sum(x*y for x,y in zip(lam,coarse(n,I,J)))
   assert r>=0,(n,I,J,r)
   cnt+=1;m=r if m is None else min(r,m)
   if I==63:coremin=r if coremin is None else min(r,coremin)
 assert cnt==63*2**(n-1) and m==expected
 universal[n]={'columns':cnt,'minimum':str(m),'core_minimum':str(coremin)}
report={'status':'PASS','claim_id':'CA-SIX-MAXIMA-HALF','n5_routes':52,'n5_columns':count5,'n5_minimum':str(min5),'universal':universal,'certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),'audit_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'proof_sha256':hashlib.sha256((repo/'research/current/customer_attraction/six_maxima_joint_bound.md').read_bytes()).hexdigest(),'method':'Independent direct mask enumeration; route completeness checked by canonicalizing all 6^5 labeled full routes. No import of author or discovery code.'}
if args.output:
 assert not args.output.exists(),'Frozen output exists; choose a new destination.'
 args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
