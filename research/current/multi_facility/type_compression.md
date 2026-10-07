# Exact type compression for box equilibria and global selection

Current proof, 2026-10-03. Internally independently reversed; no external review or literature-priority finding. The Lenstra theorem below is imported, not a new integer-programming result.

## 1. Exact box-NE integer program at a fixed occupancy

Fix an MF-MODEL occupancy on occupied sites O, with m=|O|, positive integers
q_s, and a positive rational gamma. The required box is

    q_s gamma <= W_s <= (q_s+1) gamma.

A site-pure/within-site-uniform customer assignment is an exact independent-
mixed customer NE precisely when, for every customer i assigned to s and every
different accessible occupied site t,

    (W_s-w_i)/q_s <= W_t/q_t.                         (NE)

This retains the subtraction of the customer's own weight. The common w_i in
the actual conditional costs cancels.

Customers with only one occupied option are fixed at that site; unserved
customers have no variables. More generally one may prescribe any chosen set
of fixed customers, but the stability of those fixed customers then needs its
own check. Let F_s be their total weight at s. Group the remaining customers by
their exact rational weight w_a and occupied option set A_a subset O. Let n_a
be the number of labeled customers of type a. Define

    U = sum_s F_s + sum_a n_a w_a.

For each a and s in A_a use integer variables x_as and y_as, with constraints

    0 <= y_as <= 1,
    0 <= x_as <= n_a y_as,
    x_as >= y_as,
    sum_(s in A_a) x_as = n_a.

Thus y_as=1 iff at least one customer of that type is assigned to s. Define
the linear expression W_s=F_s+sum_(a:s in A_a) w_a x_as. Add all box
constraints. For each a, s in A_a, t in A_a minus {s}, add

    q_t(W_s-w_a) <= q_s W_t + q_t U(1-y_as).          (IP-NE)

If y_as=1, this is exactly (NE). If y_as=0, x_as=0 and the constraint is
automatically satisfied: all W are nonnegative and at most U, so its left side
minus q_s W_t is at most q_t U. This is the only role of the large constant.

Equivalence is bidirectional. A legal boxed NE induces counts and supports
satisfying the system. Conversely, integral counts expand to labeled clients
of each type in any order, every active assignment satisfies all NE
inequalities, and each client mixes independently uniformly at its assigned
site. Fixed singleton-option clients have no site deviation. Hence when the
only fixed clients have singleton occupied options, this IP is a COMPLETE
decision and construction method for site-pure/within-site-uniform box NEs at
the chosen occupancy. It does not decide arbitrary customer mixing across
different physical sites.

If d is the number of distinct weights among multi-option customers, there
are at most d(2^m-m-1) variable types and

    R = sum_a |A_a| <= d(m 2^(m-1)-m)

type/site incidences. There are exactly 2R integer variables; the loads are
expressions, not additional variables. The counts n_a may be arbitrarily large
but only occur as binary-encoded bounds and coefficients. The number of
constraints is O(mR+T+m).

All coefficients are rational with polynomial bit length. In explicit input,
weights are binary rationals, k is explicit, q_s<=k, and gamma from greedy is a
sum of input weights divided by an integer at most k. Sums and products used
above have polynomial bit length. Multiplying each row by the product of its
denominators gives an equivalent integer-coefficient ILP, with polynomial
encoding length. No iteration over numerical weight values occurs.

Lenstra's fixed-variable integer-programming theorem gives time
f(m,d) times a polynomial in input encoding length. Feasibility can return a
witness; alternatively polynomially many binary feasibility queries fix each
bounded integer count. This is an FPT algorithm in (m,d), not a general
polynomial algorithm when these parameters vary. On a greedy occupancy, a
feasible output combines with SC-K-GREEDY-BOX-TO-2 to give a polynomially
evaluated complete factor-two continuation.

## SC-K-FROZEN-LIGHT-FPT: refined light-component version with prescribed heavy clients

