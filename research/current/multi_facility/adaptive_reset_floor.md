# Adaptive original-pool reset and forced-client floors

Current conditional result, 2026-10-04. This is a self-contained
conditional polynomial construction in the common-catalog MF-MODEL. It does
not assert that its tests accept every input. It has not been externally
reviewed and does not implement the imported scheduling algorithm.

## 1. Model, exact costs, and the greedy data

An input has a finite nonempty site catalog S, k >= 2 explicitly listed labeled
facilities, and clients i with positive binary rational weights w_i and explicit
covered site sets. Every facility can locate at every site. A client with at
least one covering facility must select one such facility; otherwise it is
unserved. Clients randomize independently. If client i selects facility f, its
conditional expected cost is

    w_i + sum_{j != i} w_j p_jf.

Facility f receives expected weight a_f = sum_i w_i p_if. A complete
continuation chooses an exact client NE at every labeled layout. A factor-two
certificate consists of an on-path layout and its continuation, with every
actual facility deviation giving the mover at most 2 a_f.

Run the following greedy occupancy procedure. At each of k insertions an
occupied site s has score W_s^0/(q_s+1), where J_s^0 is its already assigned
client pool and W_s^0 is the pool weight. An unoccupied site has score equal to
its currently uncovered client weight. Choose a maximum score with fixed site
tie breaking. When a site first opens, assign to it every previously uncovered
client it covers; these original pools never change during greedy. Let O be
the final occupied set, q_s its multiplicities, and gamma the last insertion
score. If positive reach exists, gamma > 0.

Three facts will be used:

    q_s gamma <= W_s^0 <= (q_s+1) gamma   for s in O;
    N_r <= gamma                         for r not in O;
    i in J_s^0 and i covered by t in O imply q_t <= q_s.

Here N_r is the weight covered by r but by no site in O. These are properties
of the original greedy pools, not of subsequent equilibrium assignments.

For completeness, chosen greedy maxima are nonincreasing: inserting at an
occupied site lowers only its next-seat score, and opening a site can only
decrease uncovered-weight scores elsewhere. A site's final mean W_s^0/q_s
is its last chosen insertion score and is therefore at least gamma. The final
next-seat score at every occupied site is at most gamma, giving the upper
bound. Every never-opened site's final uncovered score is at most gamma.

To prove the third fact, if i was first served at s and t also covers i, t
opens later. Just before s opens, t's uncovered weight contains all of its
future original pool and i, which is not in that pool. Thus W_s^0 > W_t^0.
If q_t > q_s, at t's last insertion the already occupied s has candidate score

    W_s^0/(q_s^then+1) >= W_s^0/(q_s+1)
                         > W_t^0/(q_s+1) >= W_t^0/q_t,

contradicting the selected t score. This proves maximal original multiplicity.

The zero-reach case is separate: no client can be served at any layout, and an
arbitrary layout with the empty continuation is already exact.

## 2. The two polynomial continuation primitives

### 2.1 Packing with isolated large clients

Given a > 0 and h >= 1, clients of total weight at most (h+1)a can be packed
into at most h bins so that every bin either has total at most 2a or is a
single client of weight greater than 2a. Start with one bin per client and
merge any pair whose combined total is at most 2a. At termination every pair
of distinct bin totals sums to more than 2a. If b >= h+1 bins remained,
summing all pair inequalities would give W > ba >= (h+1)a, a contradiction.
An original bin above 2a was a singleton and never merged. The algorithm has
at most n-1 merges and polynomial exact arithmetic cost. Empty pools use no
bins.

### 2.2 Capped pure Nashification

At a fixed layout, suppose an explicitly feasible pure client assignment has
every ordinary facility load at most B, and every other facility holds exactly
one client whose weight exceeds B. A distinguished ordinary facility can be
kept at most B while constructing an exact pure client NE in input-bit
polynomial time.

The imported algorithmic fact is the restricted identical-parallel-links
Nashification algorithm of Gairing, Lucking, Mavronicolas, and Monien,
*Computing Nash Equilibria for Scheduling on Restricted Parallel Links*, STOC
2004, Section 4, Corollary 4.3 and Theorem 4.7. Its Corollary 4.3 preserves both extrema for each blocking-flow call;
tracking the algorithm's stage ranges and the unchanged complementary links
in its Section 4 gives a pure NE in polynomial time while preserving the
initial global minimum load from below and the initial global maximum load
from above. This range-preservation conclusion is a deduction from the
algorithm, not a separate assertion of Theorem 4.7. The
minimum-load property is needed for the on-path constructor below; the
makespan property alone would be insufficient there.

