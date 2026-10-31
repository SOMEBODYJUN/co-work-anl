# Provisional review: UM-UNIFORM-CARDINALITY-PAIR-SPARSE-SUPPORT-v1 proof note

This is a local pre-read only. It is not a formal claim, completion receipt, or remote delivery because the authenticated write endpoint is blocked.

## Source identity

- Source id: `61cb238f913688d42791`
- Path: `history/source/notes/unrelated_machines/boss11_uniform_cardinality_pair_sparse_support_proof_v1.md`
- SHA-256: `f3d759b4a0e147ab215f2aa1c09f72aca5aeda687426a3adac3ce2643fc28274`
- Size: 2728 bytes
- Frozen commits: `68fad804ec5946cb296f77dc5b336308a66abf12`, `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`

## What the note actually contains

The note is a proof sketch for the explicit sparse support claim. For each `d>=1` and `0<=h<=d`, it uses the feature vector

`v(A)=(1, (1_r(A))_r, (1_r(A)1_s(A))_{r<s})`

of dimension `D_d=1+d+binom(d,2)`. It recursively splits `[d]` into blocks of sizes `a=floor(d/2)` and `b=d-a`, recursively builds sparse supports for all feasible block cardinalities, forms unions, and deduplicates. The candidate count is bounded by `(d+1)D_aD_b=O(d^5)`, while a basic rational LP returns at most `D_d` positive columns reproducing the uniform `h`-subset first and pair marginals. The proof uses the hypergeometric mixture over block cardinalities as an existence witness and then invokes standard rational LP/basic-solution compression; it does not enumerate all `h`-subsets.

The note also states polynomial bit-length control for the rational basic solution, caching all block/cardinality states, and a `d=1`, `h=0`, `h=d` base-case treatment. Its seven-state application replaces each of six uniform-cardinality classes by this first/pair-equivalent support, preserving row first/pair and row load. It explicitly does not preserve third or higher moments, does not replace the common law `L`, and does not claim a general scheduling gap, hardness result, or software implementation.

## Cross-repository comparison

The exact same identity is already recorded in the frozen claim ledger as `UM-UNIFORM-CARDINALITY-PAIR-SPARSE-SUPPORT-v1` (ledger lines 3401 onward) and appears as a dependency of `UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-LOCAL-v2`. The canonical seven-state review and finite audit separate this local first/pair law from the full degree-six/global quadratic law, affine Boolean-owner boundary, and faithful-AND obstruction. The existing canonical objects also state the same critical boundaries: explicit `d`-label time is polynomial in `d` rather than in `log d`; `d=1` has no pair features; the sparse law preserves only first/pair; it is not a common-law replacement, a generic CONFIG solver, a near-two gap, or hardness proof.

No independent mathematical object is added by this statement-only proof note. It is best treated as a historical proof-version source feeding the existing canonical claim, with a future formal disposition of `duplicate` or `integrated` depending on whether the ledger requires a separate proof-source receipt. The local exact note does not provide an executable implementation or an external novelty check.

## Required future action

When the write endpoint is available, Boss6 should formally claim this source (if still available), register the full-read fields, and use disposition `duplicate` or `integrated` with target `archives/unrelated-machines/state/定理/` canonical seven-state object. Until then this directory is only a provisional local record.
