# Uniform floor prices: copy cancellation and a balanced swap bound

2026-10-25, credible12. Root proposed the uniform-cost analytical domain;
this branch checks its scope and derives the order-swap component below.
The result is valid on arbitrary original CAG inputs and all player counts,
with no fixed-size computation. **Original HALF remains OPEN.** The
balanced-flow condition and its source inventory have not been constructed
for the shared-saddle covariance.

Tree12 independently checked reset signs, SWAP, the factor 1/2, balance
and source capacity in `../tree/uniform_swap_and_raw_flow_independent_review.md`;
no fatal issue was found. This is internal review, not a completed HALF
application or external novelty certification.

## 1. One explicit cost, rather than assumed multiplier normalization

Fix actual prefix h_i, actual utility u_i and a raw ordered terminal tail z.
The entering action may be any legal A, including the original actual
action: actual tags are analytically freed. Let d_i(z) be entering utility,
ell_i(z) its deleted-slot load, and

    C_i(z)=d_i(z)+sum_(k>i)[M(z_<k)-u_k(z)].

Allow raw terminal lotteries with the ONE constraint E C_i<=u_i. This is
a nonempty compact analytical domain of legal fractional catalog loads.
An original source child SPE has future surplus

    S_i(z)=sum_(k>i)[u_k(z)-M(z_<k)]>=0,
    C_i(z)=d_i(z)-S_i(z)<=d_i(z)<=u_i.

It therefore witnesses feasibility. This domain is larger than separate
root mean caps and conditional mean floors; no new pure or mixed SPE
completion is claimed. Uniform floor prices arise by construction, not by
normalizing an arbitrary history-dependent dual.

For a shared shadow a, its row LP gives mu_i>=0 and eta_i with

    H_i=eta_i+mu_i u_i,
    r_i(z)=eta_i+mu_i C_i(z)-a dot ell_i(z)>=0
                                        for EVERY raw terminal z. (U)

Keeping ORIGINAL source queries, the KKT gap is exactly

    G=sum_i mu_i I_i+sum_i mu_i E_p S_i(z_i^0(A))
                       +sum_i E_p r_i(z_i^0(A)),
    I_i=u_i-E_p d_i^0(A)>=0.

All three terms are nonnegative. The scalar price mu_i multiplies every
future floor only because the primal cost C_i explicitly combined them.
This is one decomposition of G, not independent extra money in addition
to G. The reduced cost r below belongs to this uniform-cost domain.

For a COMMON price across different rows, use an explicit single total
constraint `sum_i E C_i<=W`, with each row lottery normalized. Original
sources are feasible because `sum_i E C_i<=sum_i E d_i<=W`. Its finite LP
has one mu>=0 and row-normalization eta_i, not arbitrarily normalized old
prices. Its exact gap is `G=mu sum_i I_i+mu sum_i E S_i+R`.
Thus common mu can be constructed with ONE actual W budget. It does not
by itself cancel row-dependent canonical threshold potentials.

## 2. A genuine copy reset cancels the current reset shares

