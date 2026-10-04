# Frozen stationary overloads and polynomial deviator-capped completion

Version 1, 2026-10-04. The statements below are conditional certificate
theorems in MF-MODEL. They strengthen the global capped-seed interface;
they do not supply an all-input on-path selector or a search algorithm for
the certificates. The proof has received independent internal review.
No external review or canonical implementation of the imported scheduler
is claimed.

## 1. Exact model and the changed interface

There are finitely many positive binary-rational-weight atomic clients,
an explicit common site catalog, and explicitly many labeled facilities.
Sites cover arbitrary client subsets. At a fixed labeled layout a covered
client must select a covering facility; an uncovered client is unserved.
Clients randomize independently, and the conditional cost at facility g
is w_i + sum_{j != i} w_j p_jg. Facility revenue is its expected assigned
weight. In a pure profile the cost of a client assigned to g is the
total load L_g, and moving to another facility h costs w_i+L_h.

The old capped-completion primitive requires every facility except
isolated single-client macros to start with load at most a common cap B.
The construction here also permits a stationary facility to retain
several clients at load above B. It checks that each retained client's
external load is at most a guaranteed floor at every ordinary alternative.
Only the final profile must be a client equilibrium; intermediate residual
states need not be equilibria of the full client game.

## 2. A computable floor in the residual pure game

Fix any set U of ordinary facilities and a set R of residual clients,
each having an accessible facility in U. Delete all other facilities and
clients temporarily. For each physical site s occupied by U, let q'_s be
its number of ordinary facilities. A residual client is forced to s if
every accessible ordinary facility is at s. Its options at s include all
q'_s ordinary facilities there.

Sort the forced weights at s as v_1 >= ... >= v_n > 0, padding v_j=0
after n. Put q=q'_s, F=sum_j v_j, H=sum_{j=1}^{q-1}v_j, D=F-H, and

    eta_s = min_{0 <= h <= q-1} max(v_{h+1}, D/(q-h)).       (1)

Thus an empty forced pool has eta_s=0 and a singleton ordinary site has
eta_s=F. Every exact pure NE of this residual game has every ordinary
facility at s loaded at least eta_s.

For completeness, let ell be a minimum load at s in such an NE. There
are h forced clients heavier than ell. None is on a minimum-load facility.
No such client can share with another forced client: the latter would
strictly improve to a minimum-load facility. Hence those h clients occupy
distinct facilities and h <= q-1. On the remaining q-h facilities, select
one least-weight forced client on each nonminimum facility that contains
forced clients. The NE inequality bounds that facility's total, and thus
its forced subtotal, by ell plus the selected weight. The minimum facility
has forced subtotal at most ell. These representatives have total at most
the q-h-1 largest remaining forced weights. Subtracting those weights from
the remaining forced pool leaves precisely D, so D <= (q-h)ell.
Also v_{h+1} <= ell. The term of (1) for this actual h is at most ell;
therefore eta_s <= ell.

This is the forced-pool lemma from adaptive_reset_floor.md applied to the
residual game. Crucially, frozen clients are absent from F and H, and q'_s
counts only ordinary facilities. It asserts a floor at final pure NE,
not at every intermediate assignment and not for arbitrary mixed NE.

## 3. MF-FROZEN-OVERLOAD-POLY: the continuation primitive

Fix any labeled layout, a distinguished facility f, and a rational cap
B >= 0. Supply a feasible pure assignment x of every client served at
this layout. Let M_g be its facility loads. Partition the facilities as
U disjoint union H, with f in U, satisfying

    M_g <= B for every g in U;
    M_h > B for every h in H.                              (2)

Condition (2) determines H uniquely from the seed and cap: it is exactly
the set of facilities loaded above B. Thus recognizing this interface
from a seed requires no search over possible frozen subsets.

Freeze every h in H together with all clients assigned to it by x. Let
R consist of the other served clients. Give each residual client all its
accessible facilities in U as its allowed set. Its initial facility is
still available, so this residual game is feasible. Compute eta_s from
Section 2 for this game. For each frozen client i assigned to h, require

    M_h-w_i <= M_h'       for every accessible h' in H, h' != h;
    M_h-w_i <= eta_s(g)   for every accessible g in U.       (3)

**Theorem.** For every such input and certificate satisfying (2)--(3),
an exact pure client NE of the full fixed-layout game with load at f at
most B can be constructed in time polynomial in the explicit input and
certificate bit lengths.

