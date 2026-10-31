# Exact-only: conditional leaf Hall lift and a degree-three normalized-flat gap

Version: `scratch-conditional-leaf-Hall-consistent-marginals-v3`.

The frozen v1 and v2 remain unchanged. Sections 1-8 retain the weaker
v2 statements. The new section 9 adds marginal consistency, with explicitly
different conditional-matching scope. This v3 extension is proposed by boss11.

This file contains definitions and theorem statements only. It intentionally
omits proofs, witness-flow formulas, and the author checker. The statements have
not yet received an independent Exact-first reconstruction. `UM-TARGET-v1`
remains OPEN.

## 1. Input, value, and full ordinary processing matrix

An input has a finite resource set U, nonempty finite group set G, and a nonempty
finite explicit indexed state set S_g for each group. State coefficients
p_gsu are nonnegative binary rationals, with sum_u p_gsu = 1 for every state.
Zero coefficients, duplicate indexed states, unused resources, and explicitly
listed zero incidences are allowed. Define

\[
v_g(B)=\max_{s\in S_g}\sum_{u\in B}p_{gsu},\qquad
V(Q)=\max_{(B_g)\text{ pairwise disjoint}}\min_g v_g(B_g).
\]

The full ordinary flat processing matrix P(Q) has one private root M_gs per
indexed state, one resource machine R_u per resource, and one original unit
selector J_g per group, eligible at every M_gs of its group. Every original
listed incidence (g,s,u), including every listed zero incidence, contributes
one distinct job whose only finite times are p_gsu at M_gs and 1 at R_u. All
remaining processing times are infinity. All original jobs of unselected
states remain in the matrix and must be scheduled. No jobs or machines are
discarded by choosing states. The exact relation is

\[
\operatorname{OPT}(P(Q))=2-V(Q).
\]

## 2. Exact threshold-unit-demand elimination

Fix a binary rational epsilon in (0,1], and put T=2-epsilon. Define

\[
H_g(\epsilon)=\{u:\max_s p_{gsu}\ge\epsilon\},\qquad
b_g(\epsilon)=\max_s\sum_{u\notin H_g(\epsilon)}p_{gsu}.
\]

Let L consist of all groups with b_g(epsilon)<epsilon, and C=G\L. For every
ell in L, v_ell(B)>=epsilon holds exactly when B intersects H_ell(epsilon).
This includes every group whose states are singleton unit-demand states. This
definition is used in all statements below; the counterexample does not rely
on leaving a threshold-unit-demand group in C.

## 3. The precise conditional leaf Hall relaxation

For c in C and s in S_c introduce lambda_cs>=0, with sum_s lambda_cs=1.
Introduce z_csu with 0<=z_csu<=lambda_cs on positive state incidences; put z=0
outside that support. Require

\[
\sum_u p_{csu}z_{csu}\ge\epsilon\lambda_{cs}.
\tag{R1}
\]

Introduce a global leaf flow y^0_ell,u>=0 supported on u in H_ell(epsilon),
and, separately for every core-state (c,s), a conditional leaf flow
y^{cs}_ell,u>=0 on the same leaf edges. Require the complete rows and columns

\[
\begin{aligned}
&\sum_{u\in H_\ell}y^0_{\ell u}=1
&&\text{for every }\ell\in L,\\
&\sum_{c,s}z_{csu}+\sum_{\ell\in L}y^0_{\ell u}\le1
&&\text{for every }u\in U,\\
&\sum_{u\in H_\ell}y^{cs}_{\ell u}=\lambda_{cs}
&&\text{for every }(c,s),\ell\in L,\\
&z_{csu}+\sum_{\ell\in L}y^{cs}_{\ell u}\le\lambda_{cs}
&&\text{for every }(c,s),u\in U.
\end{aligned}
\tag{R2}
\]

Each conditional column contains only that particular state's z. It does not
contain the usages of the other cores. No common joint distribution of states
or of conditional matchings is required. All lambda=0 perspectives have zero
z and zero conditional leaf flow. Empty C, empty L, empty neighborhoods of
unused resources, and all listed zero coefficients are interpreted literally.

**Necessary polynomial relaxation.** If V(Q)>=epsilon, equivalently if
OPT(P(Q))<=T, then (R1)-(R2) is feasible. The relaxation and the threshold test
are constructible and solvable in deterministic time polynomial in the total
explicit binary input length and the bit length of epsilon. With S_C core
states, I_C positive core-state incidences and E_L leaf edges, its variable
count is S_C+I_C+(1+S_C)E_L, with O(I_C+S_C(|U|+|L|)+|U|+|L|) constraints apart
from normalization and nonnegativity. This is a necessary test only.

## 4. A completely specified family before the path-port lift

Fix an integer t>=2 and let D=t^2. Old resources are

\[
\{g_{a,j}:a,j\in[D]\}\;\sqcup\;
\{A_{a,h}:a\in[D],h\in[t]\}.
\]

There is a core group M and one core group H_{a,j} for every a,j in [D]. M has
D states: state a gives coefficient 1/D to all g_{a,j}, j in [D], and zero
elsewhere. H_{a,j} has exactly two states:

