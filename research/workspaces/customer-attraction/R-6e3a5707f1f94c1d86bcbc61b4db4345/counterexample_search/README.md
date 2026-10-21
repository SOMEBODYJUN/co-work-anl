# Counterexample attack: price portfolios and symmetric continuation orbits

Status: finite research evidence and an explicit exact quotient argument; no
universal welfare or price theorem. No counterexample to Q-CAG-HALF found.
All providers and customers have unit weight; positive integer multiplicities
encode different customers. No Git operations were performed by this agent.

## Price-cone attack

`price_cone_attack.py` attacks the auxiliary claim

\[
B(\min_i u_i)\le W,\qquad
B(v)=\max_{z\ge0}\{\sum_x\min(1,\sum_{T\ni x}z_T)-v\sum_Tz_T\}.
\]

It reuses the existing complete-history strategy-cone engine from
`R-18e993ca519949aba29e030d3d7b15b3/counterexample_search/cone_walk.py`.
The all-SPE set recurrence proposes an actual terminal outcome. A complete
ordered-history strategy is independently reconstructed, and its exact
LCM-scaled comparison rows define a fixed genuine SPE cone. Alternating LPs
choose a capped-coverage portfolio and change the customer multiplicities
inside that fixed cone, with actual welfare normalized to one. Floats only
propose points. Recovered integer multiplicities satisfy every cone row in
Python integer arithmetic, and every best witness is verified by the
canonical full-history certificate verifier. Rationalizing the portfolio and
evaluating its objective exactly gives a **lower bound** on B; no floating
optimal status is promoted to an exact upper bound.

Frozen run `price_m5p7_run.json`: m=5, p=7, seed=2026102137,
40 requested iterations, 38 distinct complete-history cones, four LP rounds
per cone, 152 rounds total. Largest exact feasible-portfolio value divided
by actual W is 4/5, realized by `price_m5p7_best.json`. No floating proposal
exceeded 4/5. This is a bounded attack, not an upper certificate over other
portfolios, strategies, cones, or instances.

## Exact symmetry quotient, with unrestricted history-dependent ties

`symmetric_core_satellite.py` handles the following specific input class.
There are k individually labeled core topics and ell interchangeable
satellite topics. For every core subset B, each satellite j has exactly
w_B customers whose entire interest set is B union {j}. These satellite
blocks are disjoint and have **identical** integer multiplicities w_B across
j. There may additionally be g_B customers interested in a nonempty core
subset B alone; g_empty=0. There are no customers liking two satellites.
Zeros and empty topic coverages are permitted. No theorem about general
asymmetric satellite blocks follows.

A count state is represented with core counts unchanged and satellite
counts sorted. At this state, terminal outcomes are identified only under
permutations of satellites having the same **current** count. Thus the
representative terminal tuple sorts final counts separately inside each
current-count class. It does not sort arbitrary terminal coordinates across
different current-count classes.

Here is the exact orbit-set recurrence proof. Let G_k be the stabilizer of
the current satellite-count vector. It preserves the input and the
continuation game. By induction, retain all G_k orbits of terminal outcomes
realizable by some complete-history pure subgame equilibrium. For a core
action the satellite stabilizer is unchanged, so child representatives and
the current mover payoff map directly to parent representatives. For a
satellite action from count class r, the chosen topic moves from class r to
class r+1. The child stabilizer can interchange it with any topic in the
new class. Consequently, in every child terminal orbit its final count can
be **any distinct final count occurring in that class**. For each such
choice v, remove one v from the child r+1 class and insert it into the
parent r class, leaving all other classes unchanged. Sort within each
parent class and attach the satellite mover payoff at final count v.
These are exactly all parent orbit/payoff pairs for that action; none may
be discarded before evaluating the mover's minimum.

For each action class take the minimum of the current mover's payoff over
its entire mapped child set, then let M be the maximum of these minima.
Retain every mapped outcome/payoff pair whose payoff is at least M. This
is the canonical all-SPE recurrence before quotienting, because action
classes are G_k orbits and all within-class choices are isomorphic. Every
retained pair can be assembled with separately chosen minimizing child
SPEs in all other action subtrees. These subtrees are disjoint in the
ordered history tree, so no equality of tie choices at different histories
is imposed. This proves sufficiency as well as necessity, by induction on
remaining players. The base case is the terminal count state itself.

