# R-87980b0103884433b5d9a132419b08e8 的个人研究工作区

研究存档：`unrelated-machines`；发布身份：`R-87980b0103884433b5d9a132419b08e8`。

## 当前精确问题

继续研究 `UM-TARGET-v1`：对一般不相关并行机 makespan，寻找统一 ε>0 和确定性输入位长多项式算法，输出实际分配并满足 `C_max ≤ (2−ε)OPT`。零值、空任务、不可用边和非均匀有理时间属于模型；当前主目标仍 OPEN。

## 本轮采用的前沿

已同步至 main `485589c`。已读固定向量/HS 矩提取的无界反例、共同匹配接口的全窗口困难性、加权共同组联合槽及其审查。当前承重缺口是：一般有环核心中，允许接收机增载并可重开旧选择的共同容量机制；任何候选都必须同时给出可构造性、全机器负载界和总位复杂度。

本轮内部攻击两条路线：

- rank`(M2)−rank(M1)=1` 的未冻结共同交换投影候选；先要求精确定义和支持选择算法，不把公屏摘要当 Claim。
- 将共同组加权出口/槽流推广到异资格或异端耗时；先检验任务身份与实际出口成本是否会破坏 token 计费。

本轮已形成可复用的范围边界：给定 `T` 的共同资格/等端私有组可用乘法最小覆盖 FPTAS 和可调阈值 `τ` 得到候选界 `R*=((1+η)(3+δ))/(2+η)<2`；任意资格或异端耗时的标量 token 扩展有四机精确反例。另有 `m` 核心机加一扩展机的 LST 正支撑反例，说明真实 `OPT=T=1` 调度可能依赖分数证书中的零质量边。rank-jump-one 对真实有限正权支持可由 Boolean 代数闭合恢复 `R+1` 原子；对一般伪矩，共同交换条件和 `V2` localizer 仍是开放义务。

## 可访问材料

[共同匹配接口](../../../../current/unrelated_machines/joint_matching_completion_and_block_cuts.md)、[全局共同矩](../../../../current/unrelated_machines/global_assignment_moment_rounding.md)、[加权共同组联合槽](../../../../current/unrelated_machines/weighted_group_joint_slot_rounding.md)、[本轮开放义务与边界](../../../../questions/unrelated_machines/barrier_escape_obligations.md)、[路线整合审查](../../../../reviews/unrelated_machines/joint_capacity_route_feasibility_review.md)。精确审计脚本和冻结输出为 `lst_support_release_and_threshold_group.py` / `lst_support_release_and_threshold_group_audit.json`。成熟数学资产沿既有目录入库；这里仅记录读取入口和当前卡点。

## 当前状态

没有把任何尚未冻结的正面候选升级为定理。若本轮只得到条件性构造或精确反驳，将分别按其真实身份保存；若没有改变主目标认识，不制造新的共同资产。
