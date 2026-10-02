# SC-K-2-E: a uniform factor two for every number of facilities

**Version:** 1, 2026-10-02. **Status:** complete internal proof, accompanied by
reverse reconstruction and a definition-level independent implementation.
Neither external peer review nor literature priority is certified. This file is
a new proof, not an import of the two-facility ring or Wardrop argument.

**Input class:** finite positive-real-weight atomic clients; arbitrary explicit
coverage by a finite nonempty COMMON site catalog; any integer k >= 2 labeled
facilities; repeated locations; compulsory service when covered; independent
mixed client strategies; linear actual-load costs INCLUDING the client's own
weight. See [the explicit model](model.md).

**Exact statement.** For every such instance there exist a pure labeled facility
layout and a complete continuation of exact independent-mixed client Nash
equilibria under which every unilateral facility deviation gains a factor at
most 2. Moreover, the on-path equilibrium can be chosen so that each served
client selects one occupied physical site and independently chooses uniformly
among the facilities at that site. EVERY off-path continuation can be pure.

Thus, writing alpha^*(I,k) for the optimum under the full continuation quantifier,

\[
  \forall k\ge2\ \forall I\qquad \alpha^*(I,k)\le2.                 \tag{T}
\]

This does not assert that 2 is sharp, that every client NE works, that off-path
continuations are symmetric, or that a witness is computable in polynomial time.
The known two-facility lower bound implies only that the sharp constant UNIFORM
OVER ALL k belongs to [phi,2]. It is not imported as a lower bound for each fixed
k>2. The theorem actually remains true for k=1, where exact stability is simpler.

## 1. A finite family of feasible on-path profiles

For a layout s, let O be its occupied physical sites, q_t the number of facilities
at t in O, and assign every served client i to a single site t(i) in O that covers
it. Write J_t={i:t(i)=t} and W_t=sum_{i in J_t}w_i. Unserved clients receive no
assignment. At this stage the assignment need NOT be a client equilibrium.

Let every client in J_t choose each of the q_t facilities at t with probability
1/q_t, independently of every other client. Each facility there has load

\[
                     \ell_t=W_t/q_t.                              \tag{1}
\]

Call this a site-uniform profile. It is an ordinary independent mixed profile,
NOT a split realization of an atomic customer and NOT a joint random choice.
There are finitely many layouts and site assignments. Choose one whose sorted
nondecreasing vector of all k facility loads is lexicographically maximum. Keep
one such layout and assignment fixed. Any tie-breaking among maximizers works.

We use a simple sorted-vector fact repeatedly: if all entries below x are
unchanged or increased, every changed entry originally greater than x remains
greater than x, and at least one entry equal to x is removed or increased with no
new entry at most x replacing it, the sorted vector strictly increases. The same
conclusion holds when some formerly smaller entries increase: the first such
change already improves the sorted vector. In the applications the number of
coordinates remains k and the statements can also be checked by the multiset of
entries at each level.

Let R=max_t sum_{i in C_t}w_i. If R=0, all profiles are empty and exact stability is
immediate. Otherwise, co-locate all k facilities at a maximum-reach site and use
the site-uniform profile. All k loads equal R/k. Consequently every facility in
the chosen lexicographic maximizer has strictly positive load, at least R/k.
All divisions below therefore have a positive denominator.

## 2. The selected on-path profile is an exact client NE

For i assigned to t, its conditional cost at any facility at t is

\[
                w_i+(W_t-w_i)/q_t.                                \tag{2}
\]

At an accessible facility at a DIFFERENT occupied site u it is
w_i+W_u/q_u. Suppose such an alternative strictly improves the cost. Then

\[
                 (W_t-w_i)/q_t>W_u/q_u.                            \tag{3}
\]

