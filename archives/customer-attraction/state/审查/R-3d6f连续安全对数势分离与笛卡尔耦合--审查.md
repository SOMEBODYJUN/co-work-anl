---
id: customer-attraction/r3d6f-continuous-log-separation-and-cartesian-coupling-review
kind: review
type_tag: 审查
title: R-3d6f 连续安全对数势分离与笛卡尔耦合审查
status: exact-static-boundary-and-cartesian-audit-reviewed
truth_status: representation-boundary-confirmed; no-Q-CAG-HALF-counterexample
review_level: source-comparison-with-exact-fraction-replays
scope: continuous security log potential, a finite exact separation family, and Cartesian catalog coupling with non-factorizing SPE
source_refs:
  - source:df2fd076ec0c4bd72a73:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/security_bridge/README.md
  - source:170e4369c7ad4983e666:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/security_bridge/audit_cartesian_coupling.py
  - source:4e87003baec5fb3596b7:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/security_bridge/audit_continuous_log_boundary.py
  - source:401225dff6c2fdf4d5bc:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/security_bridge/cartesian_catalog_coupling.md
  - source:cd3a78004dcc96236840:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/security_bridge/cartesian_coupling_audit.json
  - source:f626e7ebfe61a5830624:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/security_bridge/continuous_log_audit.json
  - source:f0b7d59c941dfce22f67:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/security_bridge/continuous_security_log_boundary.md
---

# R-3d6f 连续安全对数势分离与笛卡尔耦合审查

## 1. 对象与审查问题

这七个源围绕同一候选接口：把有限客户的静态安全值改写为连续查询向量 q 上的最坏目录值，再以对数势或笛卡尔积结构尝试证明 Q-CAG-HALF。审查逐个重读定义、量词、客户重数、最坏目录的取法和程序输出；其中两个 Python 程序只使用 Python 标准库 Fraction，JSON 是程序写出的 exact 回归，不是浮点求解器的结论。

连续接口的定义是：

    g_A(q) = Σ_{x∈A} 1 / (1 + (m−1)q_x)
    v_cont = min_{q∈Δ_m} max_A g_A(q)

这里 q_x ≥ 0 且 Σ_x q_x = 1，目录 A 的客户按其实际喜欢的主题取和。continuous_security_log_boundary.md 还研究对数势（按目录乘积的 log 和取极值）作为 q 的代理目标。该代理值与上述 minimax 定义必须分开保留；前者的 KKT 点不自动给出后者的最优查询。

## 2. 连续对数势的精确分离族

源文给出 m ≥ 2 的单位客户族，主题可记作 0、1、2、3。客户类型及重数为：

* {1} 的客户 a = k + 3 个；
* {2} 的客户 a = k + 3 个；
* {3} 的客户 a = k + 3 个；
* {0,2,3} 的客户 d = 2k + 3 个；
* {0,1} 的客户 d = 2k + 3 个；

其中 k = m − 1，总客户数为 6m + 9。在对数势的平衡点，q* = (0, 1/3, 1/3, 1/3)（其余主题按零质量理解）使四个目录代表值均为 6。源程序对 m = 2, 3, …, 30, 50, 100, 1000 用有理数逐项代入，并检查该点满足对数势的临界关系。

同一程序在一个保持 Σ_x q_x = 1 的扰动 q' 上精确比较四个 g_A，验证四个值都严格低于 6；因此该对数势平衡点不是连续 minimax 的最小化点。这个结论只证明“对数势代理”和“最坏目录 minimax”在该族上分离，未证明 v_cont 的全局闭式，也未给出任何完整历史 SPE。

audit_continuous_log_boundary.py 的回归覆盖上述整数 m 列表，所有分数相等性和严格不等式均由 Fraction 验证；continuous_log_audit.json 的字段只记录这些 exact 代数检查及正的 gap_below_log_KKT_value。因此该族可以作为后续证明中的表示边界/障碍对象，不能升级成半覆盖率反例。

## 3. 与静态桥的关系

