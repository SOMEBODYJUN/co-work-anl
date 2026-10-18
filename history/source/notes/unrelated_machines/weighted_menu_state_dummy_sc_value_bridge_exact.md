# Exact statements: normalized weighted menus and state-dummy Santa Claus value

Candidate identity: `UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1`.

Statement-first scratch freeze, 2026-10-18. This lemma isolates an exact value-and-assignment contract using the standard device of state agents and one fewer shared dummy item than agents. The selector idea is not claimed as new. No approximation backend, hardness theorem, production software, or finite-enumeration evidence is asserted. Proof disclosure is withheld pending independent Exact-only review.

## A. Complete normalized flat-menu UM domain

Let G be a finite nonempty group set and U a finite explicitly listed resource set. Every group g has a nonempty explicitly listed indexed state menu A_g, of size K_g. For every indexed state s, S_gs is an explicitly listed set of distinct resource identities, and every u in S_gs has a nonnegative binary rational private time p_gsu. Require the exact normalization

`sum_{u in S_gs} p_gsu=1` for every indexed state.

Zero-time incidences and duplicate indexed states are allowed. A normalized state has at least one positive incidence. States may have different resource sets and different weight vectors. There is no bound on menu sizes, resource group degree, resource state-agent degree, or group interaction.

The complete ordinary UM instance P consists of:

- one distinct private state machine M_gs per indexed state and one distinct resource machine R_u per resource;
- one selector J_g per group, eligible at time exactly one on every private state machine of that group;
- one distinct incidence job I_gsu per listed state-resource incidence, eligible on M_gs at time p_gsu and on R_u at time exactly one.

All other processing times are infinity. These are all machines, jobs, and eligibility options. Every job and indexed state is retained in scheduling translations below. In particular, incidence jobs of unselected states remain part of P.

Set `n=|G|`, `S=sum_g K_g`, `m=|U|`, and `I=sum_g sum_s |S_gs|`. Selectors imply `OPT_UM(P)>=1`; the full-private schedule has load at most two.

## B. Allocation value on resource subsets

Extend p_gsu by zero when u is absent from S_gs. For B subset of U, define

`a_gs(B)=sum_{u in B} p_gsu`,

`f_g(B)=max_{s in A_g} a_gs(B)`.

Let

`V(P)=max_{pairwise disjoint B_g subset U} min_{g in G} f_g(B_g)`.

Unused resources are permitted. Every a_gs and f_g lies between zero and one on every resource subset, and `0<=V(P)<=1`. Maxima are attained because the instance and allocation choices are finite. No value oracle or optimization algorithm is part of the input or the claim.

## C. Explicit additive Santa Claus construction

Construct SC(P) with one additive agent b_gs per indexed state. For each original resource u in U, include one real item r_u, whose value to b_gs is p_gsu, including zero when the original incidence was absent or had private time zero.

For every group g, add exactly K_g-1 distinct dummy items d_g,1,...,d_g,K_g-1. Each such item has value exactly one to **all K_g state agents of its own group**, and value zero to every agent of every other group. When K_g=1 there are no dummy items for that group. There are no other items or values.

An SC allocation assigns each item to at most one agent; agents may receive any finite number of items and items may remain unused. Utility is the sum of that agent's item values, and the SC objective is to maximize the minimum utility over all S agents. Requiring a full partition of all items gives the same optimum because values are nonnegative; this does not permit one item to be shared.

Private state machines and incidence jobs do not become separate SC items. There is exactly one real SC item per original resource; different state-incidence jobs on that resource give valuation entries for this one item. The complete original UM job assignment is reconstructed separately as specified below.

## D. Exact value and assignment claims

The construction is deterministic and polynomial in the explicit binary input length, and satisfies

`OPT_SC(SC(P))=V(P)`,

`OPT_UM(P)=2-V(P)=2-OPT_SC(SC(P))`.

Both identities include K_g=1, zero private times, V=0, V=1, and the boundary OPT_UM=2. No positive-value assumption is made. The following constructive translations are part of the claim.

1. **Resource allocation to additive SC.** Given pairwise disjoint resource sets B_g, choose for each g a maximizing indexed state s(g) for f_g(B_g). Give the real items of B_g to b_g,s(g), and give each of the other K_g-1 state agents of g one distinct group dummy item. This produces an SC allocation whose minimum utility is at least `min_g f_g(B_g)`. Other real items may stay unused.

2. **Additive SC to one state per group.** Given any SC allocation with minimum utility t, every group has at least one state agent receiving none of that group's K_g-1 dummy items. Choose one such agent b_g,s(g), and let B_g consist of the real items it received. Dummy items of other groups have value zero for it. Thus the B_g are pairwise disjoint and `a_g,s(g)(B_g)>=t` for every g. In particular t<=1 for every SC allocation, and this translation never combines real bundles of several state agents into one group bundle.

