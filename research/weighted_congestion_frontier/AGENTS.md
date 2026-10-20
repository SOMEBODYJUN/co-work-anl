<!-- Branch-specific user decision, 2026-10-20 -->
**本分支覆盖说明：`research/or-optimization-selection-20261020` 按用户最新决定重新选择运筹学/优化理论题目，入口为 [选题地图](../topic_selection/README.md)，save=`or-optimization-selection`，独立公屏`topics/or-optimization-board`。后文UM-TARGET-v1/main默认指保留的旧研究快照，不是本分支的当前任务。用户明确授权本次独立分支及六路teamwork；探索不设前置审核。旧数学身份及OPEN状态不变。**

# 共享协作工具与独立拥塞资产的工作规则

当前主攻是 UM-TARGET-v1，save=unrelated-machines：一般R∥C_max的统一常数(2−ε)确定性位多项式实际构造。完整目标和操作在[新题BOSS提示词](../unrelated_machines/BOSS_START.md)、[新题手册](../unrelated_machines/RUNBOOK.md)，数学以[本题模型](../current/unrelated_machines/model_and_classical_barriers.md)和[精确账本](../unrelated_machines/CLAIMS.md)为准。本目录名保留历史，不把所有调用tools的对话变成拥塞研究。

本目录tools/work.py是全仓统一入口；新建未绑定clone默认新题，已绑定shared或其他save保持原绑定。新题另用独立clone，不改绑旧题。首次start显式--save unrelated-machines，核对返回的save、research_entry、research_prompt和本人工作区。后续sync/read/send/dm/inbox/ack/visit/checkpoint沿绑定save。完整命令见本题手册与prompts/OPERATIONS.md。

每个Work独立clone、稳定唯一发布编号；同clone复用，内部subagents由boss汇集，按实际义务调用，人数、轮数和时长按需要决定。main保存成果，wcg/board是原异步消息流，不创建研究分支。未完成想法注明不确定性即可交流，不要求先成稿或审查。默认checkpoint包含相应专题与本人桌面，不带他人草稿；全部待推历史受范围和凭据审计。真实冲突保留双方，禁止强推或自动ours/theirs。

本目录MODEL.md、CLAIMS.md、ACCEPTANCE.md、PRO_BRIEF.md及其来源清单只定义/记录独立的旧拥塞研究，不作为新题模型或完成标准。旧冻结Pro材料中的OPEN是其当时快照，旧Cd/ln d命题现已被否定；查旧数学时先从README和现行旧题地图核对状态。底层无save旧事件仍属于shared，勿改历史路由。当前角色提示词已改为新题，旧版在Git历史保留。

新数学结果按根AGENTS/GROWTH维护精确身份、正文、审查、资产和图，重要状态升级须实际证明、独立攻击与异议处理。修改协作工具运行相应tests；交付前运行build_catalog/build_map/build_crosswalk的--check、check_active_research.py、check_assets.py及check_wc_assets.py --check。工程测试与数学真值分别记录；冻结原件和证据不原位改写。
