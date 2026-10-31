# Provisional review — Boss11 shared UD tiny-home k² v4 Exact-only

Source ID: `3001ace70a0b1621eb88`
Path: `history/source/notes/unrelated_machines/boss11_shared_ud_tiny_home_k2_refinement_exact_v4.md`
SHA-256: `8948b47cc8b2f303f7f1446ecb0137da163d0b65e906ec4169c5f85294ef877d`
Size: 2486 bytes; both frozen commits point to the same source bytes.

## Reading and comparison

The complete 2486-byte source was read. It is an exact-only statement, explicitly withholding proof and implementation. Its identity is `UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v4`. The domain is a normalized-flat typed input with single-state outers, physically distinct homes, one own-unit helper per home, arbitrary shared B fallback states, and optional exact-threshold UD leaves. For `k=1`, no home tiny-weight cap is imposed beyond normalized positive weights; for `k>=2`, the cap is `1/(16384 k^2)`. Zero/incidence/duplicate/unused jobs remain in the full ordinary UM output.

The exact quantifiers require a fixed deterministic worst-case bit-polynomial algorithm, using only the explicit input Q, to output every original job with `C_max <= (19/10) OPT(P(Q))`; no OPT, joint law, feasible LP point, profile, precision, or SDP oracle is supplied. The source explicitly leaves the claim as a candidate and keeps the general UM target open.

The current canonical review `archives/unrelated-machines/state/审查/全局行基数过滤与多外层单态小home双源审查--审查.md` already records the same v4 identity and boundaries: shared B-only fallback, extra exact-threshold UD leaves, k1 greedy branch, k>=2 `1/(16384 k^2)` cap, 19/10 target, and the separation from v1 `1/(4096 k^4)` and later v5 `1/(1024 k)`. It also records that v4 proof, independent reconstruction, and finite exchange audit are separate evidence layers, and that the finite software does not implement the full profile search, Frank–Wolfe, prefix-flow, k1 greedy, or complete job output.

The source's unique contribution is provenance and an explicit warning that it is not the v3 statement: it widens the k=1 quantifier and must not be silently merged with the unpublished v3 `k^4` draft. It contains no proof, algorithm, finite experiment, or new object beyond the v4 candidate statement. Therefore the mathematical content is already integrated in the canonical review, while the source fingerprint and version distinction should be preserved.

## Recommended disposition

Recommend `integrated` into the existing v4/v5 review, with the source retained as a statement-only historical input. It should not be promoted to a theorem or algorithm object and should not be treated as independent proof. After write access returns, submit a receipt with `full_file_reviewed=true`, `related_material_checked=true`, `unique_content_accounted_for=true`, disposition `integrated`, and target `archives/unrelated-machines/state/审查/全局行基数过滤与多外层单态小home双源审查--审查.md`.

This is a provisional local review only: no claim, done, or push was performed because the authenticated receive-pack is currently blocked.
