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
| 个人可复用草稿 | research/workspaces/customer-attraction/<actor>/；成熟内容按数学对象入库 |
| 过期指挥文本与原始来源 | history/，保留来源位置和hash；重复无增量输出不入库 |

每个有价值阶段：自足正文及真实证据 → 精确身份/状态/相关文件和依赖 → 对应核验 → work.py checkpoint普通提交推送。保存候选不自动提升状态。只有status=pushed才报告远端保存。生成目录只维护文件身份，不制造数学结论。

## 大规模并行与隔离

每个独立Work对话使用独立clone、main和稳定R-UUID；subagents由该boss汇总，不接管别人的身份。公屏用于公开研讨，私聊由显式收件人隔离，桌面按save和actor分开。半成形思路可以直接交流，注明身份；公屏不是成果唯一副本。

新未绑定clone默认customer-attraction。已有shared、unrelated-machines等绑定保持；旧clone不自动改绑。默认checkpoint保存当前存档数学目录、共同登记和本人的桌面；显式paths会替换整个范围，必须列全本次成果，不能用“.”粗放包揽。

推送前安全同步；冲突保留双方后按内容解决，不强推、不自动ours/theirs、不另开研究分支躲冲突。凭据始终在仓库外，完整待推历史也须排除敏感信息。正常研究、核验、入库与普通推送已获授权。

## 整理与成稿

清洗者实质检查并入库；整理者扣除前人贡献后判断独立文章、合理拆合、读者与意义，准确突出优势。README是研究地图，不是证明来源。独有数学不按“旧题”批量删除，过时角色和重复指挥文本退出当前读取链。

新增/移动文件维护catalog中文名、用途和实际链接。修改Claim时再同步精确账本、review_status、assets和graph。按需运行build_catalog、build_map、build_crosswalk、check_active_research、check_assets及对应回归；不改冻结证据原字节去适配新路径。详见[GROWTH](GROWTH.md)及[本次清理记录](customer_attraction/CURATION.md)。
