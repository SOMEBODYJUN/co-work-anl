from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json
beta=F(1499,750)
def term(b,d):return F(b,d) if b else F(0)
def rho(p,abcd,qrs):
 a,b,c,d=abcd;q,r,s=qrs;k=sum(abcd);t=d+q+r+s
 pay=[term(h,p+k) for h in abcd]
 z=[term(h,p+t) for h in (d,q,r,s)]
 D=(p+1)*(p+2)*(p+3)*(p+4)
 delta2=F(1,p+1)-F(1,p+a+b+1)+(F(2*p*p,3*D) if a+b==2 else 0)
 delta3=F(1,p+1)-F(1,p+a+b+c+1)+(F(p*p+p,D) if a+b+c==3 else 0)
 P=2*(pay[2]+pay[3]+F(c,(p+a+b+1)*(p+a+b+2)))+delta2
 E=4*pay[3]+delta3
 FF=pay[0]-z[0]
 KK=[pay[1]-F(x,p+a+3) for x in (c,d,q,r,s)]
 LL=[z[1]-F(s,p+d+3),z[2]-F(c,p+d+q+2),z[2]-F(s,p+d+q+2),z[3]-F(b,p+d+q+r+1)]
 G=(sum(w*x for w,x in zip((341,302,306,302,355),KK))+354*E+646*P+1267*FF+sum(w*x for w,x in zip((24,8,17,108),LL)))/1000
 return beta*term(k,p+k)-G
mins={(p,b):min(rho(p,b,q) for q in product((0,1),repeat=3)) for p in [0,1] for b in product((0,1),repeat=4)}

def audit_primal(primal_path=None):
 if primal_path is None:
  root=next(p for p in Path(__file__).resolve().parents if (p/'work.py').is_file())
  primal_path=root/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_pricing/exact_optimum_primal_terminal_cross.json'
 z=json.loads(Path(primal_path).read_text());row=F(0);bonus=F(0)
 for atom in z['atoms']:
  b=list(map(int,atom['bits']));mass=F(atom['exact_mass']);d=sum(atom['AB_hist'][4:]);cc=sum(b[:5]);V=F(sum(b[1:5]),cc) if cc else F(0)
  target=sum(comb(d,j)*comb(5-d,4-j)*F(j,b[0]+j) for j in range(1,5) if j<=d and 0<=4-j<=5-d)
  row+=mass*(5*beta*V-target);bonus+=mass*5*mins[b[0],tuple(b[1:5])]
 return {'row':row,'bonus':bonus,'tightened':row-bonus}

def main():
 for b in product((0,1),repeat=4):print(''.join(map(str,b)),str(mins[0,b]),str(mins[1,b]))
 print(' '.join(f'{name} {float(value)}' for name,value in audit_primal().items()))

if __name__=='__main__':
 main()