Run greedy with positive reach, and let gamma>0 be its final insertion score.
Its initial loads obey every box. Freeze all clients of weight >=gamma at
their original greedy sites, and all clients having one occupied option. Form
the graph on occupied sites by connecting the occupied options of every
remaining multi-option client of weight <gamma. Each remaining client has
all its occupied options within one connected component. The IP above splits
into independent IPs, one per nontrivial light component.

For a component C use F_s for its fixed loads and

    U_C = sum_(s in C) F_s + sum_(a in C) n_a w_a.

If c bounds the number of sites per component and d bounds the number of
distinct variable light weights per component, each component has at most
2d(c2^(c-1)-c) integer variables. Thus all components can be solved in
f(c,d) times polynomial total input length. Isolated sites contain only fixed
clients and retain their initial boxed total.

Every frozen heavy client remains at exact NE at EVERY feasible boxed output:
if assigned at s, w_i>=gamma and the upper box give

    (W_s-w_i)/q_s <= ((q_s+1)gamma-gamma)/q_s = gamma,

whereas every occupied alternative t has W_t/q_t>=gamma. Light components
cannot interact through movable clients, and these heavy-client inequalities
also hold across components. Therefore feasible component outputs together
give an exact NE of the full game, and the box-to-two theorem completes all
deviations.

Crucial limitation: an INFEASIBLE component certifies only nonexistence with
these heavy clients PRESCRIBED at their original greedy sites. It does not
exclude a box NE that moves a heavy client. The unrestricted program in
Section 1 is needed for a complete fixed-occupancy decision.

If maximum reach is zero, all customers are unserved at every layout and any
layout has an exact zero-load certificate. If reach is positive then greedy
scores, including gamma, are positive. Empty type sets are handled directly;
there is no division by gamma in the formulation.

## SC-K-CATALOG-WEIGHT-XP-2: unconditional global factor-two construction at bounded catalog and weights

Let p=|S| be the entire physical catalog size and let d be the number of
distinct input customer weights. For fixed p,d, there is an INPUT-BIT-
POLYNOMIAL algorithm for a complete factor-two witness, for arbitrary explicit
customer number and arbitrary explicit k. This does not rely on the existence
of a box NE at the greedy occupancy.

Group customers by (exact weight, full physical-site coverage set A subset S).
There are at most d(2^p-1) nonempty-coverage types; the uncovered type is
permanently unserved. Equal-type labels have no effect on feasibility, expected
loads, or NE inequalities.

Enumerate the facility occupancy vectors q in Z_>=0^p with sum q_s=k. Their
number is binomial(k+p-1,p-1), at most (k+1)^(p-1) for p>=1. For each q, a
type's occupied options are A intersect O. If empty, its clients are unserved;
otherwise distribute its n_a labeled customers by integer counts x_as>=0,
sum x_as=n_a. One vector of such counts represents exactly the site-uniform
family of SC-K-2-E at that occupancy, up to irrelevant equal-type label swaps.

A completely elementary implementation enumerates each type's weak
compositions. There are at most (N+1)^(r_a-1) when r_a=|A intersect O|>=1.
The total exponent is bounded by a function of p,d, independent of N,k and
weight magnitudes. For every count vector calculate W_s, form q_s copies of
W_s/q_s, sort all k coordinates, and retain the lexicographic maximum across
all q and counts. This is exactly the GLOBAL lexmax profile in SC-K-2-E, so
its existing proof supplies exact on-path customer NE and all four budgets.
MF-PURE-CAP-POLY supplies all deviation continuations and a polynomial-time
default evaluator on every other labeled layout. Hence a complete factor-two
certificate is obtained, unconditionally in this bounded-(p,d) class.

The on-path output has k explicit facility coordinates and one occupied site
per served labeled client; probabilities are 1/q_s on the chosen site's
facilities, with O(log k) bits. Store the k(p-1) actual unilateral deviations
as pure labeled-client assignments, requiring O(kpN log k) bits apart from
the input. Distinct actual deviations from one labeled on-path tuple lead to
distinct labeled layouts, so these prescribed continuations never conflict.
The other exponentially many layouts are represented by the existing
polynomial-time default evaluator, not by an explicit table. Weight arithmetic
and every load are sums/quotients of polynomial-bit rational input numbers.

