---
id: mathlab-prompts-role-contracts
kind: resource
type_tag: upstream-prompt-implementation
title: MathLab 提示角色合同与黑板摘要边界
status: retained
summary: 实读 MathLab prompts.py，保存基础研究规范、八种角色合同、黑板摘要截断和 prompt 组装接口，并标明这些上游 API 未部署到当前 Boss3 清洗分支。
source_refs:
  - source:f413aad10283f4e6337a:research/weighted_congestion_frontier/upstream/mathlab/src/mathlab/prompts.py
  - source:local:archives/unrelated-machines/state/资源/MathLab黑板架构与证据状态阶梯--资源.md
  - source:local:tools/README.md
---

# MathLab 提示角色合同与黑板摘要边界

## 来源身份

Claim `f413aad10283f4e6337a` 对应上游 `research/weighted_congestion_frontier/upstream/mathlab/src/mathlab/prompts.py`，冻结 blob 为 `b99b90dc5b57d652ecc85fe81916907183032102`，SHA-256 为 `74cee56c656a37ad1fe273aedf9ad7676ffbff52374a0a1674000f31fbaf771a`，大小 6117 B。完整原文保存在 [prompts.py evidence](../../tools/evidence/mathlab-prompts-20261031/original/prompts.py)，逐段比较记录在 [comparison-notes.md](../../tools/evidence/mathlab-prompts-20261031/comparisons/comparison-notes.md)。

该文件是提示和调度实现资源，不是数学命题。处置为 `retained`：其角色合同和摘要边界对研究工程有可复用的审查启发，但上游 API、状态词和 prompt 组装逻辑没有在本结果分支部署。

## BASE 研究合同

`BASE` 明确要求把 genuine research progress 与 persuasive prose 区分，分别标注 proof、computation、conjecture、heuristic 和 failure。它要求使用本地 shell 做 exact computation、实验、符号代数和文件工作；有用脚本/结果存入工作区并只发布 durable findings；禁止有限计算升级定理；优先尽早证伪吸引人的错误主张；重要证明以 `PROVISIONAL_PROOF` 发布供新鲜 verifier 攻击；反例以 `REFUTED` 和显式 evidence 发布；能力不足时用 `request_capability`；通过消息和 promoted blackboard artifacts 协作；用 `log_progress` 保持简洁实质进度。

这些规范与当前第二阶段的“实读定义域、量词、假设、证据与缺口；保留开放问题；正文先 checkpoint 再 done”在原则上相容。它们只是工程合同，不能替代本题的 stable ID、source hash、正式正文或数学判断。

## 八种角色合同

- **cartographer**：从 handoff 提取目标、定义、已知结果、猜想、死路、计算证据和瓶颈，生成保守 claim/task，不在此轮试图解完整题。
- **director**：查看黑板、开放任务、失败和近期发现，跨不同研究岛分配高信息量任务，保留方法多样性，避免重复。
- **researcher**：深入处理指定问题，可证明、重述、计算、找反例或指出障碍，产出可复用数学资产。
- **experimentalist**：把模糊结构转成精确数据，优先 exact arithmetic、归一化、分解、插值和小反例，并明确证据边界。
- **falsifier**：攻击隐藏假设、边界情况、统一性、分母、极限交换、非消失和渐近；精确障碍或反例是成功结果。
- **verifier**：独立思考后逐行审计证明，只在完整时 ACCEPT；分类 ACCEPT/FIXABLE/REJECT/UNCERTAIN；拒绝证明不等于证明命题为假。
- **synthesizer**：比较研究岛进展，迁移有用想法，保留冲突与死路，不强制共识。
- **framework_engineer**：实现最小 project-local capability，优先 `.mathlab/extensions` 热加载脚本和 manifest；运行验收测试后才能标 FULFILLED，核心框架修改默认禁止。

当前 Boss3 的清洗角色由阶段提示词和 `clean` 操作绑定，不能把上述角色名当作本会话的新身份或审批层级。

## 黑板摘要函数的精确边界

`blackboard_digest(claims, tasks, features)` 只保留 claims 前 60 项、tasks 前 40 项、features 前 20 项，并从每项选择固定字段后生成 JSON 文本；它不递归读取全部黑板，也没有数学验证。`build_instructions` 再把 BASE、角色、agent、island、project root、handoff 和 digest 拼接成一份 prompt。

因此摘要是上下文压缩，而不是完整状态证明。旧 claim/task 可能因顺序和截断不在摘要里；字段缺失也不会自动暴露。当前清洗保全必须继续依赖 `clean list --full`、`clean show`、实际正文/evidence 和已推送 receipt，不能以一次 prompt digest 代替全仓来源完成。

## 与 MathLab ARCHITECTURE 对象的关系

本对象与 `MathLab黑板架构与证据状态阶梯--资源.md` 属于同一上游选集但作用不同：ARCHITECTURE 说明系统级 handoff/blackboard/islands/Verifier/RA 数据流；本对象说明 Python prompt 合同、角色文本、摘要截断和指令拼装。两者相互引用但不合并为单一部署事实。

本对象没有验证 MathLab 的实际运行、SQLite 持久化、Verifier 管线、extension manifest 加载或任何外部优先权。若未来要采用其中一项机制，须在本仓库另写接入设计、测试和权限边界；其上游状态词不能直接改变当前数学对象的 `候选/条件结论/有限实验/障碍` 分类。
