"""Definition-level exact audit of the raw23-client core used by the
P^k LAST counterfamily. No optimization, parameter search, or SPE construction.
The complete P-padding strategy is an external analytic dependency.
"""
from fractions import Fraction as F
from pathlib import Path
import json
blocks=[([0],3),([1],4),([2,3],6),([2,4],6),([0,3,4],2),([1,3,4],2)]
clients=[set(B) for B,n in blocks for _ in range(n)]
prefix=[0,1]
K=[[sum((F(1,1+sum(a in C for a in prefix)+int(A in C)) for C in clients if T in C),F(0)) for A in range(5)] for T in range(5)]
t=[sum((F(1,(1+sum(a in C for a in prefix))*(2+sum(a in C for a in prefix))) for C in clients if A in C),F(0)) for A in range(5)]
tau=sum((F(sum(a in C for a in prefix),1+sum(a in C for a in prefix)) for C in clients),F(0))
assert K[2]==list(map(F,[12,12,6,9,9]))
assert [K[T][2] for T in range(5)]==[F(5,2),F(3),F(6),F(5),F(5)]
assert t==[F(5,6),F(1),F(6),F(11,3),F(11,3)]
assert tau==F(11,2)
security=[sum((F(1,1+sum(a in C for a in [2,3,4])) for C in clients if T in C),F(0)) for T in range(5)]
assert security==[F(11,3),F(14,3),F(4),F(10,3),F(10,3)]
assert max(security)<5
# A single prescribed boundary substitution cross-checks the general formulas.
k=22;m=k+3;W=5*k+23
tP=F(5*k,(k+1)*(k+2))
col_costs=[m*x+y for x,y in zip(K[2]+[F(12)],t+[tP])]
assert min(col_costs)==6*m+6 and col_costs.index(min(col_costs))==2
B=6*m+tau+F(5*k*k,k+1)+6
assert B-2*W==F(33,46)
assert F(2*k*k-41*k-33,2*(k+1))==B-2*W
out={'scope':'Static K,t,allQ row-certificate and pure security certificate only; not a full-SPE audit.',
 'core_clients':len(clients),'core_K':[[str(v) for v in row] for row in K],
 'core_t':list(map(str,t)),'core_tau':str(tau),
 'pure_security_core_234':list(map(str,security)),
 'all_k_security_upper':5,'all_k_aggregate_security_slack_lower':8,
 'boundary_k':k,'boundary_augmented_minus_2W':str(B-2*W),
 'boundary_all_column_costs':list(map(str,col_costs))}
Path(__file__).with_name('retained_tax_raw_core_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_exact_checks_pass':True,'boundary_gap':str(B-2*W),'pure_core_security_cap':str(max(security))},indent=2))
