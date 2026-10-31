# Position aware root reply bound

Status: exact conditional necessary inequality derived from the original full-history SPE IC; this is not a six-player half proof or a target counterexample. It refines `root_supported_reply_bound.md` by retaining the position of the comparison query.

Fix an arbitrary optimal comparison tuple `T_1,...,T_m`, with union `O`, and fix a complete pure SPE with actual root union `U` and welfare `W`. For each position `i`, force the player at the actual prefix `(A_1,...,A_{i-1})` to choose `T_i`, and follow the unique continuation prescribed by the same strategy. Let `touch_i(x)` mean that some later prescribed action on this forced branch covers customer `x`.

Assign each customer of `O` to one index `i` whose comparison theme contains it. For a customer `x∈O\\U` assigned to `i`, the actual prefix has no cover of `x`. If `touch_i(x)` is false, the forced player receives a full unit from `x`; if it is true, at most `m-i` later providers also cover it, so the forced player receives at least `1/(m-i+1)`. For `x∈O∩U`, the forced player receives at least `1/m` regardless of the forced continuation. The original SPE IC therefore gives, with `r_i=m-i+1`,

`W >= |O\\U| - Σ_i (1-1/r_i) b_i + |O∩U|/m`,

where `b_i` is the number of assigned customers in `O\\U` touched on the forced `T_i` branch. Since `|O∩U|≤W`,

`OPT_m <= (2-1/m) W + Σ_i (1-1/r_i) b_i`.  (PBR)

The assignment can be chosen customer by customer. Define

`β(x) = min { (1-1/(m-i+1)) * touch_i(x) : x∈T_i }`,

where a non-touched occurrence contributes zero. Then the assignment-free form is

`OPT_m <= (2-1/m) W + Σ_{x∈O\\U} β(x)`.

For `m=6`, the position weights are `5/6, 4/5, 3/4, 2/3, 1/2, 0`. Thus a strict six-player half violation would require `Σ β(x) > W/6`. In particular, an omitted customer occurring in `T_6` has zero penalty because there is no later reply; only omitted customers whose every available optimal occurrence is touched on a sufficiently early forced branch can support a violation. This is a necessary condition from genuine ordered-history continuations. It does not aggregate welfare across mutually exclusive branches, so it does not close the main gap by itself.
