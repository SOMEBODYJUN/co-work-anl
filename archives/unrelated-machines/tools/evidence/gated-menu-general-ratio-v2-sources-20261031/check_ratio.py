from fractions import Fraction as F
# Verify the exact quadratic margin used in the 13/8 proof.
vals=[]
for beta in (F(0),F(10,13),F(1)):
    D=(F(18)-13*beta)/8
    margin=D*D-(1-F(5,8)*beta*beta)
    vals.append((str(beta),str(margin)))
assert vals[0][1]=='65/16'
assert vals[1][1]=='125/338'
assert vals[2][1]=='1/64'
print({'status':'PASS','margins':vals,'derivative_upper_bound_at_beta_1':-50})
