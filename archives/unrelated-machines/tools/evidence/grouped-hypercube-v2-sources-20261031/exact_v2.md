# Exact statements: grouped hypercube-slice scheduling, v2

Candidate ID: **UM-GROUPED-HYPERCUBE-SLICE-SCHEDULING-v2**.

Frozen on 2026-10-18. This exact-statement file and `um_grouped_hypercube_slice_scheduling_v2_proof.md` form a pair. The predecessor `bicriteria_hypercube_hall_exact.md` is preserved unchanged. All formal statements and input assumptions are here; proofs are in the paired file. These are structural statements about a normalized explicit construction class, with no claim of literature novelty or approximation hardness.

Provenance of the v2 strengthening: root first proposed the full-class actual `3/2` upper bound and sharp example. The independent reviewer identified as rainbow reached the same conclusion and supplied the shorter Bernoulli proof used in the paired proof file. This author independently checked that argument and the sharpness construction. A's general Hall bound and B/C's DGR `19/15` specialization are retained from v1.

## Exact statements


### A. Input model and general Hall allocation theorem

Fix integers `d >= 1` and `Q >= 1`. Write `[d] = {1,...,d}` and `[Q] = {1,...,Q}`. Let `X` be a finite set of variables and `G` a nonempty finite set of groups.

For every group `g`, specify a nonempty **set of distinct variables** `X_g` and a nonempty finite, explicitly listed set of states `A_g`. For every variable `x`, require

\[
G(x):=\{g\in G:x\in X_g\},\qquad |G(x)|\le d,
\]

and specify an injective incidence-index map

\[
j_x:G(x)\hookrightarrow[d].
\]

A state `s in A_g` assigns one label `ell_{g,s}(x) in [Q]` to each `x in X_g`. Thus a state uses each variable at most once, and it uses exactly one slice of that variable's gadget. Different states may have identical label vectors; they remain separately indexed states. No condition of consistency between different states is imposed.

Define tagged, mutually disjoint variable universes and their slices by

\[
U_x:=\{x\}\times[d]^{[Q]},\qquad U:=\biguplus_{x\in X}U_x,
\]
\[
P_{x,i,j}:=\{(x,a)\in U_x:a(i)=j\},\qquad
S_{g,s}:=\biguplus_{x\in X_g}P_{x,\ell_{g,s}(x),j_x(g)}.
\]

The variable tag is part of a resource's identity. There is no identification of resources belonging to different variables. Set membership has no multiplicity. Put

\[
h:=d^{Q-1},\quad q_g:=|X_g|,\quad k_g:=q_gh=|S_{g,s}|,
\quad c_d:=1-(1-1/d)^d.
\]

For every choice function `s(g) in A_g`, simultaneously for every subfamily `F subseteq G`,

\[
\tag{A1}
\left|\bigcup_{g\in F}S_{g,s(g)}\right|
\ \ge\ c_d\sum_{g\in F}k_g.
\]

Consequently, with

\[
b_g:=\lfloor c_dk_g\rfloor,
\]

there are pairwise disjoint resource subsets

\[
\tag{A2}
B_g\subseteq S_{g,s(g)},\qquad |B_g|=b_g\quad(g\in G).
\]

This is an **all choices, all groups** guarantee. It does not rely on a YES promise or on any CSP satisfiability property. Globally equal set sizes are not required; `q_g` and hence `k_g` may vary between groups. Within a group, the model makes its state sets equally sized because `X_g` is fixed.

The stronger fractional statement with each demand equal to `c_d k_g` also holds. The integral statement guarantees `floor(c_d k_g)` resources, not `ceil(c_d k_g)` and not necessarily a literal `c_d` fraction after rounding.

Degenerate cases:

- If `d=1`, then `c_1=1`, and all selected sets are already disjoint: each variable belongs to at most one group. No expression `0^0` is used in the proof.
- If `Q=1`, then all selected sets are already disjoint: each variable's single partition is addressed by the distinct indices `j_x(g)`. Here one may replace `c_d` by the sharper constant `1`.
- `Q=0` and `d=0` are outside the statement. Empty `X_g` are excluded to keep later normalization by `k_g` defined. Adding empty groups with demand zero would not change (A1)–(A2).

### B. Binary degree-five specialization

Under A's hypotheses with `d=5` and `Q=2`, replace `c_d` in (A1) by `19/25`. Thus

\[
\tag{B1}
\left|\bigcup_{g\in F}S_{g,s(g)}\right|
\ge\frac{19}{25}\sum_{g\in F}k_g.
\]

In particular, when every group has exactly three distinct variables, `k_g=15`, and **any choice of one state per group admits disjoint subsets of size 11 for every selected state**.

The value `19/25` is the exact minimum of the local union-to-total-slice-size ratio over nonempty choices of at most five distinct incidences in one binary gadget. This does not assert that 11 is the best possible global integer guarantee after optimizing the state choices.

### C. An actual ordinary unrelated-machines construction

More generally, start with any explicitly listed, nonempty, indexed set menus `{S_{g,s}:s in A_g}`, with `k_{g,s}:=|S_{g,s}| >= 1`, over a universe `U`. This part does not assume the slice structure or equal sizes.

