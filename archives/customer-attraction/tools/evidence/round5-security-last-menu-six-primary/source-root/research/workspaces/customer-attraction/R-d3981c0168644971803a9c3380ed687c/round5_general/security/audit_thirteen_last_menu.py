"""Exact LAST-menu certificate on the already known13-player tax witness.
This audits the finite static comparison only; complete SPE is inherited from
its old112050-comparison certificate, not re-audited here. No optimization.
"""
from fractions import Fraction as F
from pathlib import Path
import json
names=['A','B','T','D','E','P']
blocks=[([0],2),([1],2),([2],1),([2,3],1),([2,4],1),([0,3,4],3),([1,3,4],1),([5],25)]
customers=[set(A) for A,n in blocks for _ in range(n)]
z=[5]*10+[0,0,1];prefix=z[:-1]
p=[F(0),F(1,3),F(1,3),F(1,6),F(1,6),F(0)];q=p

def utility(profile,i):
 return sum((F(1,sum(a in C for a in profile)) for C in customers if profile[i] in C),F(0))
K=[[sum((F(1,1+sum(a in C for a in prefix)+int(A in C)) for C in customers if T in C),F(0)) for A in range(6)] for T in range(6)]
rows=[sum(K[T][A]*q[A] for A in range(6)) for T in range(6)]
columns=[sum(p[T]*K[T][A] for T in range(6)) for A in range(6)]
L=F(7,3)
assert max(rows)==min(columns)==L
us=[utility(z,i) for i in range(13)]
assert all(u>=L for u in us)
assert sum(us)==33
out={'claim':'Only this known exact witness passes LAST and its individual strengthening; no general conclusion',
 'names':names,'actual_path':z,'row_and_column_distribution':list(map(str,p)),
 'K':[[str(x) for x in row] for row in K],
 'pure_query_returns_against_q':list(map(str,rows)),
 'mixed_query_returns_against_pure_columns':list(map(str,columns)),
 'exact_L':str(L),'actual_profits':list(map(str,us)),
 'W':33,'individual_minimum_margin':str(min(us)-L),'aggregate_margin_W_minus_mL':str(sum(us)-13*L)}
Path(__file__).with_name('thirteen_last_menu_exact.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['pure_query_returns_against_q','mixed_query_returns_against_pure_columns','exact_L','individual_minimum_margin','aggregate_margin_W_minus_mL']},indent=2))