For capped completion, delete the isolated large clients and their facilities.
Each remaining client retains its initially assigned ordinary facility and
is restricted to all covering ordinary facilities. Apply the imported
algorithm to this restricted game and reinsert the deleted singleton clients.
Ordinary clients now pay at most B, so moving to an isolated client above B
would cost more than B. Each isolated client already pays its own weight, the
smallest possible cost. The result is an exact NE of the full game, including
all omitted choices, and the distinguished facility stays at most B.

Rational weights are scaled by the product of their denominators. That product
has bit length at most the sum of input denominator bit lengths. The imported
algorithm is polynomial in the logarithm of total integer weight; this is not
a loop over a denominator's numerical value.

## 3. Adaptive original-pool reset theorem

**Theorem AR (`SC-K-ADAPTIVE-RESET`).** Fix a positive-reach greedy occupancy and gamma > 0. Suppose
an explicitly encoded rational independent-mixed exact on-path client NE is
supplied, with every facility's expected payoff a_f >= gamma. For each
occupied source site u with q_u >= 2, let

    b_u = min {a_f : f is at u}.

Suppose a supplied partition of the original pool J_u^0 into at most q_u-1
bins has each bin either of total at most 2 b_u or consisting of one client
whose weight is greater than 2 b_u. Then the same layout and supplied on-path
NE admit a complete exact factor-two continuation, constructible in time
polynomial in the explicit input and on-path encoding lengths.

The theorem remains true with any supplied scalar rho_u satisfying
gamma <= rho_u <= b_u, provided the source partition is certified at cap
2 rho_u. An adaptive constructor can therefore use a proven lower bound on
b_u without knowing the final equilibrium payoffs in advance.

### 3.1 Sources with q_u >= 2

Fix a labeled deviator f at u and a different target r. Put B = 2 b_u (or
B = 2 rho_u in the lower-bound version). All old occupied sites survive.
Reset every previously served client to its original greedy site. Every such
client remains served and this reset is feasible, regardless of its on-path
mixed strategy or where its on-path support was located.

At u, put the supplied deletion bins on its q_u-1 stationary facilities. At
each other old occupied site t, all q_t old facilities are stationary, including
when t is the target. Its original total obeys

    W_t^0 <= (q_t+1) gamma <= (q_t+1) b_u.

Apply Section 2.1 with h = q_t and a = b_u. An occupied target starts the mover
empty. If r was never opened, the only newly served clients are precisely the
clients covered by r and by no old occupied site; assign all of these to the
mover. Their total is N_r <= gamma <= b_u. No old client loses coverage because
u still has a stationary facility. This accounts for the entire customer set
served at the actual deviation layout.

Every stationary facility is now ordinary of load at most B or an isolated
client above B; the mover is ordinary. Section 2.2 constructs an exact pure
NE of this full deviation game and keeps the mover at most

    B = 2 b_u <= 2 a_f.

All client restrictions used in Nashification are those of the actual
deviation layout. In particular, newly served clients have their initial
ordinary mover option. Reinserting a large isolated client introduces no
profitable ordinary move and leaves that client's own cost minimal.

### 3.2 Singleton sources and all customer-set boundary cases

For q_u = 1, the source vanishes. The following reset argument needs only
a_f >= gamma, and does not use its on-path assignment.

Let K = {s in O : q_s = 1}, and P be the union of original pools J_s^0 over
s in K. Maximal original multiplicity says that every occupied site covering
a P-client lies in K. At the first opening s of a K-site, every P-client is
still uncovered: a previously opened site outside K could not cover it.
Greedy comparison and the final unused second-seat score therefore give

    w(P intersect C_t) <= W_s^0 <= 2 gamma   for every t in K.

Reset every old client outside J_u^0 to its original site. For a client in
J_u^0, select any surviving occupied site covering it, if one exists; this
site belongs to K. If none exists but the mover has opened a never-opened
site covering it, assign it to the mover. Otherwise it is unserved at the
actual deviation layout. At an occupied target every covered old J_u^0
client has a stationary covering facility, so the mover starts empty.