**Proof.** On the residual game run the published polynomial restricted
identical-link Nashification algorithm, starting from x restricted to R.
Only its maximum-load-preservation property is needed: the resulting
pure NE has every ordinary facility load at most B. Each ordinary site
also has every facility loaded at least eta_s by Section 2. If R is
empty, return the empty ordinary assignment directly.

Reinsert the frozen clients at their unchanged facilities. Residual
clients have no improving ordinary move because their profile is a NE
of the residual game. An ordinary client's current cost is at most B;
joining a frozen facility h would cost w_i+M_h > B. A frozen client's
current cost is M_h. Every other frozen alternative costs at least
w_i+(M_h-w_i) by the first line of (3), and every ordinary alternative
costs at least that much by its floor and the second line of (3).
Thus every covered client is best replying in the full game. Feasibility
and the served/unserved client set are unchanged by removal and
reinsertion. The distinguished facility is ordinary and keeps load at
most B. QED.

The scheduling input consists of positive-weight jobs with arbitrary
allowed subsets of identical labeled links, exactly the residual pure
client game. The imported result is Gairing, Lucking, Mavronicolas and
Monien, [*Computing Nash Equilibria for Scheduling on Restricted Parallel
Links*](https://cgi.csc.liv.ac.uk/~gairing/publications/2004-stoc.pdf),
STOC 2004, Section 4, Corollary 4.3 and Theorem 4.7, as used in
MF-PURE-CAP-POLY. Its polynomial
bound is in the binary weight encoding, not the numerical total weight.
The present proof adds no mixed-multiplicity related-link substitution.

Every old isolated-macro certificate is accepted: a frozen singleton's
external load is zero and all loads and floors are nonnegative. The new
test also permits frozen facilities with multiple clients. It does not
require their total loads to satisfy B after completion.

### Optional stronger floors

Form the full bipartite incidence graph of residual clients and ordinary
facilities, using all allowed choices. A component consists of its
ordinary facilities and residual clients. An unused ordinary facility
is a singleton component. Apply the imported scheduler separately in
each component. If its range-preservation property is invoked as in
adaptive_reset_floor.md, each final facility in component C has load at
least the minimum mu_C of the seed loads in C. Therefore (3) may instead
use

    rho_g = max(eta_s(g), mu_C(g)).                         (4)

The components are for the residual game: frozen clients may connect
several of them in the full game and are checked against each destination
individually. The basic theorem using only eta does not depend on this
additional minimum-preservation property.

## 4. Exact strict separation from global cap feasibility

Use the existing ten-client integer fixture in
examples/multi_facility/greedy_cap_obstruction.json. Sites in order are
(A,E,B,C,D,G); the clients, in file order, are

    (20,A), (8,AB), (24,EBG), (20,B), (10,AC),
    (30,C), (13,BD), (67,D), (20,E), (20,G).                 (5)

The established greedy layout has multiplicities (1,1,2,1,3,0), and its
specific exact site-uniform on-path NE has assigned site totals
(30,44,41,30,67,0). A B facility earns 41/2. Move one B facility to G.
Label the resulting facilities in the order

    (A,E,B,G,C,D,D,D),

so f=3 is the mover and its factor-two cap is B=41. The following pure
seed is deliberately not yet a customer NE:

| Facility label | Site | Assigned clients by weight | Load | Role |
| --- | --- | --- | ---: | --- |
| 0 | A | 20,8,10 | 38 | ordinary |
| 1 | E | 20,24 | 44 | frozen |
| 2 | B | 20 | 20 | ordinary |
| 3 | G | 20 | 20 | ordinary mover |
| 4 | C | 30 | 30 | ordinary |
| 5 | D | 67 | 67 | frozen |
| 6 | D | 13 | 13 | ordinary |
| 7 | D | empty | 0 | ordinary |

The residual forced-pool floors at (A,B,G,C,D) are (20,20,20,30,0);
there are two ordinary D facilities. The frozen weight-24 client has
external load 20 and ordinary alternatives only at B and G, both with
floor 20. The frozen E-private weight-20 client has no other option.
The frozen weight-67 D client has external load zero, so all its ordinary
D alternatives satisfy the test. No frozen cross-facility comparison
adds an obstruction. All ordinary loads are at most 38 < 41.

One strict move by the weight-8 client from A, at cost 38, to B, at cost
28 gives the loads

    (30,44,28,20,30,67,13,0),                              (6)

and this is a full pure NE. The other shared clients have costs 44 at E
versus 52 at B and 44 at G; 30 at A versus 40 at C; and 13 at D versus
41 at B and 13 at the empty D facility. Private clients and the isolated
67 also best reply. The mover earns 20 <= 41.

Yet no pure seed of this deviation game can satisfy the old global
ordinary cap 41 with isolated macros. There is one facility at each of
B,E,G, each forced to serve a private weight-20 client. The weight-24
client must join one of them, creating a load at least 44. Neither atom
exceeds 41, so the resulting overload is not an isolated macro. This is
an impossibility over every pure assignment, including cross-site
redistribution. The fixture strictly separates the new certificate
interface from the old one at the same layout, mover and cap.

The certificate is not a new factor-two existence theorem for this
instance: the existing note already exhibited (6). Its new role is a
general polynomial mechanism that permits this multi-client overload
without requiring the supplied ordinary assignment to be an equilibrium.

## 5. Complete-continuation corollary and exact remaining obligations

**SC-K-FROZEN-OVERLOAD-2.** Supply any on-path labeled layout and an
explicitly rational exact independent-mixed client NE with payoffs a_f.
For each actual one-coordinate deviation f to a different catalog site,
supply a frozen-overload certificate satisfying Section 3 at B=2a_f,
using the actual deviation layout and its actual served-client set.
Then a complete exact factor-two continuation is constructible in time
polynomial in the input and total supplied certificate lengths.

Use the primitive on each of the k(|S|-1) actual deviations, keep the
supplied on-path NE, and use a fixed polynomial pure-NE scheduling rule
at every remaining layout. Distinct actual deviations have distinct
labeled tuples, so these specifications do not conflict. A lookup of
the on-path and actual-deviation layouts plus the default evaluator is
a polynomial-size, polynomial-time-evaluable complete continuation.
It does not write an exponential table. If a_f=0, the cap is exactly
zero, and the same proof forces every selected deviation payoff to zero.

This corollary has no greedy or original-pool premise. It can be paired
with any on-path construction, including adaptive reset where its
certificates exist. It does not claim that every on-path NE has such
certificates. In particular, SC-K-GREEDY-REPAIR-ORDER-NO forces payoff
176 in every mixed NE after one deviation from a source earning 165/2.
No correct completion primitive can certify cap 165 there. An all-input
factor-two constructor still needs a polynomial on-path selection rule
and polynomial generation of successful deviation certificates, or
another invariant that eliminates those obligations.

## 6. Bit complexity and audit scope

The certificate is a facility assignment per served client, a subset H,
and the cap B. Its size is polynomial in explicit n and k. Partitioning,
load sums, incidence checks, the at most k terms of each forced-floor
formula, and all frozen-client comparisons take polynomially many exact
rational operations. Sorting costs O(n log n) comparisons in total up
to the usual per-site bound. An input denominator product has bit length
at most the sum of denominator encoding lengths; divisions in (1) add
only O(log k) bits. Optional incidence components and seed minima also
take polynomial time. All intermediate quantities have polynomial bit
length. Scaling input weights by their denominator product puts the
imported scheduler in its binary-integer input form; this scaling does
not create a numerical-weight iteration.

The independent Fraction audit tests/audits/kfac_frozen_overload.py
reconstructs the fixture, checks residual floors and frozen comparisons,
checks that the initial ordinary seed has a strict improvement, and
checks the resulting full NE. It also enumerates the small residual
assignment space to check that every capped residual pure NE lifts to
a full pure NE in this fixture. This is finite arithmetic evidence for
the example, not an implementation or running-time audit of the
published polynomial scheduling algorithm and not a universal proof.
Its executed finite enumeration finds two residual pure NEs among 12
feasible assignments; both respect the cap and lift to full-game NEs.

Sources: MF-MODEL; the forced-pool proof in adaptive_reset_floor.md;
MF-PURE-CAP-POLY and SC-K-GREEDY-CAP-INFEASIBLE in
polytime_frontier.md. The only external algorithmic premise is the
restricted-identical-link theorem already imported there. The two
corollaries do not resolve the unrestricted selector, global boxed-NE
existence, or the optimal universal constant.
