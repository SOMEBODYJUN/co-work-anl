# 半权直接共居C五份历史来源与版本证据

本包五主源为冻结statement、root作者Proof、general先行独立初稿/final和作者读后。实际pushed/synced认领确认776eb54ad832ed0a91f8b12fd1bfe1b09680ea38后逐份全文读取，五份原件均新保存、size/SHA对inventory。相同结论不抹去两种证明或初稿/final版本身份。

[完整证明](../../../state/证明/半权直接共居的精确三半间隔与双计数--证明.md)自足保固定半权原矩阵、所有公式完整三半构造、任意低于三半actual的双计数/环方向解码、SAT q/u真实同机及两种另外非空下界。[历史审查](../../../state/审查/半权直接共居的陈述先行与排版终稿边界--审查.md)保原有先验/作者后读、真正版本差异、C/B互不代审与有限证据归属。已有全局摘要及原程序完整解释不重复认领，新的关键数学与历史增量均有自足正文。

| 证据 | 内容 |
| --- | --- |
| [source-manifest.json](source-manifest.json) | 五主源原始冻结定位、size/SHA、保存路径与全文阅读。 |
| [comparison-manifest.json](comparison-manifest.json) | 九完整比较源：B Exact、canonical、两方终读/根审查、两个C JSON、原固定audit代码；comparison不抵done。 |
| [initial-final-delta.json](initial-final-delta.json) / [原始diff](independent-v1-to-final.diff) | 原初稿7837B至final8071B，只改一个间隔排版并加冻结说明，差234B；无数学修订，两原字节不改。 |
| [scope-and-sha-chain.json](scope-and-sha-chain.json) | 五条原文SHA链、共同§1/C§4与B§2–3context切片、actual statement-first/后读顺序。 |
| [quantifier-ledger.json](quantifier-ledger.json) | 非空/空、任意完整调度、所有原jobs、严格阈值、参数/重复/计数/位域及不认证外推。 |
| [finite-check-provenance.json](finite-check-provenance.json) | general先行5184、root独立原JSON、既有固定audit首次复现分层；本轮数学run0。 |
| [comparison-artifacts.json](comparison-artifacts.json) | 实际读过的三份既有运行命令/输出/verification指纹；没有运行入口。 |
| [relation-review.json](relation-review.json) | 两种证明、异权特化、版本排版、先验/后读和有限核验分工；阶段二无正式超图。 |
| [完整性checker](verify_delivery.py) / [实际结果](delivery-self-check.json) | 只验来源字节、可逆版本差异、原文hash链/章节、历史转录、receipt与链接，不解SAT或枚举调度。 |
| [五条receipt](../../../../../cleanup/workspaces/Boss4/r3-half-weight-cohabiting-history/semantic-receipts.json) | 每源实际全文、比较、独有内容去向及3 retained/2 integrated。 |

general先见B Exact的原P定义和既有strict/全公式/分支合同陈述，再见root新C消息，独立重证固定半权后先冻初稿/final和枚举JSON。root实读final后才解封作者statement文件/Proof。后续C canonical-final完整读3e6ac…全文，正式仅共同§1和C§4，B§2–3仅context，且明确未读/未运行root audit-only代码或输出。当前清洗读过它们也不回填历史general的先验。

有限资源可在已有证据包直接查阅：[general原JSON](../query-witness-originals/comparisons/direct_cohabiting_sat_sharp_three_halves_independent_enum_v1.json)、[root原JSON](../query-witness-originals/comparisons/direct_cohabiting_sharp_unsat_root_integer_enumeration.json)、[原audit代码](../query-witness-originals/original/audit_query_return_source_fixed_certificates.py)、[原实际命令](../query-witness-originals/runs/original-replay-001/commands.json)、[已存输出](../query-witness-originals/runs/original-replay-001/fixed-certificates-audit.json)、[既有verification](../query-witness-originals/runs/original-replay-001/verification.json)。代码对C固定8机10job例枚举5184，其take/continue是另一26机30job达界证书，不是C或两个strict见证。完整解释见[原程序计算对象](../../../state/计算/双见证查询染色与固定矩阵证书的原程序核验--计算.md)。本包不重跑任何入口，不把有限check当全公式证明或生产实现。

## 完整性复核

`ROOT`为本staging根，`REPO`为已保存依赖原件的仓库根；拷入后可两者都指仓库。只输出指定完整性报告，无Git/认领/done操作。

```bash
python ROOT/archives/unrelated-machines/tools/evidence/half-weight-cohabiting-history/verify_delivery.py --root ROOT --fallback-root REPO --output ROOT/archives/unrelated-machines/tools/evidence/half-weight-cohabiting-history/delivery-self-check.json
```

这不是新的数学run、blind审查、枚举、source decoder生产实现或一般UM求解。实际数学判断写在正文，checker只防交付遗漏和版本转录错误。
