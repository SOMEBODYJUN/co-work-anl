# Independent Exact-only review: bounded-interaction weighted menus

Reviewed candidate: `UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2`.

Review date: 2026-10-18. Scope: the reviewer received the informal claim, first identified the missing within-state injectivity assumption, and then read only the formal Exact file below. No author or rainbow Proof file was read. The derivations in this review were reconstructed independently from the Exact statement.

Formal Exact reviewed:

`/workspace/scratch/038d9dcc4cac/bounded_group_interaction_weighted_menu_v2_exact.md`

Expected SHA256:

`6267e81738a786ad1145e067637a7792b411328ee35842e8db889ebb22e62c16`

## Exact review verdict

**PASS under the full formal input domain A, including the distinct-resource set condition within each indexed state.** The claim is a deterministic polynomial-time approximation for the stated original ordinary-UM instances. It does not require an optimum value, a YES witness, a distribution on states, or a Santa Claus approximation subroutine. It allows arbitrary explicit menu sizes, zero private times, and empty original state sets.

Let `D=M+2 Delta-1`, `beta=1/D`, and `R=2-beta`. Since `M>=0, Delta>=1`, `D>=1` and `0<beta<=1`. The success and failure branches each give ratio at most `R`, for different independently justified reasons. No universal absolute load `R` is claimed for the failure branch.

The normalization preserves the optimum exactly and preserves the stated bounds on resource degree across groups and on the complete-menu group-interaction graph. The endpoint `Delta=1,M=0` yields actual optimum and returned load exactly `1`. Binary-encoded large upper bounds on `M,Delta` create no replication proportional to their numerical values.

The full-class result has no novelty or sharpness conclusion in this review. It is an elementary combination of heavy-edge matching, a sorted-block lower-allocation inequality, and private bonus normalization. Its bounded group-interaction hypothesis is genuine additional structure, not a general unrelated-machines improvement.

## Indispensable assumption: noninjective counterexample preserved

The initial informal description did not explicitly repeat the within-state injectivity condition. If that condition were removed, the attached actual-OPT-1 endpoint assertion would be false.

Take one group with one state, its selector of size `1`, and **two distinct incidence jobs pointing to the same resource**. Give each incidence job private processing time `1/2` and external processing time `1`. The root private total is `1`; resource group degree is `Delta=1`; the group interaction maximum is `M=0`. Nevertheless the ordinary-UM optimum is exactly `3/2`: one incidence job can be exported and the other retained; makespan below `3/2` forces both jobs to the same resource machine and then gives load `2`.

This example violates formal A, which explicitly requires each `S_gs` to be a finite set of distinct resource identities with one job per incidence. It is not a counterexample to the formal v2 theorem. It does not establish that the noninjective version of the ratio claim is false, since ratio `1` might in principle be obtained by a different exact algorithm on this tiny example. It proves that injectivity is indispensable for the stated endpoint and the given slot proof. It must not be erased from the formal scope.

## Independent derivation

### 1. Normalize without learning OPT

The nonempty group set and the size-1 selectors force `OPT(P)>=1`, even when every original private time is zero or some original state is empty.

For each indexed state of private total `W<1`, add its own new, globally unique resource and one bonus job with private time `1-W` and external time `1`. Do this for **all** deficient indexed states, not just states ultimately selected. Every state now has private total exactly `1`.

Projection of any normalized schedule deletes only bonuses and cannot increase load. Conversely, any original schedule of makespan `C>=1` extends by exporting every bonus to its dedicated resource, each with load `1`. Thus `OPT(N(P))=OPT(P)`. The original jobs and their processing times are unchanged. A bonus resource belongs to one group only and introduces no interaction edge, so the same valid `M,Delta` remain valid. The construction adds at most one job and resource per explicit indexed state.

It remains to verify the normalized statement. Any normalized output can be projected back without increasing load.

### 2. Heavy-matching failure certifies an optimum lower bound

A diffuse state has all private times at most `beta`. Choose one diffuse state for every group that has one, by explicit input order. Let `L` be these groups. Every state of every remaining group `g in H` has some private incidence time strictly greater than `beta`.

Create the explicit graph whose edges `(g,u)` mean that an existing state of `g` has an incidence at `u` with private time greater than `beta`. Store one such state per edge.

Suppose a schedule of makespan `C<1+beta` existed. The selector of each `g in H` chooses one actual state machine. At least one heavy incidence job of that state cannot remain there, since `1+p>1+beta>C`. It must be exported to its sole external resource. Since `C<1+beta<=2`, each resource machine accepts at most one external size-1 job. Picking one such exported heavy incidence for each H group gives a matching covering H.

Consequently, if no covering matching exists, `OPT>=1+beta`. This reasoning uses the actual selected state of an arbitrary putative schedule and does not presume that a state witness is supplied.

The all-private schedule, with every incidence job on its own root and each selector on any own state, has makespan at most `2`. Its ratio in this branch is at most

\[
\frac{2}{1+\beta}\le 2-\beta,
\]

because `(2-beta)(1+beta)-2=beta(1-beta)>=0`.

### 3. Heavy-matching success and the stolen-weight charge

If a covering matching exists, select its stored witness state for each H group and export exactly the indicated one heavy incidence. Distinct matched resources give legal unit-capacity exports, and each such group removes private mass strictly greater than `beta`.

