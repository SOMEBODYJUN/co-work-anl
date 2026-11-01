"""Independent literal formula audit; no LP and no branch-projection imports."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
POINT=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json'
def sh(n,d):return F(n,d) if n else F()
def hval(p,b,c,z,pi,d,e):
 q=p+b
 return sh(35*b-3*d-14*e,q+d+e)+F(11*c,q+d+1)+F(3*(c+z),q+1)-F(3*(d+c*z),(q+1)*(q+2))+10*pi*d+(12*pi+3)*e

def literal(p,b,c,z,pi,d,e):
 q=p+b;den=q+d+e
 # Remove source/payments constants. This is a sum of exact legal rows.
 source=-sh(b,den)
 last=sh(e,den)-F(c,q+d+1)
 pair=sh(d+e,den)+F(d,(q+1)*(q+2))-F(c+z,q+1)+F(c*z,(q+1)*(q+2))
 return 35*source+11*last+3*pair-10*pi*d-12*pi*e-3*e

def psi(p,b,c,z,pi):return min(hval(p,b,c,z,pi,d,e) for d,e in product(range(2),repeat=2))

def main():
 count=0
 for p in range(10):
  for b,c,z,d,e in product(range(2),repeat=5):
   for pi in (F(0),F(1,7),F(1,6),F(1,5),F(1,4),F(1,3),F(1,2),F(1)):
    assert literal(p,b,c,z,pi,d,e)+hval(p,b,c,z,pi,d,e)==0
    count+=1
 data=json.loads(POINT.read_text());K=F(data['columns'][0]['weight']);w=F(data['W']);u4=u6=F();right=F();O=F()
 coeff=[]
 for col in data['columns']:
  if col['kind']!='hist':continue
  a=tuple(map(int,col['actual_bits']));n=F(col['weight']);hh=col['hist'];p=sum(a[:3]);ell=sum(a[:5]);s=sum(a)
  u4+=n*sh(a[3],s);u6+=n*sh(a[5],s)
  val=sum(mult*psi(p,b,c,a[5],F(1,ell+1)) for mult,(t,b,c) in zip(hh,product(range(2),repeat=3)))
  right+=n*val
  coeff.append({'actual_bits':col['actual_bits'],'hist':hh,'psi_sum':str(val)})
 left=6*(35*u4+22*u6+3*K);slack=left-right
 diagnostic=json.loads((HERE/'early_reply_promotion.json').read_text())
 assert slack/74==F(diagnostic['exact_slack']) and slack<0
 report={'status':'exact local formula identities and strict separation of specified lifted point verified; not a half proof','local_identity_checks':count,'query_indices':6,'left':str(left),'right':str(right),'raw_slack':str(slack),'slack_divided_by_74':str(slack/74),'point_sha256':hashlib.sha256(POINT.read_bytes()).hexdigest(),'coefficients':coeff}
 (HERE/'early_reply_promotion_exact.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='coefficients'},indent=2))
if __name__=='__main__':main()
