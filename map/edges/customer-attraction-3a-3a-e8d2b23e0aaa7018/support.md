# Fixed common-Q witness and dual specialization

This support note records the single useful relation delivered by this 3A task. The endpoint theorem `CA-SECURITY-CONE-DUAL` states, for every fixed complete ordered-history strategy σ and rational query distribution p, the Farkas/minimax equivalence

`c − n E_Q β(p) = Γᵀλ + r`, with `Q, λ, r ≥ 0`,

for the whole fixed customer cone `K_σ`. The assigned core is one concrete n=4, k=6 strategy cone. Its reconstructed full ordered tree has 259 nodes / 1554 comparisons, 306 nonzero deduplicated rows, and exact scale `G=12Γ`. The exact rational reconstruction supplies one Q independent of the query: mass `3/4` on `(0,1,2,0,0,0)` and `1/4` on `(0,0,2,0,0,1)`. For each pure query a=0,…,5, the saved rational multipliers and nonnegative residuals satisfy

`c_T/4 − E_Q b_{a,T} = (λ_a·G)_T/12 + r_{a,T}`

for every 63 customer type columns. Multiplying by 4 identifies this with the endpoint theorem's certificate at p=δ_a; convexly mixing the six identities gives the theorem's certificate for every rational p while retaining the same Q. The finite witness therefore specializes the general fixed-σ,p dual interface and strengthens it by making Q common across all pure queries for this one σ.

The edge scope is exactly this specialization. It does not claim a certificate for arbitrary σ/p, does not upgrade the five-player floating candidate, and does not assert per-player safety or the six-player half target. The common-Q proof is on the one fixed cone shared by A/B/C; the three seeds are not three universal theorems.
