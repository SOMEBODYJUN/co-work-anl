# A genuine root SPE violating the proposed last-menu budget

2026-10-24. **Analytic all-history construction and exact k=12 mode audit.** Capacity independently reconstructed and reviewed the simplified controller; see its separate review. The original Q-CAG-HALF remains OPEN. This construction refutes the helper budget

    m L <= W+u_m/2,

where b is the original root SPE's actual first m-1 prefix and

    L=max_p min_A sum_T p_T sum_(x in T) 1/(b_x+1+1_A(x)).

There is no widening to arbitrary backgrounds or partial equilibria. The actual outcome covers every customer, so it emphatically does not refute half. The input uses a fixed finite catalogue merely to refute this precise all-input helper; it is not a fixed-number positive-result project.

## 1. Unit-client input and exact result

For every integer k>=1, take m=k+3 unit providers and six common topics 0,1,2,3,4,P. The six core customer types and an independent P block are:

| Interested topics | Distinct unit customers |
|---|---:|
| {0} | 3 |
| {1} | 4 |
| {2,3} | 6 |
| {2,4} | 6 |
| {0,3,4} | 2 |
| {1,3,4} | 2 |
| {P} | 5k |

The old 23-client core and its original complete three-player SPE are due to `R-7e9f44beea424d469713364afe7dd180/credible_counterexample/payoff_cap_failure.md`. This note supplies the new all-k padding/controller argument; the original three-player strategy is not silently declared valid after adding P and k providers.

There exists a complete pure SPE, with all ordered histories and repeated choices retained, whose actual path is

    P^k,0,1,2.

Its payoffs, welfare, and optimum are

    u=(5,...,5,5,6,12),    W=OPT_m=5k+23.

At its actual last prefix b=P^k,0,1, the last-menu value is exactly L=6. Thus

    mL-W-u_m/2 = k-11.

Every k>=12 is a strict counterexample to this helper. For k=12 there are 15 providers and 83 distinct unit customers, with 90>83+6. At m=5 (k=2), this same formula gives helper gap -9; the family does not supply any m=5 separation or general welfare theorem. Its role is falsification of the universal helper, not a new small-m result.

## 2. Permanent complete-SPE exits

At any explicitly specified exit history, choose a genuine complete pure SPE of that exact remaining game by finite backward induction, and stay in it permanently. Different ordered exit histories may use independent choices. For concreteness, a deterministic version chooses a payoff-maximizing action, with the first label breaking ties, at every backwards-induction count state. This is a permissible complete-history strategy; it imposes no anonymity restriction on other SPEs.

A fixed current player's utility can only weakly decrease when further players select topics. Therefore an action's immediate utility after the current prefix is a valid raw upper bound on its final utility under any such complete-SPE exit. The proof uses this only to bound the player making the exit. It does not impose unpaid promises on earlier players' payoffs after a later deviation.

## 3. The old three-core-player good mode

The original core SPE selects root 0. Its second choices after first topic 0,...,4 are (1,2,3,4,2). Its last choices at ordered core histories (a,b) are the following, including repeats:

| a \\ b | 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|---:|
| 0 | 2 | 2 | 2 | 2 | 2 |
| 1 | 2 | 2 | 3 | 2 | 2 |
| 2 | 2 | 3 | 3 | 2 | 3 |
| 3 | 2 | 2 | 2 | 2 | 2 |
| 4 | 2 | 2 | 3 | 2 | 2 |

Its last player's maximum utility at every two-core prefix is:

| a \\ b | 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|---:|
| 0 | 12 | 12 | 6 | 9 | 9 |
| 1 | 12 | 12 | 6 | 9 | 9 |
| 2 | 6 | 6 | 6 | 5 | 5 |
| 3 | 9 | 9 | 5 | 8 | 6 |
| 4 | 9 | 9 | 5 | 6 | 8 |

Its second player's final utilities for the five choices, following that actual last rule, are:

| first \\ second | 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|---:|
| 0 | 5/2 | 6 | 6 | 6 | 6 |
| 1 | 5 | 3 | 9 | 6 | 6 |
| 2 | 5 | 5 | 5 | 6 | 5 |
| 3 | 4 | 5 | 5 | 4 | 5 |
| 4 | 4 | 5 | 6 | 5 | 4 |

The selected second action maximizes every row, and every possible first core action under these continuations obtains exactly 5. The tables follow directly from the six displayed unit-client types and verify the old complete core SPE. Every selected current utility is at least 5, at every one of its ordered histories.

