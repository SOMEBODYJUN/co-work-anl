# Exact statements: degree-three weighted menus embed in zero-weight cubes

Candidate identity: `UM-DEGREE-THREE-WEIGHTED-MENU-CUBE-EMBEDDING-v1`.

Statement-first scratch freeze, 2026-10-18. This is an exact instance-and-schedule embedding, not a new approximation algorithm or hardness source. A separate Proof is withheld pending independent Exact-only review. The source below is a complete explicit ordinary UM instance, not a literature hardness promise.

## A. Source flat weighted-menu domain

Let G be a finite nonempty group set, U a finite explicitly listed resource set, and A_g a nonempty indexed state menu for each group. Every state s has an explicitly listed set S_gs of distinct resources. Empty sets and duplicate indexed states are allowed. There is one binary rational private time p_gsu>=0 per listed state-resource incidence, with

`W_gs=sum_{u in S_gs} p_gsu<=1`.

The complete source ordinary UM instance P has one distinct private machine M_gs per indexed state, one resource machine R_u per u in U, one selector of time exactly one eligible on every state machine of its own group, and one incidence job I_gsu eligible on its own private machine at time p_gsu and its own resource at time exactly one. All other times are infinity. Every original indexed state, selector, resource machine, and incidence job is retained. There are no other jobs or eligibility options.

Write `U_g=union_s S_gs` and `q_g=|U_g|`. The only degree restriction is

`|{g:u in U_g}|<=3` for every resource u.

There is no menu-size bound, no interaction-degree bound, no assumption that q_g is positive, and no assumption that every listed incidence has positive private time. Let `K_g=|A_g|` and `S=sum_g K_g`. The group interaction degree M is computed from complete unions U_g; unused original resources in U are allowed.

## B. Target grouped-cube domain

The target C(P) is a weighted grouped coordinate-slice instance with fixed `d=Q=3`, realized as the same complete ordinary UM scheduling format:

- every variable x has its own tagged resource cube `{x} x [3]^3`, disjoint from other variables' cubes;
- every variable occurs in at most three groups, with distinct group incidence indices `j_x(g) in [3]`;
- a group's indexed state assigns one coordinate label in [3] to every variable of that group, and contains the corresponding full slice `{(x,a):a_label=j_x(g)}` of nine resource cells per variable;
- each indexed state has one distinct incidence job per cell of each such full slice, with private time a nonnegative rational and resource time exactly one;
- every state has private mass at most one, and one unit selector chooses among all its group's indexed private state machines.

The target expressly allows **zero cell weights**, arbitrary state-dependent cell weights, and distinct indexed states with the same coordinate-label vector. The state-dependent costs, private machines, and jobs retain the original state identities. This is not the more restrictive model in which a label vector uniquely determines all processing times or indexed states. It is not an embedding into a model requiring every cell weight to be strictly positive.

All cubes, state labels, slice-cell jobs, and resource machines are explicit. The construction never uses a succinct representation of `[3]^3`.

## C. Exact construction

For every original resource u in U, create a tagged variable x_u with all 27 cells of `[3]^3`, including if u was unused. Its incident groups are exactly `{g:u in U_g}`. Assign these at most three groups distinct indices `j_{x_u}(g)` in [3], for example in input order. Let

`a*=(1,2,3)`.

For every g with q_g>0, the target variables of g are exactly `{x_u:u in U_g}`. In **every** indexed state of that group, set the coordinate label of x_u to `j_{x_u}(g)`. Consequently a* belongs to that group's chosen slice, independently of the indexed state. The coordinate label does not encode the old state; the old state is retained as an indexed state with its own cost table.

In target state s of group g and variable x_u:

- at the active cell `(x_u,a*)`, place private time p_gsu if the original incidence I_gsu existed in S_gs, and identify this target job with that original incidence job;
- if the original state had no incidence on u, the active cell has an additional job of private time zero;
- every other cell of the selected slice has an additional job of private time zero.

For every group with U_g empty, create one extra dummy variable y_g occurring only in that group, with incidence index one and state label one in all its indexed states. All nine slice-cell jobs in each state have private time zero. This makes each target group's variable set nonempty without changing original jobs or interactions. All 27 cells of each dummy variable are explicit.

Map each original private machine, selector, and indexed state to the identically indexed target object. Map each original resource machine R_u to the active-cell resource machine `(x_u,a*)`. All other target machines and all other target jobs are auxiliary. The original zero-time incidence jobs, if any, are included in the identity map as well; they are not silently discarded or replaced.

