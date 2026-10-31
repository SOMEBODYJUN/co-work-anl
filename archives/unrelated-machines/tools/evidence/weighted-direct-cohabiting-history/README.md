# 异权直接共居与两份canonical限定认证的原始证据

本包处理五个正式主源：fb794955429597b2945d的共享四环/pool最终scope，及f94da770c9ad10f0642e、7f8060462a608a576777、0aeec153b2fb633b1126、220c9dc4a72fb7eb45de的异权B Exact/作者Proof/独立Exact-only/作者读后。认领pushed确认1c077c0373ad382868c055a58357ba873eaebc47后，逐主源全文读取并核inventory原字节。旧同SHA原件读作依赖，不替本次五个主源的语义处置。

[完整证明](../../../state/证明/直接共居的严格身份与异权三半共同调度--证明.md)自足给新B原矩阵、严格SAT双向身份、作者E/R与typed槽饱和两证明、作者全图与typed缩减图、一个共同整数matching、恢复全部原jobs及真实异权负载。[历史与跨稿范围](../../../state/审查/直接共居异权合同的独立证据与跨稿范围--审查.md)保typed先独立冻结、作者matching策略简述后到、再读Proof的实际顺序，且单列另一6074 canonical的共享外端§4–5最终认证。两份whole hash的不同章节认证没有合并。

| 文件 | 用途 |
| --- | --- |
| [source-manifest.json](source-manifest.json) | 五主源size/SHA/冻结来源/原件位置。新存四份B原件，fb原件复用已保存同SHA原件。 |
| [comparison-manifest.json](comparison-manifest.json) | 15份完整读过的相关原件：两canonical、B终读/根审查、C根审查与两个C有限JSON、四环/pool八历史；比较不自动done。 |
| [scope-and-sha-chain.json](scope-and-sha-chain.json) | 不同canonical whole与章节切片、fb八SHA链、B读后/终读/根审查三条链及历史顺序。 |
| [quantifier-ledger.json](quantifier-ledger.json) | 正异权、环/重复occurrence、dummy/空公式、strict合同和全公式输出的不同量词、计数与排除端点。 |
| [finite-check-provenance.json](finite-check-provenance.json) | B无source run；C固定5184双JSON、四环样本与pool4328的真正历史归属，本轮不重跑。 |
| [relation-review.json](relation-review.json) | 与旧摘要、两证明表示、旧D/h与真实R、半权C及6074共享外端的关系检查；阶段二未写正式超图。 |
| [verify_delivery.py](verify_delivery.py) | 只验来源字节、原文SHA链、章节切片、receipt及链接，不执行数学枚举或matching。 |
| [delivery-self-check.json](delivery-self-check.json) | 本次完整性检查的实际输出。 |
| [五条语义receipt](../../../../../cleanup/workspaces/Boss4/r3-weighted-direct-cohabiting/semantic-receipts.json) | 逐源实际阅读、比较、独有内容与处置，不用程序判定数学。 |

`3e6ac…`为8871字节direct-cohabiting全文：typed及root B正式共同§1、B§2–3，固定半权C§4仅typed上下文，root C另有最终限定认证。`6074c…`为14658字节private-clause/shared-outside全文：fb正式只四环§4及pool§5，§1–3仅上下文。四环已有完整全谱、pool已有全部pattern及实际σ证明，本包不复制其全文；新审查仍自足保留最终记录所核矩阵、严格阈值/等号、量词与证据归属。

B不把strictSAT改写成异权非空OPT1或sharp，也不把固定半权的5184枚举用作B证明。历史两个C JSON在原query-witness证据中保持字节；固定证书代码audit_only。B及fb本次无数学run、无软件实现；有限报告不是一般证明。当前清洗是read-after，未新增blind审查，没有改原独立记录。

## 可复核命令

合入前从任意目录执行，`ROOT`指本包staging根，`REPO`指已有依赖原件根；合入后两者都指仓库根。参数只读原件，输出写指定自查JSON。

```bash
python ROOT/archives/unrelated-machines/tools/evidence/weighted-direct-cohabiting-history/verify_delivery.py --root ROOT --fallback-root REPO --output ROOT/archives/unrelated-machines/tools/evidence/weighted-direct-cohabiting-history/delivery-self-check.json
```

该命令不认领、不done、不Git、不访问凭据、不求解SAT或UM、不重演C5184/pool4328。完整数学审读及关系判断已写入正文；checker仅辅助交付完整性。