- home: coefficient 1 on g_{a,j};
- parking: coefficient 1/t on every A_{a,h}, h in [t].

All states have total coefficient one. The core groups deliberately include
unit coefficients. The parking state's entire normalized value is one;
it is not a vanishing perturbation of a singleton state. At epsilon=1 none
of these groups is threshold-unit-demand. For each fixed epsilon>0 the same
classification holds whenever t>1/epsilon.

## 5. The specified degree-three path-port lift

For every old resource u, list its positive core neighbors in the following
fixed order: for u=g_{a,j}, list M then H_{a,j}; for u=A_{a,h}, list
H_{a,1},...,H_{a,D}. If the list is c_1,...,c_d, replace u by d distinct ports
u_1,...,u_d. Core c_i values only its own u_i, at exactly its former
coefficient on u, in all of its original indexed states. Add d-1 new leaf
groups ell_{u,i}, i in [d-1]; ell_{u,i} has exactly two singleton states, one
of coefficient one on u_i and one of coefficient one on u_{i+1}.

Denote the resulting menu by Q_t. The resource operation is the existing
BCG adjacent-dummy/path-copy operation, applied here to group-resource
ports. This statement does not claim that the path construction itself is
new or that it gives a general approximation-preserving normalization.
All ports, original indexed states and added indexed states are retained.
Every resource is positive for at most three groups and for at most three
indexed states in this family. The entire set of threshold-unit-demand
groups at epsilon=1 is exactly the set of added path leaves.

## 6. Claimed feasibility and exact actual value

For every integer t>=2, the complete relaxation (R1)-(R2) on Q_t is feasible
at epsilon=1, hence T=1. It has a rational witness in which

\[
\lambda_{M,a}=1/D,\quad
\lambda_{H_{a,j},\mathrm{home}}=1-1/D,\quad
\lambda_{H_{a,j},\mathrm{parking}}=1/D,
\]

and z_cs,u=lambda_cs on every positive core-state incidence. The global
leaf flow has every row exactly one and satisfies all global resource
columns jointly with all core z. For every core-state, its entire
conditional leaf flow can be chosen as lambda_cs times one integral
matching covering **all** path leaves. Thus the counterexample does not
use an omitted leaf, a fractional conditional matching defect, or an
incorrect perspective capacity. In addition, the original positive-support
FSLP(1) on all groups of Q_t is feasible.

Nevertheless the exact actual values of this same explicit input are

\[
\boxed{V(Q_t)=1/t,\qquad
\operatorname{OPT}(P(Q_t))=2-1/t.}
\tag{GAP}
\]

The upper value is attained by explicit pairwise-disjoint original resource
bundles and by a complete legal schedule of every original flat-UM job.
The lower bound ranges over all state choices, all partial bundles and all
complete ordinary schedules. Zero incidences, if explicitly appended, can
all be retained at their private zero endpoints without changing either
value; unused resources and any duplicate indexed states may likewise be
retained without changing this family value. No positive original job is
deleted or made free. For every fixed epsilon>0, taking t>1/epsilon gives
a feasible relaxation under its own exact threshold preprocessing but
V(Q_t)<epsilon and OPT(P(Q_t))>2-epsilon. There is no positive constant
lower bound on actual V implied by feasibility of this relaxation.

## 7. Explicit sizes and limits of the statement

Write

\[
K=1+D^2,\quad S_C=D+2D^2,\quad
P_0=D^2(t+2),\quad L_0=D^2+Dt(D-1).
\]

Q_t has K cores, L_0 leaves, P_0 resources, S_C+2L_0 indexed states, and
I=P_0+2L_0 positive state incidences. Its full ordinary matrix has
S_C+2L_0+P_0 machines and K+L_0+I jobs. It has S_C+2L_0+2I finite
eligibilities; a dense explicit matrix additionally lists every infinity.
The positive data size is O(t^5 polylog t), and dense size is polynomial
in t as well. The construction and rational witness have polynomial bit
length in this explicit size; no poly(log t) output claim is made.

The smallest parameter t=2 gives 17 cores, 40 leaves, 64 resources,
116 indexed states, 144 positive incidences, and a full ordinary instance
of 180 machines and 201 jobs, with exact V=1/2 and OPT=3/2. No global
minimality among counterexamples is claimed.

This is an unconditional integrality-gap statement for the specific
relaxation. It does not prove computational hardness, contradict a
constant approximation under an actual-YES promise, rule out stronger
joint-core conditions, or give a general unrelated-machines algorithm.
It does not claim all core coefficients are small, nor any robust
constant-fraction low-value conclusion. The main target remains OPEN.

## 8. General exact projection under the same existing path operation

Let Q be any finite explicit normalized menu with a nonempty set C of
designated core groups, and fix epsilon in (0,1]. Define its basic relaxation
to have only lambda,z, their normalization and bounds from section 3, (R1),
and the old resource columns

\[
\sum_{c,s}z_{csu}\le1\quad(u\in U).
\tag{B}
\]

No support-completeness assumption z=lambda is made in this section. All
coefficients, states and zero incidences satisfy section 1's definitions.