Construct ordinary `R||C_max` as follows. The tags below make all machines and jobs distinct.

| Object | Definition and finite processing times |
|---|---|
| State machine `M_{g,s}` | One for each indexed state. |
| Resource machine `R_u` | One for each `u in U`. |
| Selector job `J_g` | Processing time `1` on every `M_{g,s}` of its own group. |
| Incidence job `I_{g,s,u}`, for `u in S_{g,s}` | Processing time `1/k_{g,s}` on `M_{g,s}`, and processing time `1` on `R_u`. |

Every unlisted processing time is infinity. Every job must be scheduled once; there are no rejected jobs, additional constraints, or altered objectives.

**C1, completeness.** If one can choose one state per group whose entire sets are pairwise disjoint, this UM instance has optimum exactly `1`.

**C2, explicit upper bound.** For any choice `s(g)` and any pairwise disjoint subsets `B_g subseteq S_{g,s(g)}`, with integer sizes `b_g`, the instance has a schedule of makespan

\[
\tag{C2}
\max\left\{1,\max_{g\in G}\left(2-\frac{b_g}{k_{g,s(g)}}\right)\right\}.
\]

Apply C to A with the demands in (A2). This gives an unconditional upper bound on every such input, whether its generating CSP is YES or NO. Apply C to B with three variables per group. Then **every input admits a schedule with**

\[
\tag{C3}
C_{\max}\le 2-11/15=19/15.
\]

In particular the construction obtained from the DGR clause menus cannot yield a `1` versus nearly `2` UM gap. This statement concerns the concrete ordinary-UM construction above, not a bicriteria or set-packing objective substituted for UM.

### D. Uniform absolute scheduling bound 3/2, attained exactly

This section assumes the hypercube input model A and the actual UM construction C. Its bound applies to every input, without any YES promise, and to every initial choice of one state per group.

**D1, half allocation.** If `d>=2` and `Q>=2`, for every state choice there are pairwise disjoint subsets

\[
B_g\subseteq S_{g,s(g)},\qquad |B_g|=\lceil k_g/2\rceil\quad(g\in G).
\]

These subsets are found by the same integral max-flow algorithm as in A, using demands `ceil(k_g/2)`. If `d=1` or `Q=1`, the selected sets are already pairwise disjoint, so their entire resource sets can be allocated.

**D2, actual scheduling consequence.** Every UM instance constructed by C from A has optimum at most `3/2`. More precisely, for `d>=2,Q>=2` it has an explicitly constructible schedule of makespan

\[
\max\left\{1,\max_g\left(2-\frac{\lceil k_g/2\rceil}{k_g}\right)\right\}\le\frac32.
\]

If `d=1` or `Q=1`, its optimum is exactly `1`. The bounds of A, B, and C remain valid; in particular the DGR specialization retains the stronger unconditional `19/15` bound.

**D3, exact sharpness as a normalized absolute bound.** The constant `3/2` in D2 is attained by a finite instance of A and C. Take `d=2,Q=2`, one variable `x`, and two groups `g_1,g_2`, each with exactly one state and variable set `{x}`. Let `j_x(g_1)=1`, `j_x(g_2)=2`, and let their state labels be `1` and `2`, respectively. Suppressing the common variable tag, their sets are

\[
S_1=\{(1,1),(1,2)\},\qquad
S_2=\{(1,2),(2,2)\}.
\]

The associated ordinary UM instance has two selector jobs, each forced to its unique state machine, and four incidence jobs, with processing times `1/2` on their own state machine and `1` on their indexed resource machine. The fourth cube resource `(2,1)` is unused. Its optimum is exactly `3/2`.

The meaning of sharpness is

\[
\max_{\text{all explicit inputs satisfying A}}
\operatorname{OPT}(\text{construction C})=3/2,
\]

where C fixes the normalization by giving selectors processing time `1` and total private incidence load `1` per state machine. It is not an NP-hard approximation threshold, a configuration-LP gap, a YES/NO hardness gap, or an assertion that the sharp example has a full disjoint state selection. The statement concerns this structured construction class only.

### E. Explicit representation and bit complexity

The algorithmic claim is polynomial time in the **explicitly materialized resource/incidence instance**, not in a succinct encoding of a potentially exponential cube.

Let

\[
n_U=|X|d^Q,\qquad a=\sum_g|A_g|,\qquad
L=\sum_g\sum_{s\in A_g}|S_{g,s}|.
\]

All groups, states, variable incidences, labels, resource identities, and state-resource memberships are explicitly represented, or the latter two are materialized before applying the algorithm. Binary integers and rational processing times are used. For any fixed choice of states, (A2) is found by an integral maximum-flow computation with source-to-group capacities `b_g`, group-to-member-resource capacities `1`, and resource-to-sink capacities `1`. This network has `O(|G|+n_U)` vertices and `O(|G|+n_U+sum_g k_g)` edges.

The constructed UM instance has `a+n_U` machines and `|G|+L` jobs, with two eligible machines per incidence job. Its finite times are `1` and `1/k_{g,s}`, encoded using `O(log(k_{g,s}+1))` bits. An explicit dense processing-time matrix, if required instead of eligible-machine lists, also has polynomial size in these explicit counts.