After exactly k preceding P actions, enter **G mode** and execute this whole old core strategy, with precisely three providers left. Every core-action child remains in G with the extended core history, even if the action differs from the prescription. Any P deviation permanently exits to a true complete SPE. Such a P chooser already has at least k+1 P copies, so its final utility is at most

    5k/(k+1) < 5.

All prescribed core utilities are at least 5; hence these P exits do not invalidate any old core IC. This defines a genuine full SPE of the augmented three-player tail, including every repeated-core and P off-path history. Its actual core leaf is (0,1,2).

## 4. Saturated three-core punishment plans

Suppose an early P player instead selects a core topic T. Topic 0 has total size 5, so for T=0 attach an arbitrary permanent complete SPE immediately; that fixed deviator can never receive more than 5. **This raw cap eliminates any need for a four-core punishment.**

For T in {1,2,3,4}, use the following main plans for the next two core choices. P choices may postpone these core choices as defined below.

| fixed first core T | next core a | final core c | three core payoffs (T,a,c) |
|---:|---:|---:|---|
| 1 | 2 | 3 | (5,9,6) |
| 2 | 3 | 2 | (5,6,5) |
| 3 | 4 | 2 | (5,5,6) |
| 4 | 2 | 3 | (5,6,5) |

In every listed terminal, the immediate utility of **every further core query** is at most 5. The same holds for the three additional terminals below. Such a terminal is called saturated only as shorthand for this explicit numerical bound; it is not a new equilibrium assumption.

To control deviations by the second core actor, the immediate utility table after first T is:

| first T \\ current core query | 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 3 | 12 | 9 | 9 |
| 2 | 5 | 6 | 6 | 7 | 7 |
| 3 | 4 | 5 | 9 | 5 | 8 |
| 4 | 4 | 5 | 9 | 8 | 5 |

Except for the prescribed action itself and the following three exceptional alternatives, every entry is at most the prescribed second actor's final utility in the main table. Attach permanent complete SPE exits to all these raw-capped alternatives. For the exceptions, prescribe one additional core action:

| first T | alternative second a' | prescribed third c' | alternative actor payoff | third actor payoff |
|---:|---:|---:|---:|---:|
| 2 | 4 | 2 | 6 | 5 |
| 3 | 2 | 2 | 5 | 5 |
| 4 | 3 | 2 | 5 | 6 |

The alternative actor's payoff is no larger than its original prescribed utility (6,5,6 respectively). Each third actor gets at least 5. These alternative terminals are also saturated. No other second-core branch is omitted: the two tables list all five core actions after every first T.

For each main or exceptional two-core prefix, its prescribed third action is an immediate best response among all five core actions, as can also be read from the preceding maximum-utility table. Its utility is at least 5. Every other core choice therefore has immediate utility at most its prescribed utility; assign a permanent complete-SPE exit to each such choice. The prescribed third action enters the all-P saturated mode below.

All the statements in this section are exact finite algebra on the six fixed core customer types. They do not presume anything about P continuations. P is disjoint and will not change any of these core utilities on the prescribed branches.

## 5. P skips, deadlines, and the saturated all-P mode

An active punishment controller stores only its ordered core prefix and the specified next core action. Before the second core action it needs q=2 more core actors; before the final core action it needs q=1. Its domain has r>=q providers left, and all actions outside the stored core prefix have been P choices. Prescribe the specified next core action.

If the current player instead chooses P and r>q, retain exactly the same controller at the child. Along its normal subsequent choices it will still complete exactly three core actions and all other choices will be P. The total final P count is therefore m-3=k, and the P-skipping deviator earns exactly 5. Every prescribed core actor in Sections 4's main and exceptional controllers earns at least 5, so such a P skip does not improve its utility.

If the player chooses P at the deadline r=q, the prior prefix has a=3-q core choices and

    p=m-r-a=m-3=k

P choices already. Its new P choice therefore has raw final payoff at most 5k/(k+1)<5. Give this child a permanent complete-SPE exit. No continuation has been frozen, and no impossible extra core slot is assumed after the deadline.

After any prescribed saturated three-core terminal, enter **S mode**: prescribe P at every subsequent history reached without a new core deviation. With three fixed core choices, the maximum possible number of final P players is k, so every prescribed P player obtains at least 5 (exactly 5 along this mode). Any core deviation has immediate utility at most 5 by saturation, and future choices can only decrease it; give its child a permanent complete-SPE exit. This proves S mode optimal at every one of its ordered histories. It also proves all its exit children genuine by construction.