Let z be a genuine source child-SPE leaf. At future role j>i, let that
player deviate to the entering action A and follow the same genuine
strategy, producing z'. In z' the entrant and deviator both choose A, so

    d_i(z')=u_j(z'),
    [d_i(z')-d_i(z)]+Gamma_j=u_j(z)-d_i(z),
    Gamma_j=u_j(z)-u_j(z')>=0.                         (COPY)

This is exact same-leaf equality of equal-action unit providers. No
cross-branch old-player equality is used.

Write S_desc for canonical floor surplus of roles k>j in the respective
leaf. New descendants follow genuine sub-SPEs, so S_desc(z')>=0. Directly
in the uniform cost,

    C_i(z')=M(z_<j)
        +sum_(i<k<j)[M(z_<k)-u_k(z')]-S_desc(z').      (CCOST)

In particular FIRST j=i+1 gives

    C_i(z')=M(h_i,A)-S_desc(z')<=M(h_i,A).

The entering share and copying mover's share cancel absolutely. Later
resets retain the signed intermediate-prefix floor deficits in CCOST.

## 3. Raw order swap preserves all deeper counts and floors

Take i<m and any raw leaf written `(h_i,A,B,Y)`. Put

    z=(h_i,A,B,Y),    zswap=(h_i,B,A,Y),
    d=u_i(z),        v=u_(i+1)(z),
    K_i(T)=M(h_i,T), P_i(T)=a dot 1_T+mu_i K_i(T).

Both leaves are in the raw domain underlying (U), irrespective of whether
the swapped first follower is best responding. Their final counts are
identical. After the first two positions their prefix counts are also
identical. Canonical M is equal for count-isomorphic subgames: future
payoffs depend on prefix loads and the common catalog, and the set of all
complete-history pure continuations is carried bijectively by the
isomorphism. This does not restrict a fixed strategy's tie choices to be
count-dependent.

The root/follower terminal payoffs swap, later payoffs and deeper canonical
floors match, and deleted loads differ only by the removed entering action.
Consequently

    C_i(zswap)-C_i(z)=2(v-d)+K_i(B)-K_i(A),
    a dot[ell_i(zswap)-ell_i(z)]=a dot(1_A-1_B).

Substitution in (U) gives the exact relation

    r_i(zswap)-r_i(z)
      =2 mu_i(v-d)+P_i(B)-P_i(A).                    (SWAP)

There is no division by mu_i; mu_i=0 is covered. This component removes
all deeper-tail reset terms by an order swap preserving final and deeper
prefix counts. It is not a claim that the swapped leaf is itself an SPE.

## 4. A genuinely joint half-inventory bound under exact balance

Fix the SAME row i and prefix h_i. Consider finitely many source leaves
z_e=(h_i,A_e,B_e,Y_e), with weights theta_e>=0. Suppose the directed
first-follower action flow is balanced:

    sum_(e:A_e=T)theta_e=sum_(e:B_e=T)theta_e
                                      for every legal theme T. (BALANCE)

The P_i differences in SWAP telescope. Since every raw swapped leaf has
nonnegative reduced cost,

    mu_i sum_e theta_e[d_e-v_e]
      =(1/2)sum_e theta_e[r_i(z_e)-r_i(zswap_e)]
      <=(1/2)sum_e theta_e r_i(z_e).                 (HALF-R)

Thus a balanced first-follower flow has signed entrant-vs-follower
shortfall bounded by HALF one source reduced-cost inventory. This is an
all-input joint inequality under the stated balance condition. It does
not bound edgewise positive parts or absolute losses.

For application to the parent's source bank, theta must also respect its
source masses, so a reduced cost is not repeatedly charged. A balanced
flow within each row is not supplied by the shared-saddle query p. Balance
only after aggregating different rows is insufficient: mu_i K_i(T) is a
different potential in each row. That residual row/prefix compatibility,
and a map from covariance to the signed shortfall in HALF-R, are unproved.

For the FULL-slot uniform-cost domain, replace a dot ell by a dot c_full
in (U). The two swapped leaves have identical full load. Hence its own
reduced costs satisfy the cleaner identity

    r_i^+(zswap)-r_i^+(z)
      =2 mu_i(v-d)+mu_i[K_i(B)-K_i(A)].                (FULL-SWAP)

The a dot theme part of P is absent. The same balanced-flow HALF-R holds
using r_i^+; indeed only balance of the canonical K potential is needed
for this variant. These are the FULL domain's own dual and source reduced
costs, not a second copy of the deleted-domain inventory. The full-slot
Taylor self-norm bank is retained in that domain, but no covariance map or
canonical-potential balance is supplied by this observation.

## 5. Social utility conservation is not an additional pool

With fixed preceding load b_i, let U_b(z) be total utility of roles i..m
only, and T_i(z)=sum_(k>i)M(z_<k). Then exactly

    C_i(z)=2d_i(z)-U_b(z)+T_i(z),
    Delta C_i=2 Delta d_i-Delta U_b+Delta T_i.

U_b has the usual resource conservation representation for remaining
providers. It does not remove the canonical-threshold reset Delta T_i,
nor fund positive prefix losses repeatedly along different branches.
Spending U_b again after its future surplus has entered C_i would duplicate
the same child slack. Uniform signed endpoint flows may telescope these
state functions; no positive-part or multi-row bound is inferred.

At m=5 the same copy, swap and HALF-R formulas hold with arbitrary
catalogs and original complete SPEs. Their balance/source-capacity
requirements and covariance application remain unproved, so there is no
unconditional five-player or all-m HALF conclusion. No scan was used.