For each old resource u with d>=1 distinct positive core neighbors, create
one port per neighboring **group**, shared across all its indexed states,
in an arbitrary fixed neighbor order. Transfer that group's coefficient
on u, in every state, to its own port, and add the d-1 adjacent path leaves
of section 5. For d=1 no leaf is added. For d=0 retain u as an unused
resource, with no new leaf. An explicitly listed old zero incidence is
retained with private coefficient zero: use its group's port when present,
otherwise a fixed port of that old resource when d>=1, and the retained
unused resource when d=0. Distinct old resource tags remain distinct.
Write Q^path for this complete new menu. Designate exactly its added path
groups as L, and all the original groups as C.

**Exact projection theorem.** The projection of the full relaxation
(R1)-(R2) for Q^path onto its original lambda variables and its core z
variables, identified via their own group ports, is **exactly** the basic
polytope (B) for Q. This equality holds for every rational epsilon in
(0,1], arbitrary fractional z, zero lambda, all d=0 and d=1 cases, and all
the retained zero and unused data. In particular, every feasible basic
point has a rational extension satisfying one complete global leaf flow
and all complete perspective conditional leaf flows simultaneously; the
extension preserves that very point (lambda,z). Every feasible lifted
point obeys all old resource columns after projection. The construction,
the lifted LP, and the rational extension have polynomial total bit size
in the explicit old data and the supplied basic point.

The same path operation exactly preserves actual normalized menu value:
V(Q^path)=V(Q). Hence OPT(P(Q^path))=OPT(P(Q))=2-V(Q), with all ordinary jobs
in each matrix present. This is an equality of the two fully constructed
instances' optimal values, not a claim that the matrices or their original
machines are identical. The positive-support FSLP(1) also projects exactly
to the old positive-support FSLP(1), preserving the original core lambda.
Only the value and the stated fractional objects are asserted to be
preserved; no new claim of a general SC normalization is made.

The designation of C,L in this theorem is a genuine common precondition.
If section 2 is used to define L automatically as **all** threshold-unit-
demand groups, the projection theorem applies as written whenever every
original group of Q is non-threshold-unit-demand at the same epsilon.
The port operation preserves that property of every original group.
Without this precondition, additional original groups can enter L and
the claimed projection equality for the basic core polytope need not
hold. The family Q_t in sections 4-6 satisfies the precondition at
epsilon=1, and at each fixed epsilon whenever t>1/epsilon.

## 9. Stronger common-marginal version: separate new assertion

The partition and threshold in this section are exactly those of section 8:
C is the designated nonempty set of old groups, and L consists exactly of the
added path leaves. Automatic all-threshold-unit-demand elimination is allowed
only under the same non-leaf precondition already stated there.

Define R_cons to consist of all the constraints (R1)-(R2) plus, for every
designated original core c and every leaf edge (ell,u), the consistency row

    sum_{s in S_c} y^{cs}_{ell,u} = y^0_{ell,u}.                 (MC)

Thus the conditional flows now average to the same global leaf-edge
marginals for each entire core menu. In any genuine epsilon allocation,
the deterministic witness used in section 3 satisfies (MC), so this is
still a necessary relaxation. Its construction and exact rational LP
feasibility are deterministic total-bit polynomial; it adds at most
|C| E_L explicit linear equalities. It does not request a common distribution
over complete leaf matchings or a common distribution of all core states.

**New exact projection assertion.** For every old normalized menu Q and
every basic feasible point (lambda,z) of section 8, there is an R_cons
extension on D_+(Q) preserving that exact original point. Conversely every
R_cons point projects to a basic point. The extension has polynomial rational
bit length and can be constructed in deterministic polynomial time in the
explicit old input and the supplied point. D_+ here names the positive-neighbor
path variant already defined in section 8; it does not redefine the old repo
D operation that also lists groups with only zero incidences.

The extension may require each conditional flow to be a rational convex
mixture of full integral leaf matchings. It is not asserted that each
conditional flow is lambda_cs times a SINGLE integral matching while (MC)
holds. Section 6's single-integral-matching witness remains valid for its
weaker R1-R2 system only; it is not silently transferred to R_cons.

**New sharp-family assertion.** On the same Q_t from sections 4-7, R_cons is
feasible at epsilon=1 for the same core lambda and z=lambda. Actual
V(Q_t)=1/t and OPT(P(Q_t))=2-1/t remain exactly those of the same original
complete matrix. For each fixed epsilon>0, taking t>1/epsilon keeps its
automatic threshold partition equal to these designated C,L, and the same
R_cons point is feasible while V<epsilon. All zero/unused/duplicate and
complete-original-job scope from sections 6-8 continues to apply.

Consequently even consistent GLOBAL LEAF-EDGE MARGINALS plus complete
per-state perspective matching flows do not imply any constant lower
bound on V, or a guarantee uniformly below 2 times this unit relaxation
threshold. This does not rule out joint-core conditioned values/capacities,
a shared full leaf-matching law, higher moments, other relaxations, or
algorithms whose guarantee is measured against actual OPT.
