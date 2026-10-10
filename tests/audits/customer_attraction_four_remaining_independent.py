"""Independent symbolic reconstruction of corrected fixed-background four bound.
Raw original SPE slack definitions and complete P/E comparison multiplicities.
No imports of the candidate audit or manuscript implementation.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import argparse
import hashlib
import platform
import subprocess

D4=(24,50,35,10,1)

def add(*items):
 return tuple(sum(row[i] if i<len(row) else 0 for row in items) for i in range(5))
def times(k,row):return tuple(k*x for x in row)
def divide(offsets):
 coeff=list(map(F,D4))
 for offset in offsets:
  out=[F(0)]*(len(coeff)-1);out[-1]=coeff[-1]
  for i in range(len(out)-2,-1,-1):out[i]=coeff[i+1]-offset*out[i+1]
  if coeff[0]!=offset*out[0]:raise ValueError((offsets,coeff))
  coeff=out
 return tuple(coeff)
def fraction(numerator,*offsets):
 return (F(0),) if not numerator else times(numerator,divide(offsets))
def unit(own,*others):return fraction(own,own+sum(others))
def delta_two(v):
 base=fraction(v,1,v+1)
 return add(base,(0,0,F(2,3),0,0)) if v==2 else base

def delta_three(v):
 base=fraction(v,1,v+1)
 return add(base,(0,1,1,0,0)) if v==3 else base

def four_rho(a,b,c,d,q,r,s):
 alpha,beta,gamma,eta=(unit(x,*rest) for x,rest in ((a,(b,c,d)),(b,(a,c,d)),(c,(a,b,d)),(d,(a,b,c))))
 zd,zq,zr,zs=(unit(x,*rest) for x,rest in ((d,(q,r,s)),(q,(d,r,s)),(r,(d,q,s)),(s,(d,q,r))))
 H=add(gamma,eta,fraction(c,a+b+1,a+b+2))
 Pbase=add(times(2,H),delta_two(a+b))
 Ebase=add(times(4,eta),delta_three(a+b+c))
 K=[add(beta,times(-1,fraction(x,a+3))) for x in (c,d,q,r,s)]
 root=add(alpha,times(-1,zd))
 Lqs=add(zq,times(-1,fraction(s,d+3)))
 Lrc=add(zr,times(-1,fraction(c,d+q+2)))
 Lrs=add(zr,times(-1,fraction(s,d+q+2)))
 Lsb=add(zs,times(-1,fraction(b,d+q+r+1)))
 terms=list(zip((341,302,306,302,355),K))
 terms.extend(((354,Ebase),(646,Pbase),(1267,root),(24,Lqs),(8,Lrc),(17,Lrs),(108,Lsb)))
 G=add(*(times(F(w,1000),row) for w,row in terms))
 total=a+b+c+d
 return times(3000,add(times(F(1499,750),fraction(total,total)),times(-1,G)))

pair_cases=[]
for v in range(3):
 for d in range(5):
  # 1/3 times the six pair payoffs: d(4-d) singles and C(d,2) doubles.
  pair=add(fraction(F(d*(4-d),3),v+1),fraction(F(d*(d-1),3),v+2),delta_two(v))
  row=times(3,add(pair,times(-1,fraction(d,d))))
  if any(x<0 for x in row):raise ValueError(('pair',v,d,row))
  pair_cases.append({'prefix_membership_count':v,'comparison_membership_count':d,'coefficients_3D4':[str(x) for x in row]})
last_cases=[]
for v in range(4):
 for d in range(5):
  row=add(fraction(d,v+1),delta_three(v),times(-1,fraction(d,d)))
  if any(x<0 for x in row):raise ValueError(('last',v,d,row))
  last_cases.append({'prefix_membership_count':v,'comparison_membership_count':d,'coefficients_D4':[str(x) for x in row]})
rho_rows={}
for bits in product(range(2),repeat=7):
 row=four_rho(*bits)
 if row[4] or any(x<0 for x in row):raise ValueError(('rho',bits,row))
 if any(x.denominator!=1 for x in row):raise ValueError(('nonintegral',bits,row))
 rho_rows[''.join(map(str,bits))]=[int(x) for x in row[:4]]
report={'claim_review':'CA-FOUR-REMAINING-PROFIT-1499-750',
        'method':'complete exact polynomial division from original SPE slack definitions and repaired P/E inequalities',
        'profit_objective':'max over four legal comparison topics of sum_x comparison_count/(background+comparison_count)',
        'pair_comparison_cases':pair_cases,'last_comparison_cases':last_cases,
        'rho_membership_cases':len(rho_rows),'scaled_rho_coefficients_3000D4':rho_rows,
        'all_coefficients_nonnegative':True,'all_nonnegative_real_backgrounds_covered':True,
        'rho_degree_at_most_three':True,'slack_weight_sum_on_negative_comparison_profit':'(354+646)/1000=1',
        'minimum_scaled_rho_coefficients':[min(row[j] for row in rho_rows.values()) for j in range(4)]}
root = Path(__file__).resolve().parents[2]
report.update(python_version=platform.python_version(),
              base_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              replay_commands=['python3 tests/audits/customer_attraction_four_remaining_independent.py'],
              randomness='none; all legal membership types enumerated')
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args = parser.parse_args()
if args.output:
    if args.output.exists(): raise FileExistsError('refusing to overwrite frozen evidence')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
