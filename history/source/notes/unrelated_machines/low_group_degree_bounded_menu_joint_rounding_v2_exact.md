# Exact statements v2: degree-two bounded-menu weighted UM approximation

Candidate identity: `UM-DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v2`.

Statement-first scratch file, 2026-10-18. This strengthens the unchanged promise-only v1 in `low_group_degree_bounded_menu_joint_rounding_exact.md`. Proof is withheld pending independent review. The reviewer proposed group-level averaging to root before writing a proof; root independently checked that mechanism, proposed the relative-OPT strengthening and exact bonus normalization, and the reviewer independently checked those statements before freezing this file. This is a direct structural application of a published additive allocation algorithm, with no novelty or general-UM claim.

## A. Complete actual input domain

Let G be a finite nonempty set of groups. Each group g has a nonempty explicitly listed indexed menu A_g of size K_g. Put `K=max_g K_g >= 1`.

Every indexed state s has a finite explicitly listed resource set S_gs, with no multiplicity inside a state. Empty sets may be allowed; their private sum below is zero. Every resource u lies in the union of state sets of at most two **distinct groups**. It may occur in arbitrarily many states of either group. Groups and states are never split into independent original agents.

For each incidence `(g,s,u)` specify a nonnegative binary rational private processing time p_gsu, with

`W_gs=sum_{u in S_gs} p_gsu <= 1`.

The complete ordinary unrelated-machines instance P contains:

- a private state machine M_gs for every indexed state;
- a resource machine R_u for every explicitly listed resource;
- one selector job J_g per group, with processing time exactly 1 at every state machine of its own group;
- one distinct incidence job I_gsu, with processing time p_gsu at M_gs and processing time exactly 1 at R_u.

Every unlisted time is infinity. All jobs must be assigned once. There are no other jobs, preloads, side constraints, job rejections, shared private machines, or hidden multiplicity encodings. Resources and private machines have distinct tags. Zero private times and duplicated states with distinct indices are allowed. All machines, states, resource memberships, and processing times are explicit.

## B. Normalized-state identity and group-level averaging

First suppose `W_gs=1` for every state. Define weighted clauses

`a_gs(B)=sum_{u in B cap S_gs} p_gsu`,

and the explicit XOS functions `f_g(B)=max_{s in A_g} a_gs(B)`.

Let

`V=max_{B_g pairwise disjoint subsets of U} min_g f_g(B_g)`.

The exact actual optimum is

`OPT(P)=2-V`, with `0<=V<=1` and `1<=OPT(P)<=2`.

Define one additive auxiliary valuation per **group**:

`v_g(u)=(1/K_g) sum_{s in A_g, u in S_gs} p_gsu`.

For every set B,

`f_g(B)/K <= f_g(B)/K_g <= v_g(B) <= f_g(B)`.

Each auxiliary resource has positive value to at most two groups. The auxiliary max-min additive optimum A therefore satisfies `A>=V/K`.

## C. Actual joint rounding and approximation guarantee

For all inputs in A, including zero private times and nonnormalized sums W_gs<=1, there is a deterministic algorithm, polynomial in the total explicit binary input length, that outputs a complete original-job schedule sigma with

`C_max(sigma) <= 2-(2-OPT(P))/(2K)`.

Consequently,

`C_max(sigma) <= (2-1/(2K)) OPT(P)`.

No optimum value, optimum allocation, YES witness, or feasible state-distribution certificate is supplied to the algorithm. K may grow with input length; the algorithm remains polynomial but its improvement over 2 may tend to zero. For every fixed K this is a uniform strictly-below-2 approximation for this exact structured class only. No sharpness of this factor is claimed.

For normalized inputs, the proposed algorithm applies the published deterministic factor-2 additive MaxMin-balancing algorithm to the group valuations v_g, obtains pairwise disjoint resource sets B_g, chooses for each group a single original state maximizing a_gs(B_g), exports just the jobs for that chosen state's allocated resources, and parks every other original incidence job at its own state machine. This is one joint allocation: it does not commit a heavy matching before serving diffuse states or realize multiple states of a group at once.

For nonnormalized inputs, use the optimum-preserving auxiliary normalization in D, run the normalized construction there, and then delete auxiliary bonus jobs from the output.