Backward induction over remaining players now verifies every active punishment controller. Its prescribed core child uses a previously verified smaller controller or S mode. Its P skip either retains a smaller remaining-player controller with payoff 5 or exits with raw payoff below 5. Its core alternatives either exit under an explicit raw cap or enter an exceptional one-core controller with the exact bounded alternative-actor payoff in Section 4. Every resulting ordered child has a complete SPE, so all the comparisons use true complete continuations.

In particular, after a first early core entry T=1,2,3,4 the fixed entrant's actual prescribed payoff is 5, as the main table states. P skips do not change it. Earlier-player payoff caps are not imposed on later-deviation exit branches; they are unnecessary for the original entrant's own IC, which compares its actual prescribed continuation.

## 6. Root normal mode and completeness of the full strategy

In **N mode**, the observed history is P^s with 0<=s<k. Prescribe P. If it is chosen, continue N until s=k, then enter G. If a core topic 0 is chosen, permanently enter an arbitrary complete BI subtree. If T in {1,2,3,4} is chosen, enter its Section 4 punishment controller. There are at least three subsequent providers after an early core entry, since s<=k-1; the controller needs only two, so its domain is valid.

The normal current P player's payoff is 5. A core-0 deviation has utility at most 5 by its bare topic size. A core-T deviation for T in {1,2,3,4} obtains 5 under its genuine main punishment continuation. Hence every N node is optimal. Backwards induction along the normal P clock, using the complete G and punishment subgames already proved, yields a full root SPE.

For clarity, modes are permanent choices on their specified history subtrees. A first BI exit never returns to N, G, an active controller, or S by later matching counts. G keeps its exact ordered core history; controllers keep their exact ordered core prefix while allowing P skips. Every history has one of these modes and each decision has a child for every one of the six actions. Each transition increases the observed action count and total depth by one, ending exactly at m. Thus the proof covers all ordered histories, repeated choices, and arbitrary later deviations; it is not verification of one proposed path.

The actual path stays in N for k P actions, then follows G to (0,1,2). The 23 core clients are all covered by 0,1,2, and P covers its 5k private clients. This proves the stated utilities and W=OPT_m=5k+23.

## 7. Exact last-menu value and helper failure

At the **actual** last prefix b=P^k,0,1, query topic 2 covers two untouched six-client blocks. Against any one extra action A, it receives at least 6, with equality for A=2. Therefore pure query 2 proves L>=6.

Conversely, for extra action A=2 the six query utilities (0,1,2,3,4,P) are

    (5/2,3,6,5,5,5k/(k+1)).

All are at most 6, so pure extra action 2 proves L<=6. These are legal pure primal/dual certificates in the exact finite static game; L=6 requires no optimization or numerical approximation. The last provider's actual payoff is 12. Thus

    (k+3)6 - (5k+23) - 12/2 = k-11.

The original proposed weak LAST budget is strictly false for every k>=12. Every instance still has W=OPT_m, so the original half conclusion holds with a large margin. Security's separate note evaluates the stronger retained-tax/augmented-menu interface on this same genuine SPE; that calculation is separate from the present controller proof.

## 8. Exact finite audit, scope, and provenance

`audit_padded_core_controller.py --k 12` expands all 83 unit clients and implements the simplified permanent-mode controller above. Every BI exit is the deterministic complete backwards-induction policy on its actual count state. The audit recursively verifies every reachable mode/count state and every one of its six legal transitions, computes the prescribed and deviating true terminals, and checks utilities using an integer common denominator lcm(1,...,15). It imports no repository model, optimizer, or SPE solver.

The saved `padded_core_k12_audit.json` reports 234 controller decision states and 38,656 BI decision states, with respectively 1,404 and 231,936 exact IC comparisons, minimum gap zero. This is an exact finite acyclic automaton audit covering every ordered history through deterministic mode transitions. It does **not** claim to enumerate the full ordered tree of size 1+6+...+6^14. The analytic Sections 2-6, not the finite parameter audit, carry the all-k quantifier.

Source and review separation: the old 23-client core and its good three-player strategy are pre-existing; capacity supplied the early padding lead and independently reviewed the corrected/simplified controller. Construction supplied the explicit raw-cap BI gluing, the core-0 simplification, the full theorem and definition-level finite audit. No external review or novelty certification is claimed.