Every surviving singleton site t now holds a subset of P intersect C_t,
and hence total at most 2 gamma. Every higher-multiplicity site retains its
original pool and is packed on its q_t stationary facilities by Section 2.1
with a = gamma. At a never-opened target r, assign its genuinely new clients
to the mover as well. At the instant u originally opened, r's uncovered
weight included both N_r and J_u^0 intersect C_r, disjointly. Consequently

    N_r + w(J_u^0 intersect C_r) <= W_u^0 <= 2 gamma.

The mover's actual reset load is bounded by this quantity, and every client
served after the deviation has now been assigned. Apply Section 2.2 at
B = 2 gamma. The selected exact pure NE gives the mover at most
2 gamma <= 2 a_f.

### 3.3 Complete continuation and scope

There are k(|S|-1) actual one-coordinate labeled deviations. Their layouts
are distinct, so the selected witnesses are compatible with a single
continuation. At all remaining layouts, use a fixed polynomial pure-NE rule:
choose any covering facility for each served client and run the imported
restricted-link algorithm without deleting any facility. There is no
facility-optimality requirement at these remaining layouts.

The theorem is a sufficient interface. It does not assert that arbitrary
greedy inputs possess the supplied on-path NE or deletion partitions. It
does not solve a bin-packing search problem when those partitions are absent.
In particular, its adaptive cap still imposes a global capped-seed condition
for each deviation; some stable on-path NEs have no such global seed.

## 4. A computable local floor for every pure equilibrium

For occupied s define its forced pool T_s to be the clients whose only
covered occupied site is s. Such a client may cover never-opened sites; it
is only its current occupied option set that matters. Every T_s client can
choose all q_s facilities at s and cannot choose a facility at another
occupied site.

Write q = q_s and sort its forced weights as

    v_1 >= v_2 >= ... >= v_n > 0,

padding v_j = 0 after the end when needed. Let

    F = sum_{j=1}^n v_j,
    H = sum_{j=1}^{q-1} v_j,
    D = F-H,
    eta_s = min_{h=0,...,q-1} max(v_{h+1}, D/(q-h)).          (FLOOR)

Empty forced pools give eta_s = 0. For q = 1, eta_s = F.

**Lemma F (`SC-K-FORCED-FLOOR`).** Every exact pure client NE at this fixed occupancy has every
facility at s of load at least eta_s. This assertion is only for pure NE.

**Proof.** Let l be the minimum facility load at s and choose a facility g
attaining it. Put h = number of forced clients whose weights exceed l. Such
a client cannot be on g. No two of these clients can share a facility,
because either would strictly improve to g. In fact a forced client above l
cannot share its facility with any other forced client: that other forced
client's source exterior load would exceed l. Thus h <= q-1, and those h
clients occupy distinct facilities separate from the remaining forced pool.

There remain q-h facilities carrying all remaining forced clients. At g their
forced subtotal is at most l. At any other facility with forced clients,
choose one of minimum forced weight x. That client's NE comparison with g
gives total load <= l+x, and therefore forced subtotal <= l+x. A facility
with no forced client contributes zero and can be bounded by l. The chosen
representative clients are distinct; there are at most q-h-1. Their total
is at most the sum of the largest q-h-1 remaining forced weights. Subtracting
these largest weights from the remaining forced total gives exactly D,
because the h weights above l are the largest h original weights. Hence

    D <= (q-h) l,   and   v_{h+1} <= l.

The term in (FLOOR) for this actual h is at most l. Its minimum eta_s is
therefore at most l. QED.

The simpler q-th-largest-atom bound follows directly by pigeonhole: a bin
below v_q contains none of q forced atoms of weight at least v_q; another
bin holds two, creating a profitable same-site move. Formula (FLOOR)
dominates both this bound v_q and the residual-average bound D/q.
For example q = 3 and forced weights (100,100,1,1,1,1) give eta_s = 4,
whereas v_q = 1 and D/q = 4/3.

## 5. Adaptive double-LPT conditional algorithm

**Theorem AD (`SC-K-ADAPTIVE-DOUBLE-LPT-2`).** The following deterministic recognition and construction
procedure is polynomial in the explicit binary-rational input length.
Whenever its tests pass it constructs a complete exact factor-two
continuation at the greedy occupancy. Tests may return unknown.

