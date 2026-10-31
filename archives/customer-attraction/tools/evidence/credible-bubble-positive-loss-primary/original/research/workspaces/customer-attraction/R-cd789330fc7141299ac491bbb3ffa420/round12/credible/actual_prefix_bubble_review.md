# Independent proof check: actual-prefix query bubble

2026-10-25, credible12, responding to root's BUBBLE contract. The general
proof was reconstructed before reading the supplied literal-unit QA script.
No finite case supplies a general argument. Original all-m HALF is OPEN.

## 1. A genuine next-row child with the same query background

Let h_i be the actual prefix before i and b_i its actual action. Let Y be
the ordered leaf of a genuine complete pure SPE after `(h_i,A,b_i)`. Put

    z=(h_i,A,b_i,Y),       w=(h_i,b_i,A,Y).

The first future action b_i in z need not be a best response. In w the
prefix `(h_i,b_i)` is exactly the next ACTUAL prefix. After both swapped
actions, prefix counts agree. Future subgames are isomorphic: the same
players remain and payoffs depend on prefix loads. Transporting the full
Y witness therefore proves w is a genuine forced-A child-SPE endpoint at
row i+1.

This does not claim w is the original sigma continuation or its entering
utility is capped by u_(i+1). Actual tags are analytically freed. The same
full counts and equal provider weights give exactly

    ell_i(z)=ell_(i+1)(w),       d_i(z)=d_(i+1)(w).        (QUERY)

Thus the query is A on both sides; it is not silently replaced by b_i.

## 2. Uniform net cost and its common-price identity

For the explicit uniform cost

    C_i(y)=d_i(y)-sum_(k>i)[u_k(y)-M(y_<k)],

all deeper payoffs and canonical thresholds agree after the swap. The only
unmatched future term is the first future role. Hence

    C_i(z)-C_(i+1)(w)=M(h_i,A)-u_(i+1)(z).             (BUBBLE)

If a valid analytical domain gives a COMMON mu>=0 and duals

    r_i(y)=eta_i+mu C_i(y)-a dot ell_i(y)>=0,

then QUERY yields exactly

    r_i(z)-r_(i+1)(w)
      =eta_i-eta_(i+1)+mu[M(h_i,A)-u_(i+1)(z)].        (PRICE)

The common price must be produced by an explicit common-cost constraint,
not normalization of unrelated row duals. Eta has no assumed sign. Eta
terms telescope on a consecutive chain but leave boundary terms. Moving
mass between rows must preserve final row normalizations or account for
the boundary mass and prices.

## 3. Original IC gap versus a newly constructed canonical witness

If Y is the ORIGINAL first-follower deviation tail to b_i inside an original
child-SPE witness after h_i A, let that source's prescribed payoff be v.
Then exactly

    Gamma=v-u_(i+1)(z)>=0,
    s=v-M(h_i,A)>=0,
    M(h_i,A)-u_(i+1)(z)=Gamma-s.                       (ORIG)

Gamma is a genuine same-witness IC gap, not a free actual-profit wallet.
The s term already occurs in the uniform source-S bank. Offsetting a
bubble deficit with it must debit that same inventory rather than retain
an independent copy in G. Positive Gamma terms still need legitimate
signed IC/flow accounting or an allowed actual-source budget; their mere
nonnegativity does not pay a positive expense.

For arbitrary genuine Y put delta=M(h_i,A)-u_(i+1)(z). If delta<=0, z is
itself a genuine child-SPE endpoint: its first future payoff meets M and
Y supplies all deeper floors.

If delta>0, choose a canonical maximizing action C with a minimizing child
endpoint giving current payoff exactly M. C cannot be b_i: that would make
its minimum M while the given Y endpoint gives it less than M. Prescribe C
with that endpoint, choose Y as the offpath b_i child, and use minimizing
child SPEs at all other actions. Every deviation gives at most M, so this
is a genuine complete child SPE. Its current payoff is M and its true
deviation to b_i has IC gap exactly delta.

Thus every positive deficit has an actual original-model IC witness. That
witness need not be ORIGINAL sigma, and its entering payoff or cost need
not fit the original cap. It creates no new original source bank for free.
Replacing witnesses requires consistent I,S and reduced-cost accounting.

## 4. Chaining and the all-m obligation

One bubble is a genuine legal actual-prefix reset with preserved query
background. A second bubble additionally requires its next actual action
to be the next recorded action. Arbitrary Y need not have this property.
Raw algebra can continue through a forced actual suffix, but then the
intermediate tails need not be genuine SPEs and their extra deficits stay
charged. Count isomorphism does not remove them.

There is nevertheless a genuine iterative construction. From a genuine
source child SPE z0 after h_i A, force its FIRST future mover to b_i,
following that same witness thereafter, obtaining raw z=(h_i,A,b_i,Y).
BUBBLE transports Y into a genuine next-row child w. Use that transported
witness for the next first-future intervention to b_(i+1), and repeat.
Every intervention is a real IC in its current genuine witness. This does
not assume a single old Y already follows the actual suffix.

Writing S_i for total future canonical surplus, the combined intervention
and bubble edge has exactly

    C_(i+1)(w)-C_i(z0)
      =[d_(i+1)(w)-d_i(z0)]+S_i(z0)-S_(i+1)(w).      (CHAIN)

The first-intervention Gamma and first canonical slack cancel between the
reset and bubble identities. They must not be funded separately. With a
common mu, eta, query-profit, S and reduced-cost differences telescope.
The final child is query A at the last actual prefix, with payoff at most
original u_m. Fixed common-shadow work still gives endpoint duality,
rather than a diagonal covariance amount. Intermediate witnesses differ
from original sigma; their floor/reduced-cost terms cancel instead of
receiving fresh original-source banks.

All identities hold for arbitrary m and m=5. No conservative covariance
decomposition, eta boundary budget, or joint funding of all bubble deficits
has been established. The general proof check passes; HALF payment does
not follow. No finite scan was run for this review.
