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

## B20-HOMOGENEOUS-SCREEN-v1

- **Exact statement/quantifiers:** 对每个原模型有限目录、任意正整数 m,r，若某个合法主题 B 是面对 r−1 个 B 时的末位最佳回复，则 K=max_T|T|=|B|，且 OPT_m≤[1+(m−1)/r]K。任意完整 m 人 SPE 均有 W≥K。因此 r≥m−1（m≥2）时，该目录所有 SPE 均满足 half。
- **Definitions/assumptions:** 假设等价于对每个 T 有 r|T\\B|+|T∩B|≤|B|；不要求实际路径使用 B 或在平局时选 B。m=1、空 B、零客户均单独核对，无零比率。
- **Source-plan version:** 完整计划仅根可能失去最优性、根最大真实后悔 Δ≥0 时 W+Δ≥K。因此 r=m−1 给 OPT−2W−3Δ≤−Δ，r=m 给更强的 −W/m−(1+1/m)Δ。仅代数界；原常数3编译器是既有依赖。
- **Dependencies/evidence:** 同质历史末位真实比较、最优覆盖联合的非重计求和、每位偏离最大主题的 K/m 保证。作者、root 和独立审查者分别重构；root 重放12个被冻结 source 计划的全部正深度比较，但一般引理由解析证明承担。
- **Status/scope:** 内部已核对的一般筛选组件；不主张新颖性/外审，也不解决不满足筛选的目录。没有重启受限目录正面扩张项目。
- **Files:** `construct/homogeneous_screen.md`、`independent_audit/review_homogeneous_catalogue_screen.md`；直接原目标 source 攻击代码与精确回放在 `construct/README.md` 索引。
