"""Definition-level exact audit of the third/fourth source shared-query line."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import json,hashlib
HERE=Path(__file__).resolve().parent
POINT=HERE/'promotion_joint_atoms_exact.json'
def sh(n,d):return F(n,d) if n else F()
def H(p,r,b,c,z,pi,rho,d,s,e,f):
 q=p+b;v=q+d+s
 return sh(44*b-d-2*e-9*f,v+e+f)+F(c,q+r-1)+F(7*c,v+e+1)+F(2*(c+z),v+1)-F(2*(e+c*z),(v+1)*(v+2))+6*rho*d+7*rho*e+(pi+7*rho+2)*f

def raw(p,r,b,c,z,pi,rho,d,s,e,f):
 q=p+b;v=q+d+s;total=v+e+f
 src=-sh(b,total)
 first=sh(d,total)-F(c,q+r-1)
 last=sh(f,total)-F(c,v+e+1)
 pair=sh(e+f,total)+F(e,(v+1)*(v+2))-F(c+z,v+1)+F(c*z,(v+1)*(v+2))
 return 44*src+first+7*last+2*pair-6*rho*d-7*rho*e-pi*f-7*rho*f-2*f

def psi(p,r,b,c,z,pi,rho):return min(H(p,r,b,c,z,pi,rho,d,s,e,f) for d,e,f in product(range(2),repeat=3) for s in range(r-3))
def main():
 cases=0
 for p in range(6):
  for r in range(4,8):
   for b,c,z,d,e,f in product(range(2),repeat=6):
    for s in range(r-3):
     for pi,rho in ((F(0),F(0)),(F(1,6),F(1)),(F(1,3),F(1,5)),(F(2,7),F(4,9))):
      assert H(p,r,b,c,z,pi,rho,d,s,e,f)+raw(p,r,b,c,z,pi,rho,d,s,e,f)==0;cases+=1
 point=json.loads(POINT.read_text());masses=defaultdict(F)
 for at in point['RZ_atoms']:masses[at['hist_index']]+=F(at['weight'])
 left=12*F(point['K']);right=F();coeff=[]
 for hi,mass in masses.items():
  h=point['histograms'][hi];a=tuple(map(int,h['actual_bits']));p=sum(a[:2]);ell=sum(a[:5]);tot=sum(a)
  left+=mass*(270*sh(a[2],tot)+120*sh(a[5],tot))
  value=sum(n*psi(p,4,b,c,a[5],F(1,p+4),F(1,ell+1)) for n,(t,b,c) in zip(h['hist'],product(range(2),repeat=3)))
  right+=mass*value;coeff.append({'hist_index':hi,'psi_sum':str(value)})
 slack=left-right;expected=json.loads((HERE/'third_cross_source_integer_row.json').read_text())
 assert slack==F(expected['raw_slack']) and slack<0
 report={'status':'exact nine-row identity and specified necessary point separation verified; not half/SPE','local_identity_checks':cases,'source_remaining':4,'left':str(left),'right':str(right),'raw_slack':str(slack),'slack_divided_by_77':str(slack/77),'input_sha256':hashlib.sha256(POINT.read_bytes()).hexdigest(),'coefficients':coeff}
 (HERE/'third_cross_source_exact.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='coefficients'},indent=2))
if __name__=='__main__':main()
