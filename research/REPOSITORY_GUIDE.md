# 仓库生产、读取与保存规则

当前主攻 **Q-CAG-HALF**，存档 **customer-attraction**。数学入口是[本题短地图](customer_attraction/README.md)，协作命令集中在[RUNBOOK](customer_attraction/RUNBOOK.md)，统一程序为根[work.py](../work.py)。

## 读取与角色

先保留本地工作、安全同步main，读根四入口和本题模型，再按当前数学义务选正文、实际审查及证据。Boss不必通读工具源码、全部历史或每份登记JSON。三个角色只有[Boss](customer_attraction/BOSS_START.md)、[清洗者](customer_attraction/CLEANER.md)、[整理者](customer_attraction/EDITOR.md)，研究探索不等待审核或写作批准。

## 真实数学如何保存

| 内容 | 位置与合同 |
| --- | --- |
| 精确目标与当前义务 | 本题README/CLAIMS/RESEARCH_STATE/FAILED_ROUTES；完整CA身份仍在current/claims与review_status |
| 自足证明、反例和工具 | research/current/customer_attraction/，明确所有假设、量词、推导与边界 |
| 可接续候选 | research/questions/customer_attraction/，准确标级，不为通过检查而升级 |
| 已发生的独立检查 | research/reviews/customer_attraction/，记录版本及真正覆盖 |
| 规范实现与验证 | customer_attraction/、tests/、examples/和evidence/；有限验证不替代一般证明 |
| 个人研究与恢复备份 | research/workspaces/customer-attraction/<actor>/；未完成、未核验和错误尝试也可提交，整理后再入共享资产 |
| 过期指挥文本与原始来源 | history/，保留来源位置和hash；重复无增量输出不入库 |

个人目录每有一段新工作、换路线或中断前及时checkpoint，不以数学入库标准阻止备份；README记录当前问题、材料和下一步。共享资产正式入库时：整理正文及证据 → 明确实际身份/状态/依赖 → 对应核验 → checkpoint普通提交推送。共享目录不按角色分区，保存不自动提升数学状态。只有status=pushed才报告远端保存。

## 文件怎么命名，README谁来更新

个人区内部命名自由，自己的README负责恢复线索。共享文件使用能辨认数学对象与用途的名字，例如`three_player_sharp.md`、`prefix_balance_counterexample.md`；首标题和catalog同时给出中文数学名称、适用范围和读取用途。新文件不用日期、actor、`proof2.md`或`result_final.md`充当名称；已有稳定路径不为美观反复改名。

正式入库的人在同一次提交维护相关入口，清洗者负责检查整合是否到位：

| 变化 | 必须同步的入口 |
| --- | --- |
| 个人推导、实验与卡点 | 本人工作区README；不要求改共享地图 |
| 新增、替换、改名或移走共享正文 | research/current/customer_attraction/README.md中的对应数学资产及用途；同步catalog登记和实际引用 |
| 新定理、反例、范围改变或未解决义务变化 | 相应精确Claim及状态；本题RESEARCH_STATE/FAILED_ROUTES中实际受影响的摘要 |
| 一般目标、最好已知范围或主攻方向变化 | 根README/RESEARCH_STATE和本题短入口中实际受影响的结论 |
| 稿件判断或文章结构变化 | 相应稿件入口；研究状态只记录真实数学变化 |

根README是短总览，本题短入口是读取路线，数学README是逐文件地图，catalog是全仓检索登记；不重复复制整套证明。README不是程序自动撰写的数学结论，更新依赖实际入库者。`check_active_research.py`会拒绝当前正文漏出数学地图及失效链接，`build_catalog.py --check`会拒绝名称用途漏登记；这些检查不能判断摘要是否忠实反映新证明。

## 大规模并行与隔离

每个独立Work对话使用独立clone、main和稳定R-UUID；subagents由该boss汇总，不接管别人的身份。公屏用于公开研讨，私聊由显式收件人隔离，桌面按save和actor分开。半成形思路可以直接交流，注明身份；公屏不是成果唯一副本。

新未绑定clone默认customer-attraction。已有shared、unrelated-machines等绑定保持；旧clone不自动改绑。默认checkpoint保存当前存档数学目录、共同登记和本人的桌面；显式paths会替换整个范围，必须列全本次成果，不能用“.”粗放包揽。

推送前安全同步；冲突保留双方后按内容解决，不强推、不自动ours/theirs、不另开研究分支躲冲突。凭据始终在仓库外，完整待推历史也须排除敏感信息。正常研究、核验、入库与普通推送已获授权。

## 整理与成稿

清洗者实质检查并入库；整理者扣除前人贡献后判断独立文章、合理拆合、读者与意义，准确突出优势。README是研究地图，不是证明来源。独有数学不按“旧题”批量删除，过时角色和重复指挥文本退出当前读取链。

新增/移动文件维护catalog中文名、用途和实际链接。修改Claim时再同步精确账本、review_status、assets和graph。按需运行build_catalog、build_map、build_crosswalk、check_active_research、check_assets及对应回归；不改冻结证据原字节去适配新路径。详见[GROWTH](GROWTH.md)及[本次清理记录](customer_attraction/CURATION.md)。