1. For every original greedy pool J_s^0, use descending-weight least-loaded
   placement into q_s bins, with fixed client and facility tie breaking.
   Check that every resulting bin has load at least gamma. If a check fails,
   return unknown.
2. Compute eta_s from the forced pool and put tau_s = max(gamma, eta_s).
   For each q_s >= 2, run descending-weight least-loaded placement again on
   the original pool, now into q_s-1 bins. Check that every deletion-bin load
   is at most 2 tau_s. If a check fails, return unknown.
3. Run the imported polynomial restricted-link Nashification on the first
   complete pure assignment, using every client's actual covering facilities
   as its allowed set. Its global-minimum preservation gives every final
   facility payoff at least gamma. Lemma F independently gives every final
   facility at s payoff at least eta_s. The resulting exact pure on-path NE
   therefore has a_f >= tau_s.
4. Use Theorem AR with rho_s = tau_s and the second LPT partitions. Use the
   singleton reset at q_s = 1 and the polynomial default at all other layouts.

The first packing really is a complete feasible assignment: each served
client is still at a facility at its original greedy site, and only initially
served clients are jobs at this on-path layout. Because W_s^0 <= (q_s+1)gamma
and its other q_s-1 first bins are at least gamma, each first bin is at most
2 gamma. Thus no original client exceeds 2 gamma, so macro bins are not
needed in the second test of this particular algorithm. They remain relevant
to the general supplied-profile Theorem AR.

This procedure contains the old DOUBLE-LPT recognition test: that test uses
the same first test and requires deletion-bin loads at most 2 gamma.
Since tau_s >= gamma, every previously passing input still passes. The
following input passes the new test while the old original-pool cap is
infeasible, independently of LPT tie breaking.

## 6. Exact triangle separating the interfaces

Take k = 8 and sites in order H,M,L. Clients are:

| Client | Weight | Covered sites |
| --- | ---: | --- |
| H1 | 110 | H |
| H2 | 110 | H |
| H3 | 110 | H |
| H4 | 114 | H |
| M1 | 140 | M |
| M2 | 100 | M |
| M3 | 80 | M |
| L1 | 100 | L |
| X | 50 | H,M |
| Y | 60 | M,L |
| Z | 5 | H,L |

The strict greedy insertion trace is

    (H,499), (M,380), (H,499/2), (M,190),
    (H,499/3), (M,380/3), (H,499/4), (L,100).

Thus q = (4,3,1), gamma = 100, and original pools have totals
(499,380,100). At the beginning the site reaches are (499,430,165).
Opening H removes X and Z from subsequent uncovered scores; opening M
then removes Y. The remaining insertion comparisons above are all strict.

The first deterministic LPT bins, with client order as in the table, are:

| Site | Bin client sets | Bin loads |
| --- | --- | --- |
| H | (H4), (H1,X), (H2,Z), (H3) | 114,160,115,110 |
| M | (M1), (M2), (M3,Y) | 140,100,140 |
| L | (L1) | 100 |

The forced pools are the private H-, M-, and L-clients. Formula (FLOOR)
gives eta_H = 110, eta_M = 80, eta_L = 100, so
tau = (110,100,100). The second LPT packings are:

| Source | Deletion bin client sets | Bin loads | Allowed cap |
| --- | --- | --- | ---: |
| H | (H4,Z), (H1,H3), (H2,X) | 119,220,160 | 220 |
| M | (M1,Y), (M2,M3) | 200,180 | 200 |

All adaptive tests pass. The old cap 2 gamma = 200 cannot partition the
original H pool into three bins: its four private atoms all exceed 100, so
no two can share a cap-200 bin. None exceeds 200 and can be declared a macro.
This is an impossibility proof for the old RESET-PACK premise, not merely an
LPT rejection.

One particular exact pure on-path equilibrium is obtained from the first
packing by moving X from its H bin of load 160 to the M bin of load 100
(new cost 150), then moving Z from its H bin of load 115 to the L bin of
load 100 (new cost 105). Both moves are strict. The resulting bins are

    H: (H4),(H1),(H2),(H3),       loads (114,110,110,110);
    M: (M1),(M2,X),(M3,Y),        loads (140,150,140);
    L: (L1,Z),                   load 105.

All clients are best replying:

* Each H-private client pays exactly its own weight, the absolute minimum.
* M1 also pays exactly its own weight. M2 pays 150; its other M facilities
  would give costs 240. M3 pays 140; its other M facilities cost at least 220.