continuous_security_log_boundary.md 同时给出客户不等式导出的粗桥：

    v_cont ≥ OPT / (2m − 1)

其中 m 是主题数。这个不等式的量词是对任意合法 q 的连续目录上界，再取最小；它没有把对数势 KKT 点替换成 v_cont，也没有把静态安全值、终局客户均分值和 SPE 约束混为同一对象。要得到目标的半覆盖结论，仍需独立证明实际完整历史 SPE 的 W 与真实 v_cont（或静态安全值）之间的强桥，例如全局的 W ≥ (m − 1/2) v_cont。本批源没有提供该桥，也没有找到 W < OPT/2 的纯 SPE。

## 4. 笛卡尔目录耦合审查

cartesian_catalog_coupling.md 将客户划成互不重叠的两个组件，各组件有自己的目录，联合目录取笛卡尔积（客户仍只计入其喜欢的局部主题）。在静态问题和连续问题上，最优覆盖值及安全值按组件相加；若分别选择两个组件的完整 SPE，再按相同组件策略拼接，得到一个联合 SPE。这给出了一个可复用的“产品构造”充分方向。

反向分解不成立。源文的 exact 两玩家、8 客户例子给出一个跨组件惩罚相互耦合的完整历史纯 SPE：联合终局覆盖 W = 8，静态最优 OPT = 8，因而它不是半覆盖反例；但是把该策略投影到某一组件时可见一项大小为 1 的偏离收益。也就是说，联合完整历史中的跨组件平局和惩罚可以支撑每个玩家，即使各组件投影本身不是局部 SPE。任何“组件值相加，所以任意联合 SPE 可逐组件分析”的证明路线都被这个例子阻断。

audit_cartesian_coupling.py 枚举 5 个决策节点和 20 个精确比较，全部用整数/分数重算，报告组件参数 (2, 1)、联合 W = 8、OPT = 8，以及投影偏离改善 1；cartesian_coupling_audit.json 与程序输出一致。该审计只检验指定有限策略和投影现象，不声称枚举所有联合 SPE，也不声称笛卡尔构造下不存在更低福利的联合均衡。

## 5. 与已有正文的去重与衔接

这七源的独有内容是：

1. 以定义级 exact 公式明确区分连续最坏目录 minimax 与对数势代理，并给出任意 m ≥ 2 的分离族；
2. 用有理数回归覆盖 m = 2..30、50、100、1000，把有限计算结果限定为公式核验，而非优化器全局证明；
3. 给出笛卡尔目录的可拼接充分构造和一个非分解联合完整 SPE 的 exact 审计，阻断“任意联合 SPE 自动分解”的量词跳步。

它们不重复此前 R-3d6f 分数负载弱桥的 m² + 1 家族，也不替换既有的实际前缀、查询行或静态组件对象。尤其不能把“连续对数势不是 minimax”直接转译为“原六人模型不存在半覆盖保证”，因为中间还缺少从 SPE 终局到连续/静态安全值的正确不等式和完整历史量词。

## 6. 结论、缺口与后续使用

**已确认。** 对数势 KKT 目标与连续 minimax 在给定客户族上严格分离；笛卡尔产品可由局部 SPE 构造联合 SPE，但联合 SPE 不必分解，且 exact 小例的 W 仍等于 OPT。

**有限实验。** 两个审计程序及两个 JSON 报告是 exact 有限回归，证据覆盖了列出的 m 和指定的 8 客户策略。

**障碍。** 不能使用对数势最优点替代 v_cont，不能以组件投影的偏离改善否定联合 SPE，也不能把粗桥 v_cont ≥ OPT/(2m − 1) 反向使用为半覆盖定理。

**未决。** 仍需在当前六提供者、完整有序历史和任意平局保留的模型中，证明或反驳 W ≥ OPT/2。若采用连续查询或笛卡尔分解，后续必须显式给出：客户类型的定义域与重数、所有目录上的最坏量词、完整历史偏离证人，以及整数/exact 的全局最优性证据。
