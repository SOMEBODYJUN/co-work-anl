# Provisional review: Boss11 v3 exact-only

- Source ID: `95c635ea4087e884e26e`
- Frozen path: `history/source/notes/unrelated_machines/boss11_shared_ud_tiny_home_k2_refinement_exact_v3.md`
- Source SHA-256: `cc9d1037da7e86c74226968b890eaad6e646c4179bf16fe789a776818d2b6c39`
- Size: 2124 bytes; commits `68fad804ec5946cb296f77dc5b336308a66abf12` and `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`.

## Reading and comparison

The note is an Exact-only candidate statement for `UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v3`. It defines single-state normalized-flat outer groups, pairwise-disjoint homes with one own-unit helper, arbitrary shared normalized fallback states, optional B-only exact-threshold UD leaves, and the k-dependent home cap `1/4096` for k=1 or `1/(16384 k^2)` for k>=2. It asserts a deterministic total-bit-polynomial Q-only algorithm outputting every ordinary job with makespan at most `19/10 OPT`, while explicitly omitting the proof and keeping the general unrelated-machines target open.

The repository's canonical multi-outer object is `archives/unrelated-machines/state/审查/全局行基数过滤与多外层单态小home双源审查--审查.md`, which records v1 (`1/(4096 k^4)`), v4 (`1/(16384 k^2)` with B-only threshold-UD leaves), and v5 (`1/(1024 k)`) as separate identities. The v4 statement has the same core k>=2 cap, single-state/unique-home/shared-B/extra-UD scope, and 19/10 conclusion, but supplies the later proof, algorithmic mechanism, and evidence. The v3 note is therefore a statement-only predecessor/duplicate of the v4 scope, not a new proof or object. Its k=1 wording and “extends v1” remark are preserved as historical version metadata; they must not be silently rewritten as v4 proof evidence.

## Provisional disposition

When the write endpoint is restored and the source can be formally claimed, register this source as `duplicate` (or `retained` historical statement if the coordinator requires preserving version-specific provenance) with target pointing to the canonical v4 object/review. Do not mark `integrated` as a new theorem, and do not use this note to enlarge v4 to multi-state outers, overlapping homes, non-UD leaves, home extra groups, or general unrelated machines.

This is local pre-reading only. No claim, done receipt, checkpoint push, or remote mutation was performed.
