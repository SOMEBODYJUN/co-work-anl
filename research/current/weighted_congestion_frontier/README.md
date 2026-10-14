# Weighted congestion frontier: canonical interface

This is an independent mathematical model. It has no proved reduction to the facility-location or sequential customer-attraction tracks. The detailed research map, exact MODEL and claim identities live in [the WC branch](../../weighted_congestion_frontier/README.md). The root catalogs register reviewed local assets here without changing WC-TARGET v1's OPEN status.

## Model and quantifiers

For d≥0 let G_d comprise every finite weighted atomic congestion game with positive real player weights, finite nonempty player/resource sets and nonempty finite strategy families S_i⊆2^E. Empty strategies and zero-cost resources are allowed. Resource costs are nonnegative-coefficient polynomials of degree at most d. At a pure profile, resource load is the sum of participating weights and player cost is the sum of used resource costs, without multiplication by the player's weight. An α-PNE satisfies C_i(s)≤αC_i(t_i,s_−i) for every player and alternative. Zero costs are handled by this inequality.

The universal threshold a_*(d) is the infimum of α≥1 for which every game in G_d has an α-PNE. The goal is a full-class o(d) upper bound or a strictly improved verified infinite nonexistence lower family, eventually matching growth rates. None of the local assets below closes that goal.

## WC-R1-INTEGER-TRIAD v1: an exact local lower certificate

Weights `(16,2,5)`. Each player has binary actions. Introduce six resources in three pairs, using masks where 0 means absent, 1 means action zero, 2 action one. Masks `(0,1,1)/(0,2,2)` have costs `13x²`, `(1,1,2)/(2,2,1)` have `59x`, and `(1,2,1)/(2,1,2)` have `2x²`. A global action complement preserves costs.

For profiles `000,001,010,011`, the largest improvement ratios are respectively `1707/1523,1507/1403,286/267,963/898`. Their minimum is `286/267`; profiles `010,101` are equilibria at the endpoint. Thus the instance's best pure factor is exactly `286/267`, and `a_*(2)≥286/267`. The full costs and all deviations are [proved and replayed here](../../weighted_congestion_frontier/assets/R1/integer_triad/proof.md). This fixed-degree certificate is not an unbounded growth result; priority is unverified.

## WC-R1-RESOURCE-SUPPORT v1: a compositional obstruction

For arbitrary nonnegative nondecreasing resource costs, let r≥1 be the maximum number of potential users of a resource. The unweighted sum Φ=Σ_i C_i=Σ_e n_e c_e(x_e) decreases at every strict r-improvement. Indeed, for a deviation, partition resources into deleted D, added A and retained O. A deleted resource decreases Φ by at least its old latency; an added resource increases Φ by at most r times its new latency. Retained resources do not change. Hence

`ΔΦ≤r C_A(new)−C_D(old)≤r C_i(new)−C_i(old)`.

A global minimum over the finite pure product space is therefore an r-PNE. For r=0 all costs vanish and 1-PNE exist. This proves that any number of overlapping local gadgets still has a constant-factor equilibrium if every resource keeps bounded user support. A growing lower factor necessarily requires growing support. It does not prove that growing support suffices. See [full proof and boundary review](../../weighted_congestion_frontier/assets/R1/cyclic_layers/resource_support.md).

## WC-R1-SOURCE-D2-ENVELOPE v1: compare a specific literature formula

For the degree-two specialization of arXiv:2002.07466v3 equation (3), its integer-domain parameter supremum is at most `19/18`. For k=2 the first quotient is at most one. For k=1, simultaneous strict ratios greater than t force a=(1+w)²>t and

`F_t(n,w)=n(a−t)(1+w−tnw)−[t(1+nw)−1](ta−w²)>0`.

At t=19/18, put Q=tw(a−t)>0. Exact expansion gives

`F_n=F_1+(n−1)(F_2−F_1)−(n−1)(n−2)Q`,

`−1296F_1=148w³+3(24w−7)²+12w²+8w+1>0`,

`−324(F_2−F_1)=721w³+(42w−4)²+38w²+10w+2>0`.

For integer n≥1 this contradicts F_n>0, including n=1,2. Vanishing denominators are covered by the original strict polynomial inequalities. Thus the local triad exceeds this source parameter envelope, since `286/267−19/18=25/1602`. This is not an upper bound for G₂, and neither global degree-two priority nor source-envelope sharpness has been certified. [Complete source audit and algebra](../../weighted_congestion_frontier/assets/R1/source_d2_envelope/proof.md).

## Remaining frontier

The crucial unresolved obligation is an all-state construction with growing resource support and provably growing improvement ratios, or a universal existence mechanism beyond current linear-in-degree potential guarantees. The resource membership cone provides finite proof/attack interfaces, but finite searches and solver failures cannot decide that universal question. The branch state and public board record which precise interfaces are active; root claim/review ledgers preserve the same scope and evidence levels.
