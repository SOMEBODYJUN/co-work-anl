# Exact statements: bounded-interaction weighted state menus

Candidate identity: `UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2`.

Statement-first scratch freeze, 2026-10-18. This v2 sharpens the elementary full-block loss from beta to (Delta-1) beta / Delta; v1 remains frozen separately. This is separate from `UM-DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v2`: menus may have arbitrary size and resource group degree may exceed two, but the new hypothesis bounds how many other groups can interact with a group. The algorithm uses matching and a lower ordered-slot allocation, not a Santa Claus approximation backend. Root independently reconstructed the exact threshold and both branch guarantees from the statement before this freeze. A separate proof is withheld for independent Exact-only review.

The mechanism is a direct structural combination of ordinary matching, ordered slots, actual original-job accounting, and the previously checked private-bonus normalization. No novelty, general unrelated-machines result, hardness source, or sharpness claim is made.

## A. Explicit actual UM input domain

There is a finite nonempty group set G. Every group g has a nonempty, explicitly listed, indexed state menu A_g. The number of states is unrestricted. Every state s has a finite explicitly listed set S_gs of distinct resource identities; the set may be empty. Each state-resource incidence has a nonnegative binary rational private time p_gsu, and

`W_gs=sum_{u in S_gs} p_gsu <= 1`.

The complete original ordinary UM instance P has:

- one distinct private state machine M_gs per indexed state;
- one distinct resource machine R_u per resource;
- one selector J_g per group, taking time exactly 1 at each state machine of its own group and nowhere else;
- one distinct incidence job I_gsu, taking time p_gsu at its own state machine and exactly 1 at its indexed resource machine.

All unlisted times are infinity. There are no other jobs, preloads, side constraints, rejected tasks, or identifications of private machines and resources. Every indexed state and every original job remains part of the instance. Zero private times and duplicate indexed states are allowed.

Write `S_g=union_{s in A_g} S_gs`. Let integer parameters `Delta>=1` and `M>=0` be valid upper bounds on

`max_u |{g:u in S_g}|` and `max_g |{h!=g:S_g cap S_h is nonempty}|`,

respectively. Thus Delta bounds resource incidence across **groups**, over their complete menus; M bounds the group interaction graph's maximum degree. A resource can occur in many states of one group. Bounds can be computed from the explicit input or supplied and checked. Empty maxima are zero; Delta is still taken at least one. The numerical parameters may grow and are binary encoded.

Set

`beta=1/(M+2 Delta-1)`, `R=2-beta`.

## B. Complete actual approximation claim

For every input satisfying A there is a deterministic algorithm, polynomial in the explicit binary input length and parameter bit lengths, that outputs a complete legal assignment of the original jobs with

`C_max <= (2-1/(M+2 Delta-1)) OPT(P)`.

The algorithm does not know OPT and does not receive a YES witness, state distribution, configuration solution, or unknown feasible allocation. Menus may be arbitrarily large. The factor is uniform below two when M and Delta are fixed; if they grow, the guaranteed improvement may tend to zero. No optimum value or sharpness of this factor is asserted.

There is also a polynomial strict-unit promise consequence: distinguish `YES: OPT<=1` from `NO: OPT>2-beta` by testing the actual returned load against `2-beta`. This does not assert an unconditional absolute load `2-beta` for every input.

## C. Normalized algorithm and exact two-branch statements

First suppose every state has W_gs=1.

Call a state diffuse when every private time in it is at most beta. If a group has a diffuse state, select one such state according to a fixed explicit input order; call these groups L. Let H contain all other groups. Every indexed state of a group in H has some private time strictly greater than beta.

Build a bipartite graph between H and resources. Edge `(g,u)` exists precisely when some state of g has p_gsu>beta; store one witnessing indexed state for the edge.

**Failure branch.** If there is no matching covering H, then

`OPT(P)>=1+beta`.

Return the full-private schedule, placing each selector at an arbitrary own state machine and every incidence job at its own private machine. Its actual load is at most 2. Therefore its ratio is at most `2/(1+beta)<=2-beta`; here `0<beta<=1`, including the endpoint Delta=1,M=0.

**Success branch.** If a covering matching exists, choose the stored witnessing state for each matched H group and export exactly its one matched heavy incidence job. Park every other incidence job of that group privately. Reserve the matched heavy resources so that later exports cannot use them.

For every g in L, use its selected diffuse state and remove all reserved heavy resources from its candidate export list. The following bounds hold simultaneously:

