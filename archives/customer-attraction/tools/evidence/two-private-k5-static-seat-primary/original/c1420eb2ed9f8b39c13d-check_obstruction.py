from fractions import Fraction as F
from itertools import combinations
# Exact checks for the K5 mixed-private pattern described in the note.
assert F(4,6)==F(2,3)
nu=F(2,3)
assert sum(1 for k in range(1,7) if F(1,k)>nu)==1
# primal lower bound: each edge y_j+y_k>=6 in K5; summing all 10 edges gives 4 sum(y)>=60.
# hence sum(y)>=15; private lower bounds add 4.
edge_count=len(list(combinations(range(5),2)))
assert edge_count==10
assert F(6*edge_count,4)==15
primal_lower=F(4)+F(15)
assert primal_lower==19>12
# dual: mu=1/4 on each edge, vertex load=4/4=1; private lambda=1.
assert F(4,4)==1
assert F(4)+F(6*edge_count,4)==19
print({'nu':str(nu),'a_private':2,'K5_edge_count':edge_count,'min_sum_y':str(primal_lower),'two_n':12,'status':'exact'})
