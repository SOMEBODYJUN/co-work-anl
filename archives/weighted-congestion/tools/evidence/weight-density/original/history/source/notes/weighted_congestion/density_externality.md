# R2 original resource-externality derivation, 2026-10-14

This is a mathematical source record of the initial derivation, not a chat
transcript or a claimed complete theorem. The strengthened, independently
reconstructed finite proof is in
`research/current/weighted_congestion/weight_density.md`.

For a new resource used by a weight-w player, an incumbent of weight-v
contributes at most

    v^p min(1, d w/(w+v)) c(new total load)

to the increase of the proposed potential `sum_i w_i^p C_i`. With
`r=v/w`, the kernel is `r^p min(1,d/(1+r))`. Count incumbents in geometric
ratio-d bands and take `p=ln(2)/ln(d)`, `d>=3`. If every `[x,dx)` has at
most K potential users, the small, middle and large bands contribute at
most `2K`, `2K` and `2K/(1-2/d)`, respectively. This gives the preliminary
factor `1+K(4+2/(1-2/d))`, assuming the multi-resource move accounting is
completed. The `d=2` endpoint is excluded from this particular series.

The useful next observation is that every incumbent on the same newly
acquired resource experiences exactly the same cost increment. Hence the
externality can instead be written using its actual total weight S:

    min(1,d/(1+S)) sum_j r_j^p.

This removes the need to charge each incumbent using only its own weight.
The strengthened obligation is a sharp power-moment inequality for
geometrically sparse multisets. R2's internal independent reconstruction
provided a finite tail-sum telescoping proof. The current account proves
the full arbitrary-real version and all deviation accounting.

Provenance: derivation by the active R2 conversation; internal review was
requested through the subagent tool using gpt-6-astra/ultra with a clean
problem statement before the candidate route was shared. Requested tool
configuration is not an independently observed runtime model identity.
