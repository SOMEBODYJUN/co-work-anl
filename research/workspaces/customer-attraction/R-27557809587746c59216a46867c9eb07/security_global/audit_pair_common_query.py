"""Exact membership audit of the two pointwise inequalities.
Finite checks support the code; the general proof is in pair_common_query.md.
"""
from fractions import Fraction as F
from itertools import product

def val(u,v,b):return F(int(u),1)/(b+1+int(v))
count=0
for b in [F(0),F(1,3),F(1),F(7,2),F(100)]:
 for A,B,D,T in product([False,True],repeat=4):
  assert val(T,A,b)+val(T,B,b)<=2*val(T,D,b)+val(D,A,b)
  assert val(T,B,b)-val(T,A,b)<=val(A,B,b)
  count+=1
print({'pointwise_checks':2*count,'status':'pass','scope':'finite exact membership audit; universal proof in Markdown'})
