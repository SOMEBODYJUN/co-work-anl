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

令 \(m\) 为提供者人数，\(S\) 为有限非空的共同主题目录。\(q\in\Delta(S)\) 是目录上的概率分布。对单位客户 \(x\)，\(q_x\) 是一次按 \(q\) 查询覆盖该客户的概率。连续接口及其对数势为

    q_A ≥ 0，Σ_{A∈S} q_A = 1，q_x = Σ_{A∋x} q_A
    g_A(q) = Σ_{x∈A} 1 / (1 + (m−1)q_x)
    v_cont = min_{q∈Δ(S)} max_{A∈S} g_A(q)
    L(q) = Σ_x log(1 + (m−1)q_x)

客户覆盖边际之和 \(\sum_x q_x=\sum_{A\in S}q_A|A|\)，即一次查询的期望覆盖人数。[恢复的连续安全值原稿](../../../../research/registration/evidence/register-lead-recovered-evidence-01/continuous_security_log_boundary.md)把最大化 \(L\) 作为代理问题。下面的分离族给出最大化 \(L\) 和最小化最坏目录收益的不同结果。

## 2. 连续对数势的精确分离族

源文给出 m ≥ 2 的单位客户族，主题可记作 0、1、2、3。客户类型及重数为：

* {1} 的客户 a = k + 3 个；
* {2} 的客户 a = k + 3 个；
* {3} 的客户 a = k + 3 个；
* {0,2,3} 的客户 d = 2k + 3 个；
* {0,1} 的客户 a = k + 3 个。

其中 \(k=m-1\)，总客户数为 \(4a+d=6m+9\)。在按主题 \(0,1,2,3\) 排列的分布 \(q^*=(0,1/3,1/3,1/3)\) 处，令 \(D=1+k/3=a/3\)、\(F=1+2k/3=d/3\)。有 \(g_0=g_2=g_3=a/D+d/F=6\)、\(g_1=2a/D=6\)。由于 \(\partial L/\partial q_A=kg_A\)，该点各偏导相等。由 \(L\) 的凹性及目录概率总和为一，\(q^*\) 全局最大化 \(L\)。

取 \(s=(3d+2a)/(4(d+2a))\)、\(\varepsilon=1/(4k)\)，则

\[
q'=(\varepsilon,\,1/3-s\varepsilon,\,1/3-(1-s)\varepsilon/2,\,1/3-(1-s)\varepsilon/2).
\]

由 \(2a-d=3\) 得 \(0<s<1/2\)，故 \(q'\) 是合法目录分布。对 \(g_0(q')\)，两个客户类型的分母均严格增大。对 \(g_1\) 与 \(g_2=g_3\)，通分后，小于 6 分别等价于

\[
\varepsilon<\frac{a}{4k(d+2a)s(1-s)},\qquad
\varepsilon<\frac{1}{8ks(1-s)}.
\]

通分用到 \(D(1-2s)/2=a/[4(d+2a)]\) 和 \(sD-(1-s)F/2=1/8\)。由 \(s(1-s)\le 1/4\) 及 \(2a>d\)，两界都严格大于 \(1/(4k)\)。因此每个 \(m\ge2\) 都有 \(v_{\rm cont}\le \max_A g_A(q')<6=\max_A g_A(q^*)\)。

`audit_continuous_log_boundary.py` 对 \(m=2,3,\ldots,30,50,100,1000\) 作 Fraction 回归。`continuous_log_audit.json` 记录这些有限代数检查和正的 `gap_below_log_KKT_value`。全称分离来自上面的不等式，适用范围是静态 minimax 与对数势两个目标。

## 3. 与静态桥的关系

continuous_security_log_boundary.md 同时给出客户不等式导出的粗桥：

    v_cont ≥ OPT_m / (2m − 1)

其中 \(\operatorname{OPT}_m\) 是 \(m\) 个主题所能覆盖的最大客户数。对任意合法 \(q\)，先有 \(\operatorname{OPT}_m\le (2m-1)\max_A g_A(q)\)，再对 \(q\) 取最小。要由此推出半覆盖，仍需独立证明完整历史 SPE 福利 \(W\) 的支付桥，例如 \(W\ge(m-1/2)v_{\rm cont}\)。

## 4. 笛卡尔目录耦合审查

cartesian_catalog_coupling.md 将客户划成互不重叠的两个组件，各组件有自己的目录，联合目录取笛卡尔积（客户仍只计入其喜欢的局部主题）。在静态问题和连续问题上，最优覆盖值及安全值按组件相加；若分别选择两个组件的完整 SPE，再按相同组件策略拼接，得到一个联合 SPE。这给出了一个可复用的“产品构造”充分方向。

反向分解不成立。源文的 exact 两玩家、8 客户例子给出一个跨组件惩罚相互耦合的完整历史纯 SPE：联合终局覆盖 W = 8，静态最优 OPT = 8，因而它不是半覆盖反例；但是把该策略投影到某一组件时可见一项大小为 1 的偏离收益。也就是说，联合完整历史中的跨组件平局和惩罚可以支撑每个玩家，即使各组件投影本身不是局部 SPE。任何“组件值相加，所以任意联合 SPE 可逐组件分析”的证明路线都被这个例子阻断。

[恢复的笛卡尔耦合原稿](../../../../research/registration/evidence/register-lead-recovered-evidence-01/cartesian_catalog_coupling.md)中，分量 I 的两个不交主题 \(A,B\) 分别有 3、2 名客户，分量 II 的 \(C,D\) 分别有 2、1 名客户。完整策略首选 \(BC\)，随后对 \(AC,AD,BC,BD\) 分别选 \(BC,BC,AD,AC\)。实际路径 \(BC\to AD\) 覆盖全部 8 名客户。把第二分量的首动作固定为 \(C\) 后，第一分量首选 \(B\) 得 2，改选 \(A\) 得 3。`audit_cartesian_coupling.py` 对这份策略的 5 个决策节点作 20 项整数或分数比较。

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
