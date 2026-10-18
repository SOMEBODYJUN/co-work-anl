# Proof: bounded-interaction weighted state menus v2

Identity: `UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2`.

Statement dependency: `bounded_group_interaction_weighted_menu_v2_exact.md`, SHA-256 `6267e81738a786ad1145e067637a7792b411328ee35842e8db889ebb22e62c16`.

Proof-first disclosure is intentionally separated from the frozen Exact. Root reported that bicriteria independently reconstructed both branches and the ordered-slot inequality from the Exact alone before authorizing this Proof. This file does not replace that independent record, and no review hash is asserted here.

This is a self-contained structural corollary of bipartite matching, ordered blocks, and original-job accounting. There is no external Santa Claus approximation theorem, hardness source, claim of sharpness, or finite-enumeration substitute for the proof.

## 1. Domain and normalization

Use exactly the explicit input domain of Exact A: each state lists a **set of distinct resource identities**, has one incidence job per listed resource, and has private mass at most one. A resource may occur in many states of one group. Across complete menu unions, resource group degree is at most Delta and group interaction degree is at most M. The parameters satisfy Delta>=1 and M>=0. Let

`D=M+2 Delta-1`, `beta=1/D`, `R=2-beta`.

Since D>=1, we have `0<beta<=1` and `1<=R<2`. Every legal schedule has load at least one because the group set is nonempty and every selector takes time one at every eligible machine. The all-private schedule has load at most two.

For every state whose private mass is W<1, add one private-to-that-state bonus resource and a bonus incidence job with private time 1-W and resource time one. All original incidences and selector options remain present. The normalized instance N(P) has private mass exactly one at every state, resource group degree at most Delta, and group interaction degree at most M: each new resource belongs to exactly one group and creates no cross-group intersection.

Deleting all bonus jobs from any normalized schedule gives an original schedule with no larger load. Conversely, take any original schedule of load C. Since C>=1, exporting **every bonus job of every state**, including all unselected states, to its unique bonus resource extends the schedule with load at most C. Private loads do not increase and new resource loads are exactly one. Therefore

`OPT(N(P))=OPT(P)`.

There is at most one bonus job and resource per state. It suffices to prove the algorithm and ratio for normalized input and then delete the bonuses from the returned schedule.

## 2. Heavy matching and its failure certificate

In normalized input, let L contain every group with at least one state all of whose private times are at most beta. Choose one such state for each L group in the fixed input order. All other groups form H. For every state of an H group, at least one private time is strictly greater than beta.

Build the heavy bipartite graph with H on the left and resource identities on the right. Include edge (g,u) if some indexed state s of g has p_gsu>beta, and store one such s. This graph uses resources from all states; it does not split one group into separate state agents.

Suppose a legal schedule had makespan `C<1+beta`. Its selector picks one state s for each g in H. At least one incidence in that state has private time greater than beta. That incidence cannot stay at its private machine, since together with the selector its load would exceed 1+beta. It must be exported to its own resource.

Because `C<1+beta<=2`, no resource can receive two resource-time-one jobs. Picking one forced heavy exported job per H group therefore yields distinct resources and a matching covering H in the heavy graph. The contrapositive is

`heavy matching fails => OPT>=1+beta`.

On failure, output the all-private schedule of load at most two. Its approximation ratio is at most

`2/(1+beta)<=2-beta`,

because `(2-beta)(1+beta)-2=beta(1-beta)>=0`. This also proves the endpoint beta=1; no strict inequality at that endpoint is needed.

## 3. Success: reserve one heavy job per heavy group

Now suppose the heavy graph has a matching covering H. For each matched edge (g,u), select its stored witness state and export exactly that incidence job. Keep all other incidence jobs of the group, including all incidences of every unselected state, on their original private machines. Each H group exports private mass greater than beta. The matched resources are distinct; reserve their set T for these heavy exports.

For an L group g, take its selected diffuse state and remove the resources in T from its candidate export list. Each removed resource was reserved by one H group h. If that resource is in g's selected state then it is in both complete menu unions S_g and S_h, so h is a neighbor of g in the group interaction graph. A single h reserves only one resource. Consequently at most M selected diffuse incidences are removed. Each has private weight at most beta. The remaining mass satisfies

`W'_g>=1-M beta`,

and every remaining incidence still has private weight at most beta. This is a direct charge for the actual chosen heavy matching. No independent diffuse allocation or fractional solution is assumed to remain feasible after the heavy choice.

## 4. One matching covering all full diffuse slots

For each g in L, list its remaining resources in nonincreasing private weight

`w_1>=w_2>=...>=w_n>=0`.

Let `m=floor(n/Delta)`. Form m consecutive full blocks of Delta resources: block t has positions `(t-1)Delta+1,...,t Delta`. The final incomplete tail, if present, creates no slot. Each full block creates one left slot adjacent to its Delta **distinct original resources**. Use one common right node per unreserved resource for all groups.