3. **Additive SC to a complete UM schedule.** Apply translation 2. Place J_g on M_g,s(g). Export the original incidence job I_g,s(g),u for every real item u in B_g that is an incidence of this selected state; zero-private-time jobs may instead be parked privately. Keep every other original incidence job, including all jobs of every unselected indexed state, on its own original private machine. The resulting legal complete UM schedule has resource loads at most one, unselected private loads exactly one, selected private loads at most `2-t`, and hence makespan at most `2-t`.

4. **Complete UM schedule to additive SC at positive target.** Given any legal complete UM schedule of actual makespan C<2, choose each group's selector state s(g), and let B_g be the resources receiving exported incidence jobs of this selected state. Every resource receives at most one unit-time job because C<2, so the B_g are disjoint. Each selected state exports private mass at least `2-C`. Giving B_g to its state agent and dummy items to all other state agents as in translation 1 produces an SC allocation with minimum utility at least `2-C`. This uses actual incidence-job destinations, not an assumed all-or-none selected state.

5. **Zero target and the makespan-two endpoint.** When a supplied UM schedule has C>=2, an arbitrary SC allocation with nonnegative minimum utility witnesses the guaranteed target `max(0,2-C)=0`. The positive-target construction in translation 4 is not applied at C=2, where a resource might receive two unit jobs. Conversely an SC allocation of value zero still translates by 3 to a legal complete UM schedule of load at most two.

Equivalently, for each supplied binary rational target `t in [0,1]`,

`SC(P) admits minimum utility >=t`

if and only if

`P admits makespan <=2-t`.

At t=0 both conditions always hold; at t>0 the reverse direction uses the strict inequality `2-t<2`. This is an exact feasibility equivalence and assignment conversion, not an algorithm to decide either side.

## E. Explicit normalization and target-value scope

The number one is a fixed unit in this construction, not an estimate or input guess for OPT_SC. The input supplies normalized state rows of real-item mass exactly one. The resulting SC agent b_gs has real-item total value exactly one and **full** item total value K_g, because it values its group's K_g-1 dummy items as well. The construction does not produce SC rows of full total value one.

No unknown optimum is used to rescale any value. If a different supplied common SC value unit T>0 is desired, multiplying every real-item and dummy value in this constructed SC instance by that explicitly supplied rational T gives `OPT_SC=T V(P)` and a target t in UM units corresponds to SC target Tt. This harmless common scaling is distinct from an unsupported normalization of an arbitrary external SC instance.

The identity `OPT_UM=2-V(P)` is asserted only under exact state normalization W_gs=1. It is not asserted for the same V(P) when merely W_gs<=1. The previously established private-bonus normalization may first convert that larger UM class to W=1 while preserving its UM optimum, but V must then be defined on the augmented normalized resource system, rather than silently reusing the original unaugmented function.

There is no reverse reduction from arbitrary additive SC input to normalized explicit state menus in this lemma. Listing every target-valid bundle of an arbitrary additive agent as a state can require exponentially many states. An external YES target and an external hardness promise need their own size, normalization, and soundness proofs.

## F. Explicit binary complexity and degree boundaries

SC(P) has exactly S agents, m real items, and S-n dummy items. Its nonzero or explicitly retained original value entries require at most I original state-resource entries; dummy incidences number exactly `sum_g K_g(K_g-1)`, at most S squared. Values absent from these lists are zero. In dense representation the agent-by-item matrix has exactly

`S(m+S-n)`

entries. All entries are zero, one, or copied original binary rationals. Explicit optional common scaling by T has polynomial bit growth. No numeric item replication is used. All these counts are polynomial in the explicit original state, resource, and incidence input; an SC target t is a supplied binary rational only for the stated threshold conversion and is not needed to construct SC(P).

Each translation scans explicit allocations, state lists, and original jobs. The dummy-free agent in each group is found by inspecting actual dummy-item assignments. Maximizing a_gs on a given B_g is a direct finite sum and menu scan. Every original UM job receives an original eligible destination, and all machine loads can be recomputed by binary rational arithmetic in polynomial bit length.

This construction does not preserve resource degree measured in SC **agents**. A real item may have positive value for many indexed states of one group, and each dummy item is valued by K_g state agents. An original resource appearing in at most Delta distinct groups can have SC agent degree as large as `sum_{g incident to u} K_g`; dummy degree is K_g. In particular a degree-two SC algorithm cannot be invoked by treating these state agents as if they were the original groups.

## G. Precise hardness and remaining-source obligation

For every fixed rational delta in (0,1), a proved normalized-menu promise

`YES: OPT_UM<=1`, `NO: OPT_UM>2-delta`

translates exactly into this constructed additive-SC promise

`YES: OPT_SC=1`, `NO: OPT_SC<delta`.

The same identity reads an already proved promise on this SC image class back into the UM promise. A gap between SC values one and one-half would give the UM thresholds one and three-halves, rather than arbitrarily near two. A claim of NP-hardness or a stronger complexity assumption requires an actual gap reduction into the stated normalized image class and its explicit size bound; this lemma supplies neither.

For the resource-group-degree-three source direction, this value lemma composes with the separately frozen exact zero-cell cube embedding. It clarifies the missing quantitative source contract and preserves its difficulty; it does not make a general SC hardness statement automatically belong to that degree-three normalized menu class.
