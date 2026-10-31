# Cheng–Mao 2019 阅读日志

- source id: `af25c26da297903a6019`
- source path: `history/source/literature/unrelated_machines/cheng_mao_2019_restricted_max_min_allocation_v1.pdf`
- frozen commits: `68fad804ec5946cb296f77dc5b336308a66abf12`, `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`
- source SHA256: `ea99b29b0b05694d16fcf18b63fddcd9dc798aa6ef476ac0b78033c8eaf90e7a`
- fetched bytes: 768864; pypdf reports 28 pages (the `file` utility's page count is unreliable for this PDF)
- full_file_reviewed: true
- related_material_checked: true
- unique_content_accounted_for: true
- proposed disposition: `retained` or `integrated`
- proposed targets: `archives/unrelated-machines/state/文献/Cheng-Mao受限最大最小分配与配置LP--文献.md`; existing `archives/unrelated-machines/state/定理/逐资源正权畸变与κ边界--定理.md` and its review already use Theorem 1 as an external backend contract.

## Reading scope

Read abstract/introduction; restricted model; configuration LP and dual; fat/thin edge definitions; partial allocation and alternating paths; Section 3 Build/Collapse, layer-level node-disjoint paths, limited blocking and lazy/greedy parameters; Section 4 invariants, geometric growth and Lemmas 14–18; Appendix A node-disjoint path lemmas; Appendix B omitted invariant proofs; Appendix C local-search integrality-gap analysis with the piecewise dual prices, Claims 30–32 and termination signature.

## Comparison and unique content

The paper's unique content is the explicit `(4+δ)` algorithm contract, its finite parameterized Build/Collapse mechanism and (n^{poly(1/δ)}) running-time argument, plus the separate `99/26` integrality-gap certificate with nonuniform thin-resource dual prices. Existing resource-distortion theorem imports only the first theorem as an external restricted-Santa backend and deliberately does not claim a repository implementation; this source review preserves the paper's own object identity and the second theorem instead of collapsing it into a general unrelated-machines or six-player SPE claim.