Change only the site assignment of i from t to u, retaining the layout. Put
b=W_u/q_u. Previously the q_u coordinates at u equaled b, and all q_t coordinates
at t were greater than b. Afterwards the coordinates at t are (W_t-w_i)/q_t>b,
and those at u are (W_u+w_i)/q_u>b. Other coordinates do not change. The sorted
load vector strictly increases, contradicting maximality.

There is no strictly better pure facility choice. Since a client's expected cost
is linear in its own probabilities when other clients are fixed, no mixed
unilateral improvement exists either. Facilities at its assigned site have the
same conditional cost. Hence the site-uniform profile is an exact independent
mixed client NE. Notice the subtraction w_i/q_t in (2); using W_t/q_t as the
client's actual conditional cost would invalidate this proof.

## 3. Transfer inequalities supplied by the same lexicographic optimum

Fix ANY facility f, let u=s_f be its original site, q=q_u, and

\[
                            a=W_u/q>0.                             \tag{4}
\]

These inequalities concern every physical site in the full common catalog, not
just the eventual target of f's deviation.

### 3.1 When q >= 2: the original site survives departure

For every other occupied site t,

\[
                         W_t\le(q_t+1)a.                          \tag{5}
\]

Indeed, move f to t and keep every client assigned to its old physical site.
At u there are q-1 facilities, each with load qa/(q-1)>a. At t each new load is
W_t/(q_t+1). If (5) failed these loads would all exceed a, as did the old loads
W_t/q_t. No smaller coordinate decreases, and at least one a-coordinate is
replaced by a larger coordinate. This is a strict lexicographic improvement.
All formerly served clients remain covered.

For an unoccupied site r, let

\[
 N_r=w(C_r\setminus\bigcup_{t\in O}C_t)
\]

be the weight of genuinely newly covered clients. Then

\[
                              N_r\le a.                            \tag{6}
\]

Otherwise move f to r, assign all newly covered clients to r, and retain the old
site assignments. The new coordinate exceeds a, the remaining u-coordinates
increase, and no other coordinate decreases.

### 3.2 When q = 1: all clients of the departing site must be accounted for

Put J=J_u, so w(J)=a. For every other occupied site t, the stronger inequality is

\[
               W_t+w(J\cap C_t)\le(q_t+1)a.                       \tag{7}
\]

To prove it, move f to t. Assign ALL clients J cap C_t to t. Keep the other old
assignments. Any client in J not assigned to t that remains covered is assigned
to any remaining site covering it; clients that become uncovered are unserved,
as required by the model. These extra assignments only increase other loads.
There are no newly covered clients, because t was already occupied.

If (7) failed, the new t-load would exceed a. Since w(J cap C_t)<=a, its old load
also exceeded a:

\[
 W_t+w(J\cap C_t)>(q_t+1)a\quad\Longrightarrow\quad W_t>q_t a.
\]

Thus the old sole coordinate a at u disappears, the t-coordinates remain above
a, and no other load decreases. Lexicographic maximality is contradicted.
The implication using w(J cap C_t)<=a is essential; it cannot be omitted.

For every unoccupied r, one similarly obtains

\[
                         N_r+w(J\cap C_r)\le a.                    \tag{8}
\]

For a violating r, move f there and assign to it both the newly covered clients
and all of J cap C_r. Redistribute the other still-covered clients of J to their
remaining sites. Replace the old a-coordinate by a larger one, with no decreases
elsewhere. This proves (8).

Equations (7) and (8), rather than the weaker (5) and (6), are what prevent an
unaccounted-for customer from a disappearing site from breaking the proof.

## 4. A packing lemma with isolated macro clients

**Lemma MF-PACK-2.** Let a>0 and h>=1 be an integer. Given positive client weights
of total W<=(h+1)a, the clients can be partitioned into at most h bins such that
each bin either has total weight at most 2a or consists of a SINGLE client of
weight greater than 2a.

