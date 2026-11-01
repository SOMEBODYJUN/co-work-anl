# 比较与处置说明

## 与既有正文的关系

本批 20 个源属于 R-21674 工作区。既有《六人协调前沿与逐人缺口探索的范围证据》只保留了 R-216 入口的历史范围、早期缺失 blob 的谨慎边界以及五人/七极大等已存在对象；它没有代替本批冻结源的逐文件阅读。新正文把本批实际取回的 JSON、Python 和 workspace metadata 接入，并把原“候选/有限运行/缺口”分开。

## 独有内容

1. `audit_three_profit_opportunity.py`、`three_profit_opportunity_audit.json` 和 `profit_endpoint_certificate.json` 共同给出固定恰三余提供者、固定合法背景的 `F_3(p)-R <= 3 u_first` 证书接口：4096 个状态、12288 个系数、公共分母 544124，最小系数为 0；独立重放在分母截断 10^6 时也得到零负 slack。该对象是三余利润机会证书，不是六人覆盖定理。
2. branch/tax/price/three-endpoint 和 opportunity-coeff 探针实际暴露了统一乘子方案的有限边界：不同 n、k、tau 和 cover/profit 目标会直接 infeasible；这保留了可继续证明的障碍，不能把某个可行点升级为一般式。
3. `gram_probe` 的条件平方切面在第18次达到零负核，但其目标约1.5、输入是固定三人六主题策略锥，不是真实客户共同矩；因此只接入为有限 Gram 资源。
4. `gap_m3p6i0`、`gap_m4p5i1` 是 HiGHS 45 秒时间限制的数值 MILP；`structured_gap_m5p7` 给出一个已精确重建的 W=5、OPT=9、utility=1 候选，并报告 universal_result=false；这些是候选/障碍，不是全历史纯 SPE 反例。`prefix_cut_benchmark.py` 与 `structured_gap_attack.py` 依赖其他工作区模块，本文没有伪造缺依赖运行。
5. `workspace.json` 只含 schema/save/actor/instance 元数据，无数学内容。

## 统一边界

- 读到的所有收益、根序列、枚举范围、优化状态和退出码均按源记录；超时的 incumbent、浮点切面、LP 可行性和一项 exact certificate 分开标记。
- “three-remaining first-player profit opportunity” 的证书依赖代码中固定的枚举状态和收益行；即使接受其 `p` 的二次分式系数核，也不能推出任意背景、任意人数或六人 `OPT >= 2W`。
- R-216 的 Gram JSON 只说明旧局部交集矩搜索与负核消除过程；没有真实非负客户质量、完整菜单或 SPE 认证，不得替代 Q-CAG-HALF 的客户实例。
- 本批未发现新的严格全局 half 反例或全局证明。Q-CAG-HALF 继续 OPEN。