* L1 has one accessible facility.
* X pays 150; another M facility costs 190, and a best H alternative costs
  160.
* Y pays 140; its other M alternatives cost at least 200, and L costs 165.
* Z pays 105, whereas its best H alternative costs 115.

The individual payoffs are all at least their tau_s. The M site total is
430 > (q_M+1)gamma = 400, so this particular on-path NE is outside the
BOX-TO-2 upper box. Theorem AR accepts it. Its exact source minima are
b_H = 110, b_M = 140, b_L = 105; the AD construction can use the smaller
certified thresholds tau_H = 110, tau_M = 100, tau_L = 100.

The light occupied-option graph is a triangle with three unequal edge
weights. It is neither a star nor a path, and its component has unequal
multiplicities. The old RANGE test fails for Y because (380-60)/3 > 100.
This does not prove that the input has no alternative boxed NE, nor does it
separate from every existing bounded-parameter selector. The separation is
precisely from the old reset/deletion premise and from requiring this
supplied NE to satisfy BOX-TO-2.

The exact finite audit in `tests/audits/kfac_adaptive_reset.py` checks the displayed first and deletion
LPT packings, strict moves, client NE, and all 16 labeled deviations by
original-pool reset and cap-preserving strict replies. The largest gain
ratio in that selected finite continuation is 22/21. This verifies only
this fixture. It is not an implementation or running-time test of the
published polynomial Nashification algorithm.

## 7. Bit complexity, short certificates, and remaining limits

Let L be the explicit input bit length. Sorting weights, computing gamma,
computing forced occupied-option sets, the q_s terms in (FLOOR), and both
LPT passes require polynomially many rational arithmetic operations. Across
sites the multiplicity sum is k. All weights, original totals and floors
have polynomial bit length: rational sum denominators can be represented
using a product of input denominators, and division by q_s-h contributes
only O(log k) denominator bits. Cross-multiplied tests are polynomial-bit
comparisons. No loop runs over numerical weight magnitudes.

The supplied mixed-profile Theorem AR is polynomial in its explicitly
rational profile encoding; it does not assume that arbitrary real mixed
strategies have a finite effective encoding. The AD constructor itself
outputs pure on-path probabilities, hence needs no nontrivial probability
encoding. All actual deviations have pure client assignments. There are
only k(|S|-1) such deviations, each holding one facility index or an
unserved marker per client. A fixed polynomial pure-NE default represents
all remaining labeled layouts. Consequently a complete continuation has
a polynomial-size representation with polynomial-time evaluation at a
queried layout; its full |S|^k-entry table is not written.

More generally, the existing factor-two existence theorem guarantees a
short witness format with site-pure/uniform on-path assignment and pure
NE at every actual deviation. Exact client conditional-cost checks and
the factor-two inequalities are polynomial in that witness length. Thus
this certificate search is a total polynomially balanced NP search relation
on valid MF-MODEL inputs (and can be made a TFNP relation on all strings
by handling invalid encodings separately). This is an encoding observation,
not a polynomial search algorithm or a hardness result.

The new construction still requires its first pure-packing minimum test.
For example, a single large private atom at a site with q_s >= 2 may leave
empty initial pure bins, although that atom admits a site-uniform mixed NE.
It also requires deletion LPT to pass: LPT is a sufficient certificate,
not a decision procedure for all feasible partitions. The unrestricted
polynomial factor-two target, arbitrary boxed-NE selection, and the best
universal approximation constant remain unresolved. The forced-floor
lemma must not be applied to arbitrary independent-mixed equilibria based
on this proof.

### Current-source alignment

This result extends the interface in
`research/current/multi_facility/polytime_frontier.md`, sections
SC-K-RESET-PACK-INTERFACE and SC-K-DOUBLE-LPT-GREEDY-2, using their same
model, greedy occupancy, imported scheduler, and singleton reset. It
does not change the counterexamples SC-K-GREEDY-CAP-INFEASIBLE,
SC-K-GREEDY-REPAIR-ORDER-NO, or SC-K-GREEDY-FIXED-POTENTIAL-NO.
For the bad repair and bad potential NEs, the original q_B = 2 pool
already exceeds 2 b_B with no eligible macro, so the adaptive source
partition condition correctly fails. These counterexamples therefore do
not contradict Theorem AR.
