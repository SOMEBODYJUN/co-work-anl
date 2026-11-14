# Shared-menu matching-loss denominator layers — worker note

Task `customer-attraction-3a-3a-9cc94bd73ba9fd12` was read through all seven declared reading passes (six distinct files; the large report is one file split over two passes). The assigned object is `cag-shared-menu-matching-loss-denominator-layers` (registration pin `ea6d2d0bb668ad855ab25e75f207f2d4fd6a1012a340276397dc32de8a075466`).

## Exact result and scope

## Model and quantifiers

The model is finite unit clients, a finite nonempty common **label** catalog (duplicate coverage labels and empty themes allowed), sequential unit providers, equal split of each covered client, and a fixed complete pure SPE over every ordered history, including off-path ties, repeated actions, zero clients, and arbitrary continuations. The lemma quantifies over every finite slot/menu system, positive real denominator loads, and nonnegative real weights fixed outside the client; the SPE application allows arbitrary `m` and `q >= 1` true terminal nodes. Each label group has equal source/target cardinality and each target tuple keeps one common label index across all menu units. D-complement rows are tied to the same tuple. The two-level specialization additionally assumes a common three-player prefix; without it, the general layer identity is the available statement.

For each finite common-label group of size `n`, positive source inverse denominators sorted as `d_(1) >= ... >= d_(n)`, nonnegative menu weights `w_j` fixed outside the client, tuple membership `z_i^j`, counts `k_j = sum_i z_i^j`, and tuple scores `S_i = sum_j w_j z_i^j`, the separate-minus-joint matching gap is

`Delta_t = sum_{r=1}^{n-1} (d_(r)-d_(r+1)) * [sum_j w_j min(k_j,r) - Top_S(r)] >= 0`.

The proof is an Abel/layer expansion of `Top_d(k)` and the joint sorted product. The bracket is nonnegative because any `r` target slots contain at most `min(k_j,r)` members of menu `j`. D rows are handled by complements `1-z` plus constants; complement positions remain tied to the same target tuple. Thus any fixed nonnegative O/D combination has a nonnegative matching gap. The resulting envelope is only a necessary full-client IC inequality: `sum_j w_j sum_x U^sep_{j,x} >= sum_{x,t} Delta_{x,t}`. It does not construct a shared menu, a complete strategy, or a payment into root welfare `W`.

For two unit-weight O menus with counts `(k,l)`, overlap `h`, and union `u=k+l-h`, the layer coefficient is `delta_r = max(0,min(r-h,k-h,l-h,u-r))`. Under a fixed common three-player prefix, source denominators have only two levels (`p+t+1` and `p+t+2`), so a group with `R` low-load A positions has `Delta = delta_R / ((p+t+1)(p+t+2))`; without that prefix, use the general layer identity. Strict positive loss needs exclusive membership competition for a common high inverse-denominator slot; counts alone do not force it.

## Finite evidence and boundaries

The declared report is passed with no external solver calls. It records 9,360 generic weighted three-menu checks, 9,008 two-menu trapezoid checks, and adjacent-load recovery (1,555 indexed lists, 798 margin pairs, 210 compatible pairs). The 69-atom point727 record has 217 distinct literal matchings and 20 strict-loss atoms; stored exact single-menu upper slacks are positive, the stored joint OO upper slack is negative, and the stored weighted loss is strictly positive (the report flags `independently_recomputed727_slacks: false`, so this is source/report evidence, not a fresh rerun). These checks support the fixed necessary-condition point only; they do not replace the arbitrary-size layer proof, and they do not establish a root-welfare or six-player half bound.

No read endpoint besides the assigned object was authorized. `CAG-MODEL`, `M-60da76cf3a0943d79e740518cf376645`, `M-f4f9ee21369d4955a807668976194386`, and `cag-shared-incidence-terminal-menu-upper-envelopes` were deferred candidates, so no logical edge was created. Shared model definitions and the finite checker are evidence for this lemma, not hub edges.
