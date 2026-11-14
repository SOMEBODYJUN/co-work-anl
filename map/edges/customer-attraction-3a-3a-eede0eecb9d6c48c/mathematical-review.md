# M-e88 finite aligned-dual separation review

## Exact result

The assigned object is the finite necessary-condition projection for the common labelled-catalogue model. On its fixed 2,196-row system, the stored `reopt_aligned.json` vector has 2,196 named multipliers, 36 positive active rows, source support of 64 atoms, and stored beta `1.9844871781654265`. The complete saved `price_aligned.json` report contains exactly 1,024 distinct legal atoms, one for each ten-bit mask; every saved column has the exact residual

\[
\rho(a)=\beta W(a)-O(a)-\sum_{n=1}^{2196}\lambda_nG_n(a)<0
\]

when the stored Python binary floats are interpreted as their exact rational values. The minimum exact residual is
`-224400578905030835/72057594037927936`, and the largest float replay discrepancy is below `9e-16`. The column distribution is `(W,O,d)=(0,1,1)` for 32 columns, `(1,1,1)` for 987, and `(1,1,2)` for 5.

This proves a finite separation statement: the specified stored 64-support dual cannot be a nonnegative all-column pricing certificate for the 2,196-row projection. It does not construct a nonnegative primal mass satisfying all rows, a labelled catalogue, a full ordered-history strategy, or a pure SPE.

## Evidence and comparison

The first three staged sources fix the model, all-history pure-SPE quantifiers, and the special aligned pricing contract. The two halves of `price_aligned.json` were read byte-for-byte and parsed; `reopt_aligned.json` binds the exact 2,196 names, lambda vector, 64-point support, and beta. The replay report independently re-evaluates all 2,196 coefficients for the saved columns and records all 1,024 negative columns, their atom hashes, exact binary-float rational residuals, and maximum replay error `8.881784197001252e-16`.

The aligned program is a special 36-row active support with fixed cross-family statistics. Its finite negative columns reject this particular stored vector. The adjacent `added65`/block report and later 38-support material remain distinct parameter vectors and search domains; matching or nearby beta values do not transfer the aligned conclusion to them. The block procedure is heuristic and does not search `d=0`; no joint global optimum is claimed.

## Remaining obligations

The result cannot be promoted to a universal statement that every dual fails, an infeasible-primal certificate, a low-welfare instance, an exact `OPT_6` comparison, or a six-person half counterexample. A transfer to the full game would still require a legal common directory, all ordered off-path histories, real continuation incentives, and an explicit bridge from the finite projection to `2W >= OPT_6`. Those obligations remain open.