For `d>1`, `c_d=(d^d-(d-1)^d)/d^d` has `O(d log(d+1))` bits. Since nonempty explicit cubes have `n_U >= d`, calculating `floor(c_d k_g)` exactly is polynomial in the explicit input size. Handle `d=1` directly. If `d,Q` are variable binary parameters and only the compact labels/incidence descriptions are provided, `d^Q` can be exponential in that compact description. No polynomial-time claim for that succinct input model is made. DGR's specialization has fixed `d=5,Q=2`, seven states per group, and fixed set size 15, so materialization is linear in its formula size.

## DGR source audit and the distinction between its problem and ours

Primary full text: Sami Davies, Venkatesan Guruswami, Xuandi Ren, *Scheduling Problems with Constrained Rejections*, arXiv:2511.00184v1, submitted 2025-10-31.

- Exact URL: <https://arxiv.org/html/2511.00184v1>
- Relevant locations: Definition 3; Theorems 2–4; Section 3; Section 5, especially “Reduction,” “Construction of the gadget,” and “Choice of Parameters.”
- One short quotation (14 characters): “degree-5 3-CNF”. No other source prose is quoted in this note.
- Bibliographic brief-announcement URL: <https://doi.org/10.1145/3816782.3819185>. The full arXiv proof, rather than the brief abstract, was checked.

DGR's Theorem 4 is **ungrouped set selection** hardness. Its proof uses degree-five 3SAT, seven sets per clause, binary labels, and size-15 sets. With `m` clauses it has `7m` sets and `15m` resources; the YES `m` sets partition the universe. Its parameters are `alpha=1/7`, `beta=(1-epsilon_0)/7`, `epsilon<1/30`. Section 3 turns sets into agents, gives normal items value `1/15`, adds `6m` universal dummy items of value `1`, and obtains rejection loss `delta=epsilon_0/7`. These are existence-of-constants NP-hardness claims, not arbitrary-small retained-value claims.

**Our grouping is an additional definition:** one group per clause, with its seven satisfying local assignments as states. In the standard size-15 construction, each clause uses three distinct variables. This gives exactly B's hypotheses. A satisfiable global assignment selects one full state per clause; the incidence-index partitions then cover each variable universe. In contrast, (B1) and C3 apply to every formula without using satisfiability.

The discrete distinction is also immediate: with 15-element sets, retaining `(1-epsilon)15` elements for `epsilon<1/30` forces retaining all 15 elements. Thus DGR's displayed constants do not themselves create a low-retention hardness statement. If a strict decision gap rather than a boundary “at most” statement is needed, choose an intermediate constant packing target between `(1-epsilon_0)m` and `m`; this avoids relying on the equality boundary in the displayed beta.

## What is established, what is elementary, and possible escape mechanisms

The Hall proof uses only an exact product-union calculation and capacitated Hall/max flow. V2's full-class 3/2 bound adds the Bernoulli estimate (P3), the divisibility of k_g by d, and a direct four-cell sharp example. It is best described as an **elementary structural corollary** of the hypercube partition gadget, specialized here to test this proposed bridge. A limited exact-phrase literature check did not locate this precise grouped statement or `19/15` observation. That is not evidence of novelty and no novelty claim is made; the same caution applies to the v2 3/2 corollary. The construction in C is the standard selector/configuration-machine pattern; its direct proof is included so the conclusion does not depend on transferring an approximation theorem with a different objective.

The full-class 3/2 corollary strengthens the source-specific obstruction. The theorem rules out escaping by only enlarging `Q`, enlarging clause arity, changing the CSP predicate, or increasing `d`, while retaining all of A's hypotheses. The guarantee remains approximately `1-1/e` before integral rounding. Uniformly replacing every resource by the same number of private copies preserves the same union-ratio proof. It cannot produce the required tiny-fraction NO case.

The proof can fail if one changes its actual resource structure, for example:

1. **Nonproduct slice systems or repeated incidence indices.** The exact product complement or the bound `r_x <= d` can disappear. This is an escape from this Hall lemma only. In particular, it does not by itself escape the project's separate `5/3` obstruction for uniform injective star menus.
2. **Identifying resource names across variables, or repeating a global resource within a state's nominal leaves.** Tagged-universe additivity or the injective set interpretation then fails. A useful hardness construction must still preserve YES feasibility and force difficult global state choices; a fixed congested menu or pinned noninjective tree alone does not do so.
3. **Several processing scales or state-dependent additive values.** A cardinality allocation of 11 cells need not deliver the required weighted offload. Such a candidate needs a direct ordinary-UM soundness proof tracking the actual processing times, including every eligibility edge. Calling global item sizes “unrelated” without machine-dependent processing times would not establish this escape.

These are mechanisms outside the proved hypotheses, **not new hardness results or identified hard sources**. This note identifies no source giving the desired near-2 hardness. It freezes a constructive exclusion for this entire hypercube bridge class, including the sharper DGR specialization and an exact location of the assumptions a different mechanism would have to change.
