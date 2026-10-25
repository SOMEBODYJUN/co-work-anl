# 下一轮恢复入口：顺序客户吸引半覆盖

目标 **Q-CAG-HALF**，存档 **customer-attraction**，状态 **OPEN**。本页只负责选择输入；长证明、来源库存和协作历史均按需读。

## 必读与停止扩读的位置

已读根四入口和适用 [AGENTS](../../AGENTS.md) 后，只读：

1. [模型](../current/customer_attraction/model.md)：对象、完整有序历史、任意平局和零客户。
2. [当前前沿](RESEARCH_STATE.md)：已证范围、三条可用关系和剩余义务。
3. [失败机制](FAILED_ROUTES.md)：定位拟用机制；有匹配项时再读原反例。

到这里应能准确复述问题、已知边界和一个未解义务。随后选一项义务，沿其来源读实际正文与审查；无需读完全部actor、库存或一般工作稿才能开工。[精确目标](CLAIMS.md)供逐量词引用，[完整数学地图](../current/customer_attraction/README.md)供按对象查全文。

## 按需要打开

| 目的 | 入口 |
| --- | --- |
| 连续推导及明确断点 | [一般证明工作稿](../current/customer_attraction/general_half_proof.md)，按章节取用 |
| 查同机制来源、范围和既有审查 | [成果总账](RESULTS_LEDGER.md)、[衔接说明](SYNTHESIS.md) |
| 恢复个人原稿、代码或旧尝试 | [个人区库存](WORKSPACE_RESULTS.md)；库存是带截止版本的恢复工具 |
| 引用、提升或质疑具体Claim | [精确账本](../current/claims.md)、[审查等级](../review_status.json)及原证明/审查 |
| 文献定理导入 | [文献与量词边界](../current/customer_attraction/literature.md) |
| 启动、交流、checkpoint | [RUNBOOK](RUNBOOK.md)，根 work.py 为唯一程序 |
| 角色职责 | [Boss](BOSS_START.md)、[清洗者](CLEANER.md)、[整理者](EDITOR.md) |
| 清理覆盖、未复核范围与历史 | [CURATION](CURATION.md)、[保留问题](RETAINED_QUESTIONS.md) |

每次新增材料应替换受影响的现行摘要，不再向入口追加整轮叙事。只在实际义务需要时增加读取；路径和文件数不等于数学价值。
