# Saddle price law, terminal demand, and the variance-transfer gap

2026-10-25, tree11 follow-up requested by root. Arbitrary finite common
catalog, arbitrary unit providers/clients, complete original ordered-history
pure SPE. **Shared-load payment and Q-CAG-HALF remain OPEN.**

This attempt uses the actual shared minimax saddle, rather than an arbitrary
query p. It obtains an exact descendant-IC covariance relation with its
variance-transfer term, but no new actual-bank payment. The previous
[independent review](shared_load_independent_review.md) supplies the shared
domain, reciprocal tangent, and KKT conventions.

## 1. Additional identities at the genuine saddle

Let (p*,L*) be a saddle of max_p min_(L in K) F_p(L), with value gamma. Set
t_x=(1+L*_x)^-1, rho_x=Pr_(p*)[x in A], and v_A=t 1_A. Then

    g_t(A)=1 dot v_A<=gamma  for every legal whole theme A,
    g_t(A)=gamma            if p*(A)>0.

Thus supported query actions lie on one common affine hyperplane. This
condition alone does not sign covariance: root/aggregate11's exact insurance
saddle already has C>0. Both the Bregman error and the original whole IC
slack must be retained.

The identity t_x L*_x=1-t_x also gives the exact normalization

    (rho t^2) dot L* = gamma-E_(A~p*)||v_A||^2.       (SN)

For an original terminal profile Z with full feature vector V_Z=t c(Z), the
tangent payoff is

    v_i^t(Z)=2g_t(Z_i)-v_(Z_i) dot V_Z.

In particular a supported input action has tangent baseline 2gamma, with a
fixed symmetric positive-semidefinite collision kernel. SN and this equal
baseline are additional structure; they do not by themselves bound the
adaptive collision term.

## 2. A genuine descendant law of demand with exact variance

Fix one actual penultimate prefix, with old load beta. Let A~p* be the current
forced query and B(A) the original strategy's genuine final best response.
For independent A,A'~p*, put

    Z_A=(prefix,A,B(A)),
    Z_(A,A')=(prefix,A,B(A')).

The second profile is a legal final deviation at the real history
(prefix,A); it is not asserted to be that history's prescribed profile.
Define the genuine terminal whole-IC slack

    Gamma(A,A')=u_B(A)(Z_A)-u_B(A')(Z_(A,A'))>=0.

For any provider i in a legal terminal profile, use the exact tangent error

    E_i^t(Z)=sum_(x in Z_i)(1-t_x c_x(Z))^2/c_x(Z)>=0.

Taking the iid average of the two terminal tangent payoffs cancels their
standalone action terms, norms, and common old-background terms. Only the
symmetric input/reply collision remains. Therefore the following is exact:

    sum_x t_x^2 Cov_(A~p*)(1_(x in A),1_(x in B(A)))
      = E_A E_B(A)^t(Z_A)
          -E_(A,A') E_B(A')^t(Z_(A,A'))
          -E_(A,A') Gamma(A,A').                    (DEMAND)

DEMAND is a true joint relation between different original queries at the
same role, using complete real terminal IC rows with nonnegative iid
multipliers. It does not use customer-wise reweighting of an IC. The
fixed-t quadratic kernel is essential to this displayed covariance form;
all original reciprocal discrepancies are kept in the exact error terms.

## 3. Which error is paid by the shared-load D?

The shared-load Bregman term at this penultimate query role is

    D_current=E_A E_A^t(Z_A),

whereas DEMAND uses the final provider's error. They cannot be identified.
For one fixed background beta define the nonnegative standalone-error
function on whole legal themes

    r_beta(T)=sum_(x in T)
                 (1-t_x(beta_x+1))^2/(beta_x+1).

The common clients in A intersect B have the same final error share for the
two providers. The noncommon clients have final load beta+1. Hence exact
same-leaf cancellation gives

    E_B^t(prefix,A,B)-E_A^t(prefix,A,B)
          =r_beta(B)-r_beta(A).                   (SWAP)

Consequently DEMAND yields the proved exact relation

    Cov_terminal = D_current
                     +E_A[r_beta(B(A))-r_beta(A)]
                     -E_(A,A')E_B(A')^t(Z_(A,A'))
                     -E_(A,A')Gamma(A,A').         (DV)

The last two terms are nonnegative banks being subtracted. The additional
r_beta gap is the actual missing payment in this attempt.

The saddle law does not sign this gap. Explicitly

    r_beta(T)=F_beta(T)-2g_t(T)
                   +sum_(x in T)t_x^2(beta_x+1),
    F_beta(T)=sum_(x in T)1/(beta_x+1).

For supported A and an arbitrary legal reply B,

    r_beta(B)-r_beta(A)
      =F_beta(B)-F_beta(A)+2(gamma-g_t(B))
         +sum_x[1_B(x)-1_A(x)]t_x^2(beta_x+1).

The equal-price support cancels only the input g_t(A). The F_beta difference
and the beta-weighted norm difference are not the shared KKT objective
rho t^2 dot L. Even when the reply also has price gamma, these two terms
remain. Therefore substituting the saddle price law into DEMAND does not
prove Cov_terminal<=D_current, nor does it pay the full shared covariance.

## 4. Why simply iterating SWAP is still insufficient

There is a fixed insertion-error potential

    R_t(b)=sum_x[H_(b_x)-2t_x b_x
                      +(t_x^2/2)b_x(b_x+1)],

with marginal R_t(b+1_T)-R_t(b)=r_b(T). Its marginal is nonnegative because it
is exactly a sum of squares divided by b_x+1. Thus the r_beta difference in
SWAP is a genuine potential difference, rather than an arbitrary scalar.

Nevertheless two different original query histories need not have the same
beta or selected continuation. A rollout through the complete tree changes
both arguments of this potential. The same fixed t makes the potential
well-defined everywhere, but it does not cancel the real reset profiles.
Its value is also not bounded by the one-leaf final error alone: for one
covered client of final load c>=1,

    R_t(c)-(1-tc)^2=H_c-1-(t^2/2)c(c-1),

which can be positive even when t=1/c makes the final error zero. This is
not a new impossibility theorem; it identifies exactly why replacing all
insertion errors by the original actual squared-error bank is invalid.

## 5. Status and five-player substitution

DEMAND, SWAP, DV and the saddle normalization are all general exact relations.
They neither combine mutually exclusive branch reserves nor prove a new
welfare lower bound. For the last two roles of m=5 they give precisely DV;
the earlier three actual-prefix query covariances additionally involve
their changed genuine tails. No valid cross-action/cross-history payment of
the r_beta gaps and those tail resets was found. Thus the same general
argument still does not unconditionally prove OPT_5<=2W.

No broader auxiliary conjecture was promoted, no generic finite scan was
used as evidence, and no claim was made that the exact original strategy is
an equilibrium of the tangent game. The informative stop is the explicit
standalone-error potential gap in DV, which must be jointly paid together
with earlier real resets to make this law-of-demand approach close.

Direct11 independently checked sections 2--4 after the derivation was saved:
the iid cancellation, original-IC signs, SWAP, r_beta expansion and R_t
marginal all check. The initial weaker inequality DV was tightened to the
exact equality above because every term is retained. This internal check
does not verify any unproved covariance payment or external novelty claim.
