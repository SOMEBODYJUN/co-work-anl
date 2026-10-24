# 本轮精确身份与证据

原目标 `Q-CAG-HALF` 未改对象、量词、假设或结论，状态 **OPEN**。本文只是个人研究账本；不自动替代共享 canonical。

## B20-COVARIANCE-CLIENTWISE-NO-v1

- **Exact statement:** 不存在如下全输入推论：对每份完整历史依赖纯 SPE、每个真实节点、每个目录查询分布 p、每个 0<qₓ<1 的客户，均有 H⁰ₓ≤H¹ₓ；甚至更弱的逐客户 Cₓ≤Dₓ 也为假。
- **Objects/domain/definitions:** 原 CAG-MODEL，h_F(x) 为强制 F 后原策略真实终局中除当前位外的负载；Dₓ=E[1_(x∈F)/(h_F+1)]，Cₓ=E[qₓ/(1+cₓ)]。H⁰/H¹ 是 h_F+1 倒数在 F 不含/包含 x 时的条件均值。
- **Evidence/conclusion:** 两人四单位客户的完整策略有 H⁰ₓ=1、H¹ₓ=1/2、Cₓ−Dₓ=1/12；七客户版本全部规定行动唯一最优。
- **Dependencies:** 模型定义、全部五决策节点的20个含自身比较、Fraction 精确算术。
- **Status:** 精确辅助反例。四客户见证独立研究员先重构全部 IC 再核定义，root 重放两份独立代码；七客户版本作者程序与 root 手核严格比较。没有最小性、外审或新颖性认证。
- **Counterevidence/objection/scope:** 两例均 W=OPT；跨客户总 D−C>0，未否定 aggregate pushforward、自由 Mpath 或 half。只排除逐客户单调/非正债桥。
- **Files:** `covariance/customerwise_covariance_boundary.md`、`covariance/audit_customerwise_covariance.py`、`independent_audit/review_covariance_tiny.md`、`independent_audit/audit_covariance_tiny.py`。

## B20-POT-RESET-REP-v1

- **Exact statement:** 每个有限目录、每个完整纯策略、每个真实有序节点、同一分布独立 A,T，满足 D−C=R+J；R 按依次真实强制后继序列展开为 EΣΓⱼ+EΣEⱼ，最后删位重置 Eₙ=0。
- **Definitions/domain:** 非负整数过去负载 b；Φ_b=Σ(H_(b+c)−H_b)，R 是同根 A 下两个真实后继元组的联合势差期望，J 为共同客户额外插入折扣；详见工作稿。
- **Dependencies:** 调和势插入边际、iid 交换、有限望远镜求和。Γⱼ≥0 另需完整 SPE；恒等式不需均衡。
- **Status:** 一般表示，独立代数重构通过；不是新增全局不等式或一般 half 推进闭合。
- **Evidence/objections:** 旧34客户完整 SPE 已有 R=−11/82；本轮复算 Γ总=91/164、删位重置总=−113/164、J=40571/20172，恰满足全部恒等式。删位后的两个后继不能当成删位游戏里的 SPE。
- **Files:** `GENERAL_PROOF_WORKING.md`、`root_potential_regression.py`、`independent_audit/review_potential_reset_identities.md`；原实例共享 `examples/customer_attraction/individual_security_failure.json`。

## 未决候选分开记录

全 p 的 ΣᵢCᵢ(p)≤W 比自由路径菜单更强；只对额外槽安全最优 p 证明也足以 half。两种量词均未证。负样本搜索没有产生反例，不提升真值。动态 Theta 的同序预算、mixed-owner incoming-reset 与 H4 最优元组共同支付仍是各自独立的未决接口。
