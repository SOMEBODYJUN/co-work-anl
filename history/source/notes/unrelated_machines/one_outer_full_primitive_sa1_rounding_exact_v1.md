# Exact-only: one outer private-home/fallback core, full primitive SA1

Status: scratch structural rounding deduction. This v2 changes the threshold domain of the earlier unit-only learning note; that frozen note remains unchanged. It is not a theorem for general multicore menus, not a near-zero gap, and not a claim that every second-moment point has an actual joint state distribution. PSD is not needed for this restricted structure.

## 1. Complete physical domain and common SA1 system

There is exactly one outer group `M`, with finite indexed states `a`. State `a` has its own set of home resources `g_(a,j)`, `j in J_a`, with positive binary-rational weights `w_(a,j)` summing to one. All these homes are distinct over `(a,j)`.

For every `(a,j)` there is one helper group `H_(a,j)`. Its own indexed state is the singleton `g_(a,j)`, coefficient one. Its other states are arbitrary normalized nonnegative binary-rational fallback states on a finite resource set `B` disjoint from all homes. Fallback supports may overlap arbitrarily, including across different outer states. There are no other groups and no unprotected auxiliary cores.

Use the full ordinary normalized-flat UM matrix: one unit selector per group eligible at that group's distinct state-private machines; one original incidence job per listed state-resource pair, with time its original coefficient at its private state machine and time one at its exact resource machine; all remaining cells infinity. All unselected-state jobs and any listed zero incidences remain present. No logical side constraints are added to the actual schedule.

Fix a rational threshold `0<epsilon<=1`. For binary state indicators `A_(g,s)` and claim indicators `Z_(g,s,u)`, the base system is

\[
 \sum_s A_{gs}=1,\quad
 0\le A_{gs},Z_{gsu}\le1,\quad Z_{gsu}\le A_{gs},
\tag{1}
\]
\[
 \sum_{g,s}Z_{gsu}\le1\quad(u\in U),\qquad
 \sum_u p_{gsu}Z_{gsu}\ge\epsilon A_{gs}\quad(g,s).
\tag{2}
\]

Every row of (1)–(2) is multiplied by every one of the **same** original `A/Z` primitives and by its complement. First and symmetric second moments belong to one common array, and `Y_XX=x_X` for each binary primitive. All nonnegative/box/gate rows are included. This is the literal strong primitive-SA1 system used below. Adding whole-core quality rows, unit-FSLP rows or M1 PSD does not invalidate the conclusion.

**Conclusion.** Given a rational feasible common SA1 point, one can deterministically construct, in total-bit polynomial time, a disjoint all-group actual allocation and a complete ordinary schedule with

\[
 \boxed{V\ge\epsilon^2/4,\qquad
 C_{\max}\le2-\epsilon^2/4.}
\tag{3}
\]

For every fixed positive epsilon this rules out vanishing quality in this exact one-outer architecture. It makes no conclusion for several simultaneous outer groups or for auxiliary groups without own homes.


This file contains only the model, moment system, quantified conclusion and limits; no proof or implementation is supplied. The input is the explicit menu plus a rational feasible common SA1 point. All finite indexed fallback states are explicit, normalized, and may have zeros/duplicate indices. No general feasible-point finder or unrestricted-UM statement is included. Zero fallback mass and lambda-zero states are permitted.
