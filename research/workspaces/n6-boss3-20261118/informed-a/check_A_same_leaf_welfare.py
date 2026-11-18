"""Exact algebra checks for a direct application of an existing theorem."""
from fractions import Fraction as F
from pathlib import Path
import json
rows=[]
for k in range(5):
 slack=F(k+2)-F(6*k,k+1)
 assert slack==F((k-1)*(k-2),k+1) and slack>=0
 rows.append({'k':k,'integer_capacity_slack':str(slack)})
# Coordinates D,V1,K,Iold,Inew.
Q=[F(2),F(5,3),F(-4),F(0),F(0)]
S=[F(0),F(-6),F(4),F(1),F(0)]
L=[F(0),F(0),F(4),F(-1),F(-1)]
R=[F(-1),F(0),F(0),F(0),F(1)]
combo=[18*Q[i]+5*S[i]+5*L[i]+5*R[i] for i in range(5)]
assert combo==[F(31),F(0),F(-32),F(0),F(0)]
answer={'scope':'integer inequality and coefficient identity only; formal binary-four-tail theorem is a mature cited premise',
        'integer_rows':rows,'coordinates':['D','V1','K','Iold','Inew'],'combined_coefficients':[str(v) for v in combo],
        'new_coverage_per_K':'32/31','total_welfare_per_K':'94/31'}
p=Path(__file__).resolve().with_name('A-same-leaf-welfare-check.json');p.write_text(json.dumps(answer,indent=2)+'\n')
print(json.dumps(answer,indent=2))