**Proof.** Start with one bin per client. Repeatedly merge any two bins whose
combined weight is at most 2a. A bin larger than 2a was a singleton from the
start and can never be merged. All other bins respect the cap. At termination,
any two distinct bin weights B_j,B_l obey B_j+B_l>2a. If there were b>=h+1 bins,
then b>=2 and summing all pair inequalities would give

\[
 (b-1)W>2a\binom b2=(b-1)ba,
 \quad\text{hence}\quad W>ba\ge(h+1)a,
\]

a contradiction. Empty input gives zero bins. This includes the exact equality
W=(h+1)a and the singleton boundary h=1. QED.

The merging algorithm uses at most n-1 merges; a simple pair scan takes O(n^3)
exact arithmetic operations. It is not an optimal bin-packing oracle.

**Exact limitation of this scalar lemma.** Replacing the cap and macro cutoff 2a
by ca with 1<=c<2 fails under the SAME total-weight hypothesis: take h+1 clients
each of weight a. None exceeds ca, and no two fit in a ca-bin. This is a
limitation of this packing interface, NOT a lower bound on the SPE constant.

## 5. Constructing a bounded initial pure profile after ANY deviation

Fix the same arbitrary f and let its actual target be r != u. Call all facilities
other than f *stationary*. At each surviving originally occupied site t, let h_t
be its number of stationary facilities. We now construct an initial feasible
PURE customer assignment for the deviation layout. No claim that it is already
an equilibrium is made.

### 5.1 Original site multiplicity q >= 2

Every originally occupied site survives. Keep each old client assigned to its
old physical site. At u, h_u=q-1 and its assigned weight is

\[
                         W_u=qa=(h_u+1)a.                          \tag{9}
\]

At each other old site t, h_t=q_t and (5) gives W_t<=(h_t+1)a.
Apply MF-PACK-2 separately at each site and place its bins on stationary
facilities there. Each client is covered by every facility at its assigned site.

If r is new, give the genuinely newly covered clients to f; their total is at
most a by (6). If r was occupied, no clients are newly covered and leave f empty
initially. In either case every covered client is served. The deviator has
initial load at most a. Every other facility either has load at most 2a or hosts
a single macro client of weight greater than 2a.

### 5.2 Original site multiplicity q = 1

The old site disappears. Keep clients outside J at their old assigned sites.
For each client of J, use the following exhaustive rule:

* If some stationary occupied site covers it, assign it to any one such site.
* If not, but r covers it, assign it to f.
* If neither holds, it is now uncovered and receives no service.

At every surviving old site t the added clients are a subset of J cap C_t.
By (7), its total assigned weight is at most (q_t+1)a=(h_t+1)a. Pack these clients
onto its h_t stationary facilities with MF-PACK-2.

If r is new, also give f all genuinely newly covered clients. The full weight
assigned to f is at most N_r+w(J cap C_r)<=a by (8). If r was already occupied,
every surviving client of J has a stationary option; no client is assigned to f
and it initially has load zero. Thus the same invariant as in Section 5.1 holds.

These cases include a target already occupied by several facilities, an empty
or zero-reach target, identical coverage at different sites, clients becoming
uncovered, clients newly covered, and a source site having exactly two facilities.
No aggregation identifies different customer atoms.

## 6. Exact client equilibration preserves the cap

Consider the initial pure profile just constructed. Designate as *isolated
macros* the clients of weight greater than 2a, each alone on a stationary
facility. All other, ordinary facilities have load at most 2a. The deviator is
an ordinary facility; no isolated macro was placed there.

Perform only STRICT improving pure client moves. The following facts are
invariant:

1. An isolated macro client cannot strictly improve: its present actual cost is
   exactly its own weight w_i, and any other accessible facility would cost
   w_i plus a nonnegative load. Empty alternatives merely tie and need not be
   chosen.
2. An ordinary client cannot improve by joining an isolated macro, since the
   destination cost would exceed 2a, whereas its present cost is at most 2a.
