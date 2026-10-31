# Provisional source review (not claimed)

- Source ID: `7f31a7e15c84adcfbdf4`
- Path: `history/source/notes/unrelated_machines/boss11_uniform_cardinality_pair_sparse_support_exact_v1.md`
- SHA-256: `bf45e8b182f2dd69908c9a923ed0f8b41f4341c32f36700007b1f4d87e451535`
- Size: 939 bytes; both frozen source commits point to the same blob.

## Reading and comparison

The note states the first/pair sparse-support law for an explicit cardinality slice. For explicit integers (dge1) and (0le hle d), a deterministic polynomial-in-(d) procedure outputs at most (1+d+\binom d2) actual (h)-subsets and nonnegative rational weights summing to one. The singleton marginals are (h/d), and the distinct-pair marginals are (h(h-1)/(d(d-1))) when (d>1); (d=1) has no pair constraints. The note explicitly requires materializing the subsets and weights, and it does not claim polynomial time in (log d), a higher-moment slice law, a global coupling, a scheduling algorithm, a gap, or a hardness result.

I compared the note with the canonical `UM-UNIFORM-CARDINALITY-PAIR-SPARSE-SUPPORT-v1` entry in the full CLAIMS ledger, the canonical seven-state-star document, and the existing finite-audit object `archives/unrelated-machines/state/计算/七态星全局二次审计与root重放边界--计算.md`. The canonical material preserves the same exact scope and separates this first/pair sparse certificate from the global quadratic, affine-Boolean, and AND-localizer identities. The finite audit only checks listed parameter instances and cannot be used as a universal proof of this abstract construction.

## Provisional disposition

This is a short statement-only predecessor of the canonical source/object, with no independent proof or evidence. If the write endpoint is restored, register it as `duplicate` (or `retained` historical statement if the ledger requires preserving the author’s chronology) targeting the canonical seven-state-star object and keep this SHA in the receipt. Do not create a new mathematical object from this note.

This review was local pre-reading only: **no claim, no done receipt, no push**.
