# Exact-only v2: deterministic 13/8 approximation for explicitly presented one-outer normalized-flat UM

Status: scratch structural rounding deduction. This v2 changes the threshold domain of the earlier unit-only learning note; that frozen note remains unchanged. It is not a theorem for general multicore menus, not a near-zero gap, and not a claim that every second-moment point has an actual joint state distribution. PSD is not needed for this restricted structure.

## 1. Complete physical domain and common SA1 system

There is exactly one outer group `M`, with finite indexed states `a`. State `a` has its own set of home resources `g_(a,j)`, `j in J_a`, with positive binary-rational weights `w_(a,j)` summing to one. All these homes are distinct over `(a,j)`.

For every `(a,j)` there is one helper group `H_(a,j)`. Its own indexed state is the singleton `g_(a,j)`, coefficient one. Its other states are arbitrary normalized nonnegative binary-rational fallback states on a finite resource set `B` disjoint from all homes. Fallback supports may overlap arbitrarily, including across different outer states. There are no other groups and no unprotected auxiliary cores.

Use the full ordinary normalized-flat UM matrix: one unit selector per group eligible at that group's distinct state-private machines; one original incidence job per listed state-resource pair, with time its original coefficient at its private state machine and time one at its exact resource machine; all remaining cells infinity. All unselected-state jobs and any listed zero incidences remain present. No logical side constraints are added to the actual schedule.


## New exact conclusion and quantifiers

For every explicitly presented finite normalized menu Q in the physical domain above, there exists a single deterministic total-bit-polynomial algorithm which, on Q alone, constructs the complete ordinary matrix P(Q) and outputs an assignment of every one of its original jobs such that

    C_max <= (13/8) OPT(P(Q)).

The input is the explicit typed menu Q (equivalently its generated matrix together with the displayed structural presentation), not an unrecognized arbitrary matrix. No feasible relaxation point, actual allocation, target optimum or oracle is supplied. The polynomial degree is absolute and does not depend on a denominator, state size, row width, number of helpers, or accuracy parameter. All given zeros, duplicate indexed states, and unused resources are retained.

This changes both the input contract and conclusion of the earlier given-point epsilon-squared theorem; it is a new special-case claim/version. It does not solve UM-TARGET-v1, does not recognize this presentation in an arbitrary matrix, and does not extend to multiple outer groups or helpers lacking distinct private homes.

The finite primitive-SA1 system available to a candidate algorithm is exactly that specified in the earlier Exact: every state partition, box, gate, unit-resource capacity, and per-state perspective quality row for a chosen rational 0<epsilon<=1 is multiplied by each of the same original A/Z binary primitives and by its complement. It is one common rational degree-two array. The point is not supplied: any use must construct and solve its explicit polynomial rational LP. Exact SDP, higher moments, and actual schedule optimization oracles are not provided.

This file supplies only model and quantified conclusion. No author proof, threshold-search recipe, welfare backend, implementation or novelty assertion is included.
