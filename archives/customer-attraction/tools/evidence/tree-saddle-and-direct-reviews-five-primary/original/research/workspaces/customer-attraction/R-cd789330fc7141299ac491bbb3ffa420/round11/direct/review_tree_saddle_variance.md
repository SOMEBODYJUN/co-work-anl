# Independent algebra review of tree11 terminal variance transfer

2026-10-25, direct11. Reviewed ../tree/saddle_price_law_and_variance_attempt.md
sections 2–4 from original reciprocal utilities and a fixed feature vector t.
All relations retain legal full-topic terminal IC and original history rules.
No half-coverage or common-bank payment is endorsed.

At fixed old load beta, let a=t 1_A and b=t 1_B. The follower's exact tangent
payoff is

    2 g_t(B)−b dot (t beta)−b dot a−||b||^2.

For A iid p and original B(A), all terms except the input/reply collision have
the same expectation if B(A) is replaced by the independent B(A'). Thus the
expected own-minus-cross tangent difference is exactly −Cov_t(A,B(A)).
Original follower best response gives a nonnegative full-utility Gamma at
each real history (prefix,A). Writing original utility as tangent plus exact
square error gives

    Cov_t=E E_B^t(own)−E E_B^t(cross)−E Gamma.

This verifies DEMAND, including sign and coefficient. No per-client weighted
IC was used.

In the same own leaf (prefix,A,B), the two actors' error terms agree on
A intersect B. For a noncommon client the final load is beta+1. Hence

    E_B^t−E_A^t=r_beta(B)−r_beta(A),
    r_beta(T)=sum_(x in T)(1−t_x(beta_x+1))^2/(beta_x+1).

This verifies SWAP. Substitution into DEMAND gives an exact equality for tree's
DV right side when all displayed terms are retained; the stated inequality is
therefore valid but weaker. The current-role shared-load D is E E_A^t(own),
so follower-own error cannot be silently substituted for it.

Expansion gives r_beta=F_beta−2g_t+sum_T t^2(beta+1), as stated. The insertion
potential R_t(b)=sum_x[H_b−2tb+t^2 b(b+1)/2] has marginal r_b(T), a sum of
nonnegative squares. For a positive final load c,

    R_t(c)−(1−tc)^2=H_c−1−t^2 c(c−1)/2.

This also verifies the claimed failure of automatic final-error domination;
the formula comparing to (1−tc)^2 is stated here for c>=1. The c=0 convention
for an unserved-client final error needs separate handling and is not used.

The remaining mean r_beta(B(A))−r_beta(A) and changed earlier-history resets
have no payment from the single actual W in this argument. Equal saddle theme
price cancels the g_t term only; it does not cancel F_beta or the beta-weighted
norm. The result is a valid general algebraic interface, not covariance closure.
