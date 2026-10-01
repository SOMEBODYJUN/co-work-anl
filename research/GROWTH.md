# 新研究如何进入仓库

这个仓库不是一次性归档。新结果从问题到主张有固定去处；每条现行命题都必须能沿着**前提 → 推导 → 算法 → 证据 → 限制**走通。目录名表示其在研究中的角色，不沿用提交者、模型代号或某个 ZIP 的文件夹名。

| 新内容 | 放置位置 | 成为现行命题之前的要求 |
| --- | --- | --- |
| 尚未解决的问题、反例搜索、待审证明 | research/questions/，一题一页 | 明确要证或要否定的量词和已知边界 |
| 可接受审查的数学陈述及证明 | research/current/对应分支/ | 使用[命题模板](templates/claim.md)，写出完整前提、依赖与核心推导，链接原始来源 |
| 可运行构造或精确求解 | facility_spe/按 shared、heterogeneous、local、exact 分层 | 写清输入限制、结果语义、位复杂度与失败行为；保证只有一份规范实现 |
| 实际输入、可核验输出、实验 | examples/、evidence/certificates/、evidence/runs/ | 输入与证书分开；报告注明种子、规模、版本和未检验之处；运行默认不覆盖冻结记录 |
| 回归与独立交叉核对 | tests/，探索性审查置于 tests/audits/ | 至少检查关键假设边界与输出声称；独立 oracle 不得调用被测的同一个求解核心 |
| 外来草稿、过时推导、旧源码快照 | history/source/ 或 history/proofs/ | 标记原始状态及被哪一份现行内容取代；不以历史稿作为当前命题的唯一入口 |

## 从新问题到可采用算法的流程

1. 在 research/questions/ 记录问题：实例类、客户均衡概念、量词、已知上/下界与可能反例。未知问题保持“开放”；不要在当前命题里暗示它已被解决。
2. 按[模板](templates/claim.md)在 research/current/相应分支写新稿。首先定义输入类型与所有同时成立的假设，再分别写定理、关键引理、证明链和未消除的义务。直接引用历史文段不构成新稿。
3. 若有程序，在 facility_spe/ 放唯一实现，在 tests/ 放能验证独立性质的检查。证书的验证范围应与普遍证明、最优性证明分别说明。
4. 更新 research/current/claims.md 中的编号、状态和逻辑依赖；在 research/assets.json 添加现行稿、可追溯源、实现、测试、冻结结果；在 research/graph.json 添加数学节点及带**全部共同前提**的超边。若导入原始文件，逐个登记到 research/source_crosswalk.json 并运行 research/build_crosswalk.py。有限测试用 checks 边，反例用 attacks 边，不能画成 derives。
5. 运行 python3 research/build_map.py、python3 research/build_map.py --check、python3 research/build_crosswalk.py --check、python3 research/check_assets.py 和有关回归，再更新入口 README 与 USAGE。状态升级需要重读证明和记录消除的反驳；通过测试本身不升级定理状态。

## 命题与版本约定

同一 ID 的适用类、延续选择量词和成本规则不因一次编辑而悄悄扩大。扩大或缩小范围要新建版本，说明旧版本是否仍成立。数学主张、软件实现、审查意见分别保留自己的状态。外部发表、独立复证、内部证明和有限数值运行不得合称“已证实”。当原稿与现行稿冲突，先在新稿标注冲突并开问题条目，再决定修订命题或证明。

每个分支 README 应回答：什么被证明、条件是什么、怎么运行、哪一步尚待复核、下一篇工作接在哪里。新分支直接创建 research/current/新主题/ 与对应的 claim ID；无需塞进现有两条主线。若后续问题跨出这个双设施模型，程序也新建并列的规范包；facility_spe 只管理此模型，不能变成容纳所有未来代码的杂物目录。