3. If an ordinary client moves from h to g as a strict improvement, the new
   destination load is L_g+w_i<L_h<=2a. The source load decreases. Hence all
   ordinary facility loads remain at most 2a.

A strict pure move changes one-half the sum of squared loads by

\[
                       w_i(L_g+w_i-L_h)<0.                         \tag{10}
\]

There are finitely many pure assignments of the covered clients. Consequently
the process terminates at a pure NE. All macros still have no improving move,
and termination removes every improving move of an ordinary client. The final
load of f is at most 2a. This is an exact pure client NE of the full deviation
subgame, not of an artificially restricted game with removed resources.

Equivalently, choose a minimum of the squared-load potential over the nonempty
finite invariant set with these macros fixed and ordinary loads bounded by 2a.
Any improving move in the full game would remain in this set and lower the
potential; macro moves cannot improve. This provides a second way to justify
termination without making a claim about the number of improvement steps.

We have proved, for every f and every full-catalog r != s_f, the existence of an
exact pure customer NE in the deviation layout satisfying

\[
                              L'_f\le2L_f.                         \tag{11}
\]

No coordinate minimum oracle and no classification of all mixed NE is needed
for this existence upper bound.

## 7. One COMPLETE continuation, not incompatible local choices

Use the Section 2 exact mixed NE on the selected layout. For each actual pair
(f,r), choose the pure NE constructed in Sections 5-6. These specifications do
not conflict: if two actual deviations change different coordinates f and g,
their labeled layout tuples differ in coordinate f. Two different targets for
the same facility also produce different tuples. None is the on-path layout.
This reasoning does not quotient layouts by facility permutations.

At every remaining labeled layout choose the deterministic pure NE rule from
[the model page](model.md): start with each covered client on its least-index
accessible facility and perform least-index strict improving pure best replies
until none remains. The finite potential argument proves that this rule is
well-defined on EVERY remaining layout. These continuations need satisfy only
client optimality, not facility stability at every off-path first-stage layout.

The resulting sigma is a single complete rule of exact independent-mixed NE,
pure at all off-path layouts, and (11) checks every actual facility deviation.
This proves (T). The all-zero-reach case was treated in Section 1. QED.

## 8. Encoding, finite construction, and what is NOT an algorithmic theorem

An explicit input lists n rational weights w_i=u_i/v_i>0, their subsets of m
sites, and k labeled facilities. The proof also applies to arbitrary positive
real weights, without invoking an effective real-number representation.

For rational input, an elementary finite procedure is:

1. Enumerate all layouts and all feasible site assignments, retaining the largest
   sorted load vector. Enumerating only the binomial(k+m-1,m-1) nondecreasing
   layouts is equivalent by label symmetry. Each layout has at most m^n site
   assignments. A safe bound for the naive labeled enumeration is
   O(m^(k+n) (n+k log k)) rational operations.
2. For each of k(m-1) actual deviations, apply the explicit bin mergers and strict
   pure best replies. The latter have at most k^n distinct assignments, but NO
   polynomial iteration bound is proved here.
3. Specify the deterministic finite default rule for all other layouts.

This is a finite EXACT witness procedure, not a polynomial-time algorithm.
Global lexicographic optimization and the pure best-response iteration bound
are both unresolved algorithmic obligations for this approach.

The displayed strategies have small bit length. On path, every entry is either
0 or 1/q_t with q_t<=k. On every actual deviation, entries are 0 or 1. One can
store the on-path probabilities, plus one facility index or an unserved marker
per client per actual deviation, and the constant-description default rule.
This has size polynomial in the explicit n,m,k and input bit length. It is a
succinct description of a complete continuation, NOT a claim that its full
m^k-entry table is polynomial size or that its default evaluator is fast.