An alternative decreases the customer-count exponent using fixed-variable
integer programming. For each q and each of the at most p! permutations pi of
its occupied sites, add the linear ordering inequalities

    q_(pi[j+1]) W_(pi[j]) <= q_(pi[j]) W_(pi[j+1]).

In that fixed order, maximize W_(pi[1]), then W_(pi[2]), etc., fixing each
attained earlier maximum. Since denominators q are fixed and sorted groups
have fixed positive multiplicities, this sequence gives exactly the sorted
k-coordinate lexmax among the count vectors satisfying that order. Ties do
not matter; every feasible assignment belongs to at least one order.
Each stage is a fixed-variable linear integer optimization, implementable
from Lenstra feasibility by binary search after scaling rational weights.
Compare these maxima across all orders and occupancies.

Time is bounded by

    (k+1)^(p-1) p! p f(p,d) poly(input bits).

For fixed p,d it is polynomial because k is explicitly listed in the output
and input conventions. This is NOT claimed FPT in (p,d), since k's exponent
depends on p. It does not contradict SC-K-LEXMAX-STRONG-HARD, whose
3-PARTITION reduction has unbounded physical catalog size and unbounded
distinct-weight count. The imported fixed-dimension IP theorem is standard;
the contribution is the exact MF-MODEL type compression and its scope.

For p=1, the unique occupancy q_1=k requires no enumeration and every covered
client uniformly uses its co-located facilities; there are no actual facility
deviations. If all catalog reaches are zero, take any layout, the empty
on-path profile and the all-empty default continuation. These cases include
zero customers and globally unreachable clients.

## Exact theorem import and source

H. W. Lenstra, Jr., "Integer Programming with a Fixed Number of Variables,"
Mathematics of Operations Research 8(4), 538--548 (1983), DOI
10.1287/moor.8.4.538. Author-hosted original:
https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1983i/art.pdf .

The theorem applies to arbitrary integral linear inequalities with a fixed
number of integer variables. The type supports above are integer variables,
not an appeal to a floating-point mixed-integer solver. No imported scheduling
theorem is extended to unequal multiplicities.

## Relation to existing repository assets

The old FPT-D in
research/current/local_and_exact/exact_algorithms_and_extensions.md, Section 3,
already imports fixed-dimensional ILP for TWO-FACILITY LOCAL mixed-equilibrium
load-difference spectra, after fixing the difference sign, a weight threshold,
and the number of designated mixers. Its variables count pure/mixed customers
per weight. The present type supports instead count chosen physical sites and
enforce the arbitrary-k own-weight-discount NE inequalities; its target is a
box or the original global site-uniform selection. These are extensions of an
existing parameterized method, not new integer-programming theory. No
equivalent arbitrary-k fixed-catalog/type compression claim was found in the
current multi_facility, local_and_exact, question or canonical-code layers.

## Complexity boundaries

For arbitrary fixed occupancies without the GREEDY-OUTPUT promise, boxed
site-uniform NE feasibility is in NP by the labeled assignment certificate
and exact rational inequality checks; universal feasibility is not asserted.
Under the canonical greedy-output promise, universal existence and a finite
constructor are now proved by
[SC-K-GREEDY-BOX-EXISTS](greedy_box_global_progress.md). This update does not
make an arbitrary fixed occupancy satisfy the greedy promise. The already known
SC-K-LOCAL-PLS is a valid PLS upper bound for the different total factor-two
certificate search. No PLS-hardness, NP-hardness under the GREEDY-OUTPUT
promise, or hardness of the complete factor-two goal follows from this note.

For arbitrary fixed layouts, box feasibility alone can encode 3-PARTITION:
m sites with q_s=1, private weight gamma at each site, and universally covered
items totaling m gamma; upper boxes force a partition into loads 2 gamma,
which is itself NE. However this does NOT preserve the greedy-output promise
and therefore is not proposed as a new barrier for the greedy route.