In particular, choosing only one final count v after a satellite class
merges would be a false simplification. The implementation enumerates all
such assignments. The quotient is a set equivalence, not a restriction to
a symmetric policy, an anonymous tie rule, or one action per count state.

Payoffs use L=lcm(1,...,m): every denominator is a positive integer at most
m, so all recurrence comparisons are exact integer comparisons. Coverage
and OPT are evaluated exactly. The pricing LP, when used, proposes rational
z; its exact objective remains only a feasible lower bound. Symmetrizing
the satellite portfolio coordinates loses no true optimum, because capped
coverage is concave and the input is satellite-invariant.

Independent implementation regression: `--self-test` compared orbit sets
with the canonical unrestricted Fraction solver at 288 root/prefix cases:
m in {2,3,4}, k in {1,2}, ell in {2,3}, eight integer inputs per tuple,
and three count prefixes per input. Seed 24121. All sets agreed. The
mathematical correctness argument above does not rely on this finite test.

Frozen finite runs, seed 202610218:

* `symmetric_m9_k2_l9.json`: 40 inputs, nine players, two cores and nine
  satellites. Best OPT/W=157/97, worst terminal (5,3,0,0,0,0,0,0,0,0,1),
  W=97 and OPT=157; satellite weights (9,1,1,4), core weights (0,12,2,20).
* `symmetric_m8_k3_l8.json`: 12 inputs, eight players, three cores and eight
  satellites. Best OPT/W=401/341. Largest exact feasible pricing lower
  bound divided by W was 2431/3220, across all retained root outcome orbits.

These uniform random integer inputs are exploratory; the procedure does
not exhaust this symmetric incidence class. The optional concentrated
input mode was implemented but not run in this session.

## Exact pricing of two existing replicated mechanisms

The authenticated old 13-player packet has eight types:
(A):2, (B):2, (T):1, (T,D):1, (T,E):1, (A,D,E):3,
(B,D,E):1, (P):25. Its actual W=33, with twelve actual payoffs 5/2 and one
payoff 3. B(5/2)=26 and B(3)=24, so this old mechanism does not break the
price bridge. Exact feasible primal portfolios are z_A=z_B=z_T=z_P=1
for price 5/2, and z_D=z_P=1 for price 3. Exact upper certificates use
the equivalent packing formula

\[
B(v)=|N|-\max\{\sum_B\lambda_B:0\le\lambda_B\le r_B,
\ \sum_{B\ni a}\lambda_B\le v\ (a\in\mathcal S)\}.
\]

For v=5/2 choose lambda, in the above type order,
(2,2,1/2,1,1,1/2,1/2,5/2), totaling 10. For v=3 use
(2,2,1,1,1,1,1,3), totaling 12. These packings are feasible; primal
portfolios give the matching lower values 36-10 and 36-12.

For the new disjoint replication of `aggregate_theta_failure`, a block
has nine degree-two unit types and nine degree-four types with multiplicity
three, with six topic labels permuted transitively by the block symmetry.
Concavity permits averaging every portfolio coordinate to z. Therefore

\[
B_{block}(v)=\max_{z\ge0}
 [9\min(1,2z)+27\min(1,4z)-6vz]
=\max\{0,63/2-3v/2,36-3v\}.
\]

At early payoff v=10, B_block(10)=33/2 while actual W_block=34. For
disjoint blocks, the portfolio optimization separates exactly at fixed
v, so k copies have B(10)=33k/2 and W=34k. Also OPT-W=2k whereas
m v=30k. Thus this replication's strong-theta failure does not transfer
to either the price bridge or the uncovered-mass bridge. This conclusion
uses only the reported root payoffs/coverage; its pricing algebra does not
claim to independently verify the replication's complete SPE graft.

Next useful attack: a composition changing the minimum actual payoff or
the price-portfolio additivity, with its own full BI graft proof. More
uniform random samples of the existing classes have low priority.
