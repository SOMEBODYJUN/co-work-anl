---
source_id: 937c51bf5dad30fcbdd2
source_path: history/source/notes/unrelated_machines/arbitrary_nonpool_committer_two_mode_false_escape_statement_only_v1.md
source_sha256: 4def1be309c85a6c2eec117ab892a70aef94cf6f6b9f83bff64e574368c1dc54
status: provisional-unclaimed
---

# Provisional source review (not a claim or completion)

I read the complete 5,585-byte statement-only source. It explicitly says that the proof is not included and that the note is scratch material. Its identity is `UM-ARBITRARY-NONPOOL-COMMITTER-TWO-MODE-FALSE-ESCAPE-v1`.

## Mathematical content

The source fixes an explicit ring/backbone unrelated-machines matrix with `r>=2`, even `k>=2`, `1/2<rho<1`, two unit selector pools per variable, and auxiliary jobs `J`. It gives two versions of a conditional statement:

* With two complete strict assignments supplied as input (one true variable in each assignment), if every `J` finite endpoint is on arbitrary nonpool machines (`I`, `M`, or `C`), a deterministic bit-polynomial interpolation assigns every selector to the false pool, keeps each nonpool load at most `3/2`, and keeps pool loads at most `3/2` (positive) or `1` (negative), while every non-selector job uses one of its two witness endpoints.
* If `J` may also use pools, the same construction gives `C_max <= 3/2+d/2`, where `d` is the largest *used* non-selector time on the two special positive pools. The note derives the strict/non-strict threshold distinction for `beta=2-delta` and the necessary used near-unit pool job when `1/k < 1-2delta`.

The source preserves zero endpoints, unused finite endpoints, arbitrary nonpool cohabitation and task identity. It explicitly does not claim to find the two witnesses, does not claim a source decoder, and does not claim a general UM approximation or hardness theorem.

## Full-repository comparison

The statement is already covered by the canonical object `UM-TWO-ACTUAL-INTERPOLATION-BULK-FALSE-ESCAPE-v4` in `archives/unrelated-machines/state/审查/双见证批量插值与成束耦合细分边界双源审查--审查.md` and by the corresponding canonical source `research/current/unrelated_machines/bulk_or_commit_two_witness_interpolation.md` recorded there. That canonical review explicitly includes all nonpool `M`, positive/negative `C`, and ring machines, and records the same general `(N_i,d_i,t_i)` interpolation inequality, the nonpool `3/2` specialization, the pool `3/2+d/2` bound, and the used near-unit identity obligation. The claims ledger records the same identities under `UM-UNRELATED-AUX-HEAVY-READOUT-BULK-OR-COMMIT-SPLIT-v3` and `UM-TWO-ACTUAL-INTERPOLATION-BULK-FALSE-ESCAPE-v4`.

The source contributes no proof, algorithm listing, evidence artifact, or scope correction beyond the canonical review. Its only editorial value is an earlier statement-only formulation that makes the arbitrary-nonpool qualification explicit. No new mathematical object should be created from it.

## Provisional disposition

Recommended eventual disposition: `duplicate`, with target/reference to the canonical v4 object and review above. This is **not** a formal `clean done`: no claim was made because authenticated writes are blocked, and the source remains unclaimed. If the write endpoint is restored, claim it formally, recheck the frozen SHA, then record the duplicate receipt with the canonical v4 target and this comparison note.
