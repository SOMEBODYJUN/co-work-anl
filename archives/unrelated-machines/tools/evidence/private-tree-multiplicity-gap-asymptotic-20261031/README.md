# 私有树重数配置间隙渐近：清洗证据

本目录记录 Boss8 对四个冻结文本来源的实际导出、全文阅读和相互核对。它们没有程序或有限运行；这里不把文本审查记录升级为新的计算证书。

## 冻结来源

| source id | frozen path | SHA-256 | bytes | disposition |
|---|---|---|---:|---|
| `da61ee9f09bb5f524a2d` | `history/source/notes/unrelated_machines/private_tree_multiplicity_gap_asymptotic_exact_source.md` | `fb1283d4bd3346be0dedae6e19acbef50876d68643fafdccbe537d7051156adf` | 3649 | integrated |
| `5a02bc2ebac9e4e8bd96` | `history/source/notes/unrelated_machines/private_tree_multiplicity_gap_asymptotic_proof_source.md` | `0f3852e0b2326518316769cbd433502e79590f7b6ea0cddfd0515af628412397` | 3586 | integrated |
| `7533a9fd5c970b2f6a00` | `history/source/notes/unrelated_machines/private_tree_multiplicity_gap_asymptotic_independent_cover_source.md` | `4464041c06febb6107f118735098cf996ca315f96cd8eb71dfb3995a73588ed5` | 4942 | integrated |
| `32fa815646550454c657` | `history/source/notes/unrelated_machines/private_tree_multiplicity_gap_asymptotic_read_after_cover_source.md` | `0db5855b688d6f7592fd5618c7f63f196f0174e98e093cbcaec3afb6af0b828e` | 2934 | integrated |

Each source has both frozen legacy and main provenance entries with the same content; the stable theorem object cites both commits and all four paths. The source texts are retained in Git history and were exported locally with `work.py clean show` for this read.

## Reading and comparison record

- The exact statement defines the same class `C_mu` as the bounded-multiplicity tree object and states only `2-1/mu <= G(mu) <= 2-1/(mu+2)`, with a supremum over all finite explicit instances. It does not assert a fixed-`mu` sharp value or a polynomial-in-`log(mu)` generator.
- The proof source independently checks the full `CONFIG(1)` certificate, the actual lower-bound schedule, and the direction of the supremum squeeze and integer limit. The `mu^2+1` jobs are counted as explicit output.
- The independent-cover source was read before the proof source in its own narrative and rechecks the same configuration coverage, makespan lower bound, and `mu/(mu+2) <= mu(2-G(mu)) <= 1` limit direction.
- The read-after source compares the proof against that first reconstruction and records no fatal formula or quantifier issue. It does not add an implementation, external theorem, or new runtime evidence.

No source proves general NP-hardness, a universal approximation lower bound, an exact value of `G(mu)` for fixed `mu`, or a general polynomial-time construction of the schedule. Those boundaries are preserved in the theorem object.
