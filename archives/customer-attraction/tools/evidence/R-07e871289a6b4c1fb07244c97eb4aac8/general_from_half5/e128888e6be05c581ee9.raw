"""Independent Fraction checks of the tail bridge and its all-k closed form.

Analytic proof (valid for every nonnegative integer b and every k>=2):
  H_1,...,H_{k-2},R follow the forced T, and z=sum 1_{H_j}.
  With B=b+z, U_B(T,R)-U_B(R,T)=f_B(T)-f_B(R).
  Consequently, source IC + last IC + K-|R| plus sum_R B/(B+1)
  is exactly v+K-f_B(T)-U_B(Q,T), proving that expression nonnegative.
  Since z<=k-2 and both f_B(T),U_B(Q,T) decrease in B,
  v+K >= sum_x [t/(b+k-1)+q/(b+k-1+t)].

Equivalent exact minimization of the generic hidden-bit projection:
  raw(s,g)=(t-g)/(b+t+s+g)+g+q/(b+t+s+1)
          =t/(b+s+1)+q/(b+s+t+1)+g*(b+s)/(b+s+1).
  Thus g=0 minimizes it at fixed s. Increasing s decreases the first
  two terms, so the minimum is at s=k-2. These algebraic identities
  prove the claim for all k; the finite tests below are regression checks.
"""
from fractions import Fraction as F
from itertools import product
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--k-max',type=int,default=25)
parser.add_argument('--b-max',type=int,default=50)
args=parser.parse_args()
def share(bit,den):return F(bit,den) if bit else F()
count=0
for b in range(1001):
    for t,q,r in product(range(2),repeat=3):
        # Actual strategic slacks remain abstract; verify the exact client residual.
        u_tr=share(t,b+t+r);u_rt=share(r,b+t+r)
        f_t=F(t,b+1);f_r=F(r,b+1)
        residual=u_tr+r-u_rt-f_t
        assert residual==F(b*r,b+1) and residual>=0
        assert u_tr+f_r-u_rt-f_t==0
        # The actual client's bit q is unrestricted and drops out of the identity.
        count+=1
print({'exact_case_checks':count,'b_values':1001,
       'identity':'U(T,R)+|R|-U(R,T)-f_b(T) = sum_R b/(b+1)',
       'stronger_identity':'U(T,R)+f_b(R)-U(R,T) = f_b(T)'})

hidden_checks=0;min_checks=0
for k in range(2,args.k_max+1):
    for b in range(args.b_max+1):
        for t,q in product(range(2),repeat=2):
            target=F(t,b+k-1)+F(q,b+k-1+t)
            vals=[]
            for s in range(k-1):
                core=F(t,b+s+1)+F(q,b+s+t+1)
                for g in range(2):
                    raw=share(t-g,b+t+s+g)+g+F(q,b+t+s+1)
                    assert raw==core+F(g*(b+s),b+s+1)
                    assert raw>=target
                    vals.append(raw);hidden_checks+=1
                if s<k-2:
                    next_core=F(t,b+s+2)+F(q,b+s+t+2)
                    assert core-next_core==F(t,(b+s+1)*(b+s+2))+F(q,(b+s+t+1)*(b+s+t+2))
            assert min(vals)==target;min_checks+=1
print({'k_range':[2,args.k_max],'b_range':[0,args.b_max],
       'hidden_count_cases':hidden_checks,'exact_minima_checked':min_checks,
       'closed_form':'t/(b+k-1)+q/(b+k-1+t)',
       'scope':'The algebraic proof is all k; these parameter sweeps are finite checks.'})
