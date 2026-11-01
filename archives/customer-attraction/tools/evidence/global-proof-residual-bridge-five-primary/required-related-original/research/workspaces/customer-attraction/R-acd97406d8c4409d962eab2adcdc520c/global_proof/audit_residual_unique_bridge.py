from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import json
from pathlib import Path
BASE=Path(__file__).resolve().parent
TYPES={1:10,2:13,4:8,12:5,20:5,25:6,26:4,30:1,32:8,40:5,48:5,58:1}
REPLY=(1,3,3,4,3,4)
def pays(path):
 return tuple(sum((F(w,sum(bool(mask>>t&1) for t in path)) for mask,w in TYPES.items() if mask>>a&1),F(0)) for a in path)
def cov(path):return {mask for mask in TYPES if any(mask>>a&1 for a in path)}
def welfare(path):return sum(TYPES[mask] for mask in cov(path))
rows=[]
for a in range(6):
 vals=[pays((a,b))[1] for b in range(6)]
 assert vals[REPLY[a]]==max(vals)
 rows.append([str(v) for v in vals])
root=[pays((a,REPLY[a]))[0] for a in range(6)]
assert root[0]==max(root)
assert pays((0,1))==(16,19)
assert welfare((0,1))==35
best=max(welfare(pair) for pair in combinations_with_replacement(range(6),2))
bestpairs=[pair for pair in combinations_with_replacement(range(6),2) if welfare(pair)==best]
assert best==38 and bestpairs==[(2,5)]
assert welfare((2,5))==38
assert sum(TYPES[t] for t in cov((2,5))-cov((0,1)))==36
print(json.dumps({'customers':sum(TYPES.values()),'second_payoff_rows':rows,'first_true_values':list(map(str,root)),'actual':{'path':[0,1],'W':35,'u':[16,19]},'comparison':[2,5],'comparison_uncovered':36,'OPT':best,'optimal_pairs':bestpairs,'all_pairs':{str(pair):welfare(pair) for pair in combinations_with_replacement(range(6),2)}},indent=2))
