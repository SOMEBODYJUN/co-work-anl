"""Implementation regression of the proved source-stopping parity formulas."""
from pathlib import Path
from fractions import Fraction as F
import json
rows=[]
for k in range(4,101):
 good=[i for i in range(1,k+1) if k>=2*(k-i+2)]
 assert len(good)==k//2-1
 cost=12*len(good)+6;gap=k-8
 assert cost==(6*k-6 if k%2==0 else 6*k-12)
 assert cost-gap==(5*k+2 if k%2==0 else 5*k-4)>0
 if k in [4,5,9,10,99,100]:rows.append(dict(k=k,positions=len(good),cost_lower=cost,old_gap=gap))
out={'scope':'Finite arithmetic regression of analytic position/parity formulas; no SPE enumeration or universal proof.',
 'bound_minus_gap_even':'5k+2','bound_minus_gap_odd':'5k-4','rows':rows,
 'm5_conditional_security_factor':str(F(2*5-1,5))}
Path(__file__).with_name('pair_source_arithmetic.json').write_text(json.dumps(out,indent=2)+'\n')
print('Position count, parity difference and reverse gap verified.')