The promise consequence is that for every fixed K the class admits a polynomial-time decision algorithm for `YES: OPT<=1` versus `NO: OPT>2-1/(2K)`. This follows by checking the actual returned schedule. A failure to meet the absolute threshold is a certificate against the strict unit YES promise, not a claim that every input has that absolute upper bound. In particular this theorem does **not** assert an unconditional makespan `2-1/(2K)` for arbitrary inputs.

## D. Exact normalization by private bonus resources

For every state with W_gs<1 add one new private resource z_gs, unique to that indexed state, and one new bonus incidence job having private time `1-W_gs` at M_gs and time 1 at the resource machine R_zgs. States already having W_gs=1 need no new job. The selector menus and all original jobs and times are retained.

Denote the augmented normalized instance by N(P). Every state then has total private work exactly 1, and every bonus resource belongs to just one group. Thus the at-most-two-groups-per-resource condition is preserved.

The normalization preserves the actual optimum exactly:

`OPT(N(P))=OPT(P)`.

Projection of any augmented schedule to the original jobs cannot increase makespan. Conversely every original schedule of makespan C>=1 extends to the augmented instance by exporting **all** bonus jobs to their distinct private resource machines, without changing any original assignment and without increasing makespan. This includes bonus jobs of unselected states. The construction adds at most one resource and one job per state and does not hide an expansion depending on numerical values.

## E. Primary published dependency and bit complexity

The only external algorithmic ingredient is the additive MaxMin-balancing factor-2 algorithm of Jose Verschae and Andreas Wiese, *On the Configuration-LP for Scheduling on Unrelated Machines*, arXiv:1011.4957v1, Section 5.1, Theorem 12: <https://arxiv.org/pdf/1011.4957>.

The reviewer actually opened and read Section 5.1, including its definition that each item has at most two eligible agents, its preprocessing rule, bipartite pairing argument, theorem statement, proof, and binary-input running-time qualification. Root independently read the same primary section. The intended imported statement is the deterministic additive-allocation theorem, not the paper's makespan LP-gap construction.

For the auxiliary instance there is exactly one agent per original group. Each resource has at most two positive-value auxiliary agents by A's group-degree hypothesis; no unproved reduction from at most 2K state agents to two agents is used. Private bonus items, when needed, have degree one. Zero-valued items and edges can be omitted. The additive values v_g(u) are obtained by explicit rational addition and division by K_g, so their total bit length is polynomial in the original explicit encoding. Binary rational values can be scaled to integer values using a common denominator whose bit length is at most the sum of input denominator bit lengths. This is a bit-length operation, not replication by the denominator's numerical value.

The state maximizing its actual allocated private mass is found by scanning that group's explicit menu. Every original incidence job is then output at one of its two original eligible machines, and every selector at one of its original state machines. The final projection removes only auxiliary jobs introduced by D. No polynomial claim is made for a succinct representation with exponentially many unlisted resources or states. The imported algorithm is not claimed to have been implemented in the repository or in this scratch review.

## F. Cube consequence, two-state boundary, and scope

In a tagged grouped `[d]^Q` coordinate-slice system with injective group-incidence indices, any resource can occur only in groups whose incidence indices appear among its Q coordinate values. Hence it belongs to at most `min(d,Q)` distinct groups across all their states. In particular Q=2 satisfies A for arbitrary d, group arities, state set sizes, and arbitrary cell private weights of total at most 1. No within-slice uniformity or small-cell assumption is required.

If the menus have at most seven states, the corresponding approximation factor and strict-unit promise threshold are `27/14`. This is weaker than the unconditional unweighted cube `3/2` and DGR `19/15` bounds where those stronger hypotheses hold, but it survives arbitrary private cell weights and jointly handles heavy and diffuse choices.

For menus of size at most two, strict unit feasibility additionally has a direct 2SAT formulation: each pair of state choices whose positive-weight supports intersect is forbidden. Single-state groups are fixed choices. This elementary exact unit-threshold observation does not imply an exact optimum algorithm at larger makespans and is not the proof of C's quantitative approximation.

The theorem does not cover resource group-degree three, arbitrary Q with group-degree exceeding two, unbounded menus with a constant independent of K, or a different external processing-time/packing model. It does not prove a general unrelated-machines approximation below 2 or a near-2 hardness source. Its relative bound is a direct composition of clause averaging, published degree-two additive allocation, and the actual private-state job accounting.
