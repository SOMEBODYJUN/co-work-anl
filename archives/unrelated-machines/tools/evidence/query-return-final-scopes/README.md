# 查询返回五份终审的精确范围与原件资源

正式pushed/synced认领5f8c95e7db12ca44fbe3f21f8b8416198f512399后，五主源逐份全文重新核读。它们保留B typed/root、C general/root、私有局部root三种数学接口的最终范围；旧comparison不抵本批done。正文为[三接口终审范围](../../../state/审查/查询返回三接口的最终认证范围与历史身份--审查.md)与[原件及有限运行资源](../../../state/资源/查询返回终审的原件链与有限运行资源--资源.md)。成熟完整主证明不重复，终审的全部独有域/核对/先验/状态/原件链有自足内容。

| 证据 | 实际用途 |
| --- | --- |
| [source-manifest.json](source-manifest.json) | 五主源冻结提交/path/size/SHA、实际原件位置及完整阅读。 |
| [comparison-manifest.json](comparison-manifest.json) | 19份完整比较：B四件、C五件、局部五件、两canonical、两C JSON和audit原代码。 |
| [scope-and-sha-chain.json](scope-and-sha-chain.json) | 五条原文SHA链，两个whole canonical与五个章节切片，逐主源formal/context集合。 |
| [comparison-artifacts.json](comparison-artifacts.json) | fa93旧依赖精确快照及既有命令/固定输出/verification三记录的只读指纹。 |
| [quantifier-ledger.json](quantifier-ledger.json) | B、C、给定两actual私有局部交换的完整不同合同/边界与总位成本。 |
| [finite-check-provenance.json](finite-check-provenance.json) | general历史独立5184、root有限记录、此前audit首次复现及本轮无run的不同身份。 |
| [relation-review.json](relation-review.json) | 互补分节认证、参数特化、局部不同输入、原件资源与有限检查关系；阶段二无正式超图。 |
| [verify_delivery.py](verify_delivery.py) / [实际结果](delivery-self-check.json) | 只核交付字节、原文SHA链/切片、历史转录、receipt、链接及exact copy清单；不做数学实验。 |
| [五条receipt](../../../../../cleanup/workspaces/Boss4/r3-query-return-final-scopes/semantic-receipts.json) | 3 retained、2 integrated，每源独有内容和理由，不以root摘要或同wholeSHA代替阅读。 |

3e6ac…8871B的D：B正式共同§1/B§2–3，C正式共同§1/C§4，彼此其它章节为相应reviewer的context。6074c…14658B的P：本局部root正式仅§1，其它§2–5为context。Whole hash只锁实际全文，formal section不是全文件。General C本人先行有限枚举有原JSON，但明确未读/运行root audit代码与输出，当前清洗自己读过不回填历史。

[原程序计算对象](../../../state/计算/双见证查询染色与固定矩阵证书的原程序核验--计算.md)已有audit-only的完整程序/运行解释。两个C原JSON、原audit代码、已存命令和输出在manifest中逐件指向现有原字节；本包未重跑5184、保存见证回算或任何原入口。局部实际旧依赖是[fa93快照](../query-count-v3-history/two_witness_query_separation_count_v3_canonical.md)，仅需旧single-query/不交支持/zero/位域，不借新计数或费用。

## 完整性复核与保存依赖顺序

`ROOT`为本staging根、`REPO`为已有原件的仓库根；合入后两者均可指仓库。前批半权C两正文是本页准确证明去向，Boss应先保存其28文件再保存本批。若C尚待串行拷入，预检可额外只读已冻结的C staging，不复制/覆盖其正文：

```bash
python ROOT/archives/unrelated-machines/tools/evidence/query-return-final-scopes/verify_delivery.py --root ROOT --fallback-root REPO --dependency-root C_STAGE --output ROOT/archives/unrelated-machines/tools/evidence/query-return-final-scopes/delivery-self-check.json
```

C已拷入后省略`--dependency-root C_STAGE`即可。报告逐链接记录实际解析根，暂存依赖不伪称已pushed。命令只写指定完整性JSON，不Git/claim/done、不认证数学、不执行SAT搜索或调度算法。本轮数学run0、blind0，原独立字节不改，外审/新颖性和UM目标仍未关闭。
