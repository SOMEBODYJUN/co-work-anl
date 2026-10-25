# Canonical mean floors and the exact first-tail reset relation

2026-10-25, credible12. Root proposed the canonical mean-floor enlargement;
this note independently checks its endpoint criterion and dual, then
derives the reset identity below. Tree12's independently saved domain check
was read after the reconstruction. Original arbitrary-m Q-CAG-HALF stays
**OPEN**; neither the new credit nor reset identity establishes HALF.

## 1. Exact ordered endpoint criterion

Let R(h) be all ordered terminal paths realizable by a complete pure SPE
after exact history h. For current role k define the old canonical threshold

    M(h)=max_A min_(z in R(h,A)) u_k(z).

For any ordered terminal z extending h,

    z in R(h) iff u_k(z)>=M(z_<k) at every suffix role k.     (IFF)

Necessity follows from original node IC: each prescribed alternative child
gives at least its minimum possible current payoff. For sufficiency,
construct the selected z branch backward; at each offpath sibling paste a
complete child SPE minimizing the current player's payoff. The displayed
threshold dominates all those minima. Different ordered children are
disjoint, so the pasted policies are simultaneously compatible. This is
the established exact-solver/credible-continuation mechanism, not a new
pointwise endpoint theorem.

After role i has been FORCED to A, the criterion applies only at k>i.
The entering role i is not required to best respond. Adding its M(h_i)
floor would incorrectly restrict the forced-child domain.

## 2. Mean-floor analytical domain and dual

For each role i, consider raw tagged terminal tails after its actual prefix
and a forced entering action. For strict-future ordered history h with
current role k set

    Delta_ih(z)=1_(z extends h)[M(h)-u_k(z)].

The virtual endpoint lottery q is constrained by

    E_q d_i(z)<=u_i,       E_q Delta_ih(z)<=0 for every h.   (MF)

This finite LP domain is nonempty: original sigma supplies source records
with pointwise entering caps and all strict-future Delta<=0. Its loads are
legal fractional catalog backgrounds. It need not be any pure or mixed
SPE completion; conditional mean floors are weaker than IFF leafwise.

For shadow a>=0 and deleted load ell_i, finite LP duality gives

    H_i=eta_i+mu_i u_i,
    r_i(z)=eta_i+mu_i d_i(z)
             +sum_h lambda_ih Delta_ih(z)-a dot ell_i(z)>=0,  (DUAL)
    mu_i>=0, lambda_ih>=0, eta_i unrestricted.

The signs are fixed by subtracting mu(d-u_i) and lambda Delta from the
maximization objective. Unlike the credible-endpoint-only dual, DUAL prices
every ALLOWED raw terminal, including a non-SPE unilateral-reset leaf.

If actual-action tags remain fixed to the original endpoint, this leaves
an actual-tag exception: a changed tail with the same entering actual tag
is not in that row. The identities below require both states to be allowed.
Freeing actual tags is a distinct but legitimate analytical enlargement;
original source leaves remain fixed, and no pure completion is claimed.
Canonical future-floor constraints still apply, so the old all-terminal
unfiltered all-copy collapse is not inferred for this new domain.

For ORIGINAL source queries, I_i=u_i-E_p d_i^0>=0 and Delta_ih<=0. At the
shared optimizer, the KKT gap therefore has the exact bank

    G=sum_i mu_i I_i+R+S,
    R=sum_i E_p r_i(z_i^0(A))>=0,
    S=-sum_(i,h)lambda_ih E_p Delta_ih(z_i^0(A))>=0.          (CREDIT)

This subdivides the one KKT gap G; it is not an additional independent
second copy of G. Background-selected mean floors do not fund source
floors at different histories. A history not reached by original sources
has no original S inventory, even if its dual lambda is positive.

## 3. A true deviation and its exact reset cost

Fix one original source child-SPE witness z after forced role i. At future
role j>i, deviate once and follow that SAME witness strategy, giving z'.
Both leaves retain the entering role and its action. Put

    Gamma_j=u_j(z)-u_j(z')>=0,
    U_i(y)=sum_(k>i)lambda_(i,y_<k)[M(y_<k)-u_k(y)],
    S_desc(y)=sum_(k>j)lambda_(i,y_<k)[u_k(y)-M(y_<k)].

Both source and new descendants k>j lie on genuine sub-SPE continuations,
so S_desc(z),S_desc(z')>=0. Before j the histories coincide. Thus for
i<k<j the floor change is exactly the old player's payoff loss, while at
j it is exactly Gamma_j. Therefore

    U_i(z')-U_i(z)
      =lambda_(i,z_<j) Gamma_j
       +sum_(i<k<j)lambda_(i,z_<k)[u_k(z)-u_k(z')]
       +S_desc(z)-S_desc(z').                              (FLOOR-RESET)

From DUAL's definition of r, this gives the exact all-input relation

    a dot(ell_i(z')-ell_i(z))
      =mu_i[d_i(z')-d_i(z)]
       +lambda_(i,z_<j) Gamma_j
       +sum_(i<k<j)lambda_(i,z_<k)[u_k(z)-u_k(z')]
       +S_desc(z)-S_desc(z')+r_i(z)-r_i(z').                 (RESET)

In particular for the FIRST future mover j=i+1, the ancestor sum is empty.
Dropping the two nonnegative terminal terms gives the positive upper bound

    a dot(ell_i(z')-ell_i(z))
      <=mu_i[d_i(z')-d_i(z)]
        +lambda_(i,z_<j) Gamma_j+S_desc(z)+r_i(z).           (FIRST)

The root profit change is signed and is explicitly priced. Gamma is the
genuine original witness IC gap, not a canonical floor comparison in a
different game. For a later deviator the weighted ancestor losses may have
either sign and must remain in RESET; they are not covered merely by
lambda Gamma. No absolute-value or positive-part bound is asserted.

There is also a sharper direct excess form relative to the row budget H_i.
Write `s_k(z)=u_k(z)-M(z_<k)>=0`. DUAL applied to z' gives

    a dot ell_i(z')-H_i
      <=mu_i[d_i(z')-u_i]
       +sum_(i<k<j)lambda_(i,z_<k)[u_k(z)-u_k(z')-s_k(z)]
       +lambda_(i,z_<j)[Gamma_j-s_j(z)]-S_desc(z').         (EXCESS)

For FIRST j=i+1 this has no intermediate ancestor term, so

    a dot ell_i(z')-H_i
      <=mu_i[d_i(z')-u_i]
        +lambda_(i,z_<j)[Gamma_j-s_j(z)].                  (FIRST-EXCESS)

Thus the canonical source slack subtracts from the true IC gap. The
entering cap overshoot remains signed and priced; it is not assumed
nonpositive for an arbitrary reset. EXCESS follows from the same exact
U(z') decomposition and dropping only the nonnegative reduced cost r(z').
It does not need to identify the changed descendants' histories with the
source descendants. This is a quantitative first-reset bound, not a claim
that arbitrary covariance demand consists of such resets.

## 4. All-m application and remaining amount

RESET/FIRST are valid on all original instances and for every allowed
source/reset pair. They give a concrete first-tail cost relation, but do
not show that an arbitrary covariance demand decomposes into these edges
with compatible row identities, reach probabilities and one-time use of
S and R. Reindexing an actual-tag reset to its later first-deviation row
changes mu,lambda and its wallet; that transport is still unpaid.

For m=5 the same identities apply to every catalog and complete SPE, but
neither the necessary covariance edge decomposition nor the weighted
ancestor-loss payment has been established. There is no unconditional
five-player or all-m HALF conclusion. No finite scan was used here.