Reserve those matched resources. Fix any `g in L` and its previously selected diffuse state. A reserved resource with positive private weight in this state was taken by a group that is a neighbor of `g` in the **complete-menu** group-interaction graph. Every H group took exactly one resource. Hence at most `M` resources with positive weight are removed from this state; their total weight is at most `M beta`. Zero-weight removals do not affect the inequality. The remaining private mass therefore satisfies

\[
W'_g\ge1-M\beta,
\]

and all its individual weights remain at most `beta`.

Using the complete-menu interaction graph here is essential. A graph defined only by a speculative state choice could omit a heavy witness state subsequently chosen by the matching.

### 4. Independent proof of the lower-slot inequality

Sort a diffuse group's remaining weights as `beta>=w_1>=...>=w_n>=0`. Put `m=floor(n/Delta)`. The full consecutive blocks of Delta distinct original resources have block minima `w_{Delta},w_{2 Delta},...,w_{m Delta}`.

The inequality needed by the claim is

\[
\tag{1}
W'_g\le(\Delta-1)\beta+\Delta\sum_{t=1}^{m}w_{t\Delta}.
\]

Here is a direct accounting proof that includes every possible tail length. Bound the first `min(n,Delta-1)` terms by `(Delta-1)beta`. Partition all remaining positions into the consecutive ranges

\[
[t\Delta,\ \min\{n,t\Delta+\Delta-1\}],\qquad t=1,\ldots,m.
\]

Each range has at most Delta positions and every term in it is at most `w_{t Delta}`. These ranges, together with the first Delta-1 positions when present, cover all positions exactly once. This proves (1), including `m=0`, an empty list, and `Delta=1`. The ranges used for the proof are shifted accounting ranges; the actual matching slots remain the ordinary full blocks `[ (t-1)Delta+1, t Delta ]`.

Every choice of one resource from each full block obtains private mass at least `sum_t w_{t Delta}`. Thus any covering full-slot matching gives at least

\[
\frac{W'_g-(\Delta-1)\beta}{\Delta}
\ge\frac{1-(M+\Delta-1)\beta}{\Delta}
=\beta.
\]

The last equality uses `1=(M+2 Delta-1)beta` exactly.

### 5. A single matching covers all diffuse slots

Construct one slot for every full block of every selected diffuse state. A slot has Delta distinct resource neighbors. A resource occurs in at most Delta **groups** over all menus. Within the single chosen state of any one group, it occurs once and belongs to at most one block. Therefore its degree in the slot graph is at most Delta.

For any family T of slots, count its edges: `Delta |T| <= Delta |N(T)|`. Hall supplies a matching covering all full slots. Reserved heavy resources were removed beforehand, so diffuse exports cannot collide with heavy exports. This proof explains both the necessity of matching every full slot and the dependence on within-state distinct resource identities.

### 6. Reconstruct every original job

Keep every incidence job of every unchosen state on its original state machine. Its total private load is `1` in the normalized instance. Put each selector on its chosen state machine. For H export the one matched heavy incidence; for L export precisely the jobs assigned by the full-slot matching. Keep every other incidence privately.

Every original normalized job is assigned once to an eligible machine. Resource loads are at most `1`. Each selected private root retains private mass at most `1-beta`, plus its size-1 selector, and therefore has load at most `2-beta`. This branch produces an unconditional absolute bound `R`; since `OPT>=1`, its ratio is at most `R`. Projecting the bonus jobs yields the required complete assignment of the original instance.

### 7. Endpoint and finite bit complexity

If `Delta=1,M=0`, then `beta=1`. Every normalized state is diffuse. There are no H groups. Delta-sized full blocks are single resources, and group degree one means they can all be matched. The algorithm exports every incidence of its chosen states. Selected roots carry only selectors, unselected roots have private total `1`, and all resources have load at most `1`. Returned makespan and optimum are exactly `1`, including originally empty states after projection.

All graph vertices and edges are obtained from explicit states and incidences. A maximum matching can deterministically return one stored state per chosen edge. Sorting and comparisons of private binary rationals use exact arithmetic. Only `floor(n/Delta)` full slots are created for a list of actual length n; a large binary value of Delta does not create dummy vertices or repetitions. The rational beta has a denominator of bit length `O(log(M+Delta+1))`. Exact sums of the explicit binary rationals, bonuses, and reconstructed machine loads have polynomial binary length. No step uses OPT, a hidden witness, numerical-value expansion, or an implicit enumeration of a succinct state family.

## Grouped-cube specialization check

For the fixed variable-incidence grouped coordinate-slice model, a group involving at most q distinct variables can meet at most `q(d-1)` other groups. For a tagged resource `(x,a)`, any group that can use it must have its distinct incidence index equal to one of the Q coordinate values of a. Thus at most `min(d,Q)` groups can use the resource over their complete state menus. These are valid upper bounds even when many states of one group reuse that resource.

This check depends on the union of variables used by the group having size at most q, as in the fixed `X_g` coordinate-slice model. It is not a claim about arbitrary menus that vary over an unbounded union of variables while using at most q in each individual state.

## Residual scope

No fatal defect was found in the formal v2 statement. The independent reconstruction certifies the declared factor for its exact domain. The noninjective counterexample remains a warning against silently dropping a load-bearing input restriction. Uniform below-two improvement here requires fixed valid M and Delta; the displayed formula does not yield such an improvement when these parameters are unbounded. No general-UM or hardness conclusion is inferred.