1. At most M heavy groups can take a resource carrying positive private weight for this selected diffuse state, because each heavy group exports only one job and any such group is a neighbor of g in the declared group interaction graph.
2. The removed private mass is therefore at most M beta. The remaining private mass W'_g is at least `1-M beta`, and each remaining private time is still at most beta.
3. Sort each group's remaining resources in nonincreasing private time. Divide the sorted list into consecutive **full blocks of Delta distinct resources**, discarding only the final incomplete tail of fewer than Delta resources. Each full block creates one unit-demand slot adjacent to all its Delta original resources. Find one single matching covering **all full slots of all diffuse groups**, using original resources as unit-capacity nodes.
4. Every full slot has Delta neighbors and every resource is incident to at most Delta such slots, so the covering matching exists. The algorithm must match every full slot; it is not claimed that an arbitrary unrelated rounding of fractional values has the same lower utility bound.
5. Let B_g be the resources matched to g's slots. They are disjoint across L groups, avoid all heavy reserved resources, and satisfy the weighted lower bound

   `sum_{u in B_g} p_g,s(g),u >= (W'_g-(Delta-1) beta)/Delta >= beta`.

   More explicitly, for sorted remaining weights `w_1>=...>=w_n` and `m=floor(n/Delta)`, every full-block matching gives at least `sum_{t=1}^m w_{t Delta}`, and

   `Delta sum_{t=1}^m w_{t Delta} >= W'_g-(Delta-1) beta`.

   This is the only stronger bound used to sharpen v1's constant.

Every H group exports private mass strictly greater than beta. Put all selectors at their chosen state machines, export the indicated H jobs and L jobs, and keep every remaining incidence job at its own original state machine. All resource loads are at most 1, all unselected private roots have load 1, and selected private roots have load at most `2-beta`.

Thus successful covering matching gives an unconditional actual schedule of load at most `2-beta`, without a source YES assumption. Since selectors force OPT>=1, its approximation ratio is at most `2-beta` as well. No heavy choice is assumed to preserve a separate diffuse LP exactly: the possible stolen mass is charged explicitly by M beta before the single lower-slot allocation.

## D. Nonnormalized states and exact optimum preservation

For every state with W_gs<1, add one auxiliary resource unique to that indexed state and a bonus job of private time 1-W_gs and external time 1 on that resource. This produces normalized N(P), retaining all original jobs, times, state machines, and selector menus. States with W_gs=1 need no bonus.

All bonus resources have group degree one and create no interaction between different groups. Hence the same M and Delta>=1 remain valid. The normalization has

`OPT(N(P))=OPT(P)`.

Projection deletes only bonus jobs and their auxiliary resources and cannot increase load. Conversely any original schedule has makespan at least 1 and extends without increased load by exporting **every** bonus job, including bonuses of unselected states, to its own dedicated resource. Normalization adds at most one job and resource per state. Apply C to N(P), then project the output to the original jobs; B follows.

## E. Explicit bit complexity and boundaries

The interaction and resource degrees concern explicit unions over all states. They can be checked from the resource-to-group membership lists without searching over state choices. All matching graphs have polynomial size in the listed state-resource incidences. The heavy graph stores one existing witness per edge. Sorting uses exact rational comparisons.

The lower-slot graph contains at most one edge per remaining selected incidence and one slot per full block, so it has polynomial size. Delta is never realized by creating Delta dummy copies: blocks are formed by scanning the actual resource list, and no full block is created unless Delta actual resources are present. If a binary upper bound Delta is larger than every list, no such blocks are created; the proof's hypotheses then determine whether any diffuse group can occur. No numerical-value replication or hidden succinct expansion is used.

Beta has O(log(M+Delta+1)) bits. Arithmetic for normalization, comparisons, state private sums, and final machine loads has polynomial binary length. The matching algorithms and explicit job-by-job reconstruction are deterministic polynomial-time procedures. A production implementation or finite computational verification is not claimed in this scratch statement.

## F. Grouped-cube specialization and remaining scope

For the tagged grouped coordinate-slice model, if each group uses at most q distinct variables and each variable occurs in at most d groups with injective incidence indices, then

`M<=q(d-1)` and `Delta<=min(d,Q)`.

The first bound counts other groups through the at most q shared variable gadgets; the second uses the fact that a resource's usable incidence indices must appear among its Q coordinate values. The actual degrees may be smaller. Arbitrary within-cell private weights of state sum at most 1, arbitrary state counts, and arbitrary explicit cube sizes are allowed.

Consequently fixed q,d,Q give this structured class a uniform below-two factor even for arbitrary private cell weights. For Delta=1,M=0 the algorithm returns makespan 1 and is exact. Increasing interaction degree can make this guarantee approach two. This is not a proof of a uniform factor for fixed Q,K with unbounded group interaction, not a general-UM algorithm, and not a hardness theorem. It identifies a genuine joint heavy/diffuse mechanism and a separate interaction-growth obligation for a new source bridge.
