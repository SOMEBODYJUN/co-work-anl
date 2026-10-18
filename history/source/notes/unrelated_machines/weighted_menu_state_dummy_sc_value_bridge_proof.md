# Proof: normalized weighted-menu state-dummy Santa Claus value bridge

Identity: `UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1`.

Frozen Exact dependency: `weighted_menu_state_dummy_sc_value_bridge_exact.md`, SHA-256 `ae57bf15737c54e6aadf8732869c242622ad75110facc2dbaed5fb8f7549320b`.

Root authorized this separate Proof after reporting an Exact-only independent reconstruction with no fatal issue. The author does not assert or invent a hash for that independently maintained review. This Proof is initially disclosed only to root.

The state-agent and one-fewer-dummy-item construction uses a standard selector device. The exact normalized domain, common value identities, complete original-job translations, endpoints, and explicit complexity are the content of this lemma. No new Santa Claus approximation or hardness theorem is claimed.

## 1. Resource allocation value and the constructed SC optimum

Use the domain and notation of Exact A--C. There is at least one group, and every group has K_g>=1 indexed states. Each state's nonnegative private weights have sum exactly one over its distinct resources. Extend a missing incidence's weight by zero. Thus every state value a_gs(B) is in [0,1], and so are the group maximum f_g(B) and the attainable maximum common value V(P). All relevant allocation sets are finite, so optima are attained. No allocation solver is assumed.

SC(P) has one agent b_gs per indexed state and one real item r_u per original resource. Its real-item valuations are p_gsu. Group g additionally has exactly K_g-1 dummy items, each valued at one by every state agent of g and zero by other agents. Each item is allocated at most once.

Take disjoint original resource sets B_g and, for each group, a state s(g) attaining f_g(B_g). Give b_g,s(g) the real items corresponding to B_g. Give the other K_g-1 state agents of g its K_g-1 different dummy items, one each. Real-item bundles are disjoint across groups, dummy sets are disjoint across groups, and all assignments are legal. The chosen state agent's utility is f_g(B_g), while every other state agent has utility at least one. Since f_g(B_g)<=1, the SC allocation's minimum utility is at least `min_g f_g(B_g)`. Applying this to an allocation attaining V gives

`OPT_SC(SC(P))>=V(P)`.

Conversely, take any SC allocation and denote its minimum utility by t. Group g has K_g state agents and only K_g-1 own dummy items. At most K_g-1 of its agents can receive any own dummy item, even if some agent receives several. Therefore at least one state agent b_g,s(g) receives no own dummy. All dummies of other groups have value zero for that agent. Its entire utility is consequently the value of its allocated real-item set, say B_g:

`a_g,s(g)(B_g)>=t`.

The selected agents' real bundles are disjoint because the SC allocation uses each real item at most once. Therefore `f_g(B_g)>=t` for all g, and V(P)>=t. This proves both the allocation decoder and

`OPT_SC(SC(P))<=V(P)`.

Combining inequalities gives `OPT_SC=V`. It also proves that every SC allocation has t<=1: a dummy-free selected state agent has real total value at most one. For K_g=1, no dummy exists and that group's only agent is the required dummy-free agent. Zero-valued real items and zero-valued foreign dummies never interfere with the decoder.

An at-most-once allocation and a partition of all items have the same optimum here. Every partition is an at-most-once allocation. An at-most-once allocation can be extended to a partition by assigning unused items arbitrarily, with no decrease in utility because all valuations are nonnegative.

## 2. Resource allocation to a complete original UM assignment

Take any disjoint B_g, and choose a maximizing state s(g) for each f_g(B_g). Put the original selector J_g on its selected original machine M_g,s(g). For each resource u in B_g intersect S_g,s(g), export that selected state's incidence job I_g,s(g),u to R_u. A zero-private-time incidence can instead remain private without affecting the exported private mass. Put every other original incidence job, from every selected and unselected indexed state, on its own original private machine.

Every original job has been assigned exactly once to one of its original finite eligibility options. Resource machines receive at most one exported job because the B_g are disjoint and each selected state contains distinct resource identities. Each such resource load is exactly one; unused resource loads are zero. Unselected private state machines have their full normalized incidence mass one and no selector. The selected private load is

`1 + (1-a_g,s(g)(B_g)) = 2-f_g(B_g)`.

Since all f_g(B_g)<=1, the maximum of these selected loads is at least one and dominates the upper bounds on unselected private and resource loads. Hence the schedule has makespan at most `2-min_g f_g(B_g)`. In particular

`OPT_UM(P)<=2-V(P)`.

Applying the dummy-free decoder of Section 1 to any SC allocation with minimum utility t yields disjoint B_g and one state per group with a_g,s(g)(B_g)>=t. The same original-job assignment then has makespan at most 2-t. Only one indexed state per group is used for its selector and export bundle; the construction never combines different state agents' utilities into one selected state.

## 3. Actual UM assignment to resource allocation and SC

Take a legal complete original UM schedule with actual makespan C<2. Every selector has processing time one, so C>=1. Let s(g) be its actual selected state. Let B_g consist of resources receiving externally assigned incidence jobs from that selected state. A resource-time-one job can share a resource with no other such job when C<2. Thus B_g are pairwise disjoint across groups. A state has at most one incidence for a resource, so its exported private mass is exactly a_g,s(g)(B_g).

All incidence jobs of the selected state have only the private state machine and their indexed resources as finite choices. Its private load, including its selector, is therefore exactly

`2-a_g,s(g)(B_g)`.

