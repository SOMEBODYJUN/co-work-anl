# Provisional review: Boss11 shared-UD tiny-home proof v3

## Source fingerprint and scope

- Source ID: `008523f50a31a6025502`
- Frozen path: `history/source/notes/unrelated_machines/boss11_shared_ud_tiny_home_k2_refinement_proof_v3.md`
- SHA-256: `ba7556c84d8ce5759c66fd840448085e94c435a94723573d76d73f9f5530b877`
- Size: 3235 bytes
- Both frozen commits point to the same source content.

The note is a proof-side revision for the v3 exact statement `UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v3`. It replaces the older (k^4) tiny-home bound by the (1/(16384k^2)) bound for (k\ge2), keeps a separate (k=1) branch, and derives the curvature estimate (1)–(3) using `theta=1/32`, `c=5/16`, `xi=1/(2^20 H^2)`, `tau=1/(2048H)`, and the `19/10` final guarantee. It explicitly says that the result is a restricted typed domain and does not solve general unrelated machines.

## Comparison with canonical material

The existing canonical review `archives/unrelated-machines/state/审查/全局行基数过滤与多外层单态小home双源审查--审查.md` already records the later v4 and v5 objects, including their exact scopes, algorithms, and evidence boundaries. In that comparison:

1. v3's (k\ge2) cap and 19/10 conclusion are the same domain core later recorded for v4, with the extra B-only threshold-UD leaves and single-state/unique-home/shared-B conditions.
2. v3's proof note is an intermediate algebraic derivation. The v4 canonical source contains the later proof/algorithm and finite audit; v3 adds no independent source object or general-UM theorem.
3. The (k=1) wording and the claim that the old (k^4) domain is contained in the new domain are historical version metadata. They must not be silently treated as v4 proof evidence.
4. The note's finite Fraction checks only the displayed constants and do not constitute an end-to-end implementation, external review, or novelty certification.

## Recommended disposition

Provisional recommendation: `duplicate` or `integrated` into the canonical v4 review, with a version-history pointer to this proof-side derivation. It should not create a new theorem file. When the authenticated write endpoint is restored, formally register the source with `duplicate` targeting `archives/unrelated-machines/state/审查/全局行基数过滤与多外层单态小home双源审查--审查.md`; preserve this source fingerprint and the distinction between v3's intermediate proof and v4's later canonical evidence.

This is a local pre-read only: **not claimed, not done, and not pushed**.
