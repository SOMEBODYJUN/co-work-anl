# Exact candidate: joint weighted-menu rounding at item-group degree two

Candidate identity: `UM-DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v1`.

Statement-first scratch file, 2026-10-18. Proof is withheld pending independent review of these exact claims. This is a proposed direct application of a published additive MaxMin-balancing algorithm through an averaging reduction; no novelty or general-UM claim is made.

## Input domain

There is a nonempty explicit group set G. Each group g has an explicit nonempty indexed menu A_g of size `K_g <= K`, where `K>=1` is an integer. Each state s has a finite explicitly listed set `S_gs` of distinct resources from U, and arbitrary nonnegative rational private times `p_gsu` satisfying `W_gs=sum_u p_gsu <= 1`. No assumption is made that private weights are uniform within a variable, slice, or state.

Each resource belongs to the union of the state sets of at most two **groups**. It may occur in many states of either of those groups. Menus are never split into independently served agents.

The original ordinary UM instance has one private machine per indexed state, one machine per resource, one unit selector per group eligible at its own state machines, and one incidence job per `(g,s,u)` with time `p_gsu` at its private machine and time exactly 1 at its resource machine. All other times are infinity. There are no additional jobs, preloads, rejected tasks, or restrictions. Every original state and job is retained.

## Exact algorithmic claim

There is a deterministic algorithm, polynomial in the explicit binary input length and K's bit length, that returns either FAIL or a complete original-job schedule with

`C_max <= 2 - 1/(2K)`.

Whenever the original UM instance has `OPT<=1`, the algorithm must succeed. Consequently it decides the promise

`YES: OPT<=1` versus `NO: OPT>2-1/(2K)`.

Failure is only a certificate that the strict unit YES condition is impossible. Success does not certify `OPT<=1`. No unconditional absolute upper bound is asserted for every input. When K is fixed this gives a uniform positive distance from 2; when K grows, that distance may vanish.

The claimed algorithm handles heavy and diffuse states jointly through one additive allocation at the **group** level; it does not commit a heavy matching and then serve diffuse groups separately.

## Explicit proposed reduction, for independent checking

For every state introduce an auxiliary private bonus item `b_gs` of value `1-W_gs` to its own group and value zero to all other groups. This is an allocation auxiliary object, not an original UM job.

For each original resource u define the additive auxiliary value

`v_g(u) = (1/K_g) sum_{s in A_g, u in S_gs} p_gsu`.

Give `b_gs` auxiliary additive value `(1-W_gs)/K_g` to g alone. A resource with zero auxiliary value everywhere may be discarded from the auxiliary instance. Every auxiliary item has positive value to at most two groups, including the bonus items, which have degree at most one.

Use the published deterministic factor-2 algorithm for additive MaxMin allocation with at most two positive-value agents per item. After allocation, give every private bonus item to its owner. For each group choose one original state maximizing

`1-W_gs + sum_{u allocated to g, u in S_gs} p_gsu`.

Only the original resources allocated to g and lying in that chosen state are exported by g. All other original incidence jobs stay at their own state machines. The algorithm returns this schedule if its score test reaches `1/(2K)` for every group; otherwise it returns FAIL.

The independent-review obligations are: original unit feasibility gives auxiliary additive optimum at least `1/K`; group-level averaging is dominated by the maximum over a single state after private bonuses are included; and the original selected-root load is exactly 2 minus that state's score. These are proposed interfaces, not claims that multiple states are simultaneously realized.

## Primary published dependency

Jose Verschae and Andreas Wiese, *On the Configuration-LP for Scheduling on Unrelated Machines*, arXiv:1011.4957v1, Section 5.1, Theorem 12. Primary full text: <https://arxiv.org/pdf/1011.4957>.

The theorem supplies a combinatorial factor-2 algorithm for additive MaxMin-balancing with binary-input polynomial running time. The reviewer opened and read Section 5.1, including the two-endpoint input definition, preprocessing, bipartite pairing construction, theorem statement, and rounding proof. The intended use is that additive theorem only, not its unrelated-machines makespan integrality-gap result.

## Cube specialization and limits

In a tagged grouped `[d]^Q` coordinate-slice universe with injective group-incidence indices, a resource can occur only in groups whose indices appear among its Q coordinate values. Thus at most `min(d,Q)` groups can use a resource across all their states. In particular `Q=2` satisfies this exact input domain, regardless of d, clause arity, slice size, or cell-weight variation. If menus have at most seven states, the proposed strict-unit promise upper threshold is `27/14`.

The claim does not cover arbitrary Q, a resource shared by three groups, implicit exponentially large cubes, unbounded menus with a uniform constant independent of K, or resources allowing several unit jobs below makespan 2. It neither gives a near-2 source nor substitutes an unconditional actual bound for a conditional strict-unit promise algorithm.