The assumed makespan bound implies `a_g,s(g)(B_g)>=2-C`. Consequently V(P)>=2-C. Alternatively, give B_g to b_g,s(g) in SC(P) and give one group dummy to each other state agent. Their utilities are at least 2-C and one, respectively, and `2-C<=1`. This gives the claimed SC allocation of minimum utility at least 2-C.

When a supplied schedule has C>=2, no disjointness argument is required or asserted: its requested guaranteed target is `max(0,2-C)=0`, and nonnegative SC values provide that target under any allocation. In particular C=2 is not silently treated as forbidding two unit jobs on one resource. This handles the zero-value boundary.

For every C<2, Section 3 proves `C>=2-V(P)`. For C>=2 the same inequality is immediate from V(P)>=0. Thus **every** complete UM schedule has load at least 2-V(P). Combining with Section 2 gives

`OPT_UM(P)=2-V(P)=2-OPT_SC(SC(P))`.

This argument includes OPT_UM=2 and V=0 without needing to recover a positive SC allocation from a load-two schedule. At the other endpoint V=1, Section 2 gives makespan at most one, and the selectors force equality. Finite optima exist because there are finitely many original jobs with finitely many eligible destinations.

## 4. Threshold equivalence and explicit value units

For supplied t in (0,1], an SC allocation of utility at least t converts by Sections 1--2 to a complete UM schedule of load at most 2-t. Conversely, a UM schedule of load C<=2-t has C<2, and Section 3 converts it to an SC allocation of utility at least 2-C>=t. At t=0, a nonnegative SC allocation and the full-private UM schedule of load at most two always exist. This proves the threshold equivalence for every t in [0,1]. It supplies conversions given assignments; it does not supply a decision or optimization algorithm.

The exact state normalization is part of the input domain. A constructed state agent has total **real-item** value one. It additionally values K_g-1 dummy items at one each, making its full item total K_g. Neither this full total nor OPT_SC is being normalized to one by guessing an optimum. The common value one is a fixed supplied unit induced by the normalized private budgets and unit dummies.

If a positive binary rational T is explicitly supplied as an alternative SC value unit, multiplying every SC valuation by T multiplies every allocation utility and OPT_SC by T. The identities then read `OPT_SC=T V(P)` and `OPT_UM=2-OPT_SC/T`; target t in UM units corresponds to SC target Tt. This is known common scaling, not a reduction from arbitrary externally given SC values to this normalized menu domain.

For merely W_gs<=1, the original unaugmented function V(P) need not satisfy OPT_UM=2-V(P). The earlier private-bonus normalization can first add one state-private bonus resource and a deficit job to each deficient state, preserving the UM optimum. This lemma then applies to the augmented resource sets and their normalized function. The equality does not identify that augmented function with the original unaugmented V. This proof does not require the bonus result because its own domain assumes W=1 from the start.

## 5. Explicit size and translation complexity

The SC agent count is exactly S, the real item count m, and the dummy count `sum_g(K_g-1)=S-n`. There are at most I explicitly retained original incidence valuations, with other real valuations zero by default. Each dummy of g has K_g nonzero valuations, so the exact dummy-incidence count is

`sum_g K_g(K_g-1)<=S^2`.

The dense SC valuation matrix has `S(m+S-n)` entries. Original rational values are copied, dummy values are one, and other entries are zero. All counts and bit lengths are polynomial in the explicitly listed original groups, indexed states, resources, and jobs. Optional common multiplication by supplied T also has polynomial binary length. No numeric valuation is implemented using item replication.

Given an SC allocation, scanning own dummy assignments finds a dummy-free agent for each group. Its actual real-item bundle gives the resource decoder. Given B_g, maximizing state values requires summing original rational weights over explicit menu entries. Given an original UM schedule, scanning selectors and incidence destinations gives the selected states and exported bundles when C<2. The reverse UM reconstruction assigns each of the n+I original jobs individually to an original eligible machine; it retains all incidence jobs of unselected states. All machine loads are sums of explicit binary rational processing times and can be recomputed in polynomial bit length. No enumeration over all state selections, SC allocations, or UM schedules occurs.

There is no degree preservation in SC agents. One real item can be valued by many states of each incident group, while each dummy item has K_g interested state agents. Even if a real resource belongs to at most Delta group unions, its SC agent degree can be as large as the sum of those groups' menu sizes. Thus this bridge does not justify applying an at-most-two-agents-per-item SC theorem to a group-degree-two UM input.

## 6. Gap consequence and remaining obligation

Selectors and normalization give `1<=OPT_UM<=2`, while the exact identities give `0<=OPT_SC=V<=1`. Therefore, for delta in (0,1),

`OPT_UM<=1` is equivalent to `OPT_SC=1`,

and

`OPT_UM>2-delta` is equivalent to `OPT_SC<delta`.

Strict and weak inequalities must be transferred as written; for example replacing the UM strict NO threshold by a weak inequality replaces the corresponding SC threshold by a weak one. The identities transfer an already proved promise but do not establish its computational hardness.

A one-versus-one-half SC value promise on this exact image class gives one-versus-three-halves UM thresholds by the same equation. It does not become an arbitrarily near-two gap. To use another external additive-SC, set-packing, or label-consistency source, one must separately prove the desired normalized YES value, the all-state-and-partial-export NO bound, explicit menu size, and any required group-degree constraint. Enumerating all valid bundles of an arbitrary additive agent is not part of this polynomial construction, and no polynomial inverse normalization is claimed.

The independently frozen degree-three zero-cell cube embedding may compose with this lemma on its stated source domain. It preserves the normalized UM optimum and hence the same V value, but does not manufacture the missing one-versus-arbitrarily-small quantitative source gap.
