# 顺序客户吸引：一般目录、任意人数的半覆盖研究入口

当前主目标是 **`Q-CAG-HALF`**，存档为 **`customer-attraction`**：证明任意有限共同主题目录、任意人数、每个完整历史依赖纯 SPE 的覆盖福利至少为最优的一半。目标仍 **OPEN**。这次重新设为主攻没有改变原命题、已有证明或审查等级。

主人当前策略是停止特殊人数的长期调参：固定人数方法只有在形成一般归纳、递推或统一可扩展机制时继续作为主线；否则直接攻一般情况。当前由本对话Boss2主动协调各组的障碍、交流与转向，集中线程为 `owner-general-strategy-2026-10-21`；详见[执行与协调入口](RESEARCH_STATE.md#主人当前策略与协调)。不设开工审批或路线配额。

Boss 带自己的团队直接研究，可以自由换方法、交流半成形想法、尝试证明和反例；没有路线名额、前置登记或等待审核。清洗者检查并整理可复用成果入库；整理者判断独立成稿边界、突出真实贡献并准备论文。成熟结果的审查和数学状态提升按实际证据处理。

## 最短读取路径

1. [模型](../current/customer_attraction/model.md)：单位客户、共同目录、均分收益、全部历史上的纯 SPE。
2. [精确目标](CLAIMS.md)与[当前前沿](RESEARCH_STATE.md)：一般问题未解决，哪些子类已经完成。
3. [失败机制](FAILED_ROUTES.md)：避免把已否定的局部税、逐人保底或静态均衡桥重新当定理。
4. 围绕当前想法按需打开[数学资产地图](../current/customer_attraction/README.md)中的正文、审查、代码和证据，随后直接研究。

无需先通读其他模型、全部历史、整个工具源码或所有失败材料。已有路线只是工具，不是方法清单。

## 核心对象与准确边界

有限客户集为 \(N\)，有限非空共同目录为 \(\mathcal S\subseteq2^N\)，\(m\ge1\) 名单位权提供者按固定顺序各选一次主题，观察全部有序历史。客户价值为一，在最终覆盖自己的提供者之间均分。终局 \(s=(S_1,\ldots,S_m)\) 满足

\[
c_x(s)=|\{i:x\in S_i\}|,\qquad
u_i(s)=\sum_{x\in S_i}\frac1{c_x(s)},\qquad
W(s)=\left|\bigcup_iS_i\right|=\sum_i u_i(s).
\]

最优覆盖 \(\operatorname{OPT}_m\) 是 \(m\) 个目录主题的最大并集大小。目标对**每个**完整历史依赖纯 SPE \(\sigma\) 证明 \(2W(\alpha(\sigma))\ge\operatorname{OPT}_m\)。重复主题选择、空主题、零客户及全部历史依赖平局均保留；客户整数类型重数只编码不同单位客户。异构目录、带权提供者、混合行为 SPE 是其他模型，不能暗中替换。

## 研究与生产入口

| 文件 | 用途与读取时机 |
| --- | --- |
| [BOSS_START](BOSS_START.md) | 唯一研究者提示词；直接带团队攻一般目标 |
| [CLEANER](CLEANER.md) | 检查推导、证据和命题身份，清理重复并完成正确登记 |
| [EDITOR](EDITOR.md) | 判断哪些新增数学可独立成文，组织贡献与稿件 |
| [RUNBOOK](RUNBOOK.md) | 独立 clone、身份、公屏、私聊、本人桌面与 checkpoint 命令 |
| [RESEARCH_STATE](RESEARCH_STATE.md) | 已有地基、真正未解决的承重义务与下一步 |
| [CLAIMS](CLAIMS.md) | `Q-CAG-HALF` 的完整身份及现行 CA 命题账本入口 |
| [FAILED_ROUTES](FAILED_ROUTES.md) | 已击穿机制、回收成果与重试条件 |
| [RETAINED_QUESTIONS](RETAINED_QUESTIONS.md) | 把仍开问题、已完成子题、失败桥和其他模型分开 |
| [数学全文地图](../current/customer_attraction/README.md) | 按对象找自足证明、辅助接口、审查和冻结证据 |

原始出处和导入条件分别见[文献记录](../current/customer_attraction/literature.md)与[目录、量词复核](../current/customer_attraction/literature_followup.md)。[全仓精确账本](../current/claims.md)、[审查状态](../review_status.json)、[资产合同](../assets.json)和[依赖图](../graph.json)继续保留原身份；本目录不另复制一套数学真值。

## 资产去向与入口维护

个人推导、未核验尝试和恢复笔记持续保存在`research/workspaces/customer-attraction/<actor>/`。检查整理后，自足正文进入`research/current/customer_attraction/`，候选进入本题`research/questions/`位置，独立检查进入`research/reviews/customer_attraction/`；规范程序、测试和证据沿现有目录保存。共享资产按数学对象组织，不按角色分区。

每次正式入库，同步[数学全文地图](../current/customer_attraction/README.md)的文件、用途和范围；结论或缺口改变时再同步[当前前沿](RESEARCH_STATE.md)、精确账本及实际受影响的根摘要。私人备份只需维护自己的README。名称、中文用途和更新责任见[生产规则](../REPOSITORY_GUIDE.md)；当前正文漏进数学地图会被现有路由检查拒绝，摘要的数学准确性仍由实际整理者核对。