Consider any subfamily A of full slots and its neighbor set N(A). Every slot in A has exactly Delta neighbors. A resource occurs at most once in one group's selected list, hence at most once among that group's slots. It belongs to selected lists of at most Delta distinct groups. Thus its degree into all slots, and into A, is at most Delta. Counting edges gives

`Delta |A| <= Delta |N(A)|`,

so `|N(A)|>=|A|`. Hall's theorem gives a matching covering **every full slot simultaneously**. A standard deterministic bipartite matching algorithm finds one. This is the required allocation procedure, not an arbitrary rounding of a fractional solution.

For g, any resource assigned to its t-th block has private weight at least `w_{t Delta}`. Therefore every covering matching exports private mass at least

`sum_{t=1}^m w_{t Delta}`.

To bound this quantity, write `n=m Delta+r` with `0<=r<Delta`. For `m>=1`, every entry at an index from Delta through n is bounded above by the preceding sampled entry `w_{t Delta}`; assign indices `t Delta,...,(t+1)Delta-1` to sample t, truncating the last range at n. Each sample receives at most Delta entries. Consequently

`sum_{j=Delta}^n w_j <= Delta sum_{t=1}^m w_{t Delta}`.

The first Delta-1 entries have sum at most `(Delta-1) beta`. Hence

`Delta sum_{t=1}^m w_{t Delta} >= W'_g-(Delta-1) beta`.

When m=0, the sum of all n entries is at most `(Delta-1) beta`, so the same inequality holds with an empty sampled sum. In the actual success case the lower bound below is positive, which in particular rules out m=0 for an L group.

Let B_g be the resources matched to g's slots. The total exported mass satisfies

`sum_{u in B_g} p_g,s(g),u >= (W'_g-(Delta-1) beta)/Delta`

`>= (1-(M+Delta-1) beta)/Delta = beta`,

where the equality uses `beta=1/(M+2 Delta-1)`.

The sets B_g are mutually disjoint and avoid T. The proof explicitly uses that one state has distinct resource identities. If a state could contain several incidence jobs on the same resource, resource group degree would not bound slot degree and the Hall count would not apply to this construction.

## 5. Complete original-job schedule and relative guarantee

Place each selector on its selected state machine. Export exactly the one matched incidence of every H group and the matched diffuse incidences of every L group. Put every remaining incidence job, from selected and unselected states alike, on its original private machine.

Every resource receives at most one job and has load at most one. Every unselected state machine has load one. A selected state machine has its selector plus the normalized private mass one less the exported private mass. That exported mass is greater than beta for H and at least beta for L, so every selected private load is at most `2-beta`. Thus success produces an unconditional schedule of makespan at most R. Since OPT>=1, this is also an R-approximation.

Combining this success bound with the failure ratio in Section 2 proves the all-input R-approximation for normalized input without knowing OPT. Exact normalization and projection in Section 1 prove the stated R-approximation for the original W<=1 instance. If Delta=1 and M=0, then beta=1. Every normalized state is diffuse, H is empty, each block is a single resource, and different groups use disjoint resources. The construction exports every incidence of every selected state and has load exactly one.

For the strict-unit promise consequence, a YES instance has OPT<=1 and therefore equals one. The algorithm returns load at most R. A NO instance with OPT>R cannot admit any returned legal schedule of load at most R. Testing the actual returned makespan at R separates the two promise cases.

## 6. Explicit binary running time and cube specialization

All state-resource incidences are explicitly listed. Complete menu unions S_g, resource-to-group memberships, and group interactions can therefore be formed and checked in polynomial time. Heavy graph edges and stored witnesses come from existing incidences. Diffuse states are found by exact rational comparisons with beta. The two bipartite matching graphs are polynomial in the listed incidences.

In the lower-slot graph, each remaining selected incidence occurs in at most one block and contributes at most one edge. The number of slots is at most the number of selected incidences. Delta is used only as a binary integer for comparisons, floor division, and indexing full blocks in an actual finite list. There is no loop up to an unbounded numeric Delta and no Delta-copy construction. When Delta exceeds a list's length, that list has no full block. Sorting and all binary rational sums, bonus deficits, comparisons, and output loads have polynomial bit complexity. Beta's denominator has polynomial bit length in the parameter encodings. Exporting and parking each explicit original job completes the polynomial reconstruction.

For tagged grouped cubes, a group using at most q distinct variables has at most `q(d-1)` neighboring groups: every shared resource is inside one shared tagged-variable gadget, and each such variable occurs in at most d groups. A cube resource a can belong to a group's slice only if that group's injective incidence index equals one of a's Q coordinate entries. There are at most `min(d,Q)` such indices across distinct groups. Hence `M=q(d-1)` and `Delta=max(1,min(d,Q))` are valid upper bounds, with the max redundant when d,Q>=1. These are bounds over all state menus, not over one favorable state selection.

The result permits arbitrary explicit menus and arbitrary within-cell private weights of state sum at most one. Fixed interaction and resource degree give a uniform factor below two. The proof does not supply a constant factor below two for fixed Q,K with unbounded interaction, and it does not construct or rule out a genuine near-two hardness source in that remaining regime.