All intermediate loads are sums of input rationals, possibly divided by integers
at most k. A common denominator product of the v_i has bit length bounded by
the sum of their input bit lengths. Load numerators add only O(log n) and O(log k)
bits beyond the input sum bounds; potential comparisons square these values.
Thus exponential operation counts do not hide exponential coefficient bit
length. Checking the displayed on-path and actual-deviation NE from conditional
costs is polynomial in the explicit certificate length. The default rule's
universal validity is certified by (10), not by pretending all its executions
were enumerated.

## 9. Reverse review, failed routes, and evidence

The separate [reverse review](reverse_review.md) rederives the budget requirement
backwards from a hypothetical profitable deviation, checks the singleton-source
case independently, and attacks the common-catalog and independent-randomness
assumptions. The [menu obstruction](symmetric_menu_obstruction.md) constructs a
family where symmetry-preserving off-path selection has an unbounded required
factor, but the FULL model has an exact SPE. This prevents misreporting a bad
menu as an unbounded lower bound and explains why symmetry must be broken in
Section 6.

The [lexmax layout boundary](lexmax_boundary.md) proves a stronger limitation
on sharpening this method: for each fixed k, the selected facility layout can
require an optimal full-continuation factor tending to 2 even though the full
instance has an exact SPE at another layout. Thus a sub-two universal theorem
must permit a different layout choice, not merely improve the continuation
solver or choose another NE at that same layout.

The implementation `multi_facility_spe/two_exists.py` is separate from the
repository's two-facility package. `tests/multi_facility/definition_check.py` imports no solver
and computes all original conditional costs. `tests/multi_facility/run_exact_audit.py` records
exact finite attacks and small independent exhaustive pure-NE comparisons.
Frozen records are under `evidence/runs/`; they are arithmetic evidence, not the
proof of the arbitrary-k theorem.

## 10. Dependencies and literature scope

The proof depends only on MF-MODEL, finiteness, the transfer inequalities,
MF-PACK-2, and the elementary weighted squared-load potential identity. It does
NOT depend on SC-PHI-E, the earlier five-site hardness delivery, the sharp
atomic-Wardrop error, the heterogeneous two-facility bound, or an external
existence theorem. The two-facility sharp result is used only to state the
remaining interval [phi,2] for the best constant uniform over all k.

Krogmann, Lenzner, Skopalik, Uetz and Vos, *Equilibria in Two-Stage Facility
Location with Atomic Clients*, IJCAI 2024, pp. 2842-2850, arXiv:2403.03114v2,
Sections 1, 3, 4 and 6, use the same atomic conditional-cost and full-continuation
notions. Their unweighted existence proof uses rounded profiles and a different
lexicographic continuation argument. Their weighted conclusions and Section 6
conjecture do not themselves prove this common-catalog arbitrary-weight factor
2 statement. Their general model also allows facility-dependent catalogs;
Section 3 here relies on common access to every occupied site, so the new proof
must NOT be transferred to those heterogeneous catalogs. Their PoA=2 is a
welfare ratio conditional on equilibrium existence, not the present stability
factor.

Krogmann, Lenzner, Molitor and Skopalik, *Two-Stage Facility Location Games with
Strategic Clients and Facilities*, IJCAI 2021 / arXiv:2105.01425v3, establish
results for divisible load-balancing clients. Those clients are not the present
independent atomic customers, so their equilibrium selection cannot be imported.
Krogmann, Lenzner and Skopalik, *Strategic Facility Location with Clients that
Minimize Total Waiting Time*, AAAI 2023 / arXiv:2211.14016, have an atomic-splittable
client game and a factor-3 result; that client game is different too.

Primary texts inspected online in this run:
- https://arxiv.org/html/2403.03114 (especially Sections 1, 3 and 6)
- https://arxiv.org/html/2105.01425
- https://arxiv.org/abs/2211.14016

The 2025 dissertation *Two-Sided Facility Location Games*, DOI
10.25932/publishup-69272, was NOT obtained: the DOI and institutional endpoint
were unavailable. No exhaustive literature-priority or novelty claim is made.