## D. Exact claims

The construction is a deterministic polynomial-time map with the following properties.

1. **Fixed cube parameters and preserved menus.** `d=Q=3`, every variable belongs to at most three groups with injective incidence indices, every target group has at least one distinct variable, and its number of indexed states is exactly K_g. Target state private mass is exactly the original W_gs. All original processing times are preserved on the mapped original jobs and machines.

2. **Complete schedule extension.** Every legal source schedule extends to a legal schedule of the complete target instance with exactly the same makespan, by using the stated identity maps and assigning every auxiliary zero-private-time job to its own indexed private state machine. This includes auxiliary zero jobs in selected states and all jobs of all unselected states.

3. **Complete schedule projection.** From every legal target schedule, delete the auxiliary jobs and auxiliary machines and use the inverse identity map on every original job. This gives a legal complete source schedule with no larger makespan. An original mapped job has exactly its original two finite eligibility options and cannot use a nonactive auxiliary resource machine.

4. **Actual optimum equality.** `OPT(C(P))=OPT(P)` for the complete ordinary UM instances. In particular every actual makespan promise, including strict-unit YES and partial-export NO promises, transfers without changing its thresholds. This transfers an already proved promise; it does not supply one or make an existing allocation hardness result fit this source domain.

5. **Interaction and degree.** The target group interaction graph, using complete state-resource unions, is exactly the source group intersection graph on U_g. Source groups share some original u if and only if their target slices have a common resource in the corresponding x_u cube. The added dummy variables create no interaction. Hence the maximum group interaction degree M is preserved exactly, and target resource group degree is at most three. Source resource group degree zero, one, or two is allowed. No bounded M follows from fixed d=Q=3.

6. **Strict-unit support interpretation.** At makespan at most one, every positive-private-time incidence of a selected state must be exported. Zero-private-time incidences may stay at their private machine beside its selector. Accordingly, selecting states with pairwise disjoint **positive** support is equivalent to strict-unit feasibility in both instances, and the construction preserves these positive supports exactly under the active-cell identity. The full geometric slices themselves may intersect at zero-weight cells. Their geometric intersections do not encode an extra label-consistency constraint here.

## E. Explicit binary complexity

Let `e=|{g:U_g is empty}|` and `q'_g=max(1,q_g)`. The target has:

- exactly `27(|U|+e)` resource machines;
- exactly S private state machines and |G| selectors;
- exactly `9 sum_g K_g q'_g` incidence jobs;
- exactly the original K_g indexed states per group, with q'_g explicitly specified coordinate labels per state.

There is a distinct original-job identity for every original incidence; all remaining target incidence jobs have time zero privately and one externally. The products `K_g q_g` can exceed the number of originally listed incidences by more than a constant factor. The claimed bound is polynomial in the explicit input, not necessarily linear in original incidence count. Explicit source state and resource lists imply `sum_g K_g q'_g<=S max(1,|U|)`, up to the harmless groupwise bound, and all rational times are copied without numerical replication. Zeros, ones, labels, and new resource tags have polynomial bit descriptions.

If scheduling instances are written as dense job-by-machine matrices, the target matrix has

`(|G|+9 sum_g K_g q'_g) (S+27(|U|+e))`

entries, each infinity, zero, one, or a copied original rational. This is still polynomial in the explicit source input size. Sparse explicit eligibility lists give the smaller directly listed bound. No loop or object count depends on a binary numeric processing time.

## F. Scope and composition with the positive interaction bound

The embedding shows that arbitrary zero-weight, state-dependent `d=Q=3` cubes contain the complete resource-group-degree-three flat weighted-menu class. Fixed cube dimension alone does not reduce this class to the resource-degree-two case. Increasing the number q_g of variables in a group allows the preserved interaction M to grow.

Together with `UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2`, fixed M gives the embedded domain a below-two factor `2-1/(M+5)`, using Delta=3. That positive theorem and this exact embedding leave open arbitrary M, including the fixed-menu K>=3 regime. This does not assert that degree-three Santa Claus hardness automatically supplies a normalized strict-unit-vs-tiny-export promise.

The zero weights and cost dependence on the indexed state are essential to the stated construction. Adding a positive perturbation to all geometric cells can destroy exact strict-unit completeness, because selected positive supports would then include all overlapping slices. No perturbation argument or all-positive-cell result is claimed.
