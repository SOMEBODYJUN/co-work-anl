# Reset-complete mean floor domain: independent check

2026-10-25, tree12. Root supplied the proposed relaxation and requested the
endpoint characterization, domain and dual signs be attacked. General
arbitrary-player/common-catalog/all-history HALF remains **OPEN**.

Let R(h) be the set of endpoint profiles realizable by a complete pure SPE
after exact ordered history h. If current role is k, define the old credible
threshold

    M(h)=max_A min_(z in R(h,A)) u_k(z).

The finite minima and maxima exist. For any legal terminal z extending h,

    z in R(h) iff u_k(z)>=M(z_<k) at every suffix decision k. (FLOOR-IFF)

Necessity: the selected child endpoint belongs to its child R; current IC
compares its payoff to every other child's selected payoff, each at least
that child's minimum. Sufficiency follows by backward induction down z's
selected path, then pasting minimizing child SPEs independently at every
offpath sibling. This is the established credible endpoint/min-pasting
mechanism; the new proposal is its analytical mean-floor relaxation.

For a row where role i is already forced to A, impose FLOORS only at strict
future roles k>i. The entering action is fixed and need not be a best reply;
putting its floor M(h_i) into the forced-child domain would be wrong.

Let q range over ALL raw terminal tails after the entering actual prefix,
with actual-action tag restricted to the original actual endpoint, and set

    Delta_h(z)=1_(z extends h)[M(h)-u_k(z)],
    E_q d_i(z)<=u_i,
    E_q Delta_h(z)<=0   for each strict-future ordered history h.

This is a nonempty compact finite LP domain containing all earlier capped
credible endpoint lotteries. Original sigma witnesses feasibility. It is
an analytical superset, not generally conv(R), and not claimed to implement
a pure or unaugmented mixed SPE. A mixture can offset a positive floor
deficit by surplus inside the SAME ordered history; histories are not merged.

For shadow score s(z), the maximization LP has dual mu>=0, lambda_h>=0,
eta in R, with

    H=eta+mu u_i,
    s(z)<=eta+mu d_i(z)+sum_h lambda_h Delta_h(z)
                    for EVERY ALLOWED raw tagged terminal z. (ALL-PRICE)

The signs follow by subtracting mu(d-u_i) and lambda_h Delta_h in the
maximization Lagrangian. Unlike a dual restricted to credible endpoints,
ALL-PRICE applies to all offactual-tagged unilateral deviation/reset leaves,
even those failing to be child-SPE endpoints. It explicitly charges their
floor deficits. There remains an actual-tag exception: when A=a_i is fixed
to the original endpoint, a changed-tail leaf bearing that same entering
tag is excluded and is not priced by this row's dual. Such a leaf can be
reindexed to its later FIRST actual deviation row, where it is allowed,
but that changes its dual coefficients and wallet and needs explicit
transport. Freeing actual tags is a separate analytical enlargement.

For an ORIGINAL source query z_i^0(A), all strict-future Delta_h<=0. Define

    R_i(A)=eta_i+mu_i d_i^0(A)
                    +sum_h lambda_ih Delta_h(z_i^0(A))-s(z_i^0(A))>=0,
    I_i=u_i-E_p d_i^0(A)>=0.

The corresponding shared KKT gap decomposes exactly as

    G=sum_i mu_i I_i
        +sum_(i,h)lambda_ih E_p[1_h(z_i^0(A))(u_k(z_i^0(A))-M(h))]
        +sum_i E_pR_i(A).                            (FLOOR-CREDIT)

Every displayed bank is nonnegative. FLOORS must include every affected
ancestor of a reset, not only its unilateral deviator: changing a later tail
can change every earlier on-path player's payoff and break earlier floors.

The remaining amount is not supplied by this exact dual. A proof must map
the aggregate positive Delta_h of the reset leaves it uses to these SAME
original floor-surplus/reduced-cost banks, with compatible reach masses and
no repeated spending. A history with no original source reach has no such
original floor-surplus bank, even though its lambda_h may be positive.
Selected-background complementary slackness also does not create extra
money: for a positive lambda_h its selected mean Delta_h is zero, allowing
positive deficits to balance negative slack but not bounding arbitrary new
reset demand. No such joint reset transport was proved here.

Thus the relaxation removes the earlier *credential-domain* obstruction for
allowed offactual-tagged resets, while the actual-tag reindexing and
financial capacity/reuse problems remain. All
identities apply unchanged for m=5; no unconditional m=5 or general HALF
amount follows.
